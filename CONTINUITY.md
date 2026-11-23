---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-23T06:14:09.080304+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify actual local source-candidate archive download, isolated installation and pinned-consumer
    replacement/rollback without publishing or mutating real consumers.
  includes:
  - Bounded standard-library loopback transport/checksum/USTAR/new-prefix qualification and actual installed
    PATH commands.
  - Actual previous/new local source-candidate replacement, retained-output rollback and existing pinned
    Mantle authoring proof.
  - Archive/link/clobber/runtime/source-preservation negatives with source/binary/tool/evidence identity
    retained.
  excludes:
  - No official-release authentication, publication, version/tag selection, support-matrix promotion or
    other-platform claim.
  - No actual Identity source choices, creative/ADR approval, consumer pin changes, system/global installation
    or interrupted-recovery claim.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - docs/decisions/ADR-0019-immutable-release-contract.md
  - docs/releases/NEXT_RELEASE_MATRIX.md
  - scripts/qualify_local_install.py
  - scripts/verify_consumer_authoring.py
  - docs/consumers/MANTLE_AUTHORING_PROOF.md
  - docs/work/70/LOCAL_INSTALL_2026-11-23.md
  - docs/work/70/local-install-20261123/qualification.json
  - docs/work/70/timestamp-consistency-20261123/VALIDATION.md
work:
  objective: Qualify actual local source-candidate archive download, isolated installation and pinned-consumer
    replacement/rollback without publishing or mutating real consumers.
  success_conditions:
  - Reject altered/unsafe archives before creating a new isolated install; preserve existing/link targets.
  - Run actual installed baseline/new/rollback selections using distinct pinned binary bytes and preserve
    source.
  - Retain truthful local-native scope, absent-runtime behavior, reproducibility/drift and pending real
    source/release gates.
  active_issue:
    provider: github
    id: egohygiene/identity#70
    url: https://github.com/egohygiene/identity/issues/70
  next:
    kind: action
    id: review-local-install-evidence-and-reconcile-final-qualification
    description: Review this candidate mechanism with the timestamp/artifact checkpoint stack; obtain
      actual source choices and selected release/native-install evidence under existing70/98 before support
      claims.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/70
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    ref: refs/heads/main
    verified_at: '2026-11-23T06:12:36.089787+00:00'
  candidate:
    branch: codex/70-local-install-qualification-20261123
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-23T06:14:09.080304+00:00'
    default_branch_revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    issue_state: open
    pull_request_state: not-applicable
    notes: Identity163 through166 and Aether141/142 merged; provider mainad8fca5 checked. Timestamp draft167
      is open; this local-install child has noPRyet. Existing actual records retain their sources; no
      release/source approval is inferred.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#167
    url: https://github.com/egohygiene/identity/pull/167
  - provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  - provider: github
    id: egohygiene/identity#98
    url: https://github.com/egohygiene/identity/issues/98
review:
  status: partial
  reviewed_at: '2026-11-23T06:14:09.080304+00:00'
  reviewed_by: Codex
  evidence:
  - command: Focused local-install boundary unittest module
    outcome: passed
    observed_at: '2026-11-23T06:12:36.089787+00:00'
    notes: 11methods cover real loopback/checksum/redirect, bounded malformed and unsafe archives, ELF/input
      hashes, clobber/links, selected-executable mutation and unrelated initializer deletion.
  - command: Actual qualify_local_install.py atd0ff470 with candidate37ff6ca4 and priorf6a84021
    outcome: passed
    observed_at: '2026-11-23T06:08:15.418984+00:00'
    notes: Two15.69MB archives transferred/verified/installed;17PATHcommands, absentPython negatives,
      v0/incompletev1 prep, inspect/idle recovery and actual rollback pass. Same printed1.0.0 versions
      are byte-bound source candidates, not semver release upgrade.
  - command: Existing candidate consumer authoring proof on installed binary and unchanged pinned Mantle
    outcome: passed
    observed_at: '2026-11-23T06:08:15.418984+00:00'
    notes: Two fresh19-file output inventories agree;3read-only drift cases fail asrequired;14consumed
      input files match rawb08045a Git blobs. Originalconsumer/inputbinaries unchanged.
  - command: Full Python discovery with actual Make/Task; docs/syntax/receipt/privacy/continuity/whitespace
      checks
    outcome: passed
    observed_at: '2026-11-23T06:14:09.080304+00:00'
    notes: 249discovered:247passed/twoexisting skips,19.388s. Root independently reran11focusedcontrols
      and cleared final source afterDEFLATE fix. Packet contains no hostpath/proxy/credential data.
  environment_limitations:
  - NativeLinuxamd64 on one host; no minimumGNUlibc/distribution/macOS/Windows availability claim.
  - Source-candidate local transport does not authenticate compilation, a published release, signatures
    or attestation; separate build/source receipts retain provenance.
  - Inspect/completed-empty recovery only here; actual interrupted-process recovery retains native integration
    proofs.
  - Actual Identity source decisions/new human review times and selected release/publication/consumer-upgrade
    acceptance remain pending.
  - Pinned continuity schema/headings/budgets are structural checks, not released EgoLint conformance.
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

