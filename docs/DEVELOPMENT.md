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

The base owns OS packages, Node, Python, certificates, and user provisioning.
The default is `node:24-bookworm`; supply your own tag or immutable image digest
with `BASE_IMAGE`. In a network using a TLS proxy, provision its trusted CA in
the base image's OS and Node trust stores. Docker build containers must also
be able to resolve and reach that proxy; forward proxy build arguments when
required by your Docker host. Do not disable certificate verification.
The add-on owns this repository's pinned Rust toolchain, pnpm dependencies,
and builds. It preserves the base's entrypoint and command.

```bash
docker build -f dev/Dockerfile \
  --build-arg BASE_IMAGE=your-dev-base:version \
  -t identity-dev .

# Optional browser-enabled image, on a supported Playwright Linux distribution:
docker build -f dev/Dockerfile \
  --build-arg BASE_IMAGE=your-dev-base:version \
  --build-arg WITH_BROWSERS=1 -t identity-dev-browser .

docker run --rm identity-dev \
  bash /opt/identity/scripts/dev-env.sh exec cargo --version
```

For an existing Dockerfile, copy this checkout to a writable directory and
run `bash scripts/dev-env.sh setup` there. Set `IDENTITY_DEV_PREFIX` before
installation to retain tooling separately from checkout files. Browser OS
installation requires root or supported sudo access. No application secrets,
service startup, or publication is performed during image construction.
If mounting a fresh checkout over the baked checkout, rerun `setup`: the
tooling remains in its prefix, while build outputs and renderer dependencies
belong to the checkout. A cloud task already has an isolated checkout; do not
create a Git worktree unless explicitly requested.

Required network destinations include sh.rustup.rs, static.rust-lang.org,
index.crates.io, static.crates.io, and registry.npmjs.org. Browser setup also
uses cdn.playwright.dev, storage.googleapis.com, and
playwright.download.prss.microsoft.com. Keep TLS and package verification enabled.

The separate Holon-based `experience/` workflow remains optional; see its
README for its additional repository and dependencies.
