---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T07:01:45.401764+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Repair browser qualification evidence/preparation boundaries and retain exact failed workflow
    and separate successful derived-runtime diagnostics.
  includes:
  - Keep local act receipts distinct from GitHub-hosted evidence.
  - Refuse inadequately observable/budgeted Docker stores before acquisition and reserve a bounded failure
    receipt.
  - Retain actual failed original-route/workflow observations and separate exact browser diagnostics without
    changing the original qualified gate.
  excludes:
  - Profile/font/runtime-version, screenshot, tolerance, creative-source, approval or release changes.
  - Hosted workflow dispatch, publication, deployment or issue closure.
  - Claiming derived rootfs evidence is original Docker-image or hosted CI acceptance.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/BROWSER_ENVIRONMENT.md
  - dev/browser/profile.json
  - scripts/qualify_browser.py
  - tests/test_qualify_browser.py
  - .github/workflows/reference-renderer.yml
  - docs/work/80/BROWSER_CHECKPOINT_2026-11-22.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - docs/decisions/policy-reference.json
  - https://github.com/egohygiene/identity/issues/80
  - https://github.com/egohygiene/identity/issues/70
work:
  objective: Repair browser qualification evidence/preparation boundaries and retain exact failed workflow
    and separate successful derived-runtime diagnostics.
  success_conditions:
  - Never label local act as GitHub-hosted CI.
  - Stop remote/unobservable or known-small Docker preparation without image acquisition and retain bounded
    failure evidence.
  - 'Preserve the approved screenshot and all exact profile/font pins; keep original #80 acceptance open.'
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: qualify-original-browser-workflow
    description: Run the unchanged qualified Docker workflow on adequate observable storage with supported
      acquisition of the exact pinned actions, then record current-source CI/local-entrypoint acceptance.
    readiness: blocked
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/70
    depends_on: []
state:
  base:
    revision: ca7f836234301c276de0136bd7bec80724d3b4c9
    ref: refs/heads/codex/70-engineering-baseline-20261122
    verified_at: '2026-11-22T07:01:45.401764+00:00'
  candidate:
    branch: codex/80-browser-stack-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T07:01:45.401764+00:00'
    default_branch_revision: ec8fce30c3c96c7781238eb0a8899d6f0cee0a40
    issue_state: open
    pull_request_state: not-applicable
    notes: Merged main remains ec8fce3; six finish issues remain open. Earlier155/156/157 and Aether139
      are merged. Parent draft PRs 158 are open; this next child PR does not yet exist. No overnight sprint
      PR is merged or published.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#158
    url: https://github.com/egohygiene/identity/pull/158
review:
  status: partial
  reviewed_at: '2026-11-22T07:00:22.289471+00:00'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern test_qualify_browser.py --verbose
    outcome: passed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: Nine boundary cases pass, including real failure-receipt serialization, ACT context, reserved
      writes and remote-context/coincident-path refusal.
  - command: Actual original Docker qualifier and storage-refusal experiment
    outcome: failed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: Initial VFS/BuildKit preparation exhausted shared storage; repaired route retained a valid
      refusal before acquisition. These are not browser passes.
  - command: Actual reference-renderer.yml validate job through local act 0.2.97
    outcome: failed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: Cached immutable runner starts; GoGit action acquisition fails before workflow steps. No browser
      or artifact step executes; container cleanup completes.
  - command: Existing browser qualifier in separately derived pinned OCI rootfs
    outcome: passed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: 'At clean source 57704ae: nine positives, deliberate comparison failure, restored pass, zero
      skips/retries; exact fonts/runtime/profile and all 684 copied source files verified. This is local
      diagnostic scope only.'
  - command: Independent source/evidence review
    outcome: passed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: Initial remote-endpoint blocker corrected and independently cleared; no remaining blocker reported.
      Original receipts retain actual source identity.
  - command: Documentation links, pinned continuity schema/headings/budget, evidence SHA256 inventory
      and protected-byte checks
    outcome: passed
    observed_at: '2026-11-22T07:00:22.289471+00:00'
    notes: All retained artifact hashes and12headings validate within16384bytes/240lines; profile, baseline,
      assertions, Dockerfile and every ADR record remain unchanged.
  environment_limitations:
  - Original qualified Docker workflow/current-source CI acceptance remains open; local derived-rootfs
    success is narrower evidence.
  - Shared VFS store was below preparation budget and ordinary act could not acquire a pinned public action
    through GoGit.
  - Official released EgoLint continuity conformance is not claimed; pinned schema/headings/budget checks
    are separate.
  - '#70/#82/#88/#98/#116 retain their own full acceptance, real source facts and release/adoption requirements.'
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions:
  - Private local paths and proxy values excluded from retained public evidence.
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

