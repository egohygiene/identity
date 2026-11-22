---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T07:03:33.481833+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify the existing portable setup entry points through a bounded local workflow and prevent
    demonstrated Docker VFS exhaustion before pull/build.
  includes:
  - Run the independent portable-entrypoints workflow job under act with actual Bash/Make/Task and checksum-verified
    Task installation.
  - Retain sanitized source-bound local evidence and storage refusal; preserve full default/custom image
    acceptance as pending.
  excludes:
  - Hosted CI, full clean-base image/browser qualification, release/tag/channel publication and support
    promotion.
  - Identity source, token/layer, creative/governance approvals and changes to other agents' checkpoints.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/work/82/LOCAL_ACCEPTANCE.md
  - .github/workflows/development-image.yml
  - scripts/dev-env.sh
  - scripts/qualify_dev_image.py
  - docs/DEVELOPMENT.md
  - docs/releases/NEXT_RELEASE_MATRIX.md
  - https://github.com/egohygiene/identity/issues/82
  - https://github.com/egohygiene/identity/issues/70
work:
  objective: Qualify the existing portable setup entry points through a bounded local workflow and prevent
    demonstrated Docker VFS exhaustion before pull/build.
  success_conditions:
  - Actual portable workflow job passes all five frontend protocol tests with verified Task installation.
  - Known insufficient VFS capacity stops before Docker mutation and retains failure evidence.
  - Full clean-base acceptance, hosted proof and release/source approvals remain explicitly pending.
  active_issue:
    provider: github
    id: egohygiene/identity#82
    url: https://github.com/egohygiene/identity/issues/82
  next:
    kind: action
    id: qualify-full-development-image-on-capable-host
    description: Reconcile parallel engineering checkpoints, then run the unchanged current-source default/non-root
      custom image gate on a sufficiently provisioned Docker host.
    readiness: blocked
    references:
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/70
    depends_on:
    - egohygiene/identity#80
state:
  base:
    revision: d53427184c7646195f6bebc6289c4dcfdd191a3d
    ref: refs/heads/codex/80-browser-stack-20261122
    verified_at: '2026-11-22T07:03:33.481833+00:00'
  candidate:
    branch: codex/82-setup-stack-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T07:03:33.481833+00:00'
    default_branch_revision: ec8fce30c3c96c7781238eb0a8899d6f0cee0a40
    issue_state: open
    pull_request_state: not-applicable
    notes: Merged main remains ec8fce3; six finish issues remain open. Earlier155/156/157 and Aether139
      are merged. Parent draft PRs 158,159 are open; this next child PR does not yet exist. No overnight
      sprint PR is merged or published.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#158
    url: https://github.com/egohygiene/identity/pull/158
  - provider: github
    id: egohygiene/identity#159
    url: https://github.com/egohygiene/identity/pull/159
review:
  status: partial
  reviewed_at: '2026-11-22T06:46:52.640172+00:00'
  reviewed_by: Codex
  evidence:
  - command: act workflow_dispatch -W .github/workflows/development-image.yml -j portable-entrypoints
      (bounded pinned-image local execution)
    outcome: passed
    observed_at: '2026-11-22T06:46:52.640172+00:00'
    notes: Actual verified Task 3.45.3 download/install; 5 tests passed, zero skipped, 2.181 s. Exact
      image/source hashes and local action/proxy substitutions retained under docs/work/82/qualification-2026-11-22.
  - command: python3 -m unittest discover --start-directory tests --pattern test_qualify_dev_image.py
      --verbose
    outcome: passed
    observed_at: '2026-11-22T06:46:52.640172+00:00'
    notes: Seven boundary tests pass, including insufficient VFS reserve refusing pull/build while writing
      failure evidence; unknown remote storage and explicit bypass covered.
  - command: python3 scripts/qualify_dev_image.py --receipt <external-evidence-path>
    outcome: failed
    observed_at: '2026-11-22T06:46:52.640172+00:00'
    notes: Actual vfs storage preflight refuses before pull/build; this is a demonstrated guard and an
      incomplete image qualification, not a passed image smoke.
  environment_limitations:
  - 'Full current-source pinned default and non-root custom image setup/runtime/TLS/cache checks require
    more Docker capacity; #82 remains open.'
  - The narrow workflow uses synthetic external-tool protocols and cached act runner image; it does not
    qualify real Rust/pnpm bootstrap or the development base.
  - Local checkout/action mirrors and proxy public CA differ from hosted execution; no hosted hardening,
    browser/visual or release proof is claimed.
  - 'Independent #70/#80/#88 engineering, #98 source/approval/release and #116 final consumer/release
    obligations remain.'
  - Official released EgoLint continuity conformance is not claimed; only the pinned schema/headings/budget
    check is used.
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

