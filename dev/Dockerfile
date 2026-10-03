# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Supply a base with Bash, Python >=3.11, Node >=24, curl, CA certificates,
# a C compiler/linker, and a user able to write /opt/identity{,-dev}.
ARG BASE_IMAGE=node:24-bookworm
FROM ${BASE_IMAGE}
ENV IDENTITY_DEV_PREFIX=/opt/identity-dev
WORKDIR /opt/identity
COPY . .
RUN bash scripts/dev-env.sh setup
# Browser dependencies are an explicit image option, independent of CLI setup.
ARG WITH_BROWSERS=0
RUN if [ "$WITH_BROWSERS" = 1 ]; then bash scripts/dev-env.sh browsers --with-deps; fi
# Does not replace the base image's ENTRYPOINT or CMD. The wrapper activates tools.
