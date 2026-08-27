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

Set `IDENTITY_RENDERER_BASE` when the static bundle is mounted below a route
prefix. Consumers may also change CSS variables or supply different generated
tokens without modifying the JSON contract.

## Authority labels

The page deliberately labels:

- marks, colors, and typography as **generated previews**;
- voice and usage as **canonical guidance**;
- absent color pairings, type scales, motion, imagery, mascot, license, and
  provenance data as **not declared** instead of inventing content.

Approved assets expose their format, dimensions, intended use, availability,
digest, safe zone, license, provenance, approval, and download status.

## Validation

Vitest covers contract rendering, missing-data states, asset metadata,
route-prefixed links, download structure, semantic accessibility, and the stable
full-page visual hierarchy. Playwright covers browser accessibility including
color contrast, keyboard behavior, deep links, real download responses,
responsive/reduced-motion behavior, and a reviewed desktop viewport screenshot.
