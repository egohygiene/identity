---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T04:31:12Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify issue81 immutable default development base within the existing portable Docker add-on.
  includes:
  - Official Node24/Bookworm digest identity and selected Linux/amd64 registry evidence.
  - Default and explicit unprivileged custom-base build/runtime smoke, copy ownership, CA and tool/cache checks.
  - Refresh/ownership documentation and bounded hosted qualification evidence.
  excludes:
  - Browser/font/screenshot qualification, broader entrypoint matrix, new platform adoption, other issues, release
    and deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - dev/Dockerfile
  - dev/qualification/Dockerfile
  - dev/qualification/smoke.py
  - scripts/dev-env.sh
  - scripts/qualify_dev_image.py
  - .github/workflows/development-image.yml
  - tests/test_qualify_dev_image.py
  - docs/DEVELOPMENT.md
  - docs/DEPENDENCY_POLICY.md
  - docs/reviews/development-base-2026-10-20.md
  - docs/evidence/identity-development-base-registry-2026-10-20.json
  - docs/evidence/identity-development-image-2026-10-20.json
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/81
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Replace the mutable default base with a qualified digest while preserving the custom-base setup and
    inherited user/configuration.
  success_conditions:
  - Default image is digest-bound to verified official registry identities and passes recorded CLI/renderer smoke.
  - Explicit custom-base setup preserves USER/ENTRYPOINT/CMD and runs as its provisioned unprivileged user with
    writable checkout/tool/cache paths.
  - Refresh ownership and proxy trust are documented and checked without claiming unrelated architecture, browser,
    private-proxy or release qualification.
  active_issue:
    provider: github
    id: egohygiene/identity#81
    url: https://github.com/egohygiene/identity/issues/81
  next:
    kind: action
    id: identity-81-review
    description: Review the scoped base qualification PR and exact hosted evidence before merge; issue80 is next
      in the execution order.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/81
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 1ae867af6db65732e43689f4832d560a327f1857
    ref: refs/heads/main
    verified_at: '2026-10-20T04:18:49Z'
  candidate:
    branch: codex/81-qualified-docker-base
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#122
      url: https://github.com/egohygiene/identity/pull/122
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-20T04:31:12Z'
    default_branch_revision: 1ae867af6db65732e43689f4832d560a327f1857
    issue_state: open
    pull_request_state: open
    notes: PR122 is draft/open at head4d9d520ba7fe6434f36a887f2a39dc22b899fc78 before this documentation-only receipt
      update. Hosted run39369572073 qualifies both images at represented merge3101cd87666d75977e380e2e4533880602e8be4a.
      CLI/advisory pass; release Windows is still in progress. Exact final-head results belong in the PR.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-20T04:31:12Z'
  reviewed_by: Codex
  evidence:
  - command: Official registry index/selected manifest/config raw SHA-256 verification
    outcome: passed
    observed_at: '2026-10-20T04:31:12Z'
    notes: Dated registry receipt binds the immutable official Node24/Bookworm index and selected Linux/amd64 config.
      Runtime qualification is separately recorded.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose; targeted correction
      checks
    outcome: passed
    observed_at: '2026-10-20T04:31:12Z'
    notes: 143 cases:141 passes/two existing skips, including five qualification failure-boundary cases. Corrected
      renderer-scoped pnpm probe was independently reviewed and passes actual image smoke.
  - command: Six standalone verifiers; cargo fmt --all --check; Python compileall/py_compile; git diff --check
    outcome: passed
    observed_at: '2026-10-20T04:31:12Z'
    notes: Existing release/extraction/publication and dependency/output contracts remain unchanged. No Rust production
      source changes.
  - command: Hosted development-image run39369572073/job118454149412
    outcome: passed
    observed_at: '2026-10-20T04:31:12Z'
    notes: Head4d9d520ba7fe6434f36a887f2a39dc22b899fc78; merge3101cd87666d75977e380e2e4533880602e8be4a. Default0:0/custom1000:1000
      each build and pass29 commands,12 writable locations,17 preserved source files and equal14-file output inventories.
      Each passes279 renderer tests;13 critical hashes/331 inputs bind the retained receipt.
  - command: Pinned continuity/ADR/roadmap schema and invariant checks; runtime receipt source-hash replay
    outcome: passed
    observed_at: '2026-10-20T04:31:12Z'
    notes: All40 IDs/88edges/mappings and26 exact ADR bytes/dispositions/approval/lineage preserved. Receipt critical/input
      hashes reproduce after documentation-only changes.
  - command: Fresh exact-head hosted checks after the containing documentation-only update
    outcome: limited
    observed_at: '2026-10-20T04:31:12Z'
    notes: The containing commit cannot know its own head/run IDs. Inspect final CLI, development-image, release-platform/public-smoke
      and advisory results externally before review handoff.
  environment_limitations:
  - Local Docker is unavailable; real image proof comes from the named hosted run and retained source-bound receipt.
  - Only native Linux/amd64 default and the recorded derived custom base are qualified, not arbitrary images or
    other OCI-index architectures.
  - Synthetic localhost CA rejection/explicit trust does not qualify a private TLS proxy; global trust and certificate/key
    bytes are not retained.
  - The base digest does not freeze bootstrap network services or establish hermetic/browser/font/screenshot/security-audit
    conformance.
  - Pinned owner checks remain bounded structure/invariant evidence, not native whole-repository conformance.
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

