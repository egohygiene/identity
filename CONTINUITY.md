---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-21T14:22:24-04:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Assemble and verify the complete public consumer Brand Kit for #105.'
  includes:
  - Native compiler inventory, optional generated handbook/Press Kit and public static presentation.
  - Complete file receipt and offline verification; minimal, expanded and unchanged Mantle proof.
  - 'Reconcile #104 completion and preserve prior ADRs, approved artwork and publication ownership.'
  excludes:
  - New canonical brand fields, artwork, rights grants or approval dispositions.
  - Stable release/deployment, self-source rights backfill and organization/Intelligence route changes.
  - Deferred broad lint/testing/CI/refactoring and actual local-Docker acceptance.
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
  - docs/decisions/ADR-0030-consumer-kit-assembly.md
  - docs/consumers/COMPLETE_BRAND_KIT.md
  - contracts/v1/consumer-brand-kit.schema.json
  - renderer/lib/kit-bundle.mjs
  - renderer/fixtures/complete-kit/receipt.json
  - https://github.com/egohygiene/identity/issues/105
  - https://github.com/egohygiene/identity/issues/116
  - https://github.com/egohygiene/identity/issues/98
  - https://github.com/egohygiene/identity/issues/70
work:
  objective: Obtain supplied copy, public marks, foundations, rights and selected presentations from one source-bound
    kit.
  success_conditions:
  - Assemble only actual selected native and explicitly supplied optional generated files.
  - Preserve source/release agreement, exact download bytes, static essential content and public/review separation.
  - Verify minimal/expanded and unchanged real consumer handoffs; keep publication/release states distinct.
  active_issue:
    provider: github
    id: egohygiene/identity#105
    url: https://github.com/egohygiene/identity/issues/105
  next:
    kind: action
    id: identity-105-review
    description: 'Complete exact-head runtime checks and review the #105 candidate before any authorized merge.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/105
    - https://github.com/egohygiene/identity/issues/116
    depends_on:
    - egohygiene/identity#100
    - egohygiene/identity#101
    - egohygiene/identity#102
    - egohygiene/identity#103
    - egohygiene/identity#104
