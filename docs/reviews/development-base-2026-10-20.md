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

The corrected [hosted run 39369572073](https://github.com/egohygiene/identity/actions/runs/39369572073),
job 118454149412, passes at head
4d9d520ba7fe6434f36a887f2a39dc22b899fc78, represented merge candidate
3101cd87666d75977e380e2e4533880602e8be4a. The
[source-bound runtime receipt](../evidence/identity-development-image-2026-10-20.json)
records the Docker engine, base/add-on identities, 13 critical source hashes
and a 331-file build-input inventory. Later documentation-only evidence updates
must reproduce those hashes; they do not retroactively change the observed
source revision. A fresh final-head hosted check remains required in the PR.

Both the unmodified default route (UID/GID 0:0) and explicit derived custom base
(1000:1000) build through the same add-on/setup implementation and pass all
29 recorded in-container commands. Expected nonzero TLS-rejection probes are
recorded as such. Each preserves inherited USER/ENTRYPOINT/CMD, proves 12
checkout/tool/cache write locations, and runs copied CLI help plus two
generate/verify cycles. All 17 canonical source files and the unrelated sentinel
remain unchanged. The complete 14-file output inventories, hidden manifest
included, agree within and across the images. Each image passes renderer source
checks, all 279 unit cases, build and public validation.

| Runtime | Both qualified images |
| --- | --- |
| OS/platform | Debian 12 Bookworm, Linux/amd64, glibc 2.36 |
| Node/npm | 24.22.0 / 11.19.1 |
| Python | 3.11.2 |
| Corepack/pnpm | 0.36.0 / 11.21.0 |
| Rust/Cargo | 1.97.1 / 1.97.1 |
| rustup | 1.29.1 |
| C compiler | Debian GCC 12.2.0 |
| curl/OpenSSL | 7.88.1 Debian security revision 10+deb12u15 / 3.0.22 |
| Docker host | Engine 28.0.4, Linux/amd64 |

The public-network setup exercises ordinary verified HTTPS. Inside each image,
a disposable synthetic TLS server separately proves that curl/Node reject
an unknown CA and accept explicit trust. Global trust is not modified and no
certificate/key bytes are retained. This mechanism check is not qualification
of a private organization's proxy.

The first [run 39369152128](https://github.com/egohygiene/identity/actions/runs/39369152128)
built the default image but failed a harness check: the pnpm version probe ran
from root, outside the renderer package-manager pin. The corrected probe uses
the same owning renderer workspace as setup and all renderer operations; no
installer/dependency change was needed. The earlier run remains failed
qualification evidence. This workspace has no Docker engine, so its local
unavailable result is also never a passing build.

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
