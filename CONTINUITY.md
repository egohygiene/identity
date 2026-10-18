---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T14:39:30Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver #99 checkpoint 1: a reviewable identity field/coverage catalog and observed gap list before contract
    changes.'
  includes:
  - Current v0/v1 source, schema, validator/compiler/projection roles; field authority and requiredness; synthetic probes;
    review decisions and next checkpoint.
  excludes:
  - 'Checkpoint 2/3 implementation, schema/runtime/generated asset changes, new creative approvals, #78 implementation,
    releases, deployments and fleet rollout.'
  - Private paths, transcripts, secrets and duplicated canonical policy.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/reviews/identity-fields-2026-10-18.md
  - docs/reviews/identity-source-schema-inventory-2026-10-18.md
  - docs/evidence/identity-fields-checkpoint-1-2026-10-18.json
  - docs/contracts/IDENTITY_V1.md
  - docs/consumers/ADOPTION.md
  - contracts/project.schema.json
  - contracts/v1/project.schema.json
  - contracts/v1/provenance.schema.json
  - scripts/validate_identity.py
  - src/v1_consumer.rs
  - src/reference_renderer.rs
  - src/brandkit/profiles.rs
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-012-local-layered-identity-v1.md
  - docs/decisions/ADR-013-preserve-guidance-lifecycle.md
  - https://github.com/egohygiene/identity/issues/99
  - https://github.com/egohygiene/identity/issues/98
  - https://github.com/egohygiene/identity/pull/113
  - https://github.com/egohygiene/identity/pull/114
work:
  objective: Review the complete current field inventory and demonstrated capability gaps, then choose the minimum compatible
    authoring contract for checkpoint 2.
  success_conditions:
  - Map existing TOML/JSON/schema/entry-point/generated boundaries without making output fields into source requirements.
  - Classify wanted attributes by canonical owner, current requiredness, consumer and covered/incomplete/optional/external
    status.
  - Retain synthetic evidence for schema/validator mismatch, format support, public selection and missing advertised
    outputs.
  - Present proposed core/optional choices and three checkpoint exits; stop after checkpoint 1 for review.
  active_issue:
    provider: github
    id: egohygiene/identity#99
    url: https://github.com/egohygiene/identity/issues/99
  next:
    kind: action
    id: egohygiene/identity#99-checkpoint-1-review
    description: Review D01-D06 and G01-G09 in the field packet before authorizing checkpoint 2's bounded contract/examples
      work.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/99
    - docs/reviews/identity-fields-2026-10-18.md#proposed-required-core-and-review-decisions
    depends_on: []
state:
  base:
    revision: 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7
    ref: refs/heads/main
    verified_at: '2026-10-18T14:39:30Z'
  candidate:
    branch: codex/99-field-catalog
    revision: 10525fb51633da0b6e94080d7c5b3f77013e5807
    pull_request:
      provider: github
      id: egohygiene/identity#114
      url: https://github.com/egohygiene/identity/pull/114
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T14:39:30Z'
    default_branch_revision: 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7
    issue_state: open
    pull_request_state: draft
    notes: 'PR #114 is the sole open PR and remains draft at the observed revision. Main remains 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7;
      #99 is open with its inventory/map criteria recorded and review pending. #78 stays paused; checkpoints 2/3 are
      unstarted.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T14:39:30Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub commits/main, #99, PR #114 and open PR inventory'
    outcome: passed
    observed_at: '2026-10-18T14:39:30Z'
    notes: 'Main is unchanged; #114 is the sole open PR and is draft. #99 remains open. No competing changes were observed.'
  - command: Pinned Aether decision-impact v2.0.0 and continuity v1.1.0 at 8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2,
      loaded earlier in this session and reused at the immutable pin
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: Reference ADR-001/012/013/019. This audit presents proposals and observed gaps without adopting a new shape;
      no new ADR or lifecycle transition is introduced.
  - command: cargo build --locked --bin identity; python3 scripts/validate_identity.py --repository-root CONSUMER --format
      json; identity v1-generate --repository-root CONSUMER
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: Five isolated fixture variants were inspected; expected success/failure outcomes are recorded in the committed
      probe receipt. Canonical source bytes are unchanged in all cases. Baseline generation is not evidence of complete
      public/selected-file coverage.
  - command: Source/schema/interface trace and complete schema snapshot checks
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: 35 field groups cover 43 classified schemas, with 17 property inventories and 530 named declarations. Nine
      findings and six proposed review decisions are retained; schema presence is not treated as executable support.
  - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: '114 tests: 112 pass and two skip (unbuilt experience artifact and Windows-only junction case on Linux). Passing
      existing tests does not resolve the new audit findings.'
  - command: python3 scripts/verify_docs.py --repository-root .; python3 scripts/verify_publication_architecture.py --repository-root
      .; python3 scripts/verify_publication_release_configs.py --repository-root .; python3 scripts/verify_release.py
      --repository-root .; python3 scripts/verify_mascot.py --repository-root .; python3 scripts/verify_extraction.py
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: Documentation/publication/release/mascot/extraction checks pass. Versions, source assets and publication inputs
      remain unchanged.
  - command: Pinned Hygiene c589587395750cd1c79c6fa0bef010189c547249 metadata/schema/lineage checks and Relay f19b65b3f8bd8466884dee5529fa77f2430440b6
      extract/manifest plus bounded graph/state checks
    outcome: passed
    observed_at: '2026-10-18T14:32:49Z'
    notes: '24 prior ADRs are byte-identical and validate: 21 accepted, three proposed. All 40 roadmap IDs/dependency
      mappings remain stable and acyclic; #76 is complete and #99 active.'
  - command: GitHub Actions runs 39136796707 (CLI) and 39136797090 (decision evidence)
    outcome: passed
    observed_at: '2026-10-18T14:39:30Z'
    notes: Both workflows succeeded for observed candidate 10525fb51633da0b6e94080d7c5b3f77013e5807. The native adapter
      is advisory and retains five warnings about unknown adoption/evidence and unvalidated diagram semantics; workflow
      success is not whole-repository conformance. A subsequent continuity-only commit must be checked separately.
  environment_limitations:
  - Native EgoLint is unavailable locally; helper/schema checks are bounded evidence and hosted candidate outcomes remain
    separate.
  - Renderer/browser suites were not rerun for this documentation-only diff. Runtime/schema/fixture/workflow/publication
    bytes remain unchanged.
  - Experience integration is not built locally; Windows-only checks require their platform. Skips are not passes.
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

