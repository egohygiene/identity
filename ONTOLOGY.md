---
schema: aether.architecture-document/v1
id: identity-ontology
title: Identity Ontology
kind: architecture-document
version: 0.1.0
status: provisional
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-ontology
depends_on:
  - identity-purpose
  - identity-vision
  - identity-principles
  - identity-epistemology
related:
  - identity-pillars
  - identity-manifesto
  - identity-ai-constitution
  - identity-personal-model
supersedes: []
---

# Identity Ontology

## Domain scope

Identity models the concepts needed for make every repository identity deliberate, reusable, accessible, and reproducible across its public surfaces. The ontology names conceptual entities and relationships; it is not a source-code class model, API schema, or database design.

## Canonical concepts

| Concept | Meaning |
| --- | --- |
| Identity specification | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Creative direction | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Brand asset | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Projection | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Variant | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Platform requirement | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Approval | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Provenance | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |
| Asset manifest | A canonical concept in the Identity domain whose exact fields belong to specifications or schemas, not this ontology. |

## Core relationships

- A repository or person provides source context to one or more domain artifacts.
- A specification constrains how an artifact is interpreted or produced.
- A plan separates proposed action from execution.
- Evidence supports a claim; a decision authorizes a durable direction.
- Provenance connects derived artifacts to their inputs and processing context.
- A consumer integrates through an explicit interface rather than internal structure.

## Boundaries

- Conceptual identity is distinct from filesystem path, database identifier, or display label.
- Observed state is distinct from desired state.
- Proposed relationships are not accepted facts.
- Neighboring repositories retain ownership of their domain concepts.

## Evidence and uncertainty

- **Observed:** The repository README establishes the intended boundary as the identity compiler that turns a repository-specific brand specification into coherent visual, textual, and platform assets; significant implementation remains incomplete.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
