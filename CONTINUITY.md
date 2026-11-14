---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T04:19:35Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Keep retired one-time guidance writers inactive and complete their local regression checkpoint.
  includes:
  - Read-only guard rejects both retired workflow names and renamed definitions targeting the historical
    feature branch. Existing source/documentation and release authority remain separate.
  - A narrow exact-inventory regression repair includes the two already-committed launch-document schemas;
    no product schema bytes or validation semantics change.
  excludes:
  - Rust, browser, hosted workflow and publication qualification are not part of this guard-only change.
    Existing native-v1 PR138/139/140 and wider stabilization remain independent.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - scripts/verify_retired_guidance.py
  - tests/test_verify_retired_guidance.py
  - .github/workflows/validate.yml
  - docs/work/116/workflow-retirement.md
  - https://github.com/egohygiene/identity/issues/84
work:
  objective: Keep retired one-time guidance writers inactive and complete their local regression checkpoint.
  success_conditions:
  - 168 Python tests pass with two existing skips; retirement, documentation, release metadata, generated
    validator and extraction integrity checks pass.
  - Keep source checks distinct from provider, publication and human acceptance.
  active_issue:
    provider: github
    id: egohygiene/identity#84
    url: https://github.com/egohygiene/identity/issues/84
  next:
    kind: action
    id: review-84-checkpoint
    description: Review the bounded draft and exact evidence; preserve outstanding owner/provider gates
      before broader issue closeout.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/84
    depends_on: []
state:
  base:
    revision: cfb6c29bd02589a47fc48050ab02e7e0da359719
    ref: refs/heads/main
    verified_at: '2026-11-14T04:19:35Z'
  candidate:
    branch: fix/84-retire-guidance-rewriters
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T04:19:35Z'
    default_branch_revision: cfb6c29bd02589a47fc48050ab02e7e0da359719
    issue_state: open
    pull_request_state: not-applicable
    notes: Live main and owner issue were inspected before implementation. This pre-PR candidate leaves
      its containing revision and provider reference null intentionally.
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
  reviewed_at: '2026-11-14T04:19:35Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover -s tests -p test_*.py; verify_retired_guidance.py; verify_docs.py;
      verify_release.py; build_identity_validator.py --check; verify_extraction.py
    outcome: passed
    observed_at: '2026-11-14T04:19:35Z'
    notes: 168 Python tests pass with two existing skips; retirement, documentation, release metadata,
      generated validator and extraction integrity checks pass.
  environment_limitations:
  - Rust, browser, hosted workflow and publication qualification are not part of this guard-only change.
    Existing native-v1 PR138/139/140 and wider stabilization remain independent.
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

# identity-84 continuity

## Purpose and precedence

User/runtime and scoped instructions, live provider evidence and canonical sources outrank this snapshot. No additional authority is granted.

## Resume protocol

Read AGENTS, the linked owner issue and current target branch before continuing. Verify all mutable issue/PR claims.

## Current objective and success conditions

Keep retired one-time guidance writers inactive and complete their local regression checkpoint.

## State snapshot

Candidate `fix/84-retire-guidance-rewriters` starts at main `cfb6c29bd02589a47fc48050ab02e7e0da359719`. Containing revision and pre-PR reference stay null intentionally.

## Completed and material changes

Read-only guard rejects both retired workflow names and renamed definitions targeting the historical feature branch. Existing source/documentation and release authority remain separate.

A narrow exact-inventory regression repair includes the two already-committed launch-document schemas; no product schema bytes or validation semantics change.

## Validation and review evidence

168 Python tests pass with two existing skips; retirement, documentation, release metadata, generated validator and extraction integrity checks pass.

## Blockers, risks, unknowns, and deferred work

Rust, browser, hosted workflow and publication qualification are not part of this guard-only change. Existing native-v1 PR138/139/140 and wider stabilization remain independent.

## Next dependency-ready work

Independently review the draft, reconcile any new target changes and retain remaining gates in the owning issue.

## Parallel changes and reconciliation

Known native-v1 or publication work remains separately owned; this change neither merges nor activates another candidate.

## Privacy and redaction

Public source facts and synthetic fixtures only. No private exports, credentials, personal content or raw private paths belong in this handoff.

## Handoff update protocol

Record exact tested heads, actual checks, reviewer findings and provider outcomes before integration. Do not infer acceptance from source presence.

## Compaction and supersession

This replaces the previous active snapshot. Historical release/adoption evidence remains available through Git and its owning work records.
