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
7. Commit the change:
   `git add <changed-file>`
   `git commit -m "docs: <one-line summary> per <TICKET-ID>"`
8. Push to current branch:
   `git push origin HEAD`
9. Open a PR using gh CLI:
   `gh pr create --base nvanmane-1 --title "docs: <summary> per <TICKET-ID>" --body "<pr-description>"`
10. Share the PR URL with the writer

## Notes
- Step 1 always creates a fresh branch off nvanmane-1, named
  docs/<TICKET-ID> — never commits directly to nvanmane-1 or reuses
  a leftover branch from a prior run
- Always use the PR description from step 6 as the --body content
- Branches are created from nvanmane-1, and PRs target nvanmane-1 —
  not main
- If gh pr create fails, stop and report the error — do not retry