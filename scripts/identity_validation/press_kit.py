# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal press kit validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Sequence
from .common import (
    Diagnostic,
    HTTPS_URL,
    IDENTIFIER,
    PRESS_KIT_ASSET_KEYS,
    PRESS_KIT_BOILERPLATE_KEYS,
    PRESS_KIT_CONTACT_KEYS,
    PRESS_KIT_FACT_KEYS,
    PRESS_KIT_LINK_KEYS,
    PRESS_KIT_ROOT_KEYS,
    PRESS_KIT_SOURCE_SCHEMA,
    PRESS_KIT_TEAM_MEMBER_KEYS,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance, validate_guidance_text_fields


def validate_press_kit(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate optional Press Kit source without manufacturing public facts."""

    documents = project.get("documents")
    if not isinstance(documents, dict) or documents.get("pressKit") is None:
        return
    path_value = documents["pressKit"]
    path = resolve_local_path(repository_root, path_value, "/documents/pressKit", diagnostics)
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, PRESS_KIT_ROOT_KEYS, PRESS_KIT_ROOT_KEYS, "/", diagnostics)
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/press-kit.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1801",
            f"{path_value}#/$schema",
            "Press Kit source must reference press-kit.schema.json",
            "Reference the checked-in Identity v1 Press Kit source schema.",
        )
    if document.get("schema") != PRESS_KIT_SOURCE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1801",
            f"{path_value}#/schema",
            f"Press Kit source schema must be {PRESS_KIT_SOURCE_SCHEMA}",
            "Migrate Press Kit source to the Identity v1 contract.",
        )

    def governed_collection(
        field: str,
        keys: set[str],
        text_fields: Sequence[str],
        *,
        minimum: int = 0,
    ) -> list[dict[str, Any]]:
        records = document.get(field)
        pointer = f"{path_value}#/{field}"
        if not isinstance(records, list) or len(records) < minimum:
            diagnostic(
                diagnostics,
                "IDN1801",
                pointer,
                f"Press Kit {field} must be an array with at least {minimum} record(s)",
                "Add the required reviewed records or use an empty array for an explicitly absent optional section.",
            )
            return []
        result: list[dict[str, Any]] = []
        identifiers: set[str] = set()
        for index, item in enumerate(records):
            item_pointer = f"{pointer}/{index}"
            value = require_closed(item, keys, keys, item_pointer, diagnostics)
            if value is None:
                continue
            validate_guidance_text_fields(value, text_fields, item_pointer, diagnostics)
            identifier = value.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in identifiers
            ):
                diagnostic(
                    diagnostics,
                    "IDN1801",
                    f"{item_pointer}/id",
                    f"Press Kit {field} id is invalid or duplicated",
                    "Use each stable lowercase identifier once.",
                )
            elif isinstance(identifier, str):
                identifiers.add(identifier)
            validate_guidance_governance(
                value.get("governance"),
                f"{item_pointer}/governance",
                approvals,
                diagnostics,
            )
            result.append(value)
        return result

    boilerplates = governed_collection(
        "boilerplates",
        PRESS_KIT_BOILERPLATE_KEYS,
        ("id", "text"),
        minimum=2,
    )
    kinds: set[str] = set()
    for index, item in enumerate(boilerplates):
        kind = item.get("kind")
        pointer = f"{path_value}#/boilerplates/{index}/kind"
        if kind not in {"short", "paragraph", "long"} or kind in kinds:
            diagnostic(
                diagnostics,
                "IDN1801",
                pointer,
                "Press Kit boilerplate kind must be one unique short, paragraph, or long value",
                "Declare one short and one long boilerplate, with at most one optional paragraph.",
            )
        elif isinstance(kind, str):
            kinds.add(kind)
    if not {"short", "long"}.issubset(kinds):
        diagnostic(
            diagnostics,
            "IDN1801",
            f"{path_value}#/boilerplates",
            "Press Kit source requires one short and one long boilerplate",
            "Add approved public short and long descriptions, each with its own governance record.",
        )

    governed_collection("facts", PRESS_KIT_FACT_KEYS, ("id", "label", "value"))
    links = governed_collection("links", PRESS_KIT_LINK_KEYS, ("id", "label", "url", "kind"))
    for index, link in enumerate(links):
        pointer = f"{path_value}#/links/{index}"
        if not isinstance(link.get("url"), str) or HTTPS_URL.fullmatch(link["url"]) is None:
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/url",
                "Press Kit links must use HTTPS URLs",
                "Record the canonical HTTPS destination.",
            )
        if link.get("kind") not in {
            "website",
            "product",
            "repository",
            "documentation",
            "support",
            "social",
            "other",
        }:
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/kind",
                "Press Kit link kind is unsupported",
                "Use website, product, repository, documentation, support, social, or other.",
            )
        if (
            isinstance(project.get("documents"), dict)
            and project["documents"].get("channelRegistry") is not None
            and link.get("kind") == "social"
        ):
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/kind",
                "Press Kit social links must derive from the channel registry",
                "Remove the duplicated social link and govern it through documents.channelRegistry.",
            )

    contacts = governed_collection(
        "contacts", PRESS_KIT_CONTACT_KEYS, ("id", "label", "kind", "value")
    )
    for index, contact in enumerate(contacts):
        pointer = f"{path_value}#/contacts/{index}"
        kind = contact.get("kind")
        value = contact.get("value")
        if kind not in {"email", "url", "other"}:
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/kind",
                "Press Kit contact kind is unsupported",
                "Use email, url, or other.",
            )
        if kind == "email" and (not isinstance(value, str) or "@" not in value):
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/value",
                "email contact must contain an email address",
                "Record a reviewed public email address or choose a different contact kind.",
            )
        if kind == "url" and (
            not isinstance(value, str) or HTTPS_URL.fullmatch(value) is None
        ):
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/value",
                "URL contact must use an HTTPS URL",
                "Record a reviewed HTTPS contact URL.",
            )
        if not isinstance(contact.get("notes"), str):
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{pointer}/notes",
                "Press Kit contact notes must be a string",
                "Use an empty string or add reviewed contact instructions.",
            )

    team = governed_collection("team", PRESS_KIT_TEAM_MEMBER_KEYS, ("id", "name", "role"))
    for index, member in enumerate(team):
        bio = member.get("bio")
        if bio is not None and (not isinstance(bio, str) or not bio.strip()):
            diagnostic(
                diagnostics,
                "IDN1801",
                f"{path_value}#/team/{index}/bio",
                "Press Kit team bio must be a non-empty string when supplied",
                "Omit the optional bio or provide explicitly reviewed public copy.",
            )

    assets = governed_collection("assets", PRESS_KIT_ASSET_KEYS, ("id", "assetId", "label", "notes"))
    guidance = project.get("documents", {}).get("guidance", {})
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
    selected_asset_ids: set[str] = set()
    for index, asset in enumerate(assets):
        pointer = f"{path_value}#/assets/{index}/assetId"
        asset_id = asset.get("assetId")
        if (
            not isinstance(asset_id, str)
            or IDENTIFIER.fullmatch(asset_id) is None
            or asset_id in selected_asset_ids
        ):
            diagnostic(
                diagnostics,
                "IDN1801",
                pointer,
                "Press Kit assetId is invalid or selected more than once",
                "Select each approved public usage asset by its stable id at most once.",
            )
        elif asset_id not in public_assets:
            diagnostic(
                diagnostics,
                "IDN1801",
                pointer,
                "Press Kit assets must select an active, approved public usage asset",
                "Approve and expose the source asset through usage guidance before including it in a Press Kit.",
            )
        else:
            selected_asset_ids.add(asset_id)
