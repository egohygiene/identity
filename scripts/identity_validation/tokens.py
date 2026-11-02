# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal tokens validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import (
    ALIAS,
    CONTRAST_EXTENSION_KEYS,
    Diagnostic,
    EXTENSION_NAME,
    GROUP_METADATA,
    IDENTIFIER,
    IDENTITY_EXTENSION,
    IDENTITY_EXTENSION_KEYS,
    LAYER_EXTENSION_KEYS,
    LAYER_KEYS,
    MOTION_EXTENSION_KEYS,
    OVERRIDE_EXTENSION_KEYS,
    PROVENANCE_EXTENSION_KEYS,
    SHA256,
    TOKENS_SCHEMA,
    TOKEN_METADATA,
    TOKEN_TYPES,
    TYPOGRAPHY_EXTENSION_KEYS,
    TokenRecord,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
    sha256,
)


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
