---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-23T06:02:13.695231+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Enforce the existing complete source date-time contract consistently across approval, capture,
    design-reference and channel metadata validation.
  includes:
  - Share the unchanged approval grammar/calendar check through common.py while preserving the standalone
    approval facade.
  - Reject invalid declared source capture/review times using existing diagnostic families; retain prior
    incomplete-origin findings.
  - Retain actual immutable-before/current isolated-script controls, source-preserving Python/native regressions
    and exact code/log/binary identities.
  excludes:
  - No date-only lifecycle/release or broader publisher string semantics, source timestamp rewrites, owner
    choices or invented human/capture events.
  - No schema identifier, dependency, approval/ADR lifecycle, root source adoption, release, hosted CI
    or deployment change.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - contracts/v1/approvals.schema.json
  - contracts/v1/provenance.schema.json
  - contracts/v1/design-references.schema.json
  - contracts/v1/channel-registry.schema.json
  - scripts/identity_validation/common.py
  - scripts/identity_validation/governance.py
  - scripts/identity_validation/guidance.py
  - scripts/identity_validation/handbook.py
  - scripts/identity_validation/channels.py
  - scripts/validate_identity.py
  - docs/work/70/timestamp-consistency-20261123/VALIDATION.md
  - docs/work/70/timestamp-consistency-20261123/checks.json
  - docs/work/70/timestamp-consistency-20261123/before-after.json
work:
  objective: Enforce the existing complete source date-time contract consistently across approval, capture,
    design-reference and channel metadata validation.
  success_conditions:
  - Reject formerly accepted date-only/naive/coerced source date-time values without changing source bytes
    or public diagnostic families.
  - Accept declared lowercase UTC/fraction/offset forms and retain the approval import facade, date-only
    lifecycle semantics and old incomplete-origin diagnostics.
  - Prove actual standalone/native/CLI refusal before output/cache mutation without changing actual approval
    facts.
  active_issue:
    provider: github
    id: egohygiene/identity#70
    url: https://github.com/egohygiene/identity/issues/70
  next:
    kind: action
    id: reconcile-current-source-quality-and-install-proof
    description: Review this bounded repair with the independent local artifact transport and installation
      checkpoints, then continue final current-source/native qualification. Resolve exact owner choices
      before actual self-source adoption.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/70
    - https://github.com/egohygiene/identity/issues/98
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    ref: refs/heads/main
    verified_at: '2026-11-23T06:02:13.695231+00:00'
  candidate:
    branch: codex/70-timestamp-consistency-20261123
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-23T06:02:13.695231+00:00'
    default_branch_revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh provider reads verify mainad8fca5 and issue70open, with no open Identity PR at observation.
      This candidate has no PR yet; the actual tested code is d159c68 and later changes are evidence/continuity
      only.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-23T06:02:13.695231+00:00'
  reviewed_by: Codex
  evidence:
  - command: Full Python discovery with IDENTITY_REQUIRE_FRONTENDS=1
    outcome: passed
    observed_at: '2026-11-23T06:02:13.695231+00:00'
    notes: 238discovered:236passed/two existing optionalexperience/nativeWindows skips; actualMake and
      pinnedTask3.45.3 available. Focused validator/channel28methods pass.
  - command: cargo fmt; strict locked offline all-target/all-feature Clippy; locked offline all-feature
      cargo test
    outcome: passed
    observed_at: '2026-11-23T06:02:13.695231+00:00'
    notes: 119native passes/four explicithelper-only ignores, jobs1. Six new actual CLI/library date-only/naive
      origin/guidance/reference rejection cases preserve changed source, output sentinel and cache boundary.
      Code bytes audited to d159c68.
  - command: Actual immutablead8 versus repaired standalone via Python-I-S on disposable fictional consumers
    outcome: passed
    observed_at: '2026-11-23T06:02:13.695231+00:00'
    notes: 'Twelve controls: eight former bare-date acceptances nowreject; lowercase reference UTC repaired;
      approval facade, date-only lifecycle and prior incomplete-origin diagnostics preserved. Original
      fixture and every copied source remain unchanged.'
  - command: Bundle drift, extraction/provenance, docs, whitespace and independent source/tests review
    outcome: passed
    observed_at: '2026-11-23T06:02:13.695231+00:00'
    notes: Checks pass and no code/test review blocker. Exact nine code inputs plus test/raw-log/local-binary
      hashes are retained in checks.json. Actual self-source proposal still has exactly two missing-review
      findings.
  environment_limitations:
  - Local Linux execution and test binary identity do not establish downloaded/signed releases, other
    native platforms or hosted CI.
  - Existing parser leap-second limitation remains; syntactic capture/review time validity does not prove
    an event occurred.
  - Date-only since/release.date and publisher/view-model nonempty origin strings retain separate unchanged
    contracts.
  - Actual self-source owner choices/review instants remain outside this engineering repair; no unknown
    value is filled.
  - Pinned continuity schema/headings/budgets are structural checks, not released EgoLint continuity conformance.
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

