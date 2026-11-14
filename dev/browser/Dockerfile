# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# The profile and dated registry receipt own this immutable browser environment.
ARG BROWSER_IMAGE=mcr.microsoft.com/playwright:v1.62.1-noble@sha256:dcc5531e97840b9b5e794f2814476b21571c5124a3fca2267d73041f56e7580e
FROM ${BROWSER_IMAGE}
ENV CI=1 TZ=UTC LANG=C.UTF-8 LC_ALL=C.UTF-8 PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
ENV PATH=/opt/identity-browser-tools/bin:/opt/identity-browser-tools/corepack/node_modules/.bin:$PATH
WORKDIR /opt/identity/renderer
COPY . /opt/identity
# Reuse the digest-pinned base tool; use the repository's existing fallback if absent.
# One installation layer also bounds temporary storage on local vfs daemons.
RUN --mount=type=secret,id=identity_proxy_ca \
    export NODE_USE_ENV_PROXY=1 \
    && if [ -f /run/secrets/identity_proxy_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/identity_proxy_ca; fi \
    && node ../dev/browser/install-fonts.mjs \
    && mkdir -p /opt/identity-browser-tools/bin \
    && if ! command -v corepack >/dev/null 2>&1; then npm install --prefix /opt/identity-browser-tools/corepack --no-audit --no-fund corepack@0.34.6; fi \
    && corepack enable --install-directory /opt/identity-browser-tools/bin \
    && corepack pnpm install --frozen-lockfile \
    && corepack pnpm run build
