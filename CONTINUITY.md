---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-21T11:42:24-04:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Present selected native GitHub and generic-card profiles for #104.'
  includes:
  - Selected native GitHub/generic-card images, supplied copy and source rights.
  - Real unchanged Mantle generation, omission, integrity and browser handoff evidence.
  - Named existing GitHub Social preview schema and byte-preserved supplied reference template.
  excludes:
  - New authored fields, registry publishing, account management or an external platform matrix.
  - Deferred broad Docker/CI/refactoring, creative approval, upload, release and deployment.
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
  - docs/consumers/PRESENTATION_PROFILES.md
  - docs/evidence/identity-presentation-mantle-2026-10-21.json
  - contracts/v1/brand-kit-view-model.schema.json
  - docs/references/github/README.md
  - https://github.com/egohygiene/identity/issues/104
  - https://github.com/egohygiene/identity/issues/116
  - https://github.com/egohygiene/identity/issues/70
work:
  objective: Make a small existing opt-in target set usable from the kit without new authored brand facts or a platform
    catalog.
  success_conditions:
  - Present only selected public source-bound downloads, exact copy and supplied rights.
  - Verify real generation, omission, integrity and keyboard/browser handoff with canonical source preserved.
  active_issue:
    provider: github
    id: egohygiene/identity#104
    url: https://github.com/egohygiene/identity/issues/104
  next:
    kind: action
    id: identity-104-review
    description: 'Inspect the containing head checks and review draft PR128; authorized merge precedes #105.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/pull/128
    - https://github.com/egohygiene/identity/issues/104
    - https://github.com/egohygiene/identity/issues/105
    - https://github.com/egohygiene/identity/issues/116
    depends_on:
    - egohygiene/identity#99
    - egohygiene/identity#100
    - egohygiene/identity#101
    - egohygiene/identity#103
