# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Determinism, authority, and package evidence for Press Kit projections."""

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
RENDERER_PATH = SCRIPTS_ROOT / "render_press_kit.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
sys.path.insert(0, str(SCRIPTS_ROOT))
SPEC = importlib.util.spec_from_file_location("render_press_kit", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def write_json(path: Path, value: object) -> None:
    """Write stable JSON fixture material."""

    path.write_text(f"{json.dumps(value, indent=2)}\n", encoding="utf-8")


def source_digests(repository_root: Path) -> dict[str, str]:
    """Return local canonical source checksums for mutation evidence."""

    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((repository_root / ".identity").rglob("*"))
        if path.is_file()
    }


def approval(identifier: str, subject: str) -> dict[str, object]:
    """Return a reviewed approval matching one public Press Kit record."""

    return {
        "id": identifier,
        "subject": subject,
        "candidate": f"press-kit:{identifier}/v1",
        "status": "approved",
        "reviewedBy": "example-maintainer",
        "reviewedAt": "2026-08-28T18:00:00Z",
        "evidence": f"https://example.invalid/reviews/{identifier}",
        "supersedes": None,
        "notes": "Approved for the public Press Kit fixture.",
    }


def governance(subject: str, identifier: str | None) -> dict[str, object]:
    """Return governed public source metadata for a fixture record."""

    return {
        "subject": subject,
        "state": "approved" if identifier else "candidate",
        "visibility": "public" if identifier else "internal",
        "provenance": {
            "method": "human-authored" if identifier else "handoff-candidate",
            "source": ".identity/brief.md",
            "capturedAt": "2026-08-28T18:00:00Z",
        },
        "approval": identifier,
    }


def add_press_source(repository_root: Path, *, paragraph: str | None = None) -> None:
    """Add a complete governed Press Kit source to a copied base fixture."""

    identity_path = repository_root / ".identity/identity.json"
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    identity["documents"]["pressKit"] = ".identity/guidance/press-kit.json"
    write_json(identity_path, identity)
    approvals_path = repository_root / ".identity/governance/approvals.json"
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))
    decisions = [
        approval("approve-press-short", "press-kit:boilerplate:short"),
        approval("approve-press-long", "press-kit:boilerplate:long"),
        approval("approve-press-founded", "press-kit:fact:founded"),
        approval("approve-press-website", "press-kit:link:website"),
        approval("approve-press-contact", "press-kit:contact:media"),
        approval("approve-press-founder", "press-kit:team:founder"),
        approval("approve-press-mark", "press-kit:asset:mark"),
    ]
    if paragraph is not None:
        decisions.append(approval("approve-press-paragraph", "press-kit:boilerplate:paragraph"))
    approvals["decisions"].extend(decisions)
    write_json(approvals_path, approvals)
    press = {
        "$schema": "../../../../../contracts/v1/press-kit.schema.json",
        "schema": "identity.press-kit-source/v1",
        "boilerplates": [
            {
                "id": "short",
                "kind": "short",
                "text": "Example Product turns reviewed identity intent into reusable, deterministic artifacts.",
                "governance": governance("press-kit:boilerplate:short", "approve-press-short"),
            },
            {
                "id": "long",
                "kind": "long",
                "text": "Example Product is a local-first Identity workflow for maintainers who need approved tokens, assets, and guidance without splitting brand truth across hand-maintained folders.",
                "governance": governance("press-kit:boilerplate:long", "approve-press-long"),
            },
        ],
        "facts": [
            {
                "id": "founded",
                "label": "Availability",
                "value": "Open source and available to repository maintainers.",
                "governance": governance("press-kit:fact:founded", "approve-press-founded"),
            },
            {
                "id": "candidate-fact",
                "label": "Candidate claim",
                "value": "This unreviewed claim must never be projected.",
                "governance": governance("press-kit:fact:candidate", None),
            },
        ],
        "links": [
            {
                "id": "website",
                "label": "Project repository",
                "url": "https://example.invalid/example-product",
                "kind": "repository",
                "governance": governance("press-kit:link:website", "approve-press-website"),
            }
        ],
        "contacts": [
            {
                "id": "media",
                "label": "Media contact",
                "kind": "email",
                "value": "press@example.invalid",
                "notes": "Please include the requested publication date and deadline.",
                "governance": governance("press-kit:contact:media", "approve-press-contact"),
            }
        ],
        "team": [
            {
                "id": "founder",
                "name": "Example Maintainer",
                "role": "Project maintainer",
                "bio": "Maintains the reviewed source and release boundaries for Example Product.",
                "governance": governance("press-kit:team:founder", "approve-press-founder"),
            }
        ],
        "assets": [
            {
                "id": "mark",
                "assetId": "mark",
                "label": "Primary mark",
                "notes": "Use with the accompanying approved usage guidance.",
                "governance": governance("press-kit:asset:mark", "approve-press-mark"),
            }
        ],
    }
    if paragraph is not None:
        press["boilerplates"].append({
            "id": "paragraph",
            "kind": "paragraph",
            "text": paragraph,
            "governance": governance("press-kit:boilerplate:paragraph", "approve-press-paragraph"),
        })
    write_json(repository_root / ".identity/guidance/press-kit.json", press)


