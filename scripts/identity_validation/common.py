#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Validate a local Identity v1 source contract without mutation or network access."""

from __future__ import annotations

import argparse  # noqa: F401 - standalone bundle prelude
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from typing import Any, Sequence


class SourceSnapshot:
    """Capture the local inputs actually consulted by authoritative preflight."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self.files: dict[str, str] = {}
        self.directories: set[str] = set()

    def relative(self, path: Path) -> str:
        relative = path.absolute().relative_to(self.root).as_posix()
        if not valid_relative_path(relative):
            raise OSError(f"invalid source path: {relative}")
        current = self.root
        for part in relative.split("/"):
            current /= part
            if current.is_symlink():
                raise OSError(f"source path traverses a symbolic link: {relative}")
        return relative

    def read(self, path: Path) -> bytes:
        relative = self.relative(path)
        if not path.is_file():
            raise OSError(f"source is not a regular file: {relative}")
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if self.files.setdefault(relative, digest) != digest:
            raise OSError(f"source changed during preflight: {relative}")
        return content

    def verify(self) -> None:
        for relative in list(self.files):
            self.read(self.root / relative)
        for relative in self.directories:
            path = self.root / relative
            self.relative(path)
            if not path.is_dir():
                raise OSError(f"source directory changed during preflight: {relative}")

    def as_dict(self) -> dict[str, Any]:
        return {"files": self.files, "directories": sorted(self.directories)}


_SOURCE_SNAPSHOT: ContextVar[SourceSnapshot | None] = ContextVar(
    "identity_source_snapshot", default=None
)


def read_source_bytes(path: Path) -> bytes:
    snapshot = _SOURCE_SNAPSHOT.get()
    return snapshot.read(path) if snapshot is not None else path.read_bytes()

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
CHANNEL_REGISTRY_SOURCE_SCHEMA = "identity.channel-registry-source/v1"
REPOSITORY_PRESENTATION_SOURCE_SCHEMA = "identity.repository-presentation-source/v1"
MASCOT_SCHEMA = "identity.mascot-source/v1"
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
DOCUMENT_KEYS = {
    *DOCUMENT_REQUIRED_KEYS,
    "handbook",
    "pressKit",
    "socialSurfaces",
    "channelRegistry",
    "repositoryPresentation",
    "mascot",
}
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
CHANNEL_REGISTRY_ROOT_KEYS = {"$schema", "schema", "registry", "security", "channels"}
CHANNEL_REGISTRY_METADATA_KEYS = {"id", "version", "owner", "reviewedAt"}
CHANNEL_REGISTRY_SECURITY_KEYS = {
    "secretsStored",
    "ownerReferenceKind",
    "procedureLocation",
}
CHANNEL_KEYS = {
    "id",
    "platform",
    "canonicalUrl",
    "handle",
    "ownershipEntity",
    "verification",
    "lifecycle",
    "audiencePurpose",
    "contentScope",
    "locale",
    "accessibility",
    "recoveryOwner",
    "badge",
    "governance",
}
CHANNEL_PLATFORM_KEYS = {"id", "label"}
CHANNEL_VERIFICATION_KEYS = {"state", "evidence"}
CHANNEL_LIFECYCLE_KEYS = {"state", "since", "notes"}
CHANNEL_ACCESSIBILITY_KEYS = {"label", "contactNotes"}
CHANNEL_BADGE_KEYS = {"approved", "label", "icon"}
CHANNEL_ICON_KEYS = {"id", "source", "license"}
REPOSITORY_PRESENTATION_ROOT_KEYS = {
    "$schema",
    "schema",
    "profile",
    "organizationDefault",
    "project",
}
REPOSITORY_PRESENTATION_PROFILE_KEYS = {
    "path",
    "id",
    "version",
    "status",
    "owner",
    "repository",
    "commit",
    "digest",
}
REPOSITORY_PRESENTATION_SELECTION_KEYS = {
    "bannerAssetId",
    "altText",
    "fallbackText",
    "license",
    "bannerApproval",
    "badgeApproval",
}
REPOSITORY_PRESENTATION_PROJECT_KEYS = {"visibility", "override"}
REPOSITORY_PRESENTATION_OVERRIDE_KEYS = {
    "bannerAssetId",
    "altText",
    "reason",
    "approval",
}
MASCOT_ROOT_KEYS = {
    "$schema",
    "schema",
    "id",
    "name",
    "pronouns",
    "role",
    "status",
    "character",
    "meanings",
    "canonicalAsset",
    "variants",
    "accessibility",
    "usage",
    "motion",
    "license",
    "approval",
}
MASCOT_CHARACTER_KEYS = {
    "archetype",
    "traits",
    "silhouette",
    "face",
    "eyes",
    "outfit",
    "emblem",
    "prohibitedElements",
}
MASCOT_EYE_KEYS = {"count", "treatment"}
MASCOT_EMBLEM_KEYS = {"placement", "integrated"}
MASCOT_MEANING_KEYS = {"id", "element", "meaning"}
MASCOT_ASSET_KEYS = {"assetId", "path", "sha256", "mediaType"}
MASCOT_VARIANT_KEYS = {"id", "role", "aspectRatio", "crop", "minimumWidth", "altText"}
MASCOT_ACCESSIBILITY_KEYS = {"altText", "decorativeAlt", "neverSoleCarrier"}
MASCOT_USAGE_KEYS = {"safeZone", "backgrounds", "do", "dont"}
MASCOT_MOTION_KEYS = {"status", "default", "reducedMotion", "restrictions"}
MASCOT_LICENSE_KEYS = {"spdx", "attribution", "trademark"}
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
        or ":" in value
        or "\x00" in value
    ):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def valid_canonical_source_path(value: str) -> bool:
    """Match the compiler's portable path rules for digest inventory entries."""

    if not valid_relative_path(value) or any(
        ord(character) < 0x20
        or 0x7F <= ord(character) <= 0x9F
        or 0xD800 <= ord(character) <= 0xDFFF
        or character in '\\:*?"<>|'
        for character in value
    ):
        return False
    ascii_upper = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {
        f"{prefix}{suffix}" for prefix in ("COM", "LPT") for suffix in "123456789¹²³"
    }
    return all(
        not part.endswith((".", " ")) and part.split(".", 1)[0].translate(ascii_upper) not in reserved
        for part in value.split("/")
    )


