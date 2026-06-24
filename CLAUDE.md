# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`docs-content` is the source for Elastic's unified documentation site ([elastic.co/docs](https://elastic.co/docs)), covering Elastic Stack 9.0+, ECE 4.0+, ECK 3.0+, and Serverless. Documentation for 8.x and earlier lives at elastic.co/guide and is **not** in this repo.

## Build and preview

```sh
# Full build — reports errors, warnings, and hints. Run before pushing.
docs-builder

# Local dev server at http://localhost:3000 with live reload
docs-builder serve

# Install docs-builder (first time)
curl -sL https://ela.st/docs-builder-install | sh
```

Do not introduce new build errors, warnings, or hints.

## Prose linting (Vale)

Vale runs automatically on PRs (changed lines only). To run it locally:

```sh
# Install Elastic style rules (macOS)
curl -fsSL https://raw.githubusercontent.com/elastic/vale-rules/main/install-macos.sh | bash
```

Then use the Vale VSCode extension. Fix all warnings and suggestions before opening a PR.

## Repo structure

Content is organized into top-level sections matching the site's primary navigation:

| Directory | Coverage |
|---|---|
| `get-started/` | Intro, deployment options, versioning |
| `solutions/` | Observability, Security, Search (Elasticsearch Solution) |
| `manage-data/` | Ingest, mappings, ILM, transforms |
| `explore-analyze/` | Kibana, ML, alerting, dashboards |
| `deploy-manage/` | All deployment types, upgrades, security |
| `cloud-account/` | Account/org management |
| `troubleshoot/` | Per-product troubleshooting |
| `release-notes/` | Per-product release notes |
| `reference/` | API docs, field schemas, config references |
| `contribute-docs/` | Style guide, syntax reference, contribution how-tos |

Each section contains a `toc.yml` that defines the navigation tree for that section. The root `docset.yml` stitches all sections together and also defines substitution variables (`{{es}}`, `{{kib}}`, `{{stack}}`, etc.) and cross-links to other Elastic repos.

## Navigation and TOC

- Navigation hierarchy is driven entirely by `toc.yml` files — file system structure alone does not affect nav order.
- The root `docset.yml` `toc:` block is the top-level ordering; each entry delegates to a section's `toc.yml`.
- To add a page to the nav, add it to the relevant `toc.yml` under the correct parent.
- Pages listed under `hidden:` in `docset.yml` are built but not shown in nav (e.g. `404.md`, `_search.md`).

## Frontmatter

Every `.md` file requires frontmatter. All valid keys and values are defined in `frontmatter.config.yml`.

```yaml
---
# MANDATORY on every page
applies_to:
  stack: ga 9.1        # lifecycle + optional version (e.g. "beta 9.2", "deprecated 9.0")
  serverless:          # omit value = all serverless project types
  deployment:
    eck: ga 3.0
    ece: ga 4.0
    ess: ga              # Elastic Cloud Hosted
    self: ga             # self-managed

# Drives elastic.co search filters — use valid IDs from frontmatter.config.yml
products:
  - id: elasticsearch   # elasticsearch | kibana | elastic-agent | fleet | apm | beats |
                        # logstash | security | observability | machine-learning |
                        # cloud-hosted | cloud-enterprise | cloud-kubernetes |
                        # cloud-serverless | elastic-stack | ingest | integrations |
                        # ecs | ecs-logging | elasticsearch-client | search-ui |
                        # elastic-serverless-forwarder | cloud-control-ecctl |
                        # elasticsearch-curator | painless | apm-agent | cloud-terraform

navigation_title: Short nav label   # optional — overrides sidebar label when title is long
description: SEO summary            # optional — shown in search results and link tooltips
mapped_pages:                        # optional — old elastic.co/guide URL(s) this page replaces
  - https://www.elastic.co/guide/...
layout: landing-page                 # optional — special layouts: archive | landing-page | not-found
---
```

`applies_to` can also be used at section or element level within the page body to narrow applicability for a specific block. The `product` sub-key under `applies_to` (not the same as `products:`) is for products with independent version schemes (APM agents, EDOT, ECCTL, Curator).

