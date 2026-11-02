# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal project validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import (
    COMPATIBILITY_KEYS,
    DIRECTORY_KEYS,
    DOCUMENT_KEYS,
    DOCUMENT_REQUIRED_KEYS,
    Diagnostic,
    GUIDANCE_KEYS,
    HANDBOOK_KEYS,
    HTTPS_URL,
    IDENTIFIER,
    PROJECT_KEYS,
    PROJECT_METADATA_KEYS,
    PROJECT_SCHEMA,
    diagnostic,
    require_closed,
    resolve_local_path,
)


def validate_project(
    project: dict[str, Any], repository_root: Path, diagnostics: list[Diagnostic]
) -> dict[str, Any]:
    """Validate root structure, metadata, topology, and compatibility."""

    require_closed(project, PROJECT_KEYS, PROJECT_KEYS, "/", diagnostics)
    if project.get("schema") != PROJECT_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1002",
            "/schema",
            f"schema must be {PROJECT_SCHEMA}",
            "Run the explicit v0-to-v1 migration before validating this source.",
        )
    schema_reference = project.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference.endswith(
        "/project.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1002",
            "/$schema",
            "schema reference must end in /project.schema.json",
            "Reference the checked-in Identity v1 project schema.",
        )

    metadata = require_closed(
        project.get("project"),
        PROJECT_METADATA_KEYS,
        PROJECT_METADATA_KEYS,
        "/project",
        diagnostics,
    )
    if metadata is not None:
        if not isinstance(metadata.get("id"), str) or IDENTIFIER.fullmatch(metadata["id"]) is None:
            diagnostic(
                diagnostics,
                "IDN1101",
                "/project/id",
                "project id must use lowercase letters, digits, and hyphens",
                "Choose a stable lowercase identifier.",
            )
        for field in ("displayName", "tagline"):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                diagnostic(
                    diagnostics,
                    "IDN1101",
                    f"/project/{field}",
                    "value must be a non-empty string",
                    "Provide reviewed project metadata.",
                )
        if (
            not isinstance(metadata.get("repository"), str)
            or HTTPS_URL.fullmatch(metadata["repository"]) is None
        ):
            diagnostic(
                diagnostics,
                "IDN1101",
                "/project/repository",
                "repository must be an HTTPS URL",
                "Provide the canonical HTTPS repository URL.",
            )
        if metadata.get("kind") not in {"organization", "product", "repository"}:
            diagnostic(
                diagnostics,
                "IDN1101",
                "/project/kind",
                "kind is unsupported",
                "Use organization, product, or repository.",
            )

    documents = require_closed(
        project.get("documents"), DOCUMENT_KEYS, DOCUMENT_REQUIRED_KEYS, "/documents", diagnostics
    )
    if documents is not None:
        for field in ("brief", "targets", "provenance", "approvals"):
            resolve_local_path(
                repository_root,
                documents.get(field),
                f"/documents/{field}",
                diagnostics,
            )
        guidance = require_closed(
            documents.get("guidance"),
            GUIDANCE_KEYS,
            GUIDANCE_KEYS,
            "/documents/guidance",
            diagnostics,
        )
        if guidance is not None:
            for field in ("voice", "usage"):
                if guidance.get(field) is not None:
                    resolve_local_path(
                        repository_root,
                        guidance[field],
                        f"/documents/guidance/{field}",
                        diagnostics,
                    )
        handbook = project.get("documents", {}).get("handbook")
        if handbook is not None:
            handbook = require_closed(
                handbook,
                HANDBOOK_KEYS,
                HANDBOOK_KEYS,
                "/documents/handbook",
                diagnostics,
            )
            if handbook is not None:
                for field in ("designSystem", "references"):
                    resolve_local_path(
                        repository_root,
                        handbook.get(field),
                        f"/documents/handbook/{field}",
                        diagnostics,
                    )
        press_kit = documents.get("pressKit")
        if press_kit is not None:
            resolve_local_path(
                repository_root,
                press_kit,
                "/documents/pressKit",
                diagnostics,
            )
        social_surfaces = documents.get("socialSurfaces")
        if social_surfaces is not None:
            resolve_local_path(
                repository_root,
                social_surfaces,
                "/documents/socialSurfaces",
                diagnostics,
            )
        repository_presentation = documents.get("repositoryPresentation")
        if repository_presentation is not None:
            resolve_local_path(
                repository_root,
                repository_presentation,
                "/documents/repositoryPresentation",
                diagnostics,
            )
        mascot = documents.get("mascot")
        if mascot is not None:
            resolve_local_path(
                repository_root,
                mascot,
                "/documents/mascot",
                diagnostics,
            )

    directories = require_closed(
        project.get("directories"), DIRECTORY_KEYS, DIRECTORY_KEYS, "/directories", diagnostics
    )
    if directories is not None:
        for field in sorted(DIRECTORY_KEYS):
            resolve_local_path(
                repository_root,
                directories.get(field),
                f"/directories/{field}",
                diagnostics,
                directory=True,
            )

    compatibility = require_closed(
        project.get("compatibility"),
        COMPATIBILITY_KEYS,
        COMPATIBILITY_KEYS,
        "/compatibility",
        diagnostics,
    )
    if compatibility is not None:
        if compatibility.get("acceptedSchemaMajor") != 1:
            diagnostic(
                diagnostics,
                "IDN1502",
                "/compatibility/acceptedSchemaMajor",
                "v1 requires accepted schema major 1",
                "Migrate explicitly before selecting another major.",
            )
        migration_from = compatibility.get("migrationFrom")
        if not isinstance(migration_from, list) or any(
            not isinstance(value, str) or not value for value in migration_from
        ):
            diagnostic(
                diagnostics,
                "IDN1502",
                "/compatibility/migrationFrom",
                "migrationFrom must be an array of contract identities",
                "Use an empty array or list every migrated contract identity.",
            )
    return project
