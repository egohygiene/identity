# Identity public publication surfaces

The accepted publication architecture has two public surfaces with separate
deployment and rollback authority:

| Surface | Purpose | Canonical URL |
| --- | --- | --- |
| Dogfooded product experience | LaunchKit landing plus Zensical docs, architecture, and legal surfaces | `https://egohygiene.io/identity/` |
| Release-backed Brand Kit | Immutable previews, downloads, manifests, and checksums | `https://identity.egohygiene.io/` |

The machine-readable route and lifecycle contract is
[`publication/identity-experience.architecture.json`](../../publication/identity-experience.architecture.json).
The rationale and framework boundary are accepted in
[ADR-017](../decisions/ADR-017-zensical-launchkit-publication-architecture.md).

## Dogfooded product experience

`/identity/` is a content-addressed composite based on Holon's exact-pinned
LaunchKit, Zensical, and site-suite v1 profiles. LaunchKit owns the landing;
Zensical owns `/identity/docs/`, `/identity/architecture/`, and
`/identity/legal/`. Identity supplies reviewed content and a bounded
base-path/release-binding extension. The `egohygiene.io` route owner installs
the exact reviewed bytes without rebuilding them. This repository does not own
the organization homepage.

All site adapters consume reviewed Identity release outputs read-only. Product copy
and documentation remain reviewed authored content. Adapter configuration may
select sections, navigation, and layout but may not restate tokens, asset bytes,
Kern's character facts, provenance, or approvals.

The composite's `/identity/publication.json` must expose the selected Identity
release tag and commit, source digest, asset provenance, approval evidence,
framework pins, file inventory, and artifact digest. Deployment verification
compares that release binding to the canonical Brand Kit's `/site.json` and
fails closed if they disagree.

Implementation, local preview, deployment, and live verification belong to
[issue #57](https://github.com/egohygiene/identity/issues/57). The accepted
architecture itself does not build or deploy the page.

## Compatibility routes

The organization route owner redirects `/identity/brand-kit/`, `/brand/`,
`/design/`, and `/brand-kit/` to `https://identity.egohygiene.io/`. It also
normalizes `/identity` to `/identity/`. The Brand Kit host retains its existing
local `/brand-kit/` compatibility redirect to the canonical root.

## Public boundary

The canonical public Brand Kit is `https://identity.egohygiene.io/`.

`egohygiene.io` remains the public website and application surface. Identity
owns the verified `/identity/` artifact but not the host's homepage or route
installation. The local `/brand-kit/` route is a compatibility redirect to this
site's root.

The public page is not a hand-maintained second Brand Kit. The publisher checks
out an annotated, stable Identity release tag, stages only that tag's
`assets/identity/` tree, and generates:

- the static reference renderer;
- individual approved asset downloads;
- release-owned mascot assets and their byte-bound character-package manifest;
- a deterministic `identity-brand-kit-v<version>.zip` archive;
- a public manifest with release tag, commit, source digest, file inventory,
  and archive checksum; and
- a matching checksum sidecar.

The publisher reads `publication/identity-brand-kit.config.json` from the
selected immutable release source. A newer default-branch configuration cannot
claim an asset absent from that release. The page visibly links its release and
publication manifest. `site.json` carries the same release, digest, canonical
URL, and route-alias information for a machine check without scraping HTML and
for the `/identity/` composite's cross-host release proof.

## Local preview and verification

Install the renderer's locked dependencies once, then build and inspect the
release-backed site:

```bash
cd "renderer"
corepack enable
corepack prepare "pnpm@11.21.0" --activate
pnpm install --frozen-lockfile
pnpm run build:public
pnpm run verify:public
pnpm run preview
```

`build:public` uses the `v1.0.0` source recorded in
`publication/identity-brand-kit.config.json` by default. To review a different
already-published stable release without changing repository state:

```bash
pnpm run build:public -- \
  --source-root "path/to/immutable-identity-release" \
  --release-tag "v1.0.0" \
  --release-commit "aaad8839104704cf57bfa846539b3b875421e03d"
pnpm run verify:public
```

The build intentionally rejects prerelease tags, moving references, unapproved
paths outside `assets/identity/`, and invalid release-commit identifiers.
Approved raster assets use their immutable packaged download paths for previews;
their binary bytes are never coerced into the renderer's text field.

## Deployment

`Publish Identity Brand Kit` runs whenever GitHub publishes a stable Identity
release and after a relevant merge to `main` (the public-site publisher,
publication configuration, renderer, or package generator). It checks out the
Pages publisher from `main`, creates a detached worktree at the selected
annotated stable tag, and builds the Pages artifact from that immutable
worktree.

Every deployment waits for the HTTPS canonical `site.json` to report the
selected release tag and commit, then checks the canonical page metadata. A
failed live-domain proof fails the deployment workflow rather than silently
leaving a stale or misrouted site in place.

The existing `v1.0.0` release predates this workflow. Merging the publisher
enables the first deployment automatically: the `main` trigger reads
`publication/identity-brand-kit.config.json` and selects its recorded stable
release (`v1.0.0`).

GitHub Pages must use **GitHub Actions** as its source. The published artifact
contains `CNAME` with exactly `identity.egohygiene.io`; repository settings own
the domain association and certificate issuance.

Use a manual dispatch only for recovery or rollback: select an earlier stable,
published, annotated tag and the workflow deploys and verifies it exactly like
an automatic run.

## Rollback and update

To roll back, run `Publish Identity Brand Kit` manually with an earlier stable,
published, annotated tag. It rebuilds the complete static site and archive from
that tag; no default-branch source is substituted.

To update the public Brand Kit, publish a new stable Identity release. The
workflow creates a new release-backed Pages artifact automatically. Do not edit
the live Pages artifact or upload generated files by hand.

The `/identity/` experience rolls back independently by re-promoting its
preceding verified composite. Rolling back one surface does not silently change
the other: post-deployment verification must still report an exact shared
Identity release binding before the pair is considered current.

## Framework updates

LaunchKit, Zensical, and site-suite pins change one at a time in dedicated
review. Update the pin, license/provenance evidence, frozen dependency
resolution, migration notes, visual evidence, and deterministic file inventory
together. Do not track a moving branch or let an adapter update pull new brand
source from the web.

[Holon issue #4](https://github.com/egohygiene/holon/issues/4) owns the merged
reusable profiles. Identity issue #57 consumes those profiles and owns only its
reviewed content, `/identity/` base path, release binding, compatibility
redirects, and consumer proof.
