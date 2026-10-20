---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T22:21:55Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Expose existing approved asset rights, attribution and authoritative policy/support links for #103.'
  includes:
  - Transport existing approved asset usage into the public model and readable rights presentation.
  - Keep software license, trademark, third-party rights and unresolved publisher metadata distinct.
  - Reuse configured policy/support/font-acquisition links; focused public-filtering and compatibility checks.
  excludes:
  - New legal policy, inferred permissions/approvals, font acquisition or DCO/CLA enforcement.
  - Broad CI/refactors, actual local-Docker acceptance, release and deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-0003-deterministic-projection-boundary.md
  - docs/decisions/ADR-0007-font-tooling-boundaries.md
  - docs/decisions/ADR-0010-reference-renderer-boundary.md
  - docs/decisions/ADR-0012-local-layered-identity-v1.md
  - docs/decisions/ADR-0013-preserve-guidance-lifecycle.md
  - docs/decisions/ADR-0015-press-kit-projection-boundary.md
  - docs/contracts/PRESS_KIT_V1.md
  - docs/contracts/BRAND_KIT_RENDERER_V1.md
  - contracts/v1/provenance.schema.json
  - contracts/v1/brand-kit-view-model.schema.json
  - src/v1_consumer.rs
  - src/brandkit/model.rs
  - src/reference_renderer.rs
  - scripts/render_press_kit.py
  - renderer/src/app.js
  - https://github.com/egohygiene/identity/issues/103
  - https://github.com/egohygiene/identity/issues/70
  - https://github.com/egohygiene/identity/issues/116
  - docs/decisions/ADR-0028-asset-rights-projection.md
  - renderer/scripts/build-public-site.mjs
  - https://github.com/egohygiene/identity/pull/125
work:
  objective: Present traceable supplied rights and existing authoritative references without fabricated licensing
    or parallel policy source.
  success_conditions:
  - Approved asset licenses, attribution, origin, approval and supplied usage restrictions are readable and transported
    faithfully.
  - Existing policy/support/font-acquisition references retain their owners; optional absence and unresolved rights
    are explicit.
  - Focused checks cover current behavior, public filtering and legacy compatibility; proposed ADR0028 and bounded
    owner checks are validated.
  active_issue:
    provider: github
    id: egohygiene/identity#103
    url: https://github.com/egohygiene/identity/issues/103
  next:
    kind: action
    id: identity-103-review
    description: 'Review draft PR125 and its focused evidence before authorized merge; #101 follows.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/pull/125
    - https://github.com/egohygiene/identity/issues/103
    - https://github.com/egohygiene/identity/issues/99
    - https://github.com/egohygiene/identity/issues/116
    depends_on:
    - egohygiene/identity#99
