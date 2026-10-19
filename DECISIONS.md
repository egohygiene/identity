---
schema: aether.architecture-document/v1
id: identity-decisions
title: Identity Decisions
kind: architecture-document
version: 1.4.1
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-10-18
governed_by:
  - architecture-decisions
depends_on:
  - identity-principles
  - identity-epistemology
  - identity-foundations
  - identity-system
  - identity-architecture
related:
  - identity-purpose
  - identity-vision
  - identity-pillars
  - identity-manifesto
  - identity-brand-kit-foundations-evaluation
  - identity-dependency-policy
supersedes: []
---

# Identity Decisions

The [canonical decision index](docs/decisions/README.md) links all records.
The [migration map](docs/decision-migration-2026-10-10.md) preserves historical
status claims, provenance, and the questions identified before ratification.
The [2026-10-10 human disposition](docs/decision-ratification-2026-10-10.md)
subsequently retained ADR-0001–018 and accepted ADR-0019–021. ADR-0022 remains
proposed; its implemented publication path does not supply lifecycle approval.

Legacy acceptance claims remain unchanged in their records; this navigation
page does not ratify them. New records follow the pinned
[policy reference](docs/decisions/policy-reference.json).

The headings below preserve the three historical inline links.

## ADR-0001: Keep creative approval human-owned

[Canonical record](docs/decisions/ADR-0001-creative-approval-human-owned.md).

## ADR-0002: Store consumer assets beneath a stable identity contract

[Canonical record](docs/decisions/ADR-0002-stable-identity-contract.md).

## ADR-0003: Separate deterministic projection from generative creation

[Canonical record](docs/decisions/ADR-0003-deterministic-projection-boundary.md).

## Open decisions

ADR-0022 and [ADR-0023](docs/decisions/ADR-0023-canonical-source-digest.md) await
their own human dispositions. ADR-0023 proposes the shared source-digest
compatibility contract for #74. The migration map retains the earlier
open questions as history; [ROADMAP.md](ROADMAP.md) owns current execution
order. Detailed ADR-0004 onward retain their existing paths.

## Identifier format migration (2026-10-18)

The maintainer selected four-digit numbering in [Hygiene #73](https://github.com/egohygiene/hygiene/issues/73). This padding-only migration changes current labels and anchors; logical numbers, decision content, dates and disposition remain unchanged. Git retains prior versions. New canonical records use `ADR-NNNN` under Hygiene policy v1.2.0.

| Previous ID | Current ID | Record |
| --- | --- | --- |
| `ADR-001` | `ADR-0001` | [DECISIONS.md](DECISIONS.md#adr-0001-keep-creative-approval-human-owned) |
| `ADR-002` | `ADR-0002` | [DECISIONS.md](DECISIONS.md#adr-0002-store-consumer-assets-beneath-a-stable-identity-contract) |
| `ADR-003` | `ADR-0003` | [DECISIONS.md](DECISIONS.md#adr-0003-separate-deterministic-projection-from-generative-creation) |
