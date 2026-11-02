# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal targets validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import (
    Diagnostic,
    IDENTIFIER,
    SEMVER,
    TARGETS_SCHEMA,
    TARGET_KEYS,
    TARGET_PROFILE_KEYS,
    V1_PROFILE_VERSIONS,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)


def validate_targets(
    project: dict[str, Any],
    repository_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    """Validate the consumer's versioned projection-profile selection."""

    documents = project.get("documents")
    if not isinstance(documents, dict):
        return
    path_value = documents.get("targets")
    path = resolve_local_path(repository_root, path_value, "/documents/targets", diagnostics)
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, TARGET_KEYS, TARGET_KEYS, "/", diagnostics)
    if document.get("schema") != TARGETS_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1501",
            f"{path_value}#/schema",
            f"target schema must be {TARGETS_SCHEMA}",
            "Migrate target selection to v1.",
        )
    enabled = document.get("enabled")
    if not isinstance(enabled, list) or not enabled:
        diagnostic(
            diagnostics,
            "IDN1501",
            f"{path_value}#/enabled",
            "at least one target profile is required",
            "Select one or more versioned profiles.",
        )
        return
    seen: set[str] = set()
    for index, profile in enumerate(enabled):
        pointer = f"{path_value}#/enabled/{index}"
        value = require_closed(
            profile,
            TARGET_PROFILE_KEYS,
            TARGET_PROFILE_KEYS,
            pointer,
            diagnostics,
        )
        if value is None:
            continue
        identifier = value.get("id")
        version = value.get("version")
        if (
            not isinstance(identifier, str)
            or IDENTIFIER.fullmatch(identifier) is None
            or identifier in seen
        ):
            diagnostic(
                diagnostics,
                "IDN1501",
                f"{pointer}/id",
                "profile id is invalid or duplicated",
                "Select each stable profile id once.",
            )
            continue
        seen.add(identifier)
        if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
            diagnostic(
                diagnostics,
                "IDN1501",
                f"{pointer}/version",
                "profile version must use MAJOR.MINOR.PATCH",
                "Pin an available semantic profile version.",
            )
            continue
        available_version = V1_PROFILE_VERSIONS.get(identifier)
        if available_version is None:
            diagnostic(
                diagnostics,
                "IDN1501",
                pointer,
                f"profile is not available: {identifier}@{version}",
                "Select a profile shipped by this Identity v1 package catalog.",
            )
            continue
        if available_version != version:
            diagnostic(
                diagnostics,
                "IDN1501",
                f"{pointer}/version",
                f"selected {version}, available {available_version}",
                "Pin the available profile version or update Identity explicitly.",
            )
    inapplicable = document.get("inapplicable")
    if not isinstance(inapplicable, list) or any(
        not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None for value in inapplicable
    ):
        diagnostic(
            diagnostics,
            "IDN1501",
            f"{path_value}#/inapplicable",
            "inapplicable must contain stable profile IDs",
            "Use a unique array of lowercase profile IDs.",
        )
    elif len(inapplicable) != len(set(inapplicable)) or seen.intersection(inapplicable):
        diagnostic(
            diagnostics,
            "IDN1501",
            f"{path_value}#/inapplicable",
            "profiles cannot be duplicated or both enabled and inapplicable",
            "Select one disposition for each profile.",
        )
