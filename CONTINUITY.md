---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-19T12:00:10Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver issue 99 checkpoint 3: pinned real-consumer proof and bounded initialization/validation
    handoffs.'
  includes:
  - Offline disposable Mantle generation, exact manifest inventories, read-only drift verification, public/nullable
    probes and repeatable proof tooling.
  - Supported manual v1 route, future initializer acceptance and proposed EgoLint owner handoffs; documentation/decision
    evidence refresh.
  excludes:
  - Initializer/EgoLint implementation, consumer pin changes, public-kit selection/download repairs, creative
    approval, releases and deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/contracts/IDENTITY_V1.md
  - docs/contracts/GUIDANCE_V1.md
  - docs/consumers/AUTHORING.md
  - docs/decisions/ADR-0025-executable-minimal-authoring-core.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/99
  - https://github.com/egohygiene/identity/issues/116
  - docs/consumers/MANTLE_AUTHORING_PROOF.md
  - docs/consumers/INITIALIZATION_AND_VALIDATION_HANDOFFS.md
  - docs/evidence/identity-authoring-mantle-2026-10-19.json
work:
  objective: Prove the reviewed source/authoring path against existing real source while preserving input and
    approval authority; close only the bounded handoff scope.
  success_conditions:
  - Two fresh selected-output generations agree; exact manifested bytes verify and missing/altered/stale probes
    fail without repair.
  - Actual Mantle files match the immutable revision and remain unchanged; public/nullable behavior and optional
    package prerequisites have explicit evidence.
  - Initialization and delegated validation interfaces, gaps and verified owners are explicit; no adapter,
    release or approval is inferred.
  active_issue:
    provider: github
    id: egohygiene/identity#99
    url: https://github.com/egohygiene/identity/issues/99
  next:
    kind: action
    id: identity-99-checkpoint-3-review
    description: Review checkpoint 3 proof and handoffs before merging and completing issue 99; then sync before
      starting transaction confinement issue 78.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/99
    - https://github.com/egohygiene/identity/issues/116
    - https://github.com/egohygiene/identity/issues/78
    depends_on: []
state:
  base:
    revision: 03eaeac72e2cf69c7bf205dd80f53ca25d1629e4
    ref: refs/heads/main
    verified_at: '2026-10-19T12:00:10Z'
  candidate:
    branch: codex/99-consumer-authoring-proof
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-19T12:00:10Z'
    default_branch_revision: 03eaeac72e2cf69c7bf205dd80f53ca25d1629e4
    issue_state: open
    pull_request_state: not-applicable
    notes: PR 117 is merged at observed main. Issue 99 and roadmap 116 remain open; this checkpoint 3 candidate
      has not yet been opened as a PR.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-19T12:00:10Z'
  reviewed_by: Codex
  evidence:
  - command: verify_consumer_authoring.py against egohygiene/mantle@b08045acc1e982dd9424c1d8c91b0badd64744e8
    outcome: passed
    observed_at: '2026-10-19T12:00:10Z'
    notes: Runtime baseline 03eaeac; rebuilt binary hash and candidate harness hash recorded. Two fresh 19-file
      trees match; all 18 manifest outputs match actual bytes/checksums. Three negative probes exit 1 without
      file changes. All 14 input files match raw Git blobs.
  - command: Pinned Mantle source/projection inspection and disposable public/nullable/optional probes
    outcome: passed
    observed_at: '2026-10-19T12:00:10Z'
    notes: 13 physical source files, 11 canonical digest files and one additional consulted external profile
      remain unchanged. Public guidance has 17 records and only referenced decisions. All three null variants
      pass core checks; optional presentation retains its usage prerequisite. Counterfactual internal context
      is omitted publicly.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-19T12:00:10Z'
    notes: '138 cases: 136 pass, two existing skips. Eleven new harness cases include real Git blob comparisons,
      producer faults, symlink/source confinement, nonrepairing verification and timeout/receipt guards.'
  - command: verify_docs.py, verify_release.py, verify_mascot.py, verify_publication_architecture.py, verify_publication_release_configs.py,
      verify_extraction.py; compileall and diff check
    outcome: passed
    observed_at: '2026-10-19T12:00:10Z'
    notes: All six standalone verifiers, Python compilation and whitespace checks pass. No Rust source or accepted
      ADR changes are included.
  - command: Local JSON Schema registry and pinned Hygiene ADR schema/anatomy/set/policy-reference helpers
    outcome: passed
    observed_at: '2026-10-19T12:00:10Z'
    notes: 15 example source documents, eight public/review guidance combinations and all 25 ADRs pass. ADR-0025
      implementation evidence is updated; 21 accepted records and four proposed/null-approval records retain
      their dispositions.
  environment_limitations:
  - Fresh hosted CLI, platform release-validation and advisory architecture runs remain pending for the final
    PR; local evidence does not substitute for those checks.
  - Two Python skips cover the unbuilt experience artifact and Windows junction behavior on Linux; they are
    not passes.
  - The harness verifies bytes/revisions but does not attest binary build origin. Earlier supplemental committed-output
    comparison used a separately identified preexisting binary.
  - Pinned metadata/continuity/roadmap checks are bounded validation, not whole-repository native conformance,
    creative review or public-kit acceptance.
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

