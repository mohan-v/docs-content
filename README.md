# Elastic Docs Content

![GitHub deployments](https://img.shields.io/github/deployments/elastic/docs-content/docs-preview?logo=elastic&label=docs-preview&link=https%3A%2F%2Fdocs-v3-preview.elastic.dev%2Felastic%2Fdocs-content%2Ftree%2Fmain)

This repo contains source files for Elastic documentation.

## Contribute

If you find any bugs in our documentation, or want to request an enhancement, [open an issue](https://github.com/elastic/docs-content/issues). We also welcome contributions in the form of PRs. Before you submit a PR, make sure that you have signed our [Contributor License Agreement](https://www.elastic.co/contributor-agreement/).

We write our docs in markdown. Refer to our [syntax quick reference](https://elastic.co/docs/contribute-docs/syntax-quick-reference) for examples and additional functionality.

### Preview your changes

When you open a PR, your changes are built, deployed, and ready to be previewed within minutes.

## Docs tooling

Three scripts in the repo root help you audit and review documentation before opening a PR. They require Python 3, which is pre-installed on macOS. Run them from the repo root.

> Output files (`audit_report.md`, `link_report.md`, `style_report.md`) are listed in `.gitignore` and will never be committed.

---

### `doc_audit.py` — Content quality audit

Scans every `.md` file in the repo and flags structural issues that are easy to miss during review.

**Run it:**

```sh
python3 doc_audit.py
```

Takes about 10–20 seconds. Writes a report to `audit_report.md`.

**What it checks:**

| Check | What it means |
|---|---|
| Thin full-page files | `.md` pages with fewer than 5 lines of real content (after stripping frontmatter). These are likely stubs or accidental empties. |
| Thin snippet files | Files in `_snippets/` directories with fewer than 5 lines. Listed separately — snippets are intentionally short, so these are low priority. |
| Redirect stubs | Thin files containing "This page has moved" or "Refer to". Intentional — listed for reference, not as errors. |
| Mixed `.md`/`.adoc` directories | Folders that contain both formats. This repo uses `.md`; any `.adoc` files are legacy and should not be edited. |
| Duplicate frontmatter keys | Pages where the same YAML key appears twice in the frontmatter block, which can cause unpredictable build behavior. |
| Folders with no content files | Directories that contain no `.md` or `.adoc` files. Usually leftover from a move or restructure. |

**Reading the report:**

Open `audit_report.md`. The summary table at the top gives counts per check. Each section below it lists the affected files. Focus on "Thin full-page files" and "Duplicate frontmatter keys" first — those are the most likely to indicate real problems.

**Known limitations:**

- "Thin" means fewer than 5 non-blank lines after stripping frontmatter. A file with only a heading and one sentence counts as thin even if that's intentional.
- Does not validate frontmatter *values* — only checks for duplicate keys.
- Does not scan `raw-migrated-files/` (legacy content excluded from the build).

---

### `link_checker.py` — Internal link checker

Scans every `.md` file for links to other files in this repo, and reports any that point to a path that does not exist.

**Run it:**

```sh
python3 link_checker.py
```

Takes about 30–60 seconds. Writes a report to `link_report.md`.

**What it checks:**

Every `[text](path)` and `![alt](path)` link where the target is a file inside this repo. The "Link target" column shows what was written in the source file; "Resolved path (missing)" shows where the script looked for it.

**What it skips (these are not errors):**

| Skipped type | Example |
|---|---|
| External URLs | `https://elastic.co/...` |
| Cross-repo links | `elasticsearch://reference/...`, `kibana://...` |
| Substitution variables | `{{apis}}`, `{{kib-pull}}123` |
| Anchor-only links | `#section-heading` |
| Example placeholders | `...` or `/path/to/file.md` |

**Reading the report:**

Open `link_report.md`. Each section is a source file, with a table of the broken links it contains. To fix a broken link, either correct the path in the source file or check whether the target file was moved (and update `redirects.yml` if so).

Some entries in the report are known false positives — for example, links that use URL-encoded characters or non-standard targets that the build system resolves differently. Use judgement.

**Known limitations:**

- Does not check anchor fragments — only validates that the *file* exists, not that a specific `#heading` within it exists.
- Does not validate cross-repo links (`elasticsearch://`, `kibana://`, etc.). Those are resolved at build time by `docset.yml`.
- Does not check image paths used inside `:::{image}` directives — only standard Markdown `![alt](path)` syntax.

---

### `style_checker.py` — Style guide checker

Checks `.md` files against a subset of Elastic's style rules. The same rules run automatically on PRs via Vale, but Vale only checks changed lines. This script lets you check the full file — or the full repo — at any time.

**Run it (two modes):**

```sh
# Check a single file — prints results to the terminal
python3 style_checker.py path/to/your/file.md

# Check the whole repo — writes a report to style_report.md
python3 style_checker.py
```

The single-file mode exits with code 1 if violations are found, 0 if clean — useful for scripting or editor integrations.

**Rules it enforces:**

| Rule | What's flagged | Suggested fix |
|---|---|---|
| `device-agnostic` | "click", "tap", and their variants | Use "select" instead |
| `inclusive-language` | "whitelist", "blacklist" | Use "allowlist" or "denylist" |
| `filler-words` | "please", "just", "simply", "easily" | Remove the word |
| `no-latin` | "e.g.", "i.e.", "etc." | Use "for example", "that is", "and so on" |
| `version-comparisons` | "newer", "older"; "higher"/"lower" before "version/release/than" | Use "later" or "earlier" |

**What it skips:**

- YAML frontmatter at the top of each file
- Fenced code blocks (` ``` ` or `~~~`)
- Inline code (text inside single backticks)
- The `contribute-docs/` directory (it documents forbidden terms intentionally)
- The `.cursor/` and `.github/` directories

**Reading the report (full-scan mode):**

Open `style_report.md`. The summary table shows total violations per rule. The "Violations by file" section lists every flagged line with the matched text and a suggested fix. You do not need to fix every violation in one go — prioritise files you are actively editing.

**Known limitations:**

- Covers only 5 of Elastic's Vale rules. Rules not checked here include: Oxford comma, first-person pronouns, meaningful link text, and heading capitalisation.
- The `version-comparisons` rule only flags "higher"/"lower" when they immediately precede or follow "version", "release", or "than". Uses in other contexts are not flagged.
- Terms inside inline code are skipped, so `click here` in a code span will not be flagged even if the surrounding prose uses "click".

---

## License

[![CC BY-NC-ND 4.0][cc-by-nc-nd-image]][cc-by-nc-nd] [![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License][cc-by-nc-nd].

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg
