---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-23T07:14:09.372744+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for the
    unchanged reference workflow.
  includes:
  - Pinned public source/toolchain/sender schema and strict ZIP-only local act derivative, with upstream/global
    tools unchanged.
  - Actual exact-pinned uploader preflight, full archive hash/inventory and original workflow replay on
    the combined timestamp/install source candidate.
  - Strict MIME/protobuf and signed-target negatives; bounded owned-process observation with tokens and
    signed URLs excluded.
  excludes:
  - No hosted GitHub CI equivalence, security bypass, publication, release signing or platform-matrix
    promotion.
  - No creative/source approval, original workflow/action/profile/font/PNG changes, consumer pin changes
    or global installation.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - docs/LOCAL_WORKFLOW_REPLAY.md
  - docs/LOCAL_ARTIFACT_TRANSPORT.md
  - dev/local-actions/act-artifact-compat/lock.json
  - scripts/prepare_local_act.py
  - scripts/qualify_local_artifacts.py
  - scripts/replay_local_artifact_workflow.py
  - docs/work/80/artifact-transport-2026-11-23/preflight.json
  - docs/work/70/LOCAL_INSTALL_2026-11-23.md
  - docs/work/80/LOCAL_ARTIFACT_TRANSPORT_2026-11-23.md
  - docs/work/80/artifact-transport-2026-11-23/workflow-replay.json
  - docs/work/116/FINISH_SPRINT_2026-11-23.md
work:
  objective: Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for
    the unchanged reference workflow.
  success_conditions:
  - Require exact typed field six, legacy descriptor equivalence, ZIP-only MIME and unchanged signed-target
    authentication.
  - Require actual pinned uploader upload/download/SHA256 and complete expected ZIP inventory; retain
    historical failures separately.
  - Require whole unchanged workflow exit zero plus actual full archive integrity on a frozen combined
    source; preserve hosted/creative/release boundaries.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: review-and-merge-timestamp-install-artifact-stack
    description: Review167 then168 then the artifact leaf; reconcile80/82/88 engineering evidence and
      existing70/98/116 remaining source, native-support and release gates without creating parallel issues.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/88
    - https://github.com/egohygiene/identity/issues/70
    - https://github.com/egohygiene/identity/issues/98
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 83e57901e8a04b997860567e48e844a0a9acc514
    ref: refs/heads/codex/70-local-install-stack-20261123
    verified_at: '2026-11-23T07:07:56.772152+00:00'
  candidate:
    branch: codex/80-artifact-stack-20261123
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-23T07:11:05.249409+00:00'
    default_branch_revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    issue_state: open
    pull_request_state: not-applicable
    notes: Earlier Identity163 through166 and Aether141/142 are merged. Identity167/168 and Aether143/144
      are draft; this artifact child is prepared atop168 at83e579. Mainad8/dc3549 verified live. No source
      choice, new human review time or publication is selected.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#167
    url: https://github.com/egohygiene/identity/pull/167
  - provider: github
    id: egohygiene/identity#168
    url: https://github.com/egohygiene/identity/pull/168
  - provider: github
    id: egohygiene/aether#143
    url: https://github.com/egohygiene/aether/pull/143
  - provider: github
    id: egohygiene/aether#144
    url: https://github.com/egohygiene/aether/pull/144
review:
  status: partial
  reviewed_at: '2026-11-23T07:14:09.372744+00:00'
  reviewed_by: Codex
  evidence:
  - command: Checksum/tree-bound named derivative build and strict artifact package tests
    outcome: passed
    observed_at: '2026-11-23T07:07:56.772152+00:00'
    notes: Binarye103cd43/patch1f045f15; exact legacy and patched-minus-field6 descriptor proofs,28 top-level
      Go tests/15 MIME cases/six target negatives, one explicit existing short-mode integration skip.
  - command: Actual original reference workflow on clean frozen5afa with four original action trees
    outcome: passed
    observed_at: '2026-11-23T07:07:56.772152+00:00'
    notes: Wholejob0;424 frontend tests. Each browser9positive/one intended mutation failure/one restored
      pass. Real authenticated4,074,757-byte ZIP127fb7ed matches SDK/Finalize/download and all74 default-selected
      inputs. Source/action trees preserved.
  - command: Final integrated Python discovery after parent83e579 and platform-only cache test split
    outcome: passed
    observed_at: '2026-11-23T07:07:56.772152+00:00'
    notes: 266discovered/264passed/twoexisting skips,23.238s. Earlier11 focused controls passed on host/helper;
      final13 focused controls pass on Linux. Mac/Windows capability gates do not claim native execution.
  - command: 'Root handoff integration: documentation, bundle/extraction, exact protected/native inputs
      and retained public evidence hashes'
    outcome: passed
    observed_at: '2026-11-23T07:11:05.249409+00:00'
    notes: 190 selected native inputs equal executedd159;30 artifact evidence files match hashes. Original
      workflow/renderer/profile/PNG/assets/root source/proposal unchanged fromad8. Actual runtime cleanup
      preserves shared Docker state. Source-bound checks in docs/work/116/finish-sprint-20261123/checks.json;
      no new native run. Final affected frontend module:5passed/no skips with IDENTITY_REQUIRE_FRONTENDS=1
      and actualTask3.45.3; full266 run itself had standalone/Make only.
  environment_limitations:
  - Actual workflow source is frozen5afa; subsequent test/docs-only integration is separately checked,
    not relabeled as that workflow execution.
  - 'Original uploader omits hidden state: six.last-run files have host-receipt source hashes only. Eight
    browser logs and exact actual ZIP remain private;20 explicit nonlog members are public.'
  - The observed archive is below4MiB; no large/multiblock, hosted GitHub protection, publication or additional
    native platform claim.
  - Actual self-source choices, human creative/accessibility acceptance and remaining native-support/release/publisher/Mantle
    gates remain under existing70/98/116.
  - Pinned continuity schema/headings/budgets are structural checks, not released EgoLint conformance.
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

