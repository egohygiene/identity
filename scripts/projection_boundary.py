# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Shared stdlib projection mechanics; format-specific policy stays with callers."""

from __future__ import annotations

import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

import validate_identity as validator


def load_json_object(path: Path, *, error_type: type[ValueError]) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise error_type(f"document must be an object: {path}")
    return value


def approved_public(value: dict[str, Any]) -> bool:
    """Guidance predicate, used only after authoritative source validation."""
    governance = value.get("governance")
    return (
        isinstance(governance, dict)
        and governance.get("state") == "approved"
        and governance.get("visibility") == "public"
    )


def approved_public_with_approval(value: dict[str, Any]) -> bool:
    """Press Kit admission additionally requires the existing approval identity."""
    return approved_public(value) and isinstance(value["governance"].get("approval"), str)


def source_digest(repository_root: Path, *, error_type: type[ValueError]) -> str:
    try:
        return validator.canonical_source_digest(repository_root)
    except (OSError, ValueError) as error:
        raise error_type(str(error)) from error


def generated_directory(
    repository_root: Path, value: Path, *, error_type: type[ValueError], canonical_error: str,
) -> Path:
    relative = value.as_posix()
    if not validator.valid_relative_path(relative):
        raise error_type("output directory must be normalized and repository-relative")
    if relative == ".identity" or relative.startswith(".identity/"):
        raise error_type(canonical_error)
    current = repository_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise error_type("output directory may not traverse a symbolic link")
    return repository_root / relative


def render_json(value: Any) -> str:
    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def temporary_file(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.with_name(f".{path.name}.tmp")


def atomic_write_text(path: Path, content: str) -> None:
    temporary = temporary_file(path)
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    temporary = temporary_file(path)
    temporary.write_bytes(content)
    os.replace(temporary, path)
