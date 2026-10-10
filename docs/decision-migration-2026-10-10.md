# Identity ADR migration and human disposition packet

Issue: [Identity #69](https://github.com/egohygiene/identity/issues/69).
Audit and reconstruction date: 2026-10-10.
Source boundary: [`8aae2c6767d07714ea16bf0ea493e1f1ac399b6e`](https://github.com/egohygiene/identity/tree/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e).

## Outcome and present limitation

Preserve Identity's existing decision history, inventory its authority gaps,
and prepare a reviewed migration to the ratified Hygiene policy. This packet
does not ratify a decision, rewrite historical intent, prove a conforming
complete corpus, or authorize publication. Identity #69 and Relay #115 remain
open until their respective source, handoff, and acceptance requirements are met.

The source boundary contains **18 existing decision IDs**: ADR-001 through
ADR-003 inline in root `DECISIONS.md`, and ADR-004 through ADR-018 in detailed
files. All claim acceptance in legacy prose. None has the canonical Hygiene
ADR front matter or a durable approval object. The baseline has no canonical
`docs/decisions/README.md` or `policy-reference.json`. No ID collision or declared
supersession pair was found among these 18 records.

The migration preserves ADR-004 through ADR-018 byte-for-byte. ADR-001 through
ADR-003 are extracted with their original bodies and source provenance; their
old root heading anchors remain navigation aliases. The new canonical index
must identify the acceptance labels as unresolved **legacy claims**, not
validated lifecycle dispositions. New ADR-019 through ADR-021 are proposed
historical reconstructions with null approval, separate from those claims.

## Authority and authoring sources

- [Hygiene policy 1.1.0](https://github.com/egohygiene/hygiene/blob/c589587395750cd1c79c6fa0bef010189c547249/docs/decisions/POLICY.md)
  and its [migration guide](https://github.com/egohygiene/hygiene/blob/c589587395750cd1c79c6fa0bef010189c547249/docs/decisions/MIGRATION.md)
  own lifecycle, inheritance, human authority, record anatomy, and migration.
- [Aether authoring skill 2.0.0](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/SKILL.md)
  and its [record guide](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/references/decision-record-guide.md)
  require evidence-backed reconstruction, proposed new records, and preservation
  of unsupported legacy acceptance claims as migration gaps.
- [Aether adoption guidance](https://github.com/egohygiene/aether/blob/8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2/library/organization/skills/architecture/create-decisions-document/references/adoption.md)
  selects validate-first for this existing corpus. An old Holon blueprint's
  incompatible policy pin must not be silently applied. These Identity-authored
  records are not generated Holon output.

The policy's human-ratification evidence establishes the **organization policy**;
it does not ratify Identity's local decisions. A PR author's account, a merge,
closed issue, implementation, or passing check alone cannot fill an approval
object. An exception cannot waive that requirement.

## History and provider evidence boundary

The Identity checkout is not shallow. Its audited `main` has 171 reachable
commits, from the initial commit on 2026-07-28 through PR #89 on 2026-10-03.
The full commit-subject inventory, first-parent sequence, and decision-file
introduction history were inspected. Local tags `v1.0.0-rc.1`, `v1.0.0-rc.2`,
and `v1.0.0` are present. This is not a new download, release-artifact digest,
build, deployment, or live-route verification.

Public issue comments were inspected for #7, #9, #13, #34, #35, #50, #52,
#54, #56, #65, #18, and the recent #71–#73 fixes. The original ADR introduction
and amendment PRs #4, #20, #27, #37, #48, #53, #55, #59, #61, and #64 have
no review submissions; their top-level comments are absent or automated
devActivity summaries. No explicit human ADR ratification was found in those
inspected sources. This is a bounded evidence result, not a claim that no
approval ever happened in an inaccessible conversation or another source.

The [issue #50 visual-selection comment](https://github.com/egohygiene/identity/issues/50#issuecomment-5463168075)
explicitly records human selection of a particular mascot and its promotion
through existing governance. Its scope is visual selection, not blanket
ratification of ADR-001–ADR-018 or proposed ADR-021. The
[issue #18 release closeout](https://github.com/egohygiene/identity/issues/18#issuecomment-5448834860)
records historical release evidence; it is not a separate architectural
ratification or a fresh release check.

Unmerged Identity PR #90 prepares issue-coordination edits; it is not included
in audited main and merging it does not apply those issue updates. It is not
evidence that the pilot, publication, or human authority gates have cleared.

## Existing-record migration and disposition table

Every row below has **human authority unresolved**. The original status and
date remain source claims. Introduction evidence establishes the existence of
the record, not acceptance. Keep each identifier and filename stable; no row
is silently reclassified as proposed or treated as newly accepted.

| ID and choice | Original location → canonical target | Legacy date and disposition claim | Introduction / amendment evidence |
| --- | --- | --- | --- |
| ADR-001 — Human-owned creative approval | `DECISIONS.md` inline → [ADR-001](decisions/ADR-001-creative-approval-human-owned.md) | 2026-08-19; accepted as current architectural direction | [PR #4](https://github.com/egohygiene/identity/pull/4), source `5ec2d88ef5c1ace7e7782bd000b48183af0e47f2` |
| ADR-002 — Stable consumer identity contract | `DECISIONS.md` inline → [ADR-002](decisions/ADR-002-stable-identity-contract.md) | 2026-08-19; accepted as current architectural direction | PR #4, same immutable source |
| ADR-003 — Deterministic projection versus generation | `DECISIONS.md` inline → [ADR-003](decisions/ADR-003-deterministic-projection-boundary.md) | 2026-08-19; accepted as current architectural direction | PR #4, same immutable source |
| ADR-004 — DTCG 2025.10 token contract | [Existing file retained](decisions/ADR-004-dtcg-token-contract.md) | 2026-08-20; Accepted | [PR #20](https://github.com/egohygiene/identity/pull/20), source `13c0824090755587efc3f65dca4638f6d8186374` |
| ADR-005 — Curated offline JSON Schemas | [Existing file retained](decisions/ADR-005-json-schema-contract.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-006 — Pinned Rust rendering stack | [Existing file retained](decisions/ADR-006-rust-rendering-stack.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-007 — Font tooling and approval boundaries | [Existing file retained](decisions/ADR-007-font-tooling-boundaries.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-008 — Versioned platform profiles | [Existing file retained](decisions/ADR-008-platform-profile-contracts.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-009 — Storybook consumer boundary | [Existing file retained](decisions/ADR-009-storybook-consumer-adapter.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-010 — Immutable framework-neutral view model | [Existing file retained](decisions/ADR-010-reference-renderer-boundary.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-011 — Layered accessibility and visual evidence | [Existing file retained](decisions/ADR-011-accessibility-and-visual-evidence.md) | 2026-08-20; Accepted | PR #20, same immutable source |
| ADR-012 — Local layered Identity v1 source | [Existing file retained](decisions/ADR-012-local-layered-identity-v1.md) | 2026-08-21; Accepted for Identity v1 | [PR #27](https://github.com/egohygiene/identity/pull/27), source `7885b7ea8e2bc9ac7bc2522f3655ade69babad0d` dated 2026-08-22 |
| ADR-013 — Guidance lifecycle preservation | [Existing file retained](decisions/ADR-013-preserve-guidance-lifecycle.md) | 2026-08-21; Accepted | [PR #37](https://github.com/egohygiene/identity/pull/37), source `8f4ae5d9644255b28aba387a8ed286ea5fefa99c` dated 2026-08-26 |
| ADR-014 — Governed design-system projections | [Existing file retained](decisions/ADR-014-design-system-projection-boundary.md) | 2026-08-28; Accepted | [PR #48](https://github.com/egohygiene/identity/pull/48), source `5d6b5fd954e8f18ec645ffd88cc4718b801d855a` |
| ADR-015 — Governed Press Kit projections | [Existing file retained](decisions/ADR-015-press-kit-projection-boundary.md) | 2026-08-28; Accepted | [PR #53](https://github.com/egohygiene/identity/pull/53), source `93b7447f35417d80956bdd4ec0f91dec9513c035` |
| ADR-016 — Pinned external social facts | [Existing file retained](decisions/ADR-016-pinned-social-surface-projection-boundary.md) | 2026-08-29; Accepted | [PR #55](https://github.com/egohygiene/identity/pull/55), source `c1c093f6fcc49f92085b7d8d8f798356cebe8969` |
| ADR-017 — Two-host dogfood publication | [Existing file retained](decisions/ADR-017-zensical-launchkit-publication-architecture.md) | 2026-08-30; Accepted; amended 2026-08-30 | [PR #59](https://github.com/egohygiene/identity/pull/59), source `84b97d06dd6eb954fbfc6e20b3806eaef6050ab4`; [PR #61](https://github.com/egohygiene/identity/pull/61), source `c65b1402a33a2bb922efbe99c05a0802cf89b053`; both Git dates 2026-08-29 |
| ADR-018 — Repository presentation without conformance authority | [Existing file retained](decisions/ADR-018-repository-presentation-projection-boundary.md) | 2026-08-30; Accepted | [PR #64](https://github.com/egohygiene/identity/pull/64), source `002202e25e28556c584940007af8e1fec2cfa822` |

Differences between declared dates and Git introduction dates are retained,
not silently corrected or interpreted as false history. A decision can predate
its record, but that distinction needs evidence. In particular ADR-012,
ADR-013, and ADR-017 need date review before claiming a proven historical
disposition date.

## Material historical coverage and new proposals

| Historical change | Decision treatment | Evidence and boundary |
| --- | --- | --- |
| Standalone CLI extraction and preserved consumer parity | Attach implementation evidence to ADR-002/003/012; no duplicate extraction ADR proposed | [PR #21](https://github.com/egohygiene/identity/pull/21), existing `docs/migration/EMPATHY_EXTRACTION.md` |
| Compiler, packages, profile selection, deterministic generation and guarded recovery | Evidence under ADR-003/005/006/008/012 | [PR #30](https://github.com/egohygiene/identity/pull/30), [#31](https://github.com/egohygiene/identity/pull/31), and bounded recovery correction in [#89](https://github.com/egohygiene/identity/pull/89); do not infer all future capabilities delivered |
| Preview-only studio and named local approval handoff | Evidence under ADR-001/003/013 | [PR #39](https://github.com/egohygiene/identity/pull/39), [#40](https://github.com/egohygiene/identity/pull/40), [#41](https://github.com/egohygiene/identity/pull/41); browser remains non-mutating |
| Independent immutable release and artifact trust | New [ADR-019](decisions/ADR-019-immutable-release-contract.md), proposed | Release PR #43/#44/#45 and release procedure; distinct from ADR-017's hosting decision |
| Account registry governance, lifecycle and verification | New [ADR-020](decisions/ADR-020-channel-registry-governance.md), proposed | [PR #68](https://github.com/egohygiene/identity/pull/68); external account facts are distinct from ADR-016's platform-spec catalog |
| Optional governed mascot source and derivative package | New [ADR-021](decisions/ADR-021-governed-mascot-package.md), proposed | [PR #58](https://github.com/egohygiene/identity/pull/58); visual selection evidence is not architectural ratification |
| Public guidance filtering and withheld singleton representation | Correction evidence under ADR-013 | [PR #89](https://github.com/egohygiene/identity/pull/89) and issues #71–#73; preserve review history and actual limitations |

The three new records use reconstruction date 2026-10-10, null approval, and
`implemented` only for the bounded behavior present in inspected source. They
do not claim `verified`; historical checks were not rerun for this audit. Their
historical implementation dates are notes, not invented approval dates. Actual
`identity.*` contract IDs are named in prose rather than inventing unsupported
`egohygiene.*` registration IDs to populate schema metadata.

## Source-preservation and remaining migration gaps

1. Preserve legacy prose and exact IDs. Attach canonical front matter and the
   seven required sections only in a reviewed follow-up that preserves original
   rationale and resolves human disposition. Missing alternatives stay unknown.
2. Preserve root heading anchors for inline ADR-001–ADR-003. Root `DECISIONS.md`
   becomes navigation; extracted files hold the historical bodies once each.
3. Keep the canonical index, pinned policy reference, agent-guidance pointer,
   and migration packet distinct. This packet lives outside the collected ADR
   directory so it is not mistaken for a canonical decision record.
4. The inspected `publication/identity-experience.content.json` contains
   nonexistent paths and mismatched titles for ADR-006 and ADR-013:
   `ADR-006-authoring-generated-state-boundary.md` and
   `ADR-013-public-identity-reference-page.md`. They are not alternate canonical
   decisions or ID assignments. Reconcile these public references through the
   publication owner without creating duplicate records or silent aliases to
   unrelated content.
5. Legacy detailed files have varied section names and missing canonical
   metadata. An index and policy pin alone cannot satisfy Relay's complete
   source-admission gate. Keep observed source gaps and production denial visible.
6. Do not change independent Brand Kit host, organization `/identity/` route,
   release tag, or publication authority as a side effect of ADR adoption.

## Legacy root questions and claims retained for reconciliation

The old [root document at the audit revision](https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/DECISIONS.md)
listed these open questions:

- Release and compatibility policy for the first stable version.
- Exact self-hosted and managed deployment boundaries beyond the claimed
  accepted organization-integrated `/identity/` artifact handoff.
- Which target systems must exist before runtime architecture may be called
  implemented.
- Which optional adapter profiles belong in the first independently versioned
  release.

It described significant implementation as incomplete, claimed the Brand Kit
product contract and ADR-001–ADR-018 were accepted, and kept later runtime
capabilities and roadmap phases proposed pending evidence. These statements
are preserved here as historical claims, not upgraded into current truth.
Release source and tags show that the first question needs reconciliation;
they do not automatically answer every compatibility or deployment question.
Broader roadmap/publication documentation reconciliation remains
[Identity #83](https://github.com/egohygiene/identity/issues/83).

## Concrete human disposition requested

Review the migration PR's exact **candidate commit** and this 18-row table.
For each existing ADR, choose one of the following; a single explicit statement
may cover an enumerated group of IDs if the same disposition applies:

| Response | Required evidence and next change |
| --- | --- |
| Retain the accepted direction | Explicitly ratify the named IDs at the reviewed candidate now, with human identity, current date, and durable PR/issue comment or review URL; preserve original dates as legacy claims unless separate historical proof establishes them. |
| Correct the legacy claim or content | Identify the IDs, corrected current disposition or precise correction, rationale, and supporting evidence. Do not silently relabel original historical text; record the correction and its date. |
| Supersede a direction | Name the predecessor and replacement choice. Prepare a new proposed record, obtain explicit human acceptance and old-record disposition, then validate effective reciprocal lineage. |

An explicit reply can instead point to previously existing durable approval
evidence for particular IDs. Inspect its actual scope before using it. No
response defaults to acceptance. Generic permission to do implementation work
or merge a PR is not a blanket decision ratification. ADR-019, ADR-020, and
ADR-021 require their own proposed-record disposition and are not included
implicitly in the 18 legacy choices.

## Verification and rollback boundary

Verify ADR-004–ADR-018 against the audited Git blobs and compare extracted
inline bodies with root source at the same full revision. Validate new proposed
metadata against the exact pinned owner schema and inspect the seven required
sections, local links, evidence descriptions, and privacy. Report native source
validation separately; legacy records remain incomplete until migrated.

Rollback the scoped migration through a reviewed Git revert that restores the
prior root/index/policy/navigation consistently and preserves any later authored
decisions. The immutable audit revision above retains original bodies and blame
history. This source-only checkpoint changes no live deployment, release,
consumer artifact, or historical rollback point.
