# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Unexecuted starting regressions for the optional announcement-draft boundary."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from test_render_press_kit import VALID_FIXTURE, add_press_source, source_digests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_launch_document as launch


class LaunchDocumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name) / "consumer"
        shutil.copytree(VALID_FIXTURE, self.root)
        add_press_source(self.root)
        project = json.loads((self.root / ".identity/identity.json").read_text())["project"]
        self.request = {
            "schema": launch.REQUEST_SCHEMA,
            "template": "release-announcement",
            "projectId": project["id"],
            "boilerplateId": "short",
            "release": {
                "version": "1.2.3", "date": "2026-11-02",
                "url": "https://example.invalid/releases/1.2.3",
                "highlights": ["Synthetic fixture claim, awaiting owner review."],
            },
        }

    def test_draft_is_deterministic_optional_and_source_preserving(self) -> None:
        before = source_digests(self.root)
        first = launch.build_package(self.root, self.request)
        self.assertEqual(first, launch.build_package(self.root, self.request))
        self.assertEqual(set(first), {launch.DOCUMENT, launch.RECEIPT})
        receipt = json.loads(first[launch.RECEIPT])
        self.assertEqual(receipt["status"], "draft")
        self.assertEqual(receipt["projection"]["assets"], [])
        self.assertIn(b"Announcement draft", first[launch.DOCUMENT])
        self.assertNotIn(b"Selected brand assets", first[launch.DOCUMENT])
        self.assertEqual(before, source_digests(self.root))
        directory = launch.write_outputs(self.root, Path("build/announcement"), first)
        self.assertEqual(launch.verify_directory(directory), receipt)

    def test_selected_public_assets_retain_bytes_rights_and_approval(self) -> None:
        model, approved_bytes = launch.press_kit.build_projection(self.root)
        asset = model["assets"][0]
        self.request["assetIds"] = [asset["id"]]
        outputs = launch.build_package(self.root, self.request)
        receipt = json.loads(outputs[launch.RECEIPT])
        self.assertEqual(receipt["projection"]["assets"], [asset])
        raw = outputs[launch.asset_path(asset)]
        self.assertEqual(raw, approved_bytes[asset["downloadPath"]])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), asset["sha256"])
        self.assertEqual(receipt["projection"]["assets"][0]["license"], asset["license"])
        for field in ["assetIds", "boilerplateId"]:
            bad = copy.deepcopy(self.request)
            bad[field] = ["unknown-private-record"] if field == "assetIds" else "unknown-private-record"
            with self.subTest(field=field), self.assertRaises(launch.ProjectionError):
                launch.build_package(self.root, bad)

    def test_request_rejects_unknown_or_invented_inputs(self) -> None:
        mutations = [
            ("projectId", "different-project"), ("template", "publish-to-social"),
            ("extra", "not-allowed"), ("assetIds", ["../outside"]),
            ("assetIds", ["mark", "mark"]),
        ]
        for key, value in mutations:
            bad = copy.deepcopy(self.request)
            bad[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                launch.validate_request(bad, self.request["projectId"])
        for key, value in [
            ("date", "2026-02-30"), ("version", "latest"), ("highlights", []),
            ("url", "http://example.invalid/release"),
            ("url", "https://user:password@example.invalid/release"),
            ("url", "https://example.invalid/release\nextra"),
        ]:
            bad = copy.deepcopy(self.request)
            bad["release"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                launch.validate_request(bad, self.request["projectId"])

    def test_existing_outputs_source_paths_and_damaged_drafts_reject(self) -> None:
        outputs = launch.build_package(self.root, self.request)
        before = source_digests(self.root)
        with self.assertRaises(ValueError):
            launch.write_outputs(self.root, Path(".identity/announcement"), outputs)
        directory = launch.write_outputs(self.root, Path("build/announcement"), outputs)
        with self.assertRaises(FileExistsError):
            launch.write_outputs(self.root, Path("build/announcement"), outputs)
        self.assertEqual(before, source_digests(self.root))
        (directory / launch.DOCUMENT).write_text("changed announcement", encoding="utf-8")
        with self.assertRaises(launch.ProjectionError):
            launch.verify_directory(directory)
        (directory / launch.DOCUMENT).write_bytes(outputs[launch.DOCUMENT])
        (directory / "unexpected.txt").write_text("extra file", encoding="utf-8")
        with self.assertRaises(launch.ProjectionError):
            launch.verify_directory(directory)

    def test_supplied_text_does_not_activate_html_or_markdown(self) -> None:
        self.request["release"]["highlights"] = ["<script>alert(1)</script> [fake](javascript:alert(1))"]
        output = launch.build_package(self.root, self.request)[launch.DOCUMENT].decode()
        self.assertNotIn("<script>", output)
        self.assertIn("&lt;script&gt;", output)
        self.assertNotIn("[fake](javascript:", output)


if __name__ == "__main__":
    unittest.main()
