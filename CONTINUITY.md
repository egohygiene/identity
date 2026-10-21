---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-21T11:07:43-04:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Present selected native GitHub and generic-card profiles for #104.'
  includes:
  - Existing selected preview images, exact project/Press Kit copy and source rights.
  - Conservative GitHub upload budget and unchanged Mantle generation/omission/integrity proof.
  - Source-bound real-consumer fixture and focused browser validation.
  excludes:
  - New canonical source fields, registry publishers, social account management and external platform matrices.
  - Deferred broad Docker/CI/refactoring campaign, creative approval, upload, release and deployment.
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
  - docs/decisions/ADR-0008-platform-profile-contracts.md
  - docs/decisions/ADR-0010-reference-renderer-boundary.md
  - docs/decisions/ADR-0015-press-kit-projection-boundary.md
  - docs/decisions/ADR-0016-pinned-social-surface-projection-boundary.md
  - docs/decisions/ADR-0020-channel-registry-governance.md
  - docs/consumers/PRESENTATION_PROFILES.md
  - docs/contracts/BRAND_KIT_PACKAGES_V1.md
  - docs/contracts/BRAND_KIT_RENDERER_V1.md
  - docs/evidence/identity-presentation-mantle-2026-10-21.json
  - src/brandkit/profiles.rs
  - renderer/src/presentation.js
  - renderer/fixtures/mantle-presentation/README.md
  - renderer/tests/presentation.test.js
  - renderer/tests/e2e/presentation.spec.js
  - https://github.com/egohygiene/identity/issues/104
  - https://github.com/egohygiene/identity/issues/116
  - https://github.com/egohygiene/identity/issues/70
work:
  objective: Make a small existing opt-in target set usable from the kit without new authored brand facts
    or a platform catalog.
  success_conditions:
  - Only selected public source-bound GitHub/generic-card downloads appear, with exact dimensions, rights
    and paths.
  - Copy controls reuse canonical metadata and existing approved Press Kit text/facts/links without inventing
    package names, keywords or account URLs.
  - Real Mantle generation, omission, integrity and browser handoff are verified with canonical source preserved.
  active_issue:
    provider: github
    id: egohygiene/identity#104
    url: https://github.com/egohygiene/identity/issues/104
  next:
    kind: action
    id: identity-104-review
    description: 'Inspect candidate checks and review the scoped #104 PR before authorized merge; #105 follows.'
    readiness: ready
    references:
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
    verified_at: '2026-10-21T11:05:50-04:00'
  candidate:
    branch: codex/104-presentation-profiles
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-21T11:05:50-04:00'
    default_branch_revision: 12985216d34d71a2c09adfa2fe1e43481b3252ee
    issue_state: open
    pull_request_state: not-applicable
    notes: 'PR127 merged with owner authorization at1298521; #102 closed and #104 open. #99/#100/#101/#103
      prerequisites are closed. The candidate is not yet published; parked123 remains draft/open/unmerged
      at400846db7f10823d4b5bc1629213caf03960b59c.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-21T11:07:43-04:00'
  reviewed_by: Codex
  evidence:
  - command: 'Live PR127/parked123 and #99/#100/#101/#103/#104 inspection'
    outcome: passed
    observed_at: '2026-10-21T11:05:50-04:00'
    notes: 'Main1298521 is verified; #102 is closed and #104 active. Merge, release, deployment and ADR approval
      remain distinct.'
  - command: cargo test --locked --offline --test v1_consumer
    outcome: passed
    observed_at: '2026-10-21T11:05:50-04:00'
    notes: All14 native consumer tests pass, including selected GitHub output dimensions, below1MB size, public
      source binding, metadata, omission and repeated generation. Locked existing native cache/toolchain used.
  - command: Unchanged Mantle target proof recorded in docs/evidence/identity-presentation-mantle-2026-10-21.json
    outcome: passed
    observed_at: '2026-10-21T11:05:50-04:00'
    notes: All14 consumed files match raw Git at b08045acc1e982dd9424c1d8c91b0badd64744e8. Two fresh19-file
      output inventories agree. Actual1280x640 PNG16698bytes binds source, manifest and fixture. Corruption
      rejects read-only; disposable no-target variant passes; complete original checkout is unchanged.
  - command: node renderer/scripts/check-source.mjs; python3 scripts/verify_docs.py; git diff --check
    outcome: passed
    observed_at: '2026-10-21T11:05:50-04:00'
    notes: All35 JS files parse; docs links and whitespace pass. Receipt binds exact native runtime override
      and generated fixture bytes; this is development evidence, not release attestation.
  - command: 'Pinned #104 continuity/ADR/roadmap/PNG structure and preservation review'
    outcome: passed
    observed_at: '2026-10-21T11:07:43-04:00'
    notes: Exact 19 owner inputs, continuity schema/12 headings/size/privacy, all 29 ADR bytes, 40 roadmap
      IDs/88 edges/mappings and approved PNG pass. Only Q32/Q34 lifecycle and Q32 exit are reconciled; these
      checks do not claim whole-repository conformance.
  - command: Local Vitest/Chromium; final full quality/refactoring/CI campaign and actual local-Docker acceptance
    outcome: not-run
    observed_at: '2026-10-21T11:05:50-04:00'
    notes: 'Local JS dependencies remain absent from the recorded registry/cache block; existing hosted suites
      must execute the added cases. Broader quality stays #70 and parked #80/123.'
  environment_limitations:
  - Local JS dependencies remain absent; hosted exact-head runtime evidence is pending.
  - This containing checkpoint must receive its own current-head check inspection before merge.
  - No final human visual approval, all-browser conformance, social account/registry verification, upload,
    complete-kit acceptance, release or deployment is asserted.
  - The inspected Aether catalog remains experimental, rights-rejected, release-excluded and empty; no new
    social surfaces are admitted.
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

