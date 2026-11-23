---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-23T06:51:48.946312+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for the unchanged
    reference workflow.
  includes:
  - Pinned public source/toolchain/sender schema and strict ZIP-only local act derivative, with upstream/global
    tools unchanged.
  - Actual exact-pinned uploader preflight, full archive hash/inventory and original workflow replay on the
    combined timestamp/install source candidate.
  - Strict MIME/protobuf and signed-target negatives; bounded owned-process observation with tokens and signed
    URLs excluded.
  excludes:
  - No hosted GitHub CI equivalence, security bypass, publication, release signing or platform-matrix promotion.
  - No creative/source approval, original workflow/action/profile/font/PNG changes, consumer pin changes or
    global installation.
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
work:
  objective: Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for the
    unchanged reference workflow.
  success_conditions:
  - Require exact typed field six, legacy descriptor equivalence, ZIP-only MIME and unchanged signed-target
    authentication.
  - Require actual pinned uploader upload/download/SHA256 and complete expected ZIP inventory; retain historical
    failures separately.
  - Require whole unchanged workflow exit zero plus actual full archive integrity on a frozen combined source;
    preserve hosted/creative/release boundaries.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: freeze-combined-source-and-run-original-workflow
    description: Review the bounded observer/caller, freeze the combined167/168/artifact code and execute
      the full original workflow on the measured owned runtime; retain actual full archive proof.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/70
    depends_on: []
state:
  base:
    revision: c27ebc1a53220a629994939ef81f88e44e8b5752
    ref: refs/heads/codex/70-local-install-stack-20261123
    verified_at: '2026-11-23T06:51:48.946312+00:00'
  candidate:
    branch: codex/80-artifact-transport-20261123
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-11-23T06:51:48.946312+00:00'
    default_branch_revision: ad8fca58946ca03f6f07d13be6c64046216569d0
    issue_state: open
    pull_request_state: not-applicable
    notes: Mainad8 is merged through166. Timestamp167 and its installation child168 are draft; this artifact
      child includes c27 and has no PR yet. No full original-workflow pass is inferred from the successful
      small actual sender fixture.
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
review:
  status: partial
  reviewed_at: '2026-11-23T06:51:48.946312+00:00'
  reviewed_by: Codex
  evidence:
  - command: Checksum/tree-bound Go builder; legacy and patched-minus-field6 descriptor proofs; artifact package
      tests
    outcome: passed
    observed_at: '2026-11-23T06:51:48.946312+00:00'
    notes: Actual named v2 derivative e103cd43; 28 top-level Go tests pass,15 MIME cases/six signed-binding
      negatives; one existing Docker integration test skipped by short mode.
  - command: Actual final exact-pinned uploader fixture and authenticated signed archive download
    outcome: passed
    observed_at: '2026-11-23T06:51:48.946312+00:00'
    notes: Act exit0;334-byte actual ZIP digest043bd208 equals uploader and independent download, complete
      two-file inventory matches, original input/action bytes preserved.
  - command: Focused Python transport/observer boundary tests and syntax/whitespace checks
    outcome: passed
    observed_at: '2026-11-23T06:51:48.946312+00:00'
    notes: 11 methods pass, including real loopback replies, inventory/digest rejection, descriptor delta,
      threaded owned Node descendant capture and ambient act configuration refusal.
  environment_limitations:
  - The complete unchanged original workflow has not yet been rerun with this frozen combined candidate; full
    artifact and browser evidence are pending.
  - The derivative is explicit task-local Linuxamd64 engineering, not an official act release or publisher-authenticated
    build.
  - Existing hosted security limitations, actual self-source choices, human creative review and native release/publication
    acceptance remain separate.
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

Read AGENTS, the exact lock and LOCAL_ARTIFACT_TRANSPORT. Verify main and draft167/168 before resuming. Preserve official/global act and the original workflow, all action pins, profile/fonts and approved PNG. Use the exact reviewed derivative hash and new private evidence directories.

## Current objective and success conditions

Qualify strict task-local artifact compatibility and authenticated real ZIP integrity for the unchanged reference workflow.

## State snapshot

Base is installation draft168 at c27ebc1a53220a629994939ef81f88e44e8b5752, including timestamp167. Main remains ad8fca58946ca03f6f07d13be6c64046216569d0. This containing code revision/PR is null until committed. Full original-workflow qualification is pending.

## Completed and material changes

The public lock/patch restores the exact upstream schema then adds only typed MIME field6 and a strict ZIP guard. The emitted padded signature is URL-escaped; verifier/HMAC/target binding is unchanged. Bounded source/tool builders, real sender preflight and full-workflow observer/caller preserve actual backend replies and independently check authenticated ZIP inventory.

## Validation and review evidence

Reviewed Go production patch1f045f15 and descriptor proofs pass. Actual binary e103cd43 reports0.2.98+identity.zipmime.2;28top-level tests pass with15MIME cases/six target negatives and one explicit existing integration skip. Final actual sender fixture exits0, uploads/downloads334bytes, matches digest043bd208 and both exact file hashes. Eleven Python controls pass including threaded-process ownership and ambient configuration refusal. Full workflow remains pending.

## Blockers, risks, unknowns, and deferred work

The tiny ZIP fixture does not prove the complete original workflow or multiblock artifacts. The owned runtime must expose actual measured storage and final clean source. Full observer success is required independently of backend200; inability to identify the actual owned uploader fails proof. No hosted CI, new source/creative approval or release claim is inferred.

## Next dependency-ready work

Freeze the combined code, run the unchanged workflow on the prepared owned runtime and retain actual full upload/finalization/download/archive SHA plus complete inventory and source-bound browser packets. Reconcile existing70/80/88; actual source/release gates stay under70/98, with116 last.

## Parallel changes and reconciliation

Review167 then168 then this artifact child. Aether143 owns portable-skill changes. Preserve exact prior timestamp/install/native/consumer receipts and historical official/v1 failures; evidence from a different source is not relabeled as the current candidate.

## Privacy and redaction

Public source identities, hashes and bounded outcomes only. Runtime tokens, signed URLs, proxy values, private paths and raw archives/logs remain task-local. The observer reads only bounded PID/PPID metadata globally, then command/environment/cwd only for the exact launched act descendants and owned pinned Node uploader.

## Handoff update protocol

Refresh after actual domain checks, review the diff and validate pinned schema/twelve headings/budgets. Reference ADR0011 for the optional local evidence adapter; ADR not required for routine caller/tests. Pinned Aether decision2.1.0/continuity1.1.0 remain selected without lifecycle promotion.

## Compaction and supersession

Git and exact work packets retain earlier observations. Replace stale current-state prose rather than append chronology; preserve source, human approval and release boundaries.
