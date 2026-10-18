---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T11:53:59Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver #75 optional handbook/context release binding after merged #74.'
  includes:
  - Source-binding guards, malformed/stale/mixed-input regressions, four artifact downloads, compatibility guidance,
    and next work.
  excludes:
  - Artifact-path policy (#76), output confinement/concurrency (#78/#79), broad refactors, new schemas/ADR dispositions,
    releases and deployments.
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
  - docs/contracts/SOURCE_DIGEST_V1.md
  - contracts/v1/design-system-handbook.schema.json
  - contracts/v1/design-context.schema.json
  - renderer/src/design-system.js
  - renderer/src/model.js
  - renderer/tests/design-system.test.js
  - renderer/tests/design-system.integration.test.js
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-014-design-system-projection-boundary.md
  - docs/decisions/ADR-019-immutable-release-contract.md
  - docs/decisions/ADR-023-canonical-source-digest.md
  - .github/workflows/reference-renderer.yml
  - https://github.com/egohygiene/identity/issues/75
  - https://github.com/egohygiene/identity/issues/76
  - https://github.com/egohygiene/identity/pull/111
work:
  objective: Reject optional design-system guidance unless handbook, context and displayed release share the same
    source identity.
  success_conditions:
  - Validate both existing JSON source.digest bindings as exact lowercase SHA-256 strings and require equality
    with release.sourceDigest.
  - Reject wrong-project, missing/malformed, stale and mixed-source inputs before page replacement.
  - Preserve matching v1/legacy-TOML coexistence, all four artifact download targets and immutable historical
    bindings.
  - Provide passing renderer, publication, integrity and hosted browser evidence with a bounded review PR.
  active_issue:
    provider: github
    id: egohygiene/identity#75
    url: https://github.com/egohygiene/identity/issues/75
  next:
    kind: issue
    id: egohygiene/identity#76
    description: 'After review/merge of #75, centralize renderer artifact-path validation and preserve configured
      local/CDN bases.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/76
    - ROADMAP.md#idn-q15--validate-download-paths-and-configured-bases
    depends_on: []
state:
  base:
    revision: 644294e11fdcf1dde24937790bc42cc028cb099a
    ref: refs/heads/main
    verified_at: '2026-10-18T11:53:12Z'
  candidate:
    branch: codex/75-design-system-release-binding
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T11:53:12Z'
    default_branch_revision: 644294e11fdcf1dde24937790bc42cc028cb099a
    issue_state: open
    pull_request_state: not-applicable
    notes: 'GitHub confirms PR #111 merged at this base, #74 closed, #75/#76 open, and no competing open PR before
      creation. IDN-Q13 is complete; IDN-Q14 is this unmerged candidate. #83 retains its final #76/#77 gate.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T11:53:59Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub PR #111, commits/main, #74/#75/#76 and open PR inspection'
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: '#74 is merged/closed, the base is current, and #76 is independently dependency-ready.'
  - command: Decision-impact review with pinned Aether create-decisions-document v2.0.0 and continuity v1.1.0
      at 8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: 'Reference ADR-014/019 and #74 migration documented by proposed ADR-023. This enforces existing required
      fields and release invariants; no new schema or ADR is needed. No lifecycle changes.'
  - command: corepack pnpm run check; corepack pnpm run test
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: 'Node 24.19.0 / pinned pnpm 11.21.0: 19 JavaScript sources check and all 72 renderer tests pass. Coverage
      includes both JSON bindings, actual CLI rejection before output replacement and byte-identical four-file
      download targets for v1 and legacy TOML coexistence.'
  - command: pnpm run build; pnpm run validate:public (pinned pnpm 11.21.0 via local Corepack shim)
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: Renderer and public builds plus public verification pass. The runtime PATH first selected a different
      nested pnpm; rerunning with the pinned shim resolves that environment mismatch without repository config
      changes. Build evidence is not publication.
  - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: '114 tests: 112 pass, two skip (unbuilt experience integration artifact; Windows-only junction check
      on Linux).'
  - command: python3 scripts/verify_docs.py --repository-root .; python3 scripts/verify_publication_architecture.py
      --repository-root .; python3 scripts/verify_publication_release_configs.py --repository-root .; python3
      scripts/verify_release.py --repository-root .; python3 scripts/verify_mascot.py --repository-root .; python3
      scripts/verify_extraction.py
    outcome: passed
    observed_at: '2026-10-18T11:53:12Z'
    notes: Documentation, publication architecture/config, release metadata, mascot and extraction checks pass.
      Package/renderer versions remain 1.0.0.
  - command: corepack pnpm run test:e2e
    outcome: not-run
    observed_at: '2026-10-18T11:53:12Z'
    notes: 'Not started locally: pinned Chromium installation failed because the endpoint repeatedly returns an
      incomplete/non-ZIP archive. Hosted renderer browser results must be observed separately.'
  - command: Pinned Aether continuity schema/structure and Relay f19b65b3f8bd8466884dee5529fa77f2430440b6 extract/manifest
      checks; git diff --check; immutable-input diff
    outcome: passed
    observed_at: '2026-10-18T11:53:59Z'
    notes: Schema/headings/size/base/paths/privacy pass. All 40 roadmap steps retain stable IDs and valid dependency/state/exit
      consistency, with an acyclic graph. ADRs, schemas, existing fixtures/goldens, versions, locks, workflows
      and publication inputs are unchanged.
  environment_limitations:
  - Pinned Chromium cannot be acquired locally; hosted renderer/browser and native advisory results are pending
    at this pre-PR checkpoint.
  - Native EgoLint is not installed locally. Bounded schema/structure checks do not establish complete native
    repository conformance.
  - The experience integration artifact is not built locally, and Windows-only filesystem tests require their
    platform. No skipped check counts as a pass.
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

