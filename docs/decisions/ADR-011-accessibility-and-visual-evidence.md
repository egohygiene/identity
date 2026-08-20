# ADR-011: Layer normative, exact, browser, and human quality evidence

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

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

## Consequences

- Every automated report declares its coverage and unresolved manual checks.
- Golden changes require human review and cannot self-approve.
- Browser baselines are environment-specific evidence rather than universal
  renderer truth.
- Accessibility, provenance, license, and approval failures can block release.

## Exit strategy

Tools may be replaced when they emit equivalent evidence and pass the same
fixtures. The normative WCAG and platform-profile outcomes remain stable even
when automation changes.

## Evidence

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [`axe-core`](https://github.com/dequelabs/axe-core)
- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [DSSIM licensing and behavior](https://github.com/kornelski/dssim)

