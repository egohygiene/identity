# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Unit tests for Identity's bounded dogfood adapter and verifier."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


builder = load_module(
    "build_identity_experience",
    REPOSITORY_ROOT / "scripts/build_identity_experience.py",
)
verifier = load_module(
    "verify_identity_experience",
    REPOSITORY_ROOT / "scripts/verify_identity_experience.py",
)


class IdentityExperienceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.content = json.loads(
            (REPOSITORY_ROOT / "publication/identity-experience.content.json").read_text()
        )
        self.mascot = builder.mascot_projection(REPOSITORY_ROOT, self.content)

    def test_launchkit_projection_resolves_governed_mascot_and_release(self) -> None:
        original = deepcopy(self.content)

        launchkit = builder.compile_launchkit_content(
            self.content,
            self.mascot,
            "v1.1.0",
            "a" * 40,
        )

        self.assertEqual(self.content, original)
        self.assertEqual(launchkit["demo"]["asset"]["alt"], self.mascot["altText"])
        self.assertEqual(launchkit["demo"]["asset"]["src"], self.mascot["publicPath"])
        self.assertIn("Release v1.1.0", launchkit["proof"]["items"])
        self.assertIn("Commit aaaaaaaaaaaa", launchkit["proof"]["items"])

    def test_mascot_projection_fails_when_selected_bytes_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in (
                "mascot/kern.character.json",
                "assets/identity/mascot/manifest.json",
                "assets/identity/mascot/kern-full.png",
            ):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPOSITORY_ROOT / relative, destination)
            (root / "assets/identity/mascot/kern-full.png").write_bytes(b"drift")

            with self.assertRaisesRegex(builder.BuildError, "checksum"):
                builder.mascot_projection(root, self.content)

    def test_source_digest_is_checkout_path_independent(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            roots = [Path(first), Path(second)]
            digests = []
            for root in roots:
                identity = root / "identity"
                holon = root / "holon"
                (identity / "publication").mkdir(parents=True)
                (holon / "blueprints").mkdir(parents=True)
                identity_file = identity / "publication/input.json"
                holon_file = holon / "blueprints/profile.json"
                identity_file.write_text("{}\n")
                holon_file.write_text("{}\n")
                digests.append(
                    builder.source_digest(
                        [identity_file, holon_file],
                        identity.resolve(),
                        holon.resolve(),
                    )
                )
            self.assertEqual(digests[0], digests[1])

    def test_subpath_adapter_normalizes_only_identity_routes(self) -> None:
        adapter = load_module(
            "identity_site_suite_adapter",
            REPOSITORY_ROOT / "experience/site_suite_adapter.py",
        )

        self.assertEqual(adapter.normalize_reference("/identity/docs/"), "/docs/")
        self.assertEqual(adapter.normalize_reference("/identity#proof"), "/#proof")
        self.assertEqual(adapter.normalize_reference("/brand/"), "/brand/")
        self.assertEqual(
            adapter.normalize_reference("https://identity.egohygiene.io/"),
            "https://identity.egohygiene.io/",
        )

    def test_reviewed_visual_baselines_match_their_governed_sources(self) -> None:
        self.assertEqual(verifier.verify_visual_baselines(REPOSITORY_ROOT), [])

    def test_checked_build_artifact_verifies_when_present(self) -> None:
        artifact = REPOSITORY_ROOT / ".identity-experience-build"
        if not artifact.is_dir():
            self.skipTest("local integration artifact has not been built")
        publication = json.loads(
            (artifact / "identity/publication.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            verifier.verify_artifact(
                artifact,
                repository_root=REPOSITORY_ROOT,
                expected_release_tag=publication["release"]["tag"],
                expected_release_commit=publication["release"]["commit"],
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
