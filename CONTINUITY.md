---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-10T16:13:42Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Resume consumer-owned Identity Decisions publication after merged PR #92, preserving the stable Brand Kit and obtaining live maintainer
    feedback before fleet rollout.'
  includes:
  - Single-publisher composition, immutable evidence boundaries, rollback capture, proposed ADR-022 and next owner actions.
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
work:
  objective: Publish freshly validated Decisions beneath the existing Identity Brand Kit publisher, verify the deployed bytes, and obtain maintainer
    feedback before fleet rollout.
  success_conditions:
  - Preserve the 21 accepted ADRs and explicit approval; ADR-022 stays proposed without a human disposition.
  - Retain the original 40 Brand Kit files byte-for-byte and freshly verify the rollback capture before deployment.
  - Bind publisher, immutable stable Brand Kit release and fresh ADR source separately in one composed artifact.
  - Verify live Decisions routes, alias, provenance and Brand Kit bytes, then show the page for maintainer feedback.
  active_issue:
    provider: github
    id: egohygiene/identity#69
    url: https://github.com/egohygiene/identity/issues/69
  next:
    kind: action
    id: validate-identity-decisions-publication-candidate
    description: Validate the immutable single-publisher candidate using merged Relay cabbf5b3b658d585b4d56ef0c99917969a96eed2, then retain the
      artifact, deploy and verify live evidence.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/69
    - https://github.com/egohygiene/relay/issues/115
    depends_on: []
state:
  base:
    revision: 642d096e60b729060e5880e5222d7b57184b735e
    ref: refs/heads/main
    verified_at: '2026-10-10T16:12:12Z'
  candidate:
    branch: codex/identity-69-decisions-publication
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-10T16:12:12Z'
    default_branch_revision: 642d096e60b729060e5880e5222d7b57184b735e
    issue_state: open
    pull_request_state: not-applicable
    notes: 'PR #92 merged at 2026-10-10T15:56:26Z; merge and current main were independently GET-verified. This publication candidate has no PR
      or self-SHA yet. Identity #69 remains open. No Decisions deployment is established.'
  parallel_changes:
  - provider: github
    id: egohygiene/relay#138
    url: https://github.com/egohygiene/relay/pull/138
review:
  status: partial
  reviewed_at: '2026-10-10T16:13:42Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub GET PR #92, branches/main and Identity #69; git branch --show-current; git rev-parse HEAD'
    outcome: passed
    observed_at: '2026-10-10T16:12:12Z'
    notes: 'PR #92 merged as 642d096e60b729060e5880e5222d7b57184b735e; current main and local base match. Publication branch is in progress, with
      null candidate revision and PR.'
  - command: 'Read immutable PR #92 native and production receipt at source 12227dad43c90b02e14971030f22242f3a205c9d'
    outcome: limited
    observed_at: '2026-10-10T16:12:12Z'
    notes: 'Historical 21-record proof: complete/current ADR collection; architecture incomplete with five non-ADR warnings; two clean production
      builds yielded 19 identical files. Relay was 4137cb07a017b7bbae2ee38fe9b039c58b0b17eb. This does not validate the current 22-record publication
      candidate.'
  - command: Inspect publication/decisions-rollback.json and current single-publisher composition
    outcome: limited
    observed_at: '2026-10-10T16:12:12Z'
    notes: Record observed at 2026-10-10T16:02:47Z captures 40 served Brand Kit files with site digest sha256:c690803f5eda55c7b61d7ae34a1df3e109d2dad9aad9a34ef086207d4cd0fd88.
      It is a fresh live capture, not reverification of the expired original Actions ZIP. Deployment must retain a newly checked capture and preserve
      all baseline bytes.
  - command: Draft 2020-12 validation of CONTINUITY.md front matter; exact twelve headings, size, links and git diff --check -- CONTINUITY.md
    outcome: passed
    observed_at: '2026-10-10T16:12:12Z'
    notes: Pinned Aether schema, twelve headings, links, privacy and size checked with the validation environment; shell and primary Python lack
      jsonschema. This is structure validation, not released EgoLint conformance.
  - command: python -m unittest discover -s tests -p test_identity_decisions_publication.py; consumer capture-rollback operation
    outcome: passed
    observed_at: '2026-10-10T16:13:42Z'
    notes: 'Root-reported execution: 17 focused consumer tests passed; fresh rollback capture verified all 40 files in 19.764 seconds with the
      same archive digest. This does not establish final immutable composition or deployment.'
  - command: Immutable 22-record production composition, hosted publication and live verification
    outcome: not-run
    observed_at: '2026-10-10T16:12:12Z'
    notes: 'Final immutable candidate build and deployment evidence are pending. Merged Relay PR #138 is pinned at cabbf5b3b658d585b4d56ef0c99917969a96eed2;
      its merge and all five consumer action references were checked.'
  environment_limitations:
  - Final candidate, production composition, retained hosted artifact and live checks remain pending; no new deployment is claimed.
  - Historical native and CI proof belongs to source 12227dad and reviewed head e23fad23227b933f524e6677ea1e195cf1ba1788, not this uncommitted
    candidate.
  - The prior original Pages ZIP expired; the fresh forty-file capture is independent recovery evidence, not that ZIP.
  - Official released EgoLint continuity conformance is not established by local schema/structure checks.
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