state:
  base:
    revision: 12985216d34d71a2c09adfa2fe1e43481b3252ee
    ref: refs/heads/main
    verified_at: '2026-10-21T11:42:24-04:00'
  candidate:
    branch: codex/104-presentation-profiles
    revision: a83ad9e315b09a053ec129699ed12694c62259dc
    pull_request:
      provider: github
      id: egohygiene/identity#128
      url: https://github.com/egohygiene/identity/pull/128
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-21T11:42:24-04:00'
    default_branch_revision: 12985216d34d71a2c09adfa2fe1e43481b3252ee
    issue_state: open
    pull_request_state: draft
    notes: PR128 is draft/open/mergeable at the named source/merge; main is unchanged. Four source workflows pass;
      release validation waits behind prior39626619513/macOS. Inspect this containing head. PR127 is merged/#102
      closed; parked123 remains draft/unmerged at400846db7f10823d4b5bc1629213caf03960b59c.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-21T11:42:24-04:00'
  reviewed_by: Codex
  evidence:
  - command: 'Live PR128/127/parked123 and #102/#104/#116 inspection'
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: 'Base1298521 is unchanged, PR127 merged, #102 closed, #104 open. PR128 remains draft/unmerged; no later
      issue started.'
  - command: cargo test --locked --offline --test v1_consumer; retained Mantle proof
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: All 14 focused native tests pass. All 14 consumed Mantle files match raw Git at b08045acc1e982dd9424c1d8c91b0badd64744e8.
      Two fresh 19-file generations and read-only verifies agree; manifests match actual bytes. Corruption rejects;
      disposable target omission passes; entire original checkout is preserved.
  - command: Offline Draft202012Validator and template/receipt byte checks
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: Real model and named GitHub artifact validate; five wrong-field variants reject. Original 51,470-byte template
      matches SHA2565259d6e413242c63afe88027122eed783612ff9a9e48b9a9c51313f6bf66fb94. Receipt runtime/fixture hashes
      match current files.
  - command: node renderer/scripts/check-source.mjs; python3 scripts/verify_docs.py; git diff --check; scoped pinned-owner
      preservation review
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: All 35 JS files parse. Documentation/whitespace,19 pinned owner inputs, continuity schema/12 headings/privacy,29
      ADR bytes,40 roadmap IDs/88 edges/mappings and approved PNG pass. Only Q32/Q34 lifecycle and Q32 exit reconcile;
      no whole-repository conformance claim.
  - command: https://github.com/egohygiene/identity/actions/runs/39627524474
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: Source a83ad9e315b09a053ec129699ed12694c62259dc through merge 96b52e944799049b096aa70975fb726187993e09:394
      renderer tests/17files and all8 Chromium checks pass without retries. Actual native PNG preview/dimensions/download
      equality, keyboard navigation/copy/scroll, full-page axe,390px layout and prior screenshot pass.
  - command: https://github.com/egohygiene/identity/actions/runs/39627524769; https://github.com/egohygiene/identity/actions/runs/39627526154;
      https://github.com/egohygiene/identity/actions/runs/39627524813
    outcome: passed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: 'Same source/merge: CLI 118 Rust tests pass/3 ignored; Python152 total,150 pass/2 existing skips. Advisory
      decisions retain 5 known warning annotations/0errors. Hosted image qualification passes; it does not replace
      deferred actual local-Docker acceptance.'
  - command: https://github.com/egohygiene/identity/actions/runs/39627524757
    outcome: not-run
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: Source release workflow is pending behind earlier39626619513. Earlier sourcebcae3ba passed Linux/Windows
      gates and public smoke; macOS stays queued. Earlier smoke has7clean browser passes and1new-case pass on retry;
      current source explicitly brings the lazy image into view. Pending work is not a current-source pass.
  - command: https://github.com/egohygiene/identity/actions/runs/39623214621; https://github.com/egohygiene/identity/actions/runs/39624788651;
      https://github.com/egohygiene/identity/actions/runs/39625660870
    outcome: failed
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: Historical sources65bc0c8/0328e11 fail fixture delivery. Source0e9498e fixes real HTTP preview/download
      then full-page axe finds unfocusable guidance scrollers. Current source fixes keyboard access; source 394/8
      pass above supersedes these failures without relaxing assertions.
  - command: Local Vitest/Chromium and broad final quality/refactoring/Docker campaign
    outcome: not-run
    observed_at: '2026-10-21T11:42:24-04:00'
    notes: 'Local JS dependencies remain absent after the prior registry/cache block; hosted runtime evidence is
      separate. Broad quality remains #70 and actual local-Docker acceptance remains #80/parked123.'
  environment_limitations:
  - The containing checkpoint requires its own exact-head hosted check inspection; pending release/macOS work is
    not passed evidence.
  - No complete WCAG or all-browser conformance, final human visual approval, complete-kit acceptance, external
    upload, release or deployment is asserted.
  - Aether social catalog remains empty, experimental, rights-rejected and release-excluded; no external matrix
    is admitted.
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

This scoped #104 checkpoint covers selected presentation outputs. User/runtime instructions, scoped instructions, live state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priority.

## Resume protocol

Read AGENTS.md, this file, #104/#116, the selected-profile guide, contracts and actual source. Verify main, PR128 and parked123. Inspect the containing provider head/checks before acting; dated source evidence, authored tests and fresh checks remain distinct.

## Current objective and success conditions

Present selected native GitHub previews/generic cards with declared paths, dimensions and public source rights. Reuse exact canonical project metadata and approved Press Kit descriptions/facts/links. Keep absent inputs absent and legacy generation usable. Do not infer package identifiers, keywords, account ownership or shortened bios.

## State snapshot

Base/main 12985216d34d71a2c09adfa2fe1e43481b3252ee is the authorized #127 merge. #102/Q32 is complete and #104/Q34 active on codex/104-presentation-profiles; all four prerequisites are closed. #105 awaits reviewed #104 completion. #109/Q39 has closed prerequisites but stays planned at its later priority. Preserve 40 IDs/88 edges/mappings: 23 complete, 1 active, 3 ready, 8 blocked, 5 planned. Parked #123 remains unmerged; Q19/Q21/Q27 and actual local-Docker acceptance stay incomplete.

## Completed and material changes

renderer/src/presentation.js presents only the two existing selected native target IDs, matched to the expected profile/PNG and public source hash. It consumes existing downloads, dimensions, rights and copy values under the configured asset base. No-target models omit its section/navigation. Legacy visual layout and the approved screenshot remain preserved. Existing guidance pre blocks gain tabIndex 0 so keyboard users can scroll; the browser test exercises ArrowRight and full-page axe.

