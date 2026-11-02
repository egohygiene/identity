# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal mascot validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
import re
from typing import Any
from .common import (
    Diagnostic,
    IDENTIFIER,
    MASCOT_ACCESSIBILITY_KEYS,
    MASCOT_ASSET_KEYS,
    MASCOT_CHARACTER_KEYS,
    MASCOT_EMBLEM_KEYS,
    MASCOT_EYE_KEYS,
    MASCOT_LICENSE_KEYS,
    MASCOT_MEANING_KEYS,
    MASCOT_MOTION_KEYS,
    MASCOT_ROOT_KEYS,
    MASCOT_SCHEMA,
    MASCOT_USAGE_KEYS,
    MASCOT_VARIANT_KEYS,
    SHA256,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
    sha256,
)


def validate_mascot(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate an optional reviewed mascot and character-system source."""

    documents = project.get("documents")
    if not isinstance(documents, dict) or documents.get("mascot") is None:
        return
    path_value = documents["mascot"]
    path = resolve_local_path(repository_root, path_value, "/documents/mascot", diagnostics)
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, MASCOT_ROOT_KEYS, MASCOT_ROOT_KEYS, str(path_value), diagnostics)
    if document.get("schema") != MASCOT_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/schema",
            f"mascot schema must be {MASCOT_SCHEMA}",
            "Migrate the mascot source explicitly before using it.",
        )
    schema_reference = document.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference.endswith(
        "/mascot.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/$schema",
            "mascot schema reference must end in /mascot.schema.json",
            "Reference the checked-in Identity v1 mascot schema.",
        )

    def text_field(value: dict[str, Any], field: str, pointer: str) -> None:
        if not isinstance(value.get(field), str) or not value[field].strip():
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{pointer}/{field}",
                "mascot text must be a non-empty string",
                "Provide reviewed character guidance.",
            )

    def string_list(value: Any, pointer: str) -> list[str]:
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or not item.strip() for item in value)
            or len(value) != len(set(value))
        ):
            diagnostic(
                diagnostics,
                "IDN2001",
                pointer,
                "mascot list must contain unique non-empty strings",
                "Provide at least one reviewed value without duplicates.",
            )
            return []
        return value

    mascot_id = document.get("id")
    if not isinstance(mascot_id, str) or IDENTIFIER.fullmatch(mascot_id) is None:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/id",
            "mascot id must be a stable lowercase identifier",
            "Use lowercase letters, digits, and hyphens.",
        )
    for field in ("name", "pronouns", "role"):
        text_field(document, field, str(path_value))
    if document.get("status") not in {"candidate", "approved", "rejected", "retired"}:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/status",
            "mascot lifecycle status is unsupported",
            "Use candidate, approved, rejected, or retired.",
        )

    character = require_closed(
        document.get("character"),
        MASCOT_CHARACTER_KEYS,
        MASCOT_CHARACTER_KEYS,
        f"{path_value}#/character",
        diagnostics,
    )
    if character is not None:
        for field in ("archetype", "silhouette", "face", "outfit"):
            text_field(character, field, f"{path_value}#/character")
        traits = string_list(character.get("traits"), f"{path_value}#/character/traits")
        if traits and len(traits) < 3:
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{path_value}#/character/traits",
                "mascot requires at least three reviewed traits",
                "Describe enough traits to guide consistent derivatives.",
            )
        string_list(
            character.get("prohibitedElements"),
            f"{path_value}#/character/prohibitedElements",
        )
        eyes = require_closed(
            character.get("eyes"),
            MASCOT_EYE_KEYS,
            MASCOT_EYE_KEYS,
            f"{path_value}#/character/eyes",
            diagnostics,
        )
        if eyes is not None:
            if not isinstance(eyes.get("count"), int) or not 1 <= eyes["count"] <= 8:
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{path_value}#/character/eyes/count",
                    "eye count must be an integer from 1 through 8",
                    "Record the exact reviewed eye count.",
                )
            text_field(eyes, "treatment", f"{path_value}#/character/eyes")
        emblem = require_closed(
            character.get("emblem"),
            MASCOT_EMBLEM_KEYS,
            MASCOT_EMBLEM_KEYS,
            f"{path_value}#/character/emblem",
            diagnostics,
        )
        if emblem is not None:
            text_field(emblem, "placement", f"{path_value}#/character/emblem")
            if emblem.get("integrated") is not True:
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{path_value}#/character/emblem/integrated",
                    "mascot emblem must be integrated into the character design",
                    "Use a reviewed garment or body placement instead of a detached prop.",
                )

    meanings = document.get("meanings")
    meaning_ids: set[str] = set()
    if not isinstance(meanings, list) or not meanings:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/meanings",
            "mascot meanings must be a non-empty array",
            "Explain the reviewed meaning of at least one visual element.",
        )
    else:
        for index, item in enumerate(meanings):
            pointer = f"{path_value}#/meanings/{index}"
            meaning = require_closed(
                item,
                MASCOT_MEANING_KEYS,
                MASCOT_MEANING_KEYS,
                pointer,
                diagnostics,
            )
            if meaning is None:
                continue
            meaning_id = meaning.get("id")
            if (
                not isinstance(meaning_id, str)
                or IDENTIFIER.fullmatch(meaning_id) is None
                or meaning_id in meaning_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{pointer}/id",
                    "meaning id must be a unique stable identifier",
                    "Use a unique lowercase identifier.",
                )
            else:
                meaning_ids.add(meaning_id)
            for field in ("element", "meaning"):
                text_field(meaning, field, pointer)

    canonical = require_closed(
        document.get("canonicalAsset"),
        MASCOT_ASSET_KEYS,
        MASCOT_ASSET_KEYS,
        f"{path_value}#/canonicalAsset",
        diagnostics,
    )
    if canonical is not None:
        for field in ("assetId",):
            if (
                not isinstance(canonical.get(field), str)
                or IDENTIFIER.fullmatch(canonical[field]) is None
            ):
                diagnostic(
                    diagnostics,
                    "IDN2003",
                    f"{path_value}#/canonicalAsset/{field}",
                    "canonical asset id is invalid",
                    "Reference one stable provenance asset id.",
                )
        asset_path = resolve_local_path(
            repository_root,
            canonical.get("path"),
            f"{path_value}#/canonicalAsset/path",
            diagnostics,
        )
        digest = canonical.get("sha256")
        if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/canonicalAsset/sha256",
                "canonical asset digest must be lowercase SHA-256",
                "Record the reviewed local asset digest.",
            )
        elif asset_path is not None and sha256(asset_path) != digest:
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/canonicalAsset/sha256",
                "canonical mascot digest does not match local bytes",
                "Review the changed bytes and update the digest intentionally.",
            )
        if canonical.get("mediaType") not in {"image/png", "image/svg+xml"}:
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/canonicalAsset/mediaType",
                "canonical mascot media type is unsupported",
                "Use image/png or image/svg+xml.",
            )

        provenance_path_value = documents.get("provenance")
        provenance_path = resolve_local_path(
            repository_root,
            provenance_path_value,
            "/documents/provenance",
            diagnostics,
        )
        provenance_document = (
            load_json(provenance_path, str(provenance_path_value), diagnostics)
            if provenance_path is not None
            else None
        )
        assets = provenance_document.get("assets") if provenance_document is not None else None
        matching_assets = [
            item
            for item in assets if isinstance(item, dict) and item.get("id") == canonical.get("assetId")
        ] if isinstance(assets, list) else []
        if len(matching_assets) != 1:
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/canonicalAsset/assetId",
                "canonical mascot must resolve to exactly one provenance record",
                "Add one matching governed asset record.",
            )
        elif (
            matching_assets[0].get("path") != canonical.get("path")
            or matching_assets[0].get("sha256") != canonical.get("sha256")
        ):
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/canonicalAsset",
                "mascot source and provenance bytes disagree",
                "Use the same reviewed path and digest in both contracts.",
            )

    variants = document.get("variants")
    variant_ids: set[str] = set()
    if not isinstance(variants, list) or not variants:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/variants",
            "mascot variants must be a non-empty array",
            "Declare at least one reviewed projection role.",
        )
    else:
        for index, item in enumerate(variants):
            pointer = f"{path_value}#/variants/{index}"
            variant = require_closed(
                item,
                MASCOT_VARIANT_KEYS,
                MASCOT_VARIANT_KEYS,
                pointer,
                diagnostics,
            )
            if variant is None:
                continue
            variant_id = variant.get("id")
            if (
                not isinstance(variant_id, str)
                or IDENTIFIER.fullmatch(variant_id) is None
                or variant_id in variant_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{pointer}/id",
                    "variant id must be a unique stable identifier",
                    "Use a unique lowercase variant id.",
                )
            else:
                variant_ids.add(variant_id)
            for field in ("role", "crop", "altText"):
                text_field(variant, field, pointer)
            aspect_ratio = variant.get("aspectRatio")
            if not isinstance(aspect_ratio, str) or re.fullmatch(r"[1-9][0-9]*:[1-9][0-9]*", aspect_ratio) is None:
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{pointer}/aspectRatio",
                    "variant aspect ratio must use positive width:height integers",
                    "Record the reviewed crop ratio, for example 1:1.",
                )
            if not isinstance(variant.get("minimumWidth"), int) or variant["minimumWidth"] < 1:
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{pointer}/minimumWidth",
                    "variant minimum width must be a positive integer",
                    "Record the smallest reviewed CSS-pixel width.",
                )

    accessibility = require_closed(
        document.get("accessibility"),
        MASCOT_ACCESSIBILITY_KEYS,
        MASCOT_ACCESSIBILITY_KEYS,
        f"{path_value}#/accessibility",
        diagnostics,
    )
    if accessibility is not None:
        text_field(accessibility, "altText", f"{path_value}#/accessibility")
        if accessibility.get("decorativeAlt") != "" or accessibility.get("neverSoleCarrier") is not True:
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{path_value}#/accessibility",
                "mascot accessibility must define empty decorative alt and forbid sole-carrier use",
                "Keep informative text outside the mascot and use empty alt when decorative.",
            )

    usage = require_closed(
        document.get("usage"),
        MASCOT_USAGE_KEYS,
        MASCOT_USAGE_KEYS,
        f"{path_value}#/usage",
        diagnostics,
    )
    if usage is not None:
        for field in ("safeZone", "backgrounds"):
            text_field(usage, field, f"{path_value}#/usage")
        for field in ("do", "dont"):
            string_list(usage.get(field), f"{path_value}#/usage/{field}")

    motion = require_closed(
        document.get("motion"),
        MASCOT_MOTION_KEYS,
        MASCOT_MOTION_KEYS,
        f"{path_value}#/motion",
        diagnostics,
    )
    if motion is not None:
        if motion.get("status") not in {"not-declared", "optional", "declared"}:
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{path_value}#/motion/status",
                "mascot motion status is unsupported",
                "Use not-declared, optional, or declared.",
            )
        for field in ("default", "reducedMotion"):
            text_field(motion, field, f"{path_value}#/motion")
        string_list(motion.get("restrictions"), f"{path_value}#/motion/restrictions")

    license_value = require_closed(
        document.get("license"),
        MASCOT_LICENSE_KEYS,
        MASCOT_LICENSE_KEYS,
        f"{path_value}#/license",
        diagnostics,
    )
    if license_value is not None:
        for field in ("spdx", "attribution", "trademark"):
            text_field(license_value, field, f"{path_value}#/license")
        if str(license_value.get("spdx", "")).upper() in {"NONE", "NOASSERTION", "UNKNOWN"}:
            diagnostic(
                diagnostics,
                "IDN2003",
                f"{path_value}#/license/spdx",
                "mascot license must use a reviewed SPDX expression",
                "Record the approved artwork license.",
            )

    approval_id = document.get("approval")
    decision = approvals.get(approval_id) if isinstance(approval_id, str) else None
    if (
        decision is None
        or decision.get("status") != "approved"
        or decision.get("subject") != f"mascot:{mascot_id}"
    ):
        diagnostic(
            diagnostics,
            "IDN2002",
            f"{path_value}#/approval",
            "mascot does not resolve to an approved decision for the same character",
            "Link an approved human decision whose subject is mascot:<id>.",
        )
