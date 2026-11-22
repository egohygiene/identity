---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T19:08:19.581987+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify the original Docker browser route and unchanged local workflow through explicit verified action sources and managed-network trust.
  includes:
  - Prepare full-commit archive and Git-tree verified local action mirrors without workflow edits.
  - Retain exact matching-source direct, local-act-ci and default-entrypoint browser proof.
  - Separate original browser step success from the actual local artifact-server failure.
  excludes:
  - GitHub-hosted CI, paid services, publication, tags/releases, baseline changes and new creative approval.
  - Canonical self-source adoption, full native/platform acceptance and other repository writes.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - dev/browser/profile.json
  - .github/workflows/reference-renderer.yml
  - dev/local-actions/reference-renderer.lock.json
  - docs/LOCAL_WORKFLOW_REPLAY.md
  - docs/work/80/ACTION_REPLAY_2026-11-22.md
  - docs/work/80/action-replay-2026-11-22/qualification-summary.json
  - https://github.com/egohygiene/identity/issues/80
  - https://github.com/egohygiene/identity/issues/88
work:
  objective: Establish original matching-source local Docker and actual workflow browser proof while retaining exact local transport failures.
  success_conditions:
  - Keep profile/image/font/baseline/workflow pins unchanged and preserve truthful caller contexts.
  - Run nine positives, deliberate screenshot failure and restored pass from direct and both original workflow browser steps.
  - Retain complete artifact hashes and actual whole-workflow exit without claiming hosted CI or artifact publication.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: review-original-browser-proof-and-artifact-transport
    description: 'Review the three exact a56399b browser passes for #80/#88 and reconcile the draft stack; repair local act artifact MIME protocol separately before claiming whole-workflow green.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/88
    - https://github.com/egohygiene/identity/issues/70
    depends_on: []
state:
  base:
    revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    ref: refs/heads/main
    verified_at: '2026-11-22T19:03:09Z'
  candidate:
    branch: codex/80-pinned-action-replay-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T19:03:09Z'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Provider main remains75ca39f; #80 is open. Parallel approval-timestamp PR163 is draft; this domain branch has no PR yet. No merge, hosted dispatch, release or deployment was performed by this checkpoint.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#163
    url: https://github.com/egohygiene/identity/pull/163
review:
  status: partial
  reviewed_at: '2026-11-22T19:08:19.581987+00:00'
  reviewed_by: Codex
  evidence:
  - command: Offline exact archive preparation and actual act --strict --dryrun with four explicit local repositories
    outcome: passed
    observed_at: '2026-11-22T19:06:52.147364+00:00'
    notes: All four archive SHA256/size and complete reconstructed Git trees match reviewed full-commit locks. Dry-run proves acquisition/planning only; actual action execution is separately retained.
  - command: Focused Python browser and local-action boundary suites; independent read-only source review
    outcome: passed
    observed_at: '2026-11-22T19:06:52.147364+00:00'
    notes: 22 tests pass. Actual Git tree calculation, hostile archives, pin/workflow drift, budgets and duplicate JSON are rejected. CA CLI precedence and generic path errors cover missing/directory/loops, commas/quotes/all ASCII controls and alias targets.
  - command: Original direct Docker plus unchanged reference-renderer workflow CI/default-local browser steps
    outcome: passed
    observed_at: '2026-11-22T18:57:35.045Z'
    notes: All three at clean a56399b33548cab075e4442e64605035bccd973f, same 423-file inventory 07bb513d..., nativeamd64 overlay2; each 9 positives → 1 intended failure → 1 restored pass, 0 skips/retries. Three host receipts and 48 raw artifacts retain exact hashes; PNG/tolerance unchanged.
  - command: Actual original reference-renderer workflow through act0.2.97 host executor in disposable helper
    outcome: limited
    observed_at: '2026-11-22T19:06:52.147364+00:00'
    notes: 51 source parses, 424 Vitest passes, build/public validation and both browser steps pass; whole job exits 1 after 206.755s because local act artifact server rejects unchanged uploader CreateArtifact mime_type. Original hardening pre/main/post execute self-hosted; no hosted-security or publication claim.
  - command: Retained evidence hashes, protected-source comparison, documentation/compile/whitespace and pinned continuity schema/headings/budgets
    outcome: passed
    observed_at: '2026-11-22T19:08:19.581987+00:00'
    notes: 66 retained files hashed; all 48 raw artifact hashes and three 20-file critical-input sets match. Workflow/profile/renderer/assets/contracts/ADR bytes equal 75ca39f. Metadata has 12 headings within 16384 bytes/240 lines; no released EgoLint conformance claim.
  environment_limitations:
  - Local act is not GitHub-hosted CI; the whole local job remains failed at artifact transport despite passing product/browser steps.
  - Only recorded native Linux/amd64 original image/profile is qualified; no other platform, release, human visual approval or source adoption follows.
  - The exact represented source is a56399b; later unrelated integration is not relabeled as an actual run.
  - Official released EgoLint continuity conformance is not claimed; pinned metadata, headings and budgets are narrower checks.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions:
  - Private task paths, proxy values and disposable local correlation identifiers in workflow logs; raw/sanitized hashes remain distinct.
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

