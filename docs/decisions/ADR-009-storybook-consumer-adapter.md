---
schema: egohygiene.architecture-decision/v1
id: ADR-009
title: Keep Storybook at the consumer integration boundary
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
implementation_status: not_started
evidence:
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-009 with its scope qualifiers and exact N009 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-009-storybook-consumer-adapter.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N009 and its evidence and implementation limits.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/renderer/package.json
  description: The current reference renderer has no Storybook dependency; the optional consumer adapter remains unimplemented.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-009: Keep Storybook at the consumer integration boundary

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

## Alternatives considered and rejected

The original Decision section above records its rejected or deferred
approaches. No additional historical alternatives or rationale are inferred
by this migration.

## Consequences and tradeoffs

- Consumer components can prove that Identity packages work across states and
  themes.
- The Rust core has no Storybook or Node dependency.
- Storybook version churn is isolated to adapters and consumer workspaces.
- Component accessibility evidence complements but does not replace public-route
  or generated-asset validation.

## Implementation and evidence links

The optional Storybook consumer adapter is not started in the inspected
Identity source. The separate reference renderer exists and does not require
Storybook. See N009 for the approved scope and dependency evidence.

### Original evidence links

- [Storybook documentation](https://storybook.js.org/docs)
- [Storybook accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing)

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

Another workshop can consume the same published packages and fixtures. Identity
remains valid when no consumer installs Storybook.

## Follow-up work

Add a Storybook consumer adapter only when a consumer needs one; retain its
optional status and the ownership boundary clarified by N009.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-009-storybook-consumer-adapter.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N009 — Optional Storybook integration

Storybook remains an optional consumer integration direction. Identity
currently contains no Storybook installation or delivered consumer adapter.
Its standalone renderer uses React/Vite with Vitest, Playwright and axe-core.
Retaining this decision does not require adding Storybook or Chromatic, and
does not establish any consumer's current toolchain.

Evidence: [renderer manifest](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/renderer/package.json) and
[renderer contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/BRAND_KIT_RENDERER_V1.md).
