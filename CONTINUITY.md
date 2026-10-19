---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-19T20:32:52Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Deliver issue 78 transaction-path confinement with bounded runtime evidence and preserved recovery.
  includes:
  - Fixed local cache contract; per-operation transaction/output checks, fresh workspace/file reservations
    and Windows reparse-point rejection.
  - Baseline/current runtime evidence, regression tests and reconciliation of completed issue 99.
  excludes:
  - Issue 79 writer serialization, hostile concurrent filesystem mutation, issue 77 recovery CLI, releases,
    deployment and public-kit follow-ups.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/contracts/COMPILER_V1.md
  - src/compiler/filesystem.rs
  - src/compiler/filesystem/tests.rs
  - docs/reviews/transaction-confinement-2026-10-19.md
  - docs/evidence/identity-transaction-confinement-2026-10-19.json
  - docs/decisions/ADR-0012-local-layered-identity-v1.md
  - docs/decisions/ADR-0019-immutable-release-contract.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/78
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Enforce the existing repository-local/no-link transaction contract before unsupported path writes
    while preserving deterministic generation and interrupted recovery.
  success_conditions:
  - Record actual baseline behavior without inferring an exploit; all unsafe preexisting cache/staging/backup
    paths fail without changing consumer or external sentinels.
  - Use fresh transaction leaves and exact path authority; metadata failures and Windows reparse points cannot
    become supported redirected caches.
  - Valid generation remains byte-identical to baseline; legitimate interrupted, repeated and custom-root recovery
    passes.
  active_issue:
    provider: github
    id: egohygiene/identity#78
    url: https://github.com/egohygiene/identity/issues/78
  next:
    kind: action
    id: identity-78-review
    description: Review the tested confinement PR, then merge only after maintainer acceptance; issue 79 writer
      serialization is the next scheduled work.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/78
    - https://github.com/egohygiene/identity/issues/79
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 8816294e9d9c43f250d771e9fa627c4b1861e78a
    ref: refs/heads/main
    verified_at: '2026-10-19T20:32:52Z'
  candidate:
    branch: codex/78-transaction-confinement
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-19T20:32:52Z'
    default_branch_revision: 8816294e9d9c43f250d771e9fa627c4b1861e78a
    issue_state: open
    pull_request_state: not-applicable
    notes: 'PR #118 merged at observed main and issue #99 closed. No open PR was returned by the scoped PR
      search before creating this issue #78 candidate. Issue73 prerequisite is closed.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-19T20:32:52Z'
  reviewed_by: Codex
  evidence:
  - command: Frozen baseline CLI v1-generate with four disposable cache/workspace symlink cases
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: Baseline 8816294 and binary hash are recorded in the receipt. All static cases reject with IDN2311/IDN2301
      and preserve both trees. Ten failed timing injections are explicitly inconclusive, not a safety pass
      or confirmed exploit.
  - command: cargo test --locked --all-features; final namespace confinement case rerun
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: 84 Rust tests pass, including 23 filesystem cases. Existing interruption/recovery checks remain;
      direct namespace, fresh-file/hard-link, parent/leaf redirection and special-entry checks preserve sentinels.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features -- --deny warnings
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: Pinned Rust 1.97.1 formatting and all-target/all-feature strict lint pass.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: '138 cases complete: 136 pass and two existing skips (unbuilt experience artifact and Linux-inapplicable
      Windows junction case).'
  - command: Independent baseline/candidate fresh CLI generation and verification
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: Both binaries generate identical complete 14-file inventories, including hidden manifest; both verify
      and preserve canonical fixture files. Actual binary/source hashes are recorded separately.
  - command: Six standalone docs/release/mascot/publication/extraction verifiers; compileall and diff check
    outcome: passed
    observed_at: '2026-10-19T20:32:52Z'
    notes: All pass. Repeated documentation check covers the new receipt/review links. No release, publication,
      source schema, journal schema or ADR lifecycle change occurs.
  environment_limitations:
  - Local runtime is Linux; Windows junction regression execution and macOS/Windows release gates remain fresh
    hosted requirements for the final candidate.
  - 'Failed timing injection does not reproduce or disprove a race. Pathname checks are not atomic against
    hostile directory replacement; issue #79 retains writer serialization.'
  - Pinned ADR/continuity/roadmap checks are bounded validation, not whole-repository native conformance. Exact-head
    hosted evidence belongs in the PR when available.
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

This checkpoint covers #78. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and issue #116 own execution order and dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #78/#116, compiler transaction contract, confinement review/receipt and filesystem code/tests. Refresh main, candidate PR/head and checks. The maintainer authorized merging #118 and starting #78; later issues retain their review boundaries.