def canonical_source_files(repository_root: Path) -> list[Path]:
    """Inventory egohygiene.identity.source-digest/v1 without following excluded entries or links."""

    def is_link(metadata: os.stat_result) -> bool:
        return stat.S_ISLNK(metadata.st_mode) or bool(
            getattr(metadata, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        )

    identity_root = repository_root / ".identity"
    metadata = identity_root.lstat()
    if is_link(metadata) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("canonical .identity source must be a local directory")
    files = []

    def visit(directory: Path) -> None:
        for path in directory.iterdir():
            relative = path.relative_to(identity_root)
            # Match the historical compiler exclusions before inspecting an entry.
            if path.name == "README.md" or (
                len(relative.parts) == 1
                and relative.parts[0] in {"identity.toml", "candidates", "references"}
            ):
                continue
            portable = path.relative_to(repository_root).as_posix()
            if not valid_canonical_source_path(portable):
                raise ValueError(f"invalid portable canonical source path: {portable}")
            metadata = path.lstat()
            if is_link(metadata):
                raise ValueError(f"canonical source traverses a symbolic link or reparse point: {portable}")
            if stat.S_ISDIR(metadata.st_mode):
                visit(path)
            elif stat.S_ISREG(metadata.st_mode):
                files.append(path)
            else:
                raise ValueError(f"canonical source is not a regular file or directory: {portable}")

    visit(identity_root)
    return sorted(files, key=lambda path: tuple(
        part.encode("utf-8") for part in path.relative_to(repository_root).parts
    ))


def canonical_source_digest(repository_root: Path) -> str:
    """Hash the ordered inventory using the historical v1 NUL byte framing."""

    digest = hashlib.sha256()
    for path in canonical_source_files(repository_root):
        digest.update(path.relative_to(repository_root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(read_source_bytes(path))
        digest.update(b"\0")
    return digest.hexdigest()


def load_json(path: Path, pointer: str, diagnostics: list[Diagnostic]) -> dict[str, Any] | None:
    """Load a closed JSON object and normalize file failures into diagnostics."""

    try:
        value = json.loads(
            read_source_bytes(path).decode("utf-8"),
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
    snapshot = _SOURCE_SNAPSHOT.get()
    if snapshot is not None:
        if directory:
            snapshot.directories.add(snapshot.relative(candidate))
        else:
            snapshot.read(candidate)
    return candidate


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one local file."""

    return hashlib.sha256(read_source_bytes(path)).hexdigest()
