# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Failure-boundary checks for source-preserving browser qualification."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location("qualify_browser", Path(__file__).resolve().parents[1] / "scripts/qualify_browser.py")
QUALIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUALIFY)


def inputs():
    image = "mcr.microsoft.com/playwright:v1.62.1-noble@sha256:" + "a" * 64
    profile = {
        "image": image, "platform": "linux/amd64", "playwright": "1.62.1",
        "packageManager": "pnpm@11.21.0", "chromium": {"colorProfile": "srgb", "version": "151.0.7922.34"},
        "settings": {"locale": "en-US", "timezoneId": "UTC"},
        "baseline": {"path": QUALIFY.BASELINE_PATH, "sha256": QUALIFY.APPROVED_BASELINE_SHA256, "approvalRevision": "b" * 40},
    }
    package = {"devDependencies": {"@playwright/test": "1.62.1"}, "packageManager": "pnpm@11.21.0"}
    registry = {"image": image, "platform": "linux/amd64", "index_digest": "sha256:" + "a" * 64}
    return profile, package, registry


def proof(directory, profile):
    for phase in ("positive", "negative", "restored"):
        target = directory / phase
        target.mkdir()
        (target / "report.json").write_text("{}\n")
    diff = directory / "negative/brand-kit-page-diff.png"
    diff.write_bytes(b"synthetic difference fixture, not browser evidence")
    receipt = {
        "status": "passed", "platform": "linux/amd64",
        "baseline": dict(profile["baseline"], unchanged=True),
        "settings": profile["settings"],
        "runtimes": {"playwright": profile["playwright"], "pnpm": "11.21.0"},
        "browser": {"version": profile["chromium"]["version"], "executableSha256": "e" * 64, "commandLine": ["--force-color-profile=srgb"], "settings": profile["settings"], "renderedFonts": [{"selector": "h1", "fonts": [{"familyName": "Arial"}]}]},
        "fonts": {"files": [{"path": "/font.ttf", "sha256": "f" * 64}], "configuration": [{"path": "/fonts.conf", "sha256": "d" * 64}]},
        "positive": {"exitCode": 0, "passed": 6, "failed": 0, "skipped": 0, "report": "positive/report.json"},
        "negative": {"exitCode": 1, "passed": 0, "failed": 1, "skipped": 0, "report": "negative/report.json", "expectedFailure": "screenshot-comparison", "baselineUnchanged": True, "diffArtifacts": [{"path": "negative/brand-kit-page-diff.png", "sha256": QUALIFY.sha256(diff.read_bytes())}]},
        "restored": {"exitCode": 0, "passed": 1, "failed": 0, "skipped": 0, "report": "restored/report.json"},
    }
    return receipt


def output(receipt, directory):
    (directory / "qualification.json").write_text(json.dumps(receipt))
    return QUALIFY.CONTAINER_MARKER + json.dumps(receipt)


class BrowserQualificationBoundaryTests(unittest.TestCase):
    def test_output_cannot_overwrite_source_or_reuse_stale_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            source = parent / "repository"
            source.mkdir()
            clean = parent / "clean"
            clean.mkdir()
            self.assertEqual(QUALIFY.output_destination(clean, source), clean.resolve())
            stale = parent / "stale"
            stale.mkdir()
            (stale / "qualification.json").write_text("earlier evidence")
            file = parent / "file"
            file.write_text("unchanged")
            for destination in (source, source / "nested", stale, file, parent / "mount,option"):
                with self.subTest(destination=destination):
                    with self.assertRaises(ValueError):
                        QUALIFY.output_destination(destination, source)
            redirect = parent / "redirect"
            try:
                redirect.symlink_to(source, target_is_directory=True)
            except (OSError, NotImplementedError):
                pass
            else:
                with self.assertRaises(ValueError):
                    QUALIFY.output_destination(redirect, source)
            self.assertEqual(file.read_text(), "unchanged")
            self.assertEqual((stale / "qualification.json").read_text(), "earlier evidence")
            self.assertFalse((source / "nested").exists())

    def test_mutable_images_mismatched_pins_or_changed_baseline_are_rejected(self):
        profile, package, registry = inputs()
        QUALIFY.validate_profile(profile, package, registry)
        cases = []
        for key, value in (("image", "mcr.microsoft.com/playwright:latest"), ("playwright", "1.62.2"), ("packageManager", "pnpm@12.0.0"), ("platform", "linux/arm64"), ("chromium", {})):
            cases.append(dict(profile, **{key: value}))
        cases.append(dict(profile, baseline=dict(profile["baseline"], sha256="c" * 64)))
        for candidate in cases:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    QUALIFY.validate_profile(candidate, package, registry)
        with self.assertRaises(ValueError):
            QUALIFY.validate_profile(profile, package, dict(registry, index_digest="sha256:" + "d" * 64))
        with self.assertRaises(ValueError):
            QUALIFY.validate_profile([], package, registry)

    def test_pulled_config_platform_and_digest_must_match_the_registry(self):
        profile, _, registry = inputs()
        identity = {"id": "sha256:" + "c" * 64, "os": "linux", "architecture": "amd64", "user": "", "entrypoint": None, "cmd": ["bash"], "repo_digests": [profile["image"]]}
        registry.update(config_digest=identity["id"], image_config={key: identity[key] for key in ("os", "architecture", "user", "entrypoint", "cmd")})
        QUALIFY.verify_registry_binding(profile, registry, identity)
        for key, value in (("id", "sha256:" + "d" * 64), ("architecture", "arm64"), ("repo_digests", []), ("cmd", ["node"])):
            with self.subTest(key=key):
                with self.assertRaises(RuntimeError):
                    QUALIFY.verify_registry_binding(profile, registry, dict(identity, **{key: value}))

    def test_failed_or_ambiguous_receipts_cannot_count_as_qualification(self):
        profile, _, _ = inputs()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            valid = proof(directory, profile)
            line = output(valid, directory)
            self.assertEqual(QUALIFY.container_receipt("ordinary logs\n" + line, profile, directory), valid)
            for text in ("ordinary logs", line + "\n" + line, output(dict(valid, status="failed"), directory)):
                with self.subTest(text=text):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(text, profile, directory)
            for phase, key, value in (("positive", "passed", 5), ("negative", "exitCode", 0), ("negative", "expectedFailure", "timeout"), ("restored", "skipped", 1)):
                candidate = copy.deepcopy(valid)
                candidate[phase][key] = value
                with self.subTest(phase=phase, key=key):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            for missing in ("runtimes", "browser", "fonts", "settings"):
                candidate = copy.deepcopy(valid)
                candidate.pop(missing)
                with self.subTest(missing=missing):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)

    def test_negative_difference_must_exist_inside_evidence_and_match_its_hash(self):
        profile, _, _ = inputs()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "evidence"
            directory.mkdir()
            valid = proof(directory, profile)
            for path, digest in (("../outside-diff.png", "a" * 64), ("negative/missing-diff.png", "a" * 64), ("negative/brand-kit-page-diff.png", "d" * 64)):
                candidate = copy.deepcopy(valid)
                candidate["negative"]["diffArtifacts"] = [{"path": path, "sha256": digest}]
                with self.subTest(path=path):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            line = output(valid, directory)
            (directory / "qualification.json").write_text("{}")
            with self.assertRaises(RuntimeError):
                QUALIFY.container_receipt(line, profile, directory)


if __name__ == "__main__":
    unittest.main()