This is a time-qualified operational handoff beneath user/runtime instructions, scoped instructions, live state and canonical sources. It records bounded #82 engineering evidence without replacing pending image, source/creative or release acceptance.

## Resume protocol

Read AGENTS, the #82 acceptance record, development guide and exact local receipts. Re-query main and owning issues before stacking. Preserve newer parallel changes and historical evidence; the current receipt describes exact executed bytes, not a containing-commit self-reference.

## Current objective and success conditions

Run the existing portable helper through an actual local workflow with real frontends and verified Task installation. Record deliberate version/dispatch faults and source/cache boundaries. Stop demonstrated insufficient Docker storage before pull/build while retaining the original full image gate.

## State snapshot

Stack base is `codex/80-browser-stack-20261122` at `d53427184c7646195f6bebc6289c4dcfdd191a3d`. Candidate `codex/82-setup-stack-20261122` is a draft child with no containing-revision or pre-PR self-reference. Domain receipts retain their exact independently represented source; stacking does not relabel earlier runs as tests of later code. Live main remains `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`.

## Completed and material changes

The development-image workflow gains a separate five-minute portable-entrypoints job with checksum-pinned Task and mandatory Make/Task coverage. The full qualify job remains. The dev qualifier records storage driver/free bytes and conservatively refuses insufficient or unknown capacity before pull/build; explicit measured overrides and remote bypass are documented. Sanitized source-bound act evidence and an actual storage refusal are retained under docs/work/82.

## Validation and review evidence

Actual local act 0.2.97 workflow execution passed verified Task 3.45.3 download/install and all five existing protocol tests, zero skipped, in 2.181 seconds. The fresh container used a pinned cached runner image, 2 CPUs/1 GiB, no Docker socket, explicit proxy bindings and a read-only public CA. Exact pinned action archives supplied local mirrors; hosted checkout/hardening are not claimed. Seven dev qualifier boundary tests pass. Actual full-image invocation fails safely at VFS storage preflight, with no pull/build. Documentation, pinned continuity schema/headings/budget and whitespace are checked before handoff.

## Blockers, risks, unknowns, and deferred work

Full default/non-root image qualification remains pending on a sufficiently provisioned Docker host; the local narrow job does not acquire real Rust/pnpm dependencies or build the product. Storage reserves are operational estimates, not capacity guarantees. Concurrent VFS layer copies caused an independently observed browser attempt to exhaust over 8 GiB. #70/#80/#88 retain separate engineering acceptance. #98 retains exact token/layer and formal source/governance assembly; #116 retains final release/consumer proof. No next version/tag/channel is selected or published here.

## Next dependency-ready work

Review and stack the independent engineering checkpoints while reconciling continuity semantically. Provide adequate Docker storage, check the resource budget, and run the original current-source default/custom qualifier without relabeling cached-image protocol coverage as full acceptance. Complete independent browser and product checks, then proceed through source/approval and immutable release qualification under #98/#116.

## Parallel changes and reconciliation

This checkpoint follows parent draft PRs #158 → #159. Review/merge parents before children and reconcile continuity semantically. The engineering parent owns tag admission, copied-executable isolation and portable policy references; each domain checkpoint retains its own actual qualification limits. All sprint branches remain for maintainer review.

## Privacy and redaction

Public technical facts and hashes only. Proxy values, certificate bytes, credentials and private local topology are excluded. Retained act logs replace host checkout/action-mirror paths and emulated correlation IDs; emulated run 1 is not a hosted workflow URL or run.

## Handoff update protocol

Refresh after actual checks and before handoff; validate pinned metadata, all twelve headings and byte/line budgets. Pinned Aether decision guidance was loaded with git show at dc8a16851f452763ef4f7fbe4bf057d4500b1921; Hygiene policy a05b14f8b9e2772124f879f818e09a911e996ad8 is retained. ADR not required: bounded execution coverage and resource refusal within the existing helper/qualification boundary, without product/source authority or support/approval changes.

## Compaction and supersession

Git and the owning issues retain history. Keep original acceptance gates and prior v1.0.0/source/approval receipts intact. Replace this snapshot after semantic reconciliation; never convert a failed or unrun image gate into a passing compatibility claim.
