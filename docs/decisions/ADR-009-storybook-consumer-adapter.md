# ADR-009: Keep Storybook at the consumer integration boundary

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

## Context

The organization website already uses React, Vite, Storybook, Vitest, and
Playwright. Identity needs a way to demonstrate token and asset consumption
without owning or duplicating Holon's component library.

## Decision

Adapt Storybook as an optional consumer documentation and component-test
target. Identity may publish packages, view-model fixtures, profile examples,
or configuration helpers that stories consume. Holon owns components and
stories that define component behavior.

Reject Storybook as canonical source, compiler dependency, public Brand Kit
contract, or required runtime. Reject Chromatic as a required release service;
consumers may opt into it independently.

## Consequences

- Consumer components can prove that Identity packages work across states and
  themes.
- The Rust core has no Storybook or Node dependency.
- Storybook version churn is isolated to adapters and consumer workspaces.
- Component accessibility evidence complements but does not replace public-route
  or generated-asset validation.

## Exit strategy

Another workshop can consume the same published packages and fixtures. Identity
remains valid when no consumer installs Storybook.

## Evidence

- [Storybook documentation](https://storybook.js.org/docs)
- [Storybook accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing)

