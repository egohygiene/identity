# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Contract and adversarial tests for the approved mascot package."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
import zlib


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = REPOSITORY_ROOT / "scripts/verify_mascot.py"
SPEC = importlib.util.spec_from_file_location("verify_mascot", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verifier
SPEC.loader.exec_module(verifier)


def png_chunk(kind: bytes, data: bytes) -> bytes:
    """Build one valid PNG chunk for a focused parser fixture."""

    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def write_rgb_png(path: Path) -> None:
    """Write a valid opaque 1x1 RGB PNG without an alpha channel."""

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    pixels = zlib.compress(b"\x00\xff\xff\xff")
    path.write_bytes(
        verifier.PNG_SIGNATURE
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", pixels)
        + png_chunk(b"IEND", b"")
    )


class MascotVerifierTests(unittest.TestCase):
    """Prove byte binding, alpha validation, and source/package agreement."""

    def test_checked_in_mascot_package_is_valid(self) -> None:
        self.assertEqual(verifier.verify(REPOSITORY_ROOT), [])

    def test_manifest_digest_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPOSITORY_ROOT / "mascot", root / "mascot")
            shutil.copytree(
                REPOSITORY_ROOT / "assets/identity/mascot",
                root / "assets/identity/mascot",
            )
            icon = root / "assets/identity/mascot/kern-icon.png"
            icon.write_bytes(icon.read_bytes() + b"drift")

            errors = verifier.verify(root)

        self.assertTrue(any("kern-icon.png" in error and "size" in error for error in errors))
        self.assertTrue(any("kern-icon.png" in error and "digest" in error for error in errors))

    def test_opaque_rgb_png_is_not_accepted_as_transparency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            image = Path(temporary) / "opaque.png"
            write_rgb_png(image)

            with self.assertRaisesRegex(ValueError, "RGBA"):
                verifier.inspect_rgba_png(image)

    def test_manifest_and_character_contract_identities_are_stable(self) -> None:
        source = json.loads((REPOSITORY_ROOT / "mascot/kern.character.json").read_text())
        package = json.loads(
            (REPOSITORY_ROOT / "assets/identity/mascot/manifest.json").read_text()
        )
        self.assertEqual(source["schema"], verifier.MASCOT_SCHEMA)
        self.assertEqual(package["schema"], verifier.PACKAGE_SCHEMA)
        self.assertEqual(source["character"]["eyes"]["count"], 3)
        self.assertTrue(source["character"]["emblem"]["integrated"])
        self.assertEqual(
            package["guidance"]["sha256"],
            verifier.sha256(REPOSITORY_ROOT / package["guidance"]["path"]),
        )


if __name__ == "__main__":
    unittest.main()
