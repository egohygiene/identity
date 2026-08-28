#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Build Identity in isolation and prove a new consumer can generate v1 output.

The script deliberately uses only the Python standard library.  It copies the
current source tree (rather than relying on the caller's Cargo target cache),
builds the CLI from that copy with the committed lockfile, and generates the
same fixture twice in separate clean consumer directories.  Matching output
digests are the clean-room reproducibility evidence for the release gate.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


IGNORED_SOURCE_NAMES = {".git", "target", "node_modules", "test-results", "playwright-report"}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root to copy and build.",
    )
    return parser.parse_args()


def ignore_source(directory: str, names: list[str]) -> set[str]:
    del directory
    return {name for name in names if name in IGNORED_SOURCE_NAMES}


def run(arguments: list[str], *, cwd: Path) -> None:
    try:
        completed = subprocess.run(
            arguments,
            cwd=cwd,
            check=False,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(f"required command is unavailable: {arguments[0]}") from error
    if completed.returncode == 0:
        return

    command = " ".join(arguments)
    raise RuntimeError(
        f"command failed ({completed.returncode}): {command}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )


def tree_digest(root: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        contents = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest(), len(files)


def generated_digest(binary: Path, fixture: Path, destination: Path) -> tuple[str, int]:
    shutil.copytree(fixture, destination)
    run(
        [str(binary), "v1-generate", "--repository-root", str(destination)],
        cwd=destination,
    )
    run(
        [str(binary), "v1-verify", "--repository-root", str(destination)],
        cwd=destination,
    )

    generated = destination / "assets" / "identity"
    if not generated.is_dir():
        raise RuntimeError("v1-generate did not create assets/identity")
    return tree_digest(generated)


def main() -> int:
    arguments = parse_arguments()
    repository_root = arguments.repository_root.resolve()
    fixture = repository_root / "tests" / "fixtures" / "v1" / "valid" / "minimal"
    if not fixture.is_dir():
        raise RuntimeError(f"missing v1 fixture: {fixture}")

    with tempfile.TemporaryDirectory(prefix="identity-release-smoke-") as temporary:
        temporary_root = Path(temporary)
        clean_repository = temporary_root / "identity"
        shutil.copytree(repository_root, clean_repository, ignore=ignore_source)
        run(["cargo", "build", "--locked", "--release"], cwd=clean_repository)

        executable_name = "identity.exe" if sys.platform == "win32" else "identity"
        binary = clean_repository / "target" / "release" / executable_name
        if not binary.is_file():
            raise RuntimeError(f"release build did not produce {binary}")

        copied_fixture = clean_repository / "tests" / "fixtures" / "v1" / "valid" / "minimal"
        first_digest, first_count = generated_digest(binary, copied_fixture, temporary_root / "consumer-one")
        second_digest, second_count = generated_digest(binary, copied_fixture, temporary_root / "consumer-two")

    if first_digest != second_digest or first_count != second_count:
        raise RuntimeError(
            "clean-room generations differ: "
            f"first={first_digest}/{first_count}, second={second_digest}/{second_count}"
        )

    print(
        "release smoke passed: "
        f"{first_count} generated files, sha256:{first_digest}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"release smoke failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
