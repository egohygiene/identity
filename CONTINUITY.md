---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:31:06.092872+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Enforce the existing approval review-time date-time contract in the offline validator and embedded
    native preflight.
  includes:
  - Require actual strings and complete RFC3339 date/time grammar with explicit offset before calendar
    validation.
  - Preserve source bytes, IDN1404 and existing entrypoints; regenerate the offline standalone bundle.
  - Retain actual before/after fictional-fixture probes and Python/native no-mutation regression evidence.
  excludes:
  - No inferred human review times, new approval policy, root-source adoption or creative/ADR lifecycle
    promotion.
  - Other timestamp fields, lifecycle date semantics, hosted workflows, new platform qualification and
    publication remain separate.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - contracts/v1/approvals.schema.json
  - scripts/identity_validation/governance.py
  - scripts/validate_identity.py
  - docs/work/70/review-time-20261122/VALIDATION.md
  - docs/work/70/review-time-20261122/before-after.json
  - docs/work/98/self-source-review/README.md
work:
  objective: Enforce the existing approval review-time date-time contract in the offline validator and
    embedded native preflight.
  success_conditions:
  - Reject date-only, naive/basic/week-date, numeric/coerced and malformed-offset approval values.
  - Accept declared lowercase UTC, arbitrary fractional precision and valid calendar/offset forms without
    changing source bytes.
  - Prove authoritative standalone and actual native CLI/library rejection before mutation; keep historical
    and human evidence limits explicit.
  active_issue:
    provider: github
    id: egohygiene/identity#70
    url: https://github.com/egohygiene/identity/issues/70
  next:
    kind: action
    id: qualify-original-browser-and-clean-image-paths
    description: Continue the separate browser/action acquisition and full clean-image qualification checkpoints,
      then review the exact self-source choices. Keep all new changes in draft PRs for review.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    ref: refs/heads/main
    verified_at: '2026-11-22T18:31:06.092872+00:00'
  candidate:
    branch: codex/70-rfc3339-review-times-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T18:31:06.092872+00:00'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: Current main verified; earlier158 through162 and Aether140 are merged. Six Identity issues
      remain open. This source-repair PR does not yet exist; new browser/dev/source checkpoints are separate
      in-progress branches.
  parallel_changes:
  - provider: github
    id: egohygiene/aether#141
    url: https://github.com/egohygiene/aether/pull/141
review:
  status: partial
  reviewed_at: '2026-11-22T18:31:06.092872+00:00'
  reviewed_by: Codex
  evidence:
  - command: Full generated standalone-validator fixture suite and actual before/after isolated script
      probes
    outcome: passed
    observed_at: '2026-11-22T18:31:06.092872+00:00'
    notes: 16methods,18invalid/7valid timestamp subcases and7actual before/after synthetic-fixture probes.
      Corrects old date-only/numeric/naive admission and lowercase-UTC refusal; no source rewrites.
  - command: Full Python discovery with IDENTITY_REQUIRE_FRONTENDS=1
    outcome: passed
    observed_at: '2026-11-22T18:31:06.092872+00:00'
    notes: 212discovered:210passed/two existing optionalexperience/nativeWindows skips. Actual Make and
      checksum-pinnedTask available.
  - command: cargo fmt; strict all-target/all-feature Clippy; locked offline cargo test
    outcome: passed
    observed_at: '2026-11-22T18:31:06.092872+00:00'
    notes: 119native tests pass/four explicithelper ignores. Actual CLI/library date-only/naive preflight
      negatives preserve source,sentinel,output andcache boundaries.
  - command: Standalone drift, extraction provenance, docs, whitespace and independent contract review
    outcome: passed
    observed_at: '2026-11-22T18:31:06.092872+00:00'
    notes: Checks pass; no blocking review finding. No schema/diagnostic-code or platform/release change.
      See exact source-bound work record.
  environment_limitations:
  - Only approval reviewedAt is repaired; other explicit date-time fields need separate bounded checks.
  - Existing calendar parser leap-second limitation is retained; timestamp syntax does not prove a human
    event.
  - Actual source choices and timestamps remain pending owner review; no root adoption or generated self-kit
    acceptance.
  - Original Docker/native-platform/consumer/release gates remain; no hosted workflow or publication performed.
  - No official released EgoLint continuity conformance; pinned schema/headings/budget checks are structural.
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

Runtime/user and scoped instructions, live evidence and canonical source outrank this operational snapshot. This is a draft implementation repair of an existing validity requirement.

## Resume protocol

Read AGENTS, the approval schema and source-bound work record. Verify main and current draft PRs before acting. Earlier Identity158→162 and Aether140 are merged; preserve historical receipts and unrelated checkouts.

## Current objective and success conditions

Enforce the existing approval review-time date-time contract in the offline validator and embedded native preflight.

## State snapshot

Base/main is75ca39f3fc7e5e9e0b5578af58c966cd2590a652. Candidate codex/70-rfc3339-review-times-20261122 has no containing revision or pre-PR reference. This is separate from the ongoing browser/dev/source-assembly checkpoints.

## Completed and material changes

Approval review timestamps no longer gain an invented midnight or timezone through permissive parsing/coercion. Full grammar and calendar validation preserve IDN1404/source bytes, allow valid lowercase UTC and rebuild the standalone validator used by the native bridge. Actual fixture probes and native preflight negatives retain no-mutation evidence.

## Validation and review evidence

The work70/review-time-20261122 record contains exact source and before/after probes. Full Python212methods passes with2existing skips; native119passes/4helper ignores, strictClippy,format,standalone drift,extraction,docs andwhitespace pass. Independent read-only contract/standalone review finds no blocker.

## Blockers, risks, unknowns, and deferred work

This is approval reviewedAt only; other date-time validators and date-only lifecycle semantics are not silently changed. Existing leap-second limitation remains. Actual owner choices/new review instants, original Docker acceptance, native platform/install coverage and release/live/consumer gates remain separate.

## Next dependency-ready work

Finish the source-verified local workflow acquisition and isolated-backend browser/dev qualification. Review exact self-source layer/descriptors/output choices before adoption. #98 retains real producer/publisher/release proof; #116 closes last.

## Parallel changes and reconciliation

Aether141 implements build-only metadata projection; its host-adapter child remains separate. Identity browser/dev workers own original qualification paths; source assembly retains explicitly unselected proposals. Reconcile parent continuity by meaning before stacking; do not concatenate stale snapshots.

## Privacy and redaction

Public source facts, standard fixture mutations and sanitized evidence only. No credentials, private transcript, host paths or invented actual-owner approvals.

## Handoff update protocol

Refresh after domain checks before PR handoff; validate pinned metadata, twelve headings and fixed budgets. Reference ADR0001/0005 and existing approvals schema. The pinned Aether decision/continuity workflow remains selected; no new ADR or lifecycle promotion.

## Compaction and supersession

Git and linked work records retain previous observations. This handoff replaces current operational prose while preserving historical source, approvals and release evidence.
