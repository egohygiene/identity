# Development-base qualification — 2026-10-20

Issue: [#81](https://github.com/egohygiene/identity/issues/81).
Base: merged #121 at `1ae867af6db65732e43689f4832d560a327f1857`.

## Outcome and scope

This candidate replaces the mutable default Node 24/Bookworm tag with its
verified official OCI index digest. It preserves explicit `BASE_IMAGE`
selection and the single `scripts/dev-env.sh setup` implementation. Numeric
copy-ownership arguments allow a pre-provisioned unprivileged base user to
write the copied checkout without changing the inherited `USER`, `ENTRYPOINT`
or `CMD`. No repository application/runtime dependency or generated contract
changes.

The [development guide](../DEVELOPMENT.md) owns refresh, proxy-CA trust,
tool/cache ownership and supported development-user requirements. The new
bounded development-image workflow qualifies Linux/amd64 default/custom builds;
#80 retains browser/font/screenshot qualification and #82 retains the broader
standalone/Make/Task/Docker entrypoint matrix.

## Registry identity and provenance

The [registry observation](../evidence/identity-development-base-registry-2026-10-20.json)
records anonymous official-registry reads, with verified raw-byte SHA-256 for
the index, selected manifest and image configuration. The immutable default is:

```text
docker.io/library/node:24-bookworm@sha256:14078204b6bb268c107ceff6d3c43f45a888105e5c2b18b14c32b3409d93a1b0
```

The Linux/amd64 manifest is
`sha256:7f7f17f773027e7f0475fa829fc0d793d75918fda85b9e517c9cc5aa46200406`;
its config is
`sha256:03905f546fa8c284c377142124957871d1e8b9ddd0d69e869e233b9eeffd7790`.
The upstream index identifies [Node image source
f27125230b3c367dcf63043ea3fe286fb3d0914c](https://github.com/nodejs/docker-node/tree/f27125230b3c367dcf63043ea3fe286fb3d0914c/24/bookworm).
The config declares Node 24.22.0, the upstream entrypoint and default `node`
command, with no explicit user (root). These declarations are registry evidence;
executed runtime versions belong to the separate build receipt below. The
index's other architectures are not qualified by this Linux/amd64 checkpoint.

## Executed qualification

The first [hosted run](https://github.com/egohygiene/identity/actions/runs/39369152128)
verified the registry binding and built the default image, then stopped on a
qualification-harness error: its pnpm version probe ran from the root instead
of the renderer workspace and observed Corepack's unpinned global default.
The probe now runs in the same owning renderer workspace as setup and renderer
validation. This changes no installer/runtime dependency. That run is failed
qualification evidence, not a passing image qualification. Full default/custom
runtime checks are pending the corrected hosted run.

This workspace has no Docker-compatible engine/socket; local checks alone are
not image-build evidence. Exact source-bound results and runtime versions will
be recorded before the review handoff.

## Local checks and review

Python completes 143 cases: 141 pass and two existing skips. Five new cases
cover invalid/mutable default identity, changed inherited configuration,
ambiguous/failed receipts, mismatched registry evidence and unsafe receipt
paths. Six standalone docs/release/mascot/publication/extraction verifiers,
Rust formatting, Python compilation and whitespace checks pass. Independent
read-only review found no remaining implementation blocker and separately
executed the synthetic CA probe successfully. No Rust production source,
lockfile, public schema, release binding or visual baseline changes.

The pinned owner checks preserve all 40 roadmap IDs/88 edges and mappings,
plus all 26 ADR bytes/dispositions/approval/lineage. Q16 is complete; Q20 is
active; Q22 is ready for its later final-docs position. These are bounded
invariant checks, not native whole-repository conformance.

## Safety, ownership and limits

The custom fixture derives from the same pinned official base, provisions
UID/GID `1000:1000` and writable homes/prefixes, then inherits that user through
the add-on. It exercises the explicit override/ownership route; it does not
qualify an unrelated arbitrary image. Default root and custom unprivileged
construction/runtime are separate observed cases. A runtime user override or
host mount with different ownership needs its own provisioning/qualification.

Proxy CA trust remains with the host/base owner, including OS and Node trust.
No TLS verification is disabled, no private proxy values are recorded, and a
public-network hosted run cannot establish private-proxy trust. The bounded
localhost TLS probe checks that curl and Node reject an unknown synthetic CA and
accept it only through explicit trust; it never changes a global CA store.
Cache/tool-home
bindings are preserved and must be writable by their owning user. Browser OS
installation remains an explicit privileged option, outside this smoke.

The base pin freezes the selected base bytes, not network bootstrap services,
future dependency resolutions outside committed locks, every architecture,
visual baseline, vulnerability/license audit or complete hermetic build.
No image, package or stable release is published and no deployment occurs.
The current stable v1.0.0 remains unchanged.

## Decision impact

**ADR not required:** this is straightforward dependency-policy repair and
qualification of the existing portable Node/Bookworm add-on. It introduces no
new durable runtime/platform, ownership, public schema or publication boundary.
All 26 existing ADRs (21 accepted/five proposed), lifecycle, approval and lineage
remain unchanged. ADR-0006/0011's qualified rendering/browser limitations remain
intact. Pinned Aether decision-impact 2.1.0 and continuity 1.1.0 at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921`, with Hygiene 1.2.0 at
`a05b14f8b9e2772124f879f818e09a911e996ad8`, were read from verified exact source
checkouts. Repeat this classification against the final diff before handoff.

Roadmap-Step: IDN-Q20
