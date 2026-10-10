---
schema: egohygiene.architecture-decision/v1
id: ADR-011
title: Layer normative, exact, browser, and human quality evidence
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
implementation_status: in_progress
evidence:
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-011 with its scope qualifiers and exact N011 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-011-accessibility-and-visual-evidence.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N011 and its evidence and implementation limits.
- type: implementation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/.github/workflows/reference-renderer.yml
  description: The browser workflow exists but does not yet establish the complete environment pinning required by this decision.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-011: Layer normative, exact, browser, and human quality evidence

## Context

Generated files, component states, and the published Brand Kit need different
forms of quality evidence. Automated accessibility tools cover only a subset of
WCAG, while browser screenshots vary when their environment is not pinned.

## Decision

Adopt WCAG 2.2 AA as the public-surface baseline. Adapt `axe-core` through
Storybook and Playwright for automated DOM checks while retaining explicit
manual review. Adopt first-party exact checks for generated artifacts:
dimensions, formats, byte budgets, transparency, safe zones, metadata, hashes,
pixels, and golden manifests.

Adapt Playwright screenshots for integrated public surfaces in a pinned browser
container with fixed fonts, viewport, locale, time zone, scale, animation, and
color settings. Reject DSSIM for v1 because its AGPL/commercial licensing and
threshold calibration are unnecessary. Reject Chromatic as a mandatory gate
because the deterministic core must remain offline.

## Alternatives considered and rejected

The original Decision section above records its rejected or deferred
approaches. No additional historical alternatives or rationale are inferred
by this migration.

## Consequences and tradeoffs

- Every automated report declares its coverage and unresolved manual checks.
- Golden changes require human review and cannot self-approve.
- Browser baselines are environment-specific evidence rather than universal
  renderer truth.
- Accessibility, provenance, license, and approval failures can block release.

## Implementation and evidence links

Exact artifact checks, browser accessibility checks and reviewed screenshot
fixtures provide partial implementation. The complete pinned execution
environment remains in progress. See N011 for the approved limits; this record
does not claim complete accessibility conformance or a fresh verification run.

### Original evidence links

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [`axe-core`](https://github.com/dequelabs/axe-core)
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [DSSIM licensing and behavior](https://github.com/kornelski/dssim)

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

Tools may be replaced when they emit equivalent evidence and pass the same
fixtures. The normative WCAG and platform-profile outcomes remain stable even
when automation changes.

## Follow-up work

Complete the pinned browser environment and retain explicit manual review
evidence and unresolved coverage, as required by N011.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-011-accessibility-and-visual-evidence.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N011 — Accessibility and reproducibility limits

Exact package checks, browser accessibility checks and reviewed screenshot
fixtures exist, but the full environment pinning required here is not yet
established by the reference-renderer workflow. It uses `ubuntu-latest` and a
version-pinned Playwright browser without a pinned container image or explicit
locale/time-zone configuration. Retain the stricter reproducibility requirement
as remaining implementation work. Automated passes do not constitute complete
WCAG conformance or replace manual review.

Evidence: [workflow](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/.github/workflows/reference-renderer.yml) and
[Playwright configuration](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/renderer/playwright.config.js).
