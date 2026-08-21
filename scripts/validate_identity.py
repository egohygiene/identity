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
DOCUMENT_KEYS = {"brief", "targets", "provenance", "approvals", "guidance"}
GUIDANCE_KEYS = {"voice", "usage"}
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
APPROVAL_KEYS = {"id", "subject", "status", "reviewedBy", "reviewedAt", "evidence", "notes"}
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
IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
HTTPS_URL = re.compile(r"^https://[^\s]+$")
ALIAS = re.compile(r"^\{([A-Za-z0-9_.-]+)\}$")
EXTENSION_NAME = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9-]+)+$")


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
        project.get("documents"), DOCUMENT_KEYS, DOCUMENT_KEYS, "/documents", diagnostics
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
                if guidance.get(field) is not None:
                    resolve_local_path(
                        repository_root,
                        guidance[field],
                        f"/documents/guidance/{field}",
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
        for field in ("subject", "reviewedBy", "evidence"):
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
    profile_root = Path(__file__).resolve().parents[1] / "profiles"
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
        profile_path = profile_root / f"{identifier}.json"
        if not profile_path.is_file():
            diagnostic(
                diagnostics,
                "IDN1501",
                pointer,
                f"profile is not available: {identifier}@{version}",
                "Install or select a profile shipped by this Identity version.",
            )
            continue
        available = load_json(profile_path, str(profile_path), diagnostics)
        if available is not None and available.get("version") != version:
            diagnostic(
                diagnostics,
                "IDN1501",
                f"{pointer}/version",
                f"selected {version}, available {available.get('version')}",
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
