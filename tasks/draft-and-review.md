# Task: Draft and Review (Human-in-the-loop)

## Purpose
Draft a new documentation page or major revision, then pause for
human review and decisions before making any file edits. Use when
the task involves new content, structural decisions, or anything
where AI judgment alone is insufficient.

## When to use
- Writing a new documentation page from a feature spec
- Major rewrites of existing pages
- Any task where the correct structure or placement is unclear
- When the editorial review flags "NEEDS MAJOR WORK"

## Do NOT use for
- Simple word/typo fixes (use jira-pipeline-manual-pr.md)
- Style cleanup (use style_checker.py directly)
- Link fixes (use link_checker.py output)

## Instructions for Claude Code

Given a spec, ticket, or file to rewrite:

### Stage 1 — Understand the task
1. Read the input (Confluence page, JIRA ticket, or existing file)
2. Identify:
   - What needs to be written or changed
   - Who the audience is
   - Which content type applies (how-to/tutorial/overview/troubleshooting)
   - Where in the repo this content belongs

### Stage 2 — Flag decisions needed from the human
Before drafting anything, list every decision that requires human
judgment:

Examples of decisions Claude cannot make alone:
- "Should this be a new page or added to an existing page?"
- "The spec mentions version 9.3 — is this GA or still beta?"
- "This content overlaps with [existing page] — should that page
   be updated instead?"
- "The spec doesn't specify the audience — is this for developers
   or operators?"
- "Should the applies_to tag include serverless?"

Format these as numbered questions. Stop here and wait for answers.

### Stage 3 — Draft (only after human answers Stage 2 questions)
Once the human has answered the Stage 2 questions:
1. Draft the full page using the correct template from
   contribute-docs/content-types/_snippets/templates/
2. Apply correct frontmatter (applies_to, products, navigation_title)
3. Use MyST directives (:::note, :::tip, stepper) appropriately
4. Include cross-repo links using elasticsearch:// or kibana:// format
   where relevant

### Stage 4 — Present draft for review
Show the complete draft and:
- Summarize the decisions you made while drafting
- Flag anything you're uncertain about
- Ask: "Should I write this to [filename]? Confirm yes/no."

### Stage 5 — Write file (only after explicit confirmation)
Only write to disk after the human says yes. Then:
1. Write the file
2. Add to the correct toc.yml
3. Run style_checker.py on the new file
4. Show the git diff for final review

## Critical rule
Never edit, create, or delete any file until Stage 4 confirmation
is received. Drafting happens in the conversation, not on disk.