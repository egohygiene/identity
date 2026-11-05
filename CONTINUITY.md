---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-05T05:48:49Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Prepare the actual Identity self-source/rights and native publisher draft under issue98.
  includes:
  - Existing source/rights inventory and incomplete real Identity candidate.
  - Native publication handoff proposal and consolidated owner packet.
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
  - docs/work/98/OWNER_PACKET.md
  - docs/work/98/source-inventory.json
  - docs/decisions/ADR-0034-native-release-publication-input.md
  - https://github.com/egohygiene/identity/issues/98
work:
  objective: Prepare source, owner facts and native publisher handoff without qualification or publication.
  success_conditions:
  - Retain local request, standalone candidate and missing-fact boundaries.
  - Push bounded draft checkpoints with actual source and deferred acceptance recorded.
  active_issue:
    provider: github
    id: egohygiene/identity#98
    url: https://github.com/egohygiene/identity/issues/98
  next:
    kind: action
    id: identity-98-native-publisher-draft
    description: Implement the bounded native publication adapter, update the packet and retain missing source/rights
      gates.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: 19d3d16bd149ddb61a03924a2b688e8e689af68b
    ref: refs/heads/main
    verified_at: '2026-11-05T05:23:14Z'
  candidate:
    branch: codex/98-native-publication-source
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#139
      url: https://github.com/egohygiene/identity/pull/139
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-11-05T05:23:14Z'
    default_branch_revision: 19d3d16bd149ddb61a03924a2b688e8e689af68b
    issue_state: open
    pull_request_state: draft
    notes: Main remains19d3d16; draft138 and stacked draft139 are open. This source preparation supplies no
      current-source runtime qualification or issue closure.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#138
    url: https://github.com/egohygiene/identity/pull/138
review:
  status: partial
  reviewed_at: '2026-11-05T05:48:49Z'
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
  - command: Publication Python AST, candidate JSON/workflow YAML parsing; node --check on changed publisher/verifier/download/UI
      modules; git diff --check
    outcome: passed
    observed_at: '2026-11-05T05:48:49Z'
    notes: Syntax/static source preparation only; native/legacy publication paths, file integrity failures,
      release workflows and UI behavior are unrun.
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

This is the unqualified issue98 self-source/publisher draft, stacked on PR138. User/runtime instructions, scoped instructions, live state and canonical sources outrank this snapshot.

## Resume protocol

Read AGENTS, the initializer guide, source-campaign checkpoint and live issue133/116. Recheck main, candidate head and peer PRs before acting. PR137 is merged; do not repeat the README split or earlier source merges.

## Current objective and success conditions

Prepare the real Identity source/rights candidate and an opt-in native publisher handoff. Reuse verified generated material, preserve legacy release bindings and keep missing rights/creative decisions explicit.

## State snapshot

Base/main is 19d3d16bd149ddb61a03924a2b688e8e689af68b. This branch proposes the initializer interface and implementation. Its containing commit/PR need fresh inspection; no self-referential commit hash is fabricated.

## Completed and material changes

PR139 inventories 43 existing source/package files and retains an incomplete manually prepared self-source candidate. Its native publisher adapter consumes verified native/optional artifacts, preserves native bytes, separates canonical/inventory digests and binds release-owned files to selected Git blobs. ADR-0034 remains proposed; the owner packet records missing rights and deferred qualification. PR138 remains a separate unqualified initializer draft.

## Validation and review evidence

The supported installer and browser download passed on the named base. Git/API authentication and managed Docker execution work. Those results are bootstrap evidence only. Candidate AST/JSON parsing, bounded formatting, offline Rust compilation and whitespace/source-preservation inspection passed. No candidate runtime or regression suite ran.

## Blockers, risks, unknowns, and deferred work

Refactors, audits, tests, hosted CI, merges and affected issue closures are deferred to a separate campaign. Unknown root asset rights and actual self-source/release/adoption stay issue98. Detailed protection API access is403. Publisher-affecting merges can automatically deploy and therefore remain draft.

## Next dependency-ready work

Complete the native publisher source draft and consolidated packet, then prepare issue83 documentation. Keep original dependencies, missing owner facts and deferred acceptance intact.

## Parallel changes and reconciliation

No peer open PR was observed before this initial draft. Recheck before handoff. The new public initializer needs proposed ADR-0033 under the exact pinned Aether skill; routine scheduling needs no new ADR. Existing dispositions and historical receipts remain unchanged.

## Privacy and redaction

Retain only public-safe repository facts, exact revisions, commands and bounded outcomes. Exclude credentials, private conversation, private paths and unrelated context.

## Handoff update protocol

Refresh after actual source/static checks and immediately before updating the draft. Keep all twelve headings and the 240-line/16384-byte budget. Never substitute source delivery or old test receipts for current qualification.

## Compaction and supersession

Git and the owning issues retain history. This file keeps only the current objective, evidence limits and next action. IDN-Q06 remains planned and unissued; no ecosystem-policy or component expansion is selected.
