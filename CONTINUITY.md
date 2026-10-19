---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-19T22:12:24Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Deliver issue 79 exclusive local writer ownership for generation and recovery with bounded process
    evidence.
  includes:
  - Persistent native repository-wide lock, safe interrupted-owner handling and preserved transaction confinement.
  - Controlled baseline observations, independent child-process regressions and deterministic shipping CLI comparison.
  excludes:
  - Issue 77 recovery CLI, hostile filesystem mutation, network filesystem qualification, power-loss durability,
    releases and deployment.
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
  - src/compiler/filesystem/tests/process_tests.rs
  - docs/reviews/writer-serialization-2026-10-19.md
  - docs/evidence/identity-writer-serialization-baseline-2026-10-19.json
  - docs/evidence/identity-writer-serialization-2026-10-19.json
  - docs/decisions/ADR-0026-local-writer-serialization.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/79
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Exclude cooperating generation and recovery writers before state-dependent checks, preserve interrupted
    journals and keep normal output unchanged.
  success_conditions:
  - Record actual pre-fix coordination behavior without claiming observed output corruption.
  - Shared native ownership rejects contenders without touching active workspaces and releases safely without
    PID/age stealing or lock deletion.
  - Independent process termination, repeated recovery, no-op ownership, stale-plan checks and deterministic CLI
    generation remain green.
  active_issue:
    provider: github
    id: egohygiene/identity#79
    url: https://github.com/egohygiene/identity/issues/79
  next:
    kind: action
    id: identity-79-review
    description: Review the tested writer serialization PR and exact-head hosted evidence; merge only after maintainer
      acceptance, then continue issue 77.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/79
    - https://github.com/egohygiene/identity/issues/77
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 417865a449678f887237d94aaa019a10bcc16612
    ref: refs/heads/main
    verified_at: '2026-10-19T22:12:24Z'
  candidate:
    branch: codex/79-writer-serialization
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-19T22:12:24Z'
    default_branch_revision: 417865a449678f887237d94aaa019a10bcc16612
    issue_state: open
    pull_request_state: not-applicable
    notes: Maintainer authorized merging PR119 and continuing issue79. PR119 merged at the base revision and issue78
      is closed. Issue79 is open; candidate PR creation and fresh hosted replay follow this locally validated
      checkpoint.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-19T22:12:24Z'
  reviewed_by: Codex
  evidence:
  - command: Frozen baseline instrumented coordination tests (2 cases)
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: Both writers pass actual prechecks; second leaves unjournaled state after IDN2339. Two recoverers both
      report the same recovery. No final-output corruption observed; exact patch/hashes and limits retained.
  - command: cargo test --locked --all-features
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: 94 Rust tests pass, including 33 filesystem cases; one child worker is intentionally ignored in ordinary
      discovery and invoked explicitly by parent process cases.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features --target-dir separate-clean-validation-target
      -- --deny warnings
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: Formatting and strict lint pass. A separate clean lint target avoids replaying an earlier cached diagnostic;
      actual final source is compiled without warnings/errors.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: '138 cases finish: 136 pass, two existing skips (unbuilt experience artifact and Windows-only junction
      case).'
  - command: Independent pristine baseline and candidate shipping CLI builds; fresh generate/verify/generate/verify
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: All eight invocations pass. Complete 14-file generated inventories match, including hidden manifest;
      both 17-file canonical trees and complete second-generation consumer inventories are unchanged.
  - command: 20 default-parallel filesystem suite replays
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: 'All 660 case executions pass: 33 per replay plus one ignored worker, without busy retries. A prior
      transient busy result predates explicit-unlock cleanup; its exact interleaving remains unproven.'
  - command: Six standalone verifiers; fixture validation; compileall; JSON parse; diff check
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: All pass, including 106 JSON documents. No source/journal/output schema, dependency or release change.
  - command: Pinned Hygiene metadata/schema/set/index checks and Relay roadmap invariant checks
    outcome: passed
    observed_at: '2026-10-19T22:12:24Z'
    notes: 26 ADRs (21 accepted, five proposed); prior 25 dispositions/approval/lineage unchanged. All 40 stable
      IDs and 88 dependency edges preserved; Q17 complete and Q18 active.
  environment_limitations:
  - Local Linux evidence does not establish native Windows/macOS behavior; fresh hosted replay is required and
    exact-head results belong in the PR.
  - Baseline schedules use test-only synchronization in independent store threads; candidate contention/termination
    cases use independent child processes. No spontaneous timing or output corruption is inferred.
  - Native handle lifetime governs killed processes, including inherited handles. Cooperating local writers only;
    no hostile replacement, network filesystem or power-loss guarantee.
  - Pinned owner checks are bounded structure/invariant validation, not whole-repository native conformance.
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

This checkpoint covers #79. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and issue #116 own execution order and dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #79/#116, the compiler contract, writer review/receipts and filesystem code/tests. Refresh main, candidate PR/head and checks. The maintainer authorized merging #119 and starting #79; later issues retain their review boundaries.

