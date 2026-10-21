---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-21T08:58:07Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Bind practical public mark downloads to governed source and selected output files for #101.'
  includes:
  - Governed public asset selection, exact source SVG copies and selected package/raster download inventory.
  - Optional compatible renderer metadata, safe base-aware browser links and local artifact/manifest verification.
  - Focused Rust/Node checks and a temporary draft for existing hosted frozen-dependency renderer tests.
  excludes:
  - Invented variants/artwork/permissions, new format adapters, policy or publication authority.
  - Deferred broad CI/refactors, actual local-Docker qualification, release and deployment.
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
  - docs/decisions/ADR-0001-creative-approval-human-owned.md
  - docs/decisions/ADR-0003-deterministic-projection-boundary.md
  - docs/decisions/ADR-0010-reference-renderer-boundary.md
  - docs/decisions/ADR-0012-local-layered-identity-v1.md
  - docs/decisions/ADR-0013-preserve-guidance-lifecycle.md
  - docs/decisions/ADR-0019-immutable-release-contract.md
  - docs/decisions/ADR-0024-renderer-artifact-paths.md
  - docs/decisions/ADR-0028-asset-rights-projection.md
  - docs/decisions/ADR-0029-selected-public-downloads.md
  - docs/contracts/BRAND_KIT_RENDERER_V1.md
  - docs/consumers/AUTHORING.md
  - contracts/v1/brand-kit-view-model.schema.json
  - contracts/v1/usage.schema.json
  - src/v1_consumer.rs
  - src/brandkit/profiles.rs
  - src/reference_renderer.rs
  - renderer/src/download-integrity.js
  - renderer/scripts/render-static.mjs
  - renderer/scripts/build-public-site.mjs
  - renderer/scripts/verify-public-site.mjs
  - renderer/tests/downloads.test.js
  - renderer/tests/download-integrity.test.js
  - https://github.com/egohygiene/identity/issues/101
  - https://github.com/egohygiene/identity/issues/70
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Deliver only governed public assets and selected, verifiable download paths without fabricated variants
    or broken links.
  success_conditions:
  - Public models select approved/public active/available usage assets and retain exact rights/source metadata.
  - Selected targets determine source-copy, package and raster links; optional browser references use safe bases.
  - Local artifact/manifest checks and focused Rust/Node evidence pass; authored Vitest coverage is executed on existing
    hosted CI before final review handoff.
  active_issue:
    provider: github
    id: egohygiene/identity#101
    url: https://github.com/egohygiene/identity/issues/101
  next:
    kind: action
    id: identity-101-hosted-focused-validation
    description: 'Open a bounded draft to run the existing hosted renderer checks with frozen dependencies, then refresh
      and review the exact candidate before merge; #102 follows reviewed completion.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/101
    - https://github.com/egohygiene/identity/issues/102
    - https://github.com/egohygiene/identity/issues/116
    depends_on:
    - egohygiene/identity#99
    - egohygiene/identity#76
