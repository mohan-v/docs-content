# Task: JIRA → Doc → PR Description (Manual PR)

## Purpose
Read a JIRA ticket, make the documented change, run quality checks,
and prepare everything for a PR — stopping before commit so the
writer can review and decide.

## When to use
- New or complex content changes
- Sensitive sections (security, compliance, breaking changes)
- Any time you want to review the diff before it goes anywhere

## Instructions for Claude Code

Given a JIRA ticket ID:

1. Read the ticket via Atlassian MCP
2. Find the correct file in the repo
3. Make the documented change
4. Run `python3 style_checker.py <changed-file>`
   - If violations found, fix them and re-run until clean
5. Run `tasks/pr-description-generator.md` scoped to this change
6. Show the final `git diff` for writer review

## Stop here — do not commit or push
Wait for the writer to review the diff and PR description.
The writer will run git add/commit/push when ready.