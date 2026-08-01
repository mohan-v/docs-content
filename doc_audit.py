#!/usr/bin/env python3
"""Audits the docs-content repository for common quality issues.

Usage:
  python3 doc_audit.py                        # full repo audit → audit_report.md
  python3 doc_audit.py path/to/file.md [...]   # audit only the given file(s)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent
CONTENT_EXTENSIONS = {".md", ".adoc"}
# Directories to skip entirely
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".claude", ".venv", "raw-migrated-files"}


def iter_dirs_and_files():
    """Walk the repo, yielding (dirpath, files) while skipping ignored dirs."""
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        yield Path(root), files


def iter_target_md_files(files=None):
    """Yield absolute Paths to .md files to check — either the given files or a full walk."""
    if files is not None:
        yield from (f for f in files if f.suffix == ".md")
        return
    for dirpath, filenames in iter_dirs_and_files():
        for fname in filenames:
            if fname.endswith(".md"):
                yield dirpath / fname


# ---------------------------------------------------------------------------
# Check 1: Empty or near-empty .md files (<5 lines of real content)
# Returns three lists: (full_pages, snippets, redirect_stubs)
# ---------------------------------------------------------------------------

_REDIRECT_RE = re.compile(r"This page has moved|^Refer to\b", re.IGNORECASE | re.MULTILINE)


def find_thin_md_files(files=None):
    full_pages = []
    snippets = []
    redirect_stubs = []

    for fpath in iter_target_md_files(files):
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Strip frontmatter block
        body = re.sub(r"^\s*---.*?---\s*", "", text, count=1, flags=re.DOTALL)
        real_lines = [l for l in body.splitlines() if l.strip()]
        if len(real_lines) >= 5:
            continue

        rel = str(fpath.relative_to(REPO_ROOT))
        count = len(real_lines)

        if _REDIRECT_RE.search(body):
            redirect_stubs.append((rel, count))
        elif "/_snippets/" in rel or rel.startswith("_snippets/"):
            snippets.append((rel, count))
        else:
            full_pages.append((rel, count))

    full_pages.sort(key=lambda x: x[1])
    snippets.sort(key=lambda x: x[1])
    redirect_stubs.sort(key=lambda x: x[1])
    return full_pages, snippets, redirect_stubs


# ---------------------------------------------------------------------------
# Check 2: .adoc files mixed in with .md files
# ---------------------------------------------------------------------------

def find_mixed_format_dirs(files=None):
    # Directory-level check — not meaningful when scoped to specific files.
    if files is not None:
        return []
    results = []
    for dirpath, dir_files in iter_dirs_and_files():
        has_md = any(f.endswith(".md") for f in dir_files)
        has_adoc = any(f.endswith(".adoc") for f in dir_files)
        if has_md and has_adoc:
            rel = dirpath.relative_to(REPO_ROOT)
            adoc_files = [f for f in dir_files if f.endswith(".adoc")]
            results.append((str(rel) or ".", adoc_files))
    return sorted(results)


# ---------------------------------------------------------------------------
# Check 3: Duplicate frontmatter keys in .md files
# ---------------------------------------------------------------------------

def find_duplicate_frontmatter_keys(files=None):
    results = []
    for fpath in iter_target_md_files(files):
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = re.match(r"^\s*---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            continue
        fm_block = m.group(1)
        # Collect top-level keys (lines that start without indentation)
        keys = [
            line.split(":")[0].strip()
            for line in fm_block.splitlines()
            if line and not line.startswith(" ") and ":" in line
        ]
        seen = set()
        dupes = []
        for k in keys:
            if k in seen:
                dupes.append(k)
            seen.add(k)
        if dupes:
            rel = fpath.relative_to(REPO_ROOT)
            results.append((str(rel), dupes))
    return sorted(results)


# ---------------------------------------------------------------------------
# Check 4: Folders with no content files
# ---------------------------------------------------------------------------

def find_empty_dirs(files=None):
    # Directory-level check — not meaningful when scoped to specific files.
    if files is not None:
        return []
    results = []
    for dirpath, dir_files in iter_dirs_and_files():
        if dirpath == REPO_ROOT:
            continue
        has_content = any(
            Path(dirpath / f).suffix in CONTENT_EXTENSIONS for f in dir_files
        )
        if not has_content:
            rel = dirpath.relative_to(REPO_ROOT)
            results.append(str(rel))
    return sorted(results)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def section(title, lines):
    bar = "-" * len(title)
    return f"## {title}\n\n" + ("\n".join(lines) if lines else "_None found._") + "\n"


def build_report(full_pages, snippets, redirect_stubs, mixed, dupes, empty, scope, is_scoped=False):
    parts = ["# Documentation Audit Report\n"]
    parts.append(f"**{scope}**\n")
    if is_scoped:
        parts.append(
            "> Directory-level checks (mixed .md/.adoc, empty folders) are "
            "skipped for file-scoped audits.\n"
        )

    # Summary table
    parts.append("## Summary\n")
    parts.append("| Check | Issues found |")
    parts.append("|---|---|")
    parts.append(f"| Thin full-page .md files (<5 content lines) | {len(full_pages)} |")
    parts.append(f"| Thin snippet files (<5 content lines) | {len(snippets)} |")
    parts.append(f"| Redirect stubs (thin, intentional) | {len(redirect_stubs)} |")
    parts.append(f"| Directories with mixed .md/.adoc | {len(mixed)} |")
    parts.append(f"| .md files with duplicate frontmatter keys | {len(dupes)} |")
    parts.append(f"| Folders with no content files | {len(empty)} |")
    parts.append("")

    # Check 1a — full pages (potentially problematic)
    lines = [f"- `{path}` ({count} line{'s' if count != 1 else ''})" for path, count in full_pages]
    parts.append(section("Thin full-page .md files (< 5 lines of content)", lines))

    # Check 1b — snippets (low priority, collapsed via HTML details)
    snip_lines = [f"- `{path}` ({count} line{'s' if count != 1 else ''})" for path, count in snippets]
    snip_body = "\n".join(snip_lines) if snip_lines else "_None found._"
    parts.append(
        "## Thin snippet files (intentionally short, low priority)\n\n"
        "<details>\n<summary>Show all snippet files</summary>\n\n"
        + snip_body + "\n\n</details>\n"
    )

    # Check 1c — redirect stubs (excluded from warnings)
    lines = [f"- `{path}` ({count} line{'s' if count != 1 else ''})" for path, count in redirect_stubs]
    parts.append(section("Redirect stubs (thin but intentional — excluded from warnings)", lines))

    # Check 2
    lines = []
    for dname, adoc_files in mixed:
        files_str = ", ".join(f"`{f}`" for f in adoc_files)
        lines.append(f"- `{dname}/` — .adoc files: {files_str}")
    parts.append(section("Directories with mixed .md and .adoc files", lines))

    # Check 3
    lines = [f"- `{path}` — duplicate keys: {', '.join(f'`{k}`' for k in keys)}" for path, keys in dupes]
    parts.append(section(".md files with duplicate frontmatter keys", lines))

    # Check 4
    lines = [f"- `{d}/`" for d in empty]
    parts.append(section("Folders with no content files", lines))

    return "\n".join(parts) + "\n"


def _validate_files(paths: list[Path]) -> None:
    """Validate every path exists and is a .md file before any work starts."""
    errors = []
    for p in paths:
        if not p.exists():
            errors.append(f"not found: {p}")
        elif p.suffix != ".md":
            errors.append(f"not a .md file: {p}")
    if errors:
        print("error: invalid file argument(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(2)


def _scope_line(files: list[Path] | None) -> str:
    """Build a human-readable 'Scope: ...' line describing what was audited."""
    if not files:
        return "Scope: full repo"
    rels = []
    for f in files:
        try:
            rels.append(str(f.relative_to(REPO_ROOT)))
        except ValueError:
            rels.append(str(f))
    n = len(rels)
    return f"Scope: {n} file{'s' if n != 1 else ''} (" + ", ".join(rels) + ")"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Audits the docs-content repository for common quality issues."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific .md file(s) to audit. If omitted, audits the full repo.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    files = None
    if args.files:
        files = [f if f.is_absolute() else Path.cwd() / f for f in args.files]
        _validate_files(files)

    scope = _scope_line(files)
    print("Running doc audit…")
    print(scope)

    print("  Checking for thin .md files…")
    full_pages, snippets, redirect_stubs = find_thin_md_files(files)
    print(f"    Full pages: {len(full_pages)}, snippets: {len(snippets)}, redirect stubs: {len(redirect_stubs)}")

    print("  Checking for mixed .md/.adoc directories…")
    mixed = find_mixed_format_dirs(files)
    print(f"    Found {len(mixed)}")

    print("  Checking for duplicate frontmatter keys…")
    dupes = find_duplicate_frontmatter_keys(files)
    print(f"    Found {len(dupes)}")

    print("  Checking for empty directories…")
    empty = find_empty_dirs(files)
    print(f"    Found {len(empty)}")

    report = build_report(full_pages, snippets, redirect_stubs, mixed, dupes, empty, scope, is_scoped=files is not None)
    out_path = REPO_ROOT / "audit_report.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
