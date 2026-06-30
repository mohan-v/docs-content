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
1. Find the correct file in the repo
2. Make the documented change
3. Run style_checker.py on the changed file
4. Fix any violations

### Stage 5 — Open a PR
1. Commit the change:
   git add <changed-file>
   git commit -m "docs: <summary> per <TICKET-ID>"
2. Push to current branch:
   git push origin HEAD
3. Generate PR description using tasks/pr-description-generator.md
4. Open PR:
   gh pr create --base main --title "docs: <summary> per <TICKET-ID>"
   --body "<pr-description>"
5. Share the PR URL

## Notes
- Always share the JIRA ticket URL after Stage 3 before continuing
- The JIRA ticket is the audit trail — it connects the Confluence
  spec to the PR
- If the Confluence spec is ambiguous, stop at Stage 2 and ask
  for clarification