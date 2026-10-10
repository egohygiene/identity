---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-10T17:12:27Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Republish the verified Identity Decisions canary with the merged shared filtering fix, then review live visibility and maintainer
    feedback before fleet rollout.
  includes:
  - Merged publication source, separate local/provider/live evidence, rollback capture and next owner actions.
  excludes:
  - Conversation transcripts, duplicated architecture and raw workflow logs.
  - Unrelated release or visual approval, organization experience publication and fleet rollout.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ARCHITECTURE.md
  - SYSTEM.md
  - ROADMAP.md
  - docs/decisions/README.md
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-022-decisions-publication-composition.md
  - docs/decision-ratification-2026-10-10.md
  - docs/decision-validation.md
  - docs/publication/IDENTITY_PAGES.md
  - .github/workflows/publish-brand-kit.yml
  - scripts/identity_decisions_publication.py
  - publication/decisions-rollback.json
  - docs/evidence/identity-adrs-ratified-2026-10-10.json
  - https://github.com/egohygiene/identity/issues/69
  - https://github.com/egohygiene/relay/issues/115
  - https://github.com/egohygiene/.github/issues/30
  - https://github.com/egohygiene/pace/issues/25
  - https://github.com/egohygiene/identity/pull/93
  - https://github.com/egohygiene/identity/actions/runs/38067442472
  - docs/evidence/identity-decisions-deployment-2026-10-10.json
  - https://github.com/egohygiene/relay/issues/139
  - https://github.com/egohygiene/relay/pull/141
  - https://github.com/egohygiene/identity/pull/94
work:
  objective: Adopt the merged Relay filtering repair, verify the republished canary and obtain maintainer feedback before fleet rollout.
  success_conditions:
  - Preserve the existing 21 accepted ADR dispositions and proposed ADR-022; no lifecycle promotion is implied by deployment.
  - Adopt Relay 2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0 and rebuild through the existing publisher without changing its authority.
  - Reverify source-bound artifacts, all live files and the preserved 40-file Brand Kit after the fix.
  - Obtain maintainer feedback on the working Decisions page before repository-by-repository fleet rollout.
  active_issue:
    provider: github
    id: egohygiene/identity#69
    url: https://github.com/egohygiene/identity/issues/69
  next:
    kind: issue
    id: egohygiene/identity#69
    description: Review and merge the exact Relay pin update, republish Identity, then verify browser query/facet/reset/no-match visibility and
      live bytes before pilot closeout.
    readiness: ready
    references:
    - https://github.com/egohygiene/relay/issues/139
    - https://github.com/egohygiene/identity/issues/69
    - https://identity.egohygiene.io/decisions/
    depends_on: []
state:
  base:
    revision: 0935c89ba2f85b985ee330b08ecf73059cc12bb5
    ref: refs/heads/main
    verified_at: '2026-10-10T17:10:17Z'
  candidate:
    branch: codex/identity-69-relay-filtering
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-10T17:10:17Z'
    default_branch_revision: 0935c89ba2f85b985ee330b08ecf73059cc12bb5
    issue_state: open
    pull_request_state: not-applicable
    notes: 'PR #94 merged the first deployment receipt at main 0935c89ba2f85b985ee330b08ecf73059cc12bb5. Deployed source remains
      e6bafa362de900fdcffac60c33b8bed2c3905115 from successful run 38067442472. Relay PR #141 merged its filtering repair at
      2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0; this consumer pin candidate is not deployed. Identity #69 and Relay #139 remain open.'
  parallel_changes:
  - provider: github
    id: egohygiene/relay#139
    url: https://github.com/egohygiene/relay/issues/139
