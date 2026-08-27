# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Contract and adversarial evidence for the standalone Identity v1 validator."""

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
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts/validate_identity.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
INVALID_FIXTURES = REPOSITORY_ROOT / "tests/fixtures/v1/invalid"
SPEC = importlib.util.spec_from_file_location("validate_identity", VALIDATOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def write_json(path: Path, value: object) -> None:
    """Write deterministic fixture JSON."""

    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def resolve_pointer(document: object, pointer: str) -> tuple[object, str]:
    """Resolve a fixture mutation pointer to its parent and final segment."""

    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    current = document
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current, parts[-1]


def apply_mutation(repository: Path, mutation: dict[str, object]) -> None:
    """Apply one checked-in invalid-fixture operation."""

    path = repository / str(mutation["document"])
    document = json.loads(path.read_text(encoding="utf-8"))
    parent, key = resolve_pointer(document, str(mutation["pointer"]))
    operation = mutation["operation"]
    if operation == "remove":
        if isinstance(parent, list):
            parent.pop(int(key))
        else:
            del parent[key]
    elif operation in {"add", "replace"}:
        if isinstance(parent, list):
            parent[int(key)] = mutation["value"]
        else:
            parent[key] = mutation["value"]
    else:
        raise AssertionError(f"unsupported fixture operation: {operation}")
    write_json(path, document)


def refresh_layer_digests(repository: Path) -> None:
    """Keep semantic invalid fixtures focused on their named failure."""

    project_path = repository / ".identity/identity.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    for layer in project.get("layers", []):
        token_path = repository / layer["tokens"]
        layer["sha256"] = hashlib.sha256(token_path.read_bytes()).hexdigest()
    write_json(project_path, project)


class IdentityV1ValidatorTests(unittest.TestCase):
    """Prove closed schemas, deterministic layers, and governed assets."""

    def test_complete_v1_fixture_is_valid(self) -> None:
        self.assertEqual(validator.validate_identity(VALID_FIXTURE), [])

    def test_checked_in_invalid_fixtures_emit_stable_codes(self) -> None:
        for fixture_path in sorted(INVALID_FIXTURES.glob("*.json")):
            with (
                self.subTest(fixture=fixture_path.stem),
                tempfile.TemporaryDirectory() as temporary,
            ):
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
                self.assertEqual(fixture["schema"], "identity.invalid-fixture/v1")
                for mutation in fixture["mutations"]:
                    apply_mutation(repository, mutation)
                refresh_layer_digests(repository)

                diagnostics = validator.validate_identity(repository)
                codes = {value.code for value in diagnostics}
                self.assertTrue(
                    set(fixture["expectedCodes"]).issubset(codes),
                    f"{fixture_path.name}: {sorted(codes)}",
                )
                self.assertEqual(diagnostics, sorted(set(diagnostics)))

    def test_duplicate_json_keys_fail_before_semantic_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            (repository / ".identity/identity.json").write_text(
                '{"schema":"identity.project/v1","schema":"duplicate"}\n',
                encoding="utf-8",
            )

            diagnostics = validator.validate_identity(repository)
            self.assertIn("IDN1102", {value.code for value in diagnostics})

    def test_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            project_path = repository / ".identity/identity.json"
            project = json.loads(project_path.read_text(encoding="utf-8"))
            project["documents"]["brief"] = "../brief.md"
            write_json(project_path, project)

            diagnostics = validator.validate_identity(repository)
            self.assertIn("IDN1003", {value.code for value in diagnostics})

    def test_v1_schema_identities_and_diagnostic_contract_are_stable(self) -> None:
        schemas = {
            path.name: json.loads(path.read_text(encoding="utf-8"))
            for path in (REPOSITORY_ROOT / "contracts/v1").glob("*.json")
        }
        self.assertEqual(
            set(schemas),
            {
                "approvals.schema.json",
                "brand-guidance.schema.json",
                "brand-kit-checksums.schema.json",
                "brand-kit-package.schema.json",
                "brand-kit-view-model.schema.json",
                "compiler-manifest.schema.json",
                "compiler-plan.schema.json",
                "diagnostics.schema.json",
                "motion-policy.schema.json",
                "project.schema.json",
                "quality-report.schema.json",
                "provenance.schema.json",
                "targets.schema.json",
                "tokens.schema.json",
                "usage.schema.json",
                "visual-motion-manifest.schema.json",
                "voice.schema.json",
            },
        )
        self.assertEqual(
            schemas["voice.schema.json"]["properties"]["schema"]["const"],
            validator.VOICE_SCHEMA,
        )
        self.assertEqual(
            schemas["usage.schema.json"]["properties"]["schema"]["const"],
            validator.USAGE_SCHEMA,
        )
        self.assertEqual(
            schemas["brand-guidance.schema.json"]["properties"]["schema"]["const"],
            "identity.brand-guidance/v1",
        )
        self.assertEqual(
            schemas["project.schema.json"]["properties"]["schema"]["const"],
            validator.PROJECT_SCHEMA,
        )
        self.assertEqual(
            schemas["diagnostics.schema.json"]["properties"]["schema"]["const"],
            validator.DIAGNOSTICS_SCHEMA,
        )
        self.assertEqual(
            schemas["compiler-plan.schema.json"]["properties"]["schema"]["const"],
            "identity.compiler-plan/v1",
        )
        self.assertEqual(
            schemas["compiler-manifest.schema.json"]["properties"]["schema"]["const"],
            "identity.compiler-manifest/v1",
        )
        self.assertEqual(
            schemas["brand-kit-package.schema.json"]["properties"]["schema"]["const"],
            "identity.brand-kit-package/v1",
        )
        self.assertEqual(
            schemas["brand-kit-checksums.schema.json"]["properties"]["schema"]["const"],
            "identity.brand-kit-checksums/v1",
        )
        self.assertEqual(
            schemas["brand-kit-view-model.schema.json"]["properties"]["schema"]["const"],
            "identity.brand-kit-view-model/v1",
        )
        self.assertEqual(
            schemas["quality-report.schema.json"]["properties"]["schema"]["const"],
            "identity.quality-report/v1",
        )
        self.assertEqual(
            schemas["motion-policy.schema.json"]["properties"]["schema"]["const"],
            "identity.motion-policy/v1",
        )
        self.assertEqual(
            schemas["visual-motion-manifest.schema.json"]["properties"]["schema"]["const"],
            "identity.visual-motion-manifest/v1",
        )
        self.assertEqual(
            validator.V1_PROFILE_VERSIONS,
            {
                "archive": "1.0.0",
                "core": "1.0.0",
                "docs": "1.0.0",
                "github": "1.0.0",
                "metadata": "1.0.0",
                "pwa": "1.0.0",
                "social": "1.0.0",
                "tokens": "1.0.0",
                "web": "1.0.0",
            },
        )

    def test_cli_returns_stable_json_and_process_status(self) -> None:
        valid = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                "--repository-root",
                str(VALID_FIXTURE),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        result = json.loads(valid.stdout)
        self.assertTrue(result["valid"])
        self.assertEqual(result["schema"], "identity.diagnostics/v1")

        with tempfile.TemporaryDirectory() as temporary:
            invalid_root = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, invalid_root)
            (invalid_root / ".identity/governance/provenance.json").unlink()
            invalid = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--repository-root",
                    str(invalid_root),
                    "--format",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(invalid.returncode, 1)
        self.assertFalse(json.loads(invalid.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
