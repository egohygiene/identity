# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Pure source selection shared by the host and development-image smoke."""

import hashlib
from pathlib import Path


INPUTS = (
    "Cargo.toml", "Cargo.lock", "rust-toolchain.toml",
    "renderer/package.json", "renderer/pnpm-lock.yaml",
)
SOURCE_ROOTS = ("src", "tests/fixtures/v1/valid/minimal/.identity")


def source_inventory(repository: Path) -> dict[str, str]:
    paths = set(INPUTS)
    for relative in SOURCE_ROOTS:
        directory = repository / relative
        if directory.is_symlink():
            raise RuntimeError(f"Repeat setup requires a regular source directory: {relative}")
        if directory.exists():
            paths.update(
                path.relative_to(repository).as_posix()
                for path in directory.rglob("*")
                if path.is_file() or path.is_symlink()
            )
    values = {}
    for relative in sorted(paths):
        path = repository / relative
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"Repeat setup requires a regular source input: {relative}")
        values[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values