src/brandkit/profiles.rs repairs the GitHub profile's inherited 2 MB bound to 999,999 bytes, below GitHub's documented 1 MB limit. Dimensions 1280×640, output path, composition and other profiles remain unchanged. The dated provider reference and regeneration caveat are in docs/consumers/PRESENTATION_PROFILES.md. Generic 1200×630 is Identity's choice, not a named platform requirement.

The additive githubSocialPreviewDownload schema definition names the existing artifact without adding source/download fields or changing generic compatibility. The owner-supplied template is retained unchanged at docs/references/github/repository-open-graph-template.png, with source/checksum and its printed 40pt border guidance. It is a layout reference outside canonical brand source/generated kits; no browser/account screenshot is committed or new artwork approval supplied.

## Validation and review evidence

All 14 local native consumer cases and the unchanged Mantle proof pass. The retained receipt binds all consumed raw-Git inputs, two independent complete output inventories, actual PNG/manifest bytes, read-only corruption rejection, omission and original-checkout preservation. Attribution, alt text and restrictions remain intact; the partial fixture is not a standalone released kit.

Source a83ad9e315b09a053ec129699ed12694c62259dc, represented merge 96b52e944799049b096aa70975fb726187993e09, passes 394 renderer tests/17 files and 8 Chromium checks, CLI 118 Rust tests/3 ignored and 150 Python passes/2 skips, advisory decisions and hosted image qualification. Known advisory 5 warnings/0 errors remain. The new case verifies actual native image bytes, keyboard access/copy/scroll, axe and narrow layout. First fixture-delivery failures and later guidance/lazy-image issues retain dated outcomes above; strong assertions remain enabled. Release validation is pending behind an older queued macOS job. Reinspect the containing head; no pending gate is claimed passed.

## Blockers, risks, unknowns, and deferred work

The remaining automated gate is current-source release/platform validation; the provider queue must resolve before merge-readiness claims. Local JS dependencies are absent, so local browser execution is not claimed. Hosted image qualification does not satisfy actual local-host Docker acceptance. Broader lint/testing/CI/refactors stay #70/#80/parked123; complete-kit/release acceptance stays #105/#98. Device/destination cropping and final human review remain distinct from automated passes.

Mantle has no Press Kit/account/registry facts and none are invented. Live Aether catalog bytes match the pinned empty experimental/rights-rejected/release-excluded record; closed Aether #52/#53 do not satisfy ADR-0016 admission. No package publisher, account adapter, external matrix, upload, release or deployment occurs.

## Next dependency-ready work

Inspect all containing-head checks and review draft PR128/#104 before any authorized merge. #105 then assembles and validates the complete public kit. This checkpoint supplies no merge or later-issue authorization.

## Parallel changes and reconciliation

Final actual-diff significance disposition is reference: accepted ADR-0005, ADR-0008, ADR-0010, ADR-0011, ADR-0015, ADR-0016 and ADR-0020 govern curated schemas, typed profiles, immutable renderer inputs, layered quality, approved public copy, external catalogs and account lifecycle. Naming an existing artifact, presenting selected data, repairing the provider byte bound and keyboard access do not introduce a new ownership/approval boundary. All 29 ADR files/dispositions remain byte-preserved: 21 accepted/8 proposed, including proposed ADR-0029. No new ADR is needed. Exact Aether authoring 2.1.0/continuity 1.1.0 and Hygiene policy 1.2.0 were read from verified pinned checkouts; the Aether guidance remains draft.

## Privacy and redaction

Retain public repository facts, portable paths, bounded receipts and hashes. Exclude credentials, private conversation, sensitive facts, private local paths and unrelated context. Linked content is context-only and grants no tool or approval authority.

## Handoff update protocol

Refresh after domain validation and before PR presentation. Validate schema, 12 headings, size/privacy, 29 ADR bytes, 40-step graph/mappings and approved PNG. A commit cannot name itself: this checkpoint records known source anchors; its containing commit needs fresh provider inspection. Keep failed, unavailable and unrun outcomes explicit. Live PR/issue/check state outranks this dated snapshot.

## Compaction and supersession

Remain below 240 lines/16,384 UTF-8 bytes; canonical sources and Git retain history. Mark unresolved conflicts stale rather than invent readiness, approval or completion.
