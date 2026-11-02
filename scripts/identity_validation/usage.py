# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal usage validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import (
    Diagnostic,
    GUIDANCE_CATEGORIES,
    IDENTIFIER,
    USAGE_ACCESSIBILITY_KEYS,
    USAGE_ASSET_KEYS,
    USAGE_LEGAL_KEYS,
    USAGE_LICENSE_KEYS,
    USAGE_ROOT_KEYS,
    USAGE_RULE_KEYS,
    USAGE_SCHEMA,
    USAGE_SECTION_KEYS,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance, validate_guidance_strings, validate_guidance_text_fields


def validate_usage_rule(
    value: Any,
    pointer: str,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> str | None:
    """Validate one renderer-ready do/don't usage rule."""

    rule = require_closed(
        value,
        USAGE_RULE_KEYS,
        USAGE_RULE_KEYS,
        pointer,
        diagnostics,
    )
    if rule is None:
        return None
    validate_guidance_text_fields(
        rule,
        ("id", "instruction", "rationale"),
        pointer,
        diagnostics,
    )
    identifier = rule.get("id")
    if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{pointer}/id",
            "usage rule id is invalid",
            "Use a stable lowercase identifier.",
        )
        identifier = None
    if rule.get("kind") not in {"do", "dont"}:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{pointer}/kind",
            "usage rule kind is unsupported",
            "Use do or dont.",
        )
    if rule.get("category") not in GUIDANCE_CATEGORIES:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{pointer}/category",
            "usage rule category is unsupported",
            "Use a category declared by the v1 usage schema.",
        )
    validate_guidance_strings(rule.get("details"), f"{pointer}/details", diagnostics)
    validate_guidance_strings(rule.get("contexts"), f"{pointer}/contexts", diagnostics)
    validate_guidance_governance(
        rule.get("governance"),
        f"{pointer}/governance",
        approvals,
        diagnostics,
    )
    return identifier


