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
2. Create a working branch:
   - `git checkout main`
   - `git pull origin main`
   - Derive a branch name: `<ticket-id-lowercase>-<slug>`, where
     `<slug>` is a short kebab-case version of the one-line change
     summary (e.g. `testmcp-2-replace-powerful-with-strong`)
   - `git checkout -b <branch-name>`
   - If the branch already exists locally or on the remote, stop and
     report it — do not force-overwrite an existing branch
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
   `gh pr create --base main --title "docs: <summary> per <TICKET-ID>" --body "<pr-description>"`
10. Share the PR URL with the writer

## Notes
- Step 2 always creates a fresh branch off main — never commits
  directly to main or reuses a leftover branch from a prior run
- Always use the PR description from step 6 as the --body content
- Target base: main (your fork's main)
- If gh pr create fails, stop and report the error — do not retry