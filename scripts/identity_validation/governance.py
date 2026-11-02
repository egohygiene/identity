# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal governance validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
from .common import (
    ACCESSIBILITY_KEYS,
    APPROVALS_SCHEMA,
    APPROVAL_KEYS,
    APPROVAL_ROOT_KEYS,
    ASSET_KEYS,
    Diagnostic,
    IDENTIFIER,
    LICENSE_KEYS,
    ORIGIN_KEYS,
    PROVENANCE_ROOT_KEYS,
    PROVENANCE_SCHEMA,
    USAGE_KEYS,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
    sha256,
    valid_relative_path,
)


def validate_approvals(
    project: dict[str, Any], repository_root: Path, diagnostics: list[Diagnostic]
) -> dict[str, dict[str, Any]]:
    """Load human decisions before validating governed assets and overrides."""

    documents = project.get("documents")
    if not isinstance(documents, dict):
        return {}
    path_value = documents.get("approvals")
    path = resolve_local_path(repository_root, path_value, "/documents/approvals", diagnostics)
    if path is None:
        return {}
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return {}
    require_closed(document, APPROVAL_ROOT_KEYS, APPROVAL_ROOT_KEYS, "/", diagnostics)
    if document.get("schema") != APPROVALS_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1404",
            f"{path_value}#/schema",
            f"approval schema must be {APPROVALS_SCHEMA}",
            "Migrate approval decisions to v1.",
        )
    decisions = document.get("decisions")
    if not isinstance(decisions, list):
        diagnostic(
            diagnostics,
            "IDN1404",
            f"{path_value}#/decisions",
            "decisions must be an array",
            "Use an array.",
        )
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, decision in enumerate(decisions):
        pointer = f"{path_value}#/decisions/{index}"
        value = require_closed(decision, APPROVAL_KEYS, APPROVAL_KEYS, pointer, diagnostics)
        if value is None:
            continue
        identifier = value.get("id")
        if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/id",
                "approval id is invalid",
                "Use a stable lowercase ID.",
            )
            continue
        if identifier in result:
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/id",
                "approval id is duplicated",
                "Use a unique ID.",
            )
        result[identifier] = value
        if value.get("status") not in {"approved", "rejected", "superseded"}:
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/status",
                "approval status is unsupported",
                "Use approved, rejected, or superseded.",
            )
        for field in ("subject", "candidate", "reviewedBy", "evidence"):
            if not isinstance(value.get(field), str) or not value[field].strip():
                diagnostic(
                    diagnostics,
                    "IDN1404",
                    f"{pointer}/{field}",
                    "approval evidence field must be non-empty",
                    "Record the human reviewer and evidence.",
                )
        try:
            datetime.fromisoformat(str(value.get("reviewedAt", "")).replace("Z", "+00:00"))
        except ValueError:
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/reviewedAt",
                "reviewedAt must be an RFC 3339 timestamp",
                "Record the review time with an explicit UTC offset.",
            )
        supersedes = value.get("supersedes")
        if supersedes is not None and (
            not isinstance(supersedes, str)
            or IDENTIFIER.fullmatch(supersedes) is None
            or supersedes == identifier
        ):
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/supersedes",
                "supersedes must reference a different stable approval id",
                "Use null or the stable ID of the earlier decision.",
            )
    for identifier, value in result.items():
        supersedes = value.get("supersedes")
        if value.get("status") == "superseded" and not isinstance(supersedes, str):
            diagnostic(
                diagnostics,
                "IDN1404",
                f"approval:{identifier}/supersedes",
                "superseded decision must name the earlier decision",
                "Link the exact earlier approval for the same subject.",
            )
        if isinstance(supersedes, str) and supersedes not in result:
            diagnostic(
                diagnostics,
                "IDN1404",
                f"approval:{identifier}/supersedes",
                "superseded decision does not exist",
                "Restore the earlier decision or remove the stale reference.",
            )
        elif (
            isinstance(supersedes, str)
            and result[supersedes].get("subject") != value.get("subject")
        ):
            diagnostic(
                diagnostics,
                "IDN1404",
                f"approval:{identifier}/supersedes",
                "decision chain changes subject",
                "Reference an earlier decision for the exact same subject.",
            )
    return result


