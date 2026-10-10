---
schema: egohygiene.architecture-decision/v1
id: ADR-012
title: Use local, layered Identity v1 source contracts
status: accepted
date: '2026-10-10'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/69
pull_request: https://github.com/egohygiene/identity/pull/92
related: []
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts: []
implementation_status: implemented
evidence:
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-012 with its scope qualifiers and exact N012 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-012-local-layered-identity-v1.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N012 and its evidence and implementation limits.
- type: implementation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/validate_identity.py
  description: Local layer digests, reviewed overrides and post-merge aliases are validated offline; this is implementation evidence only.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-012: Use local, layered Identity v1 source contracts

## Context

Consumers need a recognizable organization family without surrendering product
identity or depending on mutable cross-repository source. The incubated v0 TOML
contract selected profiles and creative sources, but it could not express
organization inheritance, reviewed overrides, interoperable semantic tokens,
complete provenance, or stable automation diagnostics.

## Decision

Identity v1 uses a closed JSON project manifest that pins local token layers by
SHA-256. Organization-default DTCG documents resolve first; one product layer
resolves last. Replacing an inherited token requires a reason and human
approval reference. Aliases resolve only after merge and fail closed when
missing, cyclic, or type-incompatible.

The manifest names separate local boundaries for target selection, provenance,
approvals, creative guidance, approved sources, candidates, and references.
The standard-library validator reads those boundaries without network or write
authority and emits stable `identity.diagnostics/v1` records.

## Alternatives considered and rejected

### Resolve organization defaults from a mutable remote branch

Rejected because validation would become network-dependent and non-reproducible.

### Copy final organization tokens into every product without layer identity

Rejected because inherited values and intentional overrides would become
indistinguishable.

### Make a projection format the canonical token model

Rejected because CSS, Tailwind, Style Dictionary, and renderer needs change at
different rates and should remain replaceable adapters.

### Accept unknown fields for future flexibility

Rejected because silent typos and ambiguous meaning undermine compatibility.
Extensibility uses explicit dotted namespaces and versioned contracts.

## Consequences and tradeoffs

- Consumers can review the exact organization snapshot they inherit.
- Products express intentional differences without forking the token model.
- DTCG documents remain framework-neutral source while CSS, Tailwind, and other
  formats remain projections.
- Asset licensing, provenance, accessibility metadata, usage constraints, and
  approval are available before generation.
- Updating organization defaults requires a reviewed local snapshot/digest
  change rather than an implicit default-branch read.
- The contract is more explicit than v0 and requires a review-guided migration.

## Implementation and evidence links

The local layered v1 source contract and offline validator are implemented in
the inspected source, including layer digests, reviewed overrides and alias
checks. This migration does not reverify every v1 capability. See N012 for
the approved implementation and distinct-date clarification.

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

### Reconsider when

A portable, content-addressed standard can express the same local inheritance,
override intent, human authority, asset governance, and offline diagnostics
without introducing mutable or provider-specific coupling.

## Follow-up work

Retain reviewed local snapshot upgrades and exact implementation evidence.
Keep declared historical, Git introduction and human approval dates distinct
as required by N012.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted for Identity v1
- **Date:** 2026-08-21
- **Decision owner:** `egohygiene/identity`
- **Related issues:** #1, #9

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-012-local-layered-identity-v1.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N012 — Local layers and distinct dates

Retain the local, layered, digest-pinned v1 source direction and its offline
validation boundary. Current source includes automatic embedded-validator
preflight and freshness rechecks. The original 2026-08-21 date remains a
declared historical date; the record's Git introduction on 2026-08-22 is
separate evidence. Any new human ratification uses its actual current date and
durable evidence URL, without backdating acceptance or implying fresh
verification of every v1 capability.

Evidence: [source contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/IDENTITY_V1.md) and
[original introduction](https://github.com/egohygiene/identity/commit/7885b7ea8e2bc9ac7bc2522f3655ade69babad0d).
