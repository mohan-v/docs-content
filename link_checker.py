#!/usr/bin/env python3
"""Scans .md files for broken internal links and writes link_report.md.

Usage:
  python3 link_checker.py                        # full repo scan → link_report.md
  python3 link_checker.py path/to/file.md [...]   # scan only the given file(s)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".claude", ".venv", "raw-migrated-files"}

# Regex captures the link target from both [text](target) and ![alt](target)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def iter_md_files(files=None):
    if files is not None:
        yield from (f for f in files if f.suffix == ".md")
        return
    for root, dirs, filenames in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".md"):
                yield Path(root) / fname


def parse_links(text: str):
    """Return all link targets found in the text."""
    return LINK_RE.findall(text)


def classify(target: str, source_file: Path):
    """
    Returns (resolved_path_or_None, skip_reason_or_None).
    skip_reason is set for links that should not be checked.
    """
    raw = target.strip()

    # Strip inline title: [text](path "title") -> path
    raw = re.sub(r'\s+"[^"]*"$', "", raw).strip()

    # Skip pure anchors
    if raw.startswith("#"):
        return None, "anchor-only"

    # Skip external URLs
    if re.match(r"https?://|mailto:", raw, re.IGNORECASE):
        return None, "external"

    # Skip cross-repo links (e.g. elasticsearch://, elastic-agent://, opentelemetry://)
    if re.search(r"[a-z]://", raw):
        return None, "cross-repo"

    # Skip substitution variables — resolved to URLs at build time via docset.yml subs:
    if "{{" in raw:
        return None, "substitution-var"

    # Skip placeholder/example paths used in documentation examples
    if "..." in raw or raw in ("/absolute/file.md", "/path/to/file.md"):
        return None, "example-placeholder"

    # Strip anchor fragment
    path_part = raw.split("#")[0].strip()
    if not path_part:
        return None, "anchor-only"

    # Only check links that target .md files or have no extension (directory index)
    suffix = Path(path_part).suffix
    if suffix and suffix not in {".md", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf"}:
        return None, "non-doc-file"

    if path_part.startswith("/"):
        resolved = REPO_ROOT / path_part.lstrip("/")
    else:
        resolved = source_file.parent / path_part

    resolved = resolved.resolve()
    return resolved, None


def check_links(files=None):
    """Returns {source_file: [(raw_target, resolved_path), ...]}."""
    broken = defaultdict(list)

    for md_file in iter_md_files(files):
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for target in parse_links(text):
            resolved, skip_reason = classify(target, md_file)
            if skip_reason:
                continue
            if not resolved.exists():
                rel_source = md_file.relative_to(REPO_ROOT)
                broken[str(rel_source)].append((target.split("#")[0].strip(), str(resolved.relative_to(REPO_ROOT))))

    return broken


def build_report(broken: dict, scope: str) -> str:
    total = sum(len(v) for v in broken.values())
    lines = ["# Internal Link Check Report\n"]
    lines.append(f"**{scope}**\n")

    lines.append("## Summary\n")
    lines.append(f"- Files with broken links: **{len(broken)}**")
    lines.append(f"- Total broken links: **{total}**")
    lines.append("")
    lines.append("> Cross-repo links (`elasticsearch://`, `elastic-agent://`, etc.) and external URLs are excluded.\n")

    if not broken:
        lines.append("_No broken internal links found._\n")
        return "\n".join(lines)

    lines.append("## Broken links\n")
    for source in sorted(broken):
        lines.append(f"### `{source}`\n")
        lines.append("| Link target | Resolved path (missing) |")
        lines.append("|---|---|")
        seen = set()
        for raw_target, resolved in sorted(broken[source]):
            key = (raw_target, resolved)
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"| `{raw_target}` | `{resolved}` |")
        lines.append("")

    return "\n".join(lines) + "\n"


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
    """Build a human-readable 'Scope: ...' line describing what was scanned."""
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
        description="Scans .md files for broken internal links."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific .md file(s) to scan. If omitted, scans the full repo.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    files = None
    if args.files:
        files = [f if f.is_absolute() else Path.cwd() / f for f in args.files]
        _validate_files(files)

    scope = _scope_line(files)
    print("Scanning for broken internal links…")
    print(scope)
    broken = check_links(files)

    total = sum(len(v) for v in broken.values())
    print(f"  Files with broken links: {len(broken)}")
    print(f"  Total broken links:      {total}")

    report = build_report(broken, scope)
    out = REPO_ROOT / "link_report.md"
    out.write_text(report, encoding="utf-8")
    print(f"\nReport written to {out}")


if __name__ == "__main__":
    main()