def add_authority_references(repository_root: Path) -> None:
    """Add synthetic owner-reviewed references without importing their policy text."""

    press_path = repository_root / ".identity/guidance/press-kit.json"
    press = json.loads(press_path.read_text(encoding="utf-8"))
    decisions_path = repository_root / ".identity/governance/approvals.json"
    decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
    references = (
        ("software-license", "Software license", "https://example.invalid/policies/LICENSE", "documentation"),
        ("governance", "Governance policy", "https://example.invalid/policies/governance", "documentation"),
        ("code-of-conduct", "Code of Conduct", "https://example.invalid/policies/conduct", "documentation"),
        ("security", "Security reporting policy", "https://example.invalid/policies/security", "documentation"),
        ("contributing", "Contribution guide", "https://example.invalid/policies/contributing", "documentation"),
        ("support", "Official support", "https://example.invalid/support", "support"),
        ("community", "Official community", "https://example.invalid/community", "other"),
        ("font-acquisition", "Acquire Example Typeface separately", "https://example.invalid/typefaces/example", "other"),
    )
    for identifier, label, url, kind in references:
        subject = f"press-kit:link:{identifier}"
        approval_id = f"approve-press-{identifier}"
        decisions["decisions"].append(approval(approval_id, subject))
        press["links"].append({
            "id": identifier,
            "label": label,
            "url": url,
            "kind": kind,
            "governance": governance(subject, approval_id),
        })
    contact_subject = "press-kit:contact:official-support"
    decisions["decisions"].append(approval("approve-official-support", contact_subject))
    press["contacts"].append({
        "id": "official-support",
        "label": "Official support contact",
        "kind": "email",
        "value": "support@example.invalid",
        "notes": "Use the linked security reporting policy for security reports.",
        "governance": governance(contact_subject, "approve-official-support"),
    })
    font_subject = "press-kit:fact:font-acquisition"
    decisions["decisions"].append(approval("approve-font-acquisition-note", font_subject))
    press["facts"].append({
        "id": "font-acquisition-note",
        "label": "Font availability",
        "value": "Example Typeface requires separate acquisition and is not redistributed in this kit.",
        "governance": governance(font_subject, "approve-font-acquisition-note"),
    })
    write_json(press_path, press)
    write_json(decisions_path, decisions)


