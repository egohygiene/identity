#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify the Empathy extraction baseline and intentional canonical evolution."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "migration/empathy-extraction-v1.json"
EVOLUTION_PATH = REPOSITORY_ROOT / "migration/empathy-extraction-evolution-v1.json"
EVOLUTION_SCHEMA = "identity.extraction-evolution/v1"
BASELINE_MANIFEST = "migration/empathy-extraction-v1.json"


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_sha256(value: object) -> bool:
    """Return whether a value is a lowercase SHA-256 digest."""

    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def load_evolution(errors: list[str]) -> dict[str, dict[str, object]]:
    """Load and strictly validate intentional post-extraction evolution records."""

    try:
        evolution = json.loads(EVOLUTION_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"cannot read extraction evolution registry: {error}")
        return {}

    if evolution.get("schema") != EVOLUTION_SCHEMA:
        errors.append(
            "extraction evolution schema differs: "
            f"expected {EVOLUTION_SCHEMA!r}, got {evolution.get('schema')!r}"
        )
    if evolution.get("baseline_manifest") != BASELINE_MANIFEST:
        errors.append(
            "extraction evolution baseline differs: "
            f"expected {BASELINE_MANIFEST!r}, got {evolution.get('baseline_manifest')!r}"
        )

    entries = evolution.get("entries")
    if not isinstance(entries, list):
        errors.append("extraction evolution entries must be an array")
        return {}

    evolved: dict[str, dict[str, object]] = {}
    for index, record in enumerate(entries):
        if not isinstance(record, dict):
            errors.append(f"extraction evolution entry {index} must be an object")
            continue
        destination = record.get("destination")
        if not isinstance(destination, str) or not destination:
            errors.append(f"extraction evolution entry {index} has no destination")
            continue
        if destination in evolved:
            errors.append(f"duplicate extraction evolution destination: {destination}")
            continue
        if not valid_sha256(record.get("baseline_sha256")):
            errors.append(f"invalid baseline digest for evolved file: {destination}")
        if not valid_sha256(record.get("current_sha256")):
            errors.append(f"invalid current digest for evolved file: {destination}")
        issue = record.get("issue")
        if not isinstance(issue, str) or not issue.startswith("https://github.com/"):
            errors.append(f"evolved file has no GitHub issue evidence: {destination}")
        reason = record.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"evolved file has no rationale: {destination}")
        evolved[destination] = record
    return evolved


def main() -> int:
    """Validate extracted files, explicit evolution, and preserved profile inventory."""

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    evolved = load_evolution(errors)
    copied = [
        entry for entry in manifest["entries"] if entry["disposition"] == "copied-byte-for-byte"
    ]
    copied_destinations = {entry["destination"] for entry in copied}

    for destination in sorted(set(evolved) - copied_destinations):
        errors.append(
            f"evolution record does not reference a byte-identical extraction entry: {destination}"
        )

    evolved_count = 0
    for entry in copied:
        destination_name = entry["destination"]
        destination = REPOSITORY_ROOT / destination_name
        if not destination.is_file():
            errors.append(f"missing extracted file: {destination_name}")
            continue

        expected = entry["sha256"]
        evolution = evolved.get(destination_name)
        if evolution is not None:
            evolved_count += 1
            if evolution.get("baseline_sha256") != expected:
                errors.append(
                    f"baseline digest mismatch in evolution record for {destination_name}: "
                    f"expected {expected}, got {evolution.get('baseline_sha256')}"
                )
            current_expected = evolution.get("current_sha256")
            if current_expected == expected:
                errors.append(
                    f"evolution record for {destination_name} does not differ from its baseline"
                )
        else:
            current_expected = expected

        actual = sha256(destination)
        if actual != current_expected:
            errors.append(
                f"digest mismatch for {destination_name}: "
                f"expected {current_expected}, got {actual}"
            )

    profiles = sorted((REPOSITORY_ROOT / "profiles").glob("*.json"))
    target_count = 0
    profile_ids: list[str] = []
    for path in profiles:
        profile = json.loads(path.read_text(encoding="utf-8"))
        profile_ids.append(profile["id"])
        target_count += len(profile["targets"])

    expected = manifest["profile_inventory"]
    if profile_ids != expected["ids"]:
        errors.append(f"profile inventory differs: {profile_ids!r}")
    if target_count != expected["target_count"]:
        errors.append(
            f"target inventory differs: expected {expected['target_count']}, got {target_count}"
        )

    if errors:
        print("INVALID Empathy extraction", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    untouched_count = len(copied) - evolved_count
    print(
        f"VALID Empathy extraction: {untouched_count} live byte-identical files, "
        f"{evolved_count} provenance-tracked evolved files, "
        f"{len(profiles)} profiles, {target_count} targets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
