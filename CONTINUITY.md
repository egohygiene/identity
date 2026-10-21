---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-21T09:14:54Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Bind practical public mark downloads to governed source and selected output files for #101.'
  includes:
  - Governed public asset selection, exact source SVG copies and selected package/raster download inventory.
  - Optional compatible renderer metadata, safe base-aware browser links and local artifact/manifest verification.
  - Focused local checks and existing hosted CLI, renderer, release-gate, image and decision evidence.
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
  - migration/empathy-extraction-evolution-v1.json
  - publication/release-configs/index.json
  - https://github.com/egohygiene/identity/pull/126
work:
  objective: Deliver only governed public assets and selected, verifiable download paths without fabricated variants
    or broken links.
  success_conditions:
  - Public models select approved/public active/available usage assets and retain exact rights/source metadata.
  - Selected targets determine source-copy, package and raster links; optional browser references use safe bases.
  - Local artifact checks and existing hosted Rust, Python, renderer/browser and reproducibility gates pass.
  active_issue:
    provider: github
    id: egohygiene/identity#101
    url: https://github.com/egohygiene/identity/issues/101
  next:
    kind: action
    id: identity-101-review
    description: 'Review PR126 and inspect checks for the containing documentation commit; #102 follows reviewed completion
      and authorized merge.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/pull/126
    - https://github.com/egohygiene/identity/issues/102
    - https://github.com/egohygiene/identity/issues/116
    depends_on:
    - egohygiene/identity#99
    - egohygiene/identity#76
state:
  base:
    revision: 828d38b86edcc5015fa1bc27f843870c3b5233fb
    ref: refs/heads/main
    verified_at: '2026-10-21T09:14:54Z'
  candidate:
    branch: codex/101-approved-downloads
    revision: 3f03f9b10dd0a7e6e2c292cadabb737e7902e56f
    pull_request:
      provider: github
      id: egohygiene/identity#126
      url: https://github.com/egohygiene/identity/pull/126
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-21T09:14:54Z'
    default_branch_revision: 828d38b86edcc5015fa1bc27f843870c3b5233fb
    issue_state: open
    pull_request_state: draft
    notes: PR126 open/draft at source 3f03f9b10dd0a7e6e2c292cadabb737e7902e56f, tested via merge 465107d837e3d12e1457f6fdacad2bbbc4ffe213;
      base/main unchanged. This source anchor precedes the containing continuity/ADR commit, whose new checks must
      be inspected. PR125 merged/#103 closed/#101 open; parked123 remains unmerged at400846db7f10823d4b5bc1629213caf03960b59c.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#123
    url: https://github.com/egohygiene/identity/pull/123
review:
  status: passed
  reviewed_at: '2026-10-21T09:14:54Z'
  reviewed_by: Codex
  evidence:
  - command: Live PR126/#123, issues101/#103 and target-base inspection
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: PR126 open/draft;101 open/103 closed; base828d38b unchanged. Candidate phase records scoped review readiness,
      not provider draft conversion, merge or release.
  - command: https://github.com/egohygiene/identity/actions/runs/39574561355
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: 'Exact source3f03f9b/merge465107d: all CLI steps pass;117 Rust tests pass/3 ignored; Python152 total=150
      pass/2 skip. Provenance:17 byte-identical,3 evolved;8 v0 profiles/45 targets. Clippy, formatting, docs and config
      pins pass.'
  - command: https://github.com/egohygiene/identity/actions/runs/39574561241; release public smoke job119136742609
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: 'Exact source3f03f9b: frozen dependencies restored;349 Vitest tests in15 files and6 Chromium checks pass,
      including authored download/helper coverage. Local registry/cache remained unavailable; no lock or dependency-policy
      change.'
  - command: https://github.com/egohygiene/identity/actions/runs/39574561234; https://github.com/egohygiene/identity/actions/runs/39574561648
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: 'Exact source3f03f9b: Linux/macOS/Windows source-install, contracts and clean-room reproducibility gates
      pass; public smoke and hosted development-image qualification pass. No release/tag/deployment or actual authoring-workspace
      Docker acceptance is asserted.'
  - command: https://github.com/egohygiene/identity/actions/runs/39574562283
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: 'Exact source3f03f9b: decision workflow succeeds with5 retained warning annotations and no errors. Advisory
      findings are not approval or whole-repository conformance.'
  - command: Focused local Rust17; actual v1-generate/v1-verify/schema/source checks;Node probes;28-file source check;doc
      links
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: Actual minimal output has public mark only,3 selected packages/1 download and unchanged source bytes. Model/manifest/hash/path/symlink/webmanifest
      confinement, both configs'10 new paths and release-config digest verification pass. Independent review cleared
      model-binding and filename findings.
  - command: Pinned owner continuity/ADR/roadmap schema, index/lineage, preservation and git diff --check
    outcome: passed
    observed_at: '2026-10-21T09:14:54Z'
    notes: 19 owner inputs;29 ADRs(21 accepted/8 proposed);all28 prior bytes/dispositions unchanged. ADR0029 implemented/proposed/null
      approval;40 IDs/88 edges/mappings and approved PNG preserved. Scope-bounded structural validation.
  - command: Broad final quality/refactoring/CI campaign and actual local-Docker acceptance
    outcome: not-run
    observed_at: '2026-10-21T09:14:54Z'
    notes: 'Owner-deferred to #70 and parked #80/123. Existing candidate gates do not complete that campaign, all-browser
      qualification, complete-kit readiness or #98 release/dogfood acceptance.'
  environment_limitations:
  - Local frozen JavaScript restoration was unavailable; hosted renderer/browser tests executed successfully for the
    recorded source.
  - Source3f03f9b precedes this continuity/ADR commit; inspect the actual final provider head and its checks before
    merge.
  - 'Actual authoring-workspace Docker remains unqualified; #80/draft123 is open/deferred despite hosted image success.'
  - Unknown legacy rights remain unresolved while existing release/archive bytes are distributed; no permission is
    granted.
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