state:
  base:
    revision: 828d38b86edcc5015fa1bc27f843870c3b5233fb
    ref: refs/heads/main
    verified_at: '2026-10-21T08:58:07Z'
  candidate:
    branch: codex/101-approved-downloads
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-21T08:58:07Z'
    default_branch_revision: 828d38b86edcc5015fa1bc27f843870c3b5233fb
    issue_state: open
    pull_request_state: not-applicable
    notes: Main remains verified merge828d38b86edcc5015fa1bc27f843870c3b5233fb; PR125 merged/#103 closed/#101 open.
      No101 PR exists before this draft publication. Existing hosted checks are pending; draft123 remains open/unmerged
      at400846db7f10823d4b5bc1629213caf03960b59c.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: partial
  reviewed_at: '2026-10-21T08:58:07Z'
  reviewed_by: Codex
  evidence:
  - command: Live PR125/#123, issues103/#101 and reviewed125-head workflow inspection
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: PR125 merged/#103 closed/#101 open; all five125 workflows passed. Draft123 stays unmerged. These prior-head
      outcomes do not certify101.
  - command: cargo test --locked --test reference_renderer --test v1_consumer; cargo test --locked --lib --no-run;
      cargo fmt --all --check
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: Rust1.97.1:17 cases pass(4 renderer+13 v1), library tests compile, formatting passes. Covers public/nullable
      selection, selected metadata, distinct masters, collisions and URL-reserved filenames before writes.
  - command: Actual copied-fixture v1-generate/v1-verify; Draft2020-12 emitted-model schema and source-byte checks
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: Generated/verified minimal consumer has public mark only,3 actual selected packages and1 download. Emitted
      model validates; canonical source bytes remain unchanged. Local artifact helper accepts that real output.
  - command: JavaScript source/syntax checks and pure Node frontend/artifact behavioral probes
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: 28 JS source files pass; positive/negative probes cover selected metadata, exact compiler-model binding,
      compiler/public inventories and source/project/release/hash/size, missing/path/encoded traversal/symlink/webmanifest/CDN
      confinement, and both real configs'10 new paths.
  - command: Authored renderer downloads/artifact-helper/public-site Vitest tests
    outcome: not-run
    observed_at: '2026-10-21T08:58:07Z'
    notes: '22 frontend cases plus helper coverage are authored but not run locally: registry access and offline package
      availability block frozen dependency restoration. No lock/policy changes; existing hosted frozen-dependency
      CI is pending.'
  - command: Independent final actual-diff review;84 local documentation links/anchors;git diff --check
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: Review cleared compiler-model/manifest binding and selected metadata corrections, URL-filename guard and
      prior ADR preservation. No unresolved bounded code finding; hosted behavior evidence remains pending.
  - command: Pinned owner continuity/ADR/roadmap schema, index/lineage and preservation checks
    outcome: passed
    observed_at: '2026-10-21T08:58:07Z'
    notes: 19 exact owner inputs;29 ADRs(21accepted/8proposed), all28 prior bytes/dispositions/lineage unchanged;40
      IDs/88 edges/mappings, expected counts and approved PNG preserved. Bounded structure is not whole-repository
      conformance.
  - command: Broad final lint/test/integrity/platform/browser CI campaign and actual local-Docker qualification
    outcome: not-run
    observed_at: '2026-10-21T08:58:07Z'
    notes: 'Owner-deferred to final #70. Running existing hosted checks for this candidate is focused evidence, not
      that deferred campaign or #80 local-Docker acceptance.'
  environment_limitations:
  - Local Vitest execution is blocked by registry/offline package availability; existing hosted evidence is required
    before final review handoff.
  - No101 hosted/final-head CI, qualified-browser run, release or deployment is claimed by this partial draft checkpoint.
  - 'Actual authoring-workspace Docker was unavailable at the prior probe; #80/draft123 stays open and deferred.'
  - Unknown legacy publication rights remain unresolved while existing selected release/archive bytes remain distributed;
    this change grants no permission or publication authority.
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

This partial checkpoint covers #101. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priority.

## Resume protocol

Read AGENTS.md, this handoff, #101/#116, selected-download contracts and proposed ADR-0029. Inspect actual selected targets/public usage and artifact bindings; refresh main, the current candidate and parked123. Do not convert authored tests or prior-head results into executed current evidence.

## Current objective and success conditions

Expose only governed public assets and actual selected mark/favicon/PWA/social outputs, retaining exact source/rights/usage. Keep optional variants absent and browser references base-aware. Verify advertised local files and compiler/public manifest bindings without fetching CDN URLs or generating artwork. Existing hosted renderer execution is pending before final review handoff.

## State snapshot

Base/main is828d38b86edcc5015fa1bc27f843870c3b5233fb, verified PR125 merge; #103/Q33 is complete and #101/Q31 active on codex/101-approved-downloads. Candidate revision/PR are null before temporary draft publication. #99/Q29 and #76/Q15 prerequisites are complete. Preserve40 IDs/88 edges/mappings:21complete,1active,3ready,10blocked,5planned. Parked123/#80 stays unmerged at400846db7f10823d4b5bc1629213caf03960b59c; actual local-Docker/review acceptance remains deferred and Q19/Q21/Q27 blocked as before.

