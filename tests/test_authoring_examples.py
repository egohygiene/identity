# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Executable authoring examples preserve source authority and approval checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
EXAMPLES_ROOT = REPOSITORY_ROOT / "examples/v1"
sys.path.insert(0, str(SCRIPTS_ROOT))

import render_guidance as guidance_renderer
import render_press_kit as press_renderer
import validate_identity as validator


def source_digests(repository_root: Path) -> dict[str, str]:
    """Bind every example source byte before exercising projection commands."""

    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((repository_root / ".identity").rglob("*"))
        if path.is_file()
    }


def load_json(path: Path) -> dict[str, object]:
    """Read one checked-in example source document."""

    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, document: object) -> None:
    """Write a deliberate negative mutation only inside a disposable consumer."""

    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


class AuthoringExampleTests(unittest.TestCase):
    """Prove the examples execute without creating source facts or authority."""

    def test_both_authoring_examples_validate_with_local_schema_references(self) -> None:
        for name in ("minimal", "expanded"):
            with self.subTest(example=name):
                repository = EXAMPLES_ROOT / name
                self.assertEqual(validator.validate_identity(repository), [])
                for path in sorted((repository / ".identity").rglob("*.json")):
                    schema_path = path.parent / load_json(path)["$schema"]
                    self.assertTrue(schema_path.resolve().is_file(), path)

    def test_minimal_public_guidance_is_absent_without_requiring_optional_sources(self) -> None:
        repository = EXAMPLES_ROOT / "minimal"
        source = load_json(repository / ".identity/identity.json")
        self.assertEqual(source["documents"]["guidance"], {"voice": None, "usage": None})
        for optional in (
            "handbook", "pressKit", "mascot", "channelRegistry", "socialSurfaces",
            "repositoryPresentation",
        ):
            self.assertNotIn(optional, source["documents"])
        before = source_digests(repository)
        projection = guidance_renderer.build_view_model(repository, audience="public")
        self.assertIsNone(projection["foundation"])
        self.assertEqual(projection["contexts"], [])
        self.assertEqual(projection["downloads"], [])
        self.assertIsNone(projection["legal"])
        self.assertEqual(source_digests(repository), before)

    def test_expanded_projects_canonical_copy_and_public_artwork_without_source_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(EXAMPLES_ROOT / "expanded", repository)
            before = source_digests(repository)
            voice = load_json(repository / ".identity/guidance/voice.json")
            press_source = load_json(repository / ".identity/guidance/press-kit.json")
            guidance = guidance_renderer.build_view_model(repository, audience="public")
            self.assertEqual(guidance["foundation"], voice["foundation"])
            self.assertEqual([asset["id"] for asset in guidance["downloads"]], ["mark"])

            model, assets = press_renderer.build_projection(repository)
            self.assertEqual(
                {record["kind"]: record["text"] for record in model["boilerplates"]},
                {record["kind"]: record["text"] for record in press_source["boilerplates"]},
            )
            self.assertEqual(model["contacts"][0]["value"], "press@example.invalid")
            for asset in model["assets"]:
                self.assertEqual(
                    hashlib.sha256(assets[asset["downloadPath"]]).hexdigest(), asset["sha256"]
                )
            payload = press_renderer.build_package(model, assets)
            self.assertEqual(payload, press_renderer.build_package(*press_renderer.build_projection(repository)))
            press_renderer.write_outputs(repository, Path("assets/identity/press-kit"), payload)
            self.assertEqual(source_digests(repository), before)

            # Exercise the user-facing optional command at the actual example shape.
            result = subprocess.run(
                [
                    sys.executable, str(SCRIPTS_ROOT / "render_guidance.py"),
                    "--repository-root", str(repository), "--audience", "public", "--format", "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), guidance)
            self.assertEqual(source_digests(repository), before)

    def test_minimal_still_rejects_missing_artwork_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(EXAMPLES_ROOT / "minimal", repository)
            path = repository / ".identity/governance/approvals.json"
            approvals = load_json(path)
            approvals["decisions"] = []
            write_json(path, approvals)
            diagnostics = validator.validate_identity(repository)
            self.assertIn("IDN1404", {diagnostic.code for diagnostic in diagnostics})

    def test_optional_guidance_path_is_not_a_license_to_ignore_bad_declarations(self) -> None:
        for value in (".identity/guidance/missing.json", 42, "../voice.json"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(EXAMPLES_ROOT / "minimal", repository)
                path = repository / ".identity/identity.json"
                project = load_json(path)
                project["documents"]["guidance"]["voice"] = value
                write_json(path, project)
                diagnostics = validator.validate_identity(repository)
                self.assertIn("IDN1003", {diagnostic.code for diagnostic in diagnostics})


if __name__ == "__main__":
    unittest.main()
