# Identity public Brand Kit publication

## Public boundary

The canonical public Brand Kit is `https://identity.egohygiene.io/`.

`egohygiene.io` remains the public website and application surface. Its future
`/identity`, `/brand`, `/design`, and `/brand-kit` routes may redirect here, but
they are not implemented in this repository. The local `/brand-kit/` route is a
compatibility redirect to this site's root.

The public page is not a hand-maintained second Brand Kit. The publisher checks
out an annotated, stable Identity release tag, stages only that tag's
`assets/identity/` tree, and generates:

- the static reference renderer;
- individual approved asset downloads;
- a deterministic `identity-brand-kit-v<version>.zip` archive;
- a public manifest with release tag, commit, source digest, file inventory,
  and archive checksum; and
- a matching checksum sidecar.

The page visibly links its release and publication manifest. `site.json` carries
the same release, digest, canonical URL, and route-alias information for a
machine check without scraping HTML.

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
