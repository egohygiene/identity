# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Repository banner, explicit evidence-state, and deterministic package tests."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tests/fixtures/v1/valid/minimal"
FIXTURES = ROOT / "tests/fixtures/repository-presentation"
SCRIPT = ROOT / "scripts/render_repository_presentation.py"
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("render_repository_presentation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def approval(identifier: str, subject: str) -> dict[str, object]:
    return {
        "id": identifier,
        "subject": subject,
        "candidate": f"repository-presentation:{identifier}/v1",
        "status": "approved",
        "reviewedBy": "example-maintainer",
        "reviewedAt": "2026-08-30T00:00:00Z",
        "evidence": f"https://example.invalid/reviews/{identifier}",
        "supersedes": None,
        "notes": "Approved for deterministic repository-presentation fixtures.",
    }


def prepare(repository: Path, source_name: str = "source.organization-default.json") -> None:
    shutil.copytree(BASE, repository)
    (repository / "README.md").write_text("# Consumer-authored README\n", encoding="utf-8")
    identity_path = repository / ".identity/identity.json"
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    identity["documents"]["repositoryPresentation"] = ".identity/guidance/repository-presentation.json"
    write_json(identity_path, identity)
    shutil.copyfile(FIXTURES / source_name, repository / ".identity/guidance/repository-presentation.json")
    vendor = repository / "vendor/hygiene"
    vendor.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "hygiene-profile.v1.json", vendor / "repository-presentation-profile.v1.json")
    approvals_path = repository / ".identity/governance/approvals.json"
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    approvals["decisions"].extend(
        [
            approval("approve-repository-banner-default", "repository-presentation-banner-default"),
            approval("approve-hygienic-badge-profile", "repository-presentation-badge-profile"),
            approval("approve-repository-banner-override", "repository-presentation-banner-override:example-product"),
        ]
    )
    write_json(approvals_path, approvals)


def source_digests(repository: Path) -> dict[str, str]:
    return {
        path.relative_to(repository).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((repository / ".identity").rglob("*"))
        if path.is_file()
    }


def png_dimensions(value: bytes) -> tuple[int, int]:
    if not value.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError("not a PNG")
    return struct.unpack(">II", value[16:24])