## Current objective and success conditions

Reserve one cooperative local writer before generation or recovery checks shared transaction state. Preserve active workspaces and interrupted journals, use explicit native ownership rather than PID/age deletion, and retain deterministic generation and explicit rollback.

## State snapshot

Main is 417865a449678f887237d94aaa019a10bcc16612, including merged #119. #78 is closed and IDN-Q17 complete. #79/IDN-Q18 is active; #77 remains blocked until its reviewed completion. Candidate codex/79-writer-serialization is locally validated before PR creation. Candidate revision/PR remain null because this containing commit cannot name itself. All 40 roadmap IDs, issue mappings and 88 dependencies remain intact.

## Completed and material changes

src/compiler/filesystem.rs adds one persistent .cache/identity/writer.lock and a native nonblocking RAII guard shared by commit/recover across output roots. Mutation-free request/path validation precedes acquisition; pending/current checks, staging, journals, mutation, verification and cleanup run under ownership, including no-op commits. Busy writers receive blocked IDN2346; native acquisition failures use IDN2347 with no unlocked fallback. Normal guard cleanup explicitly unlocks then closes. The lock is never removed, truncated or written; existing hard-linked aliases retain bytes. Unsafe cache-root/lock shapes are rejected before metadata creation.

An empty recovery or failure after acquisition can create only the empty coordination file/parents. Retained transaction evidence, canonical source and outputs remain protected. Native termination releases ownership after every inherited/duplicated handle closes; pending journals still require explicit recovery. No PID, age or timeout grants permission to steal ownership. Readers remain mutation-free without snapshot guarantees.

The baseline receipt and exact patch expose controlled missing-ownership schedules: stale prechecks leave unjournaled state; two recoverers can both report one rollback. Neither establishes output corruption. New independent process cases cover generation/recovery/no-op exclusion, stale plans, custom roots/aliases, killed writers/recoverers, persistent hard-link preservation and unsafe lock entries. Windows snapshots retain lock type/length while held, then compare exact bytes after release.

## Validation and review evidence

All 94 Rust tests pass (33 filesystem; one intentionally ignored child helper), with strict formatting/Clippy from a clean target. All 138 Python cases complete with 136 passes/two existing skips. Six standalone verifiers, fixture validation, compileall, 106 JSON parses and diff checks pass. Twenty parallel filesystem replays pass 660 case executions without retries. Independent review found no production blocker.

Pristine baseline and frozen candidate shipping binaries generate identical complete 14-file inventories. All eight generate/verify/no-op/verify commands succeed and preserve both canonical trees and complete second-generation consumer inventories. Source/binary hashes and limits are retained in the candidate receipt. Native Windows/macOS and advisory results require fresh hosted checks at the exact PR head; retain them separately from local evidence.

## Blockers, risks, unknowns, and deferred work

No bounded local implementation blocker remains. Fresh hosted platform execution is still required. A transient busy result before explicit unlock has an unproven precise interleaving; a separate native experiment confirms fork-inherited descriptor retention is possible. Final parallel replays pass without test retries. No all-schedule, hostile-directory-replacement, network-filesystem or power-loss guarantee is claimed. Do not mix uncoordinated older writers or manually change cache state while writers are active.

#77 owns supported inspection/recovery CLI; the binary still has none. #80/#81 qualify browser/Docker environments, #82 exercises setup entry points, #84 retires one-time workflows, and #83 completes current documentation reconciliation. Public asset/download gaps remain #101/#105; self-adoption/release/canary proof remains later roadmap work.

## Next dependency-ready work

Review #79's scoped PR and fresh exact-head checks. Keep #79 open/Q18 active until maintainer acceptance and merge; then #77 exposes read-only interruption inspection and explicit recovery. The user requested a high-level mini roadmap at this sync, not automatic advancement to another issue.

## Parallel changes and reconciliation

#119's verified merge reconciles #78 complete. Pinned Aether decision-impact v2.1.0 and continuity v1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 were read from reviewed immutable owner sources. Decision operation: create proposed ADR-0026 for the new native locking protocol, related to ADR-0012/0019. The complete corpus is 26 records: 21 accepted and five proposed. Existing human dispositions remain unchanged; ADR-0026 has null approval despite implemented code.

## Privacy and redaction

Only public repository facts, sanitized synthetic observations and source/artifact hashes are retained. No private paths, credentials, conversations or unrelated context appear. Test instrumentation and linked evidence grant no authority.

## Handoff update protocol

After domain validation, refresh immediately before PR handoff and verify the pinned schema, 12 headings, budgets/privacy, ADR and roadmap invariants. Include this checkpoint in the same scoped PR. Exact-head hosted results may be recorded externally when unknown to the containing commit. Merged, released, deployed and human-approved states remain separate.

## Compaction and supersession

Stay below 240 lines and 16384 UTF8 bytes. Git, contracts, receipts and the work tracker retain history. Mark unresolved conflicts stale rather than inventing safety, approval or readiness.