## Markdown flavor

Files use **MyST Markdown** (not standard CommonMark). Key syntax:

- Directives: `:::{tip}`, `:::{note}`, `:::{warning}`, `:::{important}` — closed with `:::`
- Includes (snippets): `:::{include} _snippets/filename.md\n:::`
- Applies-to inline block: ` ```{applies_to}\nstack: ga 9.1\n``` `
- Substitution variables: `{{es}}`, `{{kib}}`, `{{stack}}`, `{{ece}}`, etc. — defined in `docset.yml` under `subs:`
- Cross-repo links: `[text](elasticsearch://reference/path.md)` — repo name must be in `cross_links:` in `docset.yml`

Full syntax reference: [elastic.github.io/docs-builder/syntax/](https://elastic.github.io/docs-builder/syntax/)

## Snippets

`_snippets/` directories contain reusable partials intentionally kept short (1–4 lines is normal). Do not treat short files in `_snippets/` as incomplete content.

## Cumulative documentation model

This repo does **not** publish separate doc sets per version. Each page covers all supported versions of a feature in one place, using `applies_to` tags to indicate when behavior varies. When editing:

- Do not remove content for a still-supported version — refactor instead.
- Add `applies_to` tags when functionality is added, changes lifecycle state (beta → GA), or varies by deployment type.
- Content-only fixes (typos, clarity) do not need version tags.

## Redirects

When a page moves, add an entry to `redirects.yml`:

```yaml
'old/path.md': 'new/path.md'
```

Thin pages that contain only "This page has moved. Refer to [...]" are intentional redirect stubs — leave them as-is.

## raw-migrated-files/

This directory holds legacy AsciiDoc-migrated content excluded from the build (`docset.yml` `exclude:` list). Do not edit files here; they are reference only.

## PR checklist

PRs auto-deploy a preview within minutes of opening. The PR template requires a Generative AI disclosure — fill it in honestly.

## Audit tooling

Three scripts live in the repo root:

| Script | What it checks | Output |
|---|---|---|
| `doc_audit.py` | Thin files (<5 content lines), duplicate frontmatter keys, folders with no content files, `.adoc` files mixed with `.md` files | `audit_report.md` |
| `link_checker.py` | Broken internal `.md` links — skips cross-repo links (`elasticsearch://`), external URLs, and substitution variables (`{{...}}`) | `link_report.md` |
| `style_checker.py` | Elastic style violations: device-agnostic language, inclusive terminology, filler words, Latin abbreviations, version comparison wording | `style_report.md` |

```sh
python3 doc_audit.py
python3 link_checker.py
python3 style_checker.py
```

All three output files are in `.gitignore`. `style_checker.py` skips `contribute-docs/` (which documents forbidden terms intentionally), `.cursor/`, and `.github/`.

## Cursor skills (`.cursor/`)

Two skills are configured for Cursor IDE users working in this repo:

- **elastic-rag-writer** — answers questions grounded in provided doc context (repo files or Google Docs via gdrive MCP); cites sources with `[Source N]`
- **gdrive-doc-reader** — reads a named Google Doc via gdrive MCP and answers from that text only

## `applies_to` complete reference

### Keys

```yaml
applies_to:
  stack: <lifecycle> <version>          # Elastic Stack (ES, Kibana, Beats, etc.)
  serverless: <lifecycle>               # all Serverless project types
  serverless:
    security: <lifecycle>               # Security Serverless only
    elasticsearch: <lifecycle>          # Search Serverless only
    observability: <lifecycle>          # Observability Serverless only
  deployment:
    eck: <lifecycle> <version>          # Elastic Cloud on Kubernetes
    ece: <lifecycle> <version>          # Elastic Cloud Enterprise
    ess: <lifecycle>                    # Elastic Cloud Hosted
    self: <lifecycle>                   # self-managed
  product: <lifecycle> <version>        # products with independent version schemes
                                        # (APM agents, EDOT SDKs, ECCTL, Curator)
```

### Lifecycle values

`preview` | `beta` | `ga` | `deprecated` | `removed` | `unavailable`

Omitting the lifecycle value on `serverless:` or `stack:` means the feature is GA for all sub-types. Version is optional and represents the version when the lifecycle state first applied (e.g. `ga 9.1`, `deprecated 9.0`).

### Section-level and element-level tagging

Use a fenced code block with `{applies_to}` inside the page body:

````markdown
```{applies_to}
stack: beta 9.2
deployment:
  ece: unavailable
```
````

## Content types and file naming

Templates live in `contribute-docs/content-types/_snippets/templates/`. Guidelines are in `contribute-docs/content-types/`.

| Content type | Filename pattern | Required sections |
|---|---|---|
| How-to | `create-*.md`, `configure-*.md`, `troubleshoot-*.md` | intro, Before you begin, numbered steps, success checkpoint |
| Tutorial | `get-started-with-*.md`, `tutorial-*.md` | learning objectives, prerequisites, steps, next steps |
| Overview | `index.md` or `<feature>.md` | what it is, how it works, value, next steps |
| Troubleshooting | `<symptom>.md` or `troubleshoot-<problem>.md` | Symptoms, Causes, Resolution |

When creating a new page, prefer adding content to an existing page (cumulative model) over creating a new file. Create a new file only when the topic is genuinely standalone.

## Common MyST directives

These are used throughout the repo and are not standard Markdown:

```markdown
# Stepper — numbered steps with visual styling (preferred for multi-step procedures)
::::::{stepper}
:::::{step} Step title
Step content here.
:::::
:::::{step} Next step title
Content.
:::::
::::::

# Tab set — content variants (OS, deployment type, language, etc.)
:::::{tab-set}
::::{tab-item} macOS
macOS content.
::::
::::{tab-item} Linux
Linux content.
::::
:::::

# Applies-switch — like tab-set but tabs show applies_to badges, not text labels.
# All applies-switches on a page sync together.
:::::{applies-switch}
::::{applies}
:stack: ga
Stack content.
::::
::::{applies}
:serverless:
Serverless content.
::::
:::::

# Dropdown — collapsible section
::::{dropdown} Label text
:open:     ← optional: open by default
Content here.
::::

# Image
:::{image} images/my-screenshot.png
:alt: Descriptive alt text
:screenshot:    ← adds visual framing for UI screenshots
:width: 85%
:::

# Include a snippet
:::{include} _snippets/my-snippet.md
:::
```

## Images

- Store images in an `images/` subdirectory inside the same section folder as the page that uses them.
- Use the `:::{image}` directive, not standard Markdown `![]()` syntax.
- Always include `:alt:` text.
- Add `:screenshot:` for UI screenshots — this adds a border/shadow that visually frames the image.
- Accepted formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`.

## Cross-repo links

Cross-repo links use the format `[text](repo-name://path/to/file.md)`. The repo name must appear in the `cross_links:` list in `docset.yml`.

Common cross-repo targets:

| Repo name | Content |
|---|---|
| `elasticsearch` | Elasticsearch REST API and reference docs |
| `kibana` | Kibana developer/plugin docs |
| `elastic-agent` | Elastic Agent reference |
| `opentelemetry` | EDOT and OpenTelemetry reference |
| `beats` | Beats reference |
| `logstash` | Logstash reference |
| `apm-server` | APM Server reference |
| `cloud` | Elastic Cloud reference |
| `cloud-on-k8s` | ECK reference |

Example: `[ELSER model](elasticsearch://reference/elasticsearch/ml-nlp-elser.md)`

Do not use `https://` URLs to link to content that has a cross-repo target — use the cross-repo format so links resolve correctly in preview and production.

## Team ownership

CODEOWNERS maps directories to review teams. When creating or moving content, request review from the relevant team:

| Directory | Owner team(s) |
|---|---|
| `get-started/`, `extend/` | `@elastic/core-docs` |
| `solutions/observability/`, `solutions/security/` | `@elastic/experience-docs` |
| `solutions/search/` | `@elastic/developer-docs` |
| `explore-analyze/` | `@elastic/experience-docs`, `@elastic/developer-docs` |
| `manage-data/` | `@elastic/admin-docs` |
| `manage-data/ingest/`, `reference/fleet/` | `@elastic/ingest-docs` |
| `deploy-manage/`, `cloud-account/` | `@elastic/admin-docs` |
| `troubleshoot/` | `@elastic/docs` (varies by sub-path) |
| `release-notes/` | `@elastic/docs` |
| `solutions/observability/apm/apm-server/`, `reference/fleet/` | `@elastic/ingest-docs` |
| `release-notes/elastic-observability/`, `release-notes/elastic-security/` | `@elastic/ski-docs` |

All PRs require at least one `@elastic/docs` reviewer regardless of section.

## Vale style rules — most common violations

Vale runs on every PR. These rules produce the most frequent failures:

| Rule | Wrong | Right |
|---|---|---|
| DeviceAgnosticism | "click", "tap" | "select" |
| WordChoice | "whitelist", "blacklist" | "allowlist", "denylist" |
| DontUse | "please", "just", "simply", "easily", "aka" | omit or rephrase |
| Latinisms | "e.g.", "i.e.", "etc." | "for example", "that is", "and so on" |
| OxfordComma | "cats, dogs and birds" | "cats, dogs, and birds" |
| Versions | "newer", "older", "higher", "lower" (for versions) | "later", "earlier" |
| FirstPerson | "I", "me", "my" | rephrase in second or third person |
| MeaningfulCTAs | "click here", "read more" | descriptive link text |

## `learning-rag/` — not docs content

The `learning-rag/` directory contains experimental Jupyter notebooks for RAG pipeline learning. It is untracked (`?? learning-rag/` in git status) and not part of the published documentation. Do not suggest editing files there when asked about docs content, and exclude it from any content searches or audits.

## Available tasks
- `tasks/parallel-doc-review.md` — parallel doc audit using all three tools. Run before major releases or on demand.
- `tasks/breaking-change-detector.md` — classify breaking changes 
  from a diff and draft release note entries
- `tasks/pr-description-generator.md` — generate a reviewer-ready 
  PR description from the current git diff
- `tasks/consistency-checker.md` — find terminology and version 
  inconsistencies for a named feature across the repo
- `tasks/jira-pipeline-manual-pr.md` — JIRA → edit → style check → 
  PR description → stops for writer review before committing
- `tasks/jira-pipeline-auto-pr.md` — JIRA → edit → style check → 
  commit → open PR automatically (use for simple, contained fixes only)
- `tasks/pr-doc-review.md` — scoped doc review for PR changed files only. 
  Used automatically by GitHub Actions on every PR.

## Team roles and workflows

### Writer workflow
When helping a writer:
- Always check frontmatter completeness before suggesting content edits
- Suggest MyST directives (:::tip, :::note) instead of plain markdown 
  equivalents
- Flag any use of banned terms (click, tap, whitelist, blacklist, 
  please, just, simply) before finalizing a draft
- When creating new content, check contribute-docs/content-types/ 
  for the correct template first

### Doc manager workflow  
When helping a doc manager:
- Default to running tasks/parallel-doc-review.md for repo-wide audits
- Prioritize findings by: build risk first, broken links second, 
  content gaps third, style last
- When asked to assess a section, compare against CODEOWNERS to 
  identify the right review team

## When to use each tool

| Situation | Action |
|---|---|
| Before opening a PR | Run `python3 style_checker.py <file>` on changed files |
| After a content migration | Run `tasks/parallel-doc-review.md` |
| New feature to document | Check `contribute-docs/content-types/` for template |
| Broken link reported | Run `python3 link_checker.py` and check `link_report.md` |
| Release prep | Run full parallel doc review, fix critical issues first |

## Guardrails — never do these

- Do not edit files in `raw-migrated-files/` — reference only
- Do not remove `applies_to` frontmatter — refactor instead
- Do not create a new `.md` file when adding to an existing page 
  would fit the cumulative model
- Do not use standard Markdown image syntax `![]()` — use 
  `:::{image}` directive
- Do not add `https://` links to content that has a cross-repo target
- Do not suggest merging thin files in `_snippets/` — they are 
  intentionally short
