# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Governance, projection, and security evidence for organization channels."""

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
RENDERER_PATH = SCRIPTS_ROOT / "render_channel_registry.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
sys.path.insert(0, str(SCRIPTS_ROOT))
sys.path.insert(0, str(REPOSITORY_ROOT / "tests"))
import test_render_press_kit as press_tests
import test_render_social_surfaces as social_tests
SPEC = importlib.util.spec_from_file_location("render_channel_registry", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    """Write stable JSON fixture material."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def decision(identifier: str, subject: str) -> dict[str, object]:
    """Return one approved channel decision."""

    return {
        "id": identifier,
        "subject": subject,
        "candidate": f"channels:{identifier}/v1",
        "status": "approved",
        "reviewedBy": "example-maintainer",
        "reviewedAt": "2026-08-31T00:00:00Z",
        "evidence": f"https://example.invalid/reviews/{identifier}",
        "supersedes": None,
        "notes": "Approved for the deterministic channel fixture.",
    }


def channel(identifier: str, state: str, *, active: bool) -> dict[str, object]:
    """Return one governed channel fixture."""

    label = "Example Network" if identifier == "example-network" else "Future Network"
    return {
        "id": identifier,
        "platform": {"id": identifier, "label": label},
        "canonicalUrl": f"https://example.invalid/{identifier}" if active else None,
        "handle": f"@{identifier}" if active else None,
        "ownershipEntity": "Example Organization",
        "verification": {
            "state": "verified" if active else "unverified",
            "evidence": f"https://example.invalid/verification/{identifier}" if active else None,
        },
        "lifecycle": {
            "state": state,
            "since": "2026-08-31",
            "notes": "Synthetic channel fixture.",
        },
        "audiencePurpose": "Share reviewed organization updates.",
        "contentScope": ["organization updates"],
        "locale": ["en"],
        "accessibility": {
            "label": f"Example Organization on {label}",
            "contactNotes": "Use the organization website for support.",
        },
        "recoveryOwner": "organization-account-administrator",
        "badge": {
            "approved": active,
            "label": f"Follow Example Organization on {label}",
            "icon": {
                "id": identifier,
                "source": f"https://example.invalid/icons/{identifier}",
                "license": "CC0-1.0",
            },
        },
        "governance": {
            "subject": f"channel:{identifier}",
            "state": "approved",
            "visibility": "public",
            "provenance": {
                "method": "human-authored",
                "source": ".identity/brief.md",
                "capturedAt": "2026-08-31T00:00:00Z",
            },
            "approval": f"approve-channel-{identifier}",
        },
    }


def add_registry(repository_root: Path) -> Path:
    """Attach one active and one planned channel to the valid v1 fixture."""

    project_path = repository_root / ".identity/identity.json"
    project = json.loads(project_path.read_text(encoding="utf-8"))
    project["documents"]["channelRegistry"] = ".identity/guidance/channel-registry.json"
    write_json(project_path, project)
    registry_path = repository_root / ".identity/guidance/channel-registry.json"
    write_json(
        registry_path,
        {
            "$schema": "../../contracts/v1/channel-registry.schema.json",
            "schema": "identity.channel-registry-source/v1",
            "registry": {
                "id": "example-organization-channels",
                "version": "1.0.0",
                "owner": "Example Organization",
                "reviewedAt": "2026-08-31T00:00:00Z",
            },
            "security": {
                "secretsStored": False,
                "ownerReferenceKind": "role",
                "procedureLocation": "private account-recovery runbook",
            },
            "channels": [
                channel("future-network", "planned", active=False),
                channel("example-network", "active", active=True),
            ],
        },
    )
    approvals_path = repository_root / ".identity/governance/approvals.json"
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    approvals["decisions"].extend(
        [
            decision("approve-channel-example-network", "channel:example-network"),
            decision("approve-channel-future-network", "channel:future-network"),
        ]
    )
    write_json(approvals_path, approvals)
    return registry_path


class ChannelRegistryProjectionTests(unittest.TestCase):
    """Prove lifecycle honesty, deterministic adapters, and secret exclusion."""

    def test_projection_requires_explicit_registry(self) -> None:
        with self.assertRaisesRegex(renderer.ProjectionError, "documents.channelRegistry"):
            renderer.build_projection(VALID_FIXTURE)

    def test_canonical_organization_registry_is_valid_and_honestly_planned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            project_path = repository / ".identity/identity.json"
            project = json.loads(project_path.read_text(encoding="utf-8"))
            project["documents"]["channelRegistry"] = ".identity/guidance/channel-registry.json"
            write_json(project_path, project)
            canonical = json.loads(
                (REPOSITORY_ROOT / "publication/channel-registry.v1.json").read_text(
                    encoding="utf-8"
                )
            )
            canonical["$schema"] = "../../contracts/v1/channel-registry.schema.json"
            write_json(repository / ".identity/guidance/channel-registry.json", canonical)
            approvals_path = repository / ".identity/governance/approvals.json"
            approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
            approvals["decisions"].extend(
                decision(value["governance"]["approval"], f"channel:{value['id']}")
                for value in canonical["channels"]
            )
            write_json(approvals_path, approvals)

            self.assertEqual(renderer.validator.validate_identity(repository), [])
            model = renderer.build_projection(repository)
            self.assertEqual(len(model["channels"]), 8)
            self.assertEqual(model["publicChannels"], [])
            self.assertEqual(
                {value["lifecycle"]["state"] for value in model["channels"]},
                {"planned"},
            )

    def test_only_active_approved_channels_reach_badges_and_footers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_registry(repository)

            model = renderer.build_projection(repository)

            self.assertEqual(
                [value["id"] for value in model["channels"]],
                ["example-network", "future-network"],
            )
            self.assertEqual(
                [value["id"] for value in model["publicChannels"]],
                ["example-network"],
            )
            badges = renderer.render_badges(model)
            self.assertIn("Example Network", badges)
            self.assertNotIn("Future Network", badges)
            footer = json.loads(renderer.render_json(model["publicChannels"]))
            self.assertEqual(footer[0]["verification"], "verified")

    def test_lifecycle_and_verification_vocabularies_remain_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            registry_path = add_registry(repository)
            source = json.loads(registry_path.read_text(encoding="utf-8"))
            states = (
                "planned",
                "reserved",
                "active",
                "unavailable",
                "deprecated",
                "impersonation-risk",
            )
            source["channels"] = [
                channel(f"state-{state}", state, active=state == "active")
                for state in states
            ]
            write_json(registry_path, source)
            approvals_path = repository / ".identity/governance/approvals.json"
            approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
            approvals["decisions"].extend(
                decision(f"approve-channel-state-{state}", f"channel:state-{state}")
                for state in states
            )
            write_json(approvals_path, approvals)

            self.assertEqual(renderer.validator.validate_identity(repository), [])
            model = renderer.build_projection(repository)
            self.assertEqual(
                {value["lifecycle"]["state"] for value in model["channels"]},
                set(states),
            )
            self.assertEqual(
                [value["id"] for value in model["publicChannels"]],
                ["state-active"],
            )

    def test_package_is_reproducible_and_contains_no_recovery_material(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_registry(repository)

            first = renderer.build_package(renderer.build_projection(repository))
            second = renderer.build_package(renderer.build_projection(repository))

            self.assertEqual(first, second)
            self.assertNotIn(b"password", first["channel-registry.json"].lower())
            self.assertNotIn(b"recovery code", first["channel-registry.json"].lower())
            with zipfile.ZipFile(BytesIO(first["channel-registry.zip"])) as archive:
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
                self.assertIn("badges.md", archive.namelist())
                self.assertIn("footer-links.json", archive.namelist())
                checksums = archive.read("SHA256SUMS").decode("utf-8")
                for name in archive.namelist():
                    if name != "SHA256SUMS":
                        self.assertIn(hashlib.sha256(archive.read(name)).hexdigest(), checksums)

    def test_invalid_activation_verification_and_security_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            registry_path = add_registry(repository)
            source = json.loads(registry_path.read_text(encoding="utf-8"))
            source["security"]["secretsStored"] = True
            source["channels"][1]["canonicalUrl"] = None
            source["channels"][1]["verification"]["evidence"] = None
            write_json(registry_path, source)

            diagnostics = renderer.validator.validate_identity(repository)
            codes = {value.code for value in diagnostics}

            self.assertIn("IDN2102", codes)
            self.assertIn("IDN2103", codes)
            with self.assertRaisesRegex(renderer.ProjectionError, "IDN210"):
                renderer.build_projection(repository)

    def test_press_kit_and_social_surfaces_consume_the_same_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            press_repository = Path(temporary) / "press-consumer"
            shutil.copytree(VALID_FIXTURE, press_repository)
            press_tests.add_press_source(press_repository)
            add_registry(press_repository)

            press_model, _ = press_tests.renderer.build_projection(press_repository)

            social_links = [
                value for value in press_model["links"] if value["kind"] == "social"
            ]
            self.assertEqual([value["id"] for value in social_links], ["channel-example-network"])
            self.assertEqual(
                press_model["channelRegistry"]["channels"][0]["url"],
                social_links[0]["url"],
            )

            social_repository = Path(temporary) / "social-consumer"
            shutil.copytree(VALID_FIXTURE, social_repository)
            social_tests.add_social_source(social_repository)
            add_registry(social_repository)

            social_model, _, _ = social_tests.renderer.build_projection(social_repository)

            self.assertEqual(social_model["channelRegistry"]["activeChannels"], 1)
            self.assertEqual(
                {target["channel"]["id"] for target in social_model["targets"]},
                {"example-network"},
            )

    def test_cli_writes_complete_package_without_mutating_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            registry_path = add_registry(repository)
            before = hashlib.sha256(registry_path.read_bytes()).hexdigest()

            subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--output-directory",
                    "assets/identity/channels",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            destination = repository / "assets/identity/channels"
            self.assertEqual(
                set(path.name for path in destination.iterdir()),
                set(renderer.OUTPUT_FILES.values()),
            )
            self.assertEqual(hashlib.sha256(registry_path.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