def validate_provenance(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Verify approved source bytes, licenses, provenance, usage, and decisions."""

    documents = project.get("documents")
    directories = project.get("directories")
    if not isinstance(documents, dict) or not isinstance(directories, dict):
        return
    path_value = documents.get("provenance")
    path = resolve_local_path(repository_root, path_value, "/documents/provenance", diagnostics)
    source_root = resolve_local_path(
        repository_root,
        directories.get("sources"),
        "/directories/sources",
        diagnostics,
        directory=True,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, PROVENANCE_ROOT_KEYS, PROVENANCE_ROOT_KEYS, "/", diagnostics)
    if document.get("schema") != PROVENANCE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1401",
            f"{path_value}#/schema",
            f"provenance schema must be {PROVENANCE_SCHEMA}",
            "Migrate provenance records to v1.",
        )
    assets = document.get("assets")
    if not isinstance(assets, list):
        diagnostic(
            diagnostics,
            "IDN1401",
            f"{path_value}#/assets",
            "assets must be an array",
            "Use an array.",
        )
        return
    by_path: dict[str, dict[str, Any]] = {}
    for index, asset in enumerate(assets):
        pointer = f"{path_value}#/assets/{index}"
        value = require_closed(asset, ASSET_KEYS, ASSET_KEYS, pointer, diagnostics)
        if value is None:
            continue
        asset_path = value.get("path")
        if not isinstance(asset_path, str) or not valid_relative_path(asset_path):
            diagnostic(
                diagnostics,
                "IDN1401",
                f"{pointer}/path",
                "asset path must be normalized and repository-relative",
                "Point to one local governed asset.",
            )
            continue
        if asset_path in by_path:
            diagnostic(
                diagnostics,
                "IDN1401",
                f"{pointer}/path",
                "asset path is duplicated",
                "Keep one record per asset.",
            )
        by_path[asset_path] = value
        asset_file = repository_root / asset_path
        if not asset_file.is_file():
            diagnostic(
                diagnostics,
                "IDN1401",
                f"{pointer}/path",
                "governed asset does not exist",
                "Restore the asset or remove the stale record through review.",
            )
        elif value.get("sha256") != sha256(asset_file):
            diagnostic(
                diagnostics,
                "IDN1403",
                f"{pointer}/sha256",
                "asset digest does not match local bytes",
                "Review the asset change and update its digest intentionally.",
            )
        license_value = require_closed(
            value.get("license"), LICENSE_KEYS, LICENSE_KEYS, f"{pointer}/license", diagnostics
        )
        if license_value is not None:
            spdx = license_value.get("spdx")
            if (
                not isinstance(spdx, str)
                or not spdx.strip()
                or spdx.upper() in {"NONE", "NOASSERTION", "UNKNOWN"}
                or license_value.get("status") != "approved"
            ):
                diagnostic(
                    diagnostics,
                    "IDN1402",
                    f"{pointer}/license",
                    "asset license is missing, unknown, or unapproved",
                    "Record a reviewed SPDX expression and approved status.",
                )
        origin = require_closed(
            value.get("origin"),
            ORIGIN_KEYS,
            ORIGIN_KEYS,
            f"{pointer}/origin",
            diagnostics,
        )
        if origin is not None and any(
            not isinstance(origin.get(field), str) or not origin[field].strip()
            for field in ("creator", "method", "source", "capturedAt")
        ):
            diagnostic(
                diagnostics,
                "IDN1405",
                f"{pointer}/origin",
                "asset provenance is incomplete",
                "Record creator, method, source, and capture time.",
            )
        elif origin is not None and origin.get("method") not in {
            "first-party",
            "commissioned",
            "licensed",
            "generated",
        }:
            diagnostic(
                diagnostics,
                "IDN1405",
                f"{pointer}/origin/method",
                "asset origin method is unsupported",
                "Use first-party, commissioned, licensed, or generated.",
            )
        accessibility = require_closed(
            value.get("accessibility"),
            ACCESSIBILITY_KEYS,
            ACCESSIBILITY_KEYS,
            f"{pointer}/accessibility",
            diagnostics,
        )
        if accessibility is not None and (
            not isinstance(accessibility.get("altText"), str)
            or not accessibility["altText"].strip()
        ):
            diagnostic(
                diagnostics,
                "IDN1405",
                f"{pointer}/accessibility/altText",
                "approved visual asset requires alt text",
                "Add a human-reviewed accessible description.",
            )
        require_closed(value.get("usage"), USAGE_KEYS, USAGE_KEYS, f"{pointer}/usage", diagnostics)
        approval_id = value.get("approval")
        decision = approvals.get(approval_id) if isinstance(approval_id, str) else None
        if (
            decision is None
            or decision.get("status") != "approved"
            or decision.get("subject") != value.get("id")
        ):
            diagnostic(
                diagnostics,
                "IDN1404",
                f"{pointer}/approval",
                "asset does not resolve to an approved decision for the same subject",
                "Add or correct the linked human approval record.",
            )

    if source_root is not None:
        for source in sorted(path for path in source_root.rglob("*") if path.is_file()):
            if source.name in {"README.md", ".gitkeep"}:
                continue
            relative = source.relative_to(repository_root).as_posix()
            if relative not in by_path:
                diagnostic(
                    diagnostics,
                    "IDN1401",
                    relative,
                    "approved source has no provenance record",
                    "Add license, provenance, usage, digest, and approval evidence.",
                )