This handoff follows user/runtime instructions, scoped instructions, live state and canonical source. It records exact browser engineering proof without approving brand source or release policy.

## Resume protocol

Read AGENTS, ADR-0011, the browser profile and ACTION_REPLAY_2026-11-22.md. Recheck main/issues/PRs before continuing. Older #80 diagnostics and merged #158–162 receipts keep their historical sources and limits.

## Current objective and success conditions

Verify original local Docker and both original workflow browser paths from one exact clean source, with unchanged baseline/tolerance, bounded local acquisition and explicit trust configuration. Keep the full workflow result honest.

## State snapshot

Base/live main is 75ca39f. Domain branch is codex/80-pinned-action-replay-20261122; its containing revision/PR are intentionally null. The represented qualified source is a56399b33548cab075e4442e64605035bccd973f, not a later integration revision. Parallel PR163 remains draft.

## Completed and material changes

A bounded first-party helper prepares four exact pinned public action mirrors, binding archive SHA256/size and reconstructed Git trees to reviewed workflow bytes. Optional IDENTITY_BROWSER_PROXY_CA uses the existing build-secret transport; explicit CLI wins and unset/empty behavior is unchanged. Invalid CA selectors fail before Docker without leaking paths. No workflow/action/profile/font/PNG/tolerance/ADR is changed.

## Validation and review evidence

Three complete actual original-Docker runs at clean a56399b share the 423-file 07bb513d... inventory: direct local-host, original local-act-ci and original local-act-local-entrypoint-replay. Each passes 9 positives, intentionally fails the visual mutation and restores 1 pass, with 0 skips/retries. Three raw host receipts bind 48 artifacts, runtime/fonts/settings and unchanged PNG 53d7d144.... The original workflow also passes 51 source parses, 424 Vitest tests and build/public validation. Focused Python22 tests and independent review pass. Detailed hashes/receipts are in the domain packet.

The full actual act job exits 1 at the unchanged uploader's local-server MIME protocol. Pre/main/post hardening run as self-hosted; default act local checkout uses no GitHub secret. This is not hosted hardening, hosted CI or published artifact evidence. Pinned Aether decision 2.1.0 and continuity 1.1.0 guides at dc8a168 were read; Hygiene policy 1.2.0 remains referenced.

## Blockers, risks, unknowns, and deferred work

Local act's artifact server rejects CreateArtifact mime_type; repair/upgrade that local protocol before reporting whole-workflow green. Other native/platform, source approval, contrast/manual design, distribution and release gates remain separate. Prior owner choices and unresolved #98 source/governance facts are preserved unchanged.

## Next dependency-ready work

Review exact #80/#88 browser evidence and reconcile the draft checkpoint. Continue independently owned #82 engineering qualification and #70 closure; #116 remains the final aggregate. Do not promote matrix rows or issue acceptance solely from merged preparation.

## Parallel changes and reconciliation

Parent owns timestamp PR163, the isolated runtime recipe, development qualification and final stack publication. Reconcile continuity semantically; retain the exact qualified a563 source and separate passed browser steps from failed artifact transport. Only owned nested Docker resources were cleaned after heavy-slot release; unrelated global state was preserved.

## Privacy and redaction

Retain public source/pin facts and exact raw browser proof. Workflow logs redact private task paths, proxy values and disposable correlation identifiers and distinguish raw/sanitized hashes. The private local replay envfile and unused temporary cache marker were removed. No private transcript, credentials or personal paths are committed.

## Handoff update protocol

Refresh after checks/provider reads and before the parent draft handoff. Validate pinned metadata, twelve headings and 16384-byte/240-line budgets. Decision impact: reference accepted ADR-0011; local acquisition/trust transports preserve its existing contract, without a new ADR, approval or lifecycle change.

## Compaction and supersession

Git, issues and date-scoped domain receipts retain detail. Preserve the exact source/caller/native contexts and known upload failure on compaction; do not replace the old source records with a later merged-head claim.
