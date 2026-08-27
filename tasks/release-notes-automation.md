# Task: Release Notes Automation from PR Diff

## Purpose
Given a merged or open PR number, read its diff, determine if it
represents a release-notes-worthy change (new feature, enhancement,
deprecation, fix, or breaking change — NOT internal tooling/task files),
draft a properly formatted release-notes entry matching the existing
file's conventions, insert it into the correct release-notes file,
and open a PR with that change.

## When to use
- A writer or doc manager wants a release-notes entry drafted and
  filed for a specific PR, on demand
- The PR's changes are clearly user-facing (product feature area,
  not internal tooling)

## Do NOT use for
- PRs that only touch `tasks/`, `.github/`, or other non-product files
  — stop at Step 2 instead
- Changes that don't map cleanly to an existing release-notes
  file/version section — stop at Step 3 instead
- Automatic/unattended runs — this task is manually triggered per PR

## Instructions for Claude Code

Given a PR number:

1. Fetch the diff:
   - `gh` defaults to the upstream parent repo on a fork, not the fork
     itself — if a PR with the same number exists in both
     `elastic/docs-content` and the fork, this silently fetches the
     wrong PR. Derive `--repo` explicitly from the `origin` remote
     (same pattern as Step 8):
     `REPO=$(git remote get-url origin | sed -E 's#.*[:/]([^/]+/[^/]+)\.git#\1#')`
     `gh pr diff <PR-NUMBER> --repo "$REPO"`
2. Analyze the diff: what changed, what product/feature area, what
   type of change (feature/enhancement/deprecation/breaking/fix),
   and what version this targets.
   - If the diff is purely internal tooling (e.g. touches only
     `tasks/`, `.github/`, or similar non-product files), STOP and
     report that no release-notes entry applies — do not proceed
     further.
3. Find the correct release-notes file: search `release-notes/` for
   the file matching the product area and version.
   - If no matching file/version section exists, STOP and ask the
     writer where this entry belongs rather than guessing or
     creating a new file.
4. Draft the entry: write the change in the same style/format as
   existing entries in that file (opening verb, what/why, PR link
   using the file's existing substitution variable convention, and
   the correct section — e.g. "Features and enhancements" vs.
   "Breaking changes" vs. "Deprecations").
   - The PR link (e.g. `{{kib-pull}}` or the equivalent substitution
     for the relevant product repo) must reference the
     Kibana/engineering PR that made the underlying change — a
     different PR, in a different repo, from this docs-content PR.
     It must NEVER default to, reuse, or assume the docs-content PR
     number. Find the actual engineering PR number only if it
     appears explicitly in the docs-content PR's diff or description
     (e.g. a linked PR, commit message, or issue reference). If it
     is not present anywhere in the diff or description, STOP and
     ask the writer for the correct engineering PR number — do not
     proceed with any number, including the docs-content PR's own
     number, without the writer's explicit confirmation that it's
     correct.
5. Create a working branch from nvanmane-1:
   - `git checkout nvanmane-1`
   - `git pull origin nvanmane-1`
   - `git checkout -b docs/release-notes-<PR-NUMBER>`
   - If a branch named `docs/release-notes-<PR-NUMBER>` already
     exists locally or on the remote, stop and report the conflict —
     do not force-overwrite or reuse it
6. Insert the drafted entry into the correct file/section
7. Run `python3 style_checker.py <changed-file>`
   - If violations found, fix them and re-run until clean
8. Commit, push, and open a PR:
   - `git add <changed-file>`
   - `git commit -m "docs: add release note for PR #<PR-NUMBER>"`
   - `git push origin HEAD`
   - Working branches live on the `origin` fork (not the `elastic/docs-content`
     upstream), and `nvanmane-1` only exists on that fork. `gh pr create` and
     `gh repo view` both default to the upstream parent repo for a fork, which
     causes "No commits between elastic:nvanmane-1 and ..." errors — so
     `--repo` must be passed explicitly, derived from the `origin` remote URL
     (not from `gh repo view`):
     `REPO=$(git remote get-url origin | sed -E 's#.*[:/]([^/]+/[^/]+)\.git#\1#')`
     `gh pr create --repo "$REPO" --base nvanmane-1 --head docs/release-notes-<PR-NUMBER> --title "docs: release note for PR #<PR-NUMBER>" --body "<pr-description>"`
9. Share the PR URL with the writer

## Notes
- At every step, if that step fails or produces an unexpected result,
  STOP immediately and report exactly what succeeded, what failed,
  and the current state (e.g. "commit succeeded locally but push
  failed — the branch and commit still exist locally, nothing was
  lost, here's the error"). Never attempt to auto-recover, retry, or
  clean up on failure — leave the repo state exactly as it is so the
  writer can decide how to proceed. Never skip a step or continue
  forward if a prior step didn't complete successfully.
- Manual trigger only: run as "run tasks/release-notes-automation.md
  for PR #<number>"
- If the PR's diff doesn't clearly map to one release-notes file/
  section, stop and ask rather than guessing
- Distinguish this from `tasks/breaking-change-detector.md`: that task
  only comments on PRs touching `release-notes/**` and only analyzes
  breaking changes; this task handles all change types and actually
  writes the entry
- Branches are created from nvanmane-1, and PRs target nvanmane-1 —
  not main
