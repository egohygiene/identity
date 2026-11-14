---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T20:54:40+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Integrate the explicit v1 initializer with current main and continue the open-issue campaign.
  includes:
  - Authorized open-PR integration and bounded open-issue implementation.
  - Exact local validation and remaining acceptance gates.
  excludes:
  - Later repository audit and act CI campaign.
  - Human ADR disposition, invented rights, new release and deployment.
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
  - docs/decisions/policy-reference.json
  - docs/consumers/V1_INITIALIZATION.md
  - docs/work/98/OWNER_PACKET.md
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Integrate the explicit v1 initializer with current main and continue the open-issue campaign.
  success_conditions:
  - Preserve public contracts, canonical source, approvals and existing publication selectors.
  - Record actual checks and leave unsupported acceptance explicit.
  active_issue:
    provider: github
    id: egohygiene/identity#133
    url: https://github.com/egohygiene/identity/issues/133
  next:
    kind: action
    id: identity-open-work-follow-through
    description: Merge the reconciled initializer and integrate the remaining stacked publication/documentation
      PRs.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: c179a9486410b63c4fa62316b4ccb835cf77ad63
    ref: refs/heads/main
    verified_at: '2026-11-14T20:54:40+00:00'
  candidate:
    branch: codex/133-v1-initializer
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T20:54:40+00:00'
    default_branch_revision: c179a9486410b63c4fa62316b4ccb835cf77ad63
    issue_state: open
    pull_request_state: unknown
    notes: Git fetch and connected GitHub issue/PR reads verified the campaign source. Recheck live state before
      continuing.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T20:54:40+00:00'
  reviewed_by: Codex
  evidence:
  - command: 'python3 -m unittest discover -s tests -p test_verify_retired_guidance.py: three passed; retirement
      guard passed; initializer syntax, schemas, generated-validator and extraction integrity checks passed'
    outcome: passed
    observed_at: '2026-11-14T20:54:40+00:00'
    notes: Scoped local evidence only; no hosted CI, release or deployment is claimed.
  environment_limitations:
  - Initializer behavioral acceptance, native publication, refactors, platform/browser/Docker qualification
    and final tracker closure remain pending. Broad audit and act CI are later work. Root self-source rights
    and human facts remain in the owner packet.
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

User/runtime instructions, scoped repository instructions, live state and canonical sources outrank this checkpoint.

## Resume protocol

Read AGENTS.md and the canonical sources above. Verify main, open issues and PRs before choosing the next work item. Historical source-campaign deferrals do not override the current authorized campaign.

## Current objective and success conditions

Integrate the explicit v1 initializer with current main and continue the open-issue campaign.

## State snapshot

Observed main: c179a9486410b63c4fa62316b4ccb835cf77ad63. Candidate branch: codex/133-v1-initializer. Its containing revision is deliberately not self-referenced. Original open PRs were #138, #139, #140 and #146; inspect current provider state.

## Completed and material changes

PR146 is merged at c179a9486410b63c4fa62316b4ccb835cf77ad63. This reconciliation preserves current publisher and retirement changes while retaining the explicit candidate-only initializer. ADR-0033 remains proposed with null approval.

## Validation and review evidence

python3 -m unittest discover -s tests -p test_verify_retired_guidance.py: three passed; retirement guard passed; initializer syntax, schemas, generated-validator and extraction integrity checks passed. These results establish only their named local scope.

## Blockers, risks, unknowns, and deferred work

Initializer behavioral acceptance, native publication, refactors, platform/browser/Docker qualification and final tracker closure remain pending. Broad audit and act CI are later work. Root self-source rights and human facts remain in the owner packet.

## Next dependency-ready work

Merge the reconciled initializer and integrate the remaining stacked publication/documentation PRs.

## Parallel changes and reconciliation

Preserve newer Repository Intelligence/typed-feed publisher changes when integrating older product branches. Merge does not approve an ADR. Aether create-decisions-document 2.1.0 and continuity 1.1.0 were read from exact Git objects at dc8a16851f452763ef4f7fbe4bf057d4500b1921; Hygiene policy 1.2.0, ratification and migration were read at a05b14f8b9e2772124f879f818e09a911e996ad8. Initializer/native-publication interfaces reference proposed ADR-0033/0034; routine invariant-preserving cleanup needs no new ADR.

## Privacy and redaction

Retain public repository facts and bounded evidence. Exclude credentials, private conversation, sensitive personal/business data, private local paths and unrelated context.

## Handoff update protocol

Refresh after scoped domain checks and before handoff. Validate the pinned continuity schema, twelve headings, 240-line/16384-byte limits and whitespace. Keep failed, unavailable and unrun checks explicit.

## Compaction and supersession

Git and owning issues retain history. Keep this file focused on current work. Preserve roadmap IDs/dependencies, ADR lifecycle/approval and the approved screenshot bytes.
