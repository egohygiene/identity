---
schema: aether.architecture-document/v1
id: identity-brand-kit-foundations-evaluation
title: Brand Kit Foundations Evaluation
kind: evaluation
version: 1.0.0
status: active
owners:
  - egohygiene
created: 2026-08-20
updated: 2026-08-20
governed_by:
  - identity-architecture
depends_on:
  - identity-design-system
related:
  - identity-decisions
  - identity-dependency-policy
supersedes: []
---

# Brand Kit foundations evaluation

## Decision summary

Identity will own a small, deterministic Rust domain and compiler core. It will
adopt public standards as contracts, adapt mature tools behind ports, and keep
JavaScript and browser tooling at projection, documentation, and public-surface
boundaries. No evaluated tool becomes canonical domain truth.

| Area | Decision | Selected foundation | Boundary and replacement |
| --- | --- | --- | --- |
| Design tokens | Adopt | [DTCG Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/) | Canonical token interchange only; Identity extensions own non-token brand concepts. A future DTCG revision is accepted through a versioned parser and migration. |
| Token projections | Adapt | [Style Dictionary](https://styledictionary.com/) | Optional Node adapter over Identity's resolved token model. Replace with first-party formatters or another adapter without changing `.identity/`. |
| Schema | Adopt and adapt | [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) and Rust [`jsonschema`](https://github.com/Stranger6667/jsonschema) | Published schemas are the public contract. The validator is replaceable behind an offline validation port; migrations remain first-party domain behavior. |
| Vector and raster | Adopt | Rust [`usvg`/`resvg`](https://github.com/linebender/resvg) with its `tiny-skia`, `fontdb`, and text stack | Renderer adapter receives explicit fonts and options. Golden fixtures protect replacement by another SVG 2D implementation. |
| Fonts | Adapt | [`skrifa`/`read-fonts`](https://github.com/googlefonts/fontations) for inspection; pinned [`fontTools`](https://fonttools.readthedocs.io/en/latest/) subprocess for approved subsetting | Inspection, shaping, subsetting, and license approval are separate ports. Subsetting is optional and fails closed when rights are absent. |
| Platform metadata | Adopt | Primary platform specifications | Identity-owned profile serializers and validators; no third-party metadata package is canonical. |
| Component workshop | Adapt | [Storybook](https://storybook.js.org/docs) | Consumer documentation/test adapter only. Holon owns components; Identity owns tokens, packages, and the Brand Kit view model. |
| Reference renderer | Adapt | React/Vite static consumer over a framework-neutral view model | First adapter matches the organization website. The immutable view model and plain-HTML acceptance fixture provide the exit path. |
| Accessibility | Adopt and adapt | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [`axe-core`](https://github.com/dequelabs/axe-core), and human review | WCAG is normative; automated tools report bounded coverage and never replace human review. |
| Visual regression | Adapt | Exact artifact checks plus pinned [Playwright screenshots](https://playwright.dev/docs/test-snapshots) for public surfaces | Core assets use byte/pixel/golden evidence. Browser snapshots run in a pinned container and can be replaced through fixture compatibility. |

## Decision criteria

The evaluation uses these priorities in order:

1. deterministic, offline operation and explicit inputs;
2. license compatibility and auditable provenance;
3. standard interoperability and replaceable adapter boundaries;
4. cross-platform behavior and stable local/CI parity;
5. accessibility, diagnostics, and testability;
6. project health, performance, artifact size, and supply-chain cost;
7. Rust/JavaScript boundary cost.

`Adopt` means the contract or implementation is the preferred v1 foundation.
`Adapt` means it is allowed only behind an Identity-owned port. `Reject` means
it is not part of the required v1 stack; it may be reconsidered with new
evidence.

## Comparison matrix

### Token contract and transformation

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| DTCG 2025.10 | The [stable community specification](https://www.designtokens.org/tr/2025.10/format/) defines tokens, groups, aliases, composite values, types, and extensions. It explicitly notes that it is not a W3C Recommendation. | Interoperable vocabulary; typed values; aliases; extension mechanism; tool-neutral JSON. | It does not model the whole Brand Kit, and its accompanying JSON Schema remains incomplete. Future revisions require migration. | **Adopt** as the versioned token interchange subset of `.identity/`, not as the entire Identity schema. |
| Style Dictionary | The [official DTCG guidance](https://styledictionary.com/info/dtcg/) reports first-class DTCG support while warning that 2025.10 is not fully supported. Its [configuration hooks](https://styledictionary.com/reference/config/) expose preprocessors, transforms, formats, and filters. Apache-2.0. | Mature cross-platform outputs; extensible; existing ecosystem; good CSS/native projection reach. | Node runtime and supply chain; internal merge semantics could conflict with Identity; current DTCG gap. | **Adapt** after Identity validation/resolution. Never read unvalidated canonical state or write canonical state. |
| Style Dictionary as source of truth | Same evidence as above. | Fewer initial layers. | Couples the public contract to one tool, exposes unsupported DTCG behavior, and mixes resolution with projection. | **Reject**. |
| Identity-only token format | DTCG already covers the interoperable token concern. | Total implementation control. | Reinvents a standard and makes exchange harder. | **Reject** for token concepts. Identity extensions remain valid for assets, voice, approvals, provenance, and target profiles. |

### Schema authoring, validation, completion, and migration

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| JSON Schema Draft 2020-12 | The [official specification](https://json-schema.org/draft/2020-12) defines validation and reusable vocabularies supported by editor tooling. | Language-neutral public contract; editor completion through `$schema`; composable validation; broad tooling. | JSON Schema cannot express every semantic or filesystem invariant; remote references can break offline builds. | **Adopt**. Vendor all release schemas and meta-schemas; layer semantic diagnostics in Rust. |
| Rust `jsonschema` | The [project](https://github.com/Stranger6667/jsonschema) supports major drafts, custom formats, meta-schema validation, structured output, and configurable reference resolution under MIT. | Native runtime boundary; structured diagnostics; no JS needed for core validation. | Optional network/TLS features and MSRV changes add supply-chain cost. | **Adapt** with remote resolution disabled and an explicit feature set. |
| Generated schema as canonical contract | Rust schema generators can mirror data structures. | Reduces duplicate authoring. | Implementation details can silently reshape the public contract and documentation. | **Reject**. Generation may detect drift but cannot own the published schema. |
| Library-driven migrations | Generic JSON transformation libraries can edit documents. | Less custom code. | Cannot own Identity's semantic compatibility, approval, or rollback behavior. | **Reject**. Migrations are versioned first-party application use cases. |

### Vector, raster, and deterministic rendering

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| `usvg` + `resvg` | The [resvg project](https://github.com/linebender/resvg) provides a Rust SVG simplifier, renderer, rasterizer, shaping stack, and font database under MIT/Apache-2.0. | Pure Rust; small native boundary; explicit font database; strong SVG conformance; portable library and CLI. | Output can drift with dependency, font, or encoder changes; not every browser SVG feature is supported. | **Adopt** behind vector/raster ports with pinned versions, approved embedded fonts, and golden output evidence. |
| Browser/canvas rendering | Browser engines can render HTML, SVG, CSS, and text. | High fidelity to web presentation. | OS, browser, GPU, font discovery, and timing vary; expensive for CLI core. | **Reject** as the canonical asset renderer; retain only for public-surface tests. |
| ImageMagick/Inkscape shell-outs | Mature, broad file support. | Powerful conversion and authoring behavior. | External binaries, environment-specific builds, broad attack surface, and harder cross-platform parity. | **Reject** as required v1 dependencies. Optional import adapters may be reconsidered. |
| Custom SVG renderer | Full control. | Exact feature scope. | Reinvents parsing, text shaping, paint, filters, and rasterization. | **Reject**. |

Determinism means identical bytes for the same normalized source, dependency
lock, font bytes, renderer options, target triple, and encoder settings. It does
not mean different dependency versions or system fonts are equivalent.

### Font inspection, subsetting, licensing, and rendering

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| Fontations `read-fonts`/`skrifa` | [Fontations](https://github.com/googlefonts/fontations) provides Rust parsing, metadata, outlines, metrics, variations, and write-oriented crates under MIT/Apache-2.0. | Memory-safe Rust direction; structured metadata; useful inspection boundary. | Subsetting support is newer than mature Python tooling; supported table coverage evolves. | **Adapt** for inspection and policy evidence. Re-evaluate its subsetter after corpus parity tests. |
| `ttf-parser`/`fontdb`/`rustybuzz` | These are part of the selected [resvg stack](https://github.com/linebender/resvg). | Proven integration for deterministic SVG text rendering. | Duplicating font parsers elsewhere can increase binary and maintenance cost. | **Adopt transitively** inside the renderer; do not expose their types as domain contracts. |
| fontTools `pyftsubset` | The [official documentation](https://fonttools.readthedocs.io/en/latest/) identifies `pyftsubset` as the maintained subsetting utility and records the MIT license. | Mature OpenType coverage; explicit glyph/features controls; WOFF/WOFF2 support. | Python subprocess and lock; output changes across versions; subsetting can violate font licenses. | **Adapt** as an optional, exactly pinned offline subprocess. Preserve original license records and require explicit subsetting rights. |
| Download fonts during rendering | Provider APIs can simplify first use. | Convenient. | Non-deterministic, privacy-sensitive, network-dependent, and licensing provenance can be lost. | **Reject**. Canonical source names approved local font bytes and license evidence. |

### Metadata and platform profiles

| Contract | Primary evidence | v1 treatment |
| --- | --- | --- |
| Open Graph | [Open Graph protocol](https://ogp.me/) | Identity-owned serializer for required properties, image metadata, locale, and alternative text. |
| Web application manifest | [W3C Web Application Manifest](https://www.w3.org/TR/appmanifest/) | Validate members and icon purposes `any`, `maskable`, and `monochrome`; validate the maskable safe zone. |
| HTML icons | [WHATWG `rel=icon`](https://html.spec.whatwg.org/multipage/links.html#rel-icon) | Generate declared icon resources and link metadata; do not treat historical platform files as universally required. |
| GitHub repository preview | [GitHub documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) | Profile constraint: 1280×640 preferred, supported format, byte budget, and explicit safe-area validation. |
| Apple web icons | [Apple web application guidance](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html) | Versioned platform profile with provenance; archived guidance is not generalized to unrelated targets. |
| Structured data | [Schema.org](https://schema.org/) and [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) | Optional profile serializer validated independently from Open Graph. |

Generic metadata packages are **rejected as canonical truth**. These formats are
small enough to serialize from first-party typed profiles, while adapters can
still be added for consumer frameworks.

### Storybook and reference rendering

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| Storybook consumer adapter | [Storybook](https://storybook.js.org/docs) isolates component states and integrates documentation and tests. The organization website already uses React, Vite, Storybook, Vitest, and Playwright. | Existing ecosystem fit; documents Holon components consuming Identity packages; useful edge-state fixtures. | Large Node dependency graph; framework/version churn; tempting duplicate component ownership. | **Adapt** in web consumers. Identity may ship fixtures/config helpers, never Holon components or canonical source. |
| Storybook as the public Brand Kit | Storybook is a component workshop rather than Identity's public contract. | Fast internal documentation. | Couples public information architecture to a development tool and weakens static portability. | **Reject**. |
| React/Vite reference adapter | [Vite static deployment guidance](https://vite.dev/guide/static-deploy.html) and the current organization website stack. | Direct integration path; reuses Holon; static build; existing tests. | React/Vite churn and JavaScript supply chain. | **Adapt** as the first public renderer, consuming only the immutable Brand Kit view model. |
| Astro/Next/Zola as a required renderer | Each can produce static sites. | Strong page-generation features. | Adds a second website architecture before a demonstrated need; Zola also introduces a separate template/component path. | **Reject for v1**. Reconsider only if the React/Vite adapter cannot meet static metadata, accessibility, or performance gates. |

### Accessibility and visual regression

| Candidate | Evidence | Strengths | Material risks | Decision |
| --- | --- | --- | --- | --- |
| WCAG 2.2 | [W3C Recommendation](https://www.w3.org/TR/WCAG22/) | Normative success criteria and testable outcomes. | Not all criteria are automatable. | **Adopt** as the public renderer baseline, targeting AA unless a profile states a stronger requirement. |
| `axe-core` | The [official project](https://github.com/dequelabs/axe-core) supports WCAG rules and explicitly reports incomplete findings requiring manual review. MPL-2.0. | Mature browser automation; integrates with existing web tests. | Partial coverage; test dependency licensing and versioned rules require review. | **Adapt** for rendered DOM checks, with manual evidence required. |
| Storybook accessibility addon | [Official documentation](https://storybook.js.org/docs/writing-tests/accessibility-testing) integrates `axe-core` with component stories and CI. | Catches component-state issues before integration. | Does not validate the packaged assets or entire published route. | **Adapt** in consumers, not the core compiler. |
| Playwright screenshots | [Official documentation](https://playwright.dev/docs/test-snapshots) supports screenshot baselines and warns that host environments affect rendering. | Already present in the website stack; covers integrated route behavior. | Flaky without pinned browser, OS image, fonts, viewport, animations, and locale. | **Adapt** in a pinned container with reviewed baselines. |
| Exact artifact checks | Cryptographic hashes, dimensions, pixels, metadata, and golden manifests are first-party evidence. | Offline, cheap, deterministic, and suitable for compiler outputs. | Exact baselines require intentional review when renderers change. | **Adopt** for generated assets. |
| DSSIM | The [project](https://github.com/kornelski/dssim) provides perceptual image comparison but is AGPL-3.0/commercial. | Useful perceptual scoring. | License and threshold calibration add avoidable v1 complexity. | **Reject for v1**. |
| Chromatic as a release requirement | Storybook offers it as a hosted visual-testing integration. | Managed cross-browser review. | Network/service dependency, account state, and external retention conflict with offline core guarantees. | **Reject as required**; consumers may opt in without changing Identity's gates. |

## Reproducibility contract

Local and CI builds are equivalent only when they use:

- the committed lockfiles and exact direct tool versions;
- the same Rust toolchain, Node/pnpm versions, target, and container image;
- approved font files by checksum, never ambient system-font discovery;
- explicit locale, time zone, color profile, viewport, scale, and renderer flags;
- canonical JSON ordering and newline behavior for serialized artifacts;
- no timestamps, random identifiers, network reads, or machine paths in output;
- golden fixtures verified before dependency or baseline promotion.

The proof under `experiments/dtcg-projection-boundary/` demonstrates the
highest-risk contract decision: a DTCG canonical document can be projected
through a replaceable adapter without mutation, ambient state, or unstable
ordering. Renderer golden tests move into the extracted workspace in #8 and the
compiler work in #10.

## Deferred validation

This issue selects boundaries; it does not claim that the standalone runtime
exists. The following evidence belongs to its owning issue:

- #8: extracted CLI parity and real Rust dependency locks;
- #9: full JSON Schemas, semantic validation, and migrations;
- #10–#11: renderer/encoder contracts, golden asset corpus, packages, and SBOM;
- #12: release-blocking accessibility, provenance, license, and visual evidence;
- #14: reference renderer, static-export proof, and public-surface tests.