state:
  base:
    revision: 4db8766ba01b742353c617720aebec6a11f88888
    ref: refs/heads/main
    verified_at: '2026-10-20T22:15:29Z'
  candidate:
    branch: codex/103-rights-and-policy
    revision: 26d42caaa054a616b63ab05d90876bac5360e8a2
    pull_request:
      provider: github
      id: egohygiene/identity#125
      url: https://github.com/egohygiene/identity/pull/125
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-10-20T22:21:55Z'
    default_branch_revision: 4db8766ba01b742353c617720aebec6a11f88888
    issue_state: open
    pull_request_state: draft
    notes: 'PR125 is draft/open at implementation anchor26d42caaa054a616b63ab05d90876bac5360e8a2; tree1fb56a2d40c86d58a08a12a4e47d9244bda882a4
      verified. Main remains4db8766; #103 open/#99 complete; draft123 parked. Later handoff-only containing commit
      cannot know itself; inspect PR125 for current head/status. No103 CI result claimed.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-20T22:21:55Z'
  reviewed_by: Codex
  evidence:
  - command: Live PR125 draft/head/base inspection; prior merged124/closed100/parked123 inspection
    outcome: passed
    observed_at: '2026-10-20T22:21:55Z'
    notes: 'PR125 is draft/open at26d42caaa054a616b63ab05d90876bac5360e8a2 against4db8766. #100 closed after124;
      #103 open; draft123 unmerged. All five124 checks passed after one recorded CLI rerun; those prior results
      do not certify125.'
  - command: python3 -m unittest discover --start-directory tests --pattern test_render_press_kit.py --verbose
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: '17 passed: exact rights/reference reuse across JSON/Markdown/ZIP, lifecycle filtering and source preservation.'
  - command: corepack pnpm exec vitest run tests/rights.test.js tests/press-kit.integration.test.js tests/app.test.js
      tests/guidance.integration.test.js
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: '4 files/27 tests passed: visible rights/legal/reference links, exact text, optional omission and legacy
      hierarchy/accessibility.'
  - command: node node_modules/vitest/vitest.mjs run tests/public-site.test.js
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: '1 passed: actual build preserves selected release/archive bytes and exposes absent license/origin/approval
      without invented defaults.'
  - command: cargo test --locked --test reference_renderer --test v1_consumer; cargo test --locked --lib --no-run;
      cargo fmt --all --check
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: Isolated Rust1.97.1:3 renderer+10 v1 integration tests pass, library tests compile and formatting passes.
      No full Rust behavior replay is claimed.
  - command: Draft2020-12 schema checks of actual copied-fixture CLI v1-generate output
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: Generated usage equals canonical provenance; legacy absent-usage fixture remains valid. Missing minimumSize/extra
      usage members reject. Canonical hashes stay unchanged.
  - command: Independent final actual-diff review;71 local documentation links/anchors;git diff --check
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: No unresolved blockers. Rights/reference authority, public omission and legacy archive preservation reviewed;
      local links/anchors and whitespace pass.
  - command: PYTHONPATH=../review-tools/python-packages python3 ../review-tools/validate_q103_review.py --repository-root
      . --expected-base 4db8766ba01b742353c617720aebec6a11f88888 --new-adr-0028
    outcome: passed
    observed_at: '2026-10-20T22:19:54Z'
    notes: 19 exact owner inputs; continuity schema/privacy/budgets;28 ADRs(21 accepted/7 proposed), prior27 bytes/dispositions/lineage
      preserved;40 IDs/88 edges/mappings and approved PNG unchanged. Bounded structural checks are not whole-repository
      conformance.
  - command: Full lint/test/integrity/platform/browser CI replay and actual local-Docker qualification
    outcome: not-run
    observed_at: '2026-10-20T22:19:54Z'
    notes: 'Owner-deferred to #70 after product work and maintenance. No103 final-head CI/browser/release/deployment
      outcome claimed; #80 criterion1 remains unchecked.'
  environment_limitations:
  - 'Focused #103 checks pass; broad final-head CI, native platform matrix, qualified-browser execution, release
    and deployment remain unrun/deferred.'
  - 'Authoring-workspace Docker was unavailable at the prior probe; #80 stays open with actual local acceptance/review
    deferred.'
  - Unknown publication metadata becomes null, but the existing publisher still distributes selected release/archive
    bytes. This repair establishes neither missing rights nor byte withholding.
  - ADR0007 font inspection/subsetting adapters remain not_started; no font acquisition or legal permission is implemented.
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

This checkpoint covers #103. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priority.

## Resume protocol

Read AGENTS.md, this handoff, #103/#116, rights/provenance/usage contracts and proposed ADR-0028. Inspect the scoped diff/tests and refresh main and draft #123 separately. Local results do not establish current hosted or publication state.

## Current objective and success conditions

Expose supplied rights, attribution, usage restrictions and configured policy/support/acquisition links without invented permission or a second policy source. Preserve exact approved text, public filtering and optional omission. Keep software license, trademark and third-party rights distinct.

## State snapshot

