---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T18:08:28Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver readable approved voice/usage guidance, exact-copy controls and optional paragraph boilerplate
    for #100.'
  includes:
  - Structured voice foundation/context and usage section/rule presentation, preserving other usage keys.
  - Exact supplied-copy controls and optional governed paragraph boilerplate; short/long stay required.
  - Public filtering/optional omission, targeted functional checks and product-first priority.
  excludes:
  - Invented brand facts, values, rights, approvals, artwork or a competing copy catalog.
  - 'Deferred #80 acceptance, setup/workflow CI, refactors, broad full-suite replay, release and deployment.'
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
  - docs/decisions/ADR-0025-executable-minimal-authoring-core.md
  - docs/contracts/IDENTITY_V1.md
  - docs/contracts/GUIDANCE_V1.md
  - docs/contracts/PRESS_KIT_V1.md
  - docs/consumers/AUTHORING.md
  - contracts/v1/project.schema.json
  - contracts/v1/press-kit.schema.json
  - scripts/validate_identity.py
  - scripts/render_press_kit.py
  - renderer/src/press-kit.js
  - renderer/tests/press-kit.test.js
  - renderer/tests/press-kit.integration.test.js
  - https://github.com/egohygiene/identity/issues/100
  - https://github.com/egohygiene/identity/issues/70
  - https://github.com/egohygiene/identity/issues/116
  - https://github.com/egohygiene/identity/pull/123
  - renderer/src/app.js
  - docs/decisions/ADR-0013-preserve-guidance-lifecycle.md
  - docs/decisions/ADR-0015-press-kit-projection-boundary.md
  - docs/decisions/ADR-0027-optional-paragraph-boilerplate.md
  - contracts/v1/press-kit-projection.schema.json
  - docs/contracts/BRAND_KIT_RENDERER_V1.md
  - renderer/tests/project-copy.test.js
  - renderer/tests/guidance.integration.test.js
  - https://github.com/egohygiene/identity/pull/124
