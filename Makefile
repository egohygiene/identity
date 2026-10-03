# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
.PHONY: help setup tools deps build check browsers e2e preview
DEV_ARGS ?=
help:
	@bash scripts/dev-env.sh help

setup tools deps build check browsers e2e preview:
	@bash scripts/dev-env.sh $@ $(DEV_ARGS)
