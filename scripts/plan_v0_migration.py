#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Plan a reviewable Identity project/v0 to project/v1 migration without writing it."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tomllib
from typing import Any, Sequence


def sha256(path: Path) -> str:
    """Return one local file's lowercase SHA-256 digest."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan_migration(repository_root: Path) -> dict[str, Any]:
    """Return a deterministic, non-mutating migration plan for one v0 source."""

    specification_path = repository_root / ".identity/identity.toml"
    specification = tomllib.loads(specification_path.read_text(encoding="utf-8"))
    if specification.get("schema") != "identity.project/v0":
        raise ValueError("source schema must be identity.project/v0")

    brief_path = repository_root / specification["paths"]["brief"]
    required_sources = [
        {
            "role": source["role"],
            "path": source["path"],
            "format": source["format"],
            "description": source["description"],
        }
        for source in specification["sources"]["required"]
    ]
    return {
        "schema": "identity.migration-plan/v1",
        "source": {
            "schema": "identity.project/v0",
            "path": ".identity/identity.toml",
            "sha256": sha256(specification_path),
        },
        "target": {
            "schema": "identity.project/v1",
            "path": ".identity-v1/identity.json",
            "promotionPath": ".identity/identity.json",
        },
        "preserved": {
            "project": {
                "id": specification["project"]["id"],
                "displayName": specification["project"]["display_name"],
                "repository": specification["project"]["repository"],
                "tagline": specification["project"]["tagline"],
            },
            "brief": {
                "path": specification["paths"]["brief"],
                "sha256": sha256(brief_path),
            },
            "enabledProfiles": specification["profiles"]["enabled"],
            "inapplicableProfiles": specification["profiles"].get("inapplicable", []),
            "requiredSources": required_sources,
            "contextFiles": specification.get("context", {}).get("files", []),
        },
        "actions": [
            {
                "id": "create-v1-topology",
                "status": "ready",
                "authority": "migration-tool",
                "reason": "Create a separate review workspace without replacing v0 source.",
            },
            {
                "id": "pin-organization-defaults",
                "status": "requires-human-review",
                "authority": "consumer-maintainer",
                "reason": "v0 did not record an immutable organization-default token layer.",
            },
            {
                "id": "convert-palette-to-dtcg",
                "status": "requires-human-review",
                "authority": "consumer-maintainer",
                "reason": (
                    "v0 declared a palette source role but not reviewed DTCG "
                    "semantic tokens."
                ),
            },
            {
                "id": "record-license-provenance-and-approval",
                "status": "requires-human-review",
                "authority": "consumer-maintainer",
                "reason": (
                    "v0 source requirements did not prove license, byte provenance, "
                    "or approval records."
                ),
            },
            {
                "id": "structure-voice-and-usage",
                "status": "requires-human-review",
                "authority": "consumer-maintainer",
                "reason": (
                    "v0 narrative intent requires human structuring into versioned voice "
                    "and usage guidance."
                ),
            },
            {
                "id": "validate-and-compare",
                "status": "blocked",
                "authority": "identity-validator",
                "reason": (
                    "Run v1 validation and compare profile/plan evidence after "
                    "review actions complete."
                ),
            },
            {
                "id": "promote-v1",
                "status": "blocked",
                "authority": "consumer-maintainer",
                "reason": "Promotion requires human approval and a verified rollback anchor.",
            },
        ],
        "rollback": {
            "anchor": ".identity/identity.toml",
            "rule": "Keep v0 source and its last generated outputs until v1 promotion is accepted.",
        },
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the stable migration-planning command interface."""

    parser = argparse.ArgumentParser(
        description="Plan an Identity project/v0 to project/v1 migration without writing files."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Consumer repository containing .identity/identity.toml.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Migration-plan output format.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Render a plan or return a stable failure status."""

    arguments = build_parser().parse_args(argv)
    try:
        plan = plan_migration(arguments.repository_root)
    except (
        OSError,
        UnicodeError,
        tomllib.TOMLDecodeError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        print(f"error: cannot plan migration: {error}", file=sys.stderr)
        return 1
    if arguments.format == "json":
        print(json.dumps(plan, indent=2))
    else:
        print("Identity v0 → v1 migration plan")
        print(f"Source: {plan['source']['path']} ({plan['source']['sha256']})")
        print(f"Review workspace: {plan['target']['path']}")
        for action in plan["actions"]:
            print(f"- [{action['status']}] {action['id']}: {action['reason']}")
        print(f"Rollback: {plan['rollback']['rule']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
