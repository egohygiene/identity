# Development environment

The same installer supports a standalone checkout, Make, Task v3, cloud setup,
and an add-on layer over your own Docker base image. Run it from a checkout;
it resolves the repository path itself and leaves source and lockfiles intact.

The host/base image supplies Bash, Python 3.11 or newer, Node.js 24 or newer,
curl, CA certificates, and a C compiler/linker. Rust is read from
`rust-toolchain.toml`; Corepack selects pnpm from `renderer/package.json`.
If Corepack is absent, the installer installs version 0.34.6 into its prefix
using npm. Make and Task are optional frontends; neither is needed by the
standalone installer. Tools already available in the base image are reused.

```bash
bash scripts/dev-env.sh setup
# Equivalent frontends:
make setup
task setup

make check                 # Rust, Python, renderer tests and public build
task browsers -- --with-deps # Chromium and Linux libraries; needs OS privileges
make browsers DEV_ARGS=--with-deps # Equivalent Make invocation
make e2e                   # Builds the fixture renderer, then browser tests
make preview               # Builds and serves the reference renderer
bash scripts/dev-env.sh exec cargo run --locked -- --help
```

`setup` installs tools and frozen dependencies and builds the CLI and renderer.
Browser tests are a separate validation step, not implied by `setup` or
`check`. All commands are repeatable and use Cargo's lockfile and frozen pnpm
installation. `preview` runs in the foreground. Its default host/port are
127.0.0.1:4173; override `IDENTITY_DEV_HOST` and `IDENTITY_DEV_PORT` as needed.
Live preview processes must be restarted in a new cloud task.
The reviewed screenshot also depends on the Linux font environment. A custom
image with different system fonts can pass functional browser checks but fail
the exact screenshot comparison. Preserve the reviewed baseline; align the
image's fonts with CI instead of automatically updating snapshots. An existing
`FONTCONFIG_FILE` override is passed through to browser commands.

By default, local tools and caches live in the ignored
`.cache/identity/dev-env` directory. Set `IDENTITY_DEV_PREFIX` to a persistent,
writable location to share them across checkouts. Existing `CARGO_HOME`,
`RUSTUP_HOME`, `COREPACK_HOME`, and `PLAYWRIGHT_BROWSERS_PATH` bindings are
preserved. A conventional Rust installation on PATH uses its existing homes.
Use `bash scripts/dev-env.sh exec COMMAND...` to activate these bindings for
arbitrary commands without changing a login shell or the base image PATH.
The prefix must be writable by the development user; installations made as
root need appropriate ownership before switching to an unprivileged user.

## Custom base image add-on

The base owns OS packages, Node, Python, certificates and user provisioning.
The default in [`dev/Dockerfile`](../dev/Dockerfile) is the official Node 24
Bookworm image pinned by its OCI index digest. The
[dated registry receipt](evidence/identity-development-base-registry-2026-10-20.json)
records the verified index, selected Linux/amd64 manifest and image-config
identities. The [qualification review](reviews/development-base-2026-10-20.md)
records executed build/runtime evidence. An index containing other architectures
does not qualify those architectures; this checkpoint targets `linux/amd64`.

The add-on owns this repository's pinned Rust toolchain, pnpm dependencies and
builds. It preserves the base's `USER`, `ENTRYPOINT` and `CMD`; it does not
provision a user or install OS packages unless browser installation is explicitly
selected. `BASE_IMAGE` remains an explicit override, including a locally prepared
custom base. Record an immutable identity for a shared or reproducible build;
mutable local tags are exploratory inputs and do not replace the qualified default.

```bash
docker build --file dev/Dockerfile --tag identity-dev .
docker run --rm identity-dev \
  bash /opt/identity/scripts/dev-env.sh exec cargo --version

# A custom base with a pre-provisioned UID/GID 1000 development user:
docker build --file dev/Dockerfile \
  --build-arg BASE_IMAGE="registry.example/your-dev-base@sha256:<approved-digest>" \
  --build-arg IDENTITY_DEV_UID=1000 --build-arg IDENTITY_DEV_GID=1000 \
  --tag identity-dev-custom .

# Optional browser installation on a supported Playwright Linux distribution:
docker build --file dev/Dockerfile \
  --build-arg BASE_IMAGE=your-reviewed-browser-base:version \
  --build-arg WITH_BROWSERS=1 --tag identity-dev-browser .
```

### Development-user and cache ownership

The default base builds/runs as root, as declared by that upstream image. For an
unprivileged build, the custom base must provision the inherited numeric UID/GID,
a writable home, and writable `/opt/identity` and `/opt/identity-dev` directories.
Set `IDENTITY_DEV_UID`/`IDENTITY_DEV_GID` to that same numeric identity so copied
checkout files are writable during setup. The add-on's default copy owner is
`0:0`; the arguments change ownership of copied files, not the inherited user.
The [qualification base](../dev/qualification/Dockerfile) demonstrates a
`1000:1000` user without duplicating repository setup.

