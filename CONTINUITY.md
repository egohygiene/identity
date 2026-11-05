---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-05T05:32:42Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Prepare the explicit v1 initializer as an unqualified draft under issue133.
  includes:
  - Explicit v1 candidate/request interface and source implementation.
  - Current source-campaign scheduling, bootstrap evidence and durable draft checkpoints.
  excludes:
  - Refactors, runtime tests, hosted CI, merges and issue closure.
  - Creative/rights approval, release, deployment and other-repository changes.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/policy-reference.json
  - docs/consumers/V1_INITIALIZATION.md
  - docs/work/116/SOURCE_PREPARATION.md
  - https://github.com/egohygiene/identity/issues/133
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Prepare a reviewable explicit v1 initializer without changing v0 behavior.
  success_conditions:
  - Retain local request, standalone candidate and missing-fact boundaries.
  - Push bounded draft checkpoints with actual source and deferred acceptance recorded.
  active_issue:
    provider: github
    id: egohygiene/identity#133
    url: https://github.com/egohygiene/identity/issues/133
  next:
    kind: action
    id: identity-98-source-preparation
    description: Prepare the issue98 source/rights candidate, native publisher draft and owner packet; keep
      this initializer unmerged and unqualified.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/98
    - https://github.com/egohygiene/identity/pull/138
    depends_on: []
state:
  base:
    revision: 19d3d16bd149ddb61a03924a2b688e8e689af68b
    ref: refs/heads/main
    verified_at: '2026-11-05T05:23:14Z'
  candidate:
    branch: codex/133-v1-initializer
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#138
      url: https://github.com/egohygiene/identity/pull/138
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-05T05:23:14Z'
    default_branch_revision: 19d3d16bd149ddb61a03924a2b688e8e689af68b
    issue_state: open
    pull_request_state: draft
    notes: Main remains19d3d16; draft138 was opened at checkpointd513678. The containing source checkpoint
      needs fresh provider inspection. Twelve issues remain open; no issue acceptance is inferred.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-05T05:32:42Z'
  reviewed_by: Codex
  evidence:
  - command: bash scripts/dev-env.sh setup; bash scripts/dev-env.sh browsers
    outcome: passed
    observed_at: '2026-11-05T05:23:14Z'
    notes: Base 19d3d16 built with Rust1.97.1/pnpm11.21.0; Chromium151.0.7922.34 revision1234 installed. Tracked
      source remained unchanged; this does not qualify later candidate source.
  - command: Live main/issues/PRs/release/site.json reads and managed Docker health probe
    outcome: passed
    observed_at: '2026-11-05T05:23:14Z'
    notes: Injected authentication and command execution work; Docker health requires local-socket execution
      permission. Detailed protection endpoint is403; metadata reports unprotected and rulesets are empty.
  - command: Runtime/regression/native/browser/AX suites, audit and hosted CI
    outcome: not-run
    observed_at: '2026-11-05T05:23:14Z'
    notes: Deferred to a separate campaign; no merge, release, deployment or consumer adoption.
  - command: Python AST/new-schema JSON parsing; bounded rustfmt; cargo build --locked --offline; git diff
      --check; roadmap-block/PNG comparison
    outcome: passed
    observed_at: '2026-11-05T05:32:42Z'
    notes: Structural/build evidence for the draft only. Forty roadmap blocks and approved PNG are preserved;
      no initializer behavior or regression suite executed.
  environment_limitations:
  - Downloaded browsers and Docker health do not qualify fonts or the approved screenshot.
  - Onboarding skill unavailable; available cloud runtime and pinned repository guidance were read.
  - Current source, rights, platform/review/CI and final tracker acceptance remain open.
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

This is the unqualified issue133 source draft. User/runtime instructions, scoped instructions, live state and canonical sources outrank this snapshot.

## Resume protocol

Read AGENTS, the initializer guide, source-campaign checkpoint and live issue133/116. Recheck main, candidate head and peer PRs before acting. PR137 is merged; do not repeat the README split or earlier source merges.

## Current objective and success conditions

Implement explicit v1-init from local request files into a separate review candidate. Preserve v0, offline operation, same-subject approvals and source ownership. Retain missing facts honestly.

## State snapshot

Base/main is 19d3d16bd149ddb61a03924a2b688e8e689af68b. This branch proposes the initializer interface and implementation. Its containing commit/PR need fresh inspection; no self-referential commit hash is fabricated.

## Completed and material changes

Draft PR138 adds the closed request/report schemas, trusted stdlib initializer, embedded Rust bridge, examples and manual handoff. The source-campaign checkpoint reconciles scheduling and actual bootstrap. Proposed ADR-0033 defines the new interface; implementation is unqualified. The seven-criterion disposition is in docs/work/133/DRAFT.md.

## Validation and review evidence

The supported installer and browser download passed on the named base. Git/API authentication and managed Docker execution work. Those results are bootstrap evidence only. Candidate AST/JSON parsing, bounded formatting, offline Rust compilation and whitespace/source-preservation inspection passed. No candidate runtime or regression suite ran.

## Blockers, risks, unknowns, and deferred work

Refactors, audits, tests, hosted CI, merges and affected issue closures are deferred to a separate campaign. Unknown root asset rights and actual self-source/release/adoption stay issue98. Detailed protection API access is403. Publisher-affecting merges can automatically deploy and therefore remain draft.

## Next dependency-ready work

Complete the issue133 source draft, push meaningful checkpoints, then prepare issue98 source/rights/publisher work and issue83 documentation. Keep original dependencies and acceptance criteria intact.

## Parallel changes and reconciliation

No peer open PR was observed before this initial draft. Recheck before handoff. The new public initializer needs proposed ADR-0033 under the exact pinned Aether skill; routine scheduling needs no new ADR. Existing dispositions and historical receipts remain unchanged.

## Privacy and redaction

Retain only public-safe repository facts, exact revisions, commands and bounded outcomes. Exclude credentials, private conversation, private paths and unrelated context.

## Handoff update protocol

Refresh after actual source/static checks and immediately before updating the draft. Keep all twelve headings and the 240-line/16384-byte budget. Never substitute source delivery or old test receipts for current qualification.

## Compaction and supersession

Git and the owning issues retain history. This file keeps only the current objective, evidence limits and next action. IDN-Q06 remains planned and unissued; no ecosystem-policy or component expansion is selected.
