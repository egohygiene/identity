# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Contract tests for release metadata and clean-room digest helpers."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFY_RELEASE = REPOSITORY_ROOT / "scripts" / "verify_release.py"
RELEASE_SMOKE = REPOSITORY_ROOT / "scripts" / "release_smoke.py"


def load_release_smoke_module():
    specification = importlib.util.spec_from_file_location("release_smoke", RELEASE_SMOKE)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ReleaseToolsTests(unittest.TestCase):
    def create_release_metadata(self, root: Path, *, version: str = "1.0.0-rc.1") -> None:
        (root / "renderer").mkdir()
        (root / "docs" / "releases").mkdir(parents=True)
        (root / "Cargo.toml").write_text(
            "[package]\nname = \"identity\"\nversion = \"1.0.0-rc.1\"\n",
            encoding="utf-8",
        )
        (root / "renderer" / "package.json").write_text(
            json.dumps({"version": version}), encoding="utf-8"
        )
        for document in (
            "CHANGELOG.md",
            "SECURITY.md",
            "SUPPORT.md",
            "docs/releases/V1.md",
            "docs/releases/LICENSE_INVENTORY.md",
            "docs/releases/RELEASE_PROCESS.md",
        ):
            (root / document).write_text("release document\n", encoding="utf-8")

    def run_release_verifier(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VERIFY_RELEASE), "--repository-root", str(root), *arguments],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_release_metadata_accepts_matching_candidate_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_release_metadata(root)
            completed = self.run_release_verifier(root, "--tag", "v1.0.0-rc.1")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("release metadata passed", completed.stdout)

    def test_release_metadata_rejects_mismatched_versions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.create_release_metadata(root, version="1.0.0")
            completed = self.run_release_verifier(root)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("must match Cargo.toml", completed.stderr)

    def test_tree_digest_is_independent_of_creation_order(self) -> None:
        release_smoke = load_release_smoke_module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "first"
            second = root / "second"
            first.mkdir()
            second.mkdir()
            (first / "a.txt").write_text("alpha", encoding="utf-8")
            (first / "nested").mkdir()
            (first / "nested" / "b.txt").write_text("beta", encoding="utf-8")
            (second / "nested").mkdir()
            (second / "nested" / "b.txt").write_text("beta", encoding="utf-8")
            (second / "a.txt").write_text("alpha", encoding="utf-8")

            self.assertEqual(release_smoke.tree_digest(first), release_smoke.tree_digest(second))


if __name__ == "__main__":
    unittest.main()
