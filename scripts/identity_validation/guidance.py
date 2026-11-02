# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal guidance validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
from datetime import datetime
from typing import Any, Sequence
from .common import (
    Diagnostic,
    GOVERNANCE_KEYS,
    GUIDANCE_PROVENANCE_KEYS,
    GUIDANCE_STATES,
    diagnostic,
    require_closed,
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
