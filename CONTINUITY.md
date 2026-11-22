---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T05:45:58.359807+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Capture the maintainer brand answers and selected logo-use terms, repair the existing README
    raster and prepare a local token baseline for review.
  includes:
  - Capture exact owner-selected masters, provenance account, policy/credit, wording and design choices.
  - Replace the glitched legacy README raster with exact intact existing bytes and correct descriptive
    geometry metadata.
  - Prepare the scoped logo policy, proposed ADR and Identity-local token review candidate.
  excludes:
  - Root .identity adoption, exact token/layer approval and invented human facts.
  - New artwork, full runtime/native/browser/act/CI qualification, release, deployment and consumer rollout.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/work/98/OWNER_ANSWERS_2026-11-22.md
  - docs/work/98/QUESTIONNAIRE.md
  - docs/work/98/OWNER_PACKET.md
  - docs/work/98/candidate/README.md
  - docs/work/98/candidate/.identity/defaults/README.md
  - assets/identity/brand/LOGO_USE.md
  - docs/decisions/ADR-0035-scoped-logo-use-policy.md
  - docs/decisions/policy-reference.json
  - docs/consumers/V1_INITIALIZATION.md
  - https://github.com/egohygiene/identity/issues/98
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Capture the maintainer brand answers and selected logo-use terms, repair the existing README
    raster and prepare a local token baseline for review.
  success_conditions:
  - Preserve both selected master hashes, avatar, historical receipts and Kern governance.
  - Bind the technical repair to actual raster bytes/geometries and retain proposed ADR lifecycle.
  - Keep the exact token baseline, remaining answers and actual self-source acceptance explicitly reviewable.
  active_issue:
    provider: github
    id: egohygiene/identity#98
    url: https://github.com/egohygiene/identity/issues/98
  next:
    kind: action
    id: review-baseline-and-assemble-self-source
    description: 'Review the exact prepared local token/layer baseline, then assemble subject-bound source/governance
      and validate before separate output generation and publisher proof. Engineering #70 can proceed
      independently.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/98
    - https://github.com/egohygiene/identity/issues/70
    depends_on: []
state:
  base:
    revision: b687df51649226882f2b218178c7b10933f48a74
    ref: refs/heads/codex/116-spec-conformance-handoff-20261121
    verified_at: '2026-11-22T05:45:58.359807+00:00'
  candidate:
    branch: codex/98-owner-answers-and-assets-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    default_branch_revision: afc368003bfc6a2101051229efd237c8d6fadf71
    issue_state: open
    pull_request_state: not-applicable
    notes: Main remains afc3680; parent draft PR155 remains open at b687df5. Issue98 contains the assistant-captured
      first owner answers. This child candidate is not merged or published.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#155
    url: https://github.com/egohygiene/identity/pull/155
review:
  status: partial
  reviewed_at: '2026-11-22T05:45:58.359807+00:00'
  reviewed_by: Codex
  evidence:
  - command: Asset byte/pixel/hash, XML geometry and historical-source comparisons
    outcome: passed
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: README WebP equals intact hires (1500x500), exact manifest blobs/dimensions; both masters/avatar/hires/README
      SVG and historical rollback/source inventory/Kern bytes unchanged. Independent review passes.
  - command: python3 scripts/verify_docs.py --repository-root .
    outcome: passed
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: Current documentation targets resolve.
  - command: python3 scripts/verify_publication_architecture.py --repository-root .; python3 scripts/verify_publication_release_configs.py
      --repository-root .
    outcome: passed
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: Existing offline publication checks pass after the descriptive geometry correction; no deployment
      performed.
  - command: Pinned ADR metadata/anatomy and local-token schema/value comparisons
    outcome: passed
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: New ADR0035 remains proposed/null; 34 prior records unchanged; token schema and nine preserved
      publication type/value records pass with documented text-path mapping.
  - command: python3 scripts/validate_identity.py --repository-root docs/work/98/candidate --format json
    outcome: limited
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: 'Exit1, valid=false, IDN1301: unadopted layers remain empty. This is an intentionally incomplete
      review candidate, not successful source validation.'
  - command: git diff --check
    outcome: passed
    observed_at: '2026-11-22T05:45:58.359807+00:00'
    notes: No whitespace errors.
  environment_limitations:
  - The exact local token/layer review and full source/governance assembly remain pending; confirmed chat
    choices do not claim valid canonical source.
  - No full runtime/browser/act/CI, canonical-root source generation, release or live publication proof
    is supplied.
  - Official released EgoLint continuity conformance is not claimed; use the pinned schema/structure check.
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

