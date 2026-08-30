# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Tests for release-bound Brand Kit publication configurations."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = REPOSITORY_ROOT / "scripts" / "verify_publication_release_configs.py"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "verify_publication_release_configs", VERIFY_SCRIPT
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class PublicationReleaseConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_checked_in_compatibility_mapping_is_valid(self) -> None:
        self.assertEqual(self.module.verify_repository(REPOSITORY_ROOT), [])

    def test_digest_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config_directory = root / "publication" / "release-configs"
            config_directory.mkdir(parents=True)
            config = config_directory / "v1.0.0.json"
            config.write_text("{}\n", encoding="utf-8")
            index = {
                "schema": self.module.INDEX_SCHEMA,
                "releases": {
                    "v1.0.0": {
                        "commit": "a" * 40,
                        "config": "publication/release-configs/v1.0.0.json",
                        "sha256": "0" * 64,
                        "reason": "fixture",
                    }
                },
            }
            (config_directory / "index.json").write_text(
                json.dumps(index), encoding="utf-8"
            )

            errors = self.module.verify_index(root)

        self.assertTrue(any("digest drifted" in error for error in errors), errors)

    def test_config_cannot_claim_an_asset_missing_from_release(self) -> None:
        config = {
            "schema": self.module.CONFIG_SCHEMA,
            "canonicalUrl": "https://identity.egohygiene.io/",
            "release": {
                "defaultTag": "v1.0.0",
                "defaultCommit": "a" * 40,
            },
            "assets": [
                {
                    "id": "future-asset",
                    "sourcePath": "mascot/not-in-release.png",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            errors = self.module.verify_config(
                config,
                Path(temporary),
                "v1.0.0",
                "a" * 40,
            )

        self.assertTrue(any("does not contain" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
