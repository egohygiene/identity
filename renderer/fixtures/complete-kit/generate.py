#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Regenerate bounded renderer inputs using a locally built native Identity CLI."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
DESTINATION = Path(__file__).resolve().parent
BASE = "47995976ae41415226bd6fb9400fbbd02777fca6"
MANTLE = "b08045acc1e982dd9424c1d8c91b0badd64744e8"
sys.path.insert(0, str(ROOT / "scripts"))
import verify_consumer_authoring as proof
import validate_identity as validator
import render_design_system as handbook
import render_press_kit as press


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--identity-binary", required=True, type=Path)
    parser.add_argument("--mantle-root", required=True, type=Path)
    args = parser.parse_args()
    binary = args.identity_binary.resolve(strict=True)
    mantle = args.mantle_root.resolve(strict=True)
    original = proof.inventory(mantle, excluded_names=frozenset({".git"}))
    diagnostics, snapshot = validator.validate_snapshot(mantle)
    assert not diagnostics
    source = proof.source_inventory(mantle, snapshot)
    revision = proof.checkout_revision(mantle, MANTLE, [p for p, v in source.items() if v["kind"] == "file"])
    assert revision["consumedFilesMatchRevision"]
    spec = importlib.util.spec_from_file_location("press_fixture", ROOT / "tests/test_render_press_kit.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    payload = {}
    cases = {}
    with tempfile.TemporaryDirectory(prefix="identity-kit-fixtures-") as temporary:
        for name, source_root in [("minimal", ROOT / "examples/v1/minimal"),
                                  ("expanded", ROOT / "tests/fixtures/v1/valid/minimal"),
                                  ("mantle", mantle)]:
            inventories = []
            for attempt in (1, 2):
                consumer = Path(temporary) / f"{name}-{attempt}"
                proof.copy_consumer(source_root, consumer, "assets/identity")
                if name == "expanded":
                    helper.add_press_source(consumer, paragraph="A supplied synthetic paragraph for complete Brand Kit handoff checks.")
                    targets_path = consumer / ".identity/targets/profiles.json"
                    targets = json.loads(targets_path.read_text())
                    targets["enabled"] = [{"id": p, "version": "1.0.0"} for p in
                                          ["core", "web", "github", "social", "tokens", "metadata", "archive"]]
                    targets["inapplicable"] = ["pwa", "docs"]
                    targets_path.write_text(json.dumps(targets, indent=2) + "\n")
                diagnostics, selected = validator.validate_snapshot(consumer)
                assert not diagnostics, diagnostics
                before = proof.source_inventory(consumer, selected)
                source_digest = validator.canonical_source_digest(consumer)
                result = proof.run_binary(binary, "v1-generate", consumer, "assets/identity")
                assert result.returncode == 0, result.stderr
                proof.verify_read_only(binary, consumer, "assets/identity", expect_success=True)
                proof.manifest_outputs(consumer, "assets/identity", source_digest)
                roots = {"native": consumer / "assets/identity"}
                if name == "expanded":
                    handbook.write_outputs(consumer, Path("build/handbook"), handbook.build_projections(consumer))
                    model, assets = press.build_projection(consumer)
                    press.write_outputs(consumer, Path("build/press-kit"), press.build_package(model, assets))
                    press.verify_package_directory(consumer / "build/press-kit")
                    roots.update(handbook=consumer / "build/handbook", press=consumer / "build/press-kit")
                assert proof.source_inventory(consumer, selected) == before
                files = {f"{part}/{p.relative_to(directory).as_posix()}": p.read_bytes()
                         for part, directory in roots.items() for p in sorted(directory.rglob("*")) if p.is_file()}
                inventories.append(files)
                if attempt == 1:
                    cases[name] = {"sourceDigest": source_digest, "sourceInputs": before,
                                   "inputsPreserved": True, "independentGenerations": 2,
                                   "generatedFiles": {p: {"sha256": proof.sha256(b), "bytes": len(b)} for p, b in files.items()},
                                   "synthetic": name != "mantle"}
                    payload.update({f"{name}/{p}": b for p, b in files.items()})
            assert inventories[0] == inventories[1]
    assert proof.inventory(mantle, excluded_names=frozenset({".git"})) == original
    archive_path = DESTINATION / "inputs.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, contents in sorted(payload.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, contents)
    receipt = {
        "purpose": "Exact generated renderer test inputs; no new approval, release or deployment.",
        "baseRevision": BASE, "nativeBinarySha256": proof.sha256(binary.read_bytes()),
        "mantle": {"repository": "egohygiene/mantle", **revision, "entireOriginalCheckoutPreserved": True},
        "cases": cases, "archiveSha256": proof.sha256(archive_path.read_bytes()),
        "limits": ["Expanded is a disposable synthetic fixture variant, not a real project approval.",
                   "Minimal and real Mantle input sources are unchanged.",
                   "Source/manifest and byte checks are local; actual renderer/browser results are separate exact-head evidence.",
                   "This test transport archive is not a distributable Brand Kit or a new product bundle."],
    }
    (DESTINATION / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"archiveBytes": archive_path.stat().st_size,
                      "cases": {k: len(v["generatedFiles"]) for k, v in cases.items()}, "passed": True}))


if __name__ == "__main__":
    main()
