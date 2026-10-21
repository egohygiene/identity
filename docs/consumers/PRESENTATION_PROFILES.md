# Selected presentation profiles

Identity already has a small native target set. Select a target only when the
project needs it; a successful build does not create an account, publish a
package, upload media or approve new copy. The public kit exposes the selected
images, their existing source rights, and copy controls for supplied text.

## Target inventory and selection

| Need | Selection and output | Constraints and ownership |
| --- | --- | --- |
| GitHub repository link preview | Native `github@1.0.0`: `github/social-preview.png` | PNG, 1280 × 640 pixels; compiler budget 999,999 bytes. GitHub's [official upload guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) was checked on 2026-10-21: under 1 MB, with 1280 × 640 recommended for best display. The conservative compiler budget is below decimal and binary interpretations. |
| Generic card for a separately reviewed destination | Native `social@1.0.0`: `social/card-1200x630.png` | PNG, 1200 × 630 pixels, existing 2,000,000-byte budget. These are Identity's chosen generic dimensions; they do not establish requirements or approval for any named social platform. |
| Names and reusable metadata | Existing `metadata@1.0.0`: `packages/metadata/metadata.json` and `open-graph.html` | Canonical project name, repository and tagline. Image references name only selected public outputs. The HTML fragment is an integration input; the consuming site supplies its actual public URLs and deployment. |
| Package identifier, registry link, keywords, description or account URL | Existing optional Press Kit and channel registry | Reuse approved records as described below; no publishing adapter or new registry profile is selected by this issue. |

The implementation owners are the typed native catalog in
[`src/brandkit/profiles.rs`](../../src/brandkit/profiles.rs) and the
[package contract](../contracts/BRAND_KIT_PACKAGES_V1.md). The older `profiles/`
JSON files describe **v0** and are not the native v1 catalog. No new output
profile or source schema is required for this selection.

In `.identity/targets/profiles.json`, retain the project's current selections
and add only the required `{ "id": "github", "version": "1.0.0" }` or
`{ "id": "social", "version": "1.0.0" }` entry. A core-only selection remains
valid. These profiles are optional even though the underlying target document
still requires at least one native profile. No selected GitHub/social download
means no presentation section or navigation item in the public kit.

The GitHub profile previously inherited the generic 2 MB bound. This repair
enforces GitHub's existing upload requirement without changing its output path,
format, dimensions or image composition. Previously generated oversized previews
must be regenerated and reviewed with the updated immutable compiler pin; old
releases and their receipts are not rewritten.

## Reuse copy and discovery facts

| Fact | Existing governed source | Generated/public reuse |
| --- | --- | --- |
| Project name, tagline and repository | `identity.json` project metadata | Metadata JSON plus presentation copy controls; the tagline stays labeled as a tagline. |
| Short description, optional paragraph, long description/bio | Press Kit `boilerplates[]` | Exact supplied text and kind, in the kit, JSON, Markdown and archive; no auto-shortening or invented bio. |
| Official package identifier | Press Kit `facts[]`, with an explicit label such as `npm package` | Exact supplied value, including any scope/case; never derive it from a project name or treat a generated package stub as proof of a registry listing. |
| Discovery keywords | Press Kit `facts[]`, explicitly labeled by the owner | Exact reviewed string; no inferred tags or target-specific normalization. |
| Registry listing URL | Press Kit `links[]`, with `kind: "other"` and an explicit label | Supplied HTTPS URL, without querying the registry or asserting ownership/publication. |
| Social account URLs | Adopted channel registry; otherwise approved Press Kit `social` links | Registry-derived links retain its active/badge-approved boundary. Planned, withheld or unverified ownership claims are not promoted. |

Fact IDs and labels do not activate hidden registry behavior. Approvals and
provenance must cite the package or account owner's actual evidence. Authoritative
package manifests, publishing, authentication and account management keep their
existing owners. The current Identity Cargo package has `publish = false` and its
renderer is private; neither supplies an official crates.io/npm listing here.

