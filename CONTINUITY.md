---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:26:00.599757+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete real repeated-setup evidence in the existing default/non-root image qualification
    while preserving exact source, pins and outstanding native execution gates.
  includes:
  - Run the actual shared setup a second time in each built image, bound to Rust source, the minimal canonical
    fixture and toolchain/dependency inputs.
  - Require exact selected-source hashes/runtime pins and one successful repeat command before host admission.
  - Retain focused preparation controls and coordinate the full original image execution on a separately
    prepared bounded backend.
  excludes:
  - No new image/base/toolchain/profile or public identity-contract change, no source/creative/ADR adoption.
  - No full image success, hosted CI, browser acceptance, release, registry push or deployment is inferred
    from command doubles.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - scripts/qualify_dev_image.py
  - dev/qualification/smoke.py
  - dev/qualification/source_inputs.py
  - tests/test_dev_image_smoke.py
  - tests/test_qualify_dev_image.py
  - docs/DEVELOPMENT.md
  - docs/work/82/LOCAL_ACCEPTANCE.md
  - docs/work/82/FULL_IMAGE_2026-11-22.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - ROADMAP.md
work:
  objective: Complete real repeated-setup evidence in the existing default/non-root image qualification
    while preserving exact source, pins and outstanding native execution gates.
  success_conditions:
  - Actual image smoke must run the shared setup twice overall and preserve selected source and Rust/pnpm
    pins.
  - Host admission rejects missing/stale/forged repetition records rather than claim new image acceptance
    from old evidence.
  - Run the original pinned default/non-root path with actual daemon capacity; retain any unavailable
    execution as a named gate.
  active_issue:
    provider: github
    id: egohygiene/identity#82
    url: https://github.com/egohygiene/identity/issues/82
  next:
    kind: action
    id: execute-original-full-image-qualifier
    description: After the browser job and independent runtime-capacity preparation, execute the unchanged
      pinned-default/non-root image path from a clean committed source. Retain actual setup/cache/TLS/native/renderer
      and repeated-setup results.
    readiness: blocked
    references:
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/80
    depends_on:
    - sufficient-observed-daemon-capacity-and-browser-slot
state:
  base:
    revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    ref: refs/heads/main
    verified_at: '2026-11-22T18:26:00.599757+00:00'
  candidate:
    branch: codex/82-full-image-qualification-20261122
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-11-22T18:26:00.599757+00:00'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: Main75ca39f and issue82open rechecked. Earlier158→162 and Aether140 are merged. No open Identity
      PR was observed; this local candidate has no PR. Parent workers own separate current browser/runtime
      and Aether checkpoints.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-22T18:26:00.599757+00:00'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern test_*dev_image*.py --verbose
    outcome: passed
    observed_at: '2026-11-22T18:26:00.599757+00:00'
    notes: Thirteen focused controls pass:four repeat-setup smoke controls,two host-subreceipt controls
      and seven existing boundaries. Fixture/command doubles do not establish native image execution.
  - command: python3 -m py_compile on changed qualification modules/tests; python3 scripts/verify_docs.py
      --repository-root .; git diff --check
    outcome: passed
    observed_at: '2026-11-22T18:26:00.599757+00:00'
    notes: Syntax, current documentation targets and source whitespace pass.
  - command: Original default/non-root full qualification
    outcome: not-run
    observed_at: '2026-11-22T18:26:00.599757+00:00'
    notes: Managed VFS budget is insufficient; parent runtime work is preparing a separate bounded backend.
      No known-failing multi-GB image pull is repeated and no guard is bypassed merely to force a pass.
  environment_limitations:
  - Actual full current-source image builds, real cold dependency acquisition and repeated real setup
    remain unrun at this preparation checkpoint.
  - Browser/hosted CI/platform/release acceptance is separate; the prior five protocol tests are not image
    qualification.
  - No released EgoLint continuity-conformance claim; metadata/headings/budget use the existing pinned
    structural schema.
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

User/runtime and scoped instructions, live evidence and canonical sources outrank this operational checkpoint. It records qualification preparation, not complete image acceptance.

## Resume protocol

Read AGENTS, the qualifier/smoke/shared input selector, the #82 records and actual provider state. Preserve original profile/toolchain/base pins and earlier receipts. The previous five draft checkpoints are merged; their dated evidence retains its source and limits.

## Current objective and success conditions

Complete real repeated-setup evidence in the existing default/non-root image qualification while preserving exact source, pins and outstanding native execution gates.

## State snapshot

Main/base is75ca39f3fc7e5e9e0b5578af58c966cd2590a652. Candidate codex/82-full-image-qualification-20261122 is a local preparation branch with no containing-revision or PR self-reference. Issue82 remains open.

## Completed and material changes

The original smoke omitted a real second setup inside either image. The current candidate invokes the same shared helper again, preserves selected Rust/canonical-fixture/manifest/lock bytes and rechecks runtime pins. A shared pure selector lets host admission compare the actual emitted input map to the selected host source and require one successful repeat command. No production identity semantics, pins or image base changes.

## Validation and review evidence

Thirteen focused controls pass, including source/lock mutation, failed setup, runtime drift, missing/forged inventory and missing/duplicate/failed command refusal. Python compilation, documentation links and whitespace pass. These are fixture/command-double tests; full actual image execution is not reported passed.

## Blockers, risks, unknowns, and deferred work

The managed VFS store cannot meet its existing reserve. A separate runtime worker is testing a bounded backend while browser qualification gets the first heavy slot. Full pinned default/non-root image acceptance, actual dependency/cache/user/TLS/native/renderer results and new repeated real setup remain pending. #80/#88 and final #70/#98/#116 gates retain their owners.

## Next dependency-ready work

After actual backend capacity is independently observed and the browser slot is clear, run the original full qualifier from this clean committed source and retain exact source/image/command receipts. Do not close82 from protocol or storage-guard controls alone.

## Parallel changes and reconciliation

The parent coordinates current browser/action-acquisition, isolated runtime, self-source and Aether metadata checkpoints. This branch owns only development-image smoke/admission and related evidence. Reconcile root continuity semantically when stacking; no peer source is modified.

## Privacy and redaction

Public-safe source facts and scoped technical outcomes only. Exclude local filesystem topology, daemon/proxy values, credentials, private certificates/keys, unrelated personal context and transcripts.

## Handoff update protocol

Refresh after actual domain checks and before PR handoff; verify the pinned continuity schema,twelve headings and16384-byte/240-line budgets. ADR not required for this bounded existing-coverage completion; reference ADR0011 for layered evidence. Pinned Aether decision2.1.0/continuity1.1.0 and Hygiene1.2.0 retain their selected source revisions.

## Compaction and supersession

Git and owner issues retain history. Keep this current snapshot compact, preserve historical receipts and human/ADR lifecycle facts, and never relabel preparation controls as actual full qualification.
