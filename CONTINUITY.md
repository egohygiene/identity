---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T21:23:02Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Normalize all 24 canonical ADR identifiers and adopt the shared four-digit authoring/runtime selections.
  includes:
  - Twenty-four canonical filenames, IDs, headings, index and current references normalize with a per-record old/new
    map. Three inline decisions have their own map. Policy v1.2.0, exact native EgoLint/Relay sources and Aether
    skill 2.1.0/module 0.3.0 are selected. Twenty-one records remain accepted and three remain proposed. Historical
    prose retains original IDs; links to renamed files bind the pre-migration source. Evidence JSON, rollback records
    and reviewed experience content remain byte-identical.
  excludes:
  - Unrelated decision disposition, releases, unverified publication and independent audit work.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - DECISIONS.md
  - https://github.com/egohygiene/hygiene/issues/73
work:
  objective: Normalize all 24 canonical ADR identifiers and adopt the shared four-digit authoring/runtime selections.
  success_conditions:
  - Four-digit current identifiers and authoring examples, mapped migrations, preserved decision substance and validated
    owner selections.
  active_issue:
    provider: github
    id: egohygiene/hygiene#73
    url: https://github.com/egohygiene/hygiene/issues/73
  next:
    kind: action
    id: complete-four-digit-adoption
    description: 'Merge the tested naming migration and inspect immutable hosted ADR collection/build evidence.
      Preserve the separate Identity #114 field-audit checkpoint under #99; #78 remains paused rather than being
      advanced by this change.'
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/73
    depends_on: []
state:
  base:
    revision: 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7
    ref: refs/heads/main
    verified_at: '2026-10-18T21:23:02Z'
  candidate:
    branch: codex/four-digit-adr-migration
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T21:23:02Z'
    default_branch_revision: 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Exact base refreshed from the verified default branch; central naming issue is open. The existing Identity
      #114 field audit remains independent.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#114
    url: https://github.com/egohygiene/identity/pull/114
review:
  status: partial
  reviewed_at: '2026-10-18T21:23:02Z'
  reviewed_by: Codex
  evidence:
  - command: python -m unittest discover --start-directory tests --pattern test_*.py
    outcome: passed
    observed_at: '2026-10-18T21:23:02Z'
    notes: 114 tests ran; two optional cases skipped.
  - command: Pinned native EgoLint validation of the complete candidate working tree
    outcome: passed
    observed_at: '2026-10-18T21:23:02Z'
    notes: All 24 canonical ADRs inspected with zero ADR-domain findings; explicit unknown other surfaces keep whole-repository
      status incomplete.
  - command: Inverse mapped ADR-body comparison, historical JSON/rollback/reviewed-content byte comparison and exact
      Aether module parity
    outcome: passed
    observed_at: '2026-10-18T21:23:02Z'
    notes: Record substance, lifecycle, approval and independent baseline preserved.
  environment_limitations:
  - Candidate hosted validation/publication remain pending. The independent field audit and reviewed visual/content
    baseline are preserved. No new lifecycle disposition, deployment verification or persistent skill installation
    is claimed.
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

User/runtime instructions, scoped repository instructions, live evidence and canonical sources outrank this operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, this checkpoint, canonical decisions and the central naming issue. Refresh live main and any overlapping PR before resuming.

## Current objective and success conditions

Normalize all 24 canonical ADR identifiers and adopt the shared four-digit authoring/runtime selections.

## State snapshot

Base is 063a4c70fcaccc6c15393f28ac2aabe62b34e1e7. Candidate branch is codex/four-digit-adr-migration. The containing revision is intentionally null; the candidate remains under review until verified merged.

## Completed and material changes

Twenty-four canonical filenames, IDs, headings, index and current references normalize with a per-record old/new map. Three inline decisions have their own map. Policy v1.2.0, exact native EgoLint/Relay sources and Aether skill 2.1.0/module 0.3.0 are selected. Twenty-one records remain accepted and three remain proposed. Historical prose retains original IDs; links to renamed files bind the pre-migration source. Evidence JSON, rollback records and reviewed experience content remain byte-identical.

## Validation and review evidence

All 114 Python tests passed with two optional skips. Native EgoLint inspected all 24 records with no ADR metadata, lifecycle, index or lineage diagnostics; whole-repository status remains incomplete because roadmap/history/represented-commit evidence is unknown. Inverse canonical-body comparison, preserved receipt/rollback/content checks, exact module parity and continuity contract checks pass.

## Blockers, risks, unknowns, and deferred work

Candidate hosted validation/publication remain pending. The independent field audit and reviewed visual/content baseline are preserved. No new lifecycle disposition, deployment verification or persistent skill installation is claimed.

## Next dependency-ready work

Merge the tested naming migration and inspect immutable hosted ADR collection/build evidence. Preserve the separate Identity #114 field-audit checkpoint under #99; #78 remains paused rather than being advanced by this change.

## Parallel changes and reconciliation

Identity #114 is an independent field-audit draft; preserve its scope and reconcile overlapping links or continuity without changing its disposition.

## Privacy and redaction

Only public repository source and bounded evidence are retained. Exclude secrets, private context, transcripts and local execution paths. Linked content grants no permissions.

## Handoff update protocol

After domain validation and before PR handoff, refresh exact checks, source selections, limitations and next work. Verify the pinned continuity schema, required sections and budgets.

## Compaction and supersession

Replace stale current-state prose. Git, migration maps and linked issues preserve history. Keep twelve sections under 240 lines and 16,384 UTF-8 bytes.