## Current objective and success conditions

Enforce the existing fixed repository-relative transaction cache with useful failures and complete input preservation. Confirm actual baseline behavior, strengthen per-operation checks and retain legitimate generation/recovery. Keep source validity, generated state, concurrency safety and release state distinct.

## State snapshot

Main is 8816294e9d9c43f250d771e9fa627c4b1861e78a, including merged #118. #99 is closed and IDN-Q29 complete. #78/IDN-Q17 is active; prerequisite #73 is closed. Candidate codex/78-transaction-confinement has no containing SHA/PR until created. #79/IDN-Q18 remains blocked until #78 completes; no writer lock is claimed. All 40 roadmap IDs/dependencies remain intact.

## Completed and material changes

src/compiler/filesystem.rs rejects inspection errors, nonregular components, symlinks and all Windows reparse points. Native components retain exact UTF8 semantics instead of lossy slash replacement. Transaction helpers remain beneath .cache/identity/transactions and promotion beneath the independently authorized output root. New plan directories and create_new transaction leaves prevent accidental reuse or truncation of existing staging/backups/journals. Journal publication, recovery temporary writes and cleanup recheck authority. Recovery retains complete preflight, legacy-journal rejection and unlink-before-recreate behavior.

COMPILER_V1.md makes the existing fixed local cache contract explicit: no external-root option, linked fallback or automatic relocation. Serialized local pathname checks do not promise atomic protection against another process replacing directory components. Ordinary rename support is still required; failures retain recovery evidence.

The new review/receipt records actual baseline rejection of four pre-planted Unix redirects, with both trees unchanged. No current static redirected-write exploit is established. Ten timing attempts did not achieve injection and are inconclusive. New tests exercise every cache component, staged/backup parents/leaves, file/hard-link collisions, namespace escapes, special entries and legitimate recovery. Windows-specific junction tests await native execution.

## Validation and review evidence

All 84 Rust tests and strict all-target/all-feature lint/format checks pass; the final namespace case was rerun after its portable-vector correction. All 138 Python cases finish with 136 passes/two explained skips. Six standalone verifiers, compilation and diff checks pass. Two fresh baseline/current CLI trees are byte-identical across 14 files and both verify without changing canonical source. The pinned schema/helper check validates continuity, all 40 stable roadmap steps and all 25 ADRs before handoff. Hosted results remain separate exact-head evidence in the PR.

## Blockers, risks, unknowns, and deferred work

No bounded local implementation blocker remains. Local Windows/macOS execution is unavailable; hosted platform gates remain required. This does not establish concurrent-writer safety, hostile filesystem topology confinement or power-loss durability. #79 owns writer serialization; #77 later exposes supported inspection/recovery CLI. The current binary CLI still has no recovery command.

G03/G04 public asset/download work remains #101/#105, with complete-kit/self-adoption/release/upgrade proof under later roadmap owners. Proposed ADR-0025 remains proposed/null approval. Merging #118 completed the bounded authoring milestone without accepting an ADR or publishing a release.

## Next dependency-ready work

Review the #78 draft and exact-head hosted checks. Merge only after maintainer acceptance, then refresh the roadmap and sync on #79 writer serialization. Keep #78 open and Q17 active while this candidate is under review.

## Parallel changes and reconciliation

No other open PR was returned by the scoped PR search before candidate creation. The completed #99 handoff is reconciled against its verified merge. Pinned Aether decision-impact v2.1.0 and continuity v1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 were read directly through GitHub. Decision operation: reference ADR-0012/0019; localized enforcement of the existing no-link/local-output contract needs no duplicate ADR. All 25 existing records and human dispositions remain unchanged. Independent read-only review found no blocker in the bounded implementation.

## Privacy and redaction

Only public repository facts, sanitized synthetic observations and source/artifact hashes are retained. No private paths, credentials, conversations or unrelated context appear. Failed probes do not become inferred attacks; linked evidence grants no authority.

## Handoff update protocol

After domain validation, refresh this file immediately before PR handoff and verify schema, 12 headings, budgets/privacy and roadmap references through pinned owner tools. Record exact PR/head/hosted results externally when not knowable by the containing commit; no commit must contain its own SHA. Merged, released, deployed and approved remain distinct.

## Compaction and supersession

Stay below 240 lines and 16384 UTF8 bytes. Git, contracts, the review receipt and work tracker retain history. Mark unresolved conflicts stale rather than inventing safety, approval or readiness.
