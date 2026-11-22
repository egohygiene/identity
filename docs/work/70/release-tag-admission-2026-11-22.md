# Release tag admission repair — 2026-11-22

Roadmap-Step: egohygiene/identity#70

ADR-Ref: egohygiene/identity#ADR-0019 (reference)

## Demonstrated gap

At source `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`, the release
workflow checked the supplied tag's version string, but did not verify that
the remote tag was annotated, selected the event's exact checkout commit, or
belonged to `main` history. `gh release create --verify-tag` established tag
existence without binding the downloaded artifacts to the same tag object
observed before packaging. A tag replacement between these stages could
therefore associate a different selection with the built assets.

## Bounded repair

[The admission helper](../../../scripts/verify_release_admission.py) reads the
remote tag object, peeled commit and `main` revision independently of local
refs. It fetches those exact object IDs without updating local refs, verifies
the annotated object's name and direct commit, requires a clean matching
checkout and paired Cargo/renderer version, and checks current `main`
ancestry. A second remote read rejects selection changes during admission.

The first packaging admission emits the observed annotated tag object ID.
The workflow requires that same object in fresh admissions immediately before
provenance attestation, artifact upload and GitHub release creation. Missing
refs, read errors, lightweight tags, changed annotations and mismatched
commits/versions fail closed. The package checkout now fetches full history
for ancestry checks. Stable/prerelease handling and the source-check jobs
retain their prior behavior.

These observations cannot lock a remote ref or make the following GitHub
operation atomic. Repository tag protection, release permissions and
maintainer adherence to the immutable-version contract remain necessary.
This repair does not implement the proposed broader distribution matrix,
choose a new version, sign a tag, or qualify a downloaded release.

## Checks

- `python3 -m unittest discover --start-directory tests --pattern 'test_release_*.py' --verbose`:
  18 passed, including 14 admission tests against disposable real Git remotes.
  They cover valid candidate/stable selections, current-main ancestry,
  annotation naming, lightweight tags, wrong checkout/tag commit/version,
  modified source, unrelated main history, a replacement annotation at the
  same commit after simulated packaging, deleted refs and unavailable remotes.
  The replacement test retains a stale local tag and verifies no success
  output is written on rejection. Reads leave local refs unchanged.
- `actionlint` 1.7.12 on `.github/workflows/release.yml`: passed.
- Release workflow YAML parsed with PyYAML 6.0.3; source gate and renderer job
  definitions compared equal to the base revision.
- `python3 scripts/verify_release.py --repository-root .`: passed, current
  version `1.0.0`, tag not checked; this does not select a release.
- `python3 scripts/verify_docs.py --repository-root .` and `git diff --check`:
  passed.

No real repository tags, releases, hosted CI, package publication or native
release qualification were run. Temporary test repositories alone were
tagged. The root #70 handoff owns consolidated continuity and broader suite
results; this scoped repair supplies no issue-closure claim.

## Decision impact

Loaded `create-decisions-document` v2.1.0 using `git show` at Aether revision
`dc8a16851f452763ef4f7fbe4bf057d4500b1921`, as pinned in repository
instructions. This implements the existing accepted
[ADR-0019](../../decisions/ADR-0019-immutable-release-contract.md) immutable
annotated release selection. It introduces no new release boundary or ADR
disposition. Historical tags, versions, releases and existing evidence remain
unchanged.

## Follow-up — prerelease flag classification

The existing publication Bash also treated a hyphen in SemVer build metadata
as a prerelease separator: stable `v1.0.0+linux-x64` received `--prerelease`.
The condition now removes the `+` metadata suffix before checking for the
prerelease separator; the full tag remains the release selection and title.

`tests/test_release_workflow.py` extracts the actual checked-in publication
run block with a bounded standard-library indentation reader and executes it
under POSIX Bash against disposable command doubles. Six tag cases cover
stable, stable with build metadata, release candidate and prerelease with
metadata selections; a second test confirms failed admission prevents the
fake publication command. The doubles perform no network or publication.
This regression needs no Python YAML dependency; it skips on non-POSIX hosts
because this publication job runs on Linux.

All 20 `test_release_*.py` tests pass after the fix, as do actionlint, docs and
staged whitespace checks. Running the same classification regression against
the prior committed workflow fails specifically for `v1.0.0+linux-x64`.
