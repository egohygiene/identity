# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Shared Rust/Python vectors and historical source-binding compatibility."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import render_design_system as design_system
import validate_identity as validator

VECTORS = json.loads((REPOSITORY_ROOT / "tests/fixtures/source-digest-v1.json").read_text(encoding="utf-8"))
VALID_FIXTURE = REPOSITORY_ROOT / "tests/fixtures/v1/valid/minimal"
HISTORICAL_DIGEST = "1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353"


def materialize(root: Path, case: dict) -> None:
    """Write exact vector bytes, preserving the declared creation order."""

    for relative in case["directories"]:
        (root / relative).mkdir(parents=True, exist_ok=True)
    for file in case["files"]:
        path = root / file["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(bytes.fromhex(file["hex"]))
    for link in case["links"]:
        path = root / link["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(link["target"], target_is_directory=link["directory"])


class SourceDigestTests(unittest.TestCase):
    """Use the same inventories, hashes, and path rules as the Rust adapter."""

    def check_vector(self, case: dict) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            materialize(root, case)
            if case["sha256"] is None:
                with self.assertRaises((OSError, ValueError)):
                    validator.canonical_source_digest(root)
                with self.assertRaises(design_system.ProjectionError):
                    design_system.canonical_source_digest(root)
            else:
                self.assertEqual(
                    [path.relative_to(root).as_posix() for path in validator.canonical_source_files(root)],
                    case["inventory"],
                )
                self.assertEqual(validator.canonical_source_digest(root), case["sha256"])
                self.assertEqual(design_system.canonical_source_digest(root), case["sha256"])

    def test_shared_inventory_and_digest_vectors(self) -> None:
        self.assertEqual(VECTORS["contract"], "egohygiene.identity.source-digest/v1")
        for case in VECTORS["cases"]:
            if not case["links"]:
                with self.subTest(case=case["id"]):
                    self.check_vector(case)

    def test_shared_symlink_vectors(self) -> None:
        # A missing OS privilege is visible as a skipped capability check, never
        # a successful vector. Supported CI runners must exercise these cases.
        with tempfile.TemporaryDirectory() as temporary:
            try:
                (Path(temporary) / "probe").symlink_to("absent")
            except OSError as error:
                self.skipTest(f"symbolic link creation unavailable: {error}")
        for case in VECTORS["cases"]:
            if case["links"]:
                with self.subTest(case=case["id"]):
                    self.check_vector(case)

    def test_shared_portable_path_vectors(self) -> None:
        for case in VECTORS["paths"]:
            with self.subTest(path=case["path"]):
                self.assertEqual(validator.valid_canonical_source_path(case["path"]), case["valid"])

    def test_unreferenced_symlinks_fail_authoritative_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(VALID_FIXTURE, root, dirs_exist_ok=True)
            try:
                (root / ".identity/unreferenced-link").symlink_to("absent")
            except OSError as error:
                self.skipTest(f"symbolic link creation unavailable: {error}")
            self.assertEqual(validator.validate_identity(root)[0].code, "IDN1003")
            diagnostics, _ = validator.validate_snapshot(root)
            self.assertEqual(diagnostics[0].code, "IDN1003")
            with self.assertRaises(design_system.ProjectionError):
                design_system.build_projections(root)

    @unittest.skipUnless(os.name == "nt", "junction reparse points require Windows")
    def test_windows_junctions_fail_inventory_and_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(VALID_FIXTURE, root, dirs_exist_ok=True)
            target = root / "outside"
            target.mkdir()
            subprocess.run(
                ["cmd", "/C", "mklink", "/J", str(root / ".identity/junction"), str(target)],
                check=True, capture_output=True,
            )
            with self.assertRaises(ValueError):
                validator.canonical_source_digest(root)
            self.assertEqual(validator.validate_identity(root)[0].code, "IDN1003")

    def test_historical_fixture_and_legacy_coexistence_preserve_compiler_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(VALID_FIXTURE, root, dirs_exist_ok=True)
            # Both the established fixture and v0 coexistence use the historical
            # compiler hash. Existing golden output bytes remain untouched.
            for legacy in (False, True):
                with self.subTest(legacy=legacy):
                    if legacy:
                        (root / ".identity/identity.toml").write_bytes(b"legacy source\n")
                    self.assertEqual(validator.validate_identity(root), [])
                    handbook, context = design_system.build_projections(root)
                    self.assertEqual(handbook["source"]["digest"], HISTORICAL_DIGEST)
                    self.assertEqual(context["source"]["digest"], HISTORICAL_DIGEST)

    def test_unreferenced_nonportable_entries_fail_source_validation(self) -> None:
        if os.name == "nt":
            self.skipTest("native Windows cannot materialize this invalid filename; shared path vectors still run")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(VALID_FIXTURE, root, dirs_exist_ok=True)
            (root / ".identity/unreferenced:stream").write_bytes(b"invalid portable path")
            self.assertEqual(validator.validate_identity(root)[0].code, "IDN1003")
            with self.assertRaises(design_system.ProjectionError):
                design_system.build_projections(root)

    @unittest.skipUnless(os.name == "posix", "non-UTF-8 filenames require a Unix filesystem")
    def test_non_utf8_names_and_special_files_fail_without_reading(self) -> None:
        for kind in ("non-utf8", "fifo"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                shutil.copytree(VALID_FIXTURE, root, dirs_exist_ok=True)
                if kind == "non-utf8":
                    path = os.fsencode(root / ".identity") + b"/invalid-\xff"
                    with open(path, "wb") as output:
                        output.write(b"must not be lossily renamed")
                else:
                    os.mkfifo(root / ".identity/pipe")
                with self.assertRaises(ValueError):
                    validator.canonical_source_digest(root)
                self.assertEqual(validator.validate_identity(root)[0].code, "IDN1003")


if __name__ == "__main__":
    unittest.main()
