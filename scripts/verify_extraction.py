#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify the immutable Empathy-to-Identity source extraction manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPOSITORY_ROOT / "migration/empathy-extraction-v1.json"


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    """Validate every copied file and the preserved profile inventory."""

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    copied = [
        entry for entry in manifest["entries"] if entry["disposition"] == "copied-byte-for-byte"
    ]
    for entry in copied:
        destination = REPOSITORY_ROOT / entry["destination"]
        if not destination.is_file():
            errors.append(f"missing extracted file: {entry['destination']}")
            continue
        actual = sha256(destination)
        if actual != entry["sha256"]:
            errors.append(
                f"digest mismatch for {entry['destination']}: "
                f"expected {entry['sha256']}, got {actual}"
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
    print(
        f"VALID Empathy extraction: {len(copied)} byte-identical files, "
        f"{len(profiles)} profiles, {target_count} targets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
