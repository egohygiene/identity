# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Golden, determinism, and authority evidence for design-system projections."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
RENDERER_PATH = SCRIPTS_ROOT / "render_design_system.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
EXPECTED = VALID_FIXTURE / "expected"
sys.path.insert(0, str(SCRIPTS_ROOT))
SPEC = importlib.util.spec_from_file_location("render_design_system", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def source_digests(repository_root: Path) -> dict[str, str]:
    """Return stable digests for all canonical source files."""

    identity_root = repository_root / ".identity"
    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(identity_root.rglob("*"))
        if path.is_file()
    }


class DesignSystemProjectionTests(unittest.TestCase):
    """Prove deterministic projections preserve their source and ownership boundaries."""

    def test_models_match_contracts_and_reviewed_golden_outputs(self) -> None:
        handbook, context = renderer.build_projections(VALID_FIXTURE)
        handbook_schema = json.loads(
            (REPOSITORY_ROOT / "contracts/v1/design-system-handbook.schema.json").read_text(
                encoding="utf-8"
            )
        )
        context_schema = json.loads(
            (REPOSITORY_ROOT / "contracts/v1/design-context.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(handbook), set(handbook_schema["required"]))
        self.assertEqual(set(context), set(context_schema["required"]))
        self.assertEqual(
            renderer.render((handbook, context), "handbook-json"),
            (EXPECTED / "design-system-handbook.json").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            renderer.render((handbook, context), "handbook-markdown"),
            (EXPECTED / "design-system-handbook.md").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            renderer.render((handbook, context), "context-json"),
            (EXPECTED / "design-context.json").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            renderer.render((handbook, context), "context-markdown"),
            (EXPECTED / "design-context.md").read_text(encoding="utf-8"),
        )

    def test_aliases_resolve_and_capability_ownership_stays_explicit(self) -> None:
        _, context = renderer.build_projections(VALID_FIXTURE)
        tokens = {item["path"]: item for item in context["tokens"]}
        self.assertEqual(tokens["color.action.primary"]["value"], tokens["color.brand.primary"]["value"])
        self.assertEqual(
            context["profiles"],
            [
                {"id": "core", "version": "1.0.0"},
                {"id": "metadata", "version": "1.0.0"},
                {"id": "tokens", "version": "1.0.0"},
            ],
        )
        self.assertEqual(
            context["capabilities"],
            [
                {
                    "id": "product-layout",
                    "status": "not-declared",
                    "owner": "consumer",
                    "notes": "Each product owns layout decisions while consuming approved identity constraints and bounded overrides.",
                },
                {
                    "id": "reusable-components",
                    "status": "not-declared",
                    "owner": "holon",
                    "notes": "Identity records component-facing constraints but does not define or distribute component implementations.",
                },
                {
                    "id": "semantic-tokens",
                    "status": "declared",
                    "owner": "identity",
                    "notes": "Identity owns the reviewed DTCG token source, inheritance evidence, and generated platform projections.",
                },
            ],
        )

    def test_projection_is_reproducible_and_never_mutates_canonical_source(self) -> None:
        before = source_digests(VALID_FIXTURE)
        first = renderer.build_projections(VALID_FIXTURE)
        second = renderer.build_projections(VALID_FIXTURE)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["source"]["digest"], first[1]["source"]["digest"])
        self.assertEqual(source_digests(VALID_FIXTURE), before)

    def test_explicit_output_directory_writes_all_artifacts_and_refuses_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            before = source_digests(repository)
            projections = renderer.build_projections(repository)
            written = renderer.write_outputs(
                repository,
                Path("assets/identity/design-system"),
                projections,
            )
            self.assertEqual(
                [path.name for path in written],
                [
                    "design-system-handbook.json",
                    "design-system-handbook.md",
                    "design-context.json",
                    "design-context.md",
                ],
            )
            first = {path.name: path.read_bytes() for path in written}
            renderer.write_outputs(repository, Path("assets/identity/design-system"), projections)
            self.assertEqual(first, {path.name: path.read_bytes() for path in written})
            self.assertEqual(source_digests(repository), before)
            with self.assertRaisesRegex(renderer.ProjectionError, "canonical .identity"):
                renderer.write_outputs(repository, Path(".identity/design-system"), projections)

    def test_projection_requires_adopted_handbook_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            identity_path = repository / ".identity/identity.json"
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            del identity["documents"]["handbook"]
            identity_path.write_text(f"{json.dumps(identity, indent=2)}\n", encoding="utf-8")
            with self.assertRaisesRegex(renderer.ProjectionError, "requires documents.handbook"):
                renderer.build_projections(repository)

    def test_organization_level_handbook_uses_the_same_reviewed_source_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "organization"
            shutil.copytree(VALID_FIXTURE, repository)
            identity_path = repository / ".identity/identity.json"
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            identity["project"]["id"] = "example-organization"
            identity["project"]["displayName"] = "Example Organization"
            identity["project"]["repository"] = "https://example.invalid/example-organization"
            identity["project"]["kind"] = "organization"
            identity_path.write_text(f"{json.dumps(identity, indent=2)}\n", encoding="utf-8")

            handbook, context = renderer.build_projections(repository)
            self.assertEqual(handbook["project"]["kind"], "organization")
            self.assertEqual(context["project"]["kind"], "organization")
            self.assertEqual(
                handbook["inheritance"]["organizationLayers"], ["example-organization"]
            )

    def test_cli_prints_one_format_or_writes_all_artifacts(self) -> None:
        context = subprocess.run(
            [
                sys.executable,
                str(RENDERER_PATH),
                "--repository-root",
                str(VALID_FIXTURE),
                "--format",
                "context-json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(context.returncode, 0, context.stderr)
        self.assertEqual(json.loads(context.stdout)["schema"], renderer.CONTEXT_SCHEMA)
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            written = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--output-directory",
                    "assets/identity/design-system",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(written.returncode, 0, written.stderr)
            self.assertEqual(
                written.stdout.splitlines(),
                [
                    "assets/identity/design-system/design-system-handbook.json",
                    "assets/identity/design-system/design-system-handbook.md",
                    "assets/identity/design-system/design-context.json",
                    "assets/identity/design-system/design-context.md",
                ],
            )


if __name__ == "__main__":
    unittest.main()
