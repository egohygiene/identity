---
schema: aether.architecture-document/v1
id: identity-decisions
title: Identity Decisions
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
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
supersedes: []
---

# Identity Decisions

## Purpose

This document preserves significant accepted architectural choices and their rationale. Issues coordinate work, proposals explore alternatives, and this file records decisions that constrain future implementation.

## Governance

Do not rewrite historical context to fit current understanding. Amend a record for corrections that do not change meaning; supersede it with a new record when the decision changes materially.

## Index

- ADR-001: Keep creative approval human-owned
- ADR-002: Store consumer assets beneath a stable identity contract
- ADR-003: Separate deterministic projection from generative creation

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
- Exact self-hosted, managed, and organization-integrated deployment boundaries.
- Which target systems must exist before the architecture status may become active.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the identity compiler that turns a repository-specific brand specification into coherent visual, textual, and platform assets; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
