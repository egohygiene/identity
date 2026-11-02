# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal voice validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from pathlib import Path
from typing import Any
from .common import (
    Diagnostic,
    IDENTIFIER,
    LANGUAGE_TAG,
    VOICE_CHARACTERISTIC_KEYS,
    VOICE_CONTEXT_KEYS,
    VOICE_FOUNDATION_KEYS,
    VOICE_LANGUAGE_KEYS,
    VOICE_LOCALIZATION_KEYS,
    VOICE_MESSAGE_KEYS,
    VOICE_ROOT_KEYS,
    VOICE_SCHEMA,
    diagnostic,
    load_json,
    require_closed,
    resolve_local_path,
)
from .guidance import validate_guidance_governance, validate_guidance_strings, validate_guidance_text_fields


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
    if path_value is None:
        return set()
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
