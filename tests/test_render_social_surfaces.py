# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Offline catalog, inheritance, and integrity evidence for social packages."""

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
RENDERER_PATH = SCRIPTS_ROOT / "render_social_surfaces.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
SOCIAL_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/social-surfaces"
sys.path.insert(0, str(SCRIPTS_ROOT))
SPEC = importlib.util.spec_from_file_location("render_social_surfaces", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    """Write stable JSON fixture material."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def source_digests(repository_root: Path) -> dict[str, str]:
    """Return canonical source checksums for mutation evidence."""

    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((repository_root / ".identity").rglob("*"))
        if path.is_file()
    }


def approval(identifier: str, subject: str) -> dict[str, object]:
    """Return a reviewed social-surface decision."""

    return {
        "id": identifier,
        "subject": subject,
        "candidate": f"social-surfaces:{identifier}/v1",
        "status": "approved",
        "reviewedBy": "example-maintainer",
        "reviewedAt": "2026-08-29T01:00:00Z",
        "evidence": f"https://example.invalid/reviews/{identifier}",
        "supersedes": None,
        "notes": "Approved for the deterministic social-surface fixture.",
    }


def add_social_source(repository_root: Path) -> None:
    """Add a pinned catalog and explicit selections to a copied base fixture."""

    identity_path = repository_root / ".identity/identity.json"
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    identity["documents"]["socialSurfaces"] = ".identity/guidance/social-surfaces.json"
    write_json(identity_path, identity)

    source = json.loads((SOCIAL_FIXTURE / "social-surfaces.json").read_text(encoding="utf-8"))
    write_json(repository_root / ".identity/guidance/social-surfaces.json", source)
    catalog_path = repository_root / source["catalog"]["path"]
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOCIAL_FIXTURE / "aether-catalog.v1.json", catalog_path)

    approvals_path = repository_root / ".identity/governance/approvals.json"
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    for identifier in ("organic-post", "profile-header", "profile-image"):
        approvals["decisions"].extend(
            [
                approval(
                    f"approve-social-default-{identifier}",
                    f"social-surface-default:{identifier}",
                ),
                approval(
                    f"approve-social-adoption-{identifier}",
                    f"social-surface-adoption:{identifier}",
                ),
            ]
        )
    write_json(approvals_path, approvals)


class SocialSurfaceProjectionTests(unittest.TestCase):
    """Prove exact offline projection and bounded selection authority."""

    def test_projection_requires_explicit_opt_in(self) -> None:
        with self.assertRaisesRegex(renderer.ProjectionError, "documents.socialSurfaces"):
            renderer.build_projection(VALID_FIXTURE)

    def test_profile_header_and_post_targets_preserve_catalog_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)

            model, inputs, handoff = renderer.build_projection(repository)
            targets = {target["id"]: target for target in model["targets"]}
            self.assertEqual(
                set(targets),
                {"organic-post", "profile-header", "profile-image"},
            )
            self.assertEqual(
                targets["organic-post"]["surface"]["dimensions"],
                {"widthPx": 1080, "heightPx": 1080},
            )
            self.assertEqual(
                targets["profile-header"]["surface"]["dimensions"],
                {"widthPx": 1500, "heightPx": 500},
            )
            self.assertEqual(
                targets["profile-image"]["surface"]["dimensions"],
                {"widthPx": 512, "heightPx": 512},
            )
            self.assertEqual(targets["organic-post"]["surface"]["safeZone"]["state"], "unknown")
            self.assertIn("safeZone", targets["organic-post"]["constraints"]["unknownFields"])
            self.assertEqual(targets["organic-post"]["content"]["copy"]["source"], "project.tagline")
            self.assertEqual(targets["profile-header"]["content"]["copy"]["source"], "project.displayName")
            self.assertFalse(model["handoff"]["publicationAuthorized"])
            self.assertFalse(handoff["publicationAuthorized"])
            self.assertIn("inputs/mark.svg", inputs)
            self.assertIn("targets/profile-header.json", inputs)

    def test_package_is_reproducible_manifested_and_does_not_mutate_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            before = source_digests(repository)

            first = renderer.build_package(*renderer.build_projection(repository))
            second = renderer.build_package(*renderer.build_projection(repository))
            self.assertEqual(first, second)
            self.assertEqual(source_digests(repository), before)
            manifest = json.loads(first["social-surfaces-manifest.json"])
            source = json.loads(
                (repository / ".identity/guidance/social-surfaces.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["catalog"]["digest"], source["catalog"]["digest"]["value"])
            self.assertNotIn("social-surfaces.zip", manifest["files"])
            with zipfile.ZipFile(BytesIO(first["social-surfaces.zip"])) as archive:
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
                self.assertIn("inputs/mark.svg", archive.namelist())
                self.assertIn("targets/profile-image.json", archive.namelist())
                projected = json.loads(archive.read("social-surfaces.json"))
            self.assertEqual(projected["source"]["digest"], manifest["sourceDigest"])

    def test_catalog_tampering_and_unapproved_catalogs_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            source_path = repository / ".identity/guidance/social-surfaces.json"
            source = json.loads(source_path.read_text(encoding="utf-8"))
            catalog_path = repository / source["catalog"]["path"]

            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog["records"][0]["dimensions"]["width_px"] = 999
            write_json(catalog_path, catalog)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1902", {value.code for value in diagnostics})
            with self.assertRaisesRegex(renderer.ProjectionError, "IDN1902"):
                renderer.build_projection(repository)

            source["catalog"]["digest"]["value"] = renderer.normalized_catalog_digest(catalog_path)
            write_json(source_path, source)
            catalog["catalog"]["rights_review"]["state"] = "rejected"
            write_json(catalog_path, catalog)
            source["catalog"]["digest"]["value"] = renderer.normalized_catalog_digest(catalog_path)
            write_json(source_path, source)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1902", {value.code for value in diagnostics})

    def test_inheritance_supports_reviewed_override_and_opt_out(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            source_path = repository / ".identity/guidance/social-surfaces.json"
            source = json.loads(source_path.read_text(encoding="utf-8"))
            source["project"]["exclude"] = [
                {
                    "id": "organic-post",
                    "reason": "This product does not operate an organic feed.",
                    "approval": "approve-social-exclusion-organic-post",
                }
            ]
            source["project"]["overrides"] = [
                {
                    "id": "profile-header",
                    "copySource": "project.tagline",
                    "reason": "Use the product promise on this bounded header target.",
                    "approval": "approve-social-override-profile-header",
                }
            ]
            write_json(source_path, source)
            approvals_path = repository / ".identity/governance/approvals.json"
            approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
            approvals["decisions"].extend(
                [
                    approval(
                        "approve-social-exclusion-organic-post",
                        "social-surface-exclusion:organic-post",
                    ),
                    approval(
                        "approve-social-override-profile-header",
                        "social-surface-override:profile-header",
                    ),
                ]
            )
            write_json(approvals_path, approvals)

            model, _, _ = renderer.build_projection(repository)
            targets = {target["id"]: target for target in model["targets"]}
            self.assertEqual(set(targets), {"profile-header", "profile-image"})
            self.assertEqual(model["inheritance"]["excluded"], ["organic-post"])
            self.assertEqual(targets["profile-header"]["content"]["copy"]["source"], "project.tagline")
            self.assertEqual(
                targets["profile-header"]["approvals"]["override"],
                "approve-social-override-profile-header",
            )

    def test_missing_asset_and_dimensions_are_honest_validation_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            source_path = repository / ".identity/guidance/social-surfaces.json"
            source = json.loads(source_path.read_text(encoding="utf-8"))
            source["organizationDefaults"][0]["sourceAssetId"] = "missing-artwork"
            write_json(source_path, source)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1903", {value.code for value in diagnostics})

            source["organizationDefaults"][0]["sourceAssetId"] = "mark"
            write_json(source_path, source)
            catalog_path = repository / source["catalog"]["path"]
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            del catalog["records"][0]["dimensions"]
            write_json(catalog_path, catalog)
            source["catalog"]["digest"]["value"] = renderer.normalized_catalog_digest(catalog_path)
            write_json(source_path, source)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1903", {value.code for value in diagnostics})

    def test_generated_output_refuses_canonical_traversal_and_symlink_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            before = source_digests(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            written = renderer.write_outputs(
                repository,
                Path("assets/identity/social-surfaces"),
                payload,
            )
            self.assertEqual(
                [path.relative_to(repository).as_posix() for path in written],
                sorted(path.relative_to(repository).as_posix() for path in written),
            )
            self.assertEqual(source_digests(repository), before)
            with self.assertRaisesRegex(renderer.ProjectionError, "canonical .identity"):
                renderer.write_outputs(repository, Path(".identity/social-surfaces"), payload)
            with self.assertRaisesRegex(renderer.ProjectionError, "normalized"):
                renderer.write_outputs(repository, Path("../outside"), payload)
            redirect = repository / "generated-redirect"
            redirect.symlink_to(repository / ".identity", target_is_directory=True)
            with self.assertRaisesRegex(renderer.ProjectionError, "symbolic link"):
                renderer.write_outputs(repository, Path("generated-redirect/social"), payload)

    def test_cli_prints_one_view_or_writes_complete_package(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout)["schema"], renderer.PACKAGE_SCHEMA)

            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--output-directory",
                    "assets/identity/social-surfaces",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            destination = repository / "assets/identity/social-surfaces"
            for filename in renderer.OUTPUT_FILES.values():
                self.assertTrue((destination / filename).is_file(), filename)
            handoff = json.loads((destination / "press-kit-handoff.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff["schema"], renderer.HANDOFF_SCHEMA)
            self.assertFalse(handoff["publicationAuthorized"])

    def test_press_kit_consumes_only_a_verified_generated_handoff(self) -> None:
        from tests.test_render_press_kit import add_press_source, renderer as press_renderer

        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_social_source(repository)
            add_press_source(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            renderer.write_outputs(
                repository,
                Path("assets/identity/social-surfaces"),
                payload,
            )

            press_model, press_assets = press_renderer.build_projection(repository)
            press_model, press_assets = press_renderer.verified_social_package(
                repository,
                press_model,
                press_assets,
                Path("assets/identity/social-surfaces"),
            )
            self.assertEqual(press_model["socialSurfaces"]["status"], "included")
            self.assertEqual(len(press_model["socialSurfaces"]["targets"]), 3)
            self.assertIn("social/social-surfaces.zip", press_assets)
            package = press_renderer.build_package(press_model, press_assets)
            manifest = json.loads(package["press-kit-manifest.json"])
            self.assertIn("social/social-surfaces.zip", manifest["files"])

            archive_path = repository / "assets/identity/social-surfaces/social-surfaces.zip"
            archive_path.write_bytes(b"tampered")
            with self.assertRaises((press_renderer.ProjectionError, zipfile.BadZipFile)):
                press_renderer.verified_social_package(
                    repository,
                    *press_renderer.build_projection(repository),
                    Path("assets/identity/social-surfaces"),
                )


if __name__ == "__main__":
    unittest.main()
