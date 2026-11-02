# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal channels validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
from .common import (
    CHANNEL_ACCESSIBILITY_KEYS,
    CHANNEL_BADGE_KEYS,
    CHANNEL_ICON_KEYS,
    CHANNEL_KEYS,
    CHANNEL_LIFECYCLE_KEYS,
    CHANNEL_PLATFORM_KEYS,
    CHANNEL_REGISTRY_METADATA_KEYS,
    CHANNEL_REGISTRY_ROOT_KEYS,
    CHANNEL_REGISTRY_SECURITY_KEYS,
    CHANNEL_REGISTRY_SOURCE_SCHEMA,
    CHANNEL_VERIFICATION_KEYS,
    Diagnostic,
    HTTPS_URL,
    IDENTIFIER,
    SEMVER,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance


def validate_channel_registry(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate the optional public organization channel registry."""

    documents = project.get("documents")
    if not isinstance(documents, dict) or documents.get("channelRegistry") is None:
        return
    path_value = documents["channelRegistry"]
    path = resolve_local_path(
        repository_root, path_value, "/documents/channelRegistry", diagnostics
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(
        document,
        CHANNEL_REGISTRY_ROOT_KEYS,
        CHANNEL_REGISTRY_ROOT_KEYS,
        "/",
        diagnostics,
    )
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/channel-registry.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN2101",
            f"{path_value}#/$schema",
            "channel registry must reference channel-registry.schema.json",
            "Reference the checked-in Identity v1 channel registry schema.",
        )
    if document.get("schema") != CHANNEL_REGISTRY_SOURCE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN2101",
            f"{path_value}#/schema",
            f"channel registry schema must be {CHANNEL_REGISTRY_SOURCE_SCHEMA}",
            "Migrate the registry through an explicit versioned change.",
        )

    registry = require_closed(
        document.get("registry"),
        CHANNEL_REGISTRY_METADATA_KEYS,
        CHANNEL_REGISTRY_METADATA_KEYS,
        f"{path_value}#/registry",
        diagnostics,
    )
    if registry is not None:
        registry_id = registry.get("id")
        if not isinstance(registry_id, str) or IDENTIFIER.fullmatch(registry_id) is None:
            diagnostic(diagnostics, "IDN2101", f"{path_value}#/registry/id", "channel registry id is invalid", "Use a stable lowercase registry id.")
        version = registry.get("version")
        if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
            diagnostic(diagnostics, "IDN2101", f"{path_value}#/registry/version", "channel registry version must be semantic versioning", "Publish registry changes with an explicit x.y.z version.")
        if not isinstance(registry.get("owner"), str) or not registry["owner"].strip():
            diagnostic(diagnostics, "IDN2101", f"{path_value}#/registry/owner", "channel registry owner is empty", "Record the responsible organization.")
        try:
            datetime.fromisoformat(str(registry.get("reviewedAt", "")).replace("Z", "+00:00"))
        except ValueError:
            diagnostic(diagnostics, "IDN2101", f"{path_value}#/registry/reviewedAt", "channel registry reviewedAt must be RFC 3339", "Record when the registry was reviewed.")

    security = require_closed(
        document.get("security"),
        CHANNEL_REGISTRY_SECURITY_KEYS,
        CHANNEL_REGISTRY_SECURITY_KEYS,
        f"{path_value}#/security",
        diagnostics,
    )
    if security is not None and (
        security.get("secretsStored") is not False
        or security.get("ownerReferenceKind") != "role"
        or not isinstance(security.get("procedureLocation"), str)
        or not security["procedureLocation"].strip()
    ):
        diagnostic(
            diagnostics,
            "IDN2103",
            f"{path_value}#/security",
            "public channel registry must deny secrets and reference recovery owners by role",
            "Keep credentials and recovery material in a private runbook.",
        )

    channels = document.get("channels")
    if not isinstance(channels, list):
        diagnostic(diagnostics, "IDN2101", f"{path_value}#/channels", "channel registry channels must be an array", "Use an empty array when no candidates are recorded.")
        return
    identifiers: set[str] = set()
    urls: set[str] = set()
    lifecycle_states = {"planned", "reserved", "active", "unavailable", "deprecated", "impersonation-risk"}
    verification_states = {"unverified", "pending", "verified", "not-applicable"}
    for index, item in enumerate(channels):
        pointer = f"{path_value}#/channels/{index}"
        value = require_closed(item, CHANNEL_KEYS, CHANNEL_KEYS, pointer, diagnostics)
        if value is None:
            continue
        identifier = value.get("id")
        if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None or identifier in identifiers:
            diagnostic(diagnostics, "IDN2101", f"{pointer}/id", "channel id is invalid or duplicated", "Use each stable lowercase channel id once.")
        elif isinstance(identifier, str):
            identifiers.add(identifier)
        platform = require_closed(value.get("platform"), CHANNEL_PLATFORM_KEYS, CHANNEL_PLATFORM_KEYS, f"{pointer}/platform", diagnostics)
        if platform is not None:
            platform_id = platform.get("id")
            if not isinstance(platform_id, str) or IDENTIFIER.fullmatch(platform_id) is None:
                diagnostic(diagnostics, "IDN2101", f"{pointer}/platform/id", "platform id is invalid", "Use a stable lowercase platform id.")
            if not isinstance(platform.get("label"), str) or not platform["label"].strip():
                diagnostic(diagnostics, "IDN2101", f"{pointer}/platform/label", "platform label is empty", "Record the public platform name.")
        canonical_url = value.get("canonicalUrl")
        if canonical_url is not None and (not isinstance(canonical_url, str) or HTTPS_URL.fullmatch(canonical_url) is None):
            diagnostic(diagnostics, "IDN2101", f"{pointer}/canonicalUrl", "canonical channel URL must use HTTPS", "Record the official HTTPS URL or null.")
        elif isinstance(canonical_url, str):
            if canonical_url in urls:
                diagnostic(diagnostics, "IDN2102", f"{pointer}/canonicalUrl", "canonical channel URL is duplicated", "Associate each canonical URL with one record.")
            urls.add(canonical_url)
        handle = value.get("handle")
        if handle is not None and (not isinstance(handle, str) or not handle.strip()):
            diagnostic(diagnostics, "IDN2101", f"{pointer}/handle", "channel handle must be non-empty or null", "Record the exact handle or null.")
        for field in ("ownershipEntity", "audiencePurpose", "recoveryOwner"):
            if not isinstance(value.get(field), str) or not value[field].strip():
                diagnostic(diagnostics, "IDN2101", f"{pointer}/{field}", f"channel {field} must be non-empty", "Record the reviewed public responsibility boundary.")
        for field in ("contentScope", "locale"):
            entries = value.get(field)
            if not isinstance(entries, list) or not entries or any(not isinstance(entry, str) or not entry.strip() for entry in entries):
                diagnostic(diagnostics, "IDN2101", f"{pointer}/{field}", f"channel {field} must contain non-empty strings", "Record at least one reviewed value.")
        verification = require_closed(value.get("verification"), CHANNEL_VERIFICATION_KEYS, CHANNEL_VERIFICATION_KEYS, f"{pointer}/verification", diagnostics)
        if verification is not None:
            if verification.get("state") not in verification_states:
                diagnostic(diagnostics, "IDN2101", f"{pointer}/verification/state", "channel verification state is unsupported", "Use a defined verification state.")
            evidence = verification.get("evidence")
            if evidence is not None and (not isinstance(evidence, str) or HTTPS_URL.fullmatch(evidence) is None):
                diagnostic(diagnostics, "IDN2101", f"{pointer}/verification/evidence", "verification evidence must use HTTPS", "Record public evidence or null.")
            if verification.get("state") == "verified" and evidence is None:
                diagnostic(diagnostics, "IDN2102", f"{pointer}/verification/evidence", "verified channels require public evidence", "Link evidence before marking the account verified.")
        lifecycle = require_closed(value.get("lifecycle"), CHANNEL_LIFECYCLE_KEYS, CHANNEL_LIFECYCLE_KEYS, f"{pointer}/lifecycle", diagnostics)
        lifecycle_state = lifecycle.get("state") if lifecycle is not None else None
        if lifecycle is not None:
            if lifecycle_state not in lifecycle_states:
                diagnostic(diagnostics, "IDN2101", f"{pointer}/lifecycle/state", "channel lifecycle state is unsupported", "Use a defined lifecycle state.")
            try:
                datetime.fromisoformat(str(lifecycle.get("since", "")))
            except ValueError:
                diagnostic(diagnostics, "IDN2101", f"{pointer}/lifecycle/since", "channel lifecycle since must be an ISO date", "Record when the state began.")
            if not isinstance(lifecycle.get("notes"), str):
                diagnostic(diagnostics, "IDN2101", f"{pointer}/lifecycle/notes", "channel lifecycle notes must be a string", "Use an empty string or reviewed notes.")
        accessibility = require_closed(value.get("accessibility"), CHANNEL_ACCESSIBILITY_KEYS, CHANNEL_ACCESSIBILITY_KEYS, f"{pointer}/accessibility", diagnostics)
        if accessibility is not None and (
            not isinstance(accessibility.get("label"), str)
            or not accessibility["label"].strip()
            or not isinstance(accessibility.get("contactNotes"), str)
        ):
            diagnostic(diagnostics, "IDN2101", f"{pointer}/accessibility", "channel accessibility metadata is incomplete", "Record a meaningful label and string contact notes.")
        badge = require_closed(value.get("badge"), CHANNEL_BADGE_KEYS, CHANNEL_BADGE_KEYS, f"{pointer}/badge", diagnostics)
        badge_approved = False
        if badge is not None:
            badge_approved = badge.get("approved") is True
            if not isinstance(badge.get("approved"), bool) or not isinstance(badge.get("label"), str) or not badge["label"].strip():
                diagnostic(diagnostics, "IDN2101", f"{pointer}/badge", "badge approval and label are invalid", "Record a boolean approval and accessible label.")
            icon = require_closed(badge.get("icon"), CHANNEL_ICON_KEYS, CHANNEL_ICON_KEYS, f"{pointer}/badge/icon", diagnostics)
            if icon is not None:
                if not isinstance(icon.get("id"), str) or IDENTIFIER.fullmatch(icon["id"]) is None:
                    diagnostic(diagnostics, "IDN2101", f"{pointer}/badge/icon/id", "badge icon id is invalid", "Use a stable lowercase icon id.")
                if not isinstance(icon.get("source"), str) or HTTPS_URL.fullmatch(icon["source"]) is None:
                    diagnostic(diagnostics, "IDN2101", f"{pointer}/badge/icon/source", "badge icon source must use HTTPS", "Link the reviewed icon source.")
                if not isinstance(icon.get("license"), str) or not icon["license"].strip():
                    diagnostic(diagnostics, "IDN2101", f"{pointer}/badge/icon/license", "badge icon license is empty", "Record icon licensing metadata.")
        if lifecycle_state == "active" and canonical_url is None:
            diagnostic(diagnostics, "IDN2102", f"{pointer}/canonicalUrl", "active channels require a canonical URL", "Record the official URL before activation.")
        if lifecycle_state != "active" and badge_approved:
            diagnostic(diagnostics, "IDN2102", f"{pointer}/badge/approved", "only active channels may approve public badges", "Withhold the badge until the account is active.")
        governance = value.get("governance")
        validate_guidance_governance(governance, f"{pointer}/governance", approvals, diagnostics)
        if isinstance(governance, dict) and governance.get("subject") != f"channel:{identifier}":
            diagnostic(diagnostics, "IDN2102", f"{pointer}/governance/subject", "channel governance subject does not match its id", "Use channel:<id> and an approval for the same subject.")
