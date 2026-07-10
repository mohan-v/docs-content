# Task: Automated PR Description Generation

## Purpose
Generate a complete, reviewer-ready PR description from the current git diff. Saves writer time and ensures consistent PR quality.

## Instructions for Claude Code

### Step 1 — Analyze the diff
Run: git diff main...HEAD
Identify:
- Which files changed
- What type of change each file represents (new content, edit,
  restructure, fix, style cleanup)
- Whether any changes are breaking or user-facing

### Step 2 — Infer the motivation
Based on the changes, infer the most likely reason for the PR:
- Bug fix (broken link, incorrect info, build error)
- New feature documentation
- Style/terminology cleanup
- Structural reorganization
- Release notes update

### Step 3 — Write the PR description

Use this exact format:

## Summary
[2-3 sentences: what changed and why]

## Changes
[bullet list: each changed file with one-line description]

## User impact
[None / Low / Medium / High] — [one sentence explanation]

## Reviewer notes
[anything specific the reviewer should check or be aware of]

## Checklist
- [ ] Style checker passed on changed files
- [ ] Internal links verified
- [ ] Frontmatter complete on all changed files
- [ ] applies_to tags accurate
- [ ] No content removed that's still needed for supported versions

### Step 4 — Flag anything uncertain
If the motivation is unclear from the diff alone, say so explicitly
and ask the writer one clarifying question.
