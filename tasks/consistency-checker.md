# Task: Cross-repo Documentation Consistency Check

## Purpose
Find all references to a feature or topic across the repository,
identify inconsistencies, and produce a prioritized fix list.

## Instructions for Claude Code

Given a feature name or topic:

### Step 1 — Find all references
Search the entire repo for the feature name and common variations.
Include: .md files, toc.yml files, docset.yml.
Exclude: raw-migrated-files/, learning-rag/, _snippets/ unless
specifically relevant.

### Step 2 — Extract key claims
For each file that references the feature, extract:
- Version numbers mentioned (applies_to tags, inline version refs)
- Terminology used (exact feature name, abbreviations, variations)
- Cross-repo links (elasticsearch://, kibana://, etc.)
- Any "how it works" descriptions

### Step 3 — Compare for inconsistencies
Look for:
- Different version numbers for the same lifecycle state
- Terminology variations (e.g. "ELSER" vs "Elastic Learned Sparse
  EncodeR" vs "elser model")
- Contradictory descriptions of the same behavior
- Cross-repo links that point to non-existent targets
- applies_to tags that conflict across pages covering the same feature

### Step 4 — Produce consistency report

Format:
1. Feature coverage map — every file that mentions this feature
2. Inconsistencies found — specific conflicts with file + line refs
3. Terminology audit — all variations found, recommended standard
4. Recommended fixes — ordered by severity

## Notes
- Version inconsistencies are highest priority (build risk)
- Terminology variations are medium priority (user confusion)
- Cross-repo link issues may be false positives — flag but don't
  assume broken

## Cross-repo checking (when additional repos are available locally)

If other Elastic repos are cloned under ~/repos/, extend the search:

### Additional repos to check
- ~/repos/elasticsearch/docs/ — Elasticsearch reference docs
- ~/repos/kibana/docs/ — Kibana docs (if cloned)

### Step 1 (extended) — Find all references across repos
Search each available repo for the feature name:
```bash
grep -r "<feature>" ~/repos/docs-content/ --include="*.md" -l
grep -r "<feature>" ~/repos/elasticsearch/docs/ --include="*.md" -l
```

### Step 2 (extended) — Compare across repos
For each file found in both repos, compare:
- Model IDs and parameter names — must match exactly
- Version numbers — should be consistent
- Terminology — same feature name spelling and capitalization
- Descriptions — should not contradict each other

### Step 3 (extended) — Flag cross-repo conflicts
Report any inconsistency where docs-content and elasticsearch 
describe the same thing differently.