# ADR-017: Compose Identity's dogfood experience without moving brand authority

- **Status:** Accepted
- **Date:** 2026-08-30
- **Tracking:** [Identity issue #56](https://github.com/egohygiene/identity/issues/56)
- **Implementation:** [Identity issue #57](https://github.com/egohygiene/identity/issues/57)
- **Decision owners:** Identity maintainers and the `egohygiene.io` route owner
- **Machine contract:** [`publication/identity-experience.architecture.json`](../../publication/identity-experience.architecture.json)

## Context

Identity already publishes an immutable, release-backed Brand Kit at
`https://identity.egohygiene.io/`. That site proves downloads, manifests,
source digests, asset provenance, approvals, and rollback from stable annotated
Identity tags. Replacing it with a marketing framework would weaken an existing
trust boundary.

Identity also needs a first-class product experience at
`https://egohygiene.io/identity/`. The page should explain the product, show the
system using its own approved outputs, introduce Kern as one governed mascot
projection, and lead into durable technical documentation. Hand-maintaining
colors, assets, or character facts inside a site framework would create a
second source of brand truth.

Holon now provides the versioned `landing-launchkit` profile at commit
`93364d7461e537bc2fbe1beaf7b812b2b290feda`. It composes a manifest-driven
LaunchKit landing page over the generic React/Vite foundation and pre-renders
the complete page before progressive hydration. The reusable Zensical profile
tracked by [Holon issue #4](https://github.com/egohygiene/holon/issues/4) is not
yet implemented. Zensical itself is still marked alpha, so Identity must pin an
exact release and keep the first adapter deliberately local to the dogfood.

## Decision

Publish two related but independently rollbackable surfaces.

1. `egohygiene.io/identity/` is the product experience. LaunchKit renders the
   landing route and Zensical renders the `/identity/docs/` subtree. Identity
   builds and verifies one content-addressed composite; the organization route
   owner installs that reviewed artifact without rebuilding it.
2. `identity.egohygiene.io/` remains the canonical public Brand Kit. The
   existing reference renderer and release-backed publisher continue to own
   that host, its package downloads, manifests, checksum sidecars, and rollback
   by stable annotated tag.

LaunchKit, Zensical, the reference renderer, and the route composer are
replaceable projections. None is a canonical brand source. They may consume
reviewed Identity outputs read-only and may contain adapter-only layout,
navigation, and framework configuration. They may not copy token values,
mascot facts, asset bytes, approvals, provenance, or package metadata into a
second maintained truth.

The accepted machine contract pins:

- Holon's `landing-launchkit` v1 profile to commit
  `93364d7461e537bc2fbe1beaf7b812b2b290feda`, blueprint Git blob
  `6f87ad486fe92ab0ee40f8116a4427ccf7ff7989`;
- Zensical `0.0.57` to annotated tag object
  `ad8188ee60ae9187d64a4fe7c4970d3a1947028d` and commit
  `f18bb9957cb2740e5dd66d4a438c780b4e15d64c`; and
- the existing release-backed Identity renderer to its repository-local source
  and publication configuration.

Issue #57 must add a lockfile or equivalent package-resolution evidence for
every transitive build dependency. A tag or version string alone is not a
complete dependency lock.

## Responsibility boundary

| Concern | Owner | Required behavior |
| --- | --- | --- |
| Brand intent, tokens, approved assets, mascot facts, provenance, approvals | Identity contracts and generated `assets/identity/` package | Canonical; compiled and reviewed before site build |
| Landing information architecture and typed section composition | Holon `landing-launchkit` profile | Pre-rendered, progressively enhanced, configured by reviewed content |
| Product positioning and calls to action | Identity maintainers | Authored and reviewed; may refer to generated brand facts but not redefine them |
| Durable documentation navigation and Markdown rendering | Identity's pinned Zensical dogfood adapter | Render repository-owned documentation without becoming its source |
| Brand Kit presentation and downloads | Existing Identity reference renderer | Project only an immutable stable Identity release |
| Composite route installation | Relay and the `egohygiene.io` route owner | Install exact reviewed bytes; do not rebuild them in the portal |
| General reusable docs/site blueprint | Holon issue #4 | Generalize only after the Identity dogfood supplies evidence |

## Route decision

| Public route | Behavior | Owner |
| --- | --- | --- |
| `https://egohygiene.io/identity/` | LaunchKit product landing and dogfooded identity overview | LaunchKit adapter in the Identity experience artifact |
| `https://egohygiene.io/identity/docs/` | Zensical documentation | Zensical adapter in the Identity experience artifact |
| `https://egohygiene.io/identity/publication.json` | Composite inventory, digests, release binding, and verification evidence | Route composer |
| `https://egohygiene.io/identity/brand-kit/` | Redirect to the canonical Brand Kit | Route composer |
| `https://egohygiene.io/brand/`, `/design/`, `/brand-kit/` | Compatibility redirects to the canonical Brand Kit | Organization route owner |
| `https://identity.egohygiene.io/` | Immutable Brand Kit, previews, and downloads | Existing reference renderer and publisher |
| `https://identity.egohygiene.io/site.json` | Release tag, commit, source digest, and publication-manifest proof | Existing reference renderer and publisher |
| `https://identity.egohygiene.io/packages/identity-brand-kit-v{version}.*` | Release manifest, ZIP, and checksum sidecar | Existing reference renderer and publisher |
| `https://identity.egohygiene.io/brand-kit/` | Compatibility redirect to the Brand Kit root | Existing reference renderer and publisher |

Trailing-slash normalization for `/identity` is an explicit redirect. The
landing build owns `/identity/` but must not emit anything under
`/identity/docs/`; the documentation build owns that subtree. The composite
builder fails on every other collision rather than choosing an implicit winner.

## Content compilation boundary

Three source classes enter the experience:

- **Compiled Identity outputs:** the public asset manifest, mascot package, and
  generated web token projection. Adapters consume these exact bytes read-only
  from the selected stable release.
- **Authored documentation and product copy:** maintainers own explanatory
  Markdown, positioning, examples, calls to action, and navigation labels.
  Authored prose may explain canonical facts but cannot redefine token values,
  asset identities, approval state, or provenance.
- **Adapter configuration:** base paths, section selection, navigation, and
  framework flags. This is replaceable implementation detail and may only
  reference canonical inputs.

The complete experience is built from one Identity stable release selection.
Its `publication.json` must expose the release tag, release commit, source
digest, asset-provenance references, approval-evidence references, framework
pins, file inventory, and artifact digest. Live verification compares that
binding to `identity.egohygiene.io/site.json` and fails closed on disagreement.

## Preview, build, deployment, and rollback

Local preview uses the production `/identity/` base path and mounts the landing,
docs, manifests, downloads, and redirects together. Review must cover narrow
and wide layouts, keyboard traversal, visible focus, contrast, alternative
text, heading structure, reduced motion, no-JavaScript readability, and broken
routes/assets.

Production builds use a clean checkout, frozen dependencies, pinned framework
inputs, and no network retrieval of brand or documentation source. Building the
same reviewed inputs twice must produce identical inventories and digests. A
route-collision check and release-evidence check run before handoff.

Identity hands one content-addressed artifact to the organization route owner.
Publication installs those exact bytes and then verifies the canonical HTTPS
routes and evidence. The organization experience rolls back by re-promoting a
previous verified composite. The Brand Kit rolls back independently through
its existing stable-tag workflow. Neither rollback requires rebuilding the
artifact being restored.

## Framework upgrades

LaunchKit and Zensical upgrades are separate intake events. Each upgrade:

1. changes one exact pin in a dedicated pull request;
2. records upstream version/commit, license, relevant behavior changes, and
   migration effects;
3. refreshes lock and provenance evidence;
4. runs all accessibility, route, no-JavaScript, deterministic-build, and
   release-binding checks; and
5. compares the candidate visual and file-inventory evidence before approval.

Until Holon issue #4 publishes a reviewed Zensical profile, Identity owns only
the bounded dogfood adapter. Generalization moves to Holon from observed
consumer evidence; Identity does not grow a universal multi-repository site
generator.

## Consequences

- The product experience can use LaunchKit and Zensical without weakening the
  existing immutable Brand Kit.
- The public route presents current approved Identity outputs while the
  framework remains replaceable.
- The organization homepage is not moved into this repository; publication is
  an explicit artifact handoff.
- A first Zensical adapter is temporarily local to Identity because the shared
  Holon profile does not exist yet.
- There are two deployments and therefore two rollback controls, but their
  evidence is compared through one release binding.

## Alternatives rejected

- **Replace the Brand Kit root with LaunchKit:** turns a release-proof surface
  into a marketing surface and couples downloads to presentation churn.
- **Put docs inside React components:** makes navigation and durable technical
  content dependent on the landing framework.
- **Copy tokens and mascot metadata into framework configuration:** creates a
  second brand source and permits silent drift.
- **Fetch current Identity or documentation data during a production build:**
  makes reviewed inputs mutable and prevents reliable reproduction.
- **Wait for a universal Holon site generator:** blocks the dogfood that should
  provide the evidence for that generator.

## Reconsider when

Revisit if the organization route owner cannot install content-addressed
subpath artifacts, Holon publishes an incompatible Zensical profile, Zensical
leaves the chosen compatibility line, or the two-host release binding cannot be
verified without transferring publication authority into Identity.