The active user must be able to create and update the checkout's Rust target and
renderer dependencies/outputs, the development prefix, and every selected tool
home/cache. These include `CARGO_HOME`, `RUSTUP_HOME`, `COREPACK_HOME`,
`PLAYWRIGHT_BROWSERS_PATH`, `npm_config_cache`, `XDG_CACHE_HOME` and the prefix's
`pnpm-store`. Existing bindings remain authoritative. Provision ownership in the
base or mount configuration before setup; a root-built image cannot be switched
to an arbitrary `docker run --user` and assumed writable. Qualification checks
actual writes under the inherited user for both the default and custom image.
Host bind mounts retain their host ownership and can hide baked checkout files;
matching permissions and rerunning `setup` for the mounted checkout remain the
operator's responsibility.

For an existing Dockerfile, copy the checkout with matching ownership to a
writable directory and run `bash scripts/dev-env.sh setup` there. Set
`IDENTITY_DEV_PREFIX` before installation to retain tooling separately from
checkout files. Browser OS installation requires root or supported sudo access.
No application secrets, service startup or publication occurs during construction.
A cloud task already has an isolated checkout; do not create a Git worktree
unless explicitly requested.

### Proxy trust

The Docker host/builder must reach the registry and any required proxy. The base
owner provisions a TLS proxy's trusted **public CA certificate** into the OS
trust store used by curl/Rust and Node's trust configuration (for example,
`NODE_EXTRA_CA_CERTS` pointing to a readable certificate file when required).
Forward proxy build arguments only when the host requires them. The installer
preserves supplied proxy/cache bindings and enables Node environment-proxy
handling on supported Node versions. It never disables TLS verification or
imports private host credentials. Do not bake proxy credentials into the image
or publish their values in receipts. A successful public-network build does not
qualify a private proxy CA; check that trust in the owning environment.

Required network destinations include the selected image registry,
sh.rustup.rs, static.rust-lang.org, index.crates.io, static.crates.io and
registry.npmjs.org. Browser setup separately uses cdn.playwright.dev,
storage.googleapis.com and playwright.download.prss.microsoft.com. Keep TLS and
package verification enabled.

### Qualification and refresh

Repository maintainers own refresh proposals under the
[dependency policy](DEPENDENCY_POLICY.md): monthly maintenance review, or prompt
review for a relevant security fix. Resolve the official index and selected
platform manifest/config through the authenticated registry pull API, verify
raw response SHA-256 values against their digest identities, and review the
upstream Node image source/release and applicable license/security changes.
Add a new dated registry receipt, update the qualifier's `REGISTRY_RECEIPT`
pointer and the default digest together in a scoped PR. Do not silently follow
the mutable tag or rewrite prior receipts.

On a Linux Docker host, run:

```bash
python3 scripts/qualify_dev_image.py \
  --receipt /tmp/identity-dev-qualification.json
```

The same script runs in the bounded
[development-image workflow](../.github/workflows/development-image.yml). It builds
the default without an override and an explicitly selected custom base with an
unprivileged development user, through the same add-on/setup implementation.
It checks inherited configuration, writable tool/cache paths, runtime versions,
synthetic localhost CA rejection/explicit trust with curl and Node, CLI help and repeatable v1 generation/verification, plus renderer source checks,
unit tests, build and public validation. Retain the receipt with exact source
hashes and hosted run evidence; review failures before changing the pin. Keep
the previous reviewed digest and receipt available in Git for rollback.

This is development-image qualification, not an image release, SBOM/security
audit, hermetic bootstrap or browser/font/screenshot qualification. Rust and
JavaScript locks still govern repository dependencies; the base digest alone
does not freeze bootstrap network services or qualify arbitrary custom bases.
#80 owns the reproducible browser environment and reviewed visual baseline;
#82 owns the broader standalone/Make/Task/Docker entrypoint matrix.

The separate Holon-based `experience/` workflow remains optional; see its
README for its additional repository and dependencies.

## V1 validator runtime

Current source builds require [CPython](https://www.python.org/) 3.11+ for v1
CLI and library preflight (#72). Python is a runtime dependency for this boundary;
the v0 CLI remains independent of it. The host/base distributor owns the Python
installation, version, and package checksum evidence. Cross-platform release CI
selects Python 3.12 through the pinned setup action in
[release.yml](../.github/workflows/release.yml). No Python packages are installed
by the compiler. CPython and its standard library use the
[PSF license](https://docs.python.org/3/license.html).

The owning adapter is `V1ConsumerPipeline`: it runs the release-embedded
`scripts/validate_identity.py` in a subprocess with `-I -S`, reads local source,
and returns diagnostics plus a source snapshot. It requires process execution
and read access to the consumer's declared inputs; it has no credential, network,
or write capability in its validator logic. `IDENTITY_PYTHON` may select a
trusted interpreter executable. A missing/unsupported interpreter fails closed.
The Rust/Python conformance, copied-binary, invalid-source, and freshness tests
are the replacement contract: an alternative runtime or native implementation
must preserve those diagnostics and boundaries before replacing this runner.
