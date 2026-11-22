---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T06:18:25.251493+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Record the proposed next-release distribution and compatibility plan without changing release
    artifacts, versions, workflows or current support claims.
  includes:
  - Capture staged native macOS/Linux/Windows cohorts, conditional expansion and package-channel requirements.
  - Separate historical v1.0.0 delivery from proposed next-version compatibility and actual future support
    evidence.
  - 'Reconcile the release process and owner ledger so #98/#116 remain open through their release acceptance.'
  excludes:
  - Workflow, Cargo/lockfile, source, schema, asset, version or support-policy changes.
  - Builds, native/install qualification, hosted CI, signing, tag/release creation, deployment and channel
    publication.
  - Canonical self-source promotion, exact token/layer approval or new human decision disposition.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/releases/NEXT_RELEASE_MATRIX.md
  - docs/releases/RELEASE_PROCESS.md
  - docs/releases/V1.md
  - docs/work/98/OWNER_PACKET.md
  - docs/work/98/OWNER_ANSWERS_2026-11-22.md
  - docs/work/98/candidate/README.md
  - docs/work/98/candidate/.identity/defaults/README.md
  - docs/decisions/ADR-0019-immutable-release-contract.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/98
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Record the proposed next-release distribution and compatibility plan without changing release
    artifacts, versions, workflows or current support claims.
  success_conditions:
  - Keep every new cohort/channel planned until required real build, native/downloaded-install and publication
    evidence exists.
  - Preserve published v1.0.0 and require a new compatible immutable release selection.
  - Maintain the existing source/engineering/release/consumer closure order and separate Aether skill
    installation from the Rust binary/runtime.
  active_issue:
    provider: github
    id: egohygiene/identity#98
    url: https://github.com/egohygiene/identity/issues/98
  next:
    kind: action
    id: prepare-self-source-and-qualified-release-candidate
    description: 'Review/merge the stacked source checkpoints in order, then continue exact local token/layer
      and subject-governance review under #98 plus engineering acceptance under #70. Prepare and qualify
      selected release cohorts before a concrete publication handoff.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/98
    - https://github.com/egohygiene/identity/issues/70
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: b0ab233e6ba36dc749ef07bca8b04f0f1870258f
    ref: refs/heads/codex/98-owner-answers-and-assets-20261122
    verified_at: '2026-11-22T06:15:27Z'
  candidate:
    branch: codex/98-release-matrix-plan-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T06:15:27Z'
    default_branch_revision: afc368003bfc6a2101051229efd237c8d6fadf71
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh provider reads verified main afc3680 and open draft PR155 at b687df5 plus open draft
      PR156 at b0ab233. Issues98/116 remain open. The new child PR does not yet exist; no release/tag
      selection or publication is claimed.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#155
    url: https://github.com/egohygiene/identity/pull/155
  - provider: github
    id: egohygiene/identity#156
    url: https://github.com/egohygiene/identity/pull/156
  - provider: github
    id: egohygiene/aether#139
    url: https://github.com/egohygiene/aether/pull/139
review:
  status: partial
  reviewed_at: '2026-11-22T06:15:27Z'
  reviewed_by: Codex
  evidence:
  - command: python3 scripts/verify_docs.py --repository-root .
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: All current documentation links resolve, including the proposed matrix and owner-ledger references.
  - command: python3 scripts/verify_release.py --repository-root .
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: Current Cargo and renderer metadata remain 1.0.0; tag=not-checked. This does not qualify or
      select a next release.
  - command: git diff --check
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: No whitespace errors in the scoped documentation diff.
  - command: Historical V1/Cargo/lock/workflow/SUPPORT byte comparison against parent
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: Historical release guide, code/version/dependency inputs, release workflow and current support
      claims are unchanged.
  - command: Independent read-only release-plan review
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: Parent reports no blocking finding; target/channel states remain proposed and source/engineering/release
      closure order is explicit.
  - command: Pinned continuity metadata schema, exact headings and budget verification
    outcome: passed
    observed_at: '2026-11-22T06:15:27Z'
    notes: Draft 2020-12 schema and all twelve headings validate; base/candidate/parallel shapes are explicit
      and within 16384 bytes/240 lines. Official released EgoLint continuity conformance is not claimed.
  environment_limitations:
  - 'The retained self-source candidate is still incomplete: its parent checkpoint reports exit 1 / IDN1301
    for empty layers. No new candidate-source validation or acceptance is claimed here.'
  - Exact local token/layer review and formal subject-bound source/governance assembly remain pending.
  - No new build, native or downloaded-install/upgrade/uninstall/offline/recovery qualification, signing,
    hosted CI or release/publication evidence is supplied.
  - Aether companion spec/skill is prepared separately in draft PR139. Host gh skill qualification/publication
    is blocked on installed gh2.46.0; package/source checks do not establish agent behavior.
  - Official released EgoLint continuity conformance is not claimed; this handoff uses pinned schema/heading/budget
    checks.
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

