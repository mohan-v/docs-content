# Task: Proactive Documentation Gap Detection

## Purpose
Analyze a code or API diff and identify documentation gaps —
places where the code changed but the documentation wasn't updated.
Creates JIRA tickets for any gaps found.

## When to use
- After a developer merges a PR that touches APIs or features
- As part of a scheduled review of recent code changes
- When a release is being prepared and you want to verify docs coverage

## Instructions for Claude Code

Given a diff file or patch:

### Step 1 — Analyze the diff
Read the diff and identify every user-facing change:
- New parameters or fields added
- Parameters renamed or removed
- Default values changed
- New endpoints or URLs
- Deprecated features
- Breaking changes

Ignore: internal refactoring, test changes, comment-only changes.

### Step 2 — Search for existing documentation
For each user-facing change found, search the docs repo for:
- Any page that mentions the changed parameter/feature/endpoint
- The most likely file that should cover this change
- Whether that file has been recently updated to reflect the change

### Step 3 — Identify gaps
A gap exists when:
- A feature changed but no docs page mentions the change
- A parameter was renamed but docs still use the old name
- A new feature was added with no documentation at all
- A breaking change exists with no migration guidance

### Step 4 — Report gaps
For each gap found:
- What changed (from the diff)
- Where documentation should exist (most likely file)
- Whether partial documentation exists (needs update) or none exists
  (needs creation)
- Priority: HIGH (breaking change), MEDIUM (new feature),
  LOW (minor update)

### Step 5 — Create JIRA tickets
For each HIGH and MEDIUM priority gap, create a JIRA ticket
in the TESTMCP project:
- Summary: "docs: [feature] — [one-line description of gap]"
- Description: What changed, what doc update is needed, which file
- Priority: matching the gap priority

Share all created ticket URLs before finishing.

## Notes
- Focus on user-facing changes only
- One JIRA ticket per distinct gap (don't combine unrelated gaps)
- If a gap is already covered by an existing open JIRA ticket,
  note it but don't create a duplicate