1. Read AGENTS.md, branch/status/history and the canonical publication sources.
2. Refresh main, current candidate, Identity #69 and the organization log.
3. Read ADR-022, the rollback record and the publisher's exact dependency pins.
4. Validate fresh source/composition before deployment, then check live bytes.

## Current objective and success conditions

PR #92 is merged. Complete consumer-owned Decisions publication using the existing single Pages publisher at `identity.egohygiene.io`. Preserve the stable Brand Kit, keep evidence identities distinct, and show the working page for maintainer feedback before repository-by-repository fleet rollout.

## State snapshot

Main/base is `642d096e60b729060e5880e5222d7b57184b735e`; PR #92 merged at 2026-10-10T15:56:26Z. Branch `codex/identity-69-decisions-publication` is in progress; candidate self-SHA and PR stay null. The prior 21 ADRs remain accepted under the [R1 approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806). New [ADR-022](docs/decisions/ADR-022-decisions-publication-composition.md) is proposed. Neither implementation nor deployment supplies its disposition.

## Completed and material changes

- Merged canonicalization retains all prior ADR prose/history and approved notes.
- This candidate extends `.github/workflows/publish-brand-kit.yml`; the existing
  publisher remains the sole owner of the site's composed Pages artifact.
- Fresh Relay output is composed at `renderer/dist/intelligence`; `/decisions/`
  aliases `/intelligence/decisions/`. Organization `/identity/` remains separate.
- `scripts/identity_decisions_publication.py` owns the consumer alias, recovery
  capture and full live-byte checks; the baseline's 40 original files must survive.
- `publication/decisions-rollback.json` records the fresh prior-site capture;
  it does not claim recovery of the expired original ZIP or exercised rollback.
- Pinned Aether authoring 2.0.0 and continuity 1.1.0 were loaded directly from
  `8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2`; no host installation is claimed.

## Validation and review evidence

The [prior receipt](docs/evidence/identity-adrs-ratified-2026-10-10.json) binds source `12227dad43c90b02e14971030f22242f3a205c9d`, not this candidate. Its 21-record collection passed, architecture retained five non-ADR warnings, and 19 production files reproduced exactly. Both hosted checks passed at reviewed head `e23fad23227b933f524e6677ea1e195cf1ba1788` before merge. Seventeen focused consumer tests and fresh 40-file rollback capture passed. Current immutable 22-record and publication validation must be recorded separately. The pinned continuity schema, twelve headings, links and size were checked; these are structural checks, not official continuity conformance or live proof.

## Blockers, risks, unknowns, and deferred work

Relay PR #138 merged as `cabbf5b3b658d585b4d56ef0c99917969a96eed2`; all five consumer action references select it. Historical build and rollback-helper evidence remains correctly bound to `4137cb07a017b7bbae2ee38fe9b039c58b0b17eb`. Final immutable candidate validation, retained hosted artifact, deployment receipt, live verification and feedback are pending. The original Pages ZIP has expired; freshly verified recovery bytes are required. ADR-022 stays proposed; the 21 existing approvals do not extend to it.

## Next dependency-ready work

Validate fresh collection, alias, 40-file byte preservation and rollback capture at the immutable candidate. Retain the composed artifact, deploy through the existing publisher, verify live source/provenance and bytes, then show it for feedback. Keep Identity #69 and Relay #115 open until their acceptance evidence is complete.

## Parallel changes and reconciliation

Source, workflow, documentation and tests are being prepared in the same bounded publication candidate. Relay #138 is merged; Relay #115 owns broader acceptance. Reconcile final validation receipts before PR handoff; do not overwrite peer edits. The five PR #90 coordination issue updates are already applied. Identity #83 retains broader roadmap/publication-document reconciliation.

## Privacy and redaction

Retain public source links and concise evidence only. Exclude private context, credentials, local paths and raw logs. The checkpoint grants no new authority.

## Handoff update protocol

Refresh after final domain checks with exact candidate, dependency pins and remaining gates. Leave a containing commit's own SHA null. Record artifact production, provider deployment and live verification as distinct outcomes.

## Compaction and supersession

Keep below 240 lines and 16,384 UTF-8 bytes. Replace stale observations; Git and work trackers retain history. Mark unresolved conflicts stale.