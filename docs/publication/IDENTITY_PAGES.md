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
[issue #57](https://github.com/egohygiene/identity/issues/57). The bounded
implementation now lives in [`experience/`](../../experience/README.md), with
reviewed product copy in
[`publication/identity-experience.content.json`](../../publication/identity-experience.content.json)
and an offline builder/verifier pair under `scripts/`.

The build verifies all three accepted Holon blueprint Git blobs and inventories
before materializing the shared LaunchKit `site-suite` variant. It resolves
Kern's exact bytes and alternative text from the governed mascot package,
installs Holon's frozen pnpm graph and hash-locked Zensical graph, applies only
Identity's bounded subpath/release-binding extension, rejects route collisions,
and emits one `/identity/` tree with landing, docs, architecture, and legal
surfaces. `SHA256SUMS` and `publication.json` bind every emitted file. A
deterministic tar handoff is uploaded with browser, accessibility, responsive,
reduced-motion, no-JavaScript, and visual review evidence.

`v1.1.0` is the configured candidate binding until that stable Identity release
exists. Candidate artifacts prove the build and must not be installed at the
canonical route. A tag-triggered build binds the exact stable tag and commit;
the opt-in live gate then compares those fields with the release-backed Brand
Kit `site.json` before route-owner installation is considered verified.

Local build and browser commands are documented in the
[experience README](../../experience/README.md).

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

The publisher normally reads `publication/identity-brand-kit.config.json` from
the selected immutable release source. `v1.0.0` predates that file, so its exact
tag and commit select a dedicated compatibility configuration through
`publication/release-configs/index.json`. The index binds the fallback config
to a SHA-256 digest, and offline verification confirms that every selected
asset exists in the detached release tree. A newer default-branch configuration
therefore cannot claim an asset absent from that release.

The page visibly links its release and publication manifest. `site.json`
carries the same release, digest, canonical URL, and route-alias information
for a machine check without scraping HTML and for the `/identity/` composite's
cross-host release proof.

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
enables the first deployment automatically: the `main` trigger selects the
recorded stable release (`v1.0.0`) and uses its digest-pinned compatibility
configuration without substituting current assets.

GitHub Pages must use **GitHub Actions** as its source. The published artifact
contains `CNAME` with exactly `identity.egohygiene.io`; repository settings own
the domain association and certificate issuance.

Use a manual dispatch only for recovery or rollback: select an earlier stable,
published, annotated tag and the workflow deploys and verifies it exactly like
an automatic run.

## Decisions composition checkpoint — 2026-10-10

The current implementation adds Repository Intelligence to the existing Brand
Kit publisher and host. [Proposed ADR-022](../decisions/ADR-022-decisions-publication-composition.md)
records this consumer choice separately from accepted ADR-017 and the earlier
R1 disposition. Implementation and deployment authorization do not mark
ADR-022 accepted.

| Component | Route/source boundary |
| --- | --- |
| Existing Brand Kit | Root and every existing file remain byte-preserved from the selected stable release build. The initial binding remains `v1.0.0`. |
| Repository Intelligence | The Relay action pinned to `2519eaccefaa6a6e7f199b05cc0f8cf9803c76a0` freshly collects canonical ADRs at a full repository commit and emits `renderer/dist/intelligence`. |
| Decisions | `https://identity.egohygiene.io/intelligence/decisions/` |
| Consumer alias | `https://identity.egohygiene.io/decisions/` redirects to `/intelligence/decisions/`. |
| Organization experience | `/identity/` keeps its independent route owner, stable-release gate and deployment process. |

The current publication pin adopts [Relay PR #141](https://github.com/egohygiene/relay/pull/141)'s
hidden-card styling fix. The [first deployment receipt](../evidence/identity-decisions-deployment-2026-10-10.json)
retains its original pin and filtering failure. Republish this revision and
verify query, facets, reset and no-match card visibility before recording the
repair as live; the earlier byte-verification result is not that proof.

The same `Publish Identity Brand Kit` workflow uploads and deploys one composed
Pages artifact. It records the publisher revision, ADR source revision and
stable Brand Kit release revision separately. The default ADR source is the
exact publisher commit. Manual `intelligence_revision` accepts only a full
ancestor commit and still runs fresh production admission; stale snapshots
and review-only envelopes cannot substitute for that check.

Before composition, capture all Brand Kit paths and byte hashes. Reject any
overwritten or missing baseline file and any route collision; verify the native
Decisions route and consumer alias. Retain the exact composed artifact, shared
composition evidence, source bindings and digest. After Pages deployment,
compare live Decisions and Brand Kit bytes to that retained artifact and keep
the deployment receipt separate from the live-verification result.

The [ratified-source receipt](../evidence/identity-adrs-ratified-2026-10-10.json)
is historical evidence for source `12227dad43c90b02e14971030f22242f3a205c9d`
and 21 accepted records. Adding proposed ADR-022 requires new 22-record source
validation and build evidence. Neither that old receipt nor this guide claims
that the new composition is already deployed or its rollback has been exercised.

The [rollback capture](../../publication/decisions-rollback.json) records the
prior site's complete 40-file inventory and the bytes retrieved over HTTPS on
2026-10-10. Its site digest is
`sha256:c690803f5eda55c7b61d7ae34a1df3e109d2dad9aad9a34ef086207d4cd0fd88`;
the release manifest and package checksums were also verified. The prior
successful [Pages run 37157851822](https://github.com/egohygiene/identity/actions/runs/37157851822)
used publisher `8aae2c6767d07714ea16bf0ea493e1f1ac399b6e`; its old Pages
artifact `11286585084` has expired. The upload logs establish the old file paths;
current HTTP responses supply the new capture's bytes. The original Actions
ZIP was not independently reverified. Retain this new capture with its recorded
digest and the new exact composed artifact for subsequent re-promotion; neither
capture alone proves a rollback deployment. Attach actual deployment and
live-proof results to the owning
[Identity #69](https://github.com/egohygiene/identity/issues/69) handoff.

Before deployment, the consumer's `capture-rollback` operation freshly retrieves
every recorded path and checks its exact bytes and hash. It emits
`rollback-site.tar`, `rollback-record.json` and `rollback-capture.json` under
`.relay/repository-intelligence-deployment/`. The publisher captures them after
Brand Kit verification and before composition, then retains all three with the
composed site in the ordinary
`identity-decisions-publication-<publisher_commit>-<run_id>-<run_attempt>`
workflow artifact for 30 days. The capture receipt records its actual
observation time and new archive digest. A capture failure blocks promotion
rather than silently discarding the recovery point. Artifact expiry remains a
real recovery limit; a later handoff must establish its own retained bytes.
The fixed 40-file recovery record also fails closed if those historical root
bytes change. Before subsequent stable-release changes, refresh that record
from the preceding retained, verified artifact rather than weakening its
checks.

## Rollback and update

To roll back, run `Publish Identity Brand Kit` manually with an earlier stable,
published, annotated tag. It rebuilds the Brand Kit and archive from that tag;
no default-branch asset source is substituted. The composed site's Decisions
source is independent: optionally select a reviewed full ancestor commit with
`intelligence_revision`, which must pass fresh collection and composition gates.
Record both bindings and verify the resulting live bytes. If the Intelligence
path cannot pass its gates, restore a reviewed, byte-verified prior Brand
Kit-only artifact through the existing deployment owner; do not bypass
validation or claim an expired artifact is recoverable.

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
