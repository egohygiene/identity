---
schema: aether.architecture-document/v1
id: identity-decisions
title: Identity Decisions
kind: architecture-document
version: 1.2.0
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-30
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

## Purpose

This document preserves significant accepted architectural choices and their
rationale. Issues coordinate work, evaluations compare evidence, and decision
records constrain future implementation.

## Governance

Do not rewrite historical context to fit current understanding. Amend a record
for corrections that do not change meaning; supersede it with a new record when
the decision changes materially.

## Index

- ADR-001: Keep creative approval human-owned
- ADR-002: Store consumer assets beneath a stable identity contract
- ADR-003: Separate deterministic projection from generative creation
- [ADR-004: Use DTCG 2025.10 as the token contract](docs/decisions/ADR-004-dtcg-token-contract.md)
- [ADR-005: Publish curated JSON Schemas and validate them offline](docs/decisions/ADR-005-json-schema-contract.md)
- [ADR-006: Use a pinned Rust vector and raster stack](docs/decisions/ADR-006-rust-rendering-stack.md)
- [ADR-007: Separate font inspection, rendering, subsetting, and approval](docs/decisions/ADR-007-font-tooling-boundaries.md)
- [ADR-008: Encode platform metadata as versioned first-party profiles](docs/decisions/ADR-008-platform-profile-contracts.md)
- [ADR-009: Keep Storybook at the consumer integration boundary](docs/decisions/ADR-009-storybook-consumer-adapter.md)
- [ADR-010: Render from a framework-neutral immutable view model](docs/decisions/ADR-010-reference-renderer-boundary.md)
- [ADR-011: Layer normative, exact, browser, and human quality evidence](docs/decisions/ADR-011-accessibility-and-visual-evidence.md)
- [ADR-012: Use local, layered Identity v1 source contracts](docs/decisions/ADR-012-local-layered-identity-v1.md)
- [ADR-013: Preserve guidance lifecycle state in every projection](docs/decisions/ADR-013-preserve-guidance-lifecycle.md)
- [ADR-014: Keep design-system handbooks as governed projections](docs/decisions/ADR-014-design-system-projection-boundary.md)
- [ADR-015: Keep Press Kits as governed public projections](docs/decisions/ADR-015-press-kit-projection-boundary.md)
- [ADR-016: Project social surfaces from pinned external facts](docs/decisions/ADR-016-pinned-social-surface-projection-boundary.md)
- [ADR-017: Compose Identity's dogfood experience without moving brand authority](docs/decisions/ADR-017-zensical-launchkit-publication-architecture.md)

## ADR-001: Keep creative approval human-owned

- **Status:** Accepted as the current architectural direction
- **Date:** 2026-08-19
- **Context:** Repository evidence and ecosystem ownership require an explicit durable boundary.
- **Decision:** Keep creative approval human-owned.
- **Consequences:** The choice improves ownership and predictability while requiring maintained contracts, validation, and migration discipline.
- **Reconsider when:** New evidence shows that the boundary prevents standalone usefulness, safety, portability, or maintainability.

## ADR-002: Store consumer assets beneath a stable identity contract

- **Status:** Accepted as the current architectural direction
- **Date:** 2026-08-19
- **Context:** Repository evidence and ecosystem ownership require an explicit durable boundary.
- **Decision:** Store consumer assets beneath a stable identity contract.
- **Consequences:** The choice improves ownership and predictability while requiring maintained contracts, validation, and migration discipline.
- **Reconsider when:** New evidence shows that the boundary prevents standalone usefulness, safety, portability, or maintainability.

## ADR-003: Separate deterministic projection from generative creation

- **Status:** Accepted as the current architectural direction
- **Date:** 2026-08-19
- **Context:** Repository evidence and ecosystem ownership require an explicit durable boundary.
- **Decision:** Separate deterministic projection from generative creation.
- **Consequences:** The choice improves ownership and predictability while requiring maintained contracts, validation, and migration discipline.
- **Reconsider when:** New evidence shows that the boundary prevents standalone usefulness, safety, portability, or maintainability.

## Open decisions

- Release and compatibility policy for the first stable version.
- Exact self-hosted and managed deployment boundaries beyond the accepted
  organization-integrated `/identity/` artifact handoff.
- Which target systems must exist before the runtime architecture may be called implemented.

## Evidence and uncertainty

- **Observed:** The repository defines an Identity compiler that turns a repository-specific brand specification into coherent visual, textual, and platform assets; significant implementation remains incomplete.
- **Accepted:** The Brand Kit product contract and ADR-001 through ADR-017 constrain future implementation.
- **Proposed:** Runtime capabilities and later roadmap phases remain proposals until their owning issues provide implementation evidence.
- **Open question:** Which optional adapter profiles belong in the first independently versioned release?
