---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T06:45:59.440107+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify the merged Linux engineering baseline and repair demonstrated test-harness and release-admission
    gaps in reviewable draft checkpoints.
  includes:
  - Current-source Rust/Python/renderer/integrity baseline and truthful environmental failures.
  - Isolated copied-executable consumer test writer with controlled inherited-descriptor mechanism evidence.
  - Bounded release-tag admission investigation and remaining engineering/owner-review gates.
  excludes:
  - No new supported platform, hosted CI, actual release, tag, deployment or skill publication.
  - No canonical self-source adoption, exact layer/token approval, asset redesign or ADR lifecycle promotion.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/work/70/BASELINE_2026-11-22.md
  - docs/work/70/baseline-2026-11-22.json
  - docs/work/70/EXECUTABLE_COPY_INVESTIGATION.md
  - docs/work/116/SOURCE_CLOSEOUT_2026-11-14.md
  - docs/releases/NEXT_RELEASE_MATRIX.md
  - docs/work/98/OWNER_PACKET.md
work:
  objective: Qualify the merged Linux engineering baseline and repair demonstrated test-harness and release-admission
    gaps in reviewable draft checkpoints.
  success_conditions:
  - Retain exact actual local results, failures, ignores and limits rather than infer platform/release
    conformance.
  - Close the copied-binary writable-descriptor exposure without production changes or blanket serial
    tests.
  - Preserve existing quality/immutable-release and human identity-governance boundaries.
  active_issue:
    provider: github
    id: egohygiene/identity#70
    url: https://github.com/egohygiene/identity/issues/70
  next:
    kind: action
    id: complete-bounded-admission-repair-and-qualifier-stack
    description: 'Complete the independently investigated annotated-tag/commit admission repair, then
      stack #80 browser, #82 setup, #88 renderer and #98 exact self-source review checkpoints.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/70
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: ec8fce30c3c96c7781238eb0a8899d6f0cee0a40
    ref: refs/heads/main
    verified_at: '2026-11-22T06:45:59.440107+00:00'
  candidate:
    branch: codex/70-engineering-baseline-20261122
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-11-22T06:45:59.440107+00:00'
    default_branch_revision: ec8fce30c3c96c7781238eb0a8899d6f0cee0a40
    issue_state: open
    pull_request_state: not-applicable
    notes: Main independently rechecked. Earlier155/156/157 and Aether139 are merged. Six Identity issues
      remain; this first sprint draft has no PR yet.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-22T06:45:59.440107+00:00'
  reviewed_by: Codex
  evidence:
  - command: Merged-source local Rust/Python/renderer/integrity baseline
    outcome: passed
    observed_at: '2026-11-22T06:45:59.440107+00:00'
    notes: Rust119pass/3existinghelperignores; Python186pass/2existing skips; renderer424pass/19files;
      strictClippy, frozen builds and existing integrity checks pass.
  - command: Controlled descriptor probe, standalone regression and 16-thread consumer suite
    outcome: passed
    observed_at: '2026-11-22T06:45:59.440107+00:00'
    notes: Mechanism barriers demonstrate errno26 and isolation. Focused standalone1pass; consumer14pass/1explicitworkerignore;
      strictClippy/format pass. Historical failure causality remains unproven.
  - command: Initial local Cargo and Docker attempts during VFS expansion
    outcome: limited
    observed_at: '2026-11-22T06:45:59.440107+00:00'
    notes: Initial Cargo commands failed ENOSPC; actual Cargo reruns after owned/generated cache cleanup
      passed. Ordinary pinned browser recipe did not execute after storage failure.
  - command: Release admission audit
    outcome: limited
    observed_at: '2026-11-22T06:45:59.440107+00:00'
    notes: Version/existence checks do not enforce the documented annotated immutable main-source binding.
      A bounded helper/workflow repair is in progress on a separate branch.
  environment_limitations:
  - 'Matching browser workflow and full clean-base image acceptance remain separate #80/#82 gates.'
  - Native macOS/Windows and actual downloaded release installation, upgrade and rollback remain unqualified.
  - 'Exact token/layer and subject-governance source review remain #98; incomplete candidates are not
    valid source.'
  - No released EgoLint continuity conformance is claimed; pinned schema/heading/budget checks are used.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# Identity continuity

## Purpose and precedence

Runtime/user and scoped instructions, live evidence and canonical sources outrank this current operational handoff. It records a draft engineering sprint, not completion or publication authority.

## Resume protocol

Read AGENTS and the source-bound records above. Reverify main, open issues and draft stack before acting. Earlier PR155/156/157 and Aether139 are merged; preserve unrelated existing checkouts and historical receipts.

## Current objective and success conditions

Qualify the merged Linux engineering baseline and repair demonstrated test-harness and release-admission gaps in reviewable draft checkpoints.

## State snapshot

Main/base is ec8fce30c3c96c7781238eb0a8899d6f0cee0a40. Candidate codex/70-engineering-baseline-20261122 has no self-referential revision/PR. This is the first planned draft checkpoint of the authorized overnight stack.

## Completed and material changes

The exact merged baseline passes native119 tests, Python186 tests and renderer424 tests with explicit existing helper ignores/optional skips. The separate copied-executable writer removes an uncovered parent-process descriptor inheritance window while preserving production behavior and test parallelism. Its controlled probe does not assert historical CI causality.

## Validation and review evidence

See docs/work/70/BASELINE_2026-11-22.md and EXECUTABLE_COPY_INVESTIGATION.md for exact commands and receipts. StrictClippy, formatting, frozen renderer/public builds, validator drift, publication/asset/docs/extraction and109JSONparse checks pass. Initial ENOSPC failures remain distinct from successful reruns. No hosted CI or native-platform generalization.

## Blockers, risks, unknowns, and deferred work

Release-tag admission repair is still in progress. Docker VFS materialization exhausted the ordinary browser build budget; #80/#82 retain actual acceptance. The local-act context fix, bounded entrypoint workflow and renderer/self-source packets are separate worker checkpoints. Actual source review, full engineering acceptance, release/live/consumer proof and #116 closure remain open.

## Next dependency-ready work

Finish and locally qualify the bounded release admission repair, then integrate the browser/setup/renderer/self-source checkpoints in dependency order. Keep all five draft PRs for maintainer review; do not merge, tag, release or deploy.

## Parallel changes and reconciliation

Concurrent workers own separate branches for70admission,80,82,88,98. Stack only scoped commits and reconcile continuity semantically. The governance/source/schema/asset contracts and proposed ADR lifecycles remain unchanged.

## Privacy and redaction

Public-safe source facts, synthetic fixtures and sanitized evidence only. No private transcript, credentials, proxy values, unrelated personal context or local filesystem topology in committed receipts.

## Handoff update protocol

Refresh after domain checks before each draft PR update. Validate the pinned schema, twelve headings, budgets and whitespace. Reference ADR0011 andADR0019; the isolated test-harness repair needs no duplicate ADR. Pinned Aether skill2.1.0/continuity1.1.0 and Hygiene1.2.0 retain their selected source revisions.

## Compaction and supersession

Git and linked work trackers retain history. Replace current operational prose and preserve historical receipts, approved baseline and immutable v1.0.0 release facts.