review:
  status: partial
  reviewed_at: '2026-10-10T17:12:27Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub GET PR #93, branches/main, Identity #69 and final-head Actions runs'
    outcome: passed
    observed_at: '2026-10-10T16:25:27Z'
    notes: Merge e6bafa362de900fdcffac60c33b8bed2c3905115 from reviewed head 3a77088c88cf71456eea5553252d775d14013b7f verified. Decision 38067095170,
      renderer 38067094641, CLI 38067094651 and release 38067094596 completed successfully.
  - command: 'Inspect PR #93 consumer tests, fresh rollback capture and publication/decisions-rollback.json'
    outcome: passed
    observed_at: '2026-10-10T16:25:27Z'
    notes: 17 focused tests passed, including simulated symlinked temporary root. Fresh rollback capture verified all 40 files and repeated archive
      digest d886c103ec8e47bad78cd75243c2b6b339734919e6415a41cb7cb93b0f65e9fe. Existing stable-release build matched all 40 prior live files.
  - command: GitHub GET Pages run 38067442472; inspect docs/evidence/identity-decisions-deployment-2026-10-10.json
    outcome: passed
    observed_at: '2026-10-10T16:31:34Z'
    notes: Hosted run completed successfully at source e6bafa362de900fdcffac60c33b8bed2c3905115 with Relay cabbf5b3b658d585b4d56ef0c99917969a96eed2.
      All 60 live files passed first attempt at 16:24:55Z; 40 original Brand Kit files remain byte-preserved.
  - command: Inspect independently downloaded publication handoff 11675331641 and deployment evidence 11676205317 results in the bounded receipt
    outcome: passed
    observed_at: '2026-10-10T16:31:34Z'
    notes: Both ordinary ZIP digests matched provider metadata. All 60 file bindings, Intelligence manifest files and 40-file rollback archive/inventory
      verified. Retained ordinary artifacts expire 2026-11-09; the one-day github-pages ZIP was not independently downloaded.
  - command: 'Read actual browser review in the deployment receipt and GET Relay #139'
    outcome: limited
    observed_at: '2026-10-10T16:31:34Z'
    notes: /decisions/ resolves to /intelligence/decisions/ with 22 records (21 accepted, one proposed). Search count changes but nonmatching
      cards remain visible because shared CSS overrides hidden semantics. Partial browser review only; no complete accessibility or maintainer
      acceptance claim.
  - command: Git ls-remote Identity main; GitHub GET Relay PR 141, Identity 69 and Relay 139
    outcome: passed
    observed_at: '2026-10-10T17:10:17Z'
    notes: Identity main is 0935c89ba2f85b985ee330b08ecf73059cc12bb5. Relay PR 141 merged at 2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0
      from reviewed head 5844a36a1a9f394d2d814ce05599ea68c5868df9. Both owning issues are open; the prior live receipt is unchanged.
  - command: Read Relay PR 141 validation report and browser limitation
    outcome: limited
    observed_at: '2026-10-10T17:10:17Z'
    notes: Owner reports 34 focused site tests and catalog/continuity checks passed with independent review. Generated browser fixture execution
      was blocked by local-file browser policy. Both hosted checks were running at merge; continuity 38070582632 later passed. Validation
      38070582605 attempt 1 failed during unchanged Rust 1.85.1 acquisition after base tests passed; the owner requested a failed-jobs retry,
      now in progress. No new live browser success is claimed.

  - command: Focused consumer publication, docs, pin-only workflow comparison and continuity structural checks
    outcome: passed
    observed_at: '2026-10-10T17:12:27Z'
    notes: All 17 publication tests, documentation links and publication architecture/release-config verification passed. Workflow changes are
      exactly nine immutable pin replacements; schema, twelve headings, size, relative links and diff checks passed. No new native build or
      deployment was run for this candidate; official released continuity conformance is not inferred.
  environment_limitations:
  - 'Relay #139 remains open pending the repaired consumer deployment and actual browser visibility checks; source repair alone is not live proof.'
  - Browser inspection is partial; complete accessibility and fleet readiness are not established. Maintainer feedback is pending.
  - Only Decisions has complete/current collected coverage; the other eight evidence domains remain uncollected.
  - Ordinary retained artifacts expire 2026-11-09; rollback was freshly captured and verified but not re-promoted. The expired historical original
    Pages ZIP was not recovered.
  - ADR-022 remains proposed; merge and deployment do not provide separate human disposition.
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

