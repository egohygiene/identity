---
schema: egohygiene.architecture-decision/v1
id: ADR-010
title: Render from a framework-neutral immutable view model
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
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-010 with its scope qualifiers and exact N010 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-010-reference-renderer-boundary.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N010 and its evidence and implementation limits.
- type: implementation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/reference_renderer.rs
  description: The immutable versioned renderer model is implemented; no fresh browser run or deployment is inferred.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-010: Render from a framework-neutral immutable view model

## Context

The public Brand Kit must integrate with `egohygiene.io`, export statically, and
remain portable if the website framework changes. Identity must not fork Holon
components or make a frontend framework necessary to interpret brand data.

## Decision

Make the versioned, immutable Brand Kit view model the renderer input and public
port. Adapt React/Vite as the first reference renderer because it matches the
current website stack and can consume Holon components. Require a static build,
direct route loading, metadata, no-JavaScript content availability for essential
guidance/downloads, and an acceptance fixture rendered without Holon internals.

Reject Astro, Next.js, Zola, and a Storybook deployment as required v1
foundations. They can be reconsidered only with evidence that the first adapter
cannot meet static export, accessibility, performance, or integration gates.

## Alternatives considered and rejected

The original Decision section above records its rejected or deferred
approaches. No additional historical alternatives or rationale are inferred
by this migration.

## Consequences and tradeoffs

- Renderer work can evolve without changing `.identity/` or generated packages.
- The first adapter aligns with existing organization skills and CI.
- Static/export behavior must be proven in #14; Vite's existence alone does not
  establish prerendering or accessibility.
- Holon remains replaceable and separately owned.

## Implementation and evidence links

The versioned immutable view-model port and React/Vite static adapter are
implemented in the inspected source. No new browser verification or live
publication is claimed. See N010 for the approved current-evidence boundary.

### Original evidence links

- [Vite static deployment guidance](https://vite.dev/guide/static-deploy.html)
- [Ego Hygiene website](https://github.com/egohygiene/egohygiene.io)

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

A replacement renderer consumes the same view-model fixtures and passes the
static route, semantic HTML, accessibility, download, metadata, and visual
acceptance suite.

## Follow-up work

Retain exact candidate or release evidence for future renderer verification
and publication, within the separate surface boundaries clarified by N010.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-010-reference-renderer-boundary.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N010 — Renderer implementation and current verification

The immutable view-model port and React/Vite static reference adapter are
implemented in repository source. The original reference to future proof in
issue #14 records the historical delivery sequence. Current acceptance must
use evidence for the exact candidate or release; source fixtures alone do not
prove a fresh passing browser run or live deployment. The separate product
experience described by ADR-017 does not replace the release-backed Brand Kit
renderer.

Evidence: [view-model implementation](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/reference_renderer.rs),
[view-model schema](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/contracts/v1/brand-kit-view-model.schema.json) and
[static adapter](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/renderer/scripts/render-static.mjs).
