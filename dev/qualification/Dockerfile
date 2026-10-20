# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Qualification-only example: provision a non-root development user in the base.
# The repository add-on continues to own all repository setup.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN mkdir -p /opt/identity /opt/identity-dev \
    && chown 1000:1000 /opt/identity /opt/identity-dev
USER 1000:1000
