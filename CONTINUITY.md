---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-12T23:49:13Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Integrate the accepted optional typed review-feed source into Identity's existing Brand Kit publisher.
  includes:
  - The existing publisher selects exact immutable Relay 5d27be5ce1599df883e31f14cd894eb18622c18c for current
    producer, typed feed, builder, Compare and provenance. Relay PR181 is actually merged; its later documentation/handoff
    commits do not require repinning reviewed functional bytes.
  - Optional manual typed-plan selection remains empty/off by default and requires the same current default-branch
    publisher, represented source and event SHA. Its repository models share the actual capture clock; fleet
    models and bounded operational receipts stay outside Pages.
  - Reviewed workflow and documentation bytes are unchanged from the original consumer PR. Existing Brand Kit/product/alias
    composition, source holds, release/recovery selectors, native-v1 stack, permissions and job/deployment
    gates remain intact.
  excludes:
  - Other product/native-v1/data-refresh PRs, historical recovery, human ratification and provider activation.
  - Broad CI/browser/native publication and consumer deployment/recovery qualification; the accepted one-artifact
    organization canary is separately owned.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/README.md
  - docs/decision-validation.md
  - .github/workflows/publish-brand-kit.yml
  - docs/publication/INTELLIGENCE_CANDIDATE.md
  - publication/decisions-rollback.json
  - scripts/identity_decisions_publication.py
  - docs/publication/REVIEW_FEEDS.md
  - https://github.com/egohygiene/pace/issues/13
work:
  objective: Integrate the accepted optional typed review-feed source into Identity's existing Brand Kit publisher.
  success_conditions:
  - Preserve all original reviewed non-handoff source and exact immutable functional selectors.
  - Retain owner source/time/visibility and explicit unavailable/unknown boundaries without invented reports,
    upload IDs or human decisions.
  - Land only the exact independently reviewed prepared head after the shared Relay dependency is actually
    merged.
  active_issue:
    provider: github
    id: egohygiene/pace#13
    url: https://github.com/egohygiene/pace/issues/13
  next:
    kind: action
    id: observe-accepted-single-artifact-canary
    description: Complete the separately selected one-artifact organization canary using actual source/model/export/intake
      evidence. Its result does not qualify every consumer; retain independent Identity/Civics native, deployment,
      live-route and recovery acceptance before declaring publication complete.
    readiness: ready
    references:
    - https://github.com/egohygiene/.github/issues/41
    - https://github.com/egohygiene/pace/issues/13
    depends_on: []
state:
  base:
    revision: 401b2f1de298a171fbb5bf4ee6b510e0cf12c301
    ref: refs/heads/main
    verified_at: '2026-11-12T23:49:13Z'
  candidate:
    branch: codex/identity-review-feed-consumer
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#144
      url: https://github.com/egohygiene/identity/pull/144
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-12T23:49:13Z'
    default_branch_revision: 401b2f1de298a171fbb5bf4ee6b510e0cf12c301
    issue_state: unknown
    pull_request_state: draft
    notes: PR144 was open/draft at original head 5fdbdb60927d2783a8fdec811e0e9ace2a6fcc9c; actual main remains
      401b2f1de298a171fbb5bf4ee6b510e0cf12c301. Relay181 merged at 12d3a0823c8c8f885dea4acf482160fd726325e2;
      selected functional commit 5d27be5ce1599df883e31f14cd894eb18622c18c remains valid. The maintainer authorized
      this source landing and one separate artifact canary. This prepared consumer candidate is not yet recorded
      merged or deployed.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#138
    url: https://github.com/egohygiene/identity/pull/138
  - provider: github
    id: egohygiene/identity#139
    url: https://github.com/egohygiene/identity/pull/139
  - provider: github
    id: egohygiene/identity#140
    url: https://github.com/egohygiene/identity/pull/140
