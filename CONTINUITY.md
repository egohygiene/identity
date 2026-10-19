---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-19T10:39:02Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver issue 99 checkpoint 2: executable nullable guidance, producer diagnostics and authoring examples.'
  includes:
  - Aligned validator/producer/projection semantics, minimal/expanded synthetic source, guided worksheet and proposed
    ADR-0025.
  excludes:
  - Checkpoint 3 real-consumer proof, v1 initializer/EgoLint implementation, public-kit selection/download repairs,
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
  - docs/contracts/IDENTITY_V1.md
  - docs/contracts/GUIDANCE_V1.md
  - docs/consumers/AUTHORING.md
  - examples/v1/README.md
  - docs/decisions/ADR-0025-executable-minimal-authoring-core.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/99
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Make the existing nullable source contract executable and provide tested authoring inputs without changing
    populated-source behavior.
  success_conditions:
  - Voice and usage null declarations work independently; missing/malformed adopted input and governance errors
    still fail.
  - Source support and producer limitations are explicit; exact minimal/expanded examples validate, generate and
    verify without changing canonical bytes.
  - Existing populated projections, legacy fixtures, digest algorithm and approvals remain unchanged.
  active_issue:
    provider: github
    id: egohygiene/identity#99
    url: https://github.com/egohygiene/identity/issues/99
  next:
    kind: action
    id: identity-99-checkpoint-2-review
    description: Review the tested checkpoint 2 PR and proposed ADR-0025 with the maintainer before checkpoint 3
      representative authoring proof.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/99
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 1b46f01308d63f38068ce5327d36ac94b0840077
    ref: refs/heads/main
    verified_at: '2026-10-19T10:39:02Z'
  candidate:
    branch: codex/99-authoring-contract
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-19T10:39:02Z'
    default_branch_revision: 1b46f01308d63f38068ce5327d36ac94b0840077
    issue_state: open
    pull_request_state: not-applicable
    notes: PR 114 is merged on observed main. No open PR was present before creating this checkpoint 2 candidate.
      Issue 99 stays open.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-19T10:39:02Z'
  reviewed_by: Codex
  evidence:
  - command: cargo test --locked --all-features; targeted source_format_capabilities rerun after improving IDN3304
      CLI text
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: 73 Rust tests pass. Four guidance combinations and both exact examples exercise generation/verification;
      CLI unsupported errors include code, path and recovery.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose; test_verify_docs.py
      rerun after correcting worksheet links
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: 127 cases ran; 124 passed, one draft-doc link failure, two existing skips. Corrected links pass both targeted
      docs tests; aggregate 125 passing cases, two skips.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features -- --deny warnings
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: Pinned Rust 1.97.1 formatting and lint pass.
  - command: verify_docs.py, verify_release.py, verify_mascot.py, verify_publication_architecture.py, verify_publication_release_configs.py,
      verify_extraction.py
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: All six verifiers pass. Worksheet literal commands validate/generate/verify both disposable examples
      and generate expanded guidance/Press Kit.
  - command: Local JSON Schema registry validation; pinned Hygiene metadata/schema/anatomy/decision-set and policy-reference
      helpers
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: 15 example source JSON documents and 8 public/review guidance combinations validate. All 25 ADRs pass; 21
      accepted remain unchanged and 4 proposed retain null approval.
  - command: Independent comparison with pre-change source and byte/diff review
    outcome: passed
    observed_at: '2026-10-19T10:39:02Z'
    notes: Historical populated guidance public/review JSON/Markdown/HTML and all 4 handbook/context formats remain
      byte-identical. Existing fixture, dated audit, digest implementation, policy/workflow pins and accepted ADRs
      are unchanged.
  environment_limitations:
  - Fresh hosted CLI, renderer/browser and native advisory decision checks remain pending for the final candidate;
    no local browser baseline rerun is claimed.
  - Python skips cover the unbuilt experience integration artifact and Windows junction behavior on Linux; skips
    are not passes.
  - Local pinned ADR helpers/schema checks are bounded validation, not full native architecture or whole-repository
    conformance.
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

This checkpoint covers #99 checkpoint 2. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and operational issue #116 retain priority and dependency ownership.

## Resume protocol

