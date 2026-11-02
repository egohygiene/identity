# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Canonical internal entrypoint validation; bundled offline by build_identity_validator.py."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from typing import Sequence
from .common import (
    DIAGNOSTICS_SCHEMA,
    Diagnostic,
    SourceSnapshot,
    _SOURCE_SNAPSHOT,
    canonical_source_files,
    diagnostic,
    load_json,
)
from .channels import validate_channel_registry
from .governance import validate_approvals, validate_provenance
from .handbook import validate_design_references, validate_design_system
from .mascot import validate_mascot
from .press_kit import validate_press_kit
from .project import validate_project
from .repository_presentation import validate_repository_presentation
from .social_surfaces import validate_social_surfaces
from .targets import validate_targets
from .tokens import load_layers
from .usage import validate_usage
from .voice import validate_voice


def validate_identity(repository_root: Path) -> list[Diagnostic]:
    """Return all v1 source violations without mutating repository state."""

    diagnostics: list[Diagnostic] = []
    try:
        canonical_source_files(repository_root)
    except (OSError, ValueError) as error:
        diagnostic(diagnostics, "IDN1003", ".identity", str(error),
                   "Restore regular local source files with portable paths and rerun validation.")
        return diagnostics
    identity_path = repository_root / ".identity/identity.json"
    if identity_path.is_symlink() or identity_path.parent.is_symlink():
        diagnostic(diagnostics, "IDN1003", ".identity/identity.json",
                   "source path may not traverse a symbolic link",
                   "Replace the symbolic link with repository-owned local content.")
        return diagnostics
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
    validate_channel_registry(project, repository_root, approvals, diagnostics)
    validate_press_kit(project, repository_root, approvals, diagnostics)
    validate_social_surfaces(project, repository_root, approvals, diagnostics)
    validate_repository_presentation(project, repository_root, approvals, diagnostics)
    validate_mascot(project, repository_root, approvals, diagnostics)
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
    parser.add_argument(
        "--snapshot", action="store_true",
        help="Include the validated file digests and directory paths in JSON output.",
    )
    return parser


def validate_snapshot(repository_root: Path) -> tuple[list[Diagnostic], SourceSnapshot]:
    """Validate and bind the result to every consulted local source, without writes."""

    snapshot = SourceSnapshot(repository_root)
    token = _SOURCE_SNAPSHOT.set(snapshot)
    try:
        diagnostics = validate_identity(snapshot.root)
        snapshot.verify()
    except (OSError, ValueError) as error:
        diagnostics = []
        diagnostic(diagnostics, "IDN1003", ".identity", str(error),
                   "Restore stable, regular local source files and rerun preflight.")
    finally:
        _SOURCE_SNAPSHOT.reset(token)
    return diagnostics, snapshot


def main(argv: Sequence[str] | None = None) -> int:
    """Run validation and return 0 for valid, 1 for invalid, or 2 for bad arguments."""

    arguments = build_parser().parse_args(argv)
    snapshot = None
    if arguments.snapshot:
        diagnostics, snapshot = validate_snapshot(arguments.repository_root)
    else:
        diagnostics = validate_identity(arguments.repository_root)
    result = {
        "schema": DIAGNOSTICS_SCHEMA,
        "valid": not diagnostics,
        "repository": str(arguments.repository_root),
        "diagnostics": [value.as_dict() for value in diagnostics],
    }
    if snapshot is not None:
        result["snapshot"] = snapshot.as_dict()
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
