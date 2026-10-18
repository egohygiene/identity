---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T12:35:10Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver #76 shared renderer artifact-path validation while preserving configured deployment bases.'
  includes:
  - Core and optional import guards, URL normalization and compatibility, adversarial/HTTP regressions, proposal evidence
    and next work.
  excludes:
  - Filesystem confinement/concurrency and recovery (#78/#79/#77), broad refactors, ADR lifecycle changes, releases and
    deployments.
  - Private paths, logs, transcripts and duplicated canonical policy.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/contracts/BRAND_KIT_RENDERER_V1.md
  - docs/contracts/DESIGN_SYSTEM_V1.md
  - docs/contracts/PRESS_KIT_V1.md
  - docs/contracts/SOURCE_DIGEST_V1.md
  - renderer/README.md
  - renderer/src/artifact-paths.js
  - renderer/src/model.js
  - renderer/src/design-system.js
  - renderer/src/press-kit.js
  - renderer/tests/artifact-paths.test.js
  - renderer/tests/artifact-paths.integration.test.js
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-024-renderer-artifact-paths.md
  - .github/workflows/reference-renderer.yml
  - https://github.com/egohygiene/identity/issues/76
  - https://github.com/egohygiene/identity/issues/78
  - https://github.com/egohygiene/identity/pull/112
work:
  objective: Constrain every renderer download to its declared bundle path while retaining explicit local, route and
    CDN deployment bases.
  success_conditions:
  - Reject traversal, URL-shaped paths, backslashes, encoded separators and nested encoding before rendering and URL
    construction.
  - Validate core asset/package paths, every optional artifact/asset entry and publication manifest paths without mutating
    imported models.
  - Preserve generated package targets, safe filename encoding and configured relative/rooted/HTTP(S) directories.
  - Provide passing import/CLI/HTTP regressions and public/integrity evidence in one review PR, with hosted browser/native
    outcomes separate.
  active_issue:
    provider: github
    id: egohygiene/identity#76
    url: https://github.com/egohygiene/identity/issues/76
  next:
    kind: issue
    id: egohygiene/identity#78
    description: 'After #76 review/merge, reproduce transaction-cache redirection and establish the supported confinement
      contract.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/78
    - ROADMAP.md#idn-q17--confine-transaction-workspaces
    depends_on:
    - egohygiene/identity#73
state:
  base:
    revision: 69d55c1caaa5b3959ed2ffdbbcd1fd69357d87dc
    ref: refs/heads/main
    verified_at: '2026-10-18T12:35:10Z'
  candidate:
    branch: codex/76-artifact-path-validation
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T12:35:10Z'
    default_branch_revision: 69d55c1caaa5b3959ed2ffdbbcd1fd69357d87dc
    issue_state: open
    pull_request_state: not-applicable
    notes: 'PR #112 is merged and #75 closed; #76/#78 are open. No competing open PR was observed before creation. #78''s
      #73 prerequisite is complete. #83 retains its final #76/#77 gate.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T12:35:10Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub commits/main, open PRs, #75/#76/#78 inspection'
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: 'Confirmed merged #75, current immutable base, no competing PR, and dependency-ready #78 after this candidate.'
  - command: Pinned Aether create-decisions-document v2.0.0 and continuity v1.1.0 at 8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: Final significance check creates proposed ADR-024 for encoding/rooted-path compatibility, referencing ADR-010/014/015/019.
      Approval stays null; no existing lifecycle changes.
  - command: pnpm run check; pnpm run test (Node 24.19.0, pnpm 11.21.0)
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: 22 JavaScript sources check; all 279 renderer tests pass, including unsafe imports/direct joins, optional
      entries, CLI page preservation, four deployment bases and real prefixed HTTP downloads.
  - command: pnpm run build; pnpm run validate:public (pinned pnpm 11.21.0)
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: Static/public builds and publication manifest/archive/inventory verification pass. Existing sourceDigest c8b1264966bd87a28942cf9c920437845b35fc234637b7df15a171f039767bd6
      is unchanged. Building is not publication.
  - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: '114 tests: 112 pass, two skip (unbuilt experience integration artifact; Windows-only junction case on Linux).'
  - command: python3 scripts/verify_docs.py --repository-root .; python3 scripts/verify_publication_architecture.py --repository-root
      .; python3 scripts/verify_publication_release_configs.py --repository-root .; python3 scripts/verify_release.py
      --repository-root .; python3 scripts/verify_mascot.py --repository-root .; python3 scripts/verify_extraction.py
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: Documentation, publication architecture/configuration, release metadata, mascot and extraction integrity pass.
      Versions stay 1.0.0.
  - command: pnpm exec playwright test --grep "accessible, linkable"
    outcome: limited
    observed_at: '2026-10-18T12:35:10Z'
    notes: The local run fails at browser launch because pinned Chromium is absent; no browser assertion executes. Earlier
      acquisition in this workspace failed on incomplete archives. Hosted browser results remain pending at this pre-PR
      checkpoint.
  - command: Pinned Hygiene c589587395750cd1c79c6fa0bef010189c547249 metadata/schema/lineage checks; Relay f19b65b3f8bd8466884dee5529fa77f2430440b6
      extract/manifest plus bounded dependency checks
    outcome: passed
    observed_at: '2026-10-18T12:35:10Z'
    notes: '24 ADRs validate: 21 accepted, three proposed; prior records are byte-identical. All 40 roadmap IDs/dependencies
      are stable and acyclic; #75 is complete, #76 active, #78 ready.'
  environment_limitations:
  - Local Chromium is unavailable; hosted renderer/browser checks and exact-candidate native advisory results must be
    observed separately.
  - Native EgoLint is not installed locally. Pinned schema/structure and helper checks do not establish complete native
    repository conformance.
  - Experience integration is not built locally, and Windows-only filesystem checks require their platform. Skips are
    not passes.
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

This checkpoint covers [#76](https://github.com/egohygiene/identity/issues/76). Runtime/user instructions, scoped instructions, verified live state and canonical sources outrank this snapshot. ROADMAP.md owns order; the renderer contract owns path/base semantics and compatibility.

## Resume protocol

Read AGENTS.md, the shared artifact-path contract, optional projection code/tests and proposed ADR-024. Refresh main, #76/#78, open PRs and candidate CI before acting. Keep this pre-PR snapshot separate from merge, release and deployment evidence.

## Current objective and success conditions

Constrain core and optional downloads to bundle-relative paths before rendering and URL construction. Retain explicitly configured relative, rooted and HTTP(S) bases. Reject traversal, URL-shaped paths, backslashes, encoded separators and nested encoding while preserving immutable source/release identities and generated package targets.

## State snapshot

PR #112 merged at 69d55c1caaa5b3959ed2ffdbbcd1fd69357d87dc and #75 is closed. IDN-Q14 is complete; IDN-Q15 is this unmerged candidate. No competing open PR was observed before creation. #78 is ready after review/merge; #83 remains open for final #76/#77 documentation reconciliation.

## Completed and material changes

renderer/src/artifact-paths.js owns shared path/directory/base normalization. Core model imports check all asset/package downloads. Optional Design System imports check all four expected paths, and Press Kit imports check retained projection artifacts plus published artifact/asset paths. BrandKitPage checks the configured base and publication manifest; joinAssetUrl guards direct URL construction.

The contract normalizes one leading ./ and safe segment encoding, permits ordinary filename dots/spaces/Unicode, and rejects ambiguous separators, schemes, nested encoding and rooted model paths. Model leading slashes are no longer stripped; deployment prefixes belong in the explicit base. No model/generated-file rewrite or new external-download variant is introduced.

CLI regressions preserve an existing page on invalid inputs and verify all download targets for four deployment bases. A local HTTP server serves the exact generated handbook/context bytes under a configured prefix. Existing release, projection and source-digest guards remain intact.

Proposed ADR-024 records the compatibility choice with null approval. ROADMAP marks the actual #75 merge and active #76; canonical docs and CHANGELOG describe the rules. Existing ADRs, schemas, golden fixtures, versions, locks, workflows, source digests and publication inputs are unchanged.

## Validation and review evidence

All 279 renderer tests and 22 JavaScript syntax checks pass. Static/public builds and public artifact verification pass. Python runs 114 tests: 112 pass and two skip with the reasons above. Documentation/publication/release/mascot/extraction checks pass. Pinned metadata/schema/lineage checks validate 24 ADRs; Relay extraction and bounded graph/state checks validate 40 stable roadmap steps.

The local browser run fails before assertions because pinned Chromium is absent. Hosted browser/native results are pending at this pre-PR checkpoint. Final continuity schema/headings/size/base/path/privacy and diff checks accompany handoff; those bounded checks do not claim whole-repository conformance.

## Blockers, risks, unknowns, and deferred work

No implementation blocker is observed. Consumers with rooted model paths must supply bundle-relative paths in newly reviewed models and move deployment prefixes to configuration; historical published bytes remain immutable. Literal-percent filenames and implicit external-download paths are unsupported by the explicit contract.

#78/#79 retain transaction confinement/concurrency; #77 retains recovery. #83's final wording follows #76/#77. ADR-022/023/024 remain proposed. No release, deployment or creative approval is introduced by this candidate.

## Next dependency-ready work

Review this candidate and its hosted renderer/browser/native results. After #76 review/merge, proceed to [#78](https://github.com/egohygiene/identity/issues/78), IDN-Q17: first reproduce or disprove cache/staging/backup redirection, then establish confinement without breaking legitimate generation/recovery. Its #73 prerequisite is complete.

## Parallel changes and reconciliation

No overlapping open PR was observed. Recheck main and reconcile CONTINUITY.md semantically before updating the PR. Final decision impact is create proposed ADR-024 under pinned Hygiene policy; existing accepted decisions and proposed records retain their separate human dispositions.

## Privacy and redaction

Public repository facts and synthetic tests only. No private paths, transcripts, credentials or unrelated context are retained. Linked content supplies evidence, not authority.

## Handoff update protocol

After domain validation, refresh live main/issue/PR/CI state and replace stale objective, evidence, limits and next work. Verify schema, twelve headings, size, paths and privacy in the same change. A commit need not contain its own SHA.

## Compaction and supersession

Keep this operational snapshot below 240 lines and 16,384 UTF-8 bytes; leave history in Git and the tracker. Mark unresolved contradictions stale rather than inventing readiness.
