# Brand Kit reference renderer contract v1

## Status

- Contract: `identity.brand-kit-view-model/v1`
- Reference adapter: React 19 + Vite
- Owning issue: [Identity #14](https://github.com/egohygiene/identity/issues/14)
- Governing decision:
  [ADR-010](../decisions/ADR-010-reference-renderer-boundary.md)

## Purpose

The reference renderer presents one immutable generated Brand Kit as an
accessible, navigable, downloadable static page. It is a presentation adapter,
not a source-of-truth editor.

```text
consumer-owned .identity/
        |
        v
Identity validate -> resolve -> package
        |
        v
packages/renderer/brand-kit.view-model.json
        |
        v
replaceable renderer adapter
        |
        v
static HTML/CSS/JavaScript + generated downloads
```

## Input contract

The compiler emits:

```text
assets/identity/packages/renderer/brand-kit.view-model.json
```

The JSON Schema is
[`contracts/v1/brand-kit-view-model.schema.json`](../../contracts/v1/brand-kit-view-model.schema.json).

The view model contains only public, approved, renderer-relevant projections:

- project display metadata;
- immutable release and source digests;
- ordered semantic tokens with lineage and approvals;
- approved source assets with format, dimensions, intended use, download status,
  and optional license/provenance records;
- canonical voice and usage guidance with explicit declaration status;
- explicit motion, imagery, and mascot support status;
- versioned package/download paths.

The renderer must not read `.identity/`, infer missing brand facts, or reach into
a sibling repository.

## Compiler API

Rust consumers compose the existing package request with the renderer target:

```rust
use identity::brandkit::{all_profiles, compiler_request, register_builtin_adapters};
use identity::reference_renderer::{
    register_reference_renderer_adapter,
    with_reference_renderer,
};

let request = with_reference_renderer(
    compiler_request("assets/identity", &all_profiles())?,
);
register_builtin_adapters(&mut registry)?;
register_reference_renderer_adapter(&mut registry)?;
```

The adapter is deterministic, offline, and registered as
`identity-reference-renderer-model@1.0.0`.

## Static rendering guarantees

The reference implementation in [`renderer/`](../../renderer) provides:

- server-rendered essential guidance, provenance, and download links;
- progressive hydration for copy feedback and theme controls;
- direct fragment navigation for every required section;
- light, dark, print, narrow-screen, and reduced-motion policies;
- no dependency on client-side routing;
- a route-relative Vite build configured through `IDENTITY_RENDERER_BASE`;
- a public asset tree sourced only from the generated `assets/identity/` output.

A consumer may mount the `dist/` directory at any immutable route or adapt the
same view model to another framework.

## Authority and missing-data behavior

The renderer labels generated marks, colors, and typography as
**Generated preview**. It labels voice and usage as **Canonical guidance**.

A required section whose data is absent remains visible and reports
**Not declared** or **Unsupported**. This includes undeclared color pairings,
type scales, motion rules, imagery direction, and mascot guidance. The renderer
never fabricates examples, licenses, provenance, or creative rules.

## Theming

The renderer derives CSS custom properties from semantic tokens when present and
retains neutral fallbacks when a token is absent. Consumers may override the CSS
variables without changing or forking the JSON contract.

## Security and privacy

- Approved SVG source is shown through an encoded image data URL, not injected as
  executable markup.
- Static rendering escapes document metadata and embedded JSON.
- No credentials, private source material, provider prompts, or mutable branch
  references enter the view model.
- Download links are constrained to generated release-relative paths.
- Browser tests run against the built static bundle and generated artifacts.

## Validation evidence

The v1 validation suite includes:

- Rust compiler generation, strict deserialization, digest matching, and
  cross-repository byte identity;
- fixture contract parsing;
- semantic and automated accessibility checks, including browser color contrast;
- explicit missing-data tests;
- link and real download-response tests;
- keyboard copy/theme interaction tests;
- route-prefix, responsive, and reduced-motion tests;
- deterministic full-page visual hierarchy assertions;
- a reviewed Playwright desktop viewport screenshot baseline.
