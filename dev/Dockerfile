# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Supply a base with Bash, Python >=3.11, Node >=24, curl, CA certificates,
# a C compiler/linker, and a user able to write /opt/identity{,-dev}.
# Refresh the digest through docs/DEVELOPMENT.md; qualify the selected platform.
ARG BASE_IMAGE=docker.io/library/node:24-bookworm@sha256:14078204b6bb268c107ceff6d3c43f45a888105e5c2b18b14c32b3409d93a1b0
FROM ${BASE_IMAGE}
ENV IDENTITY_DEV_PREFIX=/opt/identity-dev
WORKDIR /opt/identity
# Match an inherited non-root build user without changing USER/ENTRYPOINT/CMD.
ARG IDENTITY_DEV_UID=0
ARG IDENTITY_DEV_GID=0
COPY --chown=${IDENTITY_DEV_UID}:${IDENTITY_DEV_GID} . .
RUN bash scripts/dev-env.sh setup
# Browser dependencies are an explicit image option, independent of CLI setup.
ARG WITH_BROWSERS=0
RUN if [ "$WITH_BROWSERS" = 1 ]; then bash scripts/dev-env.sh browsers --with-deps; fi
# Does not replace the base image's ENTRYPOINT or CMD. The wrapper activates tools.