class PressKitProjectionTests(unittest.TestCase):
    """Prove source authority, deterministic packaging, and honest optional material."""

    def test_standalone_package_verification_is_read_only_and_rejects_archive_injection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            renderer.write_outputs(repository, Path("build/press"), payload)
            directory = repository / "build/press"
            verified = subprocess.run([sys.executable, str(RENDERER_PATH), "--verify-directory", str(directory)],
                                      capture_output=True, text=True, check=False)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertEqual({p: (directory / p).read_bytes() for p in payload}, payload)
            with zipfile.ZipFile(directory / "press-kit.zip", "a") as archive:
                archive.writestr("private-review.txt", "Not selected for public distribution")
            with self.assertRaisesRegex(renderer.ProjectionError, "differs from its projection"):
                renderer.verify_package_directory(directory)
            self.assertEqual(source_digests(repository), before)

    def test_package_verification_rejects_extra_files_and_unsafe_asset_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            renderer.write_outputs(repository, Path("build/press"), renderer.build_package(*renderer.build_projection(repository)))
            directory = repository / "build/press"
            (directory / "unselected.txt").write_text("Not selected", encoding="utf-8")
            with self.assertRaisesRegex(renderer.ProjectionError, "file inventory"):
                renderer.verify_package_directory(directory)
            (directory / "unselected.txt").unlink()
            model = json.loads((directory / "press-kit.json").read_text())
            model["assets"][0]["downloadPath"] = "../outside.svg"
            write_json(directory / "press-kit.json", model)
            with self.assertRaisesRegex(renderer.ProjectionError, "unsafe Press Kit artifact path"):
                renderer.verify_package_directory(directory)

    def test_projection_requires_opt_in_source(self) -> None:
        with self.assertRaisesRegex(renderer.ProjectionError, "documents.pressKit"):
            renderer.build_projection(VALID_FIXTURE)

    def test_selected_assets_still_require_declared_public_usage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            project_path = repository / ".identity/identity.json"
            project = json.loads(project_path.read_text(encoding="utf-8"))
            project["documents"]["guidance"]["usage"] = None
            write_json(project_path, project)
            before = source_digests(repository)
            with self.assertRaisesRegex(renderer.ProjectionError, "IDN1801.*public usage asset"):
                renderer.build_projection(repository)
            self.assertEqual(source_digests(repository), before)

    def test_projection_filters_unapproved_material_and_matches_contract_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            model, assets = renderer.build_projection(repository)
            schema = json.loads(
                (REPOSITORY_ROOT / "contracts/v1/press-kit-projection.schema.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(set(model), set(schema["required"]))
            self.assertEqual([value["kind"] for value in model["boilerplates"]], ["long", "short"])
            self.assertEqual([value["id"] for value in model["facts"]], ["founded"])
            self.assertEqual(model["contacts"][0]["value"], "press@example.invalid")
            self.assertEqual(model["assets"][0]["downloadPath"], "assets/example-product-mark.svg")
            self.assertEqual(
                hashlib.sha256(assets["assets/example-product-mark.svg"]).hexdigest(),
                model["assets"][0]["sha256"],
            )
            self.assertEqual(model["project"]["kind"], "product")
            self.assertEqual(model["inheritance"]["organizationLayers"], ["example-organization"])

    def test_package_is_reproducible_and_contains_manifested_public_material_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            model, assets = renderer.build_projection(repository)
            first = renderer.build_package(model, assets)
            second = renderer.build_package(*renderer.build_projection(repository))
            self.assertEqual(first, second)
            self.assertEqual(source_digests(repository), before)
            manifest = json.loads(first["press-kit-manifest.json"])
            self.assertEqual(manifest["schema"], renderer.PACKAGE_SCHEMA)
            self.assertNotIn("press-kit.zip", manifest["files"])
            with zipfile.ZipFile(BytesIO(first["press-kit.zip"])) as archive:
                self.assertEqual(archive.namelist(), sorted(archive.namelist()))
                self.assertIn("press-kit.json", archive.namelist())
                self.assertIn("assets/example-product-mark.svg", archive.namelist())
                exported = json.loads(archive.read("press-kit.json"))
            self.assertEqual([value["id"] for value in exported["facts"]], ["founded"])

    def test_markdown_exposes_supplied_asset_rights_and_third_party_notices(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            model, assets = renderer.build_projection(repository)
            payload = renderer.build_package(model, assets)
            markdown = payload["press-kit.md"].decode("utf-8")
            asset = model["assets"][0]
            asset_section = markdown.split(f"### {asset['label']}\n", 1)[1].split(
                "\n## Usage and legal guidance", 1
            )[0]
            for supplied in (
                asset["license"]["spdx"],
                asset["license"]["status"],
                asset["license"]["attribution"],
                *asset["origin"].values(),
                asset["usage"]["safeZone"],
                asset["usage"]["minimumSize"],
                *asset["usage"]["restrictions"],
                asset["sha256"],
                asset["approval"]["id"],
            ):
                self.assertIn(supplied, asset_section)
            legal = model["guidance"]["legal"]["value"]
            self.assertIn("### Third-party asset notices", markdown)
            notice_section = markdown.split("### Third-party asset notices\n", 1)[1].split(
                "\n## Downloads", 1
            )[0]
            for notice in legal["thirdPartyLicenses"]:
                for supplied in notice.values():
                    self.assertIn(supplied, notice_section)
            exported = json.loads(payload["press-kit.json"])
            self.assertEqual(exported["assets"][0], asset)
            with zipfile.ZipFile(BytesIO(payload["press-kit.zip"])) as archive:
                self.assertEqual(archive.read("press-kit.md"), payload["press-kit.md"])
                self.assertEqual(archive.read("press-kit.json"), payload["press-kit.json"])
            self.assertEqual(source_digests(repository), before)

    def test_authority_references_and_font_acquisition_link_without_importing_policy_or_font(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            add_authority_references(repository)
            policy_body = "Authoritative policy text stays with its owner, not in generated Identity copy."
            (repository / "GOVERNANCE.md").write_text(policy_body, encoding="utf-8")
            before = source_digests(repository)
            model, assets = renderer.build_projection(repository)
            payload = renderer.build_package(model, assets)
            markdown = payload["press-kit.md"].decode("utf-8")
            self.assertEqual(len(model["links"]), 9)
            for reference in model["links"]:
                self.assertIn(f"[{reference['label']}]({reference['url']})", markdown)
            support = next(value for value in model["contacts"] if value["id"] == "official-support")
            self.assertIn(support["label"], markdown)
            self.assertIn(support["value"], markdown)
            font_note = next(value for value in model["facts"] if value["id"] == "font-acquisition-note")
            self.assertIn(font_note["value"], markdown)
            exported = json.loads(payload["press-kit.json"])
            self.assertEqual(exported["links"], model["links"])
            self.assertEqual(exported["contacts"], model["contacts"])
            with zipfile.ZipFile(BytesIO(payload["press-kit.zip"])) as archive:
                self.assertEqual(archive.read("press-kit.md"), payload["press-kit.md"])
                self.assertEqual(archive.read("press-kit.json"), payload["press-kit.json"])
                self.assertEqual(
                    [name for name in archive.namelist() if name.startswith("assets/")],
                    ["assets/example-product-mark.svg"],
                )
                for name in archive.namelist():
                    self.assertNotIn(policy_body.encode("utf-8"), archive.read(name))
            self.assertEqual(source_digests(repository), before)

    def test_withheld_authority_references_never_enter_public_package(self) -> None:
        for state, visibility in (
            ("approved", "internal"),
            ("candidate", "internal"),
            ("rejected", "internal"),
            ("superseded", "internal"),
        ):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository)
                add_authority_references(repository)
                press_path = repository / ".identity/guidance/press-kit.json"
                press = json.loads(press_path.read_text(encoding="utf-8"))
                decisions_path = repository / ".identity/governance/approvals.json"
                decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
                records = [
                    next(value for value in press["links"] if value["id"] == "security"),
                    next(value for value in press["links"] if value["id"] == "font-acquisition"),
                    next(value for value in press["contacts"] if value["id"] == "official-support"),
                    next(value for value in press["facts"] if value["id"] == "font-acquisition-note"),
                ]
                withheld = [value["url"] if "url" in value else value["value"] for value in records]
                for record in records:
                    authority = record["governance"]
                    decision = next(value for value in decisions["decisions"] if value["id"] == authority["approval"])
                    authority["state"] = state
                    authority["visibility"] = visibility
                    if state == "candidate":
                        authority["approval"] = None
                        authority["provenance"]["method"] = "handoff-candidate"
                    else:
                        decision["status"] = state
                        if state == "superseded":
                            earlier = approval(f"{decision['id']}-earlier", decision["subject"])
                            decisions["decisions"].append(earlier)
                            decision["supersedes"] = earlier["id"]
                write_json(press_path, press)
                write_json(decisions_path, decisions)
                before = source_digests(repository)
                self.assertEqual(renderer.validator.validate_identity(repository), [])
                payload = renderer.build_package(*renderer.build_projection(repository))
                with zipfile.ZipFile(BytesIO(payload["press-kit.zip"])) as archive:
                    contents = [archive.read(name) for name in archive.namelist()]
                for text in withheld:
                    for output in [*payload.values(), *contents]:
                        self.assertNotIn(text.encode("utf-8"), output)
                self.assertEqual(source_digests(repository), before)

    def test_empty_optional_references_and_notices_have_no_invented_substitutes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            press_path = repository / ".identity/guidance/press-kit.json"
            press = json.loads(press_path.read_text(encoding="utf-8"))
            for collection in ("facts", "links", "contacts", "team", "assets"):
                press[collection] = []
            write_json(press_path, press)
            usage_path = repository / ".identity/guidance/usage.json"
            usage = json.loads(usage_path.read_text(encoding="utf-8"))
            usage["legal"]["thirdPartyLicenses"] = []
            write_json(usage_path, usage)
            before = source_digests(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            markdown = payload["press-kit.md"].decode("utf-8")
            exported = json.loads(payload["press-kit.json"])
            for collection in ("facts", "links", "contacts", "team", "assets"):
                self.assertEqual(exported[collection], [])
            self.assertIn("No additional public links are declared", markdown)
            self.assertIn("No public media contact is declared", markdown)
            self.assertIn("No Press Kit assets are selected", markdown)
            self.assertIn("No third-party asset notices are declared", markdown)
            self.assertNotIn("https://example.invalid/policies/", markdown)
            self.assertNotIn("typefaces/example", markdown)
            self.assertEqual(source_digests(repository), before)

    def test_unresolved_source_rights_cannot_become_a_distributed_asset(self) -> None:
        for field, unresolved in (("status", "pending"), ("spdx", "NOASSERTION")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository)
                provenance_path = repository / ".identity/governance/provenance.json"
                provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
                provenance["assets"][0]["license"][field] = unresolved
                write_json(provenance_path, provenance)
                before = source_digests(repository)
                with self.assertRaisesRegex(renderer.ProjectionError, "IDN1402.*license"):
                    renderer.build_projection(repository)
                self.assertEqual(source_digests(repository), before)

    def test_optional_paragraph_round_trips_exactly_and_omits_cleanly(self) -> None:
        paragraph = 'Example Product keeps approved copy exact: “reviewed”, reusable & local.'
        for supplied in (None, paragraph):
            with self.subTest(supplied=supplied is not None), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository, paragraph=supplied)
                before = source_digests(repository)
                model, assets = renderer.build_projection(repository)
                payload = renderer.build_package(model, assets)
                exported = json.loads(payload["press-kit.json"])
                paragraphs = [item for item in exported["boilerplates"] if item["kind"] == "paragraph"]
                self.assertEqual([item["text"] for item in paragraphs], [paragraph] if supplied else [])
                markdown = payload["press-kit.md"].decode("utf-8")
                self.assertEqual("## Paragraph boilerplate" in markdown, supplied is not None)
                if supplied is not None:
                    self.assertIn(paragraph, markdown)
                    self.assertLess(markdown.index("## Short boilerplate"), markdown.index("## Paragraph boilerplate"))
                    self.assertLess(markdown.index("## Paragraph boilerplate"), markdown.index("## Long boilerplate"))
                with zipfile.ZipFile(BytesIO(payload["press-kit.zip"])) as archive:
                    for filename in ("press-kit.json", "press-kit.md"):
                        self.assertEqual(archive.read(filename), payload[filename])
                self.assertEqual(source_digests(repository), before)

    def test_optional_paragraph_and_profile_facts_preserve_public_lifecycle_boundary(self) -> None:
        cases = (
            ("approved", "public", True),
            ("approved", "internal", False),
            ("candidate", "internal", False),
            ("rejected", "internal", False),
            ("superseded", "internal", False),
        )
        paragraph = "Supplied optional paragraph with its own review lifecycle."
        fact = "Supplied optional short name with its own review lifecycle."
        for state, visibility, public in cases:
            with self.subTest(state=state, visibility=visibility), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository, paragraph=paragraph)
                press_path = repository / ".identity/guidance/press-kit.json"
                press = json.loads(press_path.read_text(encoding="utf-8"))
                press["facts"].append({
                    "id": "short-name",
                    "label": "Short name",
                    "value": fact,
                    "governance": governance("press-kit:fact:short-name", "approve-press-short-name"),
                })
                decisions_path = repository / ".identity/governance/approvals.json"
                decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
                decisions["decisions"].append(approval("approve-press-short-name", "press-kit:fact:short-name"))
                for record in (press["boilerplates"][-1], press["facts"][-1]):
                    authority = record["governance"]
                    decision = next(item for item in decisions["decisions"] if item["id"] == authority["approval"])
                    authority["state"] = state
                    authority["visibility"] = visibility
                    if state == "candidate":
                        authority["approval"] = None
                        authority["provenance"]["method"] = "handoff-candidate"
                    else:
                        decision["status"] = state
                        if state == "superseded":
                            earlier = approval(f"{decision['id']}-earlier", decision["subject"])
                            decisions["decisions"].append(earlier)
                            decision["supersedes"] = earlier["id"]
                write_json(press_path, press)
                write_json(decisions_path, decisions)
                before = source_digests(repository)
                self.assertEqual(renderer.validator.validate_identity(repository), [])
                payload = renderer.build_package(*renderer.build_projection(repository))
                exported = json.loads(payload["press-kit.json"])
                self.assertEqual(any(item["kind"] == "paragraph" for item in exported["boilerplates"]), public)
                self.assertEqual(any(item["id"] == "short-name" for item in exported["facts"]), public)
                with zipfile.ZipFile(BytesIO(payload["press-kit.zip"])) as archive:
                    contents = [archive.read(name) for name in archive.namelist()]
                for phrase in (paragraph, fact):
                    if public:
                        for filename in ("press-kit.json", "press-kit.md"):
                            self.assertIn(phrase.encode("utf-8"), payload[filename])
                    else:
                        for output in [*payload.values(), *contents]:
                            self.assertNotIn(phrase.encode("utf-8"), output)
                self.assertEqual(source_digests(repository), before)

    def test_source_rejects_duplicate_unknown_and_missing_required_boilerplate_kinds(self) -> None:
        for invalid in ("duplicate-paragraph", "unknown-kind", "missing-short", "missing-long"):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository, paragraph="A supplied reviewed paragraph.")
                press_path = repository / ".identity/guidance/press-kit.json"
                press = json.loads(press_path.read_text(encoding="utf-8"))
                if invalid == "duplicate-paragraph":
                    duplicate = {**press["boilerplates"][-1], "id": "another-paragraph"}
                    press["boilerplates"].append(duplicate)
                elif invalid == "unknown-kind":
                    press["boilerplates"][-1]["kind"] = "unknown"
                else:
                    missing = invalid.removeprefix("missing-")
                    press["boilerplates"] = [item for item in press["boilerplates"] if item["kind"] != missing]
                write_json(press_path, press)
                with self.assertRaisesRegex(renderer.ProjectionError, "IDN1801.*boilerplate"):
                    renderer.build_projection(repository)

    def test_public_paragraph_cannot_replace_withheld_required_boilerplates(self) -> None:
        for kind in ("short", "long"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                add_press_source(repository, paragraph="A supplied reviewed paragraph.")
                press_path = repository / ".identity/guidance/press-kit.json"
                press = json.loads(press_path.read_text(encoding="utf-8"))
                next(item for item in press["boilerplates"] if item["kind"] == kind)["governance"]["visibility"] = "internal"
                write_json(press_path, press)
                self.assertEqual(renderer.validator.validate_identity(repository), [])
                with self.assertRaisesRegex(renderer.ProjectionError, "requires approved public short and long"):
                    renderer.build_projection(repository)

    def test_generated_output_cannot_mutate_or_enter_canonical_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            before = source_digests(repository)
            payload = renderer.build_package(*renderer.build_projection(repository))
            written = renderer.write_outputs(repository, Path("assets/identity/press-kit"), payload)
            self.assertEqual([path.relative_to(repository).as_posix() for path in written], sorted(
                path.relative_to(repository).as_posix() for path in written
            ))
            self.assertEqual(source_digests(repository), before)
            with self.assertRaisesRegex(renderer.ProjectionError, "canonical .identity"):
                renderer.write_outputs(repository, Path(".identity/press-kit"), payload)
            with self.assertRaisesRegex(renderer.ProjectionError, "normalized"):
                renderer.write_outputs(repository, Path("../outside"), payload)
            redirect = repository / "generated-redirect"
            redirect.symlink_to(repository / ".identity", target_is_directory=True)
            with self.assertRaisesRegex(renderer.ProjectionError, "symbolic link"):
                renderer.write_outputs(repository, Path("generated-redirect/press-kit"), payload)

    def test_validator_rejects_nonpublic_asset_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            press_path = repository / ".identity/guidance/press-kit.json"
            press = json.loads(press_path.read_text(encoding="utf-8"))
            press["assets"][0]["assetId"] = "legacy-wordmark"
            write_json(press_path, press)
            diagnostics = renderer.validator.validate_identity(repository)
            self.assertIn("IDN1801", {value.code for value in diagnostics})

    def test_organization_projection_uses_same_inheritance_model(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "organization"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            identity_path = repository / ".identity/identity.json"
            identity = json.loads(identity_path.read_text(encoding="utf-8"))
            identity["project"]["id"] = "example-organization"
            identity["project"]["displayName"] = "Example Organization"
            identity["project"]["repository"] = "https://example.invalid/example-organization"
            identity["project"]["kind"] = "organization"
            write_json(identity_path, identity)
            model, _ = renderer.build_projection(repository)
            self.assertEqual(model["project"]["kind"], "organization")
            self.assertEqual(model["inheritance"]["organizationLayers"], ["example-organization"])

    def test_cli_prints_one_format_or_writes_complete_package(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            add_press_source(repository)
            printed = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--format",
                    "json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(printed.returncode, 0, printed.stderr)
            self.assertEqual(json.loads(printed.stdout)["schema"], renderer.PRESS_KIT_SCHEMA)
            written = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER_PATH),
                    "--repository-root",
                    str(repository),
                    "--output-directory",
                    "assets/identity/press-kit",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(written.returncode, 0, written.stderr)
            self.assertIn("assets/identity/press-kit/press-kit.zip", written.stdout.splitlines())


if __name__ == "__main__":
    unittest.main()
