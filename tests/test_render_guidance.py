# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Golden and policy evidence for renderer-ready Identity guidance."""

from __future__ import annotations

import hashlib
from html import escape
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPOSITORY_ROOT / "scripts"
RENDERER_PATH = SCRIPTS_ROOT / "render_guidance.py"
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
EXPECTED = VALID_FIXTURE / "expected"
sys.path.insert(0, str(SCRIPTS_ROOT))
SPEC = importlib.util.spec_from_file_location("render_guidance", RENDERER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def source_digests(repository_root: Path) -> dict[str, str]:
    """Return stable digests for every canonical Identity source file."""

    identity_root = repository_root / ".identity"
    return {
        path.relative_to(repository_root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(identity_root.rglob("*"))
        if path.is_file()
    }


def governance_states(value: object) -> set[str]:
    """Collect lifecycle states from the renderer model recursively."""

    states: set[str] = set()
    if isinstance(value, dict):
        governance = value.get("governance")
        if isinstance(governance, dict) and isinstance(governance.get("state"), str):
            states.add(governance["state"])
        for child in value.values():
            states.update(governance_states(child))
    elif isinstance(value, list):
        for child in value:
            states.update(governance_states(child))
    return states


class BrandGuidanceRendererTests(unittest.TestCase):
    """Prove deterministic views, context lookup, and authority boundaries."""

    def test_all_formats_match_reviewed_golden_outputs(self) -> None:
        model = renderer.build_view_model(VALID_FIXTURE)
        schema = json.loads(
            (REPOSITORY_ROOT / "contracts/v1/brand-guidance.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(model), set(schema["required"]))
        for output_format, suffix in (
            ("json", "json"),
            ("markdown", "md"),
            ("html", "html"),
        ):
            with self.subTest(output_format=output_format):
                actual = renderer.render(model, output_format)
                expected = (EXPECTED / f"brand-guidance.{suffix}").read_text(
                    encoding="utf-8"
                )
                self.assertEqual(actual, expected)

    def test_candidate_and_every_decision_state_remain_visible(self) -> None:
        model = renderer.build_view_model(VALID_FIXTURE)
        self.assertEqual(
            governance_states(model),
            {"candidate", "approved", "rejected", "superseded"},
        )
        markdown = renderer.render_markdown(model)
        html = renderer.render_html(model)
        for state in ("candidate", "approved", "rejected", "superseded"):
            self.assertIn(state, markdown)
            self.assertIn(f"badge-{state}", html)

    def test_context_projection_selects_voice_and_applicable_rules(self) -> None:
        model = renderer.build_view_model(VALID_FIXTURE, "repository-readme")
        self.assertEqual(model["selectedContext"], "repository-readme")
        self.assertEqual([item["id"] for item in model["contexts"]], ["repository-readme"])
        self.assertEqual(
            {item["id"] for item in model["doDont"]},
            {"mark-clear-space", "mark-transformations", "localization-review"},
        )
        with self.assertRaisesRegex(renderer.GuidanceError, "unknown context"):
            renderer.build_view_model(VALID_FIXTURE, "missing-context")

    def test_download_and_legacy_policy_are_separate(self) -> None:
        model = renderer.build_view_model(VALID_FIXTURE)
        self.assertEqual([item["id"] for item in model["downloads"]], ["mark"])
        self.assertEqual(
            [item["id"] for item in model["legacyAssets"]],
            ["legacy-wordmark"],
        )
        legacy = model["legacyAssets"][0]
        self.assertEqual(legacy["availability"], "internal")
        self.assertEqual(legacy["replacement"], "mark")
        self.assertIsNone(legacy["downloadName"])

    def test_rendering_does_not_mutate_canonical_sources(self) -> None:
        before = source_digests(VALID_FIXTURE)
        model = renderer.build_view_model(VALID_FIXTURE)
        renderer.render_json(model)
        renderer.render_markdown(model)
        renderer.render_html(model)
        self.assertEqual(source_digests(VALID_FIXTURE), before)

    def test_cli_returns_context_json_and_rejects_source_overwrite(self) -> None:
        rendered = subprocess.run(
            [
                sys.executable,
                str(RENDERER_PATH),
                "--repository-root",
                str(VALID_FIXTURE),
                "--format",
                "json",
                "--context",
                "incident-update",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        self.assertEqual(
            [item["id"] for item in json.loads(rendered.stdout)["contexts"]],
            ["incident-update"],
        )
        public_model = json.loads(rendered.stdout)
        self.assertEqual(public_model["audience"], "public")
        self.assertNotIn("friendly-candidate", rendered.stdout)
        self.assertEqual(public_model["legacyAssets"], [])
        refused = subprocess.run(
            [
                sys.executable,
                str(RENDERER_PATH),
                "--repository-root",
                str(VALID_FIXTURE),
                "--format",
                "html",
                "--output",
                ".identity/generated-brand-kit.html",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(refused.returncode, 1)
        self.assertIn("cannot overwrite canonical .identity", refused.stderr)
        self.assertFalse((VALID_FIXTURE / ".identity/generated-brand-kit.html").exists())

    def test_invalid_legacy_policy_fails_before_rendering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "consumer"
            shutil.copytree(VALID_FIXTURE, repository)
            usage_path = repository / ".identity/guidance/usage.json"
            usage = json.loads(usage_path.read_text(encoding="utf-8"))
            usage["assets"][1]["availability"] = "public"
            usage_path.write_text(f"{json.dumps(usage, indent=2)}\n", encoding="utf-8")
            with self.assertRaisesRegex(renderer.GuidanceError, "IDN1603"):
                renderer.build_view_model(repository)

    def test_shared_public_cases_filter_every_output_and_preserve_review(self) -> None:
        cases = json.loads(
            (REPOSITORY_ROOT / "tests/fixtures/guidance-public-cases.json").read_text()
        )["cases"]
        for case in cases:
            with self.subTest(case=case["id"]), tempfile.TemporaryDirectory() as temporary:
                repository = Path(temporary) / "consumer"
                shutil.copytree(VALID_FIXTURE, repository)
                for update in case["updates"]:
                    path = repository / f".identity/guidance/{update['document']}.json"
                    document = json.loads(path.read_text())
                    tokens = update["pointer"].lstrip("/").split("/")
                    parent = document
                    for token in tokens[:-1]:
                        parent = parent[int(token)] if isinstance(parent, list) else parent[token]
                    key = int(tokens[-1]) if isinstance(parent, list) else tokens[-1]
                    parent[key] = update["value"]
                    path.write_text(json.dumps(document, indent=2) + "\n")
                before = source_digests(repository)
                # These are valid consumers: validity must not imply public visibility.
                self.assertEqual(renderer.validator.validate_identity(repository), [])
                public = renderer.build_view_model(repository, audience="public")
                review = renderer.build_view_model(repository, audience="review")
                self.assertEqual(governance_states(public), {"approved"})
                self.assertEqual(governance_states(review), {"candidate", "approved", "rejected", "superseded"})
                self.assertEqual(
                    {item["id"] for item in public["decisions"]},
                    renderer.approval_ids({key: value for key, value in public.items() if key != "decisions"}),
                )
                for output_format in ("json", "markdown", "html"):
                    output = renderer.render(public, output_format)
                    for phrase in case["withheld"]:
                        self.assertNotIn(phrase, output)
                        if output_format == "html":
                            self.assertNotIn(escape(phrase), output)
                    for phrase in case["retained"]:
                        self.assertIn(escape(phrase) if output_format == "html" else phrase, output)
                review_json = renderer.render_json(review)
                for phrase in case["withheld"]:
                    # A blocked active asset is not a download in either audience;
                    # its source remains intact and its decision stays in the review ledger.
                    if phrase not in case.get("review_omitted", []):
                        self.assertIn(phrase, review_json)
                if case["id"] == "withheld-singletons-and-containers":
                    for field in ("foundation", "localization", "accessibility", "legal"):
                        self.assertIsNone(public[field])
                        self.assertIsInstance(review[field], dict)
                    self.assertEqual([context["id"] for context in public["contexts"]], ["repository-readme"])
                    context = public["contexts"][0]
                    self.assertEqual(context["examples"], [])
                    self.assertEqual(context["antiExamples"], [])
                    self.assertEqual(context["characteristics"], [])
                    self.assertEqual(public["characteristics"], [])
                    self.assertNotIn("marks", {section["id"] for section in public["sections"]})
                    self.assertEqual(public["downloads"], [])
                    self.assertIn('<html lang="und">', renderer.render_html(public))
                    with self.assertRaisesRegex(renderer.GuidanceError, "unknown context"):
                        renderer.build_view_model(repository, "incident-update", audience="public")
                    review_context = renderer.build_view_model(repository, "incident-update", audience="review")
                    self.assertEqual([item["id"] for item in review_context["contexts"]], ["incident-update"])
                elif case["id"] == "approved-public-legacy":
                    self.assertEqual([asset["id"] for asset in public["legacyAssets"]], ["legacy-wordmark"])
                    self.assertEqual(public["legacyAssets"][0]["downloadName"], "example-product-legacy-wordmark.svg")
                    self.assertIn("LEGACY", renderer.render_html(public))
                self.assertEqual(source_digests(repository), before)

    def test_public_schema_preserves_strict_review_and_projected_context_shape(self) -> None:
        schema = json.loads((REPOSITORY_ROOT / "contracts/v1/brand-guidance.schema.json").read_text())
        voice_schema = json.loads((REPOSITORY_ROOT / "contracts/v1/voice.schema.json").read_text())
        source_context = voice_schema["$defs"]["context"]
        projected_context = schema["$defs"]["projectedContext"]
        self.assertEqual(projected_context["required"], source_context["required"])
        self.assertEqual(set(projected_context["properties"]), set(source_context["properties"]))
        review = schema["allOf"][0]
        self.assertEqual(review["if"]["properties"]["audience"], {"const": "review"})
        for field in ("foundation", "localization", "accessibility", "legal"):
            variants = schema["properties"][field]["oneOf"]
            self.assertIn({"type": "null"}, variants)
            self.assertIn(review["then"]["properties"][field], variants)


if __name__ == "__main__":
    unittest.main()
