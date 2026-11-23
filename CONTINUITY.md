---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T19:11:14.305941+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Retain actual native pinned default/non-root image acceptance and the bounded repeated-setup/proxy-trust
    repairs for review.
  includes:
  - Actual default/root and inherited1000 non-root image builds, repeat setup, exact inputs/pins, cache
    ownership, CA/TLS, native output and renderer evidence.
  - Preserved first failure and bounded scoped proxy/ephemeral CA repair with meaningful refusal controls.
  excludes:
  - No hosted hardening, all-entrypoint full CI matrix, arbitrary base/platform qualification, release
    or publication.
  - No source/creative/ADR adoption, secret or certificate-byte retention, base/toolchain/profile pin
    change.
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
  objective: Retain actual native pinned default/non-root image acceptance and the bounded repeated-setup/proxy-trust
    repairs for review.
  success_conditions:
  - Both actual images pass complete native qualification and preserve selected source/pins during actual
    repeat setup.
  - Retain exact source/image/command receipt bindings, original unchanged8GiB admission and independent
    trust-persistence negative controls.
  - Focused controls, documentation, privacy and pinned continuity structure pass before parent handoff.
  active_issue:
    provider: github
    id: egohygiene/identity#82
    url: https://github.com/egohygiene/identity/issues/82
  next:
    kind: action
    id: review-and-stack-native-image-evidence
    description: Review the source-bound native image receipts and scoped repairs, then stack the preserved
      tested commits. Parent reconciles82 with browser80 and final70/116 acceptance; do not infer hosted/all-entrypoint
      coverage.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/80
    depends_on: []
state:
  base:
    revision: b7486d47f5083914956bfcdfaea89e1cf8031226
    ref: refs/heads/codex/80-qualified-browser-stack-20261122
    verified_at: '2026-11-22T19:11:14.305941+00:00'
  candidate:
    branch: codex/82-qualified-images-stack-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T19:11:14.305941+00:00'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: Main remains 75ca39f; six Identity finish issues remain open. Earlier158 through162 and Aether140
      are merged. Parent drafts 163,164 are open; this next child PR does not yet exist. No new sprint
      PR is merged or published.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#163
    url: https://github.com/egohygiene/identity/pull/163
  - provider: github
    id: egohygiene/identity#164
    url: https://github.com/egohygiene/identity/pull/164
  - provider: github
    id: egohygiene/aether#142
    url: https://github.com/egohygiene/aether/pull/142
review:
  status: passed
  reviewed_at: '2026-11-22T19:09:25.549967+00:00'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern test_*dev_image*.py --verbose
    outcome: passed
    observed_at: '2026-11-22T19:09:25.549967+00:00'
    notes: 16 focused controls pass, including actual CLI path/loop refusal before Docker, scoped trust
      precedence, source/pin drift and forged/stale repeat-receipt rejection.
  - command: python3 scripts/qualify_dev_image.py --proxy-ca <public-ca-bundle> --receipt <outside-repository>
    outcome: passed
    observed_at: '2026-11-22T19:09:25.549967+00:00'
    notes: Clean8255c5b actual native Linuxamd64 overlay2:8957652992free exceeds unchanged8GiBguard; defaultroot
      and1000nonroot pass32commands each,58repeat-source inputs/17canonicalfiles preserved,14complete
      outputs equal. Actual first failure retained.
  - command: Actual pinned-base proxy/CA probes and network-disabled image trust-persistence controls
    outcome: passed
    observed_at: '2026-11-22T19:09:25.549967+00:00'
    notes: Proxy-only curl60/explicitreadonlyCA0; both built images retain original systemCAbytes, no
      transportENV/proxyvalues inconfig/history, no ephemeralCApaths withoutbind. No certificate/proxybytes
      retained.
  - command: Python compilation; verify_docs.py; receipt/source/hash/privacy checks; continuity schema/headings/budget;
      git diff --check
    outcome: passed
    observed_at: '2026-11-22T19:09:25.549967+00:00'
    notes: Exact public JSON receipts preserve raw hashes; tested build-input inventory remains unchanged
      by documentation-only handoff.
  environment_limitations:
  - Actual acceptance covers only the pinned default and derived1000nonroot images on native Linuxamd64,
    not arbitrary platforms/bases or hosted runner hardening.
  - Browser/workflow80 and final70/116 acceptance retain independent source/scope; no released continuity-conformance
    claim.
  - Original full-image execution represents8255c5b; parent approval/browse integration is not relabeled
    as that run. Parent browser164 separately retains clean a563 proofs and uploader-only local act failure.
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