User/runtime and scoped instructions, live evidence and canonical sources outrank this operational checkpoint. It records an existing validity repair, not a new approval or timestamp policy.

## Resume protocol

Read AGENTS, the five canonical validator modules, curated date-time schemas and timestamp-consistency VALIDATION/checks records. Recheck main, issue70 and any new draft peers before continuing. Earlier domain receipts retain their exact source and scope.

## Current objective and success conditions

Enforce the existing complete source date-time contract consistently across approval, capture, design-reference and channel metadata validation.

## State snapshot

Base/live main isad8fca58946ca03f6f07d13be6c64046216569d0. Candidate codex/70-timestamp-consistency-20261123 has no containing-revision or pre-PR reference. Executed code bytes equal d159c680e6161e85854fd45c255d4196aec5c34f; later additions are evidence and continuity, not relabeled executions.

## Completed and material changes

The existing approval parser is shared through common.valid_rfc3339_timestamp, with valid_review_timestamp retained. Declared asset origins, shared guidance provenance, design references and registry reviews now enforce complete offset-bearing string/calendar validity. Existing codes, source bytes and incomplete-origin findings remain. The generated offline standalone/native preflight bundle is regenerated.

## Validation and review evidence

Full Python238 completes236passes/two existing skips; focused28methods pass. Native119passes/four helper-only ignores, strictClippy and format pass. Actual CLI/library negatives preserve changed source, output sentinel and cache. Twelve immutable-before/current isolated-script controls show eight formerly accepted bare-date bindings rejected, valid lowercase UTC repaired, and old facade/date-only/incomplete-origin behavior preserved. Bundle, extraction, docs, whitespace and independent source/tests review pass; exact code/log/binary identities are retained.

## Blockers, risks, unknowns, and deferred work

This is local declared-contract enforcement only. Leap seconds retain the old parser limitation. Date-only lifecycle/release and broader publisher-origin strings are not reinterpreted. Actual owner choices and missing review instants remain unknown. Other native/install, local artifact transport, final merged-source quality and release/publication proof retain their owners.

## Next dependency-ready work

Review this repair with independent artifact-transport and installation proof, then reconcile final current-source quality/native coverage under70. Existing98 source review must precede actual root adoption and successful self-kit generation;116 closes last.

## Parallel changes and reconciliation

No open Identity PR was observed in the fresh provider read. Root coordinates independently scoped artifact/installation and Aether portability branches; this child changes only timestamp validation/tests/evidence. Reconcile continuity by meaning before stacking; preserve every domain receipt's actual source and qualification limits.

## Privacy and redaction

Public schema/code facts, fictional fixture mutations and bounded checks only. Public records retain hashes rather than private task logs or host topology. No transcript, proxy values, credentials, personal context or actual review-time inference is recorded.

## Handoff update protocol

Refresh after domain checks before PR handoff; verify pinned schema, twelve headings and fixed budgets. Decision impact references ADR-0001/ADR-0005/ADR-0012; no new model, schema identity or policy direction is selected. Pinned Aether decision2.1.0/continuity1.1.0 and Hygiene1.2.0 were read at their immutable revisions.

## Compaction and supersession

Git and linked work records retain prior observations. Replace current operational prose rather than append chronology; preserve historical source bindings, human dispositions and unresolved owner facts.