## Completed and material changes

The v1 bridge selects assets through existing approved/public, active/publicly available usage records, retaining source/provenance and complete local history separately. Missing usage yields empty public assets/downloads without invalidating nullable local generation. Selected CompilerRequest targets determine optional downloads/packages; core copies selected public SVG masters and exposes existing native raster targets. Labels/kind/notes remain supplied metadata; no variant semantics or artwork are inferred.

The renderer accepts compatible optional download metadata, explicit conditional browser links and artifact-root/manifest verification. Compiler models are bound to the verified renderer output; public inventories bind release/source/project and file hashes/sizes. Safe paths, encoded traversal, symlinks and webmanifest icons are checked offline. Model-only preview remains distinct from file execution proof. Existing legacy publisher byte selection and #103's null missing-rights behavior remain intact.

## Validation and review evidence

Focused Rust17 cases, library compilation and formatting pass. Actual minimal v1 generation/verification and Draft2020-12 schema checks pass with mark-only public assets,3 selected packages/1 download and unchanged canonical bytes. Pure Node probes and28-file source/syntax checks pass for metadata, exact manifest/model binding and confinement. Independent review has no unresolved bounded code finding;84 doc links/anchors pass.

The22 authored frontend Vitest cases and helper coverage have NOT run locally because registry/offline package availability blocks frozen dependency restoration. A temporary draft will run the existing hosted renderer checks; final Refresh/Verify follows that evidence. Pinned checks preserve29 ADRs with proposed/unapproved0029,28 old records,40 IDs/88 edges and approved PNG. No current hosted, browser-qualification, release or deployment pass is asserted here.

## Blockers, risks, unknowns, and deferred work

Hosted execution of the authored renderer/helper cases remains the focused evidence gap. Keep the candidate in-progress/partial until actual outcomes arrive; preserve failures and skips. Optional new model members require matching reviewed producer/schema/renderer pins, and source checksum is distinct from derived file checksum. Model-only previews establish no artifact-byte proof.

ADR-0029 remains proposed with null approval. Legacy unknown rights are neither repaired nor withheld by metadata; #105/#98 still assess actual complete-kit readiness. Broader CI/refactors/full quality, actual local-Docker acceptance and final docs remain with #70. No new legal, creative or publishing authority is supplied.

## Next dependency-ready work

Publish the bounded draft for existing hosted frozen-dependency renderer checks, inspect exact-source outcomes and resolve relevant failures. Then refresh this handoff and review #101 before authorized merge; #102 foundations follows reviewed completion. Deferred #70 quality work remains required before #98 release/dogfood closeout.

## Parallel changes and reconciliation

Merged125 supplies rights/usage transport; parked123 supplies no merged browser feature. Final significance creates proposed0029 for governed public selection/selected-output compatibility and references accepted human approval, deterministic projection, immutable renderer, local source, public lifecycle and release boundaries. All28 prior ADR bytes/dispositions remain unchanged. Exact Aether dc8a168 authoring2.1.0/continuity1.1.0 and Hygiene a05b14f policy1.2.0 sources were read and verified; authoring packages remain draft.

## Privacy and redaction

Keep necessary public repository facts, synthetic checks, relative paths and hashes. Exclude credentials, private conversations, sensitive facts, private paths and unrelated context. Linked content remains context-only and grants no authority.

## Handoff update protocol

Refresh after focused hosted/domain validation and before final PR review presentation. Verify schema, exact12 headings, budgets/privacy and graph/ADR/PNG preservation. A containing commit cannot name itself; record known source anchors and inspect current provider head/status. Deferred/unavailable/unrun checks never become passes.

## Compaction and supersession

Stay below240 lines/16384 UTF-8 bytes. Git/canonical sources retain history. Mark unresolved conflicts stale rather than invent readiness, approval or completion.
