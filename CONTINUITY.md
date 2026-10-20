---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T01:06:41Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Deliver issue 77 read-only interruption inspection and explicit standalone CLI recovery.
  includes:
  - Human-only v1-inspect/v1-recover, shared full recovery preflight, native read-only inspection and independently
    authorized output scope.
  - Standalone regression tests, actual interrupted compiler replay, preserved generation and scoped consumer
    documentation.
  excludes:
  - New machine-readable inspection schema, automatic rollback, brand-source repair, other roadmap issues, release,
    deployment and stronger durability guarantees.
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
  - docs/consumers/RECOVERY.md
  - src/cli.rs
  - src/commands.rs
  - src/compiler/filesystem.rs
  - tests/consumer_recovery.rs
  - src/compiler/filesystem/tests/inspection_tests.rs
  - docs/reviews/consumer-recovery-2026-10-19.md
  - docs/evidence/identity-consumer-recovery-2026-10-19.json
  - migration/empathy-extraction-evolution-v1.json
  - docs/decisions/ADR-0026-local-writer-serialization.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/77
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Let a standalone consumer inspect retained transaction evidence without changes, explicitly roll
    back validated interrupted state and regenerate safely.
  success_conditions:
  - Inspection creates no metadata and preserves all canonical/generated/journal/backup/unrelated bytes; active
    or damaged evidence fails with actionable diagnostics.
  - Explicit recovery uses fresh exclusive ownership and complete batch preflight under independently supplied
    output scope, even if source or Python is unavailable.
  - Real interrupted compiler evidence, standalone default/custom-root workflows and normal incremental generation
    preserve complete inventories.
  active_issue:
    provider: github
    id: egohygiene/identity#77
    url: https://github.com/egohygiene/identity/issues/77
  next:
    kind: action
    id: identity-77-review
    description: Review the scoped inspection/recovery PR and fresh hosted platform evidence; merge only after
      maintainer acceptance. Issue81 is next in the execution order.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/77
    - https://github.com/egohygiene/identity/issues/81
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 44bf13bc45916d51ae5de10e9af2ce894d3be486
    ref: refs/heads/main
    verified_at: '2026-10-20T01:06:41Z'
  candidate:
    branch: codex/77-consumer-recovery
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-20T01:06:41Z'
    default_branch_revision: 44bf13bc45916d51ae5de10e9af2ce894d3be486
    issue_state: open
    pull_request_state: not-applicable
    notes: Maintainer authorized merge120 and continuation77. PR120 merged at the base revision and issue79 is
      closed. Issue77 is open. No other open PR was returned before candidate publication; fresh exact-head hosted
      evidence follows this local checkpoint.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-20T01:06:41Z'
  reviewed_by: Codex
  evidence:
  - command: cargo test --locked --all-features --target-dir separate-clean-validation-target
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: 112 Rust cases pass, including 42 filesystem and 9 standaloneCLI cases. Three ignored helpers are explicit
      producers/owners, not counted as passing coverage.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features --target-dir separate-clean-validation-target
      -- --deny warnings
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: Formatting and strict lint pass. Independent clean targets avoid earlier stale shared-artifact observations;
      no busy/spawn retry was added.
  - command: Dated Linux recovery proof using actual compiler test worker and copied shipping CLI
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: 24 invocations pass across default/custom roots. Producer pauses after real journal publication/first
      promotion, is killed/reaped, and journal remains unchanged until explicit recovery. Active contenders fail;
      inspection changes nothing; recovery/repeat/regeneration/verification preserve source and unrelated files.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: '138 cases finish: 136 pass/two existing skips (unbuilt experience artifact and Windows-only junction
      case).'
  - command: Six standalone verifiers; source fixture; compileall/py_compile; JSON parse; diff check
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: All pass, including 105 JSON files. Original extraction manifest/digests and v0 behavior are preserved;
      three existing evolution entries record CLI77 changes.
  - command: Independent read-only review and Unix CLI output-root regression
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: No remaining production blocker. Lossy UTF8/global backslash normalization was fixed; all four commands
      reject raw invalid scopes before coordination metadata or mutation, including retained transactions for
      the portable spelling. Final dedicatedCLI9pass/1ignoredhelper.
  - command: Pinned owner ADR/roadmap checks before handoff
    outcome: passed
    observed_at: '2026-10-20T01:06:41Z'
    notes: All26 existing ADRs retain dispositions, approval and lineage. ROADMAP preserves40 IDs,88 edges and
      issue mappings; Q18complete,Q16active,Q26dependency-ready without authorizing refactor work.
  environment_limitations:
  - Local Linux evidence does not establish native Windows/macOS behavior; fresh hosted replay is required and
    exact-head results belong in the PR.
  - The real journal producer uses an explicit cfg(test) pause, not spontaneous shippingCLI timing. Separate integration
    journals are labeled synthetic.
  - Missing-lock inspection is an uncoordinated observation; recovery always obtains fresh exclusive authority.
    No hostile filesystem, network filesystem or power-loss guarantee.
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

This checkpoint covers #77. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and issue #116 own execution order and dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #77/#116, compiler/consumer recovery contracts and dated review/receipt. Refresh main, candidate PR/head and checks. The maintainer authorized merging #120 and starting #77; subsequent issues retain review boundaries.