User/runtime and scoped instructions, live evidence and canonical sources outrank this operational checkpoint. This records actual bounded native image acceptance, not a release or human approval.

## Resume protocol

Read AGENTS, the qualifier/smoke/input selector, the #82 records and live provider state. Preserve exact base/toolchain/profile pins and historical receipts. Tested source is8255c5b; the handoff adds only documentation/evidence.

## Current objective and success conditions

Retain actual native pinned default/non-root image acceptance and bounded repeated-setup/proxy-trust repairs for review.

## State snapshot

Stack base is `codex/80-qualified-browser-stack-20261122` at `b7486d47f5083914956bfcdfaea89e1cf8031226`. Candidate `codex/82-qualified-images-stack-20261122` is a draft child with no containing-revision or pre-PR self-reference. Main remains `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`. Domain receipts retain their exact independently represented source; stacking does not relabel earlier runs as tests of later code.

## Completed and material changes

Real setup now repeats in each image and host admission requires exact58-input preservation, runtime pins and one successful repeat command. Actual original build failed missing proxy forwarding; exact-base controls isolated unknownCA60 versus explicitCA0. Scoped names-only proxy transport and optional ephemeral publicCAsecret/read-only runtime bind repair that gap. Publicsecret mode0444 supports inherited1000; generic CApath refusals protect CLI diagnostics. No base/pin/truststore change.

## Validation and review evidence

Sixteen focused controls and independent code review pass. Fresh original8GiBreserve admitted8957652992bytes; exact Node pull/config binding and both complete image builds/smokes passed32commands each. Actual repeated setup preserves58inputs/Rust1.97.1/pnpm11.21.0;17canonicalfiles/unrelatedsource and14complete output files are preserved/equal. Synthetic unknownCA rejection, explicittrust, cache ownership, CLI and renderer checks pass. Both actual images retain original systemtrust with no persisted transportENV/proxyvalues or ephemeralCAfiles. Exact structured receipts and raw-output hashes live in docs/work/82/full-image-2026-11-22; syntax/docs/privacy/continuity/whitespace pass.

## Blockers, risks, unknowns, and deferred work

The current-source full default/non-root image gate is clear. Actual scope remains native Linuxamd64 on two exact bases; no full all-entrypoint CI matrix or hosted hardening follows from it. Parent owns #80/#88 and final #70/#98/#116 reconciliation and human source decisions.

## Next dependency-ready work

Review and stack preserved tested commits and the exact receipt packet. Browser parent164 now retains three original a563 browser passes; its whole local act job still fails only artifact transport. Review that evidence with this8255 image proof, then continue final audit without relabeling historical receipt scope or treating this as a release.

## Parallel changes and reconciliation

This checkpoint follows parent draft PRs #163 → #164. The engineering parent enforces existing approval timestamp validity and retains unknown actual-owner review times. Each browser, development-image and source-assembly record retains its own represented source and qualification limits. Review parents before children; keep source adoption and actual release/deployment separate. Aether metadata projection and installed-host verification retain their separate draft chain under Aether38.

## Privacy and redaction

Public source facts and bounded technical outcomes only. Proxy values, host CApath and certificate/key bytes are absent from public receipts. Raw task-local build/network logs stay outside the repository with hashes retained. Disposable synthetic container paths are recorded as actual commands, not private host topology.

## Handoff update protocol

Refresh after actual domain checks and before handoff; validate pinned schema,twelve headings and16384-byte/240-line budgets. ADR not required for completing existing image evidence and bounded compatibility repairs; ADR0011 governs layered evidence. Pinned Aether decision2.1.0/continuity1.1.0 and Hygiene1.2.0 keep their immutable revisions.

## Compaction and supersession

Git and owner issues retain history. Keep this snapshot compact, preserve historical failure/source/human disposition boundaries and distinguish actual local native evidence from later CI/release acceptance.
