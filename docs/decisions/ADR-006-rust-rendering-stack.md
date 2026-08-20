# ADR-006: Use a pinned Rust vector and raster stack

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

## Context

Identity must generate SVG and raster targets consistently on macOS, Linux, and
CI without relying on ambient browsers, system fonts, or separately installed
desktop applications.

## Decision

Adopt `usvg` and `resvg`, including their selected `tiny-skia`, font database,
parsing, and shaping stack, behind Identity-owned vector and raster ports. Pass
approved fonts and every rendering option explicitly. Pin the Rust toolchain,
crate graph, target, encoder settings, and fixture fonts for golden builds.

Reject browser/canvas rendering, ImageMagick/Inkscape shell-outs, and a custom
SVG renderer as required v1 core dependencies. Browser rendering remains
appropriate for public-route integration tests.

## Consequences

- The core remains offline and avoids a Node/browser runtime for asset output.
- Unsupported SVG features require clear diagnostics or preprocessing.
- Dependency and font changes can alter pixels and must trigger reviewed golden
  diffs.
- Platform equivalence is proven for an explicit support matrix rather than
  assumed across arbitrary environments.

## Exit strategy

All renderer adapters consume a normalized scene/asset request and emit the
same artifact/evidence contract. A replacement must pass SVG corpus, pixel,
metadata, performance, and cross-platform fixtures before promotion.

## Evidence

- [`usvg`/`resvg` project and license](https://github.com/linebender/resvg)

