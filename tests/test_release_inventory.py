# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Unit tests for deterministic release-license inventory construction."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RELEASE_INVENTORY = REPOSITORY_ROOT / "scripts" / "release_inventory.py"


def load_release_inventory_module():
    specification = importlib.util.spec_from_file_location("release_inventory", RELEASE_INVENTORY)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ReleaseInventoryTests(unittest.TestCase):
    def test_inventory_sorts_packages_and_records_missing_licenses(self) -> None:
        release_inventory = load_release_inventory_module()
        result = release_inventory.inventory(
            {
                "packages": [
                    {
                        "name": "zebra",
                        "version": "1.0.0",
                        "source": "registry+https://example.invalid",
                        "license": None,
                    },
                    {
                        "name": "alpha",
                        "version": "2.0.0",
                        "source": None,
                        "license": "MIT",
                    },
                ]
            },
            release_version="1.0.0-rc.1",
        )

        self.assertEqual(result["schema"], "identity.license-inventory/v1")
        self.assertEqual([entry["name"] for entry in result["packages"]], ["alpha", "zebra"])
        self.assertEqual(result["missingLicenseDeclarations"], ["zebra@1.0.0"])
        self.assertEqual(result["packages"][1]["license"], "NOASSERTION")


if __name__ == "__main__":
    unittest.main()
