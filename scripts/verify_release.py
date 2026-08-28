#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Verify the version and documentation contract used by an Identity release."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)

REQUIRED_DOCUMENTS = (
    "CHANGELOG.md",
    "SECURITY.md",
    "SUPPORT.md",
    "docs/releases/V1.md",
    "docs/releases/LICENSE_INVENTORY.md",
    "docs/releases/RELEASE_PROCESS.md",
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root to inspect.",
    )
    parser.add_argument(
        "--tag",
        help="Release tag that must exactly match the package version, for example v1.0.0-rc.1.",
    )
    return parser.parse_args()


def package_version(repository_root: Path) -> str:
    with (repository_root / "Cargo.toml").open("rb") as source:
        cargo = tomllib.load(source)
    version = cargo.get("package", {}).get("version")
    if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
        raise RuntimeError("Cargo.toml package.version must be valid semantic versioning")
    return version


def renderer_version(repository_root: Path) -> str:
    package_path = repository_root / "renderer" / "package.json"
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"renderer/package.json is invalid JSON: {error}") from error
    version = package.get("version")
    if not isinstance(version, str):
        raise RuntimeError("renderer/package.json must declare a string version")
    return version


def main() -> int:
    arguments = parse_arguments()
    repository_root = arguments.repository_root.resolve()
    version = package_version(repository_root)
    missing = [document for document in REQUIRED_DOCUMENTS if not (repository_root / document).is_file()]
    if missing:
        raise RuntimeError(f"release documentation is missing: {', '.join(missing)}")

    renderer = renderer_version(repository_root)
    if renderer != version:
        raise RuntimeError(
            "renderer/package.json version must match Cargo.toml package.version: "
            f"{renderer!r} != {version!r}"
        )

    if arguments.tag is not None and arguments.tag != f"v{version}":
        raise RuntimeError(
            f"release tag {arguments.tag!r} must exactly match Cargo.toml version v{version}"
        )

    print(
        "release metadata passed: "
        f"version={version}, renderer={renderer}, tag={arguments.tag or 'not-checked'}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"release metadata failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
