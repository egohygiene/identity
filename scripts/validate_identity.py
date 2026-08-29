#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Validate a local Identity v1 source contract without mutation or network access."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Sequence

PROJECT_SCHEMA = "identity.project/v1"
TOKENS_SCHEMA = "identity.tokens/v1"
TARGETS_SCHEMA = "identity.targets/v1"
PROVENANCE_SCHEMA = "identity.provenance/v1"
APPROVALS_SCHEMA = "identity.approvals/v1"
DIAGNOSTICS_SCHEMA = "identity.diagnostics/v1"
VOICE_SCHEMA = "identity.voice/v1"
USAGE_SCHEMA = "identity.usage/v1"
DESIGN_SYSTEM_SCHEMA = "identity.design-system-source/v1"
DESIGN_REFERENCES_SCHEMA = "identity.design-reference-catalog/v1"
PRESS_KIT_SOURCE_SCHEMA = "identity.press-kit-source/v1"
SOCIAL_SURFACE_SOURCE_SCHEMA = "identity.social-surface-source/v1"
V1_PROFILE_VERSIONS = {
    "archive": "1.0.0",
    "core": "1.0.0",
    "docs": "1.0.0",
    "github": "1.0.0",
    "metadata": "1.0.0",
    "pwa": "1.0.0",
    "social": "1.0.0",
    "tokens": "1.0.0",
    "web": "1.0.0",
}
IDENTITY_EXTENSION = "org.egohygiene.identity"
TOKEN_TYPES = {
    "border",
    "color",
    "cubicBezier",
    "dimension",
    "duration",
    "fontFamily",
    "fontWeight",
    "gradient",
    "number",
    "shadow",
    "strokeStyle",
    "transition",
    "typography",
}
PROJECT_KEYS = {
    "$schema",
    "schema",
    "project",
    "layers",
    "documents",
    "directories",
    "compatibility",
}
PROJECT_METADATA_KEYS = {"id", "displayName", "repository", "tagline", "kind"}
LAYER_KEYS = {"id", "kind", "priority", "tokens", "sha256"}
DOCUMENT_REQUIRED_KEYS = {"brief", "targets", "provenance", "approvals", "guidance"}
DOCUMENT_KEYS = {*DOCUMENT_REQUIRED_KEYS, "handbook", "pressKit", "socialSurfaces"}
GUIDANCE_KEYS = {"voice", "usage"}
HANDBOOK_KEYS = {"designSystem", "references"}
PRESS_KIT_ROOT_KEYS = {
    "$schema",
    "schema",
    "boilerplates",
    "facts",
    "links",
    "contacts",
    "team",
    "assets",
}
PRESS_KIT_BOILERPLATE_KEYS = {"id", "kind", "text", "governance"}
PRESS_KIT_FACT_KEYS = {"id", "label", "value", "governance"}
PRESS_KIT_LINK_KEYS = {"id", "label", "url", "kind", "governance"}
PRESS_KIT_CONTACT_KEYS = {"id", "label", "kind", "value", "notes", "governance"}
PRESS_KIT_TEAM_MEMBER_KEYS = {"id", "name", "role", "bio", "governance"}
PRESS_KIT_ASSET_KEYS = {"id", "assetId", "label", "notes", "governance"}
SOCIAL_SURFACE_ROOT_KEYS = {
    "$schema",
    "schema",
    "catalog",
    "organizationDefaults",
    "project",
}
SOCIAL_SURFACE_CATALOG_KEYS = {"path", "id", "version", "digest"}
SOCIAL_SURFACE_DIGEST_KEYS = {"algorithm", "value"}
SOCIAL_SURFACE_DEFAULT_KEYS = {
    "id",
    "surfaceId",
    "sourceAssetId",
    "copySource",
    "linkSource",
    "governance",
}
SOCIAL_SURFACE_PROJECT_KEYS = {"adopt", "exclude", "overrides"}
SOCIAL_SURFACE_ADOPTION_KEYS = {"id", "approval"}
SOCIAL_SURFACE_EXCLUSION_KEYS = {"id", "reason", "approval"}
SOCIAL_SURFACE_OVERRIDE_KEYS = {
    "id",
    "sourceAssetId",
    "copySource",
    "linkSource",
    "reason",
    "approval",
}
SOCIAL_SURFACE_RECORD_REQUIRED_KEYS = {
    "id",
    "platform",
    "placement",
    "use",
    "content_type",
    "media_format",
    "dimensions",
    "aspect_ratio",
    "file_types",
    "file_size_limit_bytes",
    "duration_limit_seconds",
    "safe_zone",
    "verification",
    "source",
    "lifecycle",
}
DIRECTORY_KEYS = {"sources", "candidates", "references"}
COMPATIBILITY_KEYS = {"acceptedSchemaMajor", "migrationFrom"}
TOKEN_METADATA = {"$value", "$type", "$description", "$extensions", "$deprecated"}
GROUP_METADATA = {"$type", "$description", "$extensions", "$deprecated"}
IDENTITY_EXTENSION_KEYS = {
    "schema",
    "layer",
    "override",
    "contrast",
    "typography",
    "motion",
    "provenance",
}
LAYER_EXTENSION_KEYS = {"id", "kind", "priority"}
OVERRIDE_EXTENSION_KEYS = {"reason", "approval"}
CONTRAST_EXTENSION_KEYS = {"intent", "pairedWith", "minimumRatio"}
TYPOGRAPHY_EXTENSION_KEYS = {"license", "languages", "legibility"}
MOTION_EXTENSION_KEYS = {"reducedMotion"}
PROVENANCE_EXTENSION_KEYS = {"record", "approval"}
TARGET_KEYS = {"$schema", "schema", "enabled", "inapplicable"}
TARGET_PROFILE_KEYS = {"id", "version"}
APPROVAL_ROOT_KEYS = {"$schema", "schema", "decisions"}
APPROVAL_KEYS = {
    "id",
    "subject",
    "candidate",
    "status",
    "reviewedBy",
    "reviewedAt",
    "evidence",
    "supersedes",
    "notes",
}
PROVENANCE_ROOT_KEYS = {"$schema", "schema", "assets"}
ASSET_KEYS = {
    "id",
    "path",
    "kind",
    "sha256",
    "license",
    "origin",
    "accessibility",
    "usage",
    "approval",
}
LICENSE_KEYS = {"spdx", "status", "attribution"}
ORIGIN_KEYS = {"creator", "method", "source", "capturedAt"}
ACCESSIBILITY_KEYS = {"altText"}
USAGE_KEYS = {"safeZone", "minimumSize", "restrictions"}
VOICE_ROOT_KEYS = {
    "$schema",
    "schema",
    "foundation",
    "characteristics",
    "contexts",
    "localization",
}
VOICE_FOUNDATION_KEYS = {
    "purpose",
    "positioning",
    "audience",
    "personality",
    "governance",
}
VOICE_CHARACTERISTIC_KEYS = {"id", "label", "description", "governance"}
VOICE_CONTEXT_KEYS = {
    "id",
    "label",
    "audience",
    "intent",
    "tone",
    "characteristics",
    "preferredVocabulary",
    "avoidedLanguage",
    "naming",
    "capitalization",
    "punctuation",
    "examples",
    "antiExamples",
    "governance",
}
VOICE_MESSAGE_KEYS = {"id", "text", "rationale", "governance"}
VOICE_LOCALIZATION_KEYS = {
    "sourceLanguage",
    "supportedLanguages",
    "fallback",
    "governance",
}
VOICE_LANGUAGE_KEYS = {"tag", "coverage", "notes"}
GOVERNANCE_KEYS = {"subject", "state", "visibility", "provenance", "approval"}
GUIDANCE_PROVENANCE_KEYS = {"method", "source", "capturedAt"}
USAGE_ROOT_KEYS = {"$schema", "schema", "sections", "assets", "accessibility", "legal"}
USAGE_SECTION_KEYS = {"id", "title", "description", "rules"}
USAGE_RULE_KEYS = {
    "id",
    "kind",
    "category",
    "instruction",
    "rationale",
    "details",
    "contexts",
    "governance",
}
USAGE_ASSET_KEYS = {
    "id",
    "label",
    "kind",
    "path",
    "status",
    "availability",
    "replacement",
    "downloadName",
    "notes",
    "governance",
}
USAGE_ACCESSIBILITY_KEYS = {"summary", "rules", "governance"}
USAGE_LEGAL_KEYS = {
    "trademark",
    "copyright",
    "attribution",
    "thirdPartyLicenses",
    "governance",
}
USAGE_LICENSE_KEYS = {"name", "spdx", "attribution"}
DESIGN_SYSTEM_ROOT_KEYS = {"$schema", "schema", "sections", "capabilities"}
DESIGN_SYSTEM_SECTION_KEYS = {"id", "title", "summary", "principles"}
DESIGN_SYSTEM_PRINCIPLE_KEYS = {
    "id",
    "title",
    "guidance",
    "rationale",
    "appliesTo",
    "governance",
}
DESIGN_SYSTEM_CAPABILITY_KEYS = {"id", "label", "status", "owner", "notes", "governance"}
DESIGN_REFERENCE_ROOT_KEYS = {"$schema", "schema", "references"}
DESIGN_REFERENCE_KEYS = {
    "id",
    "url",
    "capturedAt",
    "patterns",
    "decision",
    "notes",
    "rights",
    "affectsCanonical",
    "governance",
}
GUIDANCE_STATES = {"candidate", "approved", "rejected", "superseded"}
GUIDANCE_CATEGORIES = {
    "mark",
    "color",
    "typography",
    "imagery",
    "illustration",
    "mascot",
    "motion",
    "accessibility",
    "legal",
    "localization",
}
IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
HTTPS_URL = re.compile(r"^https://[^\s]+$")
ALIAS = re.compile(r"^\{([A-Za-z0-9_.-]+)\}$")
EXTENSION_NAME = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9-]+)+$")
LANGUAGE_TAG = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