Use the [authoring worksheet](AUTHORING.md) and
[Press Kit contract](../contracts/PRESS_KIT_V1.md). A valid consumer without a
Press Kit can still generate the selected images and copy its canonical name,
tagline and repository. Descriptions, package/discovery facts and account URLs
remain explicitly absent. Review the complete, untruncated text against each
destination's current limits before pasting it.

## Generate, inspect and hand off

From a review checkout of the matching immutable Identity source, use absolute
paths for the consumer and prepare the page before bundling it:

```bash
consumer_root="/absolute/path/to/consumer"
cargo run --locked --bin identity -- v1-generate \
  --repository-root "$consumer_root"
cargo run --locked --bin identity -- v1-verify \
  --repository-root "$consumer_root"
node renderer/scripts/render-static.mjs \
  --model "$consumer_root/assets/identity/packages/renderer/brand-kit.view-model.json" \
  --output "$PWD/renderer/index.html" \
  --asset-base-url "./" \
  --artifact-root "$consumer_root/assets/identity" \
  --artifact-manifest "$consumer_root/assets/identity/.identity-manifest.json"
```

Include the optional generated Press Kit through the renderer's existing
`--press-kit-directory` and `--press-kit-artifact-directory` arguments when
adopted. From `renderer/`, bundle the prepared page directly (the default
`pnpm run build` first replaces it with the example fixture):

```bash
IDENTITY_RENDERER_PUBLIC_DIR="$consumer_root/assets/identity" \
  corepack pnpm exec vite build --base "./"
corepack pnpm run preview
```

The build copies the selected generated assets into the preview. This local
review does not release or deploy a kit. Release/public publication follows the
existing [Pages and release-bound publication guide](../publication/IDENTITY_PAGES.md).

Inspect the selected PNG, source attribution/restrictions, exact copy values and
download bytes. For GitHub, a repository administrator manually opens Settings,
then Social preview, Edit and Upload an image. This issue stops at the reviewable
handoff and performs no upload. A destination's cropping, visibility and final
presentation still need human review.

## Add a concrete target

First record the actual need, official requirement source and review date. Reuse
an existing profile when it fits. A native target change must declare format,
dimensions, byte budget, source role, deterministic composition, verification
and version/migration impact in the typed catalog and package contract. Exercise
it against an approved real consumer, plus omission, audience/rights, dimensions,
download integrity and unchanged-source checks. A renderer view may present only
selected generated targets; it must not construct speculative paths.

For third-party social surfaces beyond the existing native targets, use
[ADR-0016's existing Aether admission boundary](../decisions/ADR-0016-pinned-social-surface-projection-boundary.md)
and the [social-surface contract](../contracts/SOCIAL_SURFACES_V1.md), preserving
the exact catalog lock, rights, release inclusion, unknowns and account boundary.
The Aether catalog inspected on 2026-10-21 is still experimental, rights-rejected,
release-excluded and empty. Closed Aether #52/#53 do not make those records
admissible. No external matrix, template pack or platform-safe-zone guess is
added here. Advanced launch/document templates remain #106.

## Real target proof

The [2026-10-21 receipt](../evidence/identity-presentation-mantle-2026-10-21.json)
uses unchanged `egohygiene/mantle@b08045acc1e982dd9424c1d8c91b0badd64744e8`.
All 14 consumed input files match raw Git blobs. Two fresh native builds and
read-only verification agree on all 19 generated files, including the compiler
manifest. The selected GitHub PNG is 1280 × 640, 16,698 bytes, with SHA-256
`39a01b2242100703c238fd4719201719eddd2ae94f882c56c697b1f43dccf79f`.
Its exact generated model and PNG are retained as a bounded
[renderer fixture](../../renderer/fixtures/mantle-presentation/README.md),
including supplied MIT attribution, public selection and restrictions.

The browser test consumes those exact bytes for hydration, preview, keyboard
copy/navigation, actual download integrity, accessibility and narrow-screen
coverage. Runtime outcomes belong to the exact PR-head checks. Native proof
also rejects a corrupted preview without repairing it and passes a disposable
GitHub/social-omission variant. Mantle's original complete checkout is preserved.
No account, package listing or Press Kit is invented for this consumer; no
upload or final human visual acceptance is claimed.