class RepositoryPresentationProjectionTests(unittest.TestCase):
    """Prove the visual projection never acquires evidence authority."""

    def test_organization_default_projects_accessible_theme_and_width_variants(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            prepare(repository)
            model, files, manifest = renderer.build_projection(
                repository,
                FIXTURES / "evidence.organization-default.json",
            )

            self.assertEqual(model["badge"]["state"], "passing")
            self.assertEqual(model["badge"]["label"], "Hygienic")
            self.assertEqual(model["badge"]["message"], "repository profile passing")
            self.assertEqual(model["badge"]["representedCommit"], "1" * 40)
            self.assertEqual(
                {item["state"] for item in model["badge"]["visualProfile"]["states"]},
                set(renderer.STATE_COLORS),
            )
            self.assertEqual(
                [item["state"] for item in model["badge"]["visualProfile"]["states"] if item["passing"]],
                ["passing"],
            )
            self.assertEqual(model["profile"]["status"], "proposed")
            self.assertFalse(model["profile"]["activationClaimed"])
            self.assertTrue(model["source"]["bannerAsset"]["inheritedFromOrganization"])
            self.assertIn("Example Product", model["banner"]["altText"])
            self.assertIn("Example Product", model["banner"]["fallbackText"])
            self.assertEqual(len(model["banner"]["variants"]), 9)
            self.assertEqual(
                {(item["theme"], item["width"]) for item in model["banner"]["variants"]},
                {(theme, width) for theme in renderer.THEMES for width in renderer.BANNER_WIDTHS},
            )
            for item in model["banner"]["variants"]:
                self.assertEqual(png_dimensions(files[item["raster"]]), (item["width"], item["height"]))
                svg = files[item["svg"]].decode("utf-8")
                self.assertIn("role=\"img\"", svg)
                self.assertIn(model["banner"]["altText"], svg)
            self.assertEqual(png_dimensions(files[model["badge"]["raster"]])[1], 24)
            self.assertIn("Hygienic: repository profile passing", files[model["badge"]["svg"]].decode("utf-8"))
            self.assertEqual(set(manifest["files"]), set(files))

    def test_project_override_is_bounded_approved_and_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            prepare(repository, "source.product-override.json")
            model, _, _ = renderer.build_projection(repository, FIXTURES / "evidence.product-override.json")
            self.assertFalse(model["source"]["bannerAsset"]["inheritedFromOrganization"])
            self.assertEqual(model["source"]["bannerAsset"]["id"], "mark")
            self.assertIn("product-specific", model["banner"]["altText"])
            self.assertEqual(model["badge"]["state"], "advisory")
            self.assertEqual(model["source"]["approval"]["projectOverride"], "approve-repository-banner-override")

    def test_private_and_missing_evidence_fixtures_fail_closed(self) -> None:
        scenarios = (
            ("source.private.json", "evidence.private.json", "private", "exempt"),
            ("source.organization-default.json", "evidence.missing.json", "public", "unknown"),
        )
        for source_name, evidence_name, visibility, state in scenarios:
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                prepare(repository, source_name)
                model, files, _ = renderer.build_projection(repository, FIXTURES / evidence_name)
                self.assertEqual(model["project"]["visibility"], visibility)
                self.assertEqual(model["badge"]["state"], state)
                self.assertNotIn("repository profile passing", files[model["badge"]["svg"]].decode("utf-8"))

    def test_every_hygiene_state_renders_only_from_explicit_exact_input(self) -> None:
        profile = json.loads((FIXTURES / "hygiene-profile.v1.json").read_text(encoding="utf-8"))
        messages = profile["claim_policy"]["state_messages"]
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            prepare(repository)
            for index, state in enumerate(profile["evidence_states"], start=1):
                with self.subTest(state=state):
                    evidence = json.loads((FIXTURES / "evidence.missing.json").read_text(encoding="utf-8"))
                    evidence["assessment"]["state"] = state
                    evidence["badge"]["state"] = state
                    evidence["badge"]["message"] = messages[state]
                    evidence["repository"]["represented_commit"] = f"{index:040x}"
                    evidence["badge"]["represented_commit"] = f"{index:040x}"
                    evidence_path = Path(temporary) / f"{state}.json"
                    write_json(evidence_path, evidence)
                    model, files, _ = renderer.build_projection(repository, evidence_path)
                    self.assertEqual(model["badge"]["state"], state)
                    self.assertEqual(model["badge"]["message"], messages[state])
                    badge = files[model["badge"]["svg"]].decode("utf-8")
                    self.assertIn(messages[state], badge)
                    if state != "passing":
                        self.assertNotIn("repository profile passing", badge)

    def test_state_message_commit_url_and_profile_pin_are_not_inferred(self) -> None:
        mutations = (
            (lambda value: value["badge"].__setitem__("message", "repository profile passing"), "label or message"),
            (lambda value: value["badge"].__setitem__("represented_commit", "abc123"), "full represented commit"),
            (lambda value: value["badge"].__setitem__("evidence_url", ""), "evidence URL"),
            (lambda value: value["badge"].__setitem__("evidence_url", "javascript:alert(1)"), "HTTPS or repository-relative"),
            (lambda value: value["repository"].__setitem__("visibility", "private"), "visibility differs"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            prepare(repository)
            for index, (mutation, message) in enumerate(mutations):
                evidence = json.loads((FIXTURES / "evidence.missing.json").read_text(encoding="utf-8"))
                mutation(evidence)
                path = Path(temporary) / f"invalid-{index}.json"
                write_json(path, evidence)
                with self.subTest(message=message), self.assertRaisesRegex(renderer.ProjectionError, message):
                    renderer.build_projection(repository, path)
            profile = repository / "vendor/hygiene/repository-presentation-profile.v1.json"
            profile.write_text(profile.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with self.assertRaisesRegex(renderer.ProjectionError, "digest"):
                renderer.build_projection(repository, FIXTURES / "evidence.missing.json")

    def test_projection_is_reproducible_and_does_not_mutate_source_or_readme(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            prepare(repository)
            before = source_digests(repository)
            readme_before = (repository / "README.md").read_bytes()
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repository-root", str(repository), "--evidence", str(FIXTURES / "evidence.organization-default.json"), "--output", str(first)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--repository-root", str(repository), "--evidence", str(FIXTURES / "evidence.organization-default.json"), "--output", str(second)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            first_files = {path.relative_to(first).as_posix(): path.read_bytes() for path in first.rglob("*") if path.is_file()}
            second_files = {path.relative_to(second).as_posix(): path.read_bytes() for path in second.rglob("*") if path.is_file()}
            self.assertEqual(first_files, second_files)
            self.assertEqual(before, source_digests(repository))
            self.assertEqual(readme_before, (repository / "README.md").read_bytes())
            self.assertFalse(any("certified" in value.decode("utf-8", errors="ignore").lower() for value in first_files.values()))


if __name__ == "__main__":
    unittest.main()