class DuplicateKeyError(ValueError):
    """Raised when JSON repeats a key and would otherwise be ambiguous."""


@dataclass(frozen=True, order=True)
class Diagnostic:
    """One stable, actionable validation result."""

    path: str
    code: str
    message: str
    recovery: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        """Return the versioned machine-readable projection."""

        return {
            "code": self.code,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
            "recovery": self.recovery,
        }


@dataclass(frozen=True)
class TokenRecord:
    """One flattened DTCG token plus its source layer."""

    path: str
    token_type: str | None
    value: Any
    extension: dict[str, Any]
    pointer: str
    layer: str


def object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object while rejecting repeated keys."""

    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def diagnostic(
    diagnostics: list[Diagnostic],
    code: str,
    path: str,
    message: str,
    recovery: str,
) -> None:
    """Append one error without interrupting independent checks."""

    diagnostics.append(Diagnostic(path, code, message, recovery))


def require_closed(
    value: Any,
    expected: set[str],
    required: set[str],
    path: str,
    diagnostics: list[Diagnostic],
) -> dict[str, Any] | None:
    """Require an object with named fields and no silent extensions."""

    if not isinstance(value, dict):
        diagnostic(
            diagnostics,
            "IDN1101",
            path,
            "value must be an object",
            "Replace it with an object.",
        )
        return None
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        diagnostic(
            diagnostics,
            "IDN1101",
            path,
            f"missing required fields: {', '.join(missing)}",
            "Add every required field using the v1 schema.",
        )
    if unknown:
        diagnostic(
            diagnostics,
            "IDN1101",
            path,
            f"unknown fields: {', '.join(unknown)}",
            "Remove unknown fields or move versioned data into a namespaced extension.",
        )
    return value


def valid_relative_path(value: Any) -> bool:
    """Return whether a string is one normalized repository-relative path."""

    if (
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or value.endswith("/")
        or "//" in value
        or "\\" in value
        or "\x00" in value
    ):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def load_json(path: Path, pointer: str, diagnostics: list[Diagnostic]) -> dict[str, Any] | None:
    """Load a closed JSON object and normalize file failures into diagnostics."""

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=object_without_duplicates,
        )
    except DuplicateKeyError as error:
        diagnostic(diagnostics, "IDN1102", pointer, str(error), "Remove the repeated key.")
        return None
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        diagnostic(
            diagnostics,
            "IDN1001",
            pointer,
            f"cannot load JSON: {error}",
            "Create readable UTF-8 JSON at the declared path.",
        )
        return None
    if not isinstance(value, dict):
        diagnostic(
            diagnostics,
            "IDN1101",
            pointer,
            "document must be an object",
            "Use a JSON object.",
        )
        return None
    return value


def resolve_local_path(
    repository_root: Path,
    value: Any,
    pointer: str,
    diagnostics: list[Diagnostic],
    *,
    directory: bool = False,
) -> Path | None:
    """Resolve one declared local path without allowing traversal or symlinks."""

    if not valid_relative_path(value):
        diagnostic(
            diagnostics,
            "IDN1003",
            pointer,
            "path must be normalized and repository-relative",
            "Use a path without absolute roots, dot segments, repeated separators, or backslashes.",
        )
        return None
    candidate = repository_root / value
    current = repository_root
    for part in PurePosixPath(value).parts:
        current = current / part
        if current.is_symlink():
            diagnostic(
                diagnostics,
                "IDN1003",
                pointer,
                "path may not traverse a symbolic link",
                "Replace the symbolic link with repository-owned local content.",
            )
            return None
    exists = candidate.is_dir() if directory else candidate.is_file()
    if not exists:
        expected = "directory" if directory else "file"
        diagnostic(
            diagnostics,
            "IDN1003",
            pointer,
            f"declared {expected} does not exist: {value}",
            f"Create the {expected} or correct the declared path.",
        )
        return None
    return candidate


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one local file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


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
                resolve_local_path(
                    repository_root,
                    guidance.get(field),
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


def validate_layer_declaration(
    layer: Any,
    index: int,
    diagnostics: list[Diagnostic],
) -> dict[str, Any] | None:
    """Validate one layer declaration before reading its token document."""

    pointer = f"/layers/{index}"
    value = require_closed(layer, LAYER_KEYS, LAYER_KEYS, pointer, diagnostics)
    if value is None:
        return None
    if not isinstance(value.get("id"), str) or IDENTIFIER.fullmatch(value["id"]) is None:
        diagnostic(
            diagnostics,
            "IDN1101",
            f"{pointer}/id",
            "layer id is invalid",
            "Use a stable lowercase identifier.",
        )
    if value.get("kind") not in {"organization-defaults", "product-override"}:
        diagnostic(
            diagnostics,
            "IDN1301",
            f"{pointer}/kind",
            "layer kind is unsupported",
            "Use organization-defaults or product-override.",
        )
    if (
        isinstance(value.get("priority"), bool)
        or not isinstance(value.get("priority"), int)
        or value["priority"] < 0
    ):
        diagnostic(
            diagnostics,
            "IDN1301",
            f"{pointer}/priority",
            "priority must be a non-negative integer",
            "Assign deterministic ascending integer priorities.",
        )
    if not isinstance(value.get("sha256"), str) or SHA256.fullmatch(value["sha256"]) is None:
        diagnostic(
            diagnostics,
            "IDN1302",
            f"{pointer}/sha256",
            "layer digest must be 64 lowercase hexadecimal characters",
            "Record the SHA-256 digest of the local token document.",
        )
    return value


def validate_extensions(
    extensions: Any, pointer: str, diagnostics: list[Diagnostic]
) -> dict[str, Any]:
    """Validate namespacing and the closed Identity extension boundary."""

    if extensions is None:
        return {}
    if not isinstance(extensions, dict):
        diagnostic(
            diagnostics,
            "IDN1202",
            pointer,
            "$extensions must be an object",
            "Use namespaced extension objects.",
        )
        return {}
    for name, value in extensions.items():
        if EXTENSION_NAME.fullmatch(name) is None or not isinstance(value, dict):
            diagnostic(
                diagnostics,
                "IDN1202",
                f"{pointer}/{name}",
                "extension must use a dotted lowercase namespace and object value",
                "Namespace and version the extension explicitly.",
            )
    identity = extensions.get(IDENTITY_EXTENSION, {})
    if isinstance(identity, dict):
        unknown = sorted(set(identity) - IDENTITY_EXTENSION_KEYS)
        if unknown:
            diagnostic(
                diagnostics,
                "IDN1202",
                f"{pointer}/{IDENTITY_EXTENSION}",
                f"unknown Identity extension fields: {', '.join(unknown)}",
                "Remove the fields or version the Identity extension contract.",
            )
        layer = identity.get("layer")
        if layer is not None:
            require_closed(
                layer,
                LAYER_EXTENSION_KEYS,
                LAYER_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/layer",
                diagnostics,
            )
        override = identity.get("override")
        if override is not None:
            value = require_closed(
                override,
                OVERRIDE_EXTENSION_KEYS,
                OVERRIDE_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/override",
                diagnostics,
            )
            if value is not None and any(
                not isinstance(value.get(field), str) or not value[field].strip()
                for field in OVERRIDE_EXTENSION_KEYS
            ):
                diagnostic(
                    diagnostics,
                    "IDN1202",
                    f"{pointer}/{IDENTITY_EXTENSION}/override",
                    "override reason and approval must be non-empty",
                    "Record reviewed override intent and its approval ID.",
                )
        contrast = identity.get("contrast")
        if contrast is not None:
            value = require_closed(
                contrast,
                CONTRAST_EXTENSION_KEYS,
                CONTRAST_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/contrast",
                diagnostics,
            )
            if value is not None:
                intent = value.get("intent")
                pairings = value.get("pairedWith")
                ratio = value.get("minimumRatio")
                if intent not in {"background", "foreground", "decorative"}:
                    diagnostic(
                        diagnostics,
                        "IDN1202",
                        f"{pointer}/{IDENTITY_EXTENSION}/contrast/intent",
                        "contrast intent is unsupported",
                        "Use background, foreground, or decorative.",
                    )
                if (
                    not isinstance(pairings, list)
                    or any(not isinstance(item, str) or not item for item in pairings)
                    or (intent in {"background", "foreground"} and not pairings)
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1202",
                        f"{pointer}/{IDENTITY_EXTENSION}/contrast/pairedWith",
                        "contrast pairings are incomplete",
                        "Name every supported foreground/background semantic token pairing.",
                    )
                if (
                    isinstance(ratio, bool)
                    or not isinstance(ratio, (int, float))
                    or not 1 <= ratio <= 21
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1202",
                        f"{pointer}/{IDENTITY_EXTENSION}/contrast/minimumRatio",
                        "minimum contrast ratio must be between 1 and 21",
                        "Declare the intended WCAG contrast threshold.",
                    )
        typography = identity.get("typography")
        if typography is not None:
            value = require_closed(
                typography,
                TYPOGRAPHY_EXTENSION_KEYS,
                TYPOGRAPHY_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/typography",
                diagnostics,
            )
            if value is not None:
                languages = value.get("languages")
                if (
                    not isinstance(value.get("license"), str)
                    or not value["license"].strip()
                    or not isinstance(languages, list)
                    or not languages
                    or any(not isinstance(item, str) or len(item) < 2 for item in languages)
                    or not isinstance(value.get("legibility"), str)
                    or not value["legibility"].strip()
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1202",
                        f"{pointer}/{IDENTITY_EXTENSION}/typography",
                        "typography governance is incomplete",
                        "Record license, language coverage, and legibility constraints.",
                    )
        motion = identity.get("motion")
        if motion is not None:
            value = require_closed(
                motion,
                MOTION_EXTENSION_KEYS,
                MOTION_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/motion",
                diagnostics,
            )
            if value is not None and (
                not isinstance(value.get("reducedMotion"), str)
                or not value["reducedMotion"].strip()
            ):
                diagnostic(
                    diagnostics,
                    "IDN1202",
                    f"{pointer}/{IDENTITY_EXTENSION}/motion/reducedMotion",
                    "motion token requires a reduced-motion alternative",
                    "Reference a stable reduced-motion semantic token.",
                )
        provenance = identity.get("provenance")
        if provenance is not None:
            value = require_closed(
                provenance,
                PROVENANCE_EXTENSION_KEYS,
                PROVENANCE_EXTENSION_KEYS,
                f"{pointer}/{IDENTITY_EXTENSION}/provenance",
                diagnostics,
            )
            if value is not None and any(
                not isinstance(value.get(field), str) or not value[field].strip()
                for field in PROVENANCE_EXTENSION_KEYS
            ):
                diagnostic(
                    diagnostics,
                    "IDN1202",
                    f"{pointer}/{IDENTITY_EXTENSION}/provenance",
                    "token provenance references are incomplete",
                    "Record provenance and approval identifiers.",
                )
        return identity
    return {}


def flatten_tokens(
    node: dict[str, Any],
    layer: str,
    diagnostics: list[Diagnostic],
    *,
    prefix: tuple[str, ...] = (),
    pointer: str = "",
    inherited_type: str | None = None,
) -> list[TokenRecord]:
    """Flatten a supported DTCG tree and validate its closed structure."""

    records: list[TokenRecord] = []
    group_type = node.get("$type", inherited_type)
    if group_type is not None and group_type not in TOKEN_TYPES:
        diagnostic(
            diagnostics,
            "IDN1204",
            f"{pointer}/$type",
            f"unsupported token type: {group_type}",
            "Use a DTCG 2025.10 stable token type.",
        )
    validate_extensions(node.get("$extensions"), f"{pointer}/$extensions", diagnostics)
    for key, child in node.items():
        if key.startswith("$"):
            if key not in GROUP_METADATA and not (pointer == "" and key == "$schema"):
                diagnostic(
                    diagnostics,
                    "IDN1202",
                    f"{pointer}/{key}",
                    "unknown DTCG group metadata",
                    "Use a supported DTCG field or namespaced extension.",
                )
            continue
        child_pointer = f"{pointer}/{key}"
        if not isinstance(child, dict):
            diagnostic(
                diagnostics,
                "IDN1202",
                child_pointer,
                "token or group must be an object",
                "Wrap values in a DTCG token object containing $value.",
            )
            continue
        if "$value" not in child:
            records.extend(
                flatten_tokens(
                    child,
                    layer,
                    diagnostics,
                    prefix=(*prefix, key),
                    pointer=child_pointer,
                    inherited_type=group_type,
                )
            )
            continue
        unknown = sorted(set(child) - TOKEN_METADATA)
        if unknown:
            diagnostic(
                diagnostics,
                "IDN1202",
                child_pointer,
                f"unknown token fields: {', '.join(unknown)}",
                "Remove unknown fields or move them into a namespaced extension.",
            )
        token_type = child.get("$type", group_type)
        if token_type is None:
            diagnostic(
                diagnostics,
                "IDN1203",
                child_pointer,
                "token has no explicit or inherited $type",
                "Declare a DTCG type on the token or its containing group.",
            )
        elif token_type not in TOKEN_TYPES:
            diagnostic(
                diagnostics,
                "IDN1204",
                f"{child_pointer}/$type",
                f"unsupported token type: {token_type}",
                "Use a DTCG 2025.10 stable token type.",
            )
        extension = validate_extensions(
            child.get("$extensions"),
            f"{child_pointer}/$extensions",
            diagnostics,
        )
        records.append(
            TokenRecord(
                path=".".join((*prefix, key)),
                token_type=token_type if isinstance(token_type, str) else None,
                value=child.get("$value"),
                extension=extension,
                pointer=child_pointer,
                layer=layer,
            )
        )
    return records


def load_layers(
    project: dict[str, Any], repository_root: Path, diagnostics: list[Diagnostic]
) -> tuple[dict[str, TokenRecord], list[tuple[str, str]]]:
    """Load, verify, merge, and alias-check every declared DTCG layer."""

    declarations = project.get("layers")
    if not isinstance(declarations, list) or not declarations:
        diagnostic(
            diagnostics,
            "IDN1301",
            "/layers",
            "layers must be a non-empty array",
            "Declare organization defaults followed by one product override.",
        )
        return {}, []
    valid = [
        value
        for index, layer in enumerate(declarations)
        if (value := validate_layer_declaration(layer, index, diagnostics)) is not None
    ]
    ids = [value["id"] for value in valid if isinstance(value.get("id"), str)]
    priorities = [
        value["priority"]
        for value in valid
        if isinstance(value.get("priority"), int) and not isinstance(value.get("priority"), bool)
    ]
    kinds = [value["kind"] for value in valid if isinstance(value.get("kind"), str)]
    if len(ids) != len(set(ids)):
        diagnostic(
            diagnostics,
            "IDN1301",
            "/layers",
            "layer ids must be unique",
            "Rename duplicate layers.",
        )
    if (
        len(priorities) != len(valid)
        or len(priorities) != len(set(priorities))
        or priorities != sorted(priorities)
    ):
        diagnostic(
            diagnostics,
            "IDN1301",
            "/layers",
            "layer priorities must be unique and ascending",
            "Order layers by unique ascending priority.",
        )
    if kinds.count("product-override") != 1 or not kinds or kinds[-1] != "product-override":
        diagnostic(
            diagnostics,
            "IDN1301",
            "/layers",
            "exactly one product-override layer must be last",
            "Place organization defaults first and one product override last.",
        )
    if "organization-defaults" not in kinds:
        diagnostic(
            diagnostics,
            "IDN1301",
            "/layers",
            "at least one organization-defaults layer is required",
            "Pin a local organization-default token snapshot.",
        )

    resolved: dict[str, TokenRecord] = {}
    override_approvals: list[tuple[str, str]] = []
    for index, layer in enumerate(valid):
        token_path = resolve_local_path(
            repository_root, layer.get("tokens"), f"/layers/{index}/tokens", diagnostics
        )
        if token_path is None:
            continue
        expected_digest = layer.get("sha256")
        actual_digest = sha256(token_path)
        if expected_digest != actual_digest:
            diagnostic(
                diagnostics,
                "IDN1302",
                f"/layers/{index}/sha256",
                f"token document digest differs: {actual_digest}",
                "Review the token change and update the digest intentionally.",
            )
        document = load_json(token_path, str(layer.get("tokens")), diagnostics)
        if document is None:
            continue
        root_extension = validate_extensions(
            document.get("$extensions"),
            "/$extensions",
            diagnostics,
        )
        if root_extension.get("schema") != TOKENS_SCHEMA:
            diagnostic(
                diagnostics,
                "IDN1201",
                f"{layer.get('tokens')}#/$extensions/{IDENTITY_EXTENSION}/schema",
                f"token document must declare {TOKENS_SCHEMA}",
                "Use the Identity v1 DTCG extension identity.",
            )
        declared_layer = root_extension.get("layer")
        expected_layer = {
            "id": layer.get("id"),
            "kind": layer.get("kind"),
            "priority": layer.get("priority"),
        }
        if declared_layer != expected_layer:
            diagnostic(
                diagnostics,
                "IDN1303",
                f"{layer.get('tokens')}#/$extensions/{IDENTITY_EXTENSION}/layer",
                "token document layer metadata does not match identity.json",
                "Make the token layer identity, kind, and priority agree.",
            )
        records = flatten_tokens(document, str(layer.get("id")), diagnostics)
        for record in records:
            previous = resolved.get(record.path)
            if previous is not None:
                override = record.extension.get("override")
                if not isinstance(override, dict) or not all(
                    isinstance(override.get(field), str) and override[field].strip()
                    for field in ("reason", "approval")
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1304",
                        f"{layer.get('tokens')}#{record.pointer}",
                        f"token {record.path} overrides {previous.layer} without reviewed intent",
                        "Add an Identity override extension with reason and approval ID.",
                    )
                else:
                    override_approvals.append((override["approval"], record.path))
            resolved[record.path] = record

    validate_aliases(resolved, diagnostics)
    return resolved, override_approvals


def validate_aliases(tokens: dict[str, TokenRecord], diagnostics: list[Diagnostic]) -> None:
    """Reject aliases that are missing, cyclic, or type-incompatible."""

    for path, token in tokens.items():
        motion = token.extension.get("motion")
        if isinstance(motion, dict):
            reduced = motion.get("reducedMotion")
            if isinstance(reduced, str) and reduced not in tokens:
                diagnostic(
                    diagnostics,
                    "IDN1305",
                    token.pointer,
                    f"motion token {path} references missing reduced-motion token {reduced}",
                    "Declare the reduced-motion token or correct the reference.",
                )
        match = ALIAS.fullmatch(token.value) if isinstance(token.value, str) else None
        if match is None:
            continue
        target = match.group(1)
        if target not in tokens:
            diagnostic(
                diagnostics,
                "IDN1305",
                token.pointer,
                f"token {path} references missing alias {target}",
                "Declare the target token or correct the alias path.",
            )
            continue
        visited = {path}
        current = target
        while True:
            if current not in tokens:
                diagnostic(
                    diagnostics,
                    "IDN1305",
                    token.pointer,
                    f"token {path} references missing alias {current}",
                    "Declare the target token or correct the alias path.",
                )
                break
            if current in visited:
                diagnostic(
                    diagnostics,
                    "IDN1306",
                    token.pointer,
                    f"token {path} participates in an alias cycle",
                    "Replace the cycle with a concrete source token.",
                )
                break
            visited.add(current)
            candidate = tokens[current]
            alias = ALIAS.fullmatch(candidate.value) if isinstance(candidate.value, str) else None
            if alias is None:
                if token.token_type != candidate.token_type:
                    diagnostic(
                        diagnostics,
                        "IDN1305",
                        token.pointer,
                        (
                            f"alias type {token.token_type} differs from target type "
                            f"{candidate.token_type}"
                        ),
                        "Make the alias and target token types agree.",
                    )
                break
            current = alias.group(1)


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


def validate_guidance_strings(
    value: Any,
    pointer: str,
    diagnostics: list[Diagnostic],
) -> list[str]:
    """Validate a unique, non-empty list of non-empty strings."""

    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
        or len(value) != len(set(value))
    ):
        diagnostic(
            diagnostics,
            "IDN1601",
            pointer,
            "guidance list must contain unique non-empty strings",
            "Provide at least one reviewed, non-empty value without duplicates.",
        )
        return []
    return value


def validate_guidance_text_fields(
    value: dict[str, Any],
    fields: Sequence[str],
    pointer: str,
    diagnostics: list[Diagnostic],
) -> None:
    """Validate required authored guidance strings."""

    for field in fields:
        if not isinstance(value.get(field), str) or not value[field].strip():
            diagnostic(
                diagnostics,
                "IDN1601",
                f"{pointer}/{field}",
                "guidance text must be a non-empty string",
                "Provide reviewed guidance text.",
            )


def validate_guidance_governance(
    value: Any,
    pointer: str,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> dict[str, Any] | None:
    """Validate lifecycle state, provenance, visibility, and human authority."""

    governance = require_closed(
        value,
        GOVERNANCE_KEYS,
        GOVERNANCE_KEYS,
        pointer,
        diagnostics,
    )
    if governance is None:
        return None
    subject = governance.get("subject")
    if not isinstance(subject, str) or not subject.strip():
        diagnostic(
            diagnostics,
            "IDN1602",
            f"{pointer}/subject",
            "governance subject must be non-empty",
            "Name the exact content or bundle reviewed by the decision.",
        )
    state = governance.get("state")
    if state not in GUIDANCE_STATES:
        diagnostic(
            diagnostics,
            "IDN1602",
            f"{pointer}/state",
            "guidance state is unsupported",
            "Use candidate, approved, rejected, or superseded.",
        )
    visibility = governance.get("visibility")
    if visibility not in {"public", "internal"}:
        diagnostic(
            diagnostics,
            "IDN1602",
            f"{pointer}/visibility",
            "guidance visibility is unsupported",
            "Use public or internal.",
        )
    if state != "approved" and visibility == "public":
        diagnostic(
            diagnostics,
            "IDN1602",
            f"{pointer}/visibility",
            "unapproved guidance cannot be public",
            "Keep candidate, rejected, and superseded content internal.",
        )

    provenance = require_closed(
        governance.get("provenance"),
        GUIDANCE_PROVENANCE_KEYS,
        GUIDANCE_PROVENANCE_KEYS,
        f"{pointer}/provenance",
        diagnostics,
    )
    if provenance is not None:
        validate_guidance_text_fields(
            provenance,
            ("source",),
            f"{pointer}/provenance",
            diagnostics,
        )
        if provenance.get("method") not in {
            "human-authored",
            "handoff-candidate",
            "imported",
        }:
            diagnostic(
                diagnostics,
                "IDN1602",
                f"{pointer}/provenance/method",
                "guidance provenance method is unsupported",
                "Use human-authored, handoff-candidate, or imported.",
            )
        try:
            datetime.fromisoformat(
                str(provenance.get("capturedAt", "")).replace("Z", "+00:00")
            )
        except ValueError:
            diagnostic(
                diagnostics,
                "IDN1602",
                f"{pointer}/provenance/capturedAt",
                "capturedAt must be an RFC 3339 timestamp",
                "Record the source capture time with an explicit UTC offset.",
            )

    approval_id = governance.get("approval")
    if state == "candidate":
        if provenance is not None and provenance.get("method") != "handoff-candidate":
            diagnostic(
                diagnostics,
                "IDN1602",
                f"{pointer}/provenance/method",
                "candidate guidance must enter through the handoff boundary",
                "Use handoff-candidate and record the explicit candidate source.",
            )
        if approval_id is not None:
            diagnostic(
                diagnostics,
                "IDN1602",
                f"{pointer}/approval",
                "candidate guidance cannot claim an approval decision",
                "Use null until a human decision is recorded.",
            )
        return governance
    decision = approvals.get(approval_id) if isinstance(approval_id, str) else None
    if (
        decision is None
        or decision.get("status") != state
        or decision.get("subject") != subject
    ):
        diagnostic(
            diagnostics,
            "IDN1602",
            f"{pointer}/approval",
            "guidance state does not resolve to a matching human decision",
            "Link the reviewed subject to a decision with the same lifecycle state.",
        )
    return governance


def validate_voice_message(
    value: Any,
    pointer: str,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> str | None:
    """Validate one voice example or anti-example."""

    message = require_closed(
        value,
        VOICE_MESSAGE_KEYS,
        VOICE_MESSAGE_KEYS,
        pointer,
        diagnostics,
    )
    if message is None:
        return None
    validate_guidance_text_fields(
        message,
        ("id", "text", "rationale"),
        pointer,
        diagnostics,
    )
    identifier = message.get("id")
    if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{pointer}/id",
            "voice example id is invalid",
            "Use a stable lowercase identifier.",
        )
        identifier = None
    validate_guidance_governance(
        message.get("governance"),
        f"{pointer}/governance",
        approvals,
        diagnostics,
    )
    return identifier


def validate_voice(
    project: dict[str, Any],
    repository_root: Path,
    approvals: dict[str, dict[str, Any]],
    diagnostics: list[Diagnostic],
) -> set[str]:
    """Validate structured voice, contextual tone, examples, and localization."""

    documents = project.get("documents")
    guidance = documents.get("guidance") if isinstance(documents, dict) else None
    if not isinstance(guidance, dict):
        return set()
    path_value = guidance.get("voice")
    path = resolve_local_path(
        repository_root,
        path_value,
        "/documents/guidance/voice",
        diagnostics,
    )
    if path is None:
        return set()
    document = load_json(path, str(path_value), diagnostics)
    if document is None:
        return set()
    require_closed(document, VOICE_ROOT_KEYS, VOICE_ROOT_KEYS, "/", diagnostics)
    schema_reference = document.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference.endswith(
        "/voice.schema.json"
    ):
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/$schema",
            "voice schema reference must end in /voice.schema.json",
            "Reference the checked-in Identity v1 voice schema.",
        )
    if document.get("schema") != VOICE_SCHEMA:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/schema",
            f"voice schema must be {VOICE_SCHEMA}",
            "Migrate voice guidance to the v1 contract.",
        )

    foundation = require_closed(
        document.get("foundation"),
        VOICE_FOUNDATION_KEYS,
        VOICE_FOUNDATION_KEYS,
        f"{path_value}#/foundation",
        diagnostics,
    )
    if foundation is not None:
        validate_guidance_text_fields(
            foundation,
            ("purpose", "positioning"),
            f"{path_value}#/foundation",
            diagnostics,
        )
        validate_guidance_strings(
            foundation.get("audience"),
            f"{path_value}#/foundation/audience",
            diagnostics,
        )
        validate_guidance_strings(
            foundation.get("personality"),
            f"{path_value}#/foundation/personality",
            diagnostics,
        )
        validate_guidance_governance(
            foundation.get("governance"),
            f"{path_value}#/foundation/governance",
            approvals,
            diagnostics,
        )

    characteristic_ids: set[str] = set()
    characteristics = document.get("characteristics")
    if not isinstance(characteristics, list) or not characteristics:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/characteristics",
            "voice requires at least one characteristic",
            "Add reviewed voice characteristics.",
        )
    else:
        for index, item in enumerate(characteristics):
            pointer = f"{path_value}#/characteristics/{index}"
            value = require_closed(
                item,
                VOICE_CHARACTERISTIC_KEYS,
                VOICE_CHARACTERISTIC_KEYS,
                pointer,
                diagnostics,
            )
            if value is None:
                continue
            validate_guidance_text_fields(
                value,
                ("id", "label", "description"),
                pointer,
                diagnostics,
            )
            identifier = value.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in characteristic_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1601",
                    f"{pointer}/id",
                    "voice characteristic id is invalid or duplicated",
                    "Use each stable lowercase identifier once.",
                )
            else:
                characteristic_ids.add(identifier)
            validate_guidance_governance(
                value.get("governance"),
                f"{pointer}/governance",
                approvals,
                diagnostics,
            )

    context_ids: set[str] = set()
    message_ids: set[str] = set()
    contexts = document.get("contexts")
    if not isinstance(contexts, list) or not contexts:
        diagnostic(
            diagnostics,
            "IDN1601",
            f"{path_value}#/contexts",
            "voice requires at least one context",
            "Add a retrievable tone context.",
        )
    else:
        for index, item in enumerate(contexts):
            pointer = f"{path_value}#/contexts/{index}"
            value = require_closed(
                item,
                VOICE_CONTEXT_KEYS,
                VOICE_CONTEXT_KEYS,
                pointer,
                diagnostics,
            )
            if value is None:
                continue
            validate_guidance_text_fields(
                value,
                (
                    "id",
                    "label",
                    "audience",
                    "intent",
                    "tone",
                    "naming",
                    "capitalization",
                    "punctuation",
                ),
                pointer,
                diagnostics,
            )
            identifier = value.get("id")
            if (
                not isinstance(identifier, str)
                or IDENTIFIER.fullmatch(identifier) is None
                or identifier in context_ids
            ):
                diagnostic(
                    diagnostics,
                    "IDN1601",
                    f"{pointer}/id",
                    "voice context id is invalid or duplicated",
                    "Use each stable lowercase context identifier once.",
                )
            else:
                context_ids.add(identifier)
            referenced = validate_guidance_strings(
                value.get("characteristics"),
                f"{pointer}/characteristics",
                diagnostics,
            )
            unknown = sorted(set(referenced) - characteristic_ids)
            if unknown:
                diagnostic(
                    diagnostics,
                    "IDN1604",
                    f"{pointer}/characteristics",
                    f"unknown voice characteristics: {', '.join(unknown)}",
                    "Reference a declared characteristic ID.",
                )
            for field in ("preferredVocabulary", "avoidedLanguage"):
                validate_guidance_strings(
                    value.get(field),
                    f"{pointer}/{field}",
                    diagnostics,
                )
            for field in ("examples", "antiExamples"):
                messages = value.get(field)
                if not isinstance(messages, list) or not messages:
                    diagnostic(
                        diagnostics,
                        "IDN1601",
                        f"{pointer}/{field}",
                        "each context needs at least one example and anti-example",
                        "Add reviewed messaging evidence.",
                    )
                    continue
                for message_index, message in enumerate(messages):
                    message_id = validate_voice_message(
                        message,
                        f"{pointer}/{field}/{message_index}",
                        approvals,
                        diagnostics,
                    )
                    if message_id in message_ids:
                        diagnostic(
                            diagnostics,
                            "IDN1601",
                            f"{pointer}/{field}/{message_index}/id",
                            "voice message id is duplicated",
                            "Use one stable ID per example or anti-example.",
                        )
                    elif message_id is not None:
                        message_ids.add(message_id)
            validate_guidance_governance(
                value.get("governance"),
                f"{pointer}/governance",
                approvals,
                diagnostics,
            )

    localization = require_closed(
        document.get("localization"),
        VOICE_LOCALIZATION_KEYS,
        VOICE_LOCALIZATION_KEYS,
        f"{path_value}#/localization",
        diagnostics,
    )
    if localization is not None:
        validate_guidance_text_fields(
            localization,
            ("sourceLanguage", "fallback"),
            f"{path_value}#/localization",
            diagnostics,
        )
        if (
            not isinstance(localization.get("sourceLanguage"), str)
            or LANGUAGE_TAG.fullmatch(localization["sourceLanguage"]) is None
        ):
            diagnostic(
                diagnostics,
                "IDN1601",
                f"{path_value}#/localization/sourceLanguage",
                "source language tag is invalid",
                "Use a BCP 47-style language tag such as en-US.",
            )
        languages = localization.get("supportedLanguages")
        language_tags: set[str] = set()
        if not isinstance(languages, list) or not languages:
            diagnostic(
                diagnostics,
                "IDN1601",
                f"{path_value}#/localization/supportedLanguages",
                "at least one language coverage record is required",
                "Record the source language and every reviewed coverage level.",
            )
        else:
            for index, item in enumerate(languages):
                pointer = f"{path_value}#/localization/supportedLanguages/{index}"
                value = require_closed(
                    item,
                    VOICE_LANGUAGE_KEYS,
                    VOICE_LANGUAGE_KEYS,
                    pointer,
                    diagnostics,
                )
                if value is None:
                    continue
                tag = value.get("tag")
                if (
                    not isinstance(tag, str)
                    or LANGUAGE_TAG.fullmatch(tag) is None
                    or tag in language_tags
                ):
                    diagnostic(
                        diagnostics,
                        "IDN1601",
                        f"{pointer}/tag",
                        "language tag is invalid or duplicated",
                        "Use each BCP 47-style language tag once.",
                    )
                else:
                    language_tags.add(tag)
                if value.get("coverage") not in {"reviewed", "partial", "unsupported"}:
                    diagnostic(
                        diagnostics,
                        "IDN1601",
                        f"{pointer}/coverage",
                        "language coverage is unsupported",
                        "Use reviewed, partial, or unsupported.",
                    )
                if not isinstance(value.get("notes"), str):
                    diagnostic(
                        diagnostics,
                        "IDN1601",
                        f"{pointer}/notes",
                        "language notes must be a string",
                        "Use an empty or reviewed explanatory string.",
                    )
        validate_guidance_governance(
            localization.get("governance"),
            f"{path_value}#/localization/governance",
            approvals,
            diagnostics,
        )
    return context_ids


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
        if kind not in {"short", "long"} or kind in kinds:
            diagnostic(
                diagnostics,
                "IDN1801",
                pointer,
                "Press Kit boilerplate kind must be one unique short or long value",
                "Declare exactly one reviewed short boilerplate and one reviewed long boilerplate.",
            )
        elif isinstance(kind, str):
            kinds.add(kind)
    if kinds != {"short", "long"}:
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
                catalog_path.read_text(encoding="utf-8")
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


def validate_identity(repository_root: Path) -> list[Diagnostic]:
    """Return all v1 source violations without mutating repository state."""

    diagnostics: list[Diagnostic] = []
    identity_path = repository_root / ".identity/identity.json"
    project = load_json(identity_path, ".identity/identity.json", diagnostics)
    if project is None:
        return sorted(set(diagnostics))
    validate_project(project, repository_root, diagnostics)
    approvals = validate_approvals(project, repository_root, diagnostics)
    _, override_approvals = load_layers(project, repository_root, diagnostics)
    for approval_id, token_path in override_approvals:
        decision = approvals.get(approval_id)
        if (
            decision is None
            or decision.get("status") != "approved"
            or decision.get("subject") != f"token:{token_path}"
        ):
            diagnostic(
                diagnostics,
                "IDN1404",
                f"approval:{approval_id}",
                "token override does not resolve to an approved decision",
                "Add or correct the linked human approval record.",
            )
    validate_provenance(project, repository_root, approvals, diagnostics)
    validate_targets(project, repository_root, diagnostics)
    validate_voice(project, repository_root, approvals, diagnostics)
    validate_usage(project, repository_root, approvals, diagnostics)
    validate_design_system(project, repository_root, approvals, diagnostics)
    validate_design_references(project, repository_root, approvals, diagnostics)
    validate_press_kit(project, repository_root, approvals, diagnostics)
    validate_social_surfaces(project, repository_root, approvals, diagnostics)
    return sorted(set(diagnostics))


def build_parser() -> argparse.ArgumentParser:
    """Build the stable standalone validator interface."""

    parser = argparse.ArgumentParser(
        description="Validate an Identity v1 source contract without network or mutation."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Consumer repository root containing .identity/identity.json.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Diagnostic output format.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run validation and return 0 for valid, 1 for invalid, or 2 for bad arguments."""

    arguments = build_parser().parse_args(argv)
    diagnostics = validate_identity(arguments.repository_root)
    result = {
        "schema": DIAGNOSTICS_SCHEMA,
        "valid": not diagnostics,
        "repository": str(arguments.repository_root),
        "diagnostics": [value.as_dict() for value in diagnostics],
    }
    if arguments.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif diagnostics:
        print(f"INVALID {arguments.repository_root}", file=sys.stderr)
        for value in diagnostics:
            print(
                f"- [{value.code}] {value.path}: {value.message} Recovery: {value.recovery}",
                file=sys.stderr,
            )
    else:
        print(f"VALID {arguments.repository_root}")
    return 1 if diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