User/runtime and scoped instructions, live provider evidence and canonical source outrank this checkpoint. The optional local derivative supplies evidence transport under ADR0011; it does not confer creative, hosted-security or release authority.

## Resume protocol

Read AGENTS, the exact lock and LOCAL_ARTIFACT_TRANSPORT_2026-11-23. Verify main and draft167/168 before resuming. Preserve official/global act, original workflow/action pins/profile/fonts/PNG and frozen5afa receipt scope. Review parents before this artifact leaf.

## Current objective and success conditions

Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for the unchanged reference workflow.

## State snapshot

Base is updated installation draft168 at 83e57901e8a04b997860567e48e844a0a9acc514, including167. Main remains ad8fca58946ca03f6f07d13be6c64046216569d0. Candidate branch is codex/80-artifact-stack-20261123; containing revision/PR remains null before draft creation. Actual complete original workflow source is 5afa292c41563fe16f48f321eb5ac37459fda3dd; later test/docs integration retains that identity.

## Completed and material changes

The public lock/patch adds only typed MIME field6, strict ZIP compatibility and escaped emitted signature. Verifier/HMAC/target binding is unchanged. Bounded source/tool builders, actual uploader preflight and full-workflow observer/caller preserve real backend responses and independently verify the complete authenticated ZIP inventory.

## Validation and review evidence

Whole original workflow passes with424 frontend tests. Each original browser entrypoint passes9positives, observes one intended screenshot failure, then restored pass; profile/fonts/PNG unchanged. Actual4,074,757-byte ZIP127fb7ed equals SDK/Finalize/download and all74 selected file hashes. Independent peer reverified raw archive and inventory. Full final integrated Python266 completes264passes/two existing skips; focused13 pass. Go28 and exact descriptor proofs pass; one pre-existing integration skip is explicit.

## Blockers, risks, unknowns, and deferred work

The actual ZIP is below4MiB; no multiblock claim. Default hidden-file selection excludes six.last-run states, whose hashes exist only in host receipts. Exact ZIP/eight browser logs remain private;20 approved nonlog members are public. Local hardening reports self-hosted context. No new human source/creative approval, broader native support or release/publication acceptance is inferred.

## Next dependency-ready work

Review/merge167 then168 then this leaf, reconciling80/82/88 engineering gates. Keep actual native/support follow-up under70, actual self-source/release/publisher/Mantle acceptance under98, and consolidated final reconciliation116 last. Root owns issue/PR updates; do not add duplicate roadmap issues. Next engineering batch prepares actual release packaging/matrix data before final source/native/release acceptance.

## Parallel changes and reconciliation

Parent168 now83e579 adds test-only POSIX/symlink capability handling and docs after c27. This leaf preserves frozen5afa workflow evidence and merges that updated parent; final Python suite covers the combination. Aether143→144 owns its independent portable-skill stack. The consolidated116 handoff records both stacks and the remaining issue order. Earlier timestamp/native/consumer receipts keep their original exact inputs.

## Privacy and redaction

Public source identities/hashes and bounded results only. Tokens, signed URLs, proxy values, private paths and raw archives/logs remain task-local. Public browser projection uses only explicit reviewed JSON/PNG/Markdown/trace members, rehashed against the actual ZIP and host receipts; no general extraction or broad log publication.

## Handoff update protocol

Refresh after actual domain checks, review the diff and validate pinned schema/twelve headings/budgets. Reference ADR0011 for the optional local adapter; routine test/docs fixes need no new ADR. Pinned Aether decision2.1.0/continuity1.1.0 remain selected without lifecycle promotion. Preserve tested source5afa and private-retention boundaries.

## Compaction and supersession

Git and exact work packets retain earlier observations. Replace stale current-state prose rather than append chronology; preserve source, human approval and release boundaries.
