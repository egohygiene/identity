---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:24:25.121653+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Prepare concrete Identity descriptor/output proposals and a separate mechanically assembled
    candidate while exact owner choices remain unselected.
  includes:
  - Concrete accessible descriptions, H/8 clear-space and digital-size recommendations bound to unchanged
    SVGs.
  - Proposed product/core/tokens/metadata plus optional candidate public-usage records; exact layer option
    A remains independently unselected.
  - A separate 14-file candidate narrows structural diagnostics to two native reviewedAt null fields and
    rejects production/verification before output.
  excludes:
  - No root identity adoption, selection of layer/descriptor/output proposals, invented timestamps or
    new human approval.
  - No runtime/schema/profile/master/rights/ADR lifecycle change, successful actual self-source generation,
    release, hosted CI or deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/contracts/IDENTITY_V1.md
  - docs/decisions/ADR-0001-creative-approval-human-owned.md
  - docs/decisions/ADR-0012-local-layered-identity-v1.md
  - docs/work/98/OWNER_ANSWERS_2026-11-22.md
  - docs/work/98/self-source-review/README.md
  - docs/work/98/source-assembly/README.md
  - docs/work/98/source-assembly/DESCRIPTORS.proposed.json
  - docs/work/98/source-assembly/OUTPUTS.proposed.json
  - docs/work/98/source-assembly/assembly-validation.json
  - docs/work/98/source-assembly/REVIEW_TIME_FINDING.md
work:
  objective: Prepare concrete Identity descriptor/output proposals and a separate mechanically assembled
    candidate while exact owner choices remain unselected.
  success_conditions:
  - Replace null descriptor proposals with exact reviewable strings and explicit measured facts versus
    authored guidance.
  - Keep actual old candidate/root/master bytes unchanged and preserve all pending human choices.
  - Exercise matching source validation and native refusal without inserting synthetic approval times.
  active_issue:
    provider: github
    id: egohygiene/identity#98
    url: https://github.com/egohygiene/identity/issues/98
  next:
    kind: action
    id: review-exact-descriptor-output-and-layer-choices
    description: Review the exact descriptor/output proposal and independent inheritance/token question;
      only then record actual packet-review time and assemble the selected governed source.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    ref: refs/heads/main
    verified_at: '2026-11-22T18:24:25.121653+00:00'
  candidate:
    branch: codex/98-proposed-source-assembly-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Fresh provider reads verify main 75ca39f and issue #98 open; no Identity PR is currently open.
      Prior #158 → #162 and Aether #140 are merged; this new candidate is not merged/adopted or released.'
  parallel_changes:
  - provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  - provider: github
    id: egohygiene/identity#82
    url: https://github.com/egohygiene/identity/issues/82
review:
  status: partial
  reviewed_at: '2026-11-22T18:24:25.121653+00:00'
  reviewed_by: Codex
  evidence:
  - command: Existing provenance/usage schemas on new candidate fragments
    outcome: passed
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    notes: Two proposed complete descriptor records and candidate-only usage document satisfy closed structural
      schemas. No installed date-time format checker is available; this is not timestamp-format proof.
  - command: python3 scripts/validate_identity.py --repository-root docs/work/98/source-assembly/candidate
      --format json
    outcome: limited
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    notes: Exit1/validfalse with exactly two IDN1404 findings at native reviewedAt nulls. Option A layers/descriptors/output
      values remain unselected proposals despite mechanical narrowing.
  - command: cargo build --locked --offline --bin identity; native v1-generate and v1-verify on proposed
      candidate
    outcome: limited
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    notes: Pinned Rust 1.97.1 local build passes; both producer/verify calls refuse with IDN1404 before
      output. All 14 candidate files and original active candidate unchanged. This is no release/download
      qualification.
  - command: Synthetic14-decision date-only control
    outcome: limited
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    notes: 'Existing validator at 75ca39f accepts bare 2026-11-22 timestamps; retained bounded finding
      for root #70 repair. No actual owner timestamp is filled and no parser fix is made here.'
  - command: Documentation, source inventories, protected-input and whitespace checks
    outcome: passed
    observed_at: '2026-11-22T18:24:25.121653+00:00'
    notes: Current proposal/manifests match; original active candidate, selected masters, runtime/contracts/profiles/ADRs
      are unchanged. Documentation links and canonical whitespace pass.
  environment_limitations:
  - Exact inheritance/token and new descriptor/output/public-usage choices remain pending owner response.
  - New native review timestamp cannot be supplied without actual explicit packet review; original exact
    instant remains unknown.
  - No successful actual source generation/public-kit/publisher/native-platform/release proof is supplied.
  - Pinned schema/heading/budget validation is narrower than official released EgoLint continuity conformance.
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

