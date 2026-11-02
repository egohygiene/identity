# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal handbook validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
from .common import (
    DESIGN_REFERENCES_SCHEMA,
    DESIGN_REFERENCE_KEYS,
    DESIGN_REFERENCE_ROOT_KEYS,
    DESIGN_SYSTEM_CAPABILITY_KEYS,
    DESIGN_SYSTEM_PRINCIPLE_KEYS,
    DESIGN_SYSTEM_ROOT_KEYS,
    DESIGN_SYSTEM_SCHEMA,
    DESIGN_SYSTEM_SECTION_KEYS,
    Diagnostic,
    HTTPS_URL,
    IDENTIFIER,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance, validate_guidance_strings, validate_guidance_text_fields


def validate_design_system(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate reviewed handbook principles and explicit capability boundaries."""

    documents = project.get("documents")
    handbook = documents.get("handbook") if isinstance(documents, dict) else None
    if not isinstance(handbook, dict):
        return
    path_value = handbook.get("designSystem")
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/handbook/designSystem",
        diagnostics,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(document, DESIGN_SYSTEM_ROOT_KEYS, DESIGN_SYSTEM_ROOT_KEYS, "/", diagnostics)
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/design-system.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1701",
            f"{path_value}#/$schema",
            "design-system source must reference design-system.schema.json",
            "Reference the checked-in Identity v1 design-system source schema.",
        )
    if document.get("schema") != DESIGN_SYSTEM_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1701",
            f"{path_value}#/schema",
            f"design-system source schema must be {DESIGN_SYSTEM_SCHEMA}",
            "Migrate design-system source to the v1 contract.",
        )

    section_ids: set[str] = set()
    principle_ids: set[str] = set()
    sections = document.get("sections")
    if not isinstance(sections, list) or not sections:
        diagnostic(
            diagnostics,
            "IDN1701",
            f"{path_value}#/sections",
            "design-system source requires at least one section",
            "Add approved handbook sections.",
        )
    else:
        for index, section in enumerate(sections):
            pointer = f"{path_value}#/sections/{index}"
            value = require_closed(
                section,
                DESIGN_SYSTEM_SECTION_KEYS,
                DESIGN_SYSTEM_SECTION_KEYS,
                pointer,
                diagnostics,
            )
            if value is None:
                continue
            validate_guidance_text_fields(value, ("id", "title", "summary"), pointer, diagnostics)
            section_id = value.get("id")
            if (
                not isinstance(section_id, str)
                or IDENTIFIER.fullmatch(section_id) is None
                or section_id in section_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1701",
                    f"{pointer}/id",
                    "design-system section id is invalid or duplicated",
                    "Use each stable lowercase section id once.",
                )
            elif isinstance(section_id, str):
                section_ids.add(section_id)
            principles = value.get("principles")
            if not isinstance(principles, list) or not principles:
                diagnostic(
                    diagnostics,
                    "IDN1701",
                    f"{pointer}/principles",
                    "design-system section requires at least one principle",
                    "Add reviewed principles that explain the design intent.",
                )
                continue
            for principle_index, principle in enumerate(principles):
                principle_pointer = f"{pointer}/principles/{principle_index}"
                principle_value = require_closed(
                    principle,
                    DESIGN_SYSTEM_PRINCIPLE_KEYS,
                    DESIGN_SYSTEM_PRINCIPLE_KEYS,
                    principle_pointer,
                    diagnostics,
                )
                if principle_value is None:
                    continue
                validate_guidance_text_fields(
                    principle_value,
                    ("id", "title", "guidance", "rationale"),
                    principle_pointer,
                    diagnostics,
                )
                principle_id = principle_value.get("id")
                if (
                    not isinstance(principle_id, str)
                    or IDENTIFIER.fullmatch(principle_id) is None
                    or principle_id in principle_ids
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1701",
                        f"{principle_pointer}/id",
                        "design-system principle id is invalid or duplicated",
                        "Use each stable lowercase principle id once.",
                    )
                elif isinstance(principle_id, str):
                    principle_ids.add(principle_id)
                validate_guidance_strings(
                    principle_value.get("appliesTo"),
                    f"{principle_pointer}/appliesTo",
                    diagnostics,
                )
                validate_guidance_governance(
                    principle_value.get("governance"),
                    f"{principle_pointer}/governance",
                    approvals,
                    diagnostics,
                )

    capability_ids: set[str] = set()
    capabilities = document.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        diagnostic(
            diagnostics,
            "IDN1701",
            f"{path_value}#/capabilities",
            "design-system source requires explicit capability declarations",
            "Declare supported, unmodelled, and unsupported design-system boundaries.",
        )
        return
    for index, capability in enumerate(capabilities):
        pointer = f"{path_value}#/capabilities/{index}"
        value = require_closed(
            capability,
            DESIGN_SYSTEM_CAPABILITY_KEYS,
            DESIGN_SYSTEM_CAPABILITY_KEYS,
            pointer,
            diagnostics,
        )
        if value is None:
            continue
        validate_guidance_text_fields(value, ("id", "label", "notes"), pointer, diagnostics)
        capability_id = value.get("id")
        if (
            not isinstance(capability_id, str)
            or IDENTIFIER.fullmatch(capability_id) is None
            or capability_id in capability_ids
        ):
            diagnostic(
                diagnostics,
                "IDN1701",
                f"{pointer}/id",
                "design-system capability id is invalid or duplicated",
                "Use each stable lowercase capability id once.",
            )
        elif isinstance(capability_id, str):
            capability_ids.add(capability_id)
        if value.get("status") not in {"declared", "not-declared", "unsupported"}:
            diagnostic(
                diagnostics,
                "IDN1701",
                f"{pointer}/status",
                "design-system capability status is unsupported",
                "Use declared, not-declared, or unsupported.",
            )
        if value.get("owner") not in {"identity", "holon", "consumer"}:
            diagnostic(
                diagnostics,
                "IDN1701",
                f"{pointer}/owner",
                "design-system capability owner is unsupported",
                "Use identity, holon, or consumer.",
            )
        validate_guidance_governance(
            value.get("governance"),
            f"{pointer}/governance",
            approvals,
            diagnostics,
        )


def validate_design_references(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate a reviewable catalog of patterns to study, never assets to copy."""

    documents = project.get("documents")
    handbook = documents.get("handbook") if isinstance(documents, dict) else None
    if not isinstance(handbook, dict):
        return
    path_value = handbook.get("references")
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/handbook/references",
        diagnostics,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(
        document,
        DESIGN_REFERENCE_ROOT_KEYS,
        DESIGN_REFERENCE_ROOT_KEYS,
        "/",
        diagnostics,
    )
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/design-references.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1702",
            f"{path_value}#/$schema",
            "reference catalog must reference design-references.schema.json",
            "Reference the checked-in Identity v1 design-reference schema.",
        )
    if document.get("schema") != DESIGN_REFERENCES_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1702",
            f"{path_value}#/schema",
            f"reference catalog schema must be {DESIGN_REFERENCES_SCHEMA}",
            "Migrate the reference catalog to the v1 contract.",
        )
    reference_ids: set[str] = set()
    references = document.get("references")
    if not isinstance(references, list) or not references:
        diagnostic(
            diagnostics,
            "IDN1702",
            f"{path_value}#/references",
            "reference catalog requires at least one reviewed record",
            "Record the pattern, decision, rights boundary, and review evidence.",
        )
        return
    for index, reference in enumerate(references):
        pointer = f"{path_value}#/references/{index}"
        value = require_closed(
            reference,
            DESIGN_REFERENCE_KEYS,
            DESIGN_REFERENCE_KEYS,
            pointer,
            diagnostics,
        )
        if value is None:
            continue
        validate_guidance_text_fields(value, ("id", "notes", "rights"), pointer, diagnostics)
        reference_id = value.get("id")
        if (
            not isinstance(reference_id, str)
            or IDENTIFIER.fullmatch(reference_id) is None
            or reference_id in reference_ids
        ):
            diagnostic(
                diagnostics,
                "IDN1702",
                f"{pointer}/id",
                "design reference id is invalid or duplicated",
                "Use each stable lowercase reference id once.",
            )
        elif isinstance(reference_id, str):
            reference_ids.add(reference_id)
        if not isinstance(value.get("url"), str) or HTTPS_URL.fullmatch(value["url"]) is None:
            diagnostic(
                diagnostics,
                "IDN1702",
                f"{pointer}/url",
                "design reference URL must use HTTPS",
                "Record the original HTTPS source URL.",
            )
        try:
            datetime.fromisoformat(str(value.get("capturedAt", "")).replace("Z", "+00:00"))
        except ValueError:
            diagnostic(
                diagnostics,
                "IDN1702",
                f"{pointer}/capturedAt",
                "design reference capturedAt must be an RFC 3339 timestamp",
                "Record when the reference was reviewed.",
            )
        validate_guidance_strings(value.get("patterns"), f"{pointer}/patterns", diagnostics)
        if value.get("decision") not in {"adopt", "adapt", "reject", "observe"}:
            diagnostic(
                diagnostics,
                "IDN1702",
                f"{pointer}/decision",
                "design reference decision is unsupported",
                "Use adopt, adapt, reject, or observe.",
            )
        if not isinstance(value.get("affectsCanonical"), bool):
            diagnostic(
                diagnostics,
                "IDN1702",
                f"{pointer}/affectsCanonical",
                "affectsCanonical must be a boolean",
                "State whether the reviewed reference changes Identity decisions.",
            )
        validate_guidance_governance(
            value.get("governance"),
            f"{pointer}/governance",
            approvals,
            diagnostics,
        )