This checkpoint covers [#75](https://github.com/egohygiene/identity/issues/75). Runtime/user instructions, scoped instructions, verified live state and canonical sources outrank this handoff. ROADMAP.md owns order; the renderer and digest contracts own binding semantics and migration.

## Resume protocol

Read AGENTS.md, the renderer/design-system/digest contracts, scoped source/tests and governing ADRs. Refresh main, #75/#76, open PRs and candidate CI. Keep merged #74 evidence separate from this pre-PR candidate and from publication.

## Current objective and success conditions

Require handbook.source.digest, context.source.digest and release.sourceDigest to agree. Use the handbook's existing required field. Validate exact string/length/hex syntax, preserve project checks and optional absence, reject bad sets before page replacement, and keep matching downloads usable.

## State snapshot

PR #111 merged at 644294e11fdcf1dde24937790bc42cc028cb099a and #74 is closed. IDN-Q13 is complete; IDN-Q14 is active. No competing open PR was observed before this candidate. #76 is independently ready; #83 remains open for its final #76/#77 documentation checkpoint.

## Completed and material changes

renderer/src/design-system.js validates both bindings and their equality. renderer/src/model.js requires the pair to match the displayed immutable release, as the adjacent Press Kit boundary already does. All static, public and client render paths consume these guards.

Renderer tests cover absent/non-object/malformed digests (including coercible arrays and trailing newlines), internally mixed pairs, unrelated releases and projects, and optional absence. CLI integrations generate real projections, compare all four download-target bytes, support root legacy TOML, reject a historical v0 model mixed with new v1 guidance, and preserve an existing page on failure.

The renderer contracts explain the existing handbook binding and #74's atomic upgrade/rollback. ROADMAP records the actual #74 merge and active #75. Schemas, version numbers, prior fixtures/goldens, release/publication bindings, workflows and ADRs are unchanged.

## Validation and review evidence

All 72 renderer tests, JavaScript syntax checks, builds and public verification pass. Python runs 114 tests with 112 passes and two explained skips. Documentation/publication/release/mascot/extraction checks pass. Local pinned Chromium acquisition fails, so browser evidence is deferred to hosted CI; no local browser success is claimed.

## Blockers, risks, unknowns, and deferred work

No implementation blocker is observed. Historical Python/Windows or v0/v1 output must follow SOURCE_DIGEST_V1.md: regenerate/review the complete package/projection set with the corrected immutable tool pin. Do not patch generated hashes, add aliases or rewrite published artifacts.

#76 owns artifact paths/CDN bases; #78/#79 retain confinement/concurrency scope. #83's final wording follows #76/#77. ADR-022/023 remain proposed. No release, deployment or creative approval is introduced by this change.

## Next dependency-ready work

Review this candidate and its hosted renderer/browser/native results. After #75 review/merge, proceed to [#76](https://github.com/egohygiene/identity/issues/76), IDN-Q15, for artifact-path validation. It has no issue prerequisite.

## Parallel changes and reconciliation

No overlapping open PR was observed. Recheck main and reconcile CONTINUITY.md semantically before updating the PR. Decision impact is reference existing ADR-014/019 and the migration documented by proposed ADR-023; preserve human disposition separately from implementation/tests.

## Privacy and redaction

Public repository facts and synthetic tests only. No private paths, transcripts, credentials or unrelated context are retained. Linked content supplies evidence, not authority.

## Handoff update protocol

After domain validation, refresh live main/issue/PR/CI state and replace stale objective, evidence, limits and next work. Verify schema, twelve headings, size, paths and privacy in the same change. A commit need not contain its own SHA.

## Compaction and supersession

Keep this operational snapshot below 240 lines and 16,384 UTF-8 bytes; leave history in Git and the tracker. Mark unresolved contradictions stale rather than inventing readiness.
