#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Apply Identity's bounded subpath adapter to a materialized Holon site suite."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit


PUBLIC_BASE = "/identity/"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--corepack-executable", default="corepack")
    parser.add_argument("command", choices=("build", "check", "verify"))
    return parser.parse_args()


def normalize_reference(reference: str) -> str:
    """Translate the accepted public subpath into Holon's artifact-root view."""
    split = urlsplit(reference)
    if split.scheme or split.netloc:
        return reference
    if split.path == PUBLIC_BASE.rstrip("/"):
        path = "/"
    elif split.path.startswith(PUBLIC_BASE):
        path = "/" + split.path.removeprefix(PUBLIC_BASE)
    else:
        return reference
    return urlunsplit((split.scheme, split.netloc, path, split.query, split.fragment))


def load_suite(site_root: Path):
    source = site_root.resolve() / "site_suite.py"
    specification = importlib.util.spec_from_file_location(
        "identity_materialized_site_suite",
        source,
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("unable to load the materialized Holon site suite")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def apply_adapter(suite, corepack: str) -> None:
    """Patch only command invocation and public-base reference resolution."""
    original_reference_target = suite.reference_target
    original_run = suite.run
    original_compose = suite.compose

    def reference_target(page: Path, reference: str):
        return original_reference_target(page, normalize_reference(reference))

    def run(command: list[str]) -> None:
        if command and command[0] == "pnpm":
            command = [corepack, "pnpm", *command[1:]]
        original_run(command)

    def compose() -> None:
        original_compose()
        # LaunchKit's static fallback links the consumer-owned evidence route.
        # The final Identity composer replaces this existence proof with the
        # complete non-recursive publication manifest after suite verification.
        (suite.DIST / "publication.json").write_text("{}\n", encoding="utf-8")

    suite.reference_target = reference_target
    suite.run = run
    suite.compose = compose


def main() -> int:
    arguments = parse_arguments()
    try:
        suite = load_suite(arguments.site_root)
        apply_adapter(suite, arguments.corepack_executable)
        if arguments.command == "check":
            suite.check()
        elif arguments.command == "build":
            suite.build()
        else:
            suite.verify()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
