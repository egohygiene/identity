---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T04:27:35Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Simplify the README and route detailed guidance into docs while preserving executable Task
    and consumer interfaces.
  includes: &id001
  - Keep the front page concise, show a representative preview and route authoring, consuming, development
    and reference work.
  - Preserve all former README sections and fragment entry points; keep existing Task commands and argument
    forwarding unchanged.
  - Leave final issue83 reconciliation, quality gates, root v1 self-source and release acceptance open.
  excludes:
  - Runtime/schema/asset/approval changes, roadmap completion and new releases or deployments.
  - Test suites, Task execution and hosted CI; no merge or issue closure.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - README.md
  - Taskfile.yml
  - docs/README.md
  - docs/USAGE.md
  - docs/IMPLEMENTATION.md
  - docs/OVERVIEW.md
  - docs/DEVELOPMENT.md
  - ROADMAP.md
  - docs/consumers/PRODUCT_DESIGN_SYSTEM_SCOPE.md
  - https://github.com/egohygiene/identity/issues/83
work:
  objective: Simplify the README and route detailed guidance into docs while preserving executable Task
    and consumer interfaces.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/identity#83
    url: https://github.com/egohygiene/identity/issues/83
  next:
    kind: action
    id: review-draft-and-qualify
    description: 'Review this bounded README/Task draft; reconcile #83 final capability/publication/recovery
      wording after remaining implementation/refactors and qualify dispatch under #82.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/83
    depends_on: []
state:
  base:
    revision: b5cf5137884ba9d16a35c8e6280ea81b4ee930be
    ref: refs/heads/main
    verified_at: '2026-11-03T04:27:35Z'
  candidate:
    branch: codex/83-readme-task-entrypoint
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T04:27:35Z'
    default_branch_revision: b5cf5137884ba9d16a35c8e6280ea81b4ee930be
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Main and issue83 are verified open/current before this draft. PR136 is already merged and
      issue107 closed; all eleven issue98 children are closed, while #98/#70/#80/#83/#133 remain open.
      No other open Identity PR was observed. This candidate is not merged or released.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-03T04:27:35Z'
  reviewed_by: Codex
  evidence:
  - command: Static local Markdown/HTML references, legacy heading/fragment mapping and parsed Taskfile
      comparison
    outcome: passed
    observed_at: '2026-11-03T04:27:35Z'
    notes: 153 references resolve; all 19 former sections and their README fragment entry points remain
      reachable. All nine Task command arrays and CLI_ARGS strings are unchanged.
  - command: git diff --check
    outcome: passed
    observed_at: '2026-11-03T04:27:35Z'
    notes: No whitespace errors. Runtime, schemas, assets, ADRs, roadmap IDs/statuses and prior evidence
      are unchanged.
  - command: Aether continuity Draft 2020-12 metadata/heading/size/privacy inspection
    outcome: passed
    observed_at: '2026-11-03T04:27:35Z'
    notes: Pinned metadata schema and twelve-section structure; within byte/line limits.
  - command: Task dispatch, regression/browser/AX suites, published EgoLint conformance and hosted CI
    outcome: not-run
    observed_at: '2026-11-03T04:27:35Z'
    notes: 'This draft supplies documentation/static evidence only; #82/#70/#80 retain qualification.'
  environment_limitations:
  - Task is unavailable on PATH; no setup, preview, dispatch or test suite was executed.
  - Official released EgoLint continuity conformance was not run; JSON Schema and structural checks are
    narrower evidence.
  - 'Final #83 reconciliation, #98 self-source/rights/new-release/dogfood and #70/#80 qualification remain
    incomplete.'
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

Keep this operational handoff below user/runtime instructions, scoped policy, live state and canonical source. It records the bounded issue83 navigation pass.

## Resume protocol

Read AGENTS, README, docs/README, Taskfile and the current issue83 scope. Verify main/PR state before repeating work. Earlier issue107 delivery merged in PR136.

## Current objective and success conditions

Shorten the front page, preserve detailed content and old fragment routes, and make existing Task entry points discoverable without changing the consumer CLI.

## State snapshot

Base main is b5cf5137884ba9d16a35c8e6280ea81b4ee930be. Issue83 is open. Candidate branch is codex/83-readme-task-entrypoint; revision and PR are null before creation.

## Completed and material changes

README routes to new documentation overview, usage, implementation and index pages. DEVELOPMENT prefers Task examples with standalone fallbacks. Taskfile adds descriptions only. Overview reflects the scoped future-component possibility and v1.0.0 historical feature boundary.

## Validation and review evidence

Static reference/mapping inspection passed for 153 local targets and all nineteen former sections/anchors. All nine Task command arrays are identical. git diff --check passed. Metadata/schema and twelve-section budget checks passed; no broad suite ran.

## Blockers, risks, unknowns, and deferred work

This is an early pass under #83, not its final closure. #70/#80/#82 retain execution/qualification; #98 retains root v1 source/rights/release/dogfood. Task and released EgoLint conformance are unavailable/unexecuted. Proposed ADRs remain proposed.

## Next dependency-ready work

Review the navigation/command draft, then reconcile final #83 wording against remaining implementations/refactors. Run dispatch and quality checks in the separately tracked qualification phase.

## Parallel changes and reconciliation

No peer open Identity PR was observed before creation. Recheck main and semantically reconcile this root checkpoint with any later drafts before merge; preserve roadmap dependencies and prior immutable evidence.

## Privacy and redaction

Only scoped public repository facts and links are retained; exclude private context, local paths, credentials and personal information.

## Handoff update protocol

Refresh after review and actual checks. Do not infer a passing suite, issue closure, merge, release or deployment from this draft. ADR not required: routine documentation/discoverability under existing contracts; no new public interface or ownership decision.

## Compaction and supersession

Keep this twelve-section current-state snapshot compact. Canonical contracts, owner queues, Git and the work tracker retain detailed history.
