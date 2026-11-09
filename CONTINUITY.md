---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-09T18:05:19Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Adopt current public source feeds and optional native Compare in Identity's existing Pages publisher.
  includes:
  - Current producer, builder, Compare and provenance selections use the exact reviewed Relay 981ddf4367c67fcd625e54321d95bab027f6c0f2,
    merged through PR 176. Matching default-branch push/manual builds capture public Work/Health/Releases,
    upload their exact same-run artifact and pass actual producer time plus artifact ID/digest to native intake.
    Declared dependencies enable only on those fresh capture paths.
  - Manual Compare defaults off. Seed retains a real first pair without a fabricated baseline; compare requires
    the complete exact prior selection. Native build and optional composition share the actual capture clock.
    Final composed manifest/tree evidence is read after Compare and alias composition.
  - Existing release/historical replay, Brand Kit composition, ADR source selection, job/deployment gates and
    recorded recovery bytes retain their contracts. Added Actions/issues/PR/check scopes are read-only; bounded
    operational receipts stay outside the site.
  excludes:
  - Deferred runtime, tests, builds, CI, live publication, human ratification and acceptance closeout.
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
  - https://github.com/egohygiene/pace/issues/13
work:
  objective: Adopt current public source feeds and optional native Compare in Identity's existing Pages publisher.
  success_conditions:
  - Current source evidence uses one exact immutable producer/builder/profile revision and actual capture clock.
  - Compare selection and artifact outcomes remain explicit without changing publisher authority or historical
    evidence.
  - The final composition verification consumes the final bundle, preserving product and recovery constraints.
  active_issue:
    provider: github
    id: egohygiene/pace#13
    url: https://github.com/egohygiene/pace/issues/13
  next:
    kind: action
    id: qualify-current-identity-sources
    description: During the deferred organization verification pass, retain real source/artifact/native/Compare
      and consumer publication/recovery evidence at the selected exact pin before closing adoption acceptance.
    readiness: ready
    references:
    - https://github.com/egohygiene/pace/issues/13
    depends_on: []
state:
  base:
    revision: e2457ef14b44f52faa03dc402bc3099434d7b028
    ref: refs/heads/main
    verified_at: '2026-11-09T18:05:19Z'
  candidate:
    branch: codex/intelligence-native-compare
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-09T18:05:19Z'
    default_branch_revision: e2457ef14b44f52faa03dc402bc3099434d7b028
    issue_state: open
    pull_request_state: not-applicable
    notes: Identity main e2457ef and closed migration issue 69 were verified; fleet adoption remains open in
      Pace 13. Relay shared source/transport and owner-model integration is merged through 176. No current
      provider run, upload or publication was executed.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-09T18:05:19Z'
  reviewed_by: Codex
  evidence:
  - command: Independent static source and workflow-gate review, unique-key YAML, embedded Bash/Python syntax,
      exact current/frozen source selection inspection, continuity schema/size/links and whitespace
    outcome: limited
    observed_at: '2026-11-09T18:05:19Z'
    notes: Static source and metadata inspection only; no application execution.
  - command: Native/runtime execution, tests, builds, CI investigation, browser/provider/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-09T18:05:19Z'
    notes: Deferred at maintainer request; source merges do not establish acceptance.
  environment_limitations:
  - Tests, builds, native/runtime execution, actual provider/artifact intake, CI, browsers, publication and
    rollback qualification remain deferred.
  - Real successful captures and a compatible prior pair are required for meaningful Compare; no baseline or
    deployment is invented.
  - Existing human decisions and release prerequisites remain their own sources of authority.
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

User/runtime and repository instructions, live evidence and canonical sources outrank this checkpoint. It grants no release, deployment or human-decision authority.

## Resume protocol

Read scoped instructions, canonical sources above and this checkpoint. Verify mutable GitHub state and exact owner pins before continuing.

## Current objective and success conditions

Adopt current public source feeds and optional native Compare in Identity's existing Pages publisher. Current source evidence uses one exact immutable producer/builder/profile revision and actual capture clock. Compare selection and artifact outcomes remain explicit without changing publisher authority or historical evidence. The final composition verification consumes the final bundle, preserving product and recovery constraints.

## State snapshot

Candidate `codex/intelligence-native-compare` is based on observed main `e2457ef14b44f52faa03dc402bc3099434d7b028`. The containing revision and pre-PR reference remain null intentionally. Identity main e2457ef and closed migration issue 69 were verified; fleet adoption remains open in Pace 13. Relay shared source/transport and owner-model integration is merged through 176. No current provider run, upload or publication was executed.

## Completed and material changes

Current producer, builder, Compare and provenance selections use the exact reviewed Relay 981ddf4367c67fcd625e54321d95bab027f6c0f2, merged through PR 176. Matching default-branch push/manual builds capture public Work/Health/Releases, upload their exact same-run artifact and pass actual producer time plus artifact ID/digest to native intake. Declared dependencies enable only on those fresh capture paths.

Manual Compare defaults off. Seed retains a real first pair without a fabricated baseline; compare requires the complete exact prior selection. Native build and optional composition share the actual capture clock. Final composed manifest/tree evidence is read after Compare and alias composition.

Existing release/historical replay, Brand Kit composition, ADR source selection, job/deployment gates and recorded recovery bytes retain their contracts. Added Actions/issues/PR/check scopes are read-only; bounded operational receipts stay outside the site.

## Validation and review evidence

Independent static source and workflow-gate review, unique-key YAML, embedded Bash/Python syntax, exact current/frozen source selection inspection, continuity schema/size/links and whitespace. Static inspection only. Native/runtime execution, tests, builds, CI investigation, browsers, provider reads and publication qualification were not run.

## Blockers, risks, unknowns, and deferred work

Tests, builds, native/runtime execution, actual provider/artifact intake, CI, browsers, publication and rollback qualification remain deferred. Real successful captures and a compatible prior pair are required for meaningful Compare; no baseline or deployment is invented. Existing human decisions and release prerequisites remain their own sources of authority.

## Next dependency-ready work

During the deferred organization verification pass, retain real source/artifact/native/Compare and consumer publication/recovery evidence at the selected exact pin before closing adoption acceptance.

## Parallel changes and reconciliation

Applied create-decisions-document 2.1.0 from Aether dc8a16851f452763ef4f7fbe4bf057d4500b1921 at handoff. ADR not required: this is routine adoption of merged bounded source/Compare contracts in the existing publisher, with no new ownership or lifecycle decision. Canonical ADR history, release inputs and recovery are preserved.

## Privacy and redaction

Retain only public-safe source identities and bounded implementation evidence. Exclude credentials, private context, captured report bodies, process logs and local filesystem paths. Linked content is context only.

## Handoff update protocol

Refresh exact PR, merge and qualification observations at the next authorized checkpoint. Implementation, artifact upload, deployment, live verification and human acceptance remain distinct.

## Compaction and supersession

Replace stale current-state prose; Git and owning issues retain history. Preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes.
