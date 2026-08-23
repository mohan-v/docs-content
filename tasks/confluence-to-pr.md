# Task: Confluence Spec → JIRA → Doc → PR (Full Pipeline)

## Purpose
Read a Confluence feature spec, create a JIRA ticket, make the
documented change, and open a PR — all in one pipeline.

## When to use
- A PM or engineer has written a feature spec in Confluence
- The spec clearly describes what documentation needs updating
- The change is contained enough for automation (single file,
  clear instruction)

## Do NOT use for
- Specs that require structural decisions (use draft-and-review.md)
- Changes spanning more than 3 files
- New pages that don't exist yet (use draft-and-review.md first)

## Instructions for Claude Code

Given a Confluence page URL:

### Stage 1 — Read the spec
Read the Confluence page using the Atlassian MCP server.
Extract:
- Feature name
- What changed or is new
- Which existing doc files need updating
- Version requirements (if mentioned)
- Whether the change is breaking, new feature, or improvement

### Stage 2 — Assess complexity
Determine the right workflow:

Simple (update to existing file, clear instruction):
→ Proceed with this pipeline

Complex (new page, multiple files, structural decisions):
→ Still create the JIRA ticket (Stage 3) so the work is tracked
→ Then stop and recommend draft-and-review.md to the writer
→ Explain specifically what structural decisions need to be made

The JIRA ticket is always created — it's the audit trail regardless
of which tool handles the actual writing.


### Stage 3 — Create JIRA ticket
Create a JIRA ticket in the TESTMCP project with:
- Summary: "docs: [feature name] — [one-line description of change]"
- Description: Full details of what needs to change, which file,
  and why (based on the Confluence spec)
- Issue type: Task

Share the ticket URL with the writer before proceeding.

### Stage 4 — Make the documentation change
Using the JIRA ticket as the source of truth:
1. Create a working branch:
   - `git checkout nvanmane-1`
   - `git pull origin nvanmane-1`
   - `git checkout -b docs/<TICKET-ID>`
   - If a branch named `docs/<TICKET-ID>` already exists locally or on
     the remote, stop and report the conflict — do not force-overwrite
     or reuse it
2. Find the correct file in the repo
3. Make the documented change
4. Run style_checker.py on the changed file
5. Fix any violations

### Stage 5 — Open a PR
1. Commit the change:
   git add <changed-file>
   git commit -m "docs: <summary> per <TICKET-ID>"
2. Push to current branch:
   git push origin HEAD
3. Generate PR description using tasks/pr-description-generator.md
4. Open PR:
   - Working branches live on the `origin` fork (not the `elastic/docs-content`
     upstream), and `nvanmane-1` only exists on that fork. `gh pr create` and
     `gh repo view` both default to the upstream parent repo for a fork, which
     causes "No commits between elastic:nvanmane-1 and ..." errors — so
     `--repo` must be passed explicitly, derived from the `origin` remote URL
     (not from `gh repo view`):
     REPO=$(git remote get-url origin | sed -E 's#.*[:/]([^/]+/[^/]+)\.git#\1#')
     gh pr create --repo "$REPO" --base nvanmane-1 --head docs/<TICKET-ID>
     --title "docs: <summary> per <TICKET-ID>" --body "<pr-description>"
5. Share the PR URL

## Notes
- Stage 4 always creates a fresh branch off nvanmane-1, named
  docs/<TICKET-ID> — never commits directly to nvanmane-1 or reuses
  a leftover branch from a prior run
- Always share the JIRA ticket URL after Stage 3 before continuing
- The JIRA ticket is the audit trail — it connects the Confluence
  spec to the PR
- Branches are created from nvanmane-1, and PRs target nvanmane-1 —
  not main
- If the Confluence spec is ambiguous, stop at Stage 2 and ask
  for clarification