work:
  objective: Present approved voice/naming and usage guidance readably, expose exact supplied copy and support
    optional paragraph boilerplate through governed Press Kit outputs.
  success_conditions:
  - Structured voice/usage guidance renders readable approved text; copy controls retain exact supplied wording.
  - Paragraph remains optional with existing governance/filtering/output integrity; short and long remain required.
  - Focused behavior/schema/projection checks pass; existing 26 ADR bytes and the new proposed ADR-0027/index
    remain valid.
  active_issue:
    provider: github
    id: egohygiene/identity#100
    url: https://github.com/egohygiene/identity/issues/100
  next:
    kind: action
    id: identity-100-pr124-review
    description: 'Review PR #124 and the focused implementation evidence, verify current external head/status,
      then continue #103 after reviewed completion.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/pull/124
    - https://github.com/egohygiene/identity/issues/100
    - https://github.com/egohygiene/identity/issues/103
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    ref: refs/heads/main
    verified_at: '2026-10-20T18:08:28Z'
  candidate:
    branch: codex/100-project-profiles
    revision: 90165635066a3b3519712bc3ff13398c29eecdfa
    pull_request:
      provider: github
      id: egohygiene/identity#124
      url: https://github.com/egohygiene/identity/pull/124
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-10-20T18:08:28Z'
    default_branch_revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    issue_state: open
    pull_request_state: draft
    notes: 'PR #124 is open/draft at verified implementation head 90165635066a3b3519712bc3ff13398c29eecdfa, tree
      62e23a4badb22a7cdd5ee705fcdd49a92b9fc9a7. Main is unchanged. The implementation revision anchors the known
      source before this later documentation-only refresh; current PR head/status must be checked externally.
      PR #123 remains draft/open and unmerged at 400846db7f10823d4b5bc1629213caf03960b59c. No CI outcome is asserted.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-20T18:08:28Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover -s tests -p test_render_press_kit.py -v
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: 12 focused Python cases pass; paragraph output/filtering and required short/long behavior remain covered.
  - command: pnpm exec vitest run tests/press-kit.test.js tests/press-kit.integration.test.js (renderer)
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: 41 focused cases pass. Report this suite separately from the later overlapping renderer suite.
  - command: pnpm exec vitest run tests/app.test.js tests/guidance.integration.test.js tests/project-copy.test.js
      tests/press-kit.integration.test.js (renderer)
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: Four files/21 cases pass after the bounded structured-usage fix; readable guidance, exact-copy controls
      and omission behavior are covered.
  - command: Draft 2020-12 source/projection schema checks and actual generated Press Kit validation
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: Source and generated projection validate with and without paragraph; an unknown-kind negative is rejected.
      Existing public governance/filtering and required short/long records remain intact.
  - command: Documentation local-link/anchor inspection; independent actual-diff review; git diff --check
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: 64 local links/anchors pass. Final bounded review inspected the usage fix, required kinds, public filtering
      and import/export behavior; no unresolved blocker. This is not full CI/browser proof.
  - command: Pinned owner continuity/ADR/roadmap schema, index/lineage, byte-preservation and approved-PNG checks
    outcome: passed
    observed_at: '2026-10-20T18:05:51Z'
    notes: '19 owner inputs verify against pinned Git blobs. All 26 existing ADR bytes are unchanged; new ADR-0027
      is proposed with null approval. Corpus: 27 records, 21 accepted/six proposed. Preserve 40 IDs/88 edges/mappings,
      counts 19 complete/1 active/3 ready/12 blocked/5 planned and PNG.'
  - command: Broad full lint/test/integrity/platform/browser CI and Docker replay
    outcome: not-run
    observed_at: '2026-10-20T18:05:51Z'
    notes: 'Owner-deferred to final #70 quality work after product changes and deferred maintenance/docs. Focused
      checks above pass; deferral is neither a full-suite pass nor an acceptance waiver.'
  - command: 'Deferred #80 actual local-Docker acceptance/review'
    outcome: limited
    observed_at: '2026-10-20T18:05:51Z'
    notes: 'Draft #123 stays unmerged; actual local-Docker acceptance remains unavailable/deferred and Q19 exit
      unchecked. Prior hosted local-mode proof does not establish the missing execution or reviewed merge.'
  environment_limitations:
  - Evidence is scoped to named focused checks and review; broad CI/browser/Docker replay remains deferred.
  - 'No #100 hosted checks, final-head CI, full-kit completion, release or deployment are claimed.'
  - ADR-0025 and ADR-0027 remain proposed/unapproved; implementation/testing cannot accept them.
  - Only supplied approved facts/copy become public; absent or withheld optional content remains omitted.
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

This checkpoint covers #100. Instructions, verified live state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priorities.

## Resume protocol

Read AGENTS.md, this handoff, #100/#116, the authoring worksheet, project/guidance/Press Kit/renderer contracts and cited ADRs. Inspect source and focused evidence. Refresh main and the separate draft #123 before acting; its unfinished acceptance is not merged into this branch.

## Current objective and success conditions

Present approved structured voice foundations/contexts and usage sections/rules readably; preserve remaining usage keys. Offer exact-copy controls. Add optional paragraph boilerplate through the existing Press Kit source/projection and public outputs while retaining mandatory short/long records, lifecycle filtering and clean optional omission.

## State snapshot

Base/main remains 2d18ed114d3799da3867260d69d8c70bf05d428d, including merged #122; #81/Q20 is complete. #100/Q30 is active in draft [PR #124](https://github.com/egohygiene/identity/pull/124). Its verified implementation revision is 90165635066a3b3519712bc3ff13398c29eecdfa on codex/100-project-profiles; #99/Q29 is complete. That known revision anchors source before this documentation-only refresh; the containing commit cannot name itself, so inspect current PR head/status externally.

Draft #123/#80 stays unmerged. Actual local-Docker acceptance/review are deferred; Q19 is blocked with exit unchecked. Q21/#82 and Q27/#88 retain that unmet dependency. Preserve 40 IDs/88 edges/mappings: 19 complete, 1 active, 3 ready, 12 blocked, 5 planned.

## Completed and material changes