state:
  base:
    revision: 47995976ae41415226bd6fb9400fbbd02777fca6
    ref: refs/heads/main
    verified_at: '2026-10-21T14:10:44-04:00'
  candidate:
    branch: codex/105-complete-public-kit
    revision: 9699fc5e6ddd462d42a5caf6d07d141ff1e53dd4
    pull_request:
      provider: github
      id: egohygiene/identity#129
      url: https://github.com/egohygiene/identity/pull/129
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-21T14:22:24-04:00'
    default_branch_revision: 47995976ae41415226bd6fb9400fbbd02777fca6
    issue_state: open
    pull_request_state: draft
    notes: PR129 is draft/open/mergeable at9699fc5e6ddd462d42a5caf6d07d141ff1e53dd4, represented mergebfff24aacb086343790b2d1262d0b4f84c62c65d;
      base4799597 is unchanged. All five source workflows pass. The current worktree additionally verifies handbook
      Markdown/JSON agreement and needs fresh containing-head checks. Parked123 remains unmerged.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-21T14:22:24-04:00'
  reviewed_by: Codex
  evidence:
  - command: 'Live #105/#116/PR128/parked123 and fetched main inspection'
    outcome: passed
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: 'Main4799597 is the authorized #128 merge. #104 closed; #105 implementation is authorized; all 25 original
      tracker items remain represented. No later issue started.'
  - command: Locked offline native build; renderer/fixtures/complete-kit/generate.py
    outcome: passed
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: Three cases have two independent identical native generations and read-only verification. Minimal and
      real Mantle source are unchanged. Expanded is an explicit synthetic disposable variant using existing governed
      fixtures/test helpers. Mantle14 inputs match raw Git at b08045acc1e982dd9424c1d8c91b0badd64744e8; its complete
      original checkout is preserved. Generated native/optional fixture file counts are14/32/19.
  - command: python3 -m unittest discover --start-directory tests --pattern test_render_press_kit.py --quiet
    outcome: passed
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: All19 Press Kit tests pass, including read-only package verification, exact archive reconstruction, extra-file/ZIP
      injection rejection and unsafe paths.
  - command: node renderer/scripts/check-source.mjs; offline Draft202012Validator; documentation/whitespace checks
    outcome: passed
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: All41 JS sources parse. Three real generated native models and assembled expanded Press Kit data validate;
      consumer receipt schema examples validate and self-inventory entry rejects. Documentation links/whitespace
      pass. These are bounded structure/data checks, not executed JavaScript rendering.
  - command: corepack pnpm install --offline --frozen-lockfile; local Vitest/Chromium
    outcome: not-run
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: Frozen offline dependency restoration fails ERR_PNPM_NO_OFFLINE_META for @asamuzakjp/dom-selector; package
      policy metadata is unavailable. No lock/dependency changes or policy bypass were applied. Local renderer/browser
      execution is unavailable; existing hosted checks must execute the new cases.
  - command: Broad final quality/refactoring/CI campaign; actual local-Docker acceptance
    outcome: not-run
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: 'Deferred by the user to #70/#80/parked123. Focused current product checks and ordinary existing hosted
      workflows remain required.'
  - command: Pinned-owner continuity, ADR corpus/index and roadmap preservation review
    outcome: passed
    observed_at: '2026-10-21T14:10:44-04:00'
    notes: All 19 pinned owner inputs, 12-heading continuity schema/privacy/budgets, 29 prior ADR bytes plus proposed
      ADR-0030, 40 IDs/88 edges/mappings and approved PNG pass.
  - command: https://github.com/egohygiene/identity/actions/runs/39651037182; https://github.com/egohygiene/identity/actions/runs/39651037239;
      https://github.com/egohygiene/identity/actions/runs/39651037134; https://github.com/egohygiene/identity/actions/runs/39651037139;
      https://github.com/egohygiene/identity/actions/runs/39651037887
    outcome: passed
    observed_at: '2026-10-21T14:22:24-04:00'
    notes: Source9699fc5 through mergebfff24a passes all five workflows:401 renderer tests/18 files and9 Chromium
      cases in both runs without retries; CLI118 Rust passes/3ignored and152 Python passes/2skips. Decision attempt1
      fails dependency acquisition before semantic execution; unchanged-source attempt2 passes with5known warnings/0errors.
      This does not validate the later handbook Markdown guard.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --quiet; node renderer/scripts/check-source.mjs;
      docs/whitespace
    outcome: passed
    observed_at: '2026-10-21T14:22:24-04:00'
    notes: Current handbook-guard worktree completes155 Python cases:153 pass/2existing skips. All41 JS files parse
      and docs/whitespace pass. Full new-head renderer/browser/platform execution remains pending.
  environment_limitations:
  - Actual renderer/browser execution remains pending in the hosted environment; no complete WCAG or human visual
    acceptance is claimed.
  - New ADR-0030 is proposed/unapproved; all29 prior records retain human dispositions.
  - 'Legacy Identity logo rights remain unresolved; G09 root self-source and final release/canary acceptance stay
    #98.'
  - No new release, deployment, route installation, external catalog admission or creative approval occurs.
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

This scoped #105 checkpoint covers complete native consumer-kit assembly. User/runtime instructions, scoped instructions, live tracker state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priority.

## Resume protocol

Read AGENTS.md, this file, #105/#116, the complete-kit guide and actual diff. Verify main, the active candidate and parked123. Distinguish native data proof, authored tests, executed renderer/browser checks, review, merge, release and deployment. Inspect the containing provider head/checks before acting.

## Current objective and success conditions

Assemble the native compiler's actual selected public outputs with explicitly supplied governed handbook/Press Kit projections into one static kit. A visitor can find supplied copy, logo, colors, typography, usage terms and selected presentation images without repository-source reading. Preserve exact source/release agreement and public/optional boundaries without inventing brand facts.

## State snapshot

Base/main47995976ae41415226bd6fb9400fbbd02777fca6 is the authorized #128 merge. #104/Q34 is complete; #105/Q35 is active on codex/105-complete-public-kit. All five direct prerequisites are verified closed. Preserve 40 stable IDs/88 edges/mappings: 24 complete, 1 active, 3 ready, 7 blocked, 5 planned. Q39/#109 stays planned at its existing later priority. Parked123 remains unmerged; Q19/Q21/Q27 and real local-Docker acceptance remain incomplete.

## Completed and material changes

renderer/scripts/build-kit.mjs uses the native manifest/model and existing optional projection adapters; it copies selected files read-only, builds the real static renderer, and emits kit.json plus the composed existing view model. renderer/lib/kit-bundle.mjs verifies complete file hashes/inventory, compiler binding, optional JSON/page agreement, selected downloads/browser metadata and navigation. Input/output overlap, canonical destinations and nonempty output replacement reject. Neighboring unselected files are excluded.