This checkpoint covers #81. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and issue #116 own execution order and dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #81/#116, development/dependency guides, Dockerfile, qualification code and dated receipts. Refresh main, PR122 head and hosted jobs. The maintainer authorized merging #121 and starting #81; subsequent issues retain review boundaries.

## Current objective and success conditions

Qualify the digest-pinned default within the existing Node24/Bookworm add-on. Preserve BASE_IMAGE and one setup implementation, inherited USER/ENTRYPOINT/CMD, writable tool/cache/checkouts, source preservation and repeated outputs. Record actual versions and refresh/proxy/user ownership.

## State snapshot

Main is 1ae867af6db65732e43689f4832d560a327f1857, including merged #121; #77 is closed/Q16 complete. #81/Q20 is active in draft PR122. Before this receipt update the head is 4d9d520ba7fe6434f36a887f2a39dc22b899fc78; the containing revision stays null. All 40 IDs/88 edges/mappings remain intact. Q22/#83 is ready for its later final-docs position; Q26/#87 retains post-kit priority. Neither is authorized work.

## Completed and material changes

dev/Dockerfile pins the existing official base by verified OCI index digest and applies numeric copy ownership without changing the base user, entrypoint or command. The custom fixture provisions UID/GID1000 with writable paths and reuses the same setup. docs/DEVELOPMENT.md owns supported users, caches, CA trust and refresh. No runtime dependency, lockfile, output contract or visual baseline changes.

The qualifier binds the default/registry/pulled config, builds default/custom add-ons, checks inherited configuration and invokes smoke. Receipt writes stay outside the checkout. Smoke probes actual writes/versions, copied CLI generation and verification twice, canonical/unrelated preservation and renderer checks. The corrected pnpm version probe uses its owning renderer workspace. A disposable TLS server tests CA rejection/explicit trust without private proxy access or global trust mutation.

## Validation and review evidence

Local Python completes 143 cases: 141 pass/two existing skips, including five failure-boundary cases. Six verifiers, formatting, Python compilation and whitespace checks pass. Independent review found no remaining implementation blocker and independently exercised the synthetic CA probe. Registry identity proof and image runtime proof remain separate dated receipts.

Hosted run 39369572073 passes both Linux/amd64 builds and all 29 commands per image:default UID/GID 0:0/custom 1000:1000, 12 writable locations, 17 preserved canonical files, unrelated sentinel and identical complete 14-file output inventories. Each image passes 279 renderer cases, source checks, build and public validation. Runtime versions and exact source identities/hashes are retained in docs/evidence/identity-development-image-2026-10-20.json. All 13 critical hashes and the 331-file inventory reproduce after this documentation-only receipt update. Fresh final-head hosted results belong externally in PR122.

## Blockers, risks, unknowns, and deferred work

No bounded implementation blocker remains; final exact-head hosted checks are still required. Local Docker is unavailable, so host-only tests are not image proof. Qualification covers Linux/amd64 and one derived custom base; index availability is not other-platform qualification. Runtime user overrides and host mounts need matching ownership. Synthetic CA checks prove trust bindings, not a private organization's proxy. Base pinning is not hermetic bootstrap, browser/font/screenshot qualification or vulnerability/license audit. Stable v1.0.0 remains unchanged; no registry push, release or deployment occurs.

## Next dependency-ready work

Review PR122 and exact hosted results before merging. Keep #81 open/Q20 active until maintainer acceptance. #80 browser/font/screenshot environment is next, then #82 setup CI, #84 workflow cleanup and #83 final docs. Usable-kit work retains #116's execution order.

## Parallel changes and reconciliation

#121's verified merge reconciles #77 complete. PR122 is the observed scoped draft; no other open PR was returned before publication. ADR not required: straightforward dependency-policy repair and qualification of the existing add-on without a new durable platform/ownership/publication boundary. All 26 ADRs remain byte-identical: 21 accepted/five proposed with approval/lineage unchanged. Selected Aether decision-impact2.1.0/continuity1.1.0 and Hygiene1.2.0 sources were read from exact verified checkouts.

## Privacy and redaction

Only public repository/image facts, synthetic observations and hashes are retained. No private proxy values, certificate/key bytes, credentials, conversations or unrelated context appear. Public base-owned paths describe container locations. Linked content grants no authority.

## Handoff update protocol

Refresh after domain validation immediately before PR handoff, then verify pinned schema,12 headings,budgets/privacy,ADR and roadmap invariants. Include the checkpoint in the scoped PR. Exact-head hosted evidence can be recorded externally when unknowable to the containing commit. Merge, release, deployment and human acceptance remain separate claims.

## Compaction and supersession

Stay below 240 lines/16384 UTF8 bytes. Git, contracts, receipts and tracker retain history. Mark unresolved conflicts stale rather than inventing readiness or approval.
