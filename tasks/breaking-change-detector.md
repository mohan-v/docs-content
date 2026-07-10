# Task: Breaking Change Detection from Diff

## Purpose
Analyze a git diff or patch file and identify all user-facing changes.
Classify each change and draft release note entries automatically.

## Instructions for Claude Code

Given a diff file or git diff output:

### Step 1 — Classify every change

For each change found, classify it as one of:
- BREAKING — user must change something on their end to avoid failure
- DEPRECATED — still works but will be removed in a future version
- NEW FEATURE — additive, no user action required
- INTERNAL — invisible to users, no doc needed

### Step 2 — Flag breaking changes prominently

List all BREAKING changes first, each with:
- What changed (before → after)
- Why it breaks existing behavior
- What the user must do to adapt

### Step 3 — Draft release note entries

For each BREAKING, DEPRECATED, and NEW FEATURE change, draft a
release note entry in this format:

**[TYPE] Short title**
Description of what changed and user impact.
*Action required: what the user must do (for BREAKING only)*

### Step 4 — Produce a summary table

| Change | Type | User impact | Action required |
|---|---|---|---|

## Notes
- Ignore whitespace-only changes
- Ignore comment-only changes  
- When in doubt, classify as BREAKING (safer for users)
- Use plain language — assume the reader is a developer, not an
  internal engineer