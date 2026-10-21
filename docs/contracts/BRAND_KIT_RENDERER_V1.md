# Brand Kit reference renderer contract v1

## Status

- Contract: `identity.brand-kit-view-model/v1`
- Reference adapter: React 19 + Vite
- Owning issue: [Identity #14](https://github.com/egohygiene/identity/issues/14)
- Governing decision:
  [ADR-0010](../decisions/ADR-0010-reference-renderer-boundary.md)

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
  and optional license/provenance/usage records;
- canonical voice and usage guidance with explicit declaration status;
- explicit motion, imagery, and mascot support status;
- selected package paths and optional source-bound download metadata.

When a consumer supplies the complete generated design-system projection
directory, the renderer may additionally consume:

```text
design-system-handbook.json
design-system-handbook.md
design-context.json
design-context.md
```

The renderer validates the handbook/context schemas, shared project identity,
and declared handbook schema. Both JSON projections must provide their existing
`source.digest` binding as a lowercase 64-character SHA-256 string. The handbook
and context digests must equal each other and `release.sourceDigest` in the Brand
Kit model before rendering the optional Design system section. Missing,
malformed, stale, or mixed-source bindings fail with an explicit error; project
identity alone cannot establish agreement. The handbook uses its existing
required binding, without adding a separate release field or model version.

That section presents approved principles, inheritance,
capability ownership, and artifact downloads. It does not re-author source
facts in renderer configuration, nor does its presence imply that Holon or a
product consumer has implemented an undeclared capability.

An absent design-system pair remains valid. For legacy/v1 coexistence, use the
[shared source-digest migration](SOURCE_DIGEST_V1.md#compatibility-and-release-migration):
regenerate the compiler view model and all four projections from the same source
and corrected immutable tool selection. Historical Python/Windows digests and
older v0 release models receive no aliases or unchecked compatibility fallback.
Keep previous published artifact sets intact and upgrade/roll back the whole set.

When a consumer supplies a generated Press Kit directory, the renderer may
also consume its `press-kit.json` projection and the packaged assets named by
that projection. It validates the Press Kit schema, shared project identity,
and the exact immutable source digest before adding an optional Press and media
kit section. It presents only the approved short/optional paragraph/long
boilerplate, facts, links, contacts,
team biographies, selected assets, usage/legal guidance, and generated
downloads present in the projection. It cannot discover or publish source
facts from `.identity/`.

Copy controls use exact projected boilerplate and fact values. Structured voice
foundation, characteristics, naming rules and practical examples remain
readable under their declared contexts; no profile text is inferred from a fact
label or from another description length. See the
[authoring field map](../consumers/AUTHORING.md#3-adopt-rich-copy-and-usage-when-needed)
and [Press Kit compatibility notes](PRESS_KIT_V1.md#compatibility).

The renderer must not read `.identity/`, infer missing brand facts, or reach into
a sibling repository.

### Public source assets and selected downloads

The generic compiler selects a public asset only when its existing usage
`assets[]` record is approved/public, `status: "active"`, and
`availability: "public"`, with the validated asset ID/path bound to local
provenance. Source rights approval alone does not select an asset for public
display. Internal, candidate, rejected, superseded and unavailable assets stay
out of the public asset model. Missing usage produces an empty public asset
list; it does not invalidate local generation with independently nullable
guidance or discard the complete source/review state.

Asset labels, optional `kind` and optional `notes` come from that selected usage
record. `intendedUse` preserves its supplied notes. These fields do not infer
logo roles, light/dark variants or new artwork from filenames or IDs. Per-asset
rights and approval continue to describe the bound provenance source.

Optional `downloads[]` describes selected source-copy and raster targets:

| Member | Meaning |
| --- | --- |
| `id`, `label` | Target identity and display label |
| `path`, `mediaType`, `profile` | Bundle-relative output path, actual format and selected target profile |
| `sourceAssetId`, `sourceSha256` | Public master asset and SHA-256 of that source's bytes |
| `dimensions` | Supplied/generated dimension description |

`sourceSha256` is not the checksum of a derived PNG. The compiler manifest
records output checksums and sizes. The public asset catalog can contain an
embedded approved master without a selected download target; it must not
invent a file for that master.

The renderer target receives the actual `CompilerRequest` targets through
`with_reference_renderer`. Only matching selected targets become packages or
downloads; an archive is advertised only when its underlying mark is public.
`BrandKitViewModel::from_brand_kit` alone has no target handoff and declares no
generated file links. Selected targets describe generation intent; successful
generation and byte verification establish that those files exist.

The v1 bridge adds distinct selected public SVG masters to the `core` request
as source-copy targets at safe `brand/<downloadName>` paths, using the existing
SVG adapter. An existing matching target is reused; conflicting targets fail
before writes. Selected native profiles can expose the existing favicon/PWA/
maskable/social PNG targets. This introduces no new universal ICO or avatar
adapter. See the [authoring worksheet](../consumers/AUTHORING.md#select-public-masters-and-downloads)
for source selection and proposed
[ADR-0029](../decisions/ADR-0029-selected-public-downloads.md) for this boundary.

## Artifact paths and configured deployment bases

Compatibility rationale is recorded in proposed
[ADR-0024](../decisions/ADR-0024-renderer-artifact-paths.md).

All model-provided download paths are relative to the published bundle:
`assets[].downloadPath`, `packages[].path`, optional `downloads[].path`, every
optional Design System and Press Kit artifact/asset path, and the separately supplied publication
`manifestPath`. Imported models are checked before rendering; URL construction
applies the same shared validator. A generated-download asset requires a path;
an embedded source may omit it or use null.

The path contract is:

- Accept non-empty strings with `/`-separated, non-empty filename segments.
  Remove one optional leading `./`. Reject `.` and `..` segments anywhere else.
- Decode each segment once and serialize it with URI component encoding. This
  preserves safe spaces, Unicode, and existing encoding such as `%20`.
- Reject absolute/rooted URLs and paths, protocol-relative paths, schemes and
  drive prefixes, backslashes, encoded separators, malformed UTF-8/escapes,
  query/fragment delimiters, and control characters (U+0000–001F and U+007F).
  Colons and decoded percent signs are forbidden, including nested encoding
  such as `%252f`. Literal percent filenames are outside this path contract.
- File paths cannot end in `/`. Artifact-directory configuration accepts one
  trailing `/` and applies the same relative-segment rules. Dots within an
  ordinary filename, such as `logo..draft.svg`, are valid.

Validation does not rewrite the imported model or any generated file. Design
System views must identify all four known files in one directory. Press Kit
published paths must remain beneath their declared Press Kit directory.

`--asset-base-url` is separate, explicit deployment configuration. It accepts
relative directories (including `../identity/`), rooted route prefixes, and
absolute HTTP(S) directory URLs. Empty/omitted bases mean `./`; one trailing
slash is ensured. HTTP(S) bases use standard URL serialization. Credentials,
query strings, fragments, protocol-relative bases, other schemes, raw
whitespace/control characters, and backslashes are rejected. Rendering remains
offline; configuring a CDN does not fetch its contents.

| Configured base | Artifact path | Download URL |
| --- | --- | --- |
| `./` | `brand/mark.svg` | `./brand/mark.svg` |
| `../identity` | `./brand/mark.svg` | `../identity/brand/mark.svg` |
| `/products/example/v1` | `packages/tokens/tokens.json` | `/products/example/v1/packages/tokens/tokens.json` |
| `https://cdn.example.test/identity/v1` | `brand/mark.svg` | `https://cdn.example.test/identity/v1/brand/mark.svg` |

Existing compiler-generated package paths retain their targets. Leading `/`
is no longer silently stripped from model paths: put deployment prefixes in
the configured base and supply bundle-relative paths in newly reviewed models.
Do not patch historical published models, source digests, or artifact bytes.
The explicit publication `releaseUrl` remains an external release-page link;
v1 has no generic external-download path variant.

### Browser metadata and local artifact verification

Static rendering accepts optional `--icon-path`, `--apple-touch-icon-path` and
`--web-manifest-path` bundle-relative paths. They use the same safe path rules
and `--asset-base-url` as downloads. An omitted option emits no corresponding
head link; the renderer does not assume that a favicon or manifest was built.

Supplying `--artifact-root` checks advertised local downloads and configured
browser assets before rendering: paths must resolve to nonempty regular files
within that root, including after symlink resolution. Source asset bytes must
match their source checksum. Add `--artifact-manifest` to verify the supported
compiler/publication inventory, output hashes/sizes and source-digest binding.
The manifest option requires an artifact root; its filesystem path is separate
from the bundle-relative paths it inventories.

For example, from `renderer/` after a successful consumer generation:

```bash
pnpm run render -- \
  --model "/path/to/consumer/assets/identity/packages/renderer/brand-kit.view-model.json" \
  --artifact-root "/path/to/consumer/assets/identity" \
  --artifact-manifest "/path/to/compiler-manifest.json" \
  --asset-base-url "/brand/"
```

Supply the actual compiler manifest path. These checks read local bytes only
and never fetch a configured CDN or download URL. Rendering a model alone
remains supported for preview, with no claim of execution or file-integrity
proof.

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
Compose the renderer after all selected targets have been added. The v1
consumer bridge uses its source-aware request to add public master copies
before calling `with_reference_renderer`; the generic profile-only helper
cannot discover additional source masters.

## Static rendering guarantees

The reference implementation in [`renderer/`](../../renderer) provides:

- server-rendered essential guidance, provenance, and download links;
- progressive hydration for copy feedback and theme controls;
- direct fragment navigation for every required section;
- light, dark, print, narrow-screen, and reduced-motion policies;
- no dependency on client-side routing;
- a route-relative Vite build configured through `IDENTITY_RENDERER_BASE`;
- a public asset tree sourced only from the generated `assets/identity/` output.
- optional generated handbook/context rendering through an explicit artifact
  directory, suitable for release-backed static publication.
- optional generated Press Kit rendering through an explicit artifact
  directory, with paths constrained to that generated package.

A consumer may mount the `dist/` directory at any immutable route or adapt the
same view model to another framework.

## Authority and missing-data behavior

The renderer labels generated marks, colors, and typography as
**Generated preview**. It labels voice and usage as **Canonical guidance**.

A required section whose data is absent remains visible and reports
**Not declared** or **Unsupported**. This includes undeclared color pairings,
type scales, motion rules, imagery direction, and mascot guidance. The renderer
never fabricates project claims, licenses, provenance, or creative rules.

### Source-bound color and typography previews

When the optional handbook/context pair is supplied, the color and type sections
read its existing declared token constraints. They show explicit roles,
foreground/background pair results, fallback order and supplied font
license/language/legibility notes. Concrete composite typography values can
produce a specimen; neighboring token names do not invent a hierarchy. Generic
specimen text and contrast sample sizes are labeled presentation examples,
not approved project copy or a new type scale.

The displayed token inventory must agree with both projections, in addition to
the existing project/release/digest binding. A mismatched value, source layer,
type, approval or token set fails before output replacement. Missing optional
constraints remain missing, and the independent legacy preview remains valid.
No source or view-model field is added. See the
[foundation behavior and limits](DESIGN_SYSTEM_V1.md#readable-color-and-typography-foundations)
for contrast precision, supported colors, font availability and licensing.

### Asset rights and compatible inputs

The optional per-asset `usage` object transports existing provenance
`safeZone`, `minimumSize` and `restrictions` text. It accompanies license,
attribution, origin, approval and the asset digest; it does not replace the
separate numeric preview `safeZone` field or derive numeric guarantees from
prose. Source and reference-renderer models omit `usage` when legacy input has
none. Missing rights fields remain absent/null and are shown as not declared,
without a default software license, creator or approval.

The page distinguishes asset rights from trademark guidance and configured
software-license/policy references. Approved usage legal guidance exposes
copyright, attribution and third-party notices; optional Press Kit links keep
the actual policy document and contact owners. The renderer does not infer
permissions from a label, a repository license or a font family name.

The additive `usage` member retains the v1 model identifier, but older strict
Rust readers can reject it as unknown. Pin a compatible compiler, schema and
renderer together before consuming a model that supplies it. Existing models
without `usage` remain accepted; old release artifacts are not edited. Proposed
[ADR-0028](../decisions/ADR-0028-asset-rights-projection.md) records this bounded
compatibility and absence treatment without supplying legal or ADR approval.

The optional `downloads`, asset `kind` and asset `notes` members likewise keep
the v1 identifier and require matching reviewed compiler/schema/renderer pins.
Older strict readers may reject them; omission remains supported. Regenerate
the complete source-bound handoff when adopting them rather than editing an
immutable published package. No model extension supplies human approval.

The separate release publisher preserves missing configured license, origin and
approval as null. Its release-owned byte/archive selection is unchanged: a
truthful missing-data label does not withhold those bytes or establish their
permissions. See the
[publication rights boundary](../publication/IDENTITY_PAGES.md#rights-metadata-and-release-selection).

## Selected presentation profiles

When the immutable model's existing public `downloads[]` contains the native
`github-social-preview` or `social-card-1200x630` target with its matching profile,
PNG media type and source asset/digest, the renderer presents that selected
image, supplied dimensions and source rights. It uses the declared artifact
path under the configured base; it does not discover or guess a file.

The same view copies project name/tagline/repository and existing generated
Press Kit boilerplates, facts and links exactly. Labels do not activate registry
or account behavior. Empty/absent downloads retain the prior kit and omit this
section/navigation. Source and view-model fields are unchanged; the schema adds
an optional named `githubSocialPreviewDownload` definition for the existing
GitHub artifact, linked to its retained layout reference.
See the [selected-profile guide](../consumers/PRESENTATION_PROFILES.md) for
bounded targets, actual consumer proof and manual upload requirements.

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
- Press Kit assets and bundle links are constrained to their generated
  Press Kit directory; a differing project ID or source digest fails closed.
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
- a cross-language handoff test that generates a consumer projection with
  `render_design_system.py` and renders those exact artifacts into static HTML.
- a cross-language handoff test that generates an approved Press Kit and
  refuses a different project before static rendering.