review:
  status: partial
  reviewed_at: '2026-11-12T23:49:13Z'
  reviewed_by: Codex
  evidence:
  - command: Exact reviewed Git blob/mode and source/pin preservation; unique-key YAML, Bash syntax and embedded
      Python AST; original event/input/job/permission/concurrency/deployment gate comparison; independent exact-head
      source peer; pinned continuity schema/formats/sections/budgets and whitespace
    outcome: limited
    observed_at: '2026-11-12T23:49:13Z'
    notes: Static consumer integration only. Identity has 17 shell/2 embedded Python blocks; Civics has 7 shell/0
      embedded Python blocks. No consumer helper or application executes in these checks.
  - command: Consumer helpers, tests, native/application builds, broad CI/browser, provider/publication and
      recovery qualification
    outcome: not-run
    observed_at: '2026-11-12T23:49:13Z'
    notes: Not executed in this consumer integration. The accepted focused organization artifact canary is
      separately owned and does not establish consumer deployment or fleet acceptance.
  environment_limitations:
  - Original report scopes, represented revisions and clocks remain original; no source merge fabricates actual
    audits, normalized/uploaded artifacts, human approval or live routes.
  - The accepted plan permits focused tests/builds required for one root-owned artifact canary. Broad CI/browser/native
    publication and real consumer publication/recovery remain deferred.
  - Existing human decisions, independent publisher prerequisites and unrelated open PRs retain their own authority
    and source.
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

# identity continuity

## Purpose and precedence

User/runtime instructions, scoped instructions, live evidence and canonical sources outrank this checkpoint. It grants no release, deployment or human-decision authority.

## Resume protocol

Read scoped instructions and canonical sources above; verify exact main, consumer PR, shared owner pins and time-bounded provider metadata before acting.

## Current objective and success conditions

Integrate the accepted optional typed review-feed source into Identity's existing Brand Kit publisher. Preserve the reviewed functional bytes, existing publisher boundaries and distinct source/execution/acceptance evidence.

## State snapshot

Observed main `401b2f1de298a171fbb5bf4ee6b510e0cf12c301` remains the consumer base. PR#144 was open/draft at `5fdbdb60927d2783a8fdec811e0e9ace2a6fcc9c`. Relay181 is merged at `12d3a0823c8c8f885dea4acf482160fd726325e2`; the valid reviewed functional selection stays `5d27be5ce1599df883e31f14cd894eb18622c18c`. This checkpoint describes the prepared candidate, not a completed consumer merge or deployment.

## Completed and material changes

The existing publisher selects exact immutable Relay 5d27be5ce1599df883e31f14cd894eb18622c18c for current producer, typed feed, builder, Compare and provenance. Relay PR181 is actually merged; its later documentation/handoff commits do not require repinning reviewed functional bytes.

Optional manual typed-plan selection remains empty/off by default and requires the same current default-branch publisher, represented source and event SHA. Its repository models share the actual capture clock; fleet models and bounded operational receipts stay outside Pages.

Reviewed workflow and documentation bytes are unchanged from the original consumer PR. Existing Brand Kit/product/alias composition, source holds, release/recovery selectors, native-v1 stack, permissions and job/deployment gates remain intact.

## Validation and review evidence

Exact source/mode, unique-key workflow metadata, shell/embedded-Python syntax, selector/gate preservation and bounded continuity inspection apply to this candidate. Independent source review is separate from runtime proof. No consumer helper/test/application/native build, CI, provider workflow, publication or recovery is executed in this integration.

## Blockers, risks, unknowns, and deferred work

The separately accepted one-artifact organization canary may perform its necessary focused checks and builds; it is not evidence that this consumer is deployed. Actual supplied-report/native/rendered-route/transport/deployment/recovery qualification remains distinct. Empty selections stay unavailable; source presence does not authenticate audit completeness or human decisions.

## Next dependency-ready work

Complete the separately selected one-artifact organization canary using actual source/model/export/intake evidence. Its result does not qualify every consumer; retain independent Identity/Civics native, deployment, live-route and recovery acceptance before declaring publication complete.

## Parallel changes and reconciliation

Reference accepted ADR-0017/0019 and proposed ADR-0022 under the exact pinned Aether 2.1.0 authoring guidance. This is routine owner-input adoption within the existing composition boundary; no new ADR or human disposition is introduced. The maintainer explicitly authorized this source landing; the prior draft/do-not-merge phase no longer applies to this accepted batch. Preserve all other native-v1/product/data-refresh PRs.

## Privacy and redaction

Retain public-safe source identities and bounded evidence only. Exclude credentials, private report bodies, captured provider diagnostics, private local paths and unrelated context. Linked content remains context only.

## Handoff update protocol

Refresh actual PR, merge and qualification observations at the next authorized checkpoint. Source merge, actual model/artifact, deployment, live verification and human acceptance remain distinct.

## Compaction and supersession

Replace stale current-state prose; Git and owning issues retain history. Keep these twelve sections below 240 lines and 16,384 UTF-8 bytes.