## Current objective and success conditions

Expose read-only interruption inspection and explicit validated rollback to standalone consumers. Preserve canonical/unrelated files and retained evidence, enforce exact independently supplied output scope, and allow recovery even when source or Python is unavailable. Regeneration remains a separate source-validated action.

## State snapshot

Main is 44bf13bc45916d51ae5de10e9af2ce894d3be486, including merged #120. #79 is closed/Q18 complete; #77/Q16 is active. Candidate codex/77-consumer-recovery is locally validated before PR creation. Candidate revision/PR remain null because this containing commit cannot name itself. All 40 roadmap IDs/88 dependencies/issue mappings remain intact. Q26/#87 is dependency-ready but deferred by the agreed post-kit priority; it is not authorized work.

## Completed and material changes

cli.rs/lib.rs/commands.rs expose human-only v1-inspect and v1-recover using existing repository/output-root options. Both bypass brand-source/Python loading; generation/verification keep full preflight. Transaction error output includes existing path/recovery guidance and actual command names. No JSON report/schema or automatic rollback is added.

filesystem.rs factors complete enumeration/preflight/conflict checks for both inspection and recovery. Inspection opens only an existing lock read-only, holds a shared native guard through observation and creates/changes/cleans nothing. Missing-lock observations are qualified and rechecked; a newly appearing lock causes full rerun under shared ownership. Explicit recovery always uses fresh exclusive ownership and the existing rollback. Active, invalid, legacy or wrong-scope evidence fails while preserving retained state.

The shared CLI scope helper rejects invalid UTF8 and retains literal Unix backslashes for portable rejection; native Windows separators normalize consistently. This fixes a review-discovered authority alias before exposing destructive recovery. The original extraction baseline remains immutable; three evolution entries record the changed CLI hashes and rationale. Consumer/help/compiler/architecture docs and unreleased notes describe the same route and distinguish source capability from old stable release bytes.

## Validation and review evidence

All 112 Rust cases pass from an independent clean target, including 42 filesystem and 9 shippingCLI cases; three helpers are intentionally ignored during ordinary discovery. Strict format/Clippy pass. Python finishes 138 cases with 136 passes/two existing skips. Six verifiers, source fixture, compileall/py_compile,105 JSON parses and diff checks pass. Independent review found no remaining production blocker.

The dated replay uses actual source loading, adapters and compiler execution with a test-only first-mutation barrier, then kills/reaps the producer. The copied unmodified shippingCLI performs 24 operations across default/custom roots. Active contenders preserve evidence, inspection creates/changes nothing, explicit/repeated recovery and regeneration preserve canonical/unrelated bytes. Both 14-file inventories include hidden manifests; default output matches the prior reviewed shipping receipt. Exact source/binary/helper/harness hashes and limits are retained in the receipt. Synthetic integration fixtures are labeled separately.

## Blockers, risks, unknowns, and deferred work

No bounded local implementation blocker remains. Fresh native Windows/macOS source-install/clean-room and advisory evidence is still required. Earlier shared-target stale-binary/ExecutableFileBusy observations are not passes; final checks use independent clean artifacts without retries. Three ignored helpers do not count as standalone passing tests.

Inspection without a persistent lock cannot guarantee future inactivity. Explicit rollback revalidates and may create only empty persistent coordination metadata/parents on an empty or later-failed recovery. No hostile-directory replacement, network-filesystem or power-loss qualification is claimed. Older uncoordinated tools must not write concurrently; never delete an active writer's workspace/lock. Release remains v1.0.0; this candidate publishes/deploys nothing.

## Next dependency-ready work

Review the scoped #77 PR and fresh exact-head platform checks. Keep #77 open/Q16 active until maintainer acceptance and merge. #81 immutable development-base qualification is next, followed by #80 browser/font environment, #82 setup CI, #84 workflow cleanup and #83 final documentation reconciliation. Usable-kit work retains the execution order in #116.

## Parallel changes and reconciliation

#120's verified merge reconciles #79 complete. No other open PR was returned before publication. Decision-impact operation: reference ADR-0012/0019 and proposed ADR-0026; this implements the existing local recovery/ownership contract through a human CLI without a new wire schema/protocol. The corpus remains 26 records: 21 accepted/five proposed, with all approval and lineage unchanged. Pinned Aether decision-impact 2.1.0/continuity 1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 and selected Hygiene 1.2.0 sources were read from exact reviewed checkouts.

## Privacy and redaction

Only public repository facts, synthetic consumer observations and artifact hashes are retained. Receipts generalize disposable local paths; no credentials, personal conversations or unrelated context appear. Test instrumentation and linked evidence grant no authority.

## Handoff update protocol

Refresh after domain validation immediately before PR handoff, then verify pinned schema, 12 headings, budgets/privacy, ADR and roadmap invariants. Include this checkpoint in the scoped PR. Exact-head hosted results can be recorded externally when unknowable to the containing commit. Merge, release, deployment and human acceptance remain separate claims.

## Compaction and supersession

Stay below 240 lines / 16384 UTF8 bytes. Git, contracts, receipts and the work tracker retain history. Mark unresolved conflicts stale rather than inventing readiness, safety or approval.
