# Task: PR-Scoped Documentation Review

## Purpose
Run documentation quality checks against only the files changed
in the current PR or branch. Produces focused, actionable feedback
rather than a full repo audit.

## When to use
- As part of a PR review workflow
- When you want feedback on specific files you've edited
- Called automatically from GitHub Actions on PR events

## Difference from parallel-doc-review.md
- parallel-doc-review.md → scans entire repo (use before releases,
  on a schedule, or for full health checks)
- pr-doc-review.md → scans only changed files (use per PR)

## Instructions for Claude Code

### Step 1 — Get changed files
Run: git diff --name-only origin/main...HEAD -- '*.md'

If that returns nothing (e.g. on a fresh branch), fall back to:
git diff --name-only HEAD~1 -- '*.md'

Exclude from results:
- Files in raw-migrated-files/
- Files in learning-rag/
- Files in _snippets/ (intentionally short)

### Step 2 — Run checks on changed files only

For each changed .md file:

1. style_checker.py <file> — flag violations
2. link_checker.py output (link_report.md) — grep for this filename
3. doc_audit.py output (audit_report.md) — grep for this filename

Note: doc_audit.py and link_checker.py scan the full repo but write
file-specific results. Run them first if reports don't exist, then
grep for the changed files.

### Step 3 — Produce a focused report

Format:

## PR Doc Review — [date]
### Files reviewed
[list of changed .md files]

### Per-file findings
For each file:
**[filename]**
- Style: [violations or "clean"]
- Links: [broken links or "clean"]
- Audit: [thin page / frontmatter issues or "clean"]

### Summary
- Files reviewed: N
- Files with issues: N
- Critical (fix before merge): [list]
- Minor (can follow up): [list]

### Verdict
READY TO MERGE / NEEDS FIXES BEFORE MERGE