def validate_usage(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate usage rules, legacy policy, accessibility, and legal notes."""

    documents = project.get("documents")
    guidance = documents.get("guidance") if isinstance(documents, dict) else None
    if not isinstance(guidance, dict):
        return
    path_value = guidance.get("usage")
    if path_value is None:
        return
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/guidance/usage",
        diagnostics,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, USAGE_ROOT_KEYS, USAGE_ROOT_KEYS, "/", diagnostics)
    schema_reference = document.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference.endswith(
        "/usage.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/$schema",
            "usage schema reference must end in /usage.schema.json",
            "Reference the checked-in Identity v1 usage schema.",
        )
    if document.get("schema") != USAGE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/schema",
            f"usage schema must be {USAGE_SCHEMA}",
            "Migrate usage guidance to the v1 contract.",
        )

    section_ids: set[str] = set()
    rule_ids: set[str] = set()
    sections = document.get("sections")
    if not isinstance(sections, list) or not sections:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/sections",
            "usage guidance requires at least one section",
            "Add reviewed do/don't rules grouped for human readers.",
        )
    else:
        for index, item in enumerate(sections):
            pointer = f"{path_value}#/sections/{index}"
            section = require_closed(
                item,
                USAGE_SECTION_KEYS,
                USAGE_SECTION_KEYS,
                pointer,
                diagnostics,
            )
            if section is None:
                continue
            validate_guidance_text_fields(
                section,
                ("id", "title", "description"),
                pointer,
                diagnostics,
            )
            identifier = section.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in section_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1601",
                    f"{pointer}/id",
                    "usage section id is invalid or duplicated",
                    "Use each stable lowercase section identifier once.",
                )
            else:
                section_ids.add(identifier)
            rules = section.get("rules")
            if not isinstance(rules, list) or not rules:
                diagnostic(
                    diagnostics,
                    "IDN1601",
                    f"{pointer}/rules",
                    "usage section requires at least one rule",
                    "Add one or more reviewed do/don't rules.",
                )
                continue
            for rule_index, rule in enumerate(rules):
                rule_id = validate_usage_rule(
                    rule,
                    f"{pointer}/rules/{rule_index}",
                    approvals,
                    diagnostics,
                )
                if rule_id in rule_ids:
                    diagnostic(
                        diagnostics,
                        "IDN1601",
                        f"{pointer}/rules/{rule_index}/id",
                        "usage rule id is duplicated",
                        "Use one stable ID per usage rule.",
                    )
                elif rule_id is not None:
                    rule_ids.add(rule_id)

    asset_ids: set[str] = set()
    legacy_replacements: list[tuple[str, str]] = []
    assets = document.get("assets")
    if not isinstance(assets, list) or not assets:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/assets",
            "usage guidance requires at least one governed asset",
            "Expose current downloads and any permitted legacy records.",
        )
    else:
        for index, item in enumerate(assets):
            pointer = f"{path_value}#/assets/{index}"
            asset = require_closed(
                item,
                USAGE_ASSET_KEYS,
                USAGE_ASSET_KEYS,
                pointer,
                diagnostics,
            )
            if asset is None:
                continue
            validate_guidance_text_fields(
                asset,
                ("id", "label", "kind", "path", "status", "availability", "notes"),
                pointer,
                diagnostics,
            )
            identifier = asset.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in asset_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1601",
                    f"{pointer}/id",
                    "usage asset id is invalid or duplicated",
                    "Use each stable lowercase asset identifier once.",
                )
            else:
                asset_ids.add(identifier)
            resolve_local_path(
                repository_root,
                asset.get("path"),
                f"{pointer}/path",
                diagnostics,
            )
            status = asset.get("status")
            availability = asset.get("availability")
            replacement = asset.get("replacement")
            download_name = asset.get("downloadName")
            governance = validate_guidance_governance(
                asset.get("governance"),
                f"{pointer}/governance",
                approvals,
                diagnostics,
            )
            if status == "legacy":
                if (
                    not isinstance(replacement, str)
                    or IDENTIFIER.fullmatch(replacement) is None
                    or replacement == identifier
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1603",
                        pointer,
                        "legacy asset policy is incomplete or unsafe",
                        "Name a different active replacement through reviewed policy.",
                    )
                else:
                    legacy_replacements.append((pointer, replacement))
                if availability == "public":
                    if (
                        not isinstance(download_name, str)
                        or not download_name.strip()
                        or governance is None
                        or governance.get("state") != "approved"
                        or governance.get("visibility") != "public"
                    ):
                        diagnostic(
                            diagnostics,
                            "IDN1603",
                            pointer,
                            "public legacy asset lacks an explicit approved policy",
                            (
                                "Approve public visibility and a stable download name, "
                                "or keep it internal."
                            ),
                        )
                elif download_name is not None:
                    diagnostic(
                        diagnostics,
                        "IDN1603",
                        f"{pointer}/downloadName",
                        "non-public legacy asset cannot expose a download name",
                        "Use null until a new decision permits public download.",
                    )
            elif status == "active":
                if replacement is not None:
                    diagnostic(
                        diagnostics,
                        "IDN1603",
                        f"{pointer}/replacement",
                        "active asset cannot declare a replacement",
                        "Use null until the asset enters a reviewed legacy state.",
                    )
                if availability == "public" and (
                    not isinstance(download_name, str) or not download_name.strip()
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1603",
                        f"{pointer}/downloadName",
                        "public active asset requires a download name",
                        "Provide a stable downloadable filename.",
                    )
            else:
                diagnostic(
                    diagnostics,
                    "IDN1603",
                    f"{pointer}/status",
                    "usage asset status is unsupported",
                    "Use active or legacy.",
                )
            if availability not in {"public", "internal", "blocked"}:
                diagnostic(
                    diagnostics,
                    "IDN1603",
                    f"{pointer}/availability",
                    "asset availability is unsupported",
                    "Use public, internal, or blocked.",
                )
        for pointer, replacement in legacy_replacements:
            if replacement not in asset_ids:
                diagnostic(
                    diagnostics,
                    "IDN1603",
                    f"{pointer}/replacement",
                    "legacy replacement does not name a declared usage asset",
                    "Reference an active governed asset ID.",
                )

    for field, keys, text_fields in (
        (
            "accessibility",
            USAGE_ACCESSIBILITY_KEYS,
            ("summary",),
        ),
        (
            "legal",
            USAGE_LEGAL_KEYS,
            ("trademark", "copyright", "attribution"),
        ),
    ):
        pointer = f"{path_value}#/{field}"
        value = require_closed(
            document.get(field),
            keys,
            keys,
            pointer,
            diagnostics,
        )
        if value is None:
            continue
        validate_guidance_text_fields(value, text_fields, pointer, diagnostics)
        validate_guidance_governance(
            value.get("governance"),
            f"{pointer}/governance",
            approvals,
            diagnostics,
        )
        if field == "accessibility":
            validate_guidance_strings(value.get("rules"), f"{pointer}/rules", diagnostics)
            continue
        licenses = value.get("thirdPartyLicenses")
        if not isinstance(licenses, list):
            diagnostic(
                diagnostics,
                "IDN1601",
                f"{pointer}/thirdPartyLicenses",
                "third-party licenses must be an array",
                "Use an empty list or add reviewed license notes.",
            )
            continue
        for index, item in enumerate(licenses):
            license_pointer = f"{pointer}/thirdPartyLicenses/{index}"
            license_value = require_closed(
                item,
                USAGE_LICENSE_KEYS,
                USAGE_LICENSE_KEYS,
                license_pointer,
                diagnostics,
            )
            if license_value is not None:
                validate_guidance_text_fields(
                    license_value,
                    ("name", "spdx", "attribution"),
                    license_pointer,
                    diagnostics,
                )
