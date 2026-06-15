# Task: Parallel Documentation Review

## Purpose
Run a full documentation health check across the repository using three
independent tools in parallel. Synthesize results into a prioritized report.

## When to run
- Before a major release
- After a large content migration
- On a scheduled weekly basis (e.g. via GitHub Actions)
- On demand by any team member

## Instructions for Claude Code

Run the following three tools concurrently as parallel subagents:

### Subagent 1 — Content audit
python3 doc_audit.py
Collect all output. Note: reports thin pages, duplicate frontmatter,
and empty directories.

### Subagent 2 — Link check
python3 link_checker.py
Collect all output. Triage results into: real broken links, unfilled
template placeholders, and likely false positives.

### Subagent 3 — Style check
python3 style_checker.py
Collect all output. Group violations by rule type and count per category.

## Output format

Once all three subagents complete, produce a report with:

1. **Summary table** — check type × issue count
2. **Top 3 critical issues** — with file names and specific fix actions
3. **Recommended fix order** — separated into:
   - This week (low effort, high impact)
   - Next sprint (content review)
   - Ongoing (style cleanup)

## Notes
- Tools are run from repo root with no file arguments (full repo scan)
- style_checker.py accepts an optional file argument for targeted runs
- False positives in link_checker.py are common in NLP example files