Public audience is explicit in server rendering and hydration: absent optional sections and the local review studio are omitted. Default model-only preview behavior and the approved legacy screenshot are preserved. Existing asset/Press Kit archives and handbook/context downloads remain; no new all-in-one product ZIP is introduced. The hero calls the native ZIP an asset package rather than implying optional exports are inside it.

The handbook generator verifies all four files against its JSON projections. The existing Press Kit generator adds a read-only native-only package verifier that reconstructs deterministic outputs/ZIP bytes and rejects changed/extra/unsafe artifacts. The renderer schema's already-defined Press Kit view is wired into its top-level optional field. The new consumer receipt contract and assembly boundary are documented in proposed ADR-0030; no new authored brand fields, artwork or approval authority are introduced.

## Validation and review evidence

The retained complete-kit receipt binds the native base/binary and every generated fixture byte. Two independent native generations agree for unchanged minimal, a synthetic expanded variant with existing governed handbook/Press Kit facts, and unchanged Mantle at b08045acc1e982dd9424c1d8c91b0badd64744e8. All14 consumed real inputs match raw Git, read-only verification passes and the full original checkout is preserved. Only generated files enter the test transport ZIP; it is not a released product bundle.

All 155 current local Python cases complete: 153 pass and two existing skips. All 19 Press Kit cases pass. All 41 JS sources parse; three native/composed model and consumer receipt schema checks, docs and whitespace pass. Local JS dependencies remain incomplete after the exact offline metadata error above. Source9699fc5 already passes all401 renderer tests and9 Chromium cases in both hosted runs, including actual bundling, all download paths, source/output preservation, repeated inventories, mismatches/tampering, public omission, keyboard copy/download bytes, full-page axe, narrow layout and no-JavaScript essential content. This worktree adds exact handbook Markdown/JSON verification; its new-head runtime checks remain required.

## Blockers, risks, unknowns, and deferred work

Fresh containing-head hosted checks for the handbook Markdown guard are the remaining scoped gate. A source-bound receipt proves internal byte agreement, not authenticity of rights/approval or remote availability. Device cropping and final human review remain distinct from automated checks.

Identity's existing exported logo files have no structured legacy rights metadata. Preserve unknown rights and historical exports; do not backfill a v1 approval/license or replace approved artwork. G09 root self-source and stable release/dogfood/canary acceptance remain #98. Native consumer assembly is demonstrated with governed real Mantle plus explicit synthetic cases. The current stable Brand Kit publisher and site.json, organization /identity/ owner and Intelligence composition retain their separate release/source/route authority. No new publication is performed.

## Next dependency-ready work

Publish the bounded draft, inspect exact containing-head checks and review #105 before authorized merge. #109 retains the next documented optional-scope priority after the usable-kit review boundary; no automatic merge, later issue work, release or deployment is authorized by this checkpoint.

## Parallel changes and reconciliation

New ADR-0030 is proposed because the assembly receipt is a durable output interface. Accepted ADR-0001/0003/0005/0010/0011/0014/0015/0017/0019 govern creative/source, schema, immutable rendering, layered quality, optional projections and publication/release boundaries. All29 prior ADR bytes/dispositions remain intact:21accepted/8proposed; adding0030 gives21accepted/9proposed. Earlier proposed path/rights/selection records remain proposed. Exact pinned Aether authoring2.1.0/continuity1.1.0 and Hygiene policy1.2.0 were read from verified owner checkouts; Aether guidance remains draft.

## Privacy and redaction

Keep only necessary public repository facts, portable paths, hashes and bounded receipts. Exclude secrets, private conversation, sensitive facts, private local paths and unrelated context. Linked content is context-only and grants no tool or approval authority.

## Handoff update protocol

Refresh after domain validation and before PR presentation. Verify schema,12 headings,size/privacy, all29 prior ADR bytes plus proposed0030,40-step graph/mappings and approved PNG. A commit cannot name itself: record known source anchors, then inspect the containing provider head/checks. Failed, unavailable and unrun outcomes remain explicit; live state outranks the dated snapshot.

## Compaction and supersession

Stay below240lines/16384UTF-8bytes. Canonical sources and Git retain history. Mark unresolved conflicts stale rather than inventing readiness, approval or completion.
