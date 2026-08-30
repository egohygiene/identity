# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Tests for the accepted Identity publication architecture contract."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFY_SCRIPT = REPOSITORY_ROOT / "scripts" / "verify_publication_architecture.py"
ARCHITECTURE = REPOSITORY_ROOT / "publication" / "identity-experience.architecture.json"


def load_module():
    specification = importlib.util.spec_from_file_location(
        "verify_publication_architecture", VERIFY_SCRIPT
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class PublicationArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.document = json.loads(ARCHITECTURE.read_text(encoding="utf-8"))

    def validate(self, document: dict) -> list[str]:
        return self.module.verify_document(document, REPOSITORY_ROOT)

    def test_repository_contract_is_valid_offline(self) -> None:
        self.assertEqual(self.module.verify_repository(REPOSITORY_ROOT), [])

    def test_route_collision_fails_closed(self) -> None:
        document = copy.deepcopy(self.document)
        document["routes"][1]["path"] = "/identity/"

        errors = self.validate(document)

        self.assertTrue(any("route collision" in error for error in errors), errors)

    def test_moving_launchkit_reference_is_rejected(self) -> None:
        document = copy.deepcopy(self.document)
        launchkit = next(adapter for adapter in document["adapters"] if adapter["id"] == "launchkit")
        launchkit["pin"]["commit"] = "main"

        errors = self.validate(document)

        self.assertTrue(any("immutable Holon profile pin" in error for error in errors), errors)
        self.assertTrue(any("full commit SHA" in error for error in errors), errors)
        self.assertTrue(any("moving reference" in error for error in errors), errors)

    def test_framework_cannot_claim_brand_authority(self) -> None:
        document = copy.deepcopy(self.document)
        zensical = next(adapter for adapter in document["adapters"] if adapter["id"] == "zensical")
        zensical["canonicalBrandSource"] = True

        errors = self.validate(document)

        self.assertTrue(any("deny canonical brand authority" in error for error in errors), errors)

    def test_identity_cannot_reclaim_the_shared_zensical_profile(self) -> None:
        document = copy.deepcopy(self.document)
        zensical = next(adapter for adapter in document["adapters"] if adapter["id"] == "zensical")
        zensical["implementationOwner"] = "egohygiene/identity"
        zensical["status"] = "dogfood-adapter"

        errors = self.validate(document)

        self.assertTrue(any("Holon docs profile" in error for error in errors), errors)

    def test_identity_composer_must_extend_the_shared_site_suite(self) -> None:
        document = copy.deepcopy(self.document)
        composer = next(
            adapter for adapter in document["adapters"] if adapter["id"] == "route-composer"
        )
        composer["pin"]["commit"] = "main"

        errors = self.validate(document)

        self.assertTrue(any("immutable Holon site-suite pin" in error for error in errors), errors)
        self.assertTrue(any("moving reference" in error for error in errors), errors)

    def test_release_evidence_cannot_omit_approval(self) -> None:
        document = copy.deepcopy(self.document)
        document["releaseEvidence"]["requiredFields"].remove("approvalEvidence")

        errors = self.validate(document)

        self.assertTrue(any("inspectable field" in error for error in errors), errors)

    def test_progressive_enhancement_gate_is_required(self) -> None:
        document = copy.deepcopy(self.document)
        document["qualityRequirements"].remove("no-javascript-readable")

        errors = self.validate(document)

        self.assertTrue(any("qualityRequirements" in error for error in errors), errors)

    def test_brand_alias_cannot_drift_from_canonical_host(self) -> None:
        document = copy.deepcopy(self.document)
        alias = next(route for route in document["routes"] if route["id"] == "organization-brand-alias")
        alias["target"] = "https://egohygiene.io/identity/"

        errors = self.validate(document)

        self.assertTrue(any("canonical Brand Kit" in error for error in errors), errors)

    def test_implemented_dogfood_routes_are_handoff_ready(self) -> None:
        document = copy.deepcopy(self.document)
        route = next(route for route in document["routes"] if route["id"] == "organization-identity")
        route["status"] = "planned"

        errors = self.validate(document)

        self.assertTrue(any("handoff-ready" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
