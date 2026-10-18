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
subsequently retained ADR-001–018 and accepted ADR-019–021. ADR-022 remains
proposed; its implemented publication path does not supply lifecycle approval.

Legacy acceptance claims remain unchanged in their records; this navigation
page does not ratify them. New records follow the pinned
[policy reference](docs/decisions/policy-reference.json).

The headings below preserve the three historical inline links.

## ADR-001: Keep creative approval human-owned

[Canonical record](docs/decisions/ADR-001-creative-approval-human-owned.md).

## ADR-002: Store consumer assets beneath a stable identity contract

[Canonical record](docs/decisions/ADR-002-stable-identity-contract.md).

## ADR-003: Separate deterministic projection from generative creation

[Canonical record](docs/decisions/ADR-003-deterministic-projection-boundary.md).

## Open decisions

ADR-022 and [ADR-023](docs/decisions/ADR-023-canonical-source-digest.md) await
their own human dispositions. ADR-023 proposes the shared source-digest
compatibility contract for #74. The migration map retains the earlier
open questions as history; [ROADMAP.md](ROADMAP.md) owns current execution
order. Detailed ADR-004 onward retain their existing paths.
