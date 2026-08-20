---
schema: aether.architecture-document/v1
id: identity-design-system
title: Identity Design System
kind: architecture-document
version: 1.0.0
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-20
governed_by:
  - architecture-design-system
depends_on:
  - identity-personal-model
  - identity-design
related:
  - identity-purpose
  - identity-vision
  - identity-principles
  - identity-pillars
supersedes: []
---

# Identity Design System

## Purpose and scope

This document defines the semantic design-system contract that Identity models and projects across documentation, terminal output, packages, reports, the reference Brand Kit, and future interactive surfaces. It does not select a frontend framework, freeze a final visual identity, or move Holon-owned components into this repository.

## Identity semantics

The v1 source contract must be capable of expressing:

| Domain | Semantic responsibility |
| --- | --- |
| Color | Roles, themes, approved pairings, contrast intent, and platform transforms |
| Typography | Families, fallbacks, weights, scales, language coverage, licenses, and legibility constraints |
| Spacing and shape | Semantic rhythm, density, radii, borders, and layout relationships |
| Motion | Meaning, timing, easing, performance budgets, and reduced-motion alternatives |
| Marks | Logos, wordmarks, mascots, variants, clear space, minimum size, backgrounds, and prohibited use |
| Imagery and illustration | Direction, treatment, aspect ratios, attribution, and accessibility guidance |
| Voice and content | Personality, tone by context, vocabulary, naming, examples, anti-examples, and localization |
| Public metadata | Product names, summaries, social metadata, manifests, structured data, and attribution |
| Operational feedback | State, severity, evidence, recovery, and authority cues across interfaces |

Concrete fields and formats belong to #9. This document defines semantic coverage and ownership.

## Semantic interface roles

| Role | Meaning |
| --- | --- |
| Canvas | Primary quiet background or base surface |
| Surface | Grouped content or bounded interaction area |
| Primary | Main action or navigational emphasis |
| Information | Neutral context or observation |
| Success | Completed and verified state |
| Caution | Review required; safe to pause |
| Danger | Destructive, security, privacy, or irreversible risk |
| Unknown | Missing, unavailable, unsupported, partial, or unverified state |

A semantic role describes meaning. A product may override its concrete expression without changing that meaning or weakening its constraints.

## Capability and operational state

Capability documentation uses **implemented**, **accepted**, **proposed**, and **deferred**. Runtime interfaces use **observed**, **planned**, **running**, **partial**, **verified**, **failed**, **blocked**, **unsupported**, and **unknown**. Neither vocabulary may present missing or partial evidence as success.

## Family inheritance

Organization defaults provide semantic continuity. Products own intentional overrides. Generated evidence must identify:

- the inherited value and its source version;
- the override value and declared rationale when required;
- conflicts, deprecated tokens, and unsupported combinations;
- the resolved value used for each projection.

Holon consumes resolved Identity tokens when composing components and templates. It must not create a parallel brand-token source. Identity does not own Holon components.

## Reference Brand Kit structure

The framework-neutral view model supports these public sections when data is present:

1. overview, support state, and version;
2. logos, marks, mascots, and variants;
3. colors, themes, and approved pairings;
4. typography and type scale;
5. voice, personality, and messaging;
6. usage rules and do/don't examples;
7. imagery, motion, and accessibility guidance;
8. downloads, packages, and integration instructions;
9. provenance, licenses, changelog, and compatibility.

Missing or unsupported sections remain explicit rather than filled with invented content.

## Content and interaction principles

- Use verbs that describe the actual operation.
- Put scope and consequence before confirmation.
- Separate preview, approval, application, and publication.
- Pair errors with recovery guidance and evidence locations.
- Preserve stable identifiers in machine-readable output.
- Make copy and download feedback perceivable without relying on color or motion.
- Keep destructive and irreversible actions visually and textually distinct.

## Accessibility contract

Supported projections and the reference renderer must account for contrast, semantic structure, alternative text, keyboard access, visible focus, target size, reduced motion, no-color operation, maskable safe zones, responsive behavior, font fallback, and small-size mark legibility. Automated checks must identify their coverage; human review remains required where automation cannot establish usability.

## Framework boundary

Tokens, content, manifests, and the Brand Kit view model are canonical contracts. CSS, Tailwind, component frameworks, Storybook integrations, static-site renderers, and provider SDKs are projections or adapters selected through #7. No adapter may become required to interpret the source contract.

## Visual direction

Ego Hygiene's family expression may be cosmic, expressive, and adaptive, but those are consumer-owned values rather than hard-coded Identity behavior. Identity preserves the ability for every product to express a distinct accessible identity through the same semantic contract.