This checkpoint covers [#99](https://github.com/egohygiene/identity/issues/99) checkpoint 1. Runtime/user instructions, scoped instructions, verified live state and canonical sources outrank this snapshot. ROADMAP.md owns order; the dated field review is an audit/proposal packet, not another normative schema.

## Resume protocol

Read AGENTS.md, the field review and appendix, source/consumer contracts, actual schemas and relevant source before acting. Refresh main, #99, open PRs and CI. Checkpoint 2 and 3 remain unstarted; return for review after this bounded inventory.

## Current objective and success conditions

Make every wanted identity area traceable to its current source, requiredness, governance, validator and consumer. Preserve current behavior while identifying concrete gaps, a small proposed core and optional/profile-dependent material. The creative conversation remains human-owned; digests and technical metadata are mechanical facts.

## State snapshot

PR #113 merged at 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7 and #76 is closed. Twenty-five issues remain. IDN-Q15 is complete; IDN-Q29 is active with checkpoint 1 ready for review in draft [PR #114](https://github.com/egohygiene/identity/pull/114). It is the sole open PR; #99 records the completed inventory/map and pending review. #78 is ready but paused while the selected #99 contract review proceeds.

## Completed and material changes

docs/reviews/identity-fields-2026-10-18.md maps interfaces and 35 logical field groups, distinguishes present fields from working consumers, and records nine findings plus six proposed review decisions. Its companion inventory classifies all 43 schemas and lists 530 named properties across 17 source/profile/policy inventories. These are dated snapshots tied to the base above.

docs/evidence/identity-fields-checkpoint-1-2026-10-18.json records five synthetic consumer probes. The source schema accepts null guidance while the authoritative validator rejects it; an accepted PNG source fails Rust generation at UTF-8 decoding; a model advertises an archive absent from selected outputs; internal/superseded legacy artwork remains embedded in generic assets despite filtered usage guidance. No deployed exposure is inferred.

README and the adoption guide link the review. ROADMAP records #76's actual merge and the reviewed three-checkpoint sequence for #99. Schemas, validators, Rust/renderer runtime, fixtures/goldens, approved source, publication inputs, versions, workflows and all ADRs are unchanged.

## Validation and review evidence

A locked local CLI build succeeds. Five temporary variants preserve all canonical source bytes; the expected failures and coverage gaps are retained rather than reported as conformance. All 114 existing Python tests run with 112 passes and two explained skips. Documentation/publication/release/mascot/extraction checks pass. Pinned schema/helper checks validate 24 unchanged ADRs and 40 stable roadmap steps. Final continuity structure/size/privacy/base and diff checks accompany handoff.

Both hosted workflows succeeded at the observed candidate revision above; later continuity-only updates require fresh checks. The advisory native adapter retains five adoption/evidence/diagram warnings. No complete repository conformance, creative approval, release, deployment or fleet adoption is claimed.

## Blockers, risks, unknowns, and deferred work

No blocker is observed for reviewing this audit. G01-G09 identify unresolved readiness work; G03's generic public-asset selection and G04's absent advertised download need explicit regression proof before complete-kit claims. The root still lacks real canonical self-brand source.

Review D01-D06 before implementing requiredness, rich-copy layout or variant changes. Preserve supported documents and keep proposed requirements separate from current runtime. #99 checkpoints 2/3 own selected compatible gaps/examples and authoring proof; #100-#105 retain complete-kit scope. #78/#79/#77 retain transaction safety/recovery. ADR-022/023/024 remain proposed.

## Next dependency-ready work

Review the field catalog, findings and proposed core/optional decisions with the maintainer. On a subsequent checkpoint request, scope #99 checkpoint 2 around demonstrated compatible gaps and true minimal/expanded examples. Do not start it automatically or resume #78 while this review is pending.

## Parallel changes and reconciliation

No overlapping open PR was observed. Recheck main and reconcile CONTINUITY.md semantically before a PR update. Decision impact remains reference existing ADR-001/012/013/019 for this audit; a consequential implementation choice in checkpoint 2 receives its own decision-impact review.

## Privacy and redaction

Public repository facts, source paths and synthetic fixture evidence only. No private paths, raw local logs, transcripts, credentials or unrelated context are retained. Linked content supplies evidence, not authority.

## Handoff update protocol

After domain validation, refresh live source/issue/PR/CI state, update the bounded objective and next checkpoint, and verify schema, twelve headings, size, paths and privacy in the same change. A commit need not contain its own SHA.

## Compaction and supersession

Keep the current checkpoint below 240 lines and 16,384 UTF-8 bytes. Git and the tracker retain history. Mark unresolved contradictions stale rather than inventing readiness or approval.