This compact checkpoint remains below user/runtime instructions, scoped instructions, live state and canonical contracts. It records a local browser-evidence repair candidate, not completion of Identity or its CI gate.

## Resume protocol

Read AGENTS, the browser guide, profile, qualifier and issue 80 checkpoint. Re-query main/open PRs before stacking. Preserve exact source identities in historical and new receipts rather than relabeling them as integrated-head evidence.

## Current objective and success conditions

Report local act truthfully, stop known-small or unobservable Docker storage before acquisition, retain bounded failure records and keep diagnostic browser evidence distinct from the original workflow acceptance.

## State snapshot

Stack base is `codex/70-engineering-baseline-20261122` at `ca7f836234301c276de0136bd7bec80724d3b4c9`. Candidate `codex/80-browser-stack-20261122` is a draft child with no containing-revision or pre-PR self-reference. Domain receipts retain their exact independently represented source; stacking does not relabel earlier runs as tests of later code. Live main remains `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`.

## Completed and material changes

qualify_browser.py distinguishes ACT from GitHub-hosted invocations, checks the selected local Unix daemon and driver budget before pulling, and reuses a 1-MiB reserved failure record. The tests cover actual receipt emission and remote-context precedence. docs/work/80 retains failed Docker/workflow observations and separate successful derived-OCI browser evidence, including actual/diff/expected screenshots and trace. The original profile, fonts, baseline, tolerance and ADR disposition remain unchanged.

## Validation and review evidence

Nine focused Python cases pass. The actual production workflow act attempt fails acquiring its pinned hardener before steps; the ordinary Docker route does not qualify. A bounded flattened OCI rootfs passes 9 positive cases, rejects deliberate screenshot drift and passes the restored assertion at source 57704ae, with zero skips/retries. Its raw receipt passes the existing strict verifier; all 684 copied source files remain exact. Independent review cleared the endpoint blocker. Detailed results and hashes live in the scoped checkpoint, not this handoff.

## Blockers, risks, unknowns, and deferred work

#80 still needs the original qualified workflow on adequate observable storage and successful exact-pin action acquisition. A local derived rootfs is not Docker-image equivalence, production-workflow success or hosted CI. No baseline/tolerance relaxation or new approval is permitted. Other engineering/self-source/release gates retain their owners.

## Next dependency-ready work

The original workflow replay is blocked by current storage/acquisition conditions. Prepare a suitable qualified runner without changing profile identity, then retain current-source CI and local-entrypoint proof. The parent may stack this bounded repair while keeping #80 open and reconciling #70/#82/#88 evidence.

## Parallel changes and reconciliation

This checkpoint follows parent draft PRs #158. Review/merge parents before children and reconcile continuity semantically. The engineering parent owns tag admission, copied-executable isolation and portable policy references; each domain checkpoint retains its own actual qualification limits. All sprint branches remain for maintainer review.

## Privacy and redaction

Only public source/profile metadata and sanitized evidence are retained. Private paths, proxy values, credentials and unrelated context are excluded. No Git credentials were forwarded to the workflow/derived runtime.

## Handoff update protocol

Apply pinned Aether decision guidance 2.1.0 and continuity 1.1.0 read via exact Git objects at dc8a16851f452763ef4f7fbe4bf057d4500b1921. Validate the metadata schema, twelve headings and byte/line budgets after domain checks. ADR-Ref: egohygiene/identity#ADR-0011 (reference); no decision disposition, release contract or creative boundary changes.

## Compaction and supersession

Git and issue 80 retain detailed history. Keep this snapshot compact, preserve raw observations and approved assets, and never promote missing/failed CI evidence into a pass.
