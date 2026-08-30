# ADR-017: Compose Identity's dogfood experience without moving brand authority

- **Status:** Accepted
- **Date:** 2026-08-30
- **Amended:** 2026-08-30 after Holon issue #4 merged
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

The first acceptance of this ADR occurred concurrently with Holon issue #4 and
therefore described a temporary Identity-owned Zensical adapter. Holon issue #4
has now merged before implementation issue #57. Holon provides independently
versioned `landing-launchkit`, `docs-zensical`, and `site-suite` profiles at
commit `2600baff6f6d944094da81b77e1a9a2e9e7a1cd6`. The shared composition has
already passed generic React/Vite and OptiFlow LaunchKit clean-room proofs.
This amendment replaces the temporary ownership assumption with the observed
shared profile while preserving the accepted two-host and brand-authority
decision. Zensical remains alpha and is transitively pinned by Holon to an exact
release and hash-locked dependency graph.

## Decision

Publish two related but independently rollbackable surfaces.

1. `egohygiene.io/identity/` is the product experience. LaunchKit renders the
   landing route and Zensical renders the docs, architecture, and legal
   subtrees. Identity builds and verifies one content-addressed composite; the
   organization route owner installs that reviewed artifact without rebuilding
   it.
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
  `2600baff6f6d944094da81b77e1a9a2e9e7a1cd6`, blueprint Git blob
  `3629339d25facb1e5b36cf6ab381c0744f1e3a14`;
- Holon's `docs-zensical` v1 profile to the same commit, blueprint Git blob
  `5f6e385d54d6271c7fe89f441787d6b253cf9fb0`, with upstream Zensical `0.0.57`
  at annotated tag object
  `ad8188ee60ae9187d64a4fe7c4970d3a1947028d` and commit
  `f18bb9957cb2740e5dd66d4a438c780b4e15d64c`;
- Holon's `site-suite` v1 profile to the same commit and blueprint Git blob
  `2635781f74fd1ba5ee5e6d742dcfabdd0289606b`; and
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
| Durable docs, architecture, legal navigation and Markdown rendering | Holon `docs-zensical` profile | Render repository-owned content without becoming its source |
| Brand Kit presentation and downloads | Existing Identity reference renderer | Project only an immutable stable Identity release |
| Common four-surface composition | Holon `site-suite` profile | Assemble the selected landing with docs, architecture, and legal output |
| Identity subpath, release binding, and compatibility redirects | Bounded Identity issue #57 adapter | Extend the shared profile through content/configuration without copying internals |
| Composite route installation | Relay and the `egohygiene.io` route owner | Install exact reviewed bytes; do not rebuild them in the portal |

## Route decision

| Public route | Behavior | Owner |
| --- | --- | --- |
| `https://egohygiene.io/identity/` | LaunchKit product landing and dogfooded identity overview | LaunchKit adapter in the Identity experience artifact |
| `https://egohygiene.io/identity/docs/` | Zensical documentation | Zensical adapter in the Identity experience artifact |
| `https://egohygiene.io/identity/architecture/` | Architecture and accepted decisions | Zensical adapter in the Identity experience artifact |
| `https://egohygiene.io/identity/legal/` | Reviewed legal and trust projection | Zensical adapter in the Identity experience artifact |
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
docs, architecture, legal, manifests, downloads, and redirects together.
Review must cover narrow and wide layouts, keyboard traversal, visible focus,
contrast, alternative text, heading structure, reduced motion, no-JavaScript
readability, and broken routes/assets.

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

LaunchKit, Zensical, and site-suite upgrades are separate intake events. Each
upgrade:

1. changes one exact pin in a dedicated pull request;
2. records upstream version/commit, license, relevant behavior changes, and
   migration effects;
3. refreshes lock and provenance evidence;
4. runs all accessibility, route, no-JavaScript, deterministic-build, and
   release-binding checks; and
5. compares the candidate visual and file-inventory evidence before approval.

Holon owns the shared Zensical and site-suite profiles. Identity issue #57 owns
only reviewed product content, the `/identity/` base-path/release-binding
extension, compatibility redirects, and consumer evidence. It does not fork
Holon internals or grow a universal multi-repository site generator.

## Consequences

- The product experience can use LaunchKit and Zensical without weakening the
  existing immutable Brand Kit.
- The public route presents current approved Identity outputs while the
  framework remains replaceable.
- The organization homepage is not moved into this repository; publication is
  an explicit artifact handoff.
- Identity can dogfood the same shared profile that later consumers adopt while
  keeping its subpath and release-binding behavior bounded to this repository.
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
- **Fork the merged Holon profiles into Identity:** would discard the reviewed
  generic/LaunchKit proofs and immediately create framework drift.

## Reconsider when

Revisit if the organization route owner cannot install content-addressed
subpath artifacts, Holon publishes a breaking profile revision, Zensical leaves
the chosen compatibility line, or the two-host release binding cannot be
verified without transferring publication authority into Identity.
