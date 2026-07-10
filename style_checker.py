#!/usr/bin/env python3
"""Checks .md files for Elastic style guide violations and writes style_report.md.

Usage:
  python3 style_checker.py              # full repo scan → style_report.md
  python3 style_checker.py path/to/file.md  # single-file check → stdout
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent

# Generated report files that must never be scanned (they contain violations as examples)
SKIP_FILES = {"style_report.md", "audit_report.md", "link_report.md"}

# Directories to skip entirely
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".claude", ".venv",
    "raw-migrated-files", "learning-rag",
    # contribute-docs intentionally uses forbidden terms as examples
    "contribute-docs",
    # internal tooling/config — not published docs content
    ".cursor", ".github",
}

# ---------------------------------------------------------------------------
# Rules — each is (rule_id, description, pattern, get_fix_fn)
# pattern is compiled with re.IGNORECASE
# get_fix_fn(match) -> suggested fix string
# ---------------------------------------------------------------------------

def _fix_click(m):
    word = m.group(0)
    return word.lower().replace("click", "select").replace("tap", "select")

def _fix_list(m):
    word = m.group(0).lower()
    return "allowlist" if "white" in word else "denylist"

RULES = [
    (
        "device-agnostic",
        "Use 'select' instead of 'click' or 'tap'",
        re.compile(r"\b(click(?:s|ed|ing)?|tap(?:s|ped|ping)?)\b", re.IGNORECASE),
        lambda m: m.group(0).lower()
            .replace("clicking", "selecting").replace("clicked", "selected")
            .replace("clicks", "selects").replace("click", "select")
            .replace("tapping", "selecting").replace("tapped", "selected")
            .replace("taps", "selects").replace("tap", "select"),
    ),
    (
        "inclusive-language",
        "Use 'allowlist'/'denylist' instead of 'whitelist'/'blacklist'",
        re.compile(r"\b(white(?:list(?:s|ed|ing)?)|black(?:list(?:s|ed|ing)?))\b", re.IGNORECASE),
        _fix_list,
    ),
    (
        "filler-words",
        "Avoid filler words that don't add value",
        re.compile(r"\b(please|just|simply|easily)\b", re.IGNORECASE),
        lambda m: f"[remove '{m.group(0)}']",
    ),
    (
        "no-latin",
        "Avoid Latin abbreviations — use plain English",
        re.compile(r"\be\.g\.|i\.e\.|etc\.\b", re.IGNORECASE),
        lambda m: {
            "e.g.": "for example",
            "i.e.": "that is",
            "etc.": "and so on",
        }.get(m.group(0).lower(), "rephrase"),
    ),
    (
        "version-comparisons",
        "Use 'later'/'earlier' for versions, not 'newer'/'older'/'higher'/'lower'",
        re.compile(
            r"\b(newer|older)\b"                                    # always flag
            r"|\b(higher|lower)\b(?=\s+(?:version|release|than))"  # only in version context
            r"|(?<=(?:version|release)\s)\b(higher|lower)\b",
            re.IGNORECASE,
        ),
        lambda m: {
            "newer": "later", "older": "earlier",
            "higher": "later", "lower": "earlier",
        }.get(m.group(0).lower(), "later/earlier"),
    ),
]


# ---------------------------------------------------------------------------
# Text parsing helpers
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`]+`")


def iter_content_lines(text: str):
    """
    Yield (line_number, line_text) for lines that are NOT inside:
    - YAML frontmatter (opening --- block)
    - Fenced code blocks (``` or ~~~)
    Inline code within a line is stripped before yielding.
    """
    lines = text.splitlines()
    in_frontmatter = False
    frontmatter_done = False
    in_fence = False

    for lineno, line in enumerate(lines, start=1):
        # --- Frontmatter handling ---
        stripped = line.strip()
        if lineno == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
                frontmatter_done = True
            continue

        # --- Code fence handling ---
        if FENCE_RE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Strip inline code so we don't flag terms inside backticks
        clean = INLINE_CODE_RE.sub("", line)
        yield lineno, clean


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

Violation = tuple  # (rule_id, description, lineno, matched_text, fix)


def check_file(path: Path) -> list[Violation]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    violations = []
    for lineno, line in iter_content_lines(text):
        for rule_id, description, pattern, get_fix in RULES:
            for m in pattern.finditer(line):
                violations.append((rule_id, description, lineno, m.group(0), get_fix(m)))
    return violations


def scan_repo():
    results = defaultdict(list)  # rel_path -> [Violation, ...]
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md") or fname in SKIP_FILES:
                continue
            fpath = Path(root) / fname
            violations = check_file(fpath)
            if violations:
                rel = str(fpath.relative_to(REPO_ROOT))
                results[rel] = violations
    return results


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

RULE_DESCRIPTIONS = {r[0]: r[1] for r in RULES}


def build_report(results: dict) -> str:
    total = sum(len(v) for v in results.values())

    # Count per rule
    rule_counts = defaultdict(int)
    for violations in results.values():
        for v in violations:
            rule_counts[v[0]] += 1

    lines = ["# Style Check Report\n"]

    lines.append("## Summary\n")
    lines.append(f"- Files with violations: **{len(results)}**")
    lines.append(f"- Total violations: **{total}**")
    lines.append("")
    lines.append("> `contribute-docs/` is excluded — it documents forbidden terms intentionally.")
    lines.append("")
    lines.append("| Rule | Violations |")
    lines.append("|---|---|")
    for rule_id, count in sorted(rule_counts.items(), key=lambda x: -x[1]):
        desc = RULE_DESCRIPTIONS.get(rule_id, rule_id)
        lines.append(f"| `{rule_id}` — {desc} | {count} |")
    lines.append("")

    lines.append("## Violations by file\n")
    for rel_path in sorted(results):
        violations = results[rel_path]
        lines.append(f"### `{rel_path}`\n")
        lines.append("| Line | Rule | Found | Fix |")
        lines.append("|---|---|---|---|")
        for rule_id, _desc, lineno, matched, fix in sorted(violations, key=lambda x: x[2]):
            lines.append(f"| {lineno} | `{rule_id}` | `{matched}` | {fix} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def check_single_file_stdout(path: Path) -> int:
    """Check one file and print violations to stdout. Returns violation count."""
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    if not path.suffix == ".md":
        print(f"error: not a .md file: {path}", file=sys.stderr)
        sys.exit(2)

    violations = check_file(path)
    if not violations:
        print(f"OK  {path}  (no violations)")
        return 0

    rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
    print(f"{rel}: {len(violations)} violation(s)")
    for rule_id, _desc, lineno, matched, fix in sorted(violations, key=lambda x: x[2]):
        print(f"  Line {lineno:4d}  [{rule_id}]  '{matched}'  →  {fix}")
    return len(violations)


def main():
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if not target.is_absolute():
            target = Path.cwd() / target
        count = check_single_file_stdout(target)
        sys.exit(1 if count else 0)

    print("Scanning for style violations…")
    results = scan_repo()

    total = sum(len(v) for v in results.values())
    print(f"  Files with violations: {len(results)}")
    print(f"  Total violations:      {total}")

    report = build_report(results)
    out = REPO_ROOT / "style_report.md"
    out.write_text(report, encoding="utf-8")
    print(f"\nReport written to {out}")


if __name__ == "__main__":
    main()