User/runtime and scoped instructions, live provider evidence and canonical source outrank this snapshot. This is local development qualification, not new release or creative authority.

## Resume protocol

Read AGENTS, existing release/consumer contracts and LOCAL_INSTALL_2026-11-23. Verify main and active PRs before resuming. Prior163→166 and Aether141/142 are merged; preserve their exact source-bound evidence and original checkouts.

## Current objective and success conditions

Qualify actual local source-candidate archive download, isolated installation and pinned-consumer replacement/rollback without publishing or mutating real consumers.

## State snapshot

Base/main isad8fca58946ca03f6f07d13be6c64046216569d0. Candidate branchcodex/70-local-install-qualification-20261123 has no containing-revision or pre-PR self-reference. Actual product source isd159c680/new37ff6ca4 versuspreviousedca416/f6a84021; proof tool isd0ff470, with later docs distinct.

## Completed and material changes

The new standard-library developer harness serves controlled archives on loopback, independently checks their expected digests, admits only a bounded single regular executable and installs only into fresh private prefixes. Real PATH commands exercise baseline/new/rollback selection, initialization, missing runtime, inspection and idle recovery. It reuses the existing consumer authoring proof rather than inventing source or approvals.

## Validation and review evidence

Eleven focused boundary controls pass. Actual fixed-source proof transfers two15.69MB archives and passes17installed commands, with per-command executable hashes. New and previous19-file Mantle output inventories agree asan observed metric; retained prior outputs/binary verify after rollback. Fourteen source inputs match rawpinned Git blobs; two fresh generations and3readonly drift negatives pass. Full Python249 completes247passes/two existing skips with actualMake/Task. Docs/syntax/hashes/privacy/whitespace and independent root review pass. See the exact receipt/hash index. Root review found invalidDEFLATE escaped the original gzipcatch; zlib.error is now handled and the exact regression/fresh proof pass.

## Blockers, risks, unknowns, and deferred work

This is one native Linuxhost and local candidate artifacts, not official-release download/authentication or broader distribution/install support. No stable version/tag, signing, provenance attestation, deployment or real consumer pin is selected. Actual Identity source questions remain pending. Recovery here is completed/empty state, not a new interrupted-process proof.

## Next dependency-ready work

Review the local install packet and reconcile with timestamp/artifact fixes; qualify the exact final merged source and selected release cohorts. Bind actual self-source choices only when supplied. #98 retains actual release/live/restore/contrasting-consumer acceptance; #116 reconciles last.

## Parallel changes and reconciliation

Timestamp draft167 coded159c680 and docs bef3411 are retained as parents. Root owns actual artifact-adapter work, final stack and mutable issue reconciliation. Reconcile continuity by meaning before stacking; do not relabel prior code/binary/tool executions as tests of a later integration revision.

## Privacy and redaction

Public source identities, hashes and bounded outcomes only. No private host paths, proxy values, certificate/key bytes or transcript are committed. Receipt command paths are normalized; actual logs remain task-local. Only private disposable installation/consumer copies are mutated.

## Handoff update protocol

Refresh after domain checks, inspect actual diff, validate pinned schema/twelve headings/size budgets and preserve exact evidence scopes. Reference ADR0011/0019; ADR not required for bounded proof of existing contracts. Pinned Aether decision2.1.0/continuity1.1.0 and Hygiene1.2.0 remain selected, without lifecycle promotion.

## Compaction and supersession

Git and canonical work records retain earlier observations. Replace stale current-state prose rather than append chronology, preserving exact source, approval and release boundaries.
