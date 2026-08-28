# Identity reference renderer

The reference renderer turns `identity.brand-kit-view-model/v1` into a static,
accessible Brand Kit page. It is a replaceable React/Vite adapter; canonical
brand intent remains in the consumer's `.identity/` source.

## Contract

Input:

```text
assets/identity/packages/renderer/brand-kit.view-model.json
```

The Rust compiler creates this file through
`identity::reference_renderer::with_reference_renderer`. The renderer never
reads `.identity/`, repository internals, or a mutable sibling branch.

Output:

```text
renderer/dist/
```

The output contains server-rendered essential content, progressive copy/theme
controls, and the generated asset tree copied from `assets/identity/`.

## Commands

```bash
corepack enable
corepack prepare "pnpm@11.21.0" --activate
pnpm install --frozen-lockfile
pnpm run validate
```

Render another immutable model:

```bash
pnpm run render -- \
  --model "../assets/identity/packages/renderer/brand-kit.view-model.json" \
  --asset-base-url "./"
pnpm run build
```

Render a reviewed design-system projection alongside the immutable Brand Kit
model:

```bash
python3 "../scripts/render_design_system.py" \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/design-system"

pnpm run render -- \
  --model "../assets/identity/packages/renderer/brand-kit.view-model.json" \
  --design-system-directory "../assets/identity/design-system" \
  --design-system-artifact-directory "design-system" \
  --asset-base-url "./"
```

The renderer validates that the handbook and AI context share a project,
handbook schema, and source digest. It presents the approved principles,
inheritance, and capability boundaries and links the four generated artifacts;
it does not recreate handbook facts from renderer configuration.

Set `IDENTITY_RENDERER_BASE` when the static bundle is mounted below a route
prefix. Consumers may also change CSS variables or supply different generated
tokens without modifying the JSON contract.

## Identity public site

The repository's own public Brand Kit is a release-backed projection at
`https://identity.egohygiene.io/`. Build it locally with:

```bash
pnpm run build:public
pnpm run verify:public
```

The public builder stages an immutable release's `assets/identity/` tree,
generates the complete public archive, manifest, and checksums, and sends that
staged tree through this renderer. It does not use a mutable default-branch
asset tree as the public source. The full deployment and rollback procedure is
documented in
[`docs/publication/IDENTITY_PAGES.md`](../docs/publication/IDENTITY_PAGES.md).

## Authority labels

The page deliberately labels:

- marks, colors, and typography as **generated previews**;
- voice and usage as **canonical guidance**;
- absent color pairings, type scales, motion, imagery, mascot, license, and
  provenance data as **not declared** instead of inventing content.
- generated design-system handbooks and AI context as **canonical guidance**
  only when the verified projection pair is supplied.

Approved assets expose their format, dimensions, intended use, availability,
digest, safe zone, license, provenance, approval, and download status.

## Validation

Vitest covers contract rendering, missing-data states, asset metadata,
route-prefixed links, download structure, semantic accessibility, and the stable
full-page visual hierarchy. It also runs a cross-language consumer handoff:
the Python projection command generates a fixture consumer's artifacts and the
static renderer consumes those exact files. Playwright covers browser accessibility including
color contrast, keyboard behavior, deep links, real download responses,
responsive/reduced-motion behavior, and a reviewed desktop viewport screenshot.
