# Task: JIRA → Doc → Auto PR (Full Automation)

## Purpose
Read a JIRA ticket, make the change, run quality checks, commit,
push, and open a PR automatically.

## When to use
- Simple, contained fixes (typos, word changes, broken links)
- Style cleanup on a single file
- Changes where the diff will be minimal and low-risk

## Do NOT use for
- New content pages
- Breaking change documentation
- Security or compliance sections
- Any change touching more than 3 files

## Instructions for Claude Code

Given a JIRA ticket ID:

1. Read the ticket via Atlassian MCP
2. Find the correct file in the repo
3. Make the documented change
4. Run `python3 style_checker.py <changed-file>`
   - If violations found, fix them and re-run until clean
5. Run `tasks/pr-description-generator.md` scoped to this change
6. Commit the change:
   `git add <changed-file>`
   `git commit -m "docs: <one-line summary> per <TICKET-ID>"`
7. Push to current branch:
   `git push origin HEAD`
8. Open a PR using gh CLI:
   `gh pr create --base main --title "docs: <summary> per <TICKET-ID>" --body "<pr-description>"`
9. Share the PR URL with the writer

## Notes
- Always use the PR description from step 5 as the --body content
- Target base: main (your fork's main)
- If gh pr create fails, stop and report the error — do not retry