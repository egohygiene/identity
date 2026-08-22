# Brand Kit packages v1

## Contract boundary

Identity's v1 package layer projects an already validated and resolved identity
into portable generated artifacts. The package layer is downstream of the
compiler contract and upstream of consumer integration:

```text
.identity/ source
      ↓ validate + resolve
resolved Brand Kit model
      ↓ versioned output profiles
compiler plan → render → verify → manifest
      ↓
assets/identity/ + distributable package files
```

Generated files are reproducible projections. They never become canonical
identity source merely because a consumer commits, copies, publishes, or
installs them.

The package implementation is offline and deterministic. It consumes only the
resolved model, approved local source bytes, versioned profile parameters, the
pinned Rust dependency graph, and the compiler's explicit existing-output
state. It does not download fonts, images, templates, or metadata.

## Resolved Brand Kit model

The package adapters consume `identity.brand-kit-model/v1`, a framework-neutral
view of resolved source state with:

- project ID, display name, repository URL, and tagline;
- flattened semantic token paths with resolved values and token types;
- source-layer lineage plus intentional override reason and approval ID;
- approved source assets with media type, bytes/text, SHA-256, alt text, and
  optional safe-zone evidence;
- optional structured voice and usage guidance.

The v1 source resolver owns how defaults, overrides, aliases, provenance, and
approvals become this model. Projection adapters must not implement a second
merge policy.

## Profile compatibility

Built-in profiles use semantic version `1.0.0`. A consumer selects a profile by
both ID and version. Identity fails closed when the profile is unknown or the
requested version is incompatible.

Within a profile major:

- additive optional artifacts may be introduced only when consumers can ignore
  them safely;
- existing artifact meaning, media type, path, or required semantics do not
  change incompatibly;
- removing or repurposing an artifact requires a profile-major change plus
  migration guidance;
- consumers should pin an immutable Identity release or package release rather
  than a mutable default branch.

A consumer may select only the profiles it needs. Selecting a subset must not
silently generate unrelated profiles.

## Built-in profiles

| Profile | v1 purpose | Stable projections |
| --- | --- | --- |
| `core` | Canonical scalable brand projection | `brand/mark.svg` |
| `web` | Browser identity | `web/favicon.svg`, 32px and 64px PNG favicons |
| `pwa` | Web App Manifest identity | 192px/512px icons, 512px maskable icon, icon metadata |
| `github` | Repository preview | 1280×640 PNG social preview |
| `docs` | Document/presentation styling | generated document CSS |
| `social` | Portable social-card surface | 1200×630 PNG card |
| `tokens` | Programmatic design system | DTCG JSON, CSS, JS, TypeScript declaration, Tailwind-compatible theme, package metadata |
| `metadata` | Public metadata and guidance | metadata JSON, Open Graph HTML, package metadata, voice/usage JSON and Markdown |
| `archive` | Download/distribution | package index, checksums, deterministic ZIP |

Every target is represented as a normal compiler `ProjectionTarget`; plans can
therefore enumerate creation, replacement, removal, unchanged state, drift,
warnings, and required approvals before mutation.

## Token projections

Semantic tokens remain canonical; generated concrete formats do not.

### DTCG JSON

The generated token document preserves the resolved token type/value while
recording Identity projection metadata, source layer, override reason, and
approval reference under a namespaced extension.

### CSS

Supported semantic values are rendered as stable `--identity-*` custom
properties. Token paths use lowercase hyphen-separated identifiers. The
projection is sorted by token path and contains no timestamps or machine paths.

### JavaScript and TypeScript

The JavaScript module exports an immutable path-to-value object. The declaration
file publishes the exact selected token-path union for editor/type-system use.

### Tailwind-compatible theme

The Tailwind projection is plain JSON shaped as `theme.extend` data. It is a
consumer adapter, not canonical Tailwind configuration and not a dependency on
Tailwind itself.

## Raster and platform projections

Raster outputs use the accepted `resvg`/`tiny-skia` adapter boundary with
explicit target dimensions. Rendering does not inspect ambient system fonts.
The approved canonical SVG source is content-addressed and its digest is checked
before rendering.