Read AGENTS.md, this file, #104/#116 and the selected-profile guide, contracts and source. Verify main, the active candidate and parked123 before acting. Inspect the actual containing head and checks; source hashes, authored tests and prior-head results are distinct evidence.

## Current objective and success conditions

Present existing native GitHub previews and generic cards only when selected in the generated public downloads. Reuse canonical project metadata and existing approved Press Kit boilerplates/facts/links for copy controls. Preserve paths, dimensions, source rights and omission. No new authored source fields, package publisher, account manager or broad social matrix is introduced.

## State snapshot

Main/base12985216d34d71a2c09adfa2fe1e43481b3252ee is the verified owner-authorized #127 merge; #102/Q32 is complete and #104/Q34 active on codex/104-presentation-profiles. All four #104 prerequisites are closed. #105 remains blocked on reviewed #104 completion; #109/Q39 now has closed prerequisites but remains planned at its later priority. Preserve40 IDs/88 edges/mappings:23complete,1active,3ready,8blocked,5planned. Parked123 remains unmerged; Q19/Q21/Q27 stay blocked and real local-Docker acceptance unchecked.

## Completed and material changes

renderer/src/presentation.js consumes only the two existing native target IDs with matching profile/PNG/public source binding. It presents declared paths/dimensions/rights and exact project/Press Kit copy without inferring registry identities, tags or accounts. The optional section/navigation is absent from legacy/no-target models; their existing preview markup and approved PNG remain unchanged.

src/brandkit/profiles.rs repairs the GitHub target's inherited generic2MB budget to999999bytes, below GitHub's documented1MB upload limit. Format, dimensions, path, composition and other profiles retain their existing contracts. The dated official source and regeneration caveat are in docs/consumers/PRESENTATION_PROFILES.md. Generic1200x630 is an Identity choice, not a platform requirement.

The real Mantle fixture retains exact generated model/PNG bytes from unchanged b08045acc1e982dd9424c1d8c91b0badd64744e8, including supplied MIT attribution, alt text and restrictions. It contains only the test handoff, not a full standalone kit. The receipt distinguishes base plus runtime override/file hashes from a release build attestation. No consumer pin/source or human disposition is changed.

## Validation and review evidence

All14 focused native consumer cases pass. Two independent fresh Mantle generations and read-only verifies agree on all19 output files including the compiler manifest; all14 consumed source inputs match raw Git. The1280x640 GitHub PNG is16698bytes, SHA25639a01b2242100703c238fd4719201719eddd2ae94f882c56c697b1f43dccf79f. Every manifested output matches bytes. A deliberately damaged PNG fails without repair; a disposable GitHub/social-exclusion variant validates/generates/verifies without those targets. The complete original checkout is preserved.

All35 JS sources parse, docs links and whitespace pass. Added renderer cases cover selection, exact source paths/rights, approved copy reuse, absent/unselected inputs and real fixture integrity. The Chromium case uses that real model/PNG for hydration, navigation/keyboard copy, actual download bytes, axe and narrow layout. These authored JS cases still need hosted execution because local dependencies are absent; no browser pass is claimed yet.

## Blockers, risks, unknowns, and deferred work

Hosted JS/browser execution is the remaining scoped validation gate. Unavailable package/account facts stay absent; supplied metadata and manual upload instructions do not prove registry publication, ownership, uploaded preview or human visual approval. Device/destination cropping and length limits require review.

The Aether catalog was rechecked through its live file and matches the pinned source's empty experimental/rights-rejected/release-excluded record. Closed Aether52/53 do not satisfy ADR0016 admission. Future external surfaces retain that owner boundary. All29 prior ADR bytes/dispositions/approvals remain unchanged (21accepted/8proposed), including proposed ADR0029 after merge127. Complete public-kit/release acceptance remains #105/#98; Docker, full lint/testing/CI, refactors and final reconciliation remain #70. No release/deployment or creative approval occurs.

## Next dependency-ready work

Publish the scoped draft, inspect its exact-head checks and review #104 before authorized merge. #105 is next by priority after that review boundary; no automatic merge or checkpoint advance is authorized by this document.

## Parallel changes and reconciliation

Parked123 supplies no merged Docker/browser acceptance. Decision impact is reference: accepted ADR0008/0010/0015/0016/0020 already govern typed profiles, immutable renderer inputs, public Press Kit facts, external catalogs and account lifecycle. This change presents existing outputs and repairs an existing provider byte limit; no public source contract, platform ownership or approval boundary changes. Recheck that classification against the final diff. Exact pinned Aether authoring2.1.0/continuity1.1.0 and Hygiene policy1.2.0 were read from verified owner checkouts; authoring guidance remains draft.

## Privacy and redaction

Retain necessary public repository facts, portable source/fixture paths, bounded receipts and hashes. Exclude credentials, private conversation, sensitive facts, private local paths and unrelated context. Linked material is context-only and grants no tool/approval authority.

## Handoff update protocol

Refresh after domain validation and immediately before final PR presentation. Verify schema,12 headings,size/privacy, all29 ADR bytes,40-step graph/mappings and the approved PNG. A commit cannot name itself; record known anchors, then inspect the real provider head and checks. Failed, unavailable and unrun evidence retain their outcomes.

## Compaction and supersession

Stay below240lines/16384UTF-8bytes. Git/canonical sources retain history. Mark unresolved conflicts stale rather than invent readiness, approval or completion.