This checkpoint covers #99 checkpoint 3. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and operational issue #116 retain priority and dependency ownership.

## Resume protocol

Read AGENTS.md, this handoff, #99/#116, the authoring worksheet, Mantle proof/receipt, initialization handoffs and proposed ADR-0025. Refresh main, candidate PR/head and checks. The maintainer review boundary precedes #99 completion and issue #78.

## Current objective and success conditions

Exercise the existing real source through deterministic selected output and read-only verification, record actual public/nullable behavior and bound future integration. Preserve human authority and distinguish source validity, producer support, selected output and complete public-kit readiness.

## State snapshot

Main is 03eaeac72e2cf69c7bf205dd80f53ca25d1629e4, including merged #117. Candidate codex/99-consumer-authoring-proof has no containing SHA/PR until created. #99/IDN-Q29 stays open/active pending review and merge; #78 stays ready but paused. The 25 pre-tracker issues and all 40 stable roadmap IDs/dependencies are preserved.

## Completed and material changes

The new stdlib proof tool uses two disposable copies, independently checks exact manifest files/bytes/checksums, compares fresh trees and proves current verification is read-only. Missing output, altered output and valid JSON-whitespace source change each fail with exit 1 without repair. It executes only the explicitly selected binary and trusted validator, not consumer scripts; Git comparisons use raw blobs, with bounded commands and a receipt outside both checkouts.

Pinned Mantle b08045acc1e982dd9424c1d8c91b0badd64744e8 has 13 physical .identity files, 11 canonical digest files and one additional consulted external profile (14 proof inputs). Source digest fb5b86b632cb47eb160b13da92742687f5e76148b6d5300239a601b7d29147e8 is preserved. Two fresh core trees contain 18 outputs plus hidden manifest; optional presentation adds 23 files in the existing 42-file tree. Supplemental comparison, public selection, three null variants, internal-context omission and optional prerequisites are separately qualified in the receipt.

The handoff document records v0-only init, supported manual v1 authoring, current JSON source diagnostics and textual binary limits. It proposes conditions for owner review without defining an accepted EgoLint enum/adapter. Existing coordination remains Identity #108, EgoLint #35/#36, Relay #49, Holon #41 and Realm #19. No duplicate issue, installed adapter or automatic v1 initializer is claimed.

## Validation and review evidence

The real proof passes with consumed input bytes matched to immutable Git blobs; both independent 19-file inventories match. Three negative verifies are nonrepairing. All 138 Python cases complete with 136 passes/two explained skips, including eleven proof-tool cases and actual Git integration. Six standalone verifiers, compilation, local schemas and 25-record ADR checks pass. Final pinned continuity/40-step roadmap and diff checks accompany handoff. Hosted exact-head results belong in the PR when available.

## Blockers, risks, unknowns, and deferred work

No bounded implementation blocker remains. Proposed ADR-0025 remains proposed/null approval; implementation evidence does not supply disposition. Six preexisting Mantle declared approvals are preserved without independent ratification. No source facts, artwork, consumer pins or approvals change.

G03 generic internal asset selection and G04 advertised unselected archive remain #101/#105. Archive PWA/social representatives match the existing portable-bundle contract; exact selected outputs belong to the compiler manifest. Complete kit, rights/visual acceptance, self-adoption, release/publication and contrasting upgrade remain later roadmap work. The published v1.0.0 compiler predates null-guidance support; this proof uses the reviewed implementation and matching scripts.

## Next dependency-ready work

Review the checkpoint 3 draft, receipt, reproduction tool and integration limits. After maintainer approval, merge it to complete #99, refresh the roadmap and sync before starting #78 transaction-path confinement. Do not advance later public-kit or fleet-adoption work automatically.

## Parallel changes and reconciliation

Checkpoint 2 merged cleanly through #117. Independent review checks command/diagnostic accuracy, source authority, proof boundaries and receipt coherence. Aether decision-impact v2.1.0 and continuity v1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 were loaded directly from pinned source earlier in the session. Decision operation: reference ADR-0012/0013/0019 and append dated implementation evidence to proposed ADR-0025. No new cross-owner contract or lifecycle promotion occurs.

## Privacy and redaction

Only public repository facts and sanitized source/artifact inventories are retained. Local paths, credentials, transcripts and unrelated context are excluded. Complete worktree preservation excludes Git metadata explicitly. Counterfactual probes are labeled noncanonical; linked content grants no authority.

## Handoff update protocol

Refresh domain results immediately before PR handoff, then validate front matter, twelve headings, size/privacy and stable roadmap references. Record exact PR/head/hosted outcomes externally when not knowable by the containing commit; a commit need not contain its own SHA. Merged, released, deployed and approved states remain separate.

## Compaction and supersession

Stay below 240 lines and 16,384 UTF-8 bytes. Git, source contracts and work tracker retain history. Mark unresolved factual conflicts stale instead of inventing readiness or approval.