The initial v1 profiles include:

- 32×32 and 64×64 favicon PNGs;
- 192×192 and 512×512 PWA icons;
- 512×512 PWA maskable icon;
- 1200×630 generic social card;
- 1280×640 GitHub social preview.

The maskable profile constrains the approved mark's bounding square to 54% of
the icon bounds so the full square remains inside the Web App Manifest central
safe circle. The compiler records verification evidence for that constraint.
Broader visual and accessibility gates belong to #12.

## Metadata and guidance

Metadata outputs are first-party serializers over the resolved model. Open Graph
markup does not depend on a framework-specific metadata package. PWA icon
metadata names only generated local resources.

Voice and usage are projected when the v1 source declares them. Until #13
stabilizes those structured contracts, the package records missing guidance as
an explicit `not-declared` state rather than inventing content.

## Package index and checksums

`packages/brand-kit/index.json` uses `identity.brand-kit-package/v1`. It records:

- package version;
- project ID and resolved source digest;
- included profile IDs;
- repository-relative package entries with SHA-256 and byte length.

`packages/brand-kit/checksums.json` uses
`identity.brand-kit-checksums/v1` and records the same file evidence under a
fixed `sha256` algorithm identifier.

The compiler manifest remains the authoritative transaction/evidence record for
the actual selected `ProjectionTarget` set. The archive index is a portable
download/consumer surface, not a replacement compiler manifest.

## Deterministic archive

`brand-kit.zip` is generated by Identity's bounded ZIP32 writer:

- entries are lexicographically sorted;
- paths are normalized relative paths;
- compression method is `store` so output does not depend on a compressor
  implementation;
- timestamps are fixed to the DOS ZIP epoch date (1980-01-01);
- CRC-32, byte sizes, offsets, and central-directory records are derived solely
  from generated bytes;
- comments, host paths, user names, random IDs, and wall-clock timestamps are
  absent.

The archive intentionally contains a portable representative Brand Kit bundle,
while the compiler manifest describes the exact selected profile build.

## Incremental generation and drift

The compiler computes expected fingerprints before rendering. When canonical
source, profile parameters, adapter descriptors, and current output bytes match
the previous manifest, targets are `unchanged` and are not rewritten.

Unmanaged files, drifted files, or stale manifest outputs are surfaced through
the compiler plan. Replacement/removal remains subject to the compiler's
approval and transaction rules.

## Consumer integration

Consumers integrate through released artifacts or versioned package files. They
must not import `src/brandkit`, `src/compiler`, or mutable repository internals.

Recommended consumer flow:

1. pin an immutable Identity release;
2. select compatible profile IDs and versions;
3. generate/obtain the verified package bundle;
4. consume only the published generated interface;
5. record the Identity/package version in dependency or desired-state metadata;
6. upgrade by generating a new plan and reviewing compatibility/drift;
7. rollback by restoring the previous immutable package/release.

Empathy and OptiFlow provide the organization-level consumer proof in #17.

## Failure behavior

The package layer fails closed when:

- a requested profile or version is unsupported;
- a required resolved token or approved source role is missing;
- approved source bytes do not match their SHA-256 record;
- an SVG cannot be parsed by the pinned renderer;
- an output cannot satisfy declared dimensions or byte budgets;
- a generated JSON/text/archive projection fails its format check;
- compiler compatibility, approval, drift, or recovery requirements fail.

Partial rendered work remains transient and is never reported as a verified
package release.

## Validation evidence

The v1 implementation is expected to prove at minimum:

- complete generation across every built-in profile;
- profile-subset generation without unrelated artifacts;
- byte-identical outputs and manifests across clean repositories for identical
  normalized inputs and the same locked toolchain;
- incremental repeated builds that do not rewrite unchanged output;
- exact PNG dimensions and maskable safe-zone evidence;
- deterministic archive bytes and checksums;
- existing CLI/source-contract parity remains intact.

Accessibility, visual regression, deeper provenance/license gates, and motion
consistency extend this evidence through #12 and umbrella #3.
