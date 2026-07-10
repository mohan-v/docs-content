# Task: AI-Powered Editorial Review

## Purpose
Review a documentation page for editorial quality — completeness,
audience fit, template compliance, and clarity. Goes beyond style
checking into content judgment. Use when inheriting existing content,
before a major rewrite, or as a pre-PR quality gate for new pages.

## When to use
- Taking ownership of an existing page for the first time
- Before rewriting or significantly editing a page
- When a page has been flagged as thin or incomplete by doc_audit.py
- As a deeper review step before opening a PR for new content

## Instructions for Claude Code

Given a file path:

### Step 1 — Identify the content type
Read the file and determine which content type it is:
- How-to: task-oriented, numbered steps, "how to do X"
- Tutorial: learning-oriented, has objectives and prerequisites
- Overview: concept-oriented, explains what something is and why
- Troubleshooting: problem-oriented, symptoms/causes/resolution

If the content type is ambiguous, state your best guess and why.

### Step 2 — Check template compliance
Compare the page against the required sections for its content type
(defined in contribute-docs/content-types/):

How-to requires:
- Introduction (what this page helps you do)
- Before you begin (prerequisites)
- Numbered steps
- Success checkpoint (how the reader knows they succeeded)

Tutorial requires:
- Learning objectives
- Prerequisites
- Numbered steps
- Next steps

Overview requires:
- What it is
- How it works
- Value/why use it
- Next steps

Troubleshooting requires:
- Symptoms (what the reader observes)
- Causes (why it happens)
- Resolution (how to fix it)

Flag any required sections that are missing or thin (less than
2 sentences).

### Step 3 — Audience assessment
Identify the implied audience from the content. Then assess:
- Is the technical level consistent throughout?
- Are there unexplained terms or assumed knowledge gaps?
- Does the page tell the reader what they need to know BEFORE
  they need to know it?
- Is there anything that would confuse a reader new to this topic?

### Step 4 — Completeness check
Read the page as a reader trying to accomplish the stated goal.
Identify:
- Steps that are unclear or ambiguous
- Missing information a reader would need
- Claims that are made without explanation
- Places where "see also" links are missing but needed

### Step 5 — Clarity check
Flag specific sentences or passages that are:
- Too long or complex (suggest a rewrite)
- Passive voice where active would be clearer
- Jargon used without definition on first use
- Contradictory with other content on the same page

### Step 6 — Produce editorial report

Format:

## Editorial Review — [filename]
**Content type:** [identified type]
**Overall verdict:** READY / NEEDS MINOR WORK / NEEDS MAJOR WORK

### Template compliance
[List missing or thin required sections]

### Audience assessment
[Who this is written for, consistency issues]

### Completeness gaps
[Missing content, unclear steps, broken logic]

### Clarity issues
[Specific sentences or passages to rewrite, with suggestions]

### Priority fix list
1. [Most important fix]
2. [Second most important]
3. [etc.]

## Notes
- Focus on content quality, not style violations
  (style_checker.py handles those separately)
- Be specific — cite line numbers or quote the problematic text
- Distinguish between "must fix before publish" and
  "nice to have"
- If the page is genuinely good, say so clearly