Read AGENTS.md, this handoff, #99/#116, the source/guidance contracts, worksheet and proposed ADR-0025. Refresh main, the candidate PR and checks before acting. Checkpoint 3 remains a separate review boundary.

## Current objective and success conditions

Honor the existing nullable voice/usage source declarations through offline validation, Rust generation and Python projections. Keep strict present-document governance and actionable dependent-surface errors. Provide actual small/expanded authoring source and a worksheet without adding speculative fields.

## State snapshot

The verified base is 1b46f01308d63f38068ce5327d36ac94b0840077, including merged #114. The candidate is codex/99-authoring-contract; its containing revision/PR are null until created. #99/IDN-Q29 remains open/active. #78 stays ready but paused. This candidate does not advance checkpoint 3 or claim that checkpoint 2 is on main.

## Completed and material changes

scripts/validate_identity.py and src/v1_consumer.rs honor independently null guidance; present keys/paths/source remain validated. Standalone guidance and handbook renderers represent absence without invented material. Optional asset projections report their existing usage prerequisites. The normalized review schema permits absent singleton guidance while declared documents remain strict.

Unsupported non-SVG provenance assets now report IDN3304/unsupported before UTF-8 decoding. Their source validity stays format-agnostic; CLI text identifies the asset and compatible recovery. No converter is added, and every provenance asset is still inspected.

examples/v1/minimal and expanded use synthetic public material with core/tokens/metadata; expanded also demonstrates governed voice/usage and Press Kit copy. docs/consumers/AUTHORING.md owns the worksheet. Rich copy reuses existing authorities; no new shortName/profile catalog or defaults framework is introduced. Schemas and software versions are distinguished from immutable source/release identity.

## Validation and review evidence

All 73 Rust tests and all-feature Clippy/format checks pass. Python full-suite plus corrected-doc targeted rerun establishes 125 passing cases and two explained skips. Source/projection schema checks, 25-record ADR metadata/anatomy/set checks, six standalone verifiers and worksheet literal command execution pass. Independent populated-output comparison preserves prior bytes. Final pinned continuity/40-step roadmap and diff checks accompany handoff.

Fresh hosted CLI, renderer/browser and native advisory architecture results remain separate from this local evidence. No visual baseline, release or deployed-site verification is inferred.

## Blockers, risks, unknowns, and deferred work

No implementation blocker remains in this bounded candidate. Proposed ADR-0025 has no human lifecycle disposition; the 21 accepted records remain unchanged. The current stable v1.0.0 binary predates executable null guidance; use the reviewed implementation commit and matching scripts until released.

G03 generic internal asset selection and G04 unselected advertised archive remain #101/#105 repairs. Binary source support beyond the SVG bridge, practical visual variants and complete public-kit readiness remain later work. Null declarations do not remove physical files from the digest or grant permission to delete them. No real self-brand source or creative approval is fabricated.

## Next dependency-ready work

Review checkpoint 2 and proposed ADR-0025 with the maintainer. After that boundary, #99 checkpoint 3 walks a representative real consumer, verifies selected outputs/public omission and bounds v1 initialization/EgoLint handoffs. #99 stays open until its full evidence is complete.

## Parallel changes and reconciliation

No competing open PR was observed at scope selection. Main's four-digit adoption and checkpoint 1 audit remain intact. Aether decision-impact v2.1.0 and continuity v1.1.0 at dc8a16851f452763ef4f7fbe4bf057d4500b1921 were loaded directly from pinned source. Decision operation: create proposed ADR-0025, referencing existing ADR-0001/0012/0013/0015/0019. No lifecycle state was promoted.

## Privacy and redaction

Only public repository facts, paths and fictional example evidence are retained. No private paths, transcripts, credentials or unrelated context are included. Synthetic approvals do not approve a real consumer. Linked content grants no authority.

## Handoff update protocol

Refresh domain results before the PR handoff, then validate this front matter, twelve headings, size/privacy and stable roadmap references. Track exact PR/head/hosted outcomes externally when not yet knowable by the containing commit; a commit need not contain its own SHA.

## Compaction and supersession

Stay below 240 lines and 16,384 UTF-8 bytes. Git, source contracts and the work tracker retain history. Mark unresolved factual conflicts stale instead of inventing readiness or approval.