This is a time-qualified operational handoff beneath user/runtime instructions, scoped instructions, live state and canonical sources. It records a proposed release-plan documentation checkpoint, not support promotion or publication authority.

## Resume protocol

Read AGENTS, the next-release guide, release process and owner packet. Re-query main, issues #98/#116 and the stacked PRs. Preserve the existing owner answers, exact selected master bytes, draft local baseline and separate engineering/release obligations.

## Current objective and success conditions

Make broad Rust CLI distribution concrete through a finite staged compatibility plan while retaining honest runtime/ABI, native install, artifact integrity, signing and publication evidence requirements.

## State snapshot

Base is open draft PR156 at b0ab233e6ba36dc749ef07bca8b04f0f1870258f, after open draft PR155 at b687df51649226882f2b218178c7b10933f48a74. Main remains afc368003bfc6a2101051229efd237c8d6fadf71. This child branch has no containing-revision or PR self-reference. Issues98/116 remain open.

## Completed and material changes

NEXT_RELEASE_MATRIX.md proposes four primary native cohorts and conditional ARM64/musl expansion, distribution channels and per-check matrix evidence. RELEASE_PROCESS.md generalizes the next-version candidate procedure and links the guide. OWNER_PACKET.md retains selected release/self-source gates and records the broader target/channel work. The docs index exposes the plan. Published v1.0.0 is immutable; v1.1.0 is only a proposal subject to compatibility review, with no selected new tag or release commit.

## Validation and review evidence

Existing documentation links, release metadata with tag not checked and whitespace checks pass. Historical V1 guide, Cargo/lock, workflow and SUPPORT bytes remain unchanged. Independent read-only review reports no blocker. These are documentation/source-scope checks, not new native, CI, package or release evidence. Pinned Aether decision guidance 2.1.0 and Hygiene policy 1.2.0 retain their existing selected revisions.

## Blockers, risks, unknowns, and deferred work

The actual self-source candidate remains incomplete with retained IDN1301 for empty layers; exact token/layer review and formal source/governance assembly are pending. #70/#80/#82/#88 retain engineering qualification. New matrix rows are planned/conditional, not supported; Python 3.11+ remains a current v1 runtime dependency. Signing identities, actual ABI minima, package channels and downloadable artifacts require their own proof. No new version, tag or release is selected.

## Next dependency-ready work

Review and merge the stack #155, then #156, then this plan, reconciling continuity semantically. Continue #98 exact baseline/source preparation and independent #70 engineering acceptance. Prepare source-changing release repairs before final qualification; then qualify the actual selected target/channel artifacts before publication. Complete #98 release/live/rollback/consumer proof and close #116 last, without requiring zero open issues before their release acceptance.

## Parallel changes and reconciliation

PR155 and PR156 remain open drafts and own earlier scoped changes. Aether's companion workflow spec/skill is prepared separately in draft PR139; its version/install/publication is distinct from Identity's Rust CLI and Python runtime. Its package/source checks pass, while the real gh skill host gate remains blocked on gh2.46.0. Preserve newer peer changes and historical receipts.

## Privacy and redaction

Only public repository facts, selected source references and proposed technical requirements appear here. Exclude private conversation transcripts, credentials, personal details and local filesystem topology.

## Handoff update protocol

Refresh after actual checks and before PR handoff; validate pinned metadata, twelve headings and byte/line budgets. ADR-Ref: egohygiene/identity#ADR-0019 (reference). This documents broader future qualification under the existing immutable-release boundary; it does not adopt a new runtime/channel, alter a public contract or promote any ADR lifecycle.

## Compaction and supersession

Git and the owning issues retain history. Keep this snapshot compact; preserve the historical v1.0.0 guide/artifacts and prior source/approval/recovery records rather than relabeling them as new-release evidence.
