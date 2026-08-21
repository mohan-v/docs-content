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

1. Create a working branch:
   - `git checkout nvanmane-1`
   - `git pull origin nvanmane-1`
   - `git checkout -b docs/<TICKET-ID>`
   - If a branch named `docs/<TICKET-ID>` already exists locally or on
     the remote, stop and report the conflict — do not force-overwrite
     or reuse it
2. Read the ticket via Atlassian MCP
3. Find the correct file in the repo
4. Make the documented change
5. Run `python3 style_checker.py <changed-file>`
   - If violations found, fix them and re-run until clean
6. Run `tasks/pr-description-generator.md` scoped to this change
7. Show the final `git diff` for writer review

## Notes
- Branches are created from nvanmane-1, named docs/<TICKET-ID> —
  never commit directly to nvanmane-1 or reuse a leftover branch
  from a prior run
- PRs (where applicable) target nvanmane-1 — not main

## Stop here — do not commit or push
Wait for the writer to review the diff and PR description.
The writer will run git add/commit/push when ready.