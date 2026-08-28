# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Determinism, authority, and package evidence for Press Kit projections."""

from __future__ import annotations

from io import BytesIO
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
RENDERER_PATH = SCRIPTS_ROOT / "render_press_kit.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
sys.path.insert(0, str(SCRIPTS_ROOT))
SPEC = importlib.util.spec_from_file_location("render_press_kit", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    """Write stable JSON fixture material."""

    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def source_digests(repository_root: Path) -> dict[str, str]:
    """Return local canonical source checksums for mutation evidence."""

    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((repository_root / ".identity").rglob("*"))
        if path.is_file()
    }


def approval(identifier: str, subject: str) -> dict[str, object]:
    """Return a reviewed approval matching one public Press Kit record."""

    return {
        "id": identifier,
        "subject": subject,
        "candidate": f"press-kit:{identifier}/v1",
        "status": "approved",
        "reviewedBy": "example-maintainer",
        "reviewedAt": "2026-08-28T18:00:00Z",
        "evidence": f"https://example.invalid/reviews/{identifier}",
        "supersedes": None,
        "notes": "Approved for the public Press Kit fixture.",
    }


def governance(subject: str, identifier: str | None) -> dict[str, object]:
    """Return governed public source metadata for a fixture record."""

    return {
        "subject": subject,
        "state": "approved" if identifier else "candidate",
        "visibility": "public" if identifier else "internal",
        "provenance": {
            "method": "human-authored" if identifier else "handoff-candidate",
            "source": ".identity/brief.md",
            "capturedAt": "2026-08-28T18:00:00Z",
        },
        "approval": identifier,
    }


def add_press_source(repository_root: Path) -> None:
    """Add a complete governed Press Kit source to a copied base fixture."""

    identity_path = repository_root / ".identity/identity.json"
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    identity["documents"]["pressKit"] = ".identity/guidance/press-kit.json"
    write_json(identity_path, identity)
    approvals_path = repository_root / ".identity/governance/approvals.json"
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    decisions = [
        approval("approve-press-short", "press-kit:boilerplate:short"),
        approval("approve-press-long", "press-kit:boilerplate:long"),
        approval("approve-press-founded", "press-kit:fact:founded"),
        approval("approve-press-website", "press-kit:link:website"),
        approval("approve-press-contact", "press-kit:contact:media"),
        approval("approve-press-founder", "press-kit:team:founder"),
        approval("approve-press-mark", "press-kit:asset:mark"),
    ]
    approvals["decisions"].extend(decisions)
    write_json(approvals_path, approvals)
    press = {
        "$schema": "../../../../../contracts/v1/press-kit.schema.json",
        "schema": "identity.press-kit-source/v1",
        "boilerplates": [
            {
                "id": "short",
                "kind": "short",
                "text": "Example Product turns reviewed identity intent into reusable, deterministic artifacts.",
                "governance": governance("press-kit:boilerplate:short", "approve-press-short"),
            },
            {
                "id": "long",
                "kind": "long",
                "text": "Example Product is a local-first Identity workflow for maintainers who need approved tokens, assets, and guidance without splitting brand truth across hand-maintained folders.",
                "governance": governance("press-kit:boilerplate:long", "approve-press-long"),
            },
        ],
        "facts": [
            {
                "id": "founded",
                "label": "Availability",
                "value": "Open source and available to repository maintainers.",
                "governance": governance("press-kit:fact:founded", "approve-press-founded"),
            },
            {
                "id": "candidate-fact",
                "label": "Candidate claim",
                "value": "This unreviewed claim must never be projected.",
                "governance": governance("press-kit:fact:candidate", None),
            },
        ],
        "links": [
            {
                "id": "website",
                "label": "Project repository",
                "url": "https://example.invalid/example-product",
                "kind": "repository",
                "governance": governance("press-kit:link:website", "approve-press-website"),
            }
        ],
        "contacts": [
            {
                "id": "media",
                "label": "Media contact",
                "kind": "email",
                "value": "press@example.invalid",
                "notes": "Please include the requested publication date and deadline.",
                "governance": governance("press-kit:contact:media", "approve-press-contact"),
            }
        ],
        "team": [
            {
                "id": "founder",
                "name": "Example Maintainer",
                "role": "Project maintainer",
                "bio": "Maintains the reviewed source and release boundaries for Example Product.",
                "governance": governance("press-kit:team:founder", "approve-press-founder"),
            }
        ],
        "assets": [
            {
                "id": "mark",
                "assetId": "mark",
                "label": "Primary mark",
                "notes": "Use with the accompanying approved usage guidance.",
                "governance": governance("press-kit:asset:mark", "approve-press-mark"),
            }
        ],
    }
    write_json(repository_root / ".identity/guidance/press-kit.json", press)


