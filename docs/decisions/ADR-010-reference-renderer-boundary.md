# ADR-010: Render from a framework-neutral immutable view model

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

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

## Consequences

- Renderer work can evolve without changing `.identity/` or generated packages.
- The first adapter aligns with existing organization skills and CI.
- Static/export behavior must be proven in #14; Vite's existence alone does not
  establish prerendering or accessibility.
- Holon remains replaceable and separately owned.

## Exit strategy

A replacement renderer consumes the same view-model fixtures and passes the
static route, semantic HTML, accessibility, download, metadata, and visual
acceptance suite.

## Evidence

- [Vite static deployment guidance](https://vite.dev/guide/static-deploy.html)
- [Ego Hygiene website](https://github.com/egohygiene/egohygiene.io)