This scoped review checkpoint covers #101. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and #116 own dependencies and product-first priority.

## Resume protocol

Read AGENTS.md, this handoff, #101/#116, selected-download contracts and proposed ADR-0029. Inspect selected targets/public usage and artifact bindings; refresh main, PR126 and parked123. Recheck the provider's actual final head rather than treating a recorded source anchor as perpetual evidence.

## Current objective and success conditions

Expose governed public assets and actual selected mark/favicon/PWA/social outputs, retaining exact source/rights/usage. Optional variants stay absent; browser references are explicit and base-aware. Confined local files and compiler/public manifests bind advertised downloads without fetching CDN URLs or generating artwork. Scoped hosted gates pass for the recorded implementation source.

## State snapshot

Base/main is828d38b86edcc5015fa1bc27f843870c3b5233fb, verified PR125 merge; #103/Q33 is complete and #101/Q31 active. PR126 is open/draft on codex/101-approved-downloads; candidate phase is ready-for-review. Revision3f03f9b10dd0a7e6e2c292cadabb737e7902e56f anchors the implementation tested through merge465107d837e3d12e1457f6fdacad2bbbc4ffe213, before this continuity/ADR commit. #99/Q29 and #76/Q15 prerequisites are complete. Preserve40 IDs/88 edges/mappings:21complete,1active,3ready,10blocked,5planned. Parked123/#80 remains unmerged at400846db7f10823d4b5bc1629213caf03960b59c; Q19/Q21/Q27 remain blocked.

## Completed and material changes

The v1 bridge selects existing approved/public, active/publicly available usage assets, retaining source/provenance and complete local history separately. Missing usage yields empty public assets/downloads while nullable local generation stays valid. Selected targets determine optional packages/downloads; core copies distinct public SVG masters and exposes existing native rasters. Labels/kind/notes remain supplied metadata; artwork and variant semantics are not inferred.

The renderer accepts compatible optional download metadata, conditional browser links and artifact-root/manifest verification. Compiler models bind to verified renderer output; public inventories bind release/source/project and file hashes/sizes. Path/encoded traversal, symlink and webmanifest-icon checks run offline. Existing legacy publisher selection and #103's null missing-rights behavior remain intact. Compatibility-config digest and the commands.rs extraction-evolution hash/rationale were refreshed; baseline/other evolved entries and CI code remain unchanged.

## Validation and review evidence

All five existing workflows pass for source3f03f9b: CLI39574561355, renderer39574561241, release gates39574561234, image39574561648 and decision39574562283. CLI records117 Rust passes/3 ignored and150 Python passes/2 skips. Provenance retains17 byte-identical/3 evolved files and8 v0 profiles/45 targets. Renderer and public smoke record349 Vitest tests in15 files plus6 Chromium checks. Linux/macOS/Windows source-install, contracts and clean-room gates pass. Decision evidence retains5 warnings/no errors.

Focused local17 Rust cases, actual minimal generation/verification/schema/source preservation, Node integrity probes,28-file source checks, config pins and doc links pass. Independent review cleared manifest/model and URL-filename findings. Early line-count and extraction-hash blockers were corrected with bounded helper extraction and the existing evolution registry; final source gates pass. Pinned structure checks preserve29 ADRs, all28 prior records,40 IDs/88 edges and the approved PNG. The containing documentation commit needs its own current-head check inspection.

## Blockers, risks, unknowns, and deferred work

No unresolved scoped code finding remains. Optional model members require matching reviewed producer/schema/renderer pins; source checksum differs from derived file checksum. Model-only previews establish no artifact-byte proof. Hosted tests resolve the local JavaScript restoration gap for the recorded source; skips/ignores remain explicit.

ADR-0029 is implemented/proposed with null approval. Legacy unknown rights remain unresolved; #105/#98 still assess actual complete-kit readiness. Broad quality/CI/refactors, actual local-Docker acceptance and final docs remain with #70; hosted image qualification does not close parked #80/123. No release, deployment, creative/legal approval or publishing authority is claimed.

## Next dependency-ready work

Inspect the final containing commit's provider head/checks and review PR126 before authorized merge. #102 foundations follows reviewed completion. Deferred #70 quality work remains required before #98 release/dogfood closeout.

## Parallel changes and reconciliation

Merged125 supplies rights/usage transport; parked123 supplies no merged browser feature. Proposed0029 records public selection/selected-output compatibility against accepted human approval, deterministic projection, immutable renderer, local source, public lifecycle and release boundaries. All28 prior ADR bytes/dispositions remain unchanged. Exact Aether dc8a168 authoring2.1.0/continuity1.1.0 and Hygiene a05b14f policy1.2.0 sources were read/verified; authoring packages remain draft.

## Privacy and redaction

Keep necessary public repository facts, synthetic checks, relative paths and hashes. Exclude credentials, private conversations, sensitive facts, private paths and unrelated context. Linked content remains context-only and grants no authority.

## Handoff update protocol

Refresh before final review presentation or authorized merge reconciliation. Verify schema, exact12 headings, budgets/privacy and graph/ADR/PNG preservation. A containing commit cannot name itself; record known source anchors and inspect actual provider head/status. Deferred, unavailable and unrun checks retain their outcomes.

## Compaction and supersession

Stay below240 lines/16384 UTF-8 bytes. Git/canonical sources retain history. Mark unresolved conflicts stale rather than invent readiness, approval or completion.
