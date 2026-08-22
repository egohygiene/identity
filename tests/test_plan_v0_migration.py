# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Migration-plan evidence for the incubated Empathy project/v0 source."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLANNER_PATH = REPOSITORY_ROOT / "scripts/plan_v0_migration.py"
FIXTURE_ROOT = REPOSITORY_ROOT / "tests/fixtures/migration/empathy-v0"
EXPECTED_PATH = FIXTURE_ROOT / "expected-plan.json"
SPEC = importlib.util.spec_from_file_location("plan_v0_migration", PLANNER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)


class IdentityV0MigrationTests(unittest.TestCase):
    """Require deterministic preservation and explicit human decisions."""

    def test_empathy_v0_fixture_matches_the_reviewed_plan(self) -> None:
        expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))

        self.assertEqual(planner.plan_migration(FIXTURE_ROOT), expected)
        self.assertEqual(expected["source"]["schema"], "identity.project/v0")
        self.assertEqual(expected["target"]["schema"], "identity.project/v1")
        self.assertEqual(len(expected["preserved"]["enabledProfiles"]), 8)
        self.assertEqual(len(expected["preserved"]["requiredSources"]), 8)

    def test_planning_does_not_mutate_the_v0_fixture(self) -> None:
        before = {
            path.relative_to(FIXTURE_ROOT): path.read_bytes()
            for path in FIXTURE_ROOT.rglob("*")
            if path.is_file()
        }

        planner.plan_migration(FIXTURE_ROOT)

        after = {
            path.relative_to(FIXTURE_ROOT): path.read_bytes()
            for path in FIXTURE_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_cli_reports_invalid_source_without_writing_a_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            identity_root = repository / ".identity"
            identity_root.mkdir()
            (identity_root / "identity.toml").write_text(
                'schema = "identity.project/v2"\n', encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(PLANNER_PATH),
                    "--repository-root",
                    str(repository),
                    "--format",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("source schema must be identity.project/v0", result.stderr)
            self.assertFalse((repository / ".identity-v1").exists())


if __name__ == "__main__":
    unittest.main()
