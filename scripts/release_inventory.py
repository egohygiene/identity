#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Create a deterministic license inventory from Cargo's locked metadata."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


SCHEMA = "identity.license-inventory/v1"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root whose locked Cargo graph is inventoried.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination JSON file for the deterministic inventory.",
    )
    return parser.parse_args()


def cargo_metadata(repository_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        ["cargo", "metadata", "--locked", "--format-version", "1"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"cargo metadata failed:\n{completed.stderr}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"cargo metadata returned invalid JSON: {error}") from error


def cargo_version(repository_root: Path) -> str:
    with (repository_root / "Cargo.toml").open("rb") as source:
        manifest = tomllib.load(source)
    version = manifest.get("package", {}).get("version")
    if not isinstance(version, str):
        raise RuntimeError("Cargo.toml package.version is missing")
    return version


def inventory(metadata: dict[str, Any], *, release_version: str) -> dict[str, Any]:
    packages = metadata.get("packages")
    if not isinstance(packages, list):
        raise RuntimeError("cargo metadata did not include a packages list")

    entries: list[dict[str, str]] = []
    missing_licenses: list[str] = []
    for package in packages:
        if not isinstance(package, dict):
            raise RuntimeError("cargo metadata package entry was not an object")
        name = package.get("name")
        version = package.get("version")
        source = package.get("source") or "workspace"
        license_expression = package.get("license")
        if not isinstance(name, str) or not isinstance(version, str) or not isinstance(source, str):
            raise RuntimeError("cargo metadata package entry was missing name, version, or source")
        if not isinstance(license_expression, str) or not license_expression.strip():
            missing_licenses.append(f"{name}@{version}")
            license_expression = "NOASSERTION"
        entries.append(
            {
                "name": name,
                "version": version,
                "source": source,
                "license": license_expression,
            }
        )

    entries.sort(key=lambda entry: (entry["name"], entry["version"], entry["source"]))
    return {
        "schema": SCHEMA,
        "releaseVersion": release_version,
        "packages": entries,
        "missingLicenseDeclarations": sorted(missing_licenses),
    }


def main() -> int:
    arguments = parse_arguments()
    repository_root = arguments.repository_root.resolve()
    result = inventory(cargo_metadata(repository_root), release_version=cargo_version(repository_root))
    if result["missingLicenseDeclarations"]:
        missing = ", ".join(result["missingLicenseDeclarations"])
        raise RuntimeError(f"locked dependency graph has packages without licenses: {missing}")

    output = arguments.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"license inventory passed: {len(result['packages'])} packages")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"license inventory failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
