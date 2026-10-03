#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export IDENTITY_DEV_PREFIX="${IDENTITY_DEV_PREFIX:-$repo_root/.cache/identity/dev-env}"
# Respect base-image bindings and reuse a conventional preinstalled Rust home.
if command -v rustup >/dev/null 2>&1; then
  export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}"
  export RUSTUP_HOME="${RUSTUP_HOME:-$HOME/.rustup}"
else
  export CARGO_HOME="${CARGO_HOME:-$IDENTITY_DEV_PREFIX/cargo}"
  export RUSTUP_HOME="${RUSTUP_HOME:-$IDENTITY_DEV_PREFIX/rustup}"
fi
export COREPACK_HOME="${COREPACK_HOME:-$IDENTITY_DEV_PREFIX/corepack-cache}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$IDENTITY_DEV_PREFIX/browsers}"
export npm_config_cache="${npm_config_cache:-$IDENTITY_DEV_PREFIX/npm-cache}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$IDENTITY_DEV_PREFIX/xdg-cache}"
export PATH="$IDENTITY_DEV_PREFIX/bin:$IDENTITY_DEV_PREFIX/corepack-cli/node_modules/.bin:$CARGO_HOME/bin:$PATH"
# Recent Corepack versions use Node's native fetch. Enable its supported
# environment proxy handling when the base supplies an HTTP(S) proxy.
if [[ -n "${HTTPS_PROXY:-${https_proxy:-${HTTP_PROXY:-${http_proxy:-}}}}" ]] && command -v node >/dev/null 2>&1; then
  if node -e 'const [major,minor]=process.versions.node.split(".").map(Number); process.exit(major > 24 || (major === 24 && minor >= 5) ? 0 : 1)'; then
    export NODE_USE_ENV_PROXY="${NODE_USE_ENV_PROXY:-1}"
  fi
fi

require() {
  command -v "$1" >/dev/null 2>&1 || { printf 'Required base tool missing: %s\n' "$1" >&2; exit 1; }
}

tools() {
  for tool in python3 node curl cc; do require "$tool"; done
  python3 -c 'import sys; sys.exit("Python 3.11 or newer is required" if sys.version_info < (3, 11) else 0)'
  node -e 'if (Number(process.versions.node.split(".")[0]) < 24) { console.error("Node.js 24 or newer is required"); process.exit(1); }'
  mkdir -p "$IDENTITY_DEV_PREFIX/bin"
  if ! command -v rustup >/dev/null 2>&1; then
    curl --fail --show-error --location https://sh.rustup.rs -o "$IDENTITY_DEV_PREFIX/rustup-init.sh"
    bash "$IDENTITY_DEV_PREFIX/rustup-init.sh" -y --no-modify-path --profile minimal --default-toolchain none
  fi
  local channel
  channel="$(python3 -c 'import sys,tomllib; print(tomllib.load(open(sys.argv[1], "rb"))["toolchain"]["channel"])' "$repo_root/rust-toolchain.toml")"
  rustup toolchain install "$channel" --profile minimal --component clippy,rustfmt
  if ! command -v corepack >/dev/null 2>&1; then
    require npm
    npm install --prefix "$IDENTITY_DEV_PREFIX/corepack-cli" --no-audit --no-fund corepack@0.34.6
  fi
  corepack enable --install-directory "$IDENTITY_DEV_PREFIX/bin"
  (cd "$repo_root/renderer" && corepack pnpm --version)
}

deps() {
  cd "$repo_root"
  cargo fetch --locked
  cd renderer
  corepack pnpm install --frozen-lockfile --store-dir "$IDENTITY_DEV_PREFIX/pnpm-store"
}

build() {
  cd "$repo_root"
  cargo build --locked
  cd renderer
  corepack pnpm build
}

check() {
  cd "$repo_root"
  cargo fmt --all --check
  cargo clippy --locked --all-targets --all-features -- -D warnings
  cargo test --locked --all-features
  python3 -m unittest discover --start-directory tests --pattern 'test_*.py'
  python3 scripts/validate_identity.py --repository-root tests/fixtures/v1/valid/minimal --format human
  cd renderer
  corepack pnpm run check
  corepack pnpm test
  corepack pnpm build
  corepack pnpm run validate:public
}

command_name="${1:-help}"
if (($#)); then shift; fi
case "$command_name" in
  setup) tools; deps; build ;;
  tools) tools ;;
  deps) deps ;;
  build) build ;;
  check) check ;;
  browsers)
    cd "$repo_root/renderer"
    corepack pnpm exec playwright install "$@" chromium
    ;;
  e2e)
    cd "$repo_root/renderer"
    corepack pnpm build
    corepack pnpm test:e2e "$@"
    ;;
  preview)
    cd "$repo_root/renderer"
    corepack pnpm build
    exec corepack pnpm run preview -- --host "${IDENTITY_DEV_HOST:-127.0.0.1}" --port "${IDENTITY_DEV_PORT:-4173}" "$@"
    ;;
  exec)
    if (($# == 0)); then printf 'exec requires a command\n' >&2; exit 2; fi
    cd "$repo_root"
    exec "$@"
    ;;
  help|--help|-h)
    printf '%s\n' 'Usage: bash scripts/dev-env.sh {setup|tools|deps|build|check|browsers|e2e|preview|exec COMMAND...}' 'browsers accepts --with-deps for supported Linux images (requires OS package privileges).' 'Override IDENTITY_DEV_PREFIX and existing CARGO_HOME/RUSTUP_HOME/cache bindings to reuse base-image tools.'
    ;;
  *) printf 'Unknown command: %s\n' "$command_name" >&2; exit 2 ;;
esac
