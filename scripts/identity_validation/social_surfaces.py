# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal social surfaces validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any
from .common import (
    Diagnostic,
    IDENTIFIER,
    SHA256,
    SOCIAL_SURFACE_ADOPTION_KEYS,
    SOCIAL_SURFACE_CATALOG_KEYS,
    SOCIAL_SURFACE_DEFAULT_KEYS,
    SOCIAL_SURFACE_DIGEST_KEYS,
    SOCIAL_SURFACE_EXCLUSION_KEYS,
    SOCIAL_SURFACE_OVERRIDE_KEYS,
    SOCIAL_SURFACE_PROJECT_KEYS,
    SOCIAL_SURFACE_RECORD_REQUIRED_KEYS,
    SOCIAL_SURFACE_ROOT_KEYS,
    SOCIAL_SURFACE_SOURCE_SCHEMA,
    diagnostic,
    load_json,
    read_source_bytes,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance


def validate_social_surfaces(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate optional pinned social-surface selections and catalog evidence."""

    documents = project.get("documents")
    if not isinstance(documents, dict) or documents.get("socialSurfaces") is None:
        return
    path_value = documents["socialSurfaces"]
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/socialSurfaces",
        diagnostics,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(
        document,
        SOCIAL_SURFACE_ROOT_KEYS,
        SOCIAL_SURFACE_ROOT_KEYS,
        "/",
        diagnostics,
    )
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/social-surfaces.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1901",
            f"{path_value}#/$schema",
            "social-surface source must reference social-surfaces.schema.json",
            "Reference the checked-in Identity v1 social-surface source schema.",
        )
    if document.get("schema") != SOCIAL_SURFACE_SOURCE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1901",
            f"{path_value}#/schema",
            f"social-surface source schema must be {SOCIAL_SURFACE_SOURCE_SCHEMA}",
            "Migrate social-surface source through an explicit versioned change.",
        )

    catalog_lock = require_closed(
        document.get("catalog"),
        SOCIAL_SURFACE_CATALOG_KEYS,
        SOCIAL_SURFACE_CATALOG_KEYS,
        f"{path_value}#/catalog",
        diagnostics,
    )
    catalog_records: dict[str, dict[str, Any]] = {}
    if catalog_lock is not None:
        digest = require_closed(
            catalog_lock.get("digest"),
            SOCIAL_SURFACE_DIGEST_KEYS,
            SOCIAL_SURFACE_DIGEST_KEYS,
            f"{path_value}#/catalog/digest",
            diagnostics,
        )
        if digest is not None:
            if digest.get("algorithm") != "sha256-utf8-lf":
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{path_value}#/catalog/digest/algorithm",
                    "catalog lock must use sha256-utf8-lf",
                    "Pin the canonical Aether catalog text digest.",
                )
            if not isinstance(digest.get("value"), str) or SHA256.fullmatch(digest["value"]) is None:
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{path_value}#/catalog/digest/value",
                    "catalog digest must be 64 lowercase hexadecimal characters",
                    "Record the reviewed Aether catalog digest.",
                )
        catalog_path = resolve_local_path(
            repository_root,
            catalog_lock.get("path"),
            f"{path_value}#/catalog/path",
            diagnostics,
        )
        catalog = (
            load_json(catalog_path, str(catalog_lock.get("path")), diagnostics)
            if catalog_path is not None
            else None
        )
        if catalog is not None and catalog_path is not None:
            normalized = (
                read_source_bytes(catalog_path).decode("utf-8")
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .encode("utf-8")
            )
            actual_digest = hashlib.sha256(normalized).hexdigest()
            if not isinstance(digest, dict) or digest.get("value") != actual_digest:
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{path_value}#/catalog/digest/value",
                    f"catalog bytes differ from the pinned digest: {actual_digest}",
                    "Review the catalog update and replace its version and digest together.",
                )
            if catalog.get("schema_version") != "aether.social-surface-catalog/v1":
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{catalog_lock.get('path')}#/schema_version",
                    "catalog does not use the supported Aether social-surface contract",
                    "Supply a compatible pinned Aether catalog artifact.",
                )
            metadata = catalog.get("catalog")
            if not isinstance(metadata, dict):
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{catalog_lock.get('path')}#/catalog",
                    "catalog metadata must be an object",
                    "Supply a complete Aether catalog artifact.",
                )
            else:
                if metadata.get("id") != catalog_lock.get("id"):
                    diagnostic(
                        diagnostics,
                        "IDN1902",
                        f"{path_value}#/catalog/id",
                        "catalog identity differs from the selected artifact",
                        "Pin the exact catalog ID supplied as build input.",
                    )
                if metadata.get("version") != catalog_lock.get("version"):
                    diagnostic(
                        diagnostics,
                        "IDN1902",
                        f"{path_value}#/catalog/version",
                        "catalog version differs from the selected artifact",
                        "Pin the exact semantic catalog version supplied as build input.",
                    )
                lifecycle = metadata.get("lifecycle")
                rights = metadata.get("rights_review")
                release = metadata.get("release")
                if not isinstance(lifecycle, dict) or lifecycle.get("state") != "stable":
                    diagnostic(
                        diagnostics,
                        "IDN1902",
                        f"{catalog_lock.get('path')}#/catalog/lifecycle",
                        "selected catalog is not stable",
                        "Use a stable Aether catalog or keep the projection unadopted.",
                    )
                if not isinstance(rights, dict) or rights.get("state") != "approved":
                    diagnostic(
                        diagnostics,
                        "IDN1902",
                        f"{catalog_lock.get('path')}#/catalog/rights_review",
                        "selected catalog is not rights-approved",
                        "Use a catalog whose publication rights were explicitly approved.",
                    )
                if not isinstance(release, dict) or release.get("included") is not True:
                    diagnostic(
                        diagnostics,
                        "IDN1902",
                        f"{catalog_lock.get('path')}#/catalog/release",
                        "selected catalog is not release-included",
                        "Consume an immutable catalog artifact from Aether's release boundary.",
                    )
            records = catalog.get("records")
            if not isinstance(records, list):
                diagnostic(
                    diagnostics,
                    "IDN1902",
                    f"{catalog_lock.get('path')}#/records",
                    "catalog records must be an array",
                    "Supply a complete Aether catalog artifact.",
                )
            else:
                for index, item in enumerate(records):
                    identifier = item.get("id") if isinstance(item, dict) else None
                    if not isinstance(identifier, str) or identifier in catalog_records:
                        diagnostic(
                            diagnostics,
                            "IDN1902",
                            f"{catalog_lock.get('path')}#/records/{index}/id",
                            "catalog record ID is missing or duplicated",
                            "Use one stable ID for each catalog record.",
                        )
                    elif isinstance(item, dict):
                        catalog_records[identifier] = item

    guidance = documents.get("guidance")
    usage_path = guidance.get("usage") if isinstance(guidance, dict) else None
    usage_document = (
        load_json(repository_root / usage_path, str(usage_path), diagnostics)
        if isinstance(usage_path, str)
        else None
    )
    public_assets: set[Any] = set()
    if isinstance(usage_document, dict):
        public_assets = {
            item.get("id")
            for item in usage_document.get("assets", [])
            if isinstance(item, dict)
            and item.get("status") == "active"
            and item.get("availability") == "public"
            and isinstance(item.get("governance"), dict)
            and item["governance"].get("state") == "approved"
            and item["governance"].get("visibility") == "public"
        }

    def selection_value(value: Any, pointer: str, allowed: set[Any]) -> None:
        if value not in allowed:
            diagnostic(
                diagnostics,
                "IDN1901",
                pointer,
                "selection source is unsupported",
                "Select only a documented approved Identity project field or null.",
            )

    defaults = document.get("organizationDefaults")
    default_ids: set[str] = set()
    if not isinstance(defaults, list):
        diagnostic(
            diagnostics,
            "IDN1901",
            f"{path_value}#/organizationDefaults",
            "organizationDefaults must be an array",
            "Use an empty array or declare reviewed organization defaults.",
        )
    else:
        for index, item in enumerate(defaults):
            pointer = f"{path_value}#/organizationDefaults/{index}"
            value = require_closed(
                item,
                SOCIAL_SURFACE_DEFAULT_KEYS,
                SOCIAL_SURFACE_DEFAULT_KEYS,
                pointer,
                diagnostics,
            )
            if value is None:
                continue
            identifier = value.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in default_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1901",
                    f"{pointer}/id",
                    "organization default ID is invalid or duplicated",
                    "Use each stable lowercase selection ID once.",
                )
                continue
            default_ids.add(identifier)
            governance_value = validate_guidance_governance(
                value.get("governance"),
                f"{pointer}/governance",
                approvals,
                diagnostics,
            )
            expected_subject = f"social-surface-default:{identifier}"
            if isinstance(governance_value, dict) and governance_value.get("subject") != expected_subject:
                diagnostic(
                    diagnostics,
                    "IDN1901",
                    f"{pointer}/governance/subject",
                    "organization default governance subject does not match its ID",
                    f"Use {expected_subject} as the reviewed subject.",
                )
            surface_id = value.get("surfaceId")
            record = catalog_records.get(surface_id) if isinstance(surface_id, str) else None
            if record is None:
                diagnostic(
                    diagnostics,
                    "IDN1903",
                    f"{pointer}/surfaceId",
                    "selected surface does not resolve in the pinned catalog",
                    "Select an exact stable record ID from the locked catalog.",
                )
            else:
                missing_record_fields = sorted(SOCIAL_SURFACE_RECORD_REQUIRED_KEYS - set(record))
                if missing_record_fields:
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        f"selected surface omits required fields: {', '.join(missing_record_fields)}",
                        "Use a complete Aether v1 surface record or keep it out of generated targets.",
                    )
                dimensions = record.get("dimensions")
                if (
                    not isinstance(dimensions, dict)
                    or not isinstance(dimensions.get("width_px"), int)
                    or isinstance(dimensions.get("width_px"), bool)
                    or dimensions["width_px"] < 1
                    or not isinstance(dimensions.get("height_px"), int)
                    or isinstance(dimensions.get("height_px"), bool)
                    or dimensions["height_px"] < 1
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface has no usable positive integer dimensions",
                        "Choose a reviewed record with exact pixel dimensions.",
                    )
                if not isinstance(record.get("platform"), str) or not record["platform"].strip():
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface has no platform label",
                        "Use a complete Aether v1 surface record.",
                    )
                if not isinstance(record.get("placement"), str) or not record["placement"].strip():
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface has no placement label",
                        "Use a complete Aether v1 surface record.",
                    )
                if record.get("use") not in {"organic", "advertising"}:
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface has an unsupported usage category",
                        "Use organic or advertising from the Aether v1 contract.",
                    )
                for field in ("content_type", "media_format", "aspect_ratio"):
                    if record.get(field) is not None and not isinstance(record[field], str):
                        diagnostic(
                            diagnostics,
                            "IDN1903",
                            f"{pointer}/surfaceId",
                            f"selected surface {field} must be a string or null",
                            "Use a complete Aether v1 surface record.",
                        )
                file_types = record.get("file_types")
                if file_types is not None and (
                    not isinstance(file_types, list)
                    or any(not isinstance(item, str) or not item for item in file_types)
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface file types must be strings or null",
                        "Use the exact nullable Aether media constraint.",
                    )
                for field in ("file_size_limit_bytes", "duration_limit_seconds"):
                    constraint = record.get(field)
                    if constraint is not None and (
                        not isinstance(constraint, (int, float))
                        or isinstance(constraint, bool)
                        or constraint < 0
                    ):
                        diagnostic(
                            diagnostics,
                            "IDN1903",
                            f"{pointer}/surfaceId",
                            f"selected surface {field} must be non-negative or null",
                            "Use the exact nullable Aether media constraint.",
                        )
                safe_zone = record.get("safe_zone")
                if (
                    not isinstance(safe_zone, dict)
                    or safe_zone.get("state") not in {"known", "unknown"}
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface has no usable safe-zone state",
                        "Preserve known or unknown safe-zone evidence from Aether.",
                    )
                for field in ("verification", "source"):
                    if not isinstance(record.get(field), dict):
                        diagnostic(
                            diagnostics,
                            "IDN1903",
                            f"{pointer}/surfaceId",
                            f"selected surface has no {field} evidence",
                            "Use a complete provenance-linked Aether v1 surface record.",
                        )
                lifecycle = record.get("lifecycle")
                if not isinstance(lifecycle, dict) or lifecycle.get("state") != "stable":
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{pointer}/surfaceId",
                        "selected surface record is not stable",
                        "Select a stable record from the pinned release catalog.",
                    )
            if value.get("sourceAssetId") not in public_assets:
                diagnostic(
                    diagnostics,
                    "IDN1903",
                    f"{pointer}/sourceAssetId",
                    "social surface must select an active approved public usage asset",
                    "Approve and expose the source asset before selecting it.",
                )
            selection_value(
                value.get("copySource"),
                f"{pointer}/copySource",
                {None, "project.displayName", "project.tagline"},
            )
            selection_value(
                value.get("linkSource"),
                f"{pointer}/linkSource",
                {None, "project.repository"},
            )

    project_selection = require_closed(
        document.get("project"),
        SOCIAL_SURFACE_PROJECT_KEYS,
        SOCIAL_SURFACE_PROJECT_KEYS,
        f"{path_value}#/project",
        diagnostics,
    )
    if project_selection is None:
        return

    def reviewed_reference(
        item: Any,
        index: int,
        field: str,
        keys: set[str],
        required: set[str],
        subject_prefix: str,
    ) -> str | None:
        pointer = f"{path_value}#/project/{field}/{index}"
        value = require_closed(item, keys, required, pointer, diagnostics)
        if value is None:
            return None
        identifier = value.get("id")
        if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
            diagnostic(
                diagnostics,
                "IDN1901",
                f"{pointer}/id",
                "project selection ID is invalid",
                "Reference a stable organization-default selection ID.",
            )
            return None
        approval_id = value.get("approval")
        decision = approvals.get(approval_id) if isinstance(approval_id, str) else None
        if (
            decision is None
            or decision.get("status") != "approved"
            or decision.get("subject") != f"{subject_prefix}:{identifier}"
        ):
            diagnostic(
                diagnostics,
                "IDN1901",
                f"{pointer}/approval",
                "project selection does not resolve to a matching approved decision",
                "Record an approved decision for this exact adoption, exclusion, or override.",
            )
        return identifier

    collections: dict[str, set[str]] = {}
    for field, keys, required, prefix in (
        (
            "adopt",
            SOCIAL_SURFACE_ADOPTION_KEYS,
            SOCIAL_SURFACE_ADOPTION_KEYS,
            "social-surface-adoption",
        ),
        (
            "exclude",
            SOCIAL_SURFACE_EXCLUSION_KEYS,
            SOCIAL_SURFACE_EXCLUSION_KEYS,
            "social-surface-exclusion",
        ),
        (
            "overrides",
            SOCIAL_SURFACE_OVERRIDE_KEYS,
            {"id", "reason", "approval"},
            "social-surface-override",
        ),
    ):
        records = project_selection.get(field)
        if not isinstance(records, list):
            diagnostic(
                diagnostics,
                "IDN1901",
                f"{path_value}#/project/{field}",
                f"project {field} must be an array",
                "Use an empty array or declare explicit reviewed selections.",
            )
            collections[field] = set()
            continue
        seen: set[str] = set()
        for index, item in enumerate(records):
            identifier = reviewed_reference(item, index, field, keys, required, prefix)
            if identifier is None:
                continue
            if identifier in seen:
                diagnostic(
                    diagnostics,
                    "IDN1901",
                    f"{path_value}#/project/{field}/{index}/id",
                    f"project {field} selection is duplicated",
                    "Reference each organization default once per operation.",
                )
            seen.add(identifier)
            if identifier not in default_ids:
                diagnostic(
                    diagnostics,
                    "IDN1901",
                    f"{path_value}#/project/{field}/{index}/id",
                    "project selection references an unknown organization default",
                    "Reference a declared organizationDefaults ID.",
                )
            if field in {"exclude", "overrides"} and isinstance(item, dict):
                if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                    diagnostic(
                        diagnostics,
                        "IDN1901",
                        f"{path_value}#/project/{field}/{index}/reason",
                        "product exclusions and overrides require a reviewed reason",
                        "Explain the bounded product-specific difference.",
                    )
            if field == "overrides" and isinstance(item, dict):
                changed = {"sourceAssetId", "copySource", "linkSource"}.intersection(item)
                if not changed:
                    diagnostic(
                        diagnostics,
                        "IDN1901",
                        f"{path_value}#/project/overrides/{index}",
                        "override changes no selection field",
                        "Change an asset, copy source, or link source, or remove the override.",
                    )
                if "sourceAssetId" in item and item.get("sourceAssetId") not in public_assets:
                    diagnostic(
                        diagnostics,
                        "IDN1903",
                        f"{path_value}#/project/overrides/{index}/sourceAssetId",
                        "override asset is not an active approved public usage asset",
                        "Select a reviewed public asset.",
                    )
                if "copySource" in item:
                    selection_value(
                        item.get("copySource"),
                        f"{path_value}#/project/overrides/{index}/copySource",
                        {None, "project.displayName", "project.tagline"},
                    )
                if "linkSource" in item:
                    selection_value(
                        item.get("linkSource"),
                        f"{path_value}#/project/overrides/{index}/linkSource",
                        {None, "project.repository"},
                    )
        collections[field] = seen

    adopted = collections.get("adopt", set())
    for field in ("exclude", "overrides"):
        unknown = sorted(collections.get(field, set()) - adopted)
        if unknown:
            diagnostic(
                diagnostics,
                "IDN1901",
                f"{path_value}#/project/{field}",
                f"project {field} must reference explicitly adopted defaults: {', '.join(unknown)}",
                "Adopt the selection explicitly before excluding or overriding it.",
            )

    contradictory = sorted(
        collections.get("exclude", set()).intersection(collections.get("overrides", set()))
    )
    if contradictory:
        diagnostic(
            diagnostics,
            "IDN1901",
            f"{path_value}#/project",
            f"project cannot both exclude and override: {', '.join(contradictory)}",
            "Keep either the reviewed exclusion or the reviewed override for each selection.",
        )

    active = adopted - collections.get("exclude", set())
    if not active:
        diagnostic(
            diagnostics,
            "IDN1901",
            f"{path_value}#/project/adopt",
            "social-surface projection selects no active surfaces",
            "Explicitly adopt at least one reviewed organization default.",
        )