This is an operational checkpoint beneath runtime/user instructions, scoped instructions, live state and canonical source. It records a draft owner-answer/asset checkpoint, not completed Identity adoption.

## Resume protocol

Read AGENTS and the owner-answer, questionnaire, policy and candidate records above. Verify main, issue98 and parent PR155 before updating this stacked branch. The owner has confirmed szmyty as reviewer and the full copy/voice/principles; unanswered technical review must not be inferred.

## Current objective and success conditions

Capture the selected brand facts and scoped logo permissions, restore the historical raster without redesign, and prepare an explicitly local token baseline for exact review.

## State snapshot

Base is parent PR155 at b687df51649226882f2b218178c7b10933f48a74; main remains afc368003bfc6a2101051229efd237c8d6fadf71. The child candidate and containing revision are not self-referenced. It is not merged, released or deployed.

## Completed and material changes

The owner selected the exact existing emblem/horizontal masters, ChatGPT-assisted origin account, scoped logo-use policy and credit, lowercase name/specification-first tagline/short copy, current palette/Inter, optional Kern and local-baseline preparation. Reviewer szmyty and the supplied longer copy/voice/principles are confirmed. The legacy README WebP now uses the intact hires bytes; manifest raster dimensions and horizontal descriptive geometry are corrected. ADR0035 proposes licensing integration without changing prior dispositions. Candidate source remains incomplete and unadopted.

## Validation and review evidence

Asset/hash/geometry checks and independent review pass. Existing docs/publication checks pass. Local-token schema, nine exact source-value records and proposed ADR metadata/anatomy checks pass. The candidate source validator explicitly returns IDN1301 for empty layers, so no valid-source result is claimed. Pinned Aether decision/continuity guidance remains dc8a16851f452763ef4f7fbe4bf057d4500b1921, with Hygiene policy1.2.0 at a05b14f8b9e2772124f879f818e09a911e996ad8.

## Blockers, risks, unknowns, and deferred work

Review the exact local token/layer declarations and construct same-subject source/governance records from the now-confirmed owner choices. External reference kits/generation links remain unidentified. The new tagline has not silently rewritten the selected original masters or legacy artwork; generated derivatives need their own review. #70/#80/#82/#88 retain engineering qualification; #98 retains actual self-source/release/live/rollback/consumer acceptance.

## Next dependency-ready work

Review the exact prepared baseline, then assemble and validate actual v1 source before generating selected outputs and exercising the real publisher handoff. Independent existing engineering work under #70 remains available. #116 closes last.

## Parallel changes and reconciliation

This branch is stacked on open draft PR155. Review/merge parent before child and reconcile continuity semantically. egohygiene/hygiene#128 tracks later required-repository policy; it is not a new producer finish gate. Preserve newer peer changes and prior exact-source receipts.

## Privacy and redaction

Capture only public-safe brand choices and technical facts the user authorized for the repository. Exclude screenshots' unrelated personal/browser context, private chat transcript, local paths and credentials.

## Handoff update protocol

Refresh after actual checks and before PR presentation; validate pinned schema, twelve headings and size budgets. ADR-Ref: egohygiene/identity#ADR-0035 (create; proposed/null approval). Existing source/token boundaries reference ADR-0001, ADR-0004 and ADR-0012; no lifecycle is promoted.

## Compaction and supersession

Git and the owning issues retain history. Keep this current record compact; do not rewrite historical inventories, rollback captures, prior ADRs or original asset-approval dates.
