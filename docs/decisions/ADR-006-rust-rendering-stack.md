---
schema: "egohygiene.architecture-decision/v1"
id: "ADR-006"
title: "Use a pinned Rust vector and raster stack"
status: "accepted"
date: "2026-10-10"
decision_scope: "repository"
visibility: "public"
owners: ["egohygiene/identity"]
issue: "https://github.com/egohygiene/identity/issues/69"
pull_request: "https://github.com/egohygiene/identity/pull/92"
related: ["ADR-007", "ADR-008", "ADR-011"]
supersedes: []
superseded_by: []
affected_repositories: ["egohygiene/identity"]
affected_contracts: []
implementation_status: "in_progress"
evidence:
  - type: "approval"
    url: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
    description: "Explicit maintainer szmyty disposition on 2026-10-10 for R1; recorded by Codex on their behalf, not inferred from merge or implementation."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md"
    description: "Approved R1 recommendation set and exact scope clarifications at the reviewed immutable packet commit."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-006-rust-rendering-stack.md"
    description: "Immutable pre-canonicalization record preserving its historical wording, date, status claim, and provenance."
  - type: "commit"
    url: "https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374"
    description: "Original record introduction; evidence of recorded history rather than proof of historical human approval."
  - type: "implementation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/brandkit/render.rs"
    description: "Inspected implementation or governing source contract; bounded evidence, not a newly executed verification result."
approval:
  date: "2026-10-10"
  by: "szmyty"
  evidence: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
exceptions: []
---

# ADR-006: Use a pinned Rust vector and raster stack

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

## Alternatives considered and rejected

The original Decision section above preserves its rejected alternatives verbatim. No additional contemporaneous alternatives or rejection rationale were established by this migration.

## Consequences and tradeoffs

- The core remains offline and avoids a Node/browser runtime for asset output.
- Unsupported SVG features require clear diagnostics or preprocessing.
- Dependency and font changes can alter pixels and must trigger reviewed golden
  diffs.
- Platform equivalence is proven for an explicit support matrix rather than
  assumed across arbitrary environments.

## Implementation and evidence links

- [`usvg`/`resvg` project and license](https://github.com/linebender/resvg)

The inspected dependency graph and raster adapter use pinned resvg/usvg/tiny-skia with default features disabled. Approved-font injection and broader golden-build requirements are not completed implementation claims; implementation remains in progress as clarified by N006 below.

[Inspected source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/brandkit/render.rs). The front-matter implementation status is independent of human acceptance. No new runtime, browser, release, or deployment verification is claimed.

[PR #20](https://github.com/egohygiene/identity/pull/20) introduced the original record in [commit `13c0824090755587efc3f65dca4638f6d8186374`](https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374) on 2026-08-20. That introduction does not prove a historical approval date.

## Replacement or exit strategy

All renderer adapters consume a normalized scene/asset request and emit the
same artifact/evidence contract. A replacement must pass SVG corpus, pixel,
metadata, performance, and cross-platform fixtures before promotion.

## Follow-up work

Validate the final canonical corpus and index through the pinned shared tools at an immutable source revision. Preserve current implementation limitations and obtain separate evidence for future capability, release, and publication claims. Acceptance of this direction does not require completing every planned adapter before ADR source admission.

## Current human disposition — 2026-10-10

Maintainer `szmyty` explicitly retained this direction now under [R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md). The [durable approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) was recorded by Codex on the maintainer's behalf. The canonical date and approval date record this current human disposition; they do not backdate acceptance to the legacy record date or establish additional implementation or publication authority.

## Approved clarification — 2026-10-10

The following N006 text is preserved verbatim from the approved R1 packet.

### N006 — Rendering implementation boundary

Retain the pinned `resvg`/`usvg`/`tiny-skia` boundary for asset rendering.
Current implementation covers the selected raster profiles with default
features disabled and no ambient-font loading. Approved-font injection,
explicit settings for any enabled text/shaping path, and broader golden-build
equivalence remain requirements, not claims of completed implementation.

Evidence: [dependency manifest](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/Cargo.toml),
[lockfile](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/Cargo.lock) and [raster adapter](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/brandkit/render.rs).

## Historical metadata and provenance

The following original metadata is preserved as historical evidence. Its status and date lines are legacy claims, not the current approval record. [Original record at `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-006-rust-rendering-stack.md).

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)
