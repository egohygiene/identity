# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal repository presentation validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
import hashlib
from pathlib import Path
import re
from typing import Any
from .common import (
    Diagnostic,
    REPOSITORY_PRESENTATION_OVERRIDE_KEYS,
    REPOSITORY_PRESENTATION_PROFILE_KEYS,
    REPOSITORY_PRESENTATION_PROJECT_KEYS,
    REPOSITORY_PRESENTATION_ROOT_KEYS,
    REPOSITORY_PRESENTATION_SELECTION_KEYS,
    REPOSITORY_PRESENTATION_SOURCE_SCHEMA,
    SOCIAL_SURFACE_DIGEST_KEYS,
    diagnostic,
    load_json,
    read_source_bytes,
    require_closed,
    resolve_local_path,
)


def validate_repository_presentation(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> None:
    """Validate optional reviewed banner source and immutable Hygiene profile lock."""

    documents = project.get("documents")
    if not isinstance(documents, dict) or documents.get("repositoryPresentation") is None:
        return
    path_value = documents["repositoryPresentation"]
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/repositoryPresentation",
        diagnostics,
    )
    if path is None:
        return
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return
    require_closed(
        document,
        REPOSITORY_PRESENTATION_ROOT_KEYS,
        REPOSITORY_PRESENTATION_ROOT_KEYS,
        "/",
        diagnostics,
    )
    if not isinstance(document.get("$schema"), str) or not document["$schema"].endswith(
        "/repository-presentation.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/$schema",
            "repository-presentation source must reference repository-presentation.schema.json",
            "Reference the checked-in Identity v1 repository-presentation source schema.",
        )
    if document.get("schema") != REPOSITORY_PRESENTATION_SOURCE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN2001",
            f"{path_value}#/schema",
            f"repository-presentation source schema must be {REPOSITORY_PRESENTATION_SOURCE_SCHEMA}",
            "Migrate the source through an explicit versioned change.",
        )

    lock = require_closed(
        document.get("profile"),
        REPOSITORY_PRESENTATION_PROFILE_KEYS,
        REPOSITORY_PRESENTATION_PROFILE_KEYS,
        f"{path_value}#/profile",
        diagnostics,
    )
    if lock is not None:
        expected = {
            "id": "egohygiene.repository-presentation-profile/v1",
            "owner": "egohygiene/hygiene",
            "repository": "https://github.com/egohygiene/hygiene",
        }
        for field, value in expected.items():
            if lock.get(field) != value:
                diagnostic(
                    diagnostics,
                    "IDN2002",
                    f"{path_value}#/profile/{field}",
                    f"profile {field} must be {value}",
                    "Pin the canonical Hygiene repository-presentation profile.",
                )
        commit = lock.get("commit")
        if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
            diagnostic(
                diagnostics,
                "IDN2002",
                f"{path_value}#/profile/commit",
                "profile commit must be a full 40-character lowercase commit",
                "Pin an immutable Hygiene commit rather than a branch or short revision.",
            )
        digest = require_closed(
            lock.get("digest"),
            SOCIAL_SURFACE_DIGEST_KEYS,
            SOCIAL_SURFACE_DIGEST_KEYS,
            f"{path_value}#/profile/digest",
            diagnostics,
        )
        profile_path = resolve_local_path(
            repository_root,
            lock.get("path"),
            f"{path_value}#/profile/path",
            diagnostics,
        )
        profile = (
            load_json(profile_path, str(lock.get("path")), diagnostics)
            if profile_path is not None
            else None
        )
        if profile is not None and profile_path is not None:
            normalized = (
                read_source_bytes(profile_path).decode("utf-8")
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .encode("utf-8")
            )
            actual_digest = hashlib.sha256(normalized).hexdigest()
            if not isinstance(digest, dict) or digest.get("algorithm") != "sha256-utf8-lf" or digest.get("value") != actual_digest:
                diagnostic(
                    diagnostics,
                    "IDN2002",
                    f"{path_value}#/profile/digest",
                    f"profile bytes differ from the pinned digest: {actual_digest}",
                    "Review and replace the profile version, commit, and digest together.",
                )
            for field, lock_field in (("schema", "id"), ("version", "version"), ("status", "status"), ("owner", "owner")):
                if profile.get(field) != lock.get(lock_field):
                    diagnostic(
                        diagnostics,
                        "IDN2002",
                        f"{path_value}#/profile/{lock_field}",
                        f"profile {field} differs from the selected artifact",
                        "Pin matching profile identity and local bytes.",
                    )
            policy = profile.get("claim_policy")
            if not isinstance(policy, dict) or policy.get("badge_label") != "Hygienic" or policy.get("unknown_fails_closed") is not True:
                diagnostic(
                    diagnostics,
                    "IDN2002",
                    f"{lock.get('path')}#/claim_policy",
                    "profile must preserve the Hygienic label and fail-closed unknown policy",
                    "Use the compatible Hygiene repository-presentation profile.",
                )

    selection = require_closed(
        document.get("organizationDefault"),
        REPOSITORY_PRESENTATION_SELECTION_KEYS,
        REPOSITORY_PRESENTATION_SELECTION_KEYS,
        f"{path_value}#/organizationDefault",
        diagnostics,
    )
    metadata = project.get("project") if isinstance(project.get("project"), dict) else {}
    if selection is not None:
        for field in ("altText", "fallbackText"):
            value = selection.get(field)
            if not isinstance(value, str) or not value.strip():
                diagnostic(
                    diagnostics,
                    "IDN2001",
                    f"{path_value}#/organizationDefault/{field}",
                    f"{field} must be first-class non-empty text",
                    "Record reviewed accessible fallback text.",
                )
        alt_text = selection.get("altText")
        display_name = metadata.get("displayName")
        if isinstance(alt_text, str) and isinstance(display_name, str) and display_name.lower() not in alt_text.lower():
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{path_value}#/organizationDefault/altText",
                "banner alt text must identify the project display name",
                "Describe this repository identity rather than decoration.",
            )
        for approval_field, subject in (
            ("bannerApproval", "repository-presentation-banner-default"),
            ("badgeApproval", "repository-presentation-badge-profile"),
        ):
            approval_id = selection.get(approval_field)
            decision = approvals.get(approval_id)
            if not isinstance(decision, dict) or decision.get("status") != "approved" or decision.get("subject") != subject:
                diagnostic(
                    diagnostics,
                    "IDN2003",
                    f"{path_value}#/organizationDefault/{approval_field}",
                    f"approval does not authorize {subject}",
                    "Add the exact human approval decision.",
                )

    project_selection = require_closed(
        document.get("project"),
        REPOSITORY_PRESENTATION_PROJECT_KEYS,
        REPOSITORY_PRESENTATION_PROJECT_KEYS,
        f"{path_value}#/project",
        diagnostics,
    )
    if project_selection is not None:
        if project_selection.get("visibility") not in {"public", "internal", "private"}:
            diagnostic(
                diagnostics,
                "IDN2001",
                f"{path_value}#/project/visibility",
                "repository visibility is unsupported",
                "Use public, internal, or private.",
            )
        override = project_selection.get("override")
        if override is not None:
            override_value = require_closed(
                override,
                REPOSITORY_PRESENTATION_OVERRIDE_KEYS,
                {"reason", "approval"},
                f"{path_value}#/project/override",
                diagnostics,
            )
            if override_value is not None:
                if not any(field in override_value for field in ("bannerAssetId", "altText")):
                    diagnostic(
                        diagnostics,
                        "IDN2001",
                        f"{path_value}#/project/override",
                        "override must change bannerAssetId or altText",
                        "Remove the empty override or record one bounded difference.",
                    )
                approval_id = override_value.get("approval")
                subject = f"repository-presentation-banner-override:{metadata.get('id')}"
                decision = approvals.get(approval_id)
                if not isinstance(decision, dict) or decision.get("status") != "approved" or decision.get("subject") != subject:
                    diagnostic(
                        diagnostics,
                        "IDN2003",
                        f"{path_value}#/project/override/approval",
                        f"approval does not authorize {subject}",
                        "Add a product-specific human approval decision.",
                    )
