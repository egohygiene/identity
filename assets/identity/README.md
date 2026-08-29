# identity brand assets

These files are the first human-approved self-hosting visual projection for the `identity` product.

## Structure

- `brand/` — approved README banners plus deterministic SVG emblem, avatar, lockup, social, and Open Graph projections.
- `guidelines/` — deterministic SVG palette, design-system, and usage-guideline boards.
- `mascot/` — approved full, portrait, and icon projections of Kern plus their byte-bound package manifest.
- `reference/` — lightweight raster previews preserving the AI-assisted visual exploration selected during review.
- `web/` — favicon, Apple touch, PWA/maskable SVG icons, web manifest, and CSS palette projection.
- `manifest.json` — dimensions, checksums, palette values, approval state, and generation provenance.

## Authority boundary

These files are **generated brand outputs**, not a replacement for canonical identity intent. The accepted Identity architecture keeps human-reviewed intent under a consumer-owned `.identity/` contract and generated outputs under `assets/identity/` or versioned packages.

The visual direction was explicitly selected and approved on 2026-08-22. When the v1 `.identity/` source contract is promoted to `main`, this kit should become the golden self-hosting fixture and be reproducible from reviewed source.

Kern's character system received its own explicit review on 2026-08-29. Its
canonical source, approval, provenance, accessibility guidance, derivative
record, and artwork license live in the repository's top-level `mascot/`
directory. This portable Brand Kit retains the exact derivatives and their
[`mascot/manifest.json`](mascot/manifest.json).

## Palette

| token | value |
| --- | --- |
| obsidian | `#0A0A0E` |
| ivory | `#F2EFE9` |
| aureus | `#D4AF6A` |
| champagne | `#CDBA9A` |
| lavender spectrum | `#BCA9FF` |
| deep violet | `#6A4CFF` |
| luminous blue | `#6EA8FF` |

## Integration targets

The `web/` directory is intentionally ready to feed repository surfaces such as Repository Intelligence, Zensical documentation, LaunchKit-derived landing pages, and future Identity package projections without making those frameworks canonical to the brand model.