class PressKitProjectionTests(unittest.TestCase):
    """Prove source authority, deterministic packaging, and honest optional material."""

    def test_projection_requires_opt_in_source(self) -> None:
        with self.assertRaisesRegex(renderer.ProjectionError, "documents.pressKit"):
            renderer.build_projection(VALID_FIXTURE)

    def test_projection_filters_unapproved_material_and_matches_contract_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            model, assets = renderer.build_projection(repository)
            schema = json.loads(
                (REPOSITORY_ROOT / "contracts/v1/press-kit-projection.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(set(model), set(schema["required"]))
            self.assertEqual([value["kind"] for value in model["boilerplates"]], ["long", "short"])
            self.assertEqual([value["id"] for value in model["facts"]], ["founded"])
            self.assertEqual(model["contacts"][0]["value"], "press@example.invalid")
            self.assertEqual(model["assets"][0]["downloadPath"], "assets/example-product-mark.svg")
            self.assertEqual(
                hashlib.sha256(assets["assets/example-product-mark.svg"]).hexdigest(),
                model["assets"][0]["sha256"],
            )
            self.assertEqual(model["project"]["kind"], "product")
            self.assertEqual(model["inheritance"]["organizationLayers"], ["example-organization"])

    def test_package_is_reproducible_and_contains_manifested_public_material_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            model, assets = renderer.build_projection(repository)
            first = renderer.build_package(model, assets)
            second = renderer.build_package(*renderer.build_projection(repository))
            self.assertEqual(first, second)
            self.assertEqual(source_digests(repository), before)
            manifest = json.loads(first["press-kit-manifest.json"])
            self.assertEqual(manifest["schema"], renderer.PACKAGE_SCHEMA)
            self.assertNotIn("press-kit.zip", manifest["files"])
            with zipfile.ZipFile(BytesIO(first["press-kit.zip"])) as archive:
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
                self.assertIn("press-kit.json", archive.namelist())
                self.assertIn("assets/example-product-mark.svg", archive.namelist())
                exported = json.loads(archive.read("press-kit.json"))
            self.assertEqual([value["id"] for value in exported["facts"]], ["founded"])

    def test_generated_output_cannot_mutate_or_enter_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            written = renderer.write_outputs(repository, Path("assets/identity/press-kit"), payload)
            self.assertEqual([path.relative_to(repository).as_posix() for path in written], sorted(
                path.relative_to(repository).as_posix() for path in written
            ))
            self.assertEqual(source_digests(repository), before)
            with self.assertRaisesRegex(renderer.ProjectionError, "canonical .identity"):
                renderer.write_outputs(repository, Path(".identity/press-kit"), payload)
            with self.assertRaisesRegex(renderer.ProjectionError, "normalized"):
                renderer.write_outputs(repository, Path("../outside"), payload)
            redirect = repository / "generated-redirect"
            redirect.symlink_to(repository / ".identity", target_is_directory=True)
            with self.assertRaisesRegex(renderer.ProjectionError, "symbolic link"):
                renderer.write_outputs(repository, Path("generated-redirect/press-kit"), payload)

    def test_validator_rejects_nonpublic_asset_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            press_path = repository / ".identity/guidance/press-kit.json"
            press = json.loads(press_path.read_text(encoding="utf-8"))
            press["assets"][0]["assetId"] = "legacy-wordmark"
            write_json(press_path, press)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1801", {value.code for value in diagnostics})

    def test_organization_projection_uses_same_inheritance_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "organization"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            identity_path = repository / ".identity/identity.json"
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            identity["project"]["id"] = "example-organization"
            identity["project"]["displayName"] = "Example Organization"
            identity["project"]["repository"] = "https://example.invalid/example-organization"
            identity["project"]["kind"] = "organization"
            write_json(identity_path, identity)
            model, _ = renderer.build_projection(repository)
            self.assertEqual(model["project"]["kind"], "organization")
            self.assertEqual(model["inheritance"]["organizationLayers"], ["example-organization"])

    def test_cli_prints_one_format_or_writes_complete_package(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            printed = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--format",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(printed.returncode, 0, printed.stderr)
            self.assertEqual(json.loads(printed.stdout)["schema"], renderer.PRESS_KIT_SCHEMA)
            written = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--output-directory",
                    "assets/identity/press-kit",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(written.returncode, 0, written.stderr)
            self.assertIn("assets/identity/press-kit/press-kit.zip", written.stdout.splitlines())


if __name__ == "__main__":
    unittest.main()