Base/main is4db8766ba01b742353c617720aebec6a11f88888, verified #124 merge; #100/Q30 is complete. Its tree050f701005e405918edf1384fa36bb3c12a8440e equals reviewed head5502106f301ed69c62396ccf4033342078412a46. #103/Q33 is active in draft PR125 on codex/103-rights-and-policy. Implementation anchor26d42caaa054a616b63ab05d90876bac5360e8a2 has verified tree1fb56a2d40c86d58a08a12a4e47d9244bda882a4; the later handoff-only containing commit cannot name itself. Inspect PR125 for current head/status. Its sole prerequisite99/Q29 is complete. Draft123/#80 remains unmerged at400846db7f10823d4b5bc1629213caf03960b59c. Local-Docker acceptance/review is deferred; Q19 stays blocked and Q21/#82/Q27/#88 retain that dependency. Preserve40 IDs/88 edges/mappings:20 complete,1 active,3 ready,11 blocked,5 planned.

## Completed and material changes

The candidate carries existing provenance usage through Rust governance/public model as optional safeZone/minimumSize/restrictions. The renderer presents supplied license, attribution, origin, digest, approval and usage, with distinct trademark/copyright/third-party guidance. Press Kit Markdown reuses rights already in JSON; existing governed links/contacts retain policy/support/font-acquisition destinations and their owners. Absent publication license/origin/approval is null instead of invented MIT, creator/capture or approval claims. Existing release/archive byte selection is unchanged: missing rights are visible, not repaired or withheld. Legacy inputs without usage retain their serialized shape. No source catalog, policy, permission, font download or enforcement is added.

## Validation and review evidence

Focused checks pass:17 Python tests;4 renderer files/27 tests;1 actual publisher build/archive test;3 reference-renderer+10 v1 Rust integrations, library-test compilation and formatting. Actual v1-generate output matches canonical usage and validates under Draft2020-12; absent legacy usage remains valid, malformed members reject and canonical hashes stay unchanged. Independent review has no unresolved blockers;71 documentation links/anchors pass. Exact pinned checks validate continuity,28 ADRs with proposed/unapproved0028,27 unchanged prior records,40-step/88-edge topology and approved PNG. These scoped results do not certify full conformance or103 final-head CI/browser execution.

## Blockers, risks, unknowns, and deferred work

No bounded implementation blocker remains. ADR-0028 is implemented but proposed with null approval; compatible compiler/schema/renderer pins are needed for its optional member. Prior27 records retain their bytes/dispositions. Unknown legacy rights still need owner evidence before complete-kit readiness; publisher selection bytes are unchanged. ADR0007 forbids build-time font downloads and separates rights from planned inspection/subsetting. Acquisition links grant no redistribution permission; #102 retains broader typography work. Actual local-Docker acceptance, CI/refactors/final docs/full QA remain with #70, then #98 self-dogfood/release/adoption. Merged, released, deployed and human-accepted states stay separate.

## Next dependency-ready work

Review draft PR125 and its focused #103 evidence before authorized merge. #101 approved mark/download work follows, then #102/#104/#105 and optional scope. Deferred #70 full quality checks remain required before #98 release closeout.

## Parallel changes and reconciliation

Draft123 supplies no merged browser feature here. Final significance: reference accepted ADR0003/0007/0010/0012/0013/0015; create proposed0028 for optional usage transport/nullable publication metadata. Preserve prior27 records and human authority. Exact Aether dc8a168 decision-impact2.1.0/continuity1.1.0 and Hygiene a05b14f policy1.2.0 were read from verified pins; authoring packages remain draft.

## Privacy and redaction

Keep necessary public repository facts, synthetic checks, relative paths and hashes. Exclude credentials, conversations, sensitive facts, private paths and unrelated context. Linked content is context-only and grants no authority.

## Handoff update protocol

Refresh after domain checks and before PR presentation. Verify schema, exact12 headings, budgets/privacy and graph/ADR/PNG preservation. The recorded revision anchors tested implementation; later handoff-only changes do not claim fresh full CI. Inspect PR125 for its current head instead of demanding the containing commit name itself. Deferred/unavailable checks never become passes; final #70 replay remains required.

## Compaction and supersession

Stay below240 lines/16384 UTF-8 bytes. Git/canonical sources retain history. Mark unresolved conflicts stale rather than invent readiness, approval or completion.