User/runtime and scoped instructions, live evidence and canonical source outrank this operational snapshot. It records a new reviewable assembly, not selected identity source.

## Resume protocol

Read AGENTS, current owner answers, original layer packet and the new source-assembly records. Recheck live main/issue/PR state and actual owner responses before adoption. Prior #158 → #162 and Aether #140 are merged.

## Current objective and success conditions

Prepare concrete Identity descriptor/output proposals and a separate mechanically assembled candidate while exact owner choices remain unselected.

## State snapshot

Base/main is 75ca39f3fc7e5e9e0b5578af58c966cd2590a652. Branch codex/98-proposed-source-assembly-20261122 stages exact new proposals and an intentionally invalid separate consumer. No containing-revision or pre-PR self-reference is required.

## Completed and material changes

New concrete descriptors preserve actual SVG titles/artboards and the horizontal old tagline. H/8 clear space and 64/600 CSS px are explicit new recommendations, with no contrast/WCAG guarantee or new license condition. Product/core/tokens/metadata and optional two-SVG public usage remain proposals. The separate candidate resolves option A structurally while native timestamps remain null.

## Validation and review evidence

Two provenance fragments and candidate usage pass structural schemas. Full proposed consumer returns exactly two IDN1404 findings; native generation and verify refuse without output or input changes. The offline pinned local CLI build succeeds with unchanged product inputs. The14-decision synthetic control identifies existing date-only timestamp acceptance for separate root #70 repair. See assembly-validation and REVIEW_TIME_FINDING; no real approval or full source pass.

## Blockers, risks, unknowns, and deferred work

Owner layer/token and exact descriptor/output choices remain unselected. Schema format support is unavailable locally and a parser loophole is not used as authority. Review timestamps remain null; original creation/reference history remains unknown. Native Kern PNG support, new-tagline derivative, full publisher/release/native/Docker acceptance stay separate.

## Next dependency-ready work

Review the concrete source bundle and independent inheritance question, then bind actual selections and the actual new packet-review time. Rerun matching strict source/producer checks before canonical adoption or real publisher handoff. Existing known brand choices need not be selected again.

## Parallel changes and reconciliation

Root owns Aether metadata repairs and independent Identity #80/#82 runtime qualification, and will repair the demonstrated approval parser under #70. This branch changes only #98 work records/candidate and continuity. Reconcile root handoff semantically before stacking; no runtime/schema or decision lifecycle is changed here.

## Privacy and redaction

Public-safe brand facts, actual geometry and sanitized source-bound diagnostics only. Exclude private transcript, credentials, personal context and local filesystem topology.

## Handoff update protocol

Refresh after domain checks and before PR handoff. Validate pinned metadata, twelve headings and size limits. Reference ADR-0001/ADR-0004/ADR-0012 and proposed ADR-0035; preparation uses pinned Aether decision 2.1.0/continuity 1.1.0 at dc8a168 and Hygiene policy 1.2.0. No duplicate ADR or new approval authority.

## Compaction and supersession

Git and linked owner records retain earlier exact packets and receipts. Preserve those historical hashes and approvals; replace current operational prose rather than append chronology.