Canonical ADRs, pinned Hygiene policy, live Git state and owning issues take precedence. Continue from [Identity #69](https://github.com/egohygiene/identity/issues/69) and [organization #30](https://github.com/egohygiene/.github/issues/30).

## Resume protocol

1. Read AGENTS.md, branch/status/history and canonical publication sources.
2. Refresh main, Identity #69 and [Relay #139](https://github.com/egohygiene/relay/issues/139).
3. Read the [bounded deployment receipt](docs/evidence/identity-decisions-deployment-2026-10-10.json), including exact artifact digests, source bindings, retention and browser limits.
4. Adopt merged Relay PR #141, republish through the existing owner and verify actual visibility before pilot closeout and fleet work.

## Current objective and success conditions

The first Decisions canary is live with verified source and byte integrity. Relay PR #141 repairs the shared filtering defect. This candidate adopts its exact merged revision; deployment, live byte checks, renewed browser visibility checks and maintainer feedback remain pending. Identity #69 stays open until pilot closeout; deployment success does not imply whole-repository conformance.

## State snapshot

Main/base is `0935c89ba2f85b985ee330b08ecf73059cc12bb5` after [PR #94](https://github.com/egohygiene/identity/pull/94). Deployed source remains `e6bafa362de900fdcffac60c33b8bed2c3905115` from [Pages run 38067442472](https://github.com/egohygiene/identity/actions/runs/38067442472). [Relay PR #141](https://github.com/egohygiene/relay/pull/141) merged at `2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0`. Consumer branch `codex/identity-69-relay-filtering` changes publication pins and current guides; self-SHA and PR remain null. The prior 21 ADRs retain [R1 approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806); [ADR-022](docs/decisions/ADR-022-decisions-publication-composition.md) stays proposed.

## Completed and material changes

- The existing single Pages publisher at `identity.egohygiene.io` composes Relay output at `renderer/dist/intelligence`; `/decisions/` aliases `/intelligence/decisions/`.
- All 60 live files passed verification: 40 unchanged Brand Kit files, 19 Intelligence files and one alias. The organization `/identity/` experience retains its owner.
- Publisher and Decisions source are `e6bafa362de900fdcffac60c33b8bed2c3905115`; the Brand Kit separately binds stable `v1.0.0` commit `aaad8839104704cf57bfa846539b3b875421e03d`.
- Candidate publication actions and provenance bind `2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0`; the first deployment retains `cabbf5b3b658d585b4d56ef0c99917969a96eed2`. Advisory validation and historical build/rollback-helper provenance retain `4137cb07a017b7bbae2ee38fe9b039c58b0b17eb`.
- The unchanged first-deployment receipt records actual deployment, independent ordinary-artifact downloads, rollback capture, live checks and the observed browser defect.
- Pinned Aether authoring 2.0.0 and continuity 1.1.0 were loaded directly from `8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2`; no host installation is claimed.

## Validation and review evidence

The [deployment receipt](docs/evidence/identity-decisions-deployment-2026-10-10.json) binds actual merged source and successful Pages execution. At `2026-10-10T16:24:55.773202Z`, all 60 live files matched on the first attempt. Independently downloaded handoff artifact `11675331641` and evidence artifact `11676205317` ZIP digests matched provider metadata; all source/file bindings and all 40 rollback files verified. The page projects 22 records (21 accepted, one proposed), with implementation declarations 12 implemented, 8 in progress, 2 not started and none verified. Four final-head CI workflows passed; earlier local integration at `a57e8e4b` remains separately bound evidence. The browser followed the alias and rendered records, but filtering left nonmatching cards visible. The earlier structural review belongs to that checkpoint. Relay reports 34 focused tests and independent review for its merged repair; its local browser fixture was not executed because of browser URL policy. Hosted owner checks were in progress at merge; continuity then passed, while native validation needed an acquisition retry. The candidate's 17 focused publication tests, docs/contracts and pin-only/continuity structural checks pass; it has no new deployment or live browser result.

## Blockers, risks, unknowns, and deferred work

[Relay #139](https://github.com/egohygiene/relay/issues/139) remains open until the merged shared stylesheet fix is consumed and verified in the deployed browser. Verify actual visible cards and headings, not only hidden properties or reported counts. No generated Identity output is patched. No full accessibility or fleet-readiness claim is made. Only Decisions is collected/current; eight other evidence domains remain uncollected. Ordinary artifacts expire 2026-11-09. Rollback bytes are a fresh verified capture, not the expired original ZIP; rollback re-promotion was not exercised. ADR-022 needs a separate human disposition.

## Next dependency-ready work

Review this exact consumer pin change, rebuild through Identity's existing publisher, verify query/facet/reset/no-match visibility and repeat live byte checks. Show [the live Decisions page](https://identity.egohygiene.io/decisions/) for maintainer feedback before fleet rollout. Keep Identity #69 open for this review. Relay #115's completed collector handoff and closure are separately reconciled by [Relay PR #140](https://github.com/egohygiene/relay/pull/140) and its owning tracker.

## Parallel changes and reconciliation

This isolated consumer branch updates only nine workflow pin/provenance values, two current guides and continuity. Events, permissions, routes, deployment ownership, Brand Kit inputs, ADRs, rollback capture and earlier receipts are unchanged. Decision-impact result: reference proposed ADR-022; this routine owner fix creates no new architecture or lifecycle disposition. Relay owns the shared filtering fix. The five PR #90 coordination updates are applied; Identity #83 retains broader roadmap/publication-document reconciliation.

## Privacy and redaction

Retain public source links and concise evidence only. Exclude private context, credentials, local paths and raw logs. The checkpoint grants no new authority.

## Handoff update protocol

After the shared fix, update exact source, artifact and live results without rewriting the first deployment receipt. Leave a containing commit's own SHA null. Keep provider deployment, byte verification, browser behavior, recovery availability, human disposition and maintainer feedback distinct.

## Compaction and supersession

Keep below 240 lines and 16,384 UTF-8 bytes. Replace stale observations; Git and work trackers retain history. Mark unresolved conflicts stale.