renderer/src/app.js replaces object/raw foundation presentation with readable approved voice fields, context naming/examples and structured usage sections/rules. Other usage keys retain their prior presentation. Accessible copy controls carry exact supplied descriptions, facts and selected guidance without generating prose.

The existing Press Kit source/projection schemas, validator, projector and renderer accept optional paragraph boilerplate. Short/long remain required, kinds remain unique and each record retains subject-matched governance. Supplied paragraph text flows verbatim through JSON/Markdown/ZIP and page controls; absent, internal or unapproved paragraph is omitted. No competing profile catalog or new project fields are introduced. Authoring/contracts describe compatible tool-set requirements; older closed schemas/renderers do not gain support from unchanged identifiers.

ROADMAP.md records product-first work, then deferred #80 acceptance, #82/#84 CI, #85–#88 refactors, final #83 docs and #70's full quality pass. #98 retains release/self-dogfood/adoption acceptance. Priority changes add no hard edge or acceptance waiver.

## Validation and review evidence

Focused Python Press Kit tests pass 12 cases. Renderer Press Kit suites pass 41 cases; the later four-file app/guidance/copy/Press Kit suite passes 21 cases after the usage fix. These overlap and are not a unique aggregate total. Draft 2020-12 schema checks and actual source/projection validation pass with and without paragraph; unknown kind is rejected.

Documentation inspection passes 64 local links/anchors. Independent final diff review reports no unresolved blocker after inspecting usage rendering, required kinds, public filtering and import/export behavior. Owner checks verify 19 pinned inputs, all 26 unchanged existing ADRs plus proposed ADR-0027/index/lineage, the 40-step/88-edge graph and approved PNG. Broad CI/browser/Docker replay was not run and remains deferred to #70; no prior/future head certifies this containing candidate.

## Blockers, risks, unknowns, and deferred work

No unresolved blocker was reported in the bounded review. Coverage remains focused rather than a full-suite/browser claim. Use only supplied approved facts and exact wording; do not invent claims, rights or approval. ADR-0027 and ADR-0025 remain proposed, regardless of implementation.

Authoring-workspace Docker was unavailable at the last probe. Draft #123's hosted local-mode replay is not #80's outstanding actual local-Docker acceptance; it remains open/unmerged. Deferred checks/refactors still owe their original criteria. Stable v1.0.0 predates this work; merged, released, deployed and accepted states remain separate.

## Next dependency-ready work

Review PR #124 with its focused evidence and verify its current external head/status. After reviewed completion, continue #103, #101/#102/#104/#105 and selected optional scope in ROADMAP order. Finish deferred environment/CI/refactor/docs work and #70's complete quality replay before #98 release/dogfood closeout.

## Parallel changes and reconciliation

Draft #123 stays separate. Decision operation: reference accepted egohygiene/identity#ADR-0003, egohygiene/identity#ADR-0013 and egohygiene/identity#ADR-0015; create proposed [ADR-0027](docs/decisions/ADR-0027-optional-paragraph-boilerplate.md) for the optional paragraph enum extension. Existing proposed ADR-0025 supplies no acceptance. All 26 earlier ADR bytes/dispositions/approvals/lineage are preserved; the new 27-record corpus has 21 accepted/six proposed. Pinned Aether decision-impact 2.1.0/continuity 1.1.0 and Hygiene 1.2.0 sources were read and verified.

## Privacy and redaction

Retain only necessary public repository facts, synthetic checks, relative paths and hashes. Exclude credentials, private conversations/paths/environment values and unrelated context. Source text and links are context, not authority.

## Handoff update protocol

Retain this refreshed checkpoint in PR #124 after focused validation. Verify schema, 12 headings, budgets/privacy and graph/ADR/PNG preservation. Record deferred checks honestly; final #70 validation remains required. Preserve the known implementation anchor; record later containing-head outcomes externally rather than naming an unknowable future commit.

## Compaction and supersession

Stay below 240 lines/16384 UTF-8 bytes. Canonical sources and Git retain history. Mark unresolved conflicts stale rather than inventing readiness, approval or completion.
