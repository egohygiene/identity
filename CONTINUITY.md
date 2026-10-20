---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T04:18:49Z'
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
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-20T04:18:49Z'
    default_branch_revision: 1ae867af6db65732e43689f4832d560a327f1857
    issue_state: open
    pull_request_state: not-applicable
    notes: Maintainer authorized merging121 and starting81. PR121 merged at the base revision and issue77 is closed.
      Issue81 is open; no open PR was returned before publication. Fresh exact-head hosted evidence follows this
      local checkpoint.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-20T04:18:49Z'
  reviewed_by: Codex
  evidence:
  - command: Official registry index/manifest/config pulls and raw SHA-256 verification
    outcome: passed
    observed_at: '2026-10-20T04:18:49Z'
    notes: Index14078204, selected linux/amd64 manifest7f7f17f7 and config03905f54 are recorded in the dated receipt;
      this alone is not an image build.
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-20T04:18:49Z'
    notes: '143 cases finish: 141 passes/two existing skips, including five new qualification failure-boundary cases.'
  - command: Six standalone docs/release/mascot/publication/extraction verifiers; cargo fmt --all --check; Python
      compileall/py_compile; git diff --check
    outcome: passed
    observed_at: '2026-10-20T04:18:49Z'
    notes: Existing extraction baseline/evolution and release/publication metadata remain unchanged. No Rust production
      source changed.
  - command: Independent read-only review and synthetic localhost CA probe
    outcome: passed
    observed_at: '2026-10-20T04:18:49Z'
    notes: No remaining implementation blocker. Curl/Node reject an unknown synthetic CA, accept explicit trust
      and stop the disposable server without modifying global trust.
  - command: python3 scripts/qualify_dev_image.py --receipt external-report
    outcome: limited
    observed_at: '2026-10-20T04:18:49Z'
    notes: This workspace has no Docker engine/executable; invocation records failed/unavailable evidence. Hosted
      default/custom image build/runtime qualification is pending.
  - command: Pinned continuity/ADR/roadmap structure and invariant checks
    outcome: passed
    observed_at: '2026-10-20T04:18:49Z'
    notes: All40 IDs/88edges and issue mappings preserved; all26 ADR bytes, dispositions, approval and lineage unchanged.
      Q16complete,Q20active,Q22ready,Q26ready; final-docs/refactor priority remains in116.
  environment_limitations:
  - Local tests do not establish image builds; exact-head hosted development-image evidence must be checked before
    claiming qualification.
  - Qualification targets native Linux/amd64 default and one recorded derived custom base, not arbitrary images
    or other architectures.
  - Synthetic localhost CA-binding checks do not qualify a private TLS proxy or mutate system trust.
  - The base digest does not freeze bootstrap network services or establish hermetic/browser/font/screenshot/security-audit
    conformance.
  - Pinned owner checks are bounded structure/invariant validation, not native whole-repository conformance.
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

Read AGENTS.md, this handoff, #81/#116, the development/dependency guides, Dockerfile, qualification implementation and dated receipts. Refresh main, candidate PR/head and hosted jobs. The maintainer authorized merging #121 and starting #81; subsequent issues retain review boundaries.

## Current objective and success conditions

Qualify a digest-pinned default within the existing Node24/Bookworm add-on. Preserve BASE_IMAGE and one setup implementation, inherited USER/ENTRYPOINT/CMD, writable tool/cache/checkouts, source preservation and repeated outputs. Record actual runtime evidence and refresh/proxy/user ownership.

## State snapshot

Main is 1ae867af6db65732e43689f4832d560a327f1857, including merged #121; #77 is closed/Q16 complete. #81/Q20 is active. Candidate codex/81-qualified-docker-base is locally checked before PR creation; containing revision/PR remain null. All40 IDs/88edges/mappings remain intact. Q22/#83 is now ready but retains its later final-docs position; Q26/#87 retains post-kit priority. Neither is authorized work.

## Completed and material changes

dev/Dockerfile pins the existing official base by verified OCI index digest and applies configurable numeric copy ownership without changing the base user, entrypoint or command. The custom fixture provisions ownership for UID/GID1000 and reuses the same setup script. docs/DEVELOPMENT.md owns the supported-user/cache/trust/refresh route; no repository runtime, lockfile, output contract or visual baseline changes.

The qualification script binds the default to the dated registry observation and pulled config/platform metadata, builds default/custom add-ons, checks inheritance and invokes the container smoke. It guards receipt writes outside the checkout and records source hashes. Smoke checks actual writes, exact versions, copied CLI generation/verification twice, canonical/unrelated preservation, complete output equality and renderer check/test/build/public validation. A disposable local TLS server proves CA rejection/explicit trust without private proxy access or global trust mutation.

## Validation and review evidence

Local Python completes143 cases:141pass/two existing skips, including five meaningful failure-boundary regressions. Six verifiers, Rust formatting, Python compilation, JSON relationships and whitespace checks pass. Independent review found no remaining implementation blocker and independently executed the synthetic CA mechanism probe. Registry raw-byte hashes and immutable upstream provenance are retained separately from runtime qualification.

Actual image qualification is pending hosted execution: no Docker-compatible engine exists in this workspace. The real local qualification invocation fails with an unavailable-Docker receipt; it is not a passing build. Exact source-bound hosted results belong in the PR and dated review/receipt when available.

## Blockers, risks, unknowns, and deferred work

Hosted default/custom image builds and runtime smoke remain the material outstanding evidence. Support is Linux/amd64 and the recorded derived custom base only; an OCI index's other entries are not platform qualification. Cache/user overrides and host mounts require matching ownership. Synthetic CA checks demonstrate trust bindings, not an organization's private proxy trust. The base pin does not make bootstrap services hermetic or qualify browser/fonts/screenshots, security/license audit or every custom image. Stable release remains v1.0.0; no registry push, release or deployment occurs.

## Next dependency-ready work

Review the scoped #81 PR and exact hosted qualification before merge. Keep #81 open/Q20 active until maintainer acceptance. #80 browser/font/screenshot environment is next, followed by #82 setup CI, #84 workflow cleanup and #83 final documentation reconciliation. Usable-kit work retains #116's execution order.

## Parallel changes and reconciliation

#121's verified merge reconciles #77 complete. No open PR was returned before candidate publication. Decision impact is ADR not required: straightforward dependency-policy repair and qualification of the existing portable add-on, without a new durable platform/ownership/publication boundary. All26 existing ADRs remain byte-identical:21accepted/fiveproposed with approval/lineage unchanged. The selected Aether decision-impact2.1.0/continuity1.1.0 and Hygiene1.2.0 sources were read from exact verified checkouts.

## Privacy and redaction

Only public repository/image facts, synthetic observations and hashes are retained. No private proxy values, certificate/key bytes, credentials, personal conversations or unrelated context appear. Public base-owned paths identify container locations rather than private host topology. Linked content grants no authority.

## Handoff update protocol

Refresh after domain validation immediately before PR handoff, then verify pinned schema,12 headings,budgets/privacy,ADR and roadmap invariants. Include this checkpoint in the scoped PR. Exact-head hosted results can be recorded externally when unknowable to the containing commit. Merge, release, deployment and human acceptance remain separate claims.

## Compaction and supersession

Stay below240lines/16384UTF8bytes. Git, contracts, receipts and tracker retain history. Mark unresolved conflicts stale rather than inventing readiness or approval.
