#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Verify Identity's approved mascot source and packaged variants offline."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import struct
import sys
from typing import Any, Sequence
import zlib


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MASCOT_SCHEMA = "identity.mascot-source/v1"
PACKAGE_SCHEMA = "identity.mascot-package/v1"
APPROVALS_SCHEMA = "identity.approvals/v1"
PROVENANCE_SCHEMA = "identity.provenance/v1"


@dataclass(frozen=True)
class PngInfo:
    """The PNG properties needed by the mascot publication gate."""

    width: int
    height: int
    alpha_min: int
    alpha_max: int


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject ambiguous JSON documents before interpreting their contracts."""

    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    """Read one unambiguous JSON object."""

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_file(repository_root: Path, value: Any) -> Path:
    """Resolve a normalized repository-relative file without following symlinks."""

    if not isinstance(value, str) or not value:
        raise ValueError("path must be a non-empty string")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError(f"path must be normalized and repository-relative: {value}")
    current = repository_root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"path may not traverse a symbolic link: {value}")
    if not current.is_file():
        raise ValueError(f"declared file does not exist: {value}")
    return current


def paeth(left: int, above: int, upper_left: int) -> int:
    """Return the PNG Paeth predictor."""

    prediction = left + above - upper_left
    distance_left = abs(prediction - left)
    distance_above = abs(prediction - above)
    distance_upper_left = abs(prediction - upper_left)
    if distance_left <= distance_above and distance_left <= distance_upper_left:
        return left
    if distance_above <= distance_upper_left:
        return above
    return upper_left


def unfilter_row(filter_type: int, row: bytes, previous: bytes, bytes_per_pixel: int) -> bytes:
    """Reverse one standard PNG scanline filter."""

    result = bytearray(len(row))
    for index, byte in enumerate(row):
        left = result[index - bytes_per_pixel] if index >= bytes_per_pixel else 0
        above = previous[index] if previous else 0
        upper_left = previous[index - bytes_per_pixel] if previous and index >= bytes_per_pixel else 0
        if filter_type == 0:
            predictor = 0
        elif filter_type == 1:
            predictor = left
        elif filter_type == 2:
            predictor = above
        elif filter_type == 3:
            predictor = (left + above) // 2
        elif filter_type == 4:
            predictor = paeth(left, above, upper_left)
        else:
            raise ValueError(f"unsupported PNG filter: {filter_type}")
        result[index] = (byte + predictor) & 0xFF
    return bytes(result)


def inspect_rgba_png(path: Path) -> PngInfo:
    """Validate an 8-bit non-interlaced RGBA PNG and inspect its alpha range."""

    contents = path.read_bytes()
    if not contents.startswith(PNG_SIGNATURE):
        raise ValueError(f"not a PNG: {path}")

    offset = len(PNG_SIGNATURE)
    width = height = 0
    idat = bytearray()
    saw_ihdr = False
    saw_iend = False
    while offset < len(contents):
        if offset + 12 > len(contents):
            raise ValueError(f"truncated PNG chunk: {path}")
        length = struct.unpack(">I", contents[offset : offset + 4])[0]
        chunk_type = contents[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_end = data_end + 4
        if crc_end > len(contents):
            raise ValueError(f"truncated PNG chunk payload: {path}")
        data = contents[data_start:data_end]
        expected_crc = struct.unpack(">I", contents[data_end:crc_end])[0]
        actual_crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        if expected_crc != actual_crc:
            raise ValueError(f"PNG chunk CRC mismatch: {path}")
        if chunk_type == b"IHDR":
            if saw_ihdr or length != 13:
                raise ValueError(f"invalid PNG IHDR: {path}")
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
                ">IIBBBBB", data
            )
            if (bit_depth, color_type, compression, filter_method, interlace) != (8, 6, 0, 0, 0):
                raise ValueError(f"PNG must be 8-bit non-interlaced RGBA: {path}")
            saw_ihdr = True
        elif chunk_type == b"IDAT":
            idat.extend(data)
        elif chunk_type == b"IEND":
            saw_iend = True
            break
        offset = crc_end

    if not saw_ihdr or not saw_iend or width < 1 or height < 1 or not idat:
        raise ValueError(f"PNG is missing required chunks: {path}")
    decoded = zlib.decompress(bytes(idat))
    row_length = width * 4
    expected_length = height * (row_length + 1)
    if len(decoded) != expected_length:
        raise ValueError(f"PNG decoded data length is invalid: {path}")

    alpha_min = 255
    alpha_max = 0
    previous = b""
    offset = 0
    for _ in range(height):
        filter_type = decoded[offset]
        filtered = decoded[offset + 1 : offset + 1 + row_length]
        row = unfilter_row(filter_type, filtered, previous, 4)
        alpha = row[3::4]
        alpha_min = min(alpha_min, min(alpha))
        alpha_max = max(alpha_max, max(alpha))
        previous = row
        offset += row_length + 1
    return PngInfo(width=width, height=height, alpha_min=alpha_min, alpha_max=alpha_max)


def verify(repository_root: Path) -> list[str]:
    """Return deterministic mascot contract and asset violations."""

    root = repository_root.resolve()
    errors: list[str] = []
    paths = {
        "source": root / "mascot/kern.character.json",
        "approval": root / "mascot/approval.json",
        "provenance": root / "mascot/provenance.json",
        "package": root / "assets/identity/mascot/manifest.json",
    }
    documents: dict[str, dict[str, Any]] = {}
    for label, path in paths.items():
        try:
            documents[label] = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"{label}: {error}")
    if errors:
        return sorted(errors)

    source = documents["source"]
    approval = documents["approval"]
    provenance = documents["provenance"]
    package = documents["package"]
    if source.get("schema") != MASCOT_SCHEMA:
        errors.append(f"source schema must be {MASCOT_SCHEMA}")
    if package.get("schema") != PACKAGE_SCHEMA:
        errors.append(f"package schema must be {PACKAGE_SCHEMA}")
    if approval.get("schema") != APPROVALS_SCHEMA:
        errors.append(f"approval schema must be {APPROVALS_SCHEMA}")
    if provenance.get("schema") != PROVENANCE_SCHEMA:
        errors.append(f"provenance schema must be {PROVENANCE_SCHEMA}")

    character_id = source.get("id")
    approval_id = source.get("approval")
    decisions = approval.get("decisions")
    decisions = decisions if isinstance(decisions, list) else []
    matching_decisions = [item for item in decisions if isinstance(item, dict) and item.get("id") == approval_id]
    if len(matching_decisions) != 1:
        errors.append("source approval must resolve to exactly one decision")
    else:
        decision = matching_decisions[0]
        if decision.get("status") != "approved":
            errors.append("mascot decision must be approved")
        if decision.get("subject") != f"mascot:{character_id}":
            errors.append("mascot decision subject does not match the character")
        if not str(decision.get("evidence", "")).startswith("https://"):
            errors.append("mascot decision requires HTTPS review evidence")

    character = source.get("character")
    if not isinstance(character, dict) or character.get("eyes", {}).get("count") != 3:
        errors.append("Kern must have exactly three eyes")
    if not isinstance(character, dict) or character.get("emblem", {}).get("integrated") is not True:
        errors.append("the identity kernel must be integrated into Kern's outfit")
    if source.get("status") != "approved":
        errors.append("canonical mascot source must be approved")

    canonical = source.get("canonicalAsset")
    canonical = canonical if isinstance(canonical, dict) else {}
    canonical_path: Path | None = None
    try:
        canonical_path = safe_file(root, canonical.get("path"))
        if sha256(canonical_path) != canonical.get("sha256"):
            errors.append("canonical mascot digest does not match local bytes")
        canonical_png = inspect_rgba_png(canonical_path)
        if canonical_png.alpha_min != 0 or canonical_png.alpha_max != 255:
            errors.append("canonical mascot must contain transparent and fully opaque pixels")
    except (OSError, ValueError, zlib.error) as error:
        errors.append(f"canonical asset: {error}")

    assets = provenance.get("assets")
    assets = assets if isinstance(assets, list) else []
    asset_id = canonical.get("assetId")
    matching_assets = [item for item in assets if isinstance(item, dict) and item.get("id") == asset_id]
    if len(matching_assets) != 1:
        errors.append("canonical asset must resolve to exactly one provenance record")
    else:
        asset = matching_assets[0]
        if asset.get("path") != canonical.get("path") or asset.get("sha256") != canonical.get("sha256"):
            errors.append("canonical source and provenance bytes disagree")
        asset_approval_id = asset.get("approval")
        asset_decisions = [
            item
            for item in decisions
            if isinstance(item, dict) and item.get("id") == asset_approval_id
        ]
        if (
            len(asset_decisions) != 1
            or asset_decisions[0].get("status") != "approved"
            or asset_decisions[0].get("subject") != asset_id
        ):
            errors.append("provenance does not resolve to an approved decision for the asset")
        license_value = asset.get("license")
        if not isinstance(license_value, dict) or license_value.get("status") != "approved":
            errors.append("mascot provenance license must be approved")

    if package.get("character") != character_id:
        errors.append("package character does not match the canonical source")
    derived = package.get("derivedFrom")
    derived = derived if isinstance(derived, dict) else {}
    if derived.get("path") != canonical.get("path") or derived.get("sha256") != canonical.get("sha256"):
        errors.append("package source does not match the canonical asset")
    generation = package.get("generation")
    generation = generation if isinstance(generation, dict) else {}
    try:
        safe_file(root, generation.get("record"))
    except ValueError as error:
        errors.append(f"generation record: {error}")
    guidance = package.get("guidance")
    guidance = guidance if isinstance(guidance, dict) else {}
    try:
        guidance_path = safe_file(root, guidance.get("path"))
        if guidance_path.parent != (root / "assets/identity/mascot"):
            errors.append("packaged mascot guidance is outside the output directory")
        if sha256(guidance_path) != guidance.get("sha256"):
            errors.append("packaged mascot guidance digest does not match local bytes")
    except (OSError, ValueError) as error:
        errors.append(f"package guidance: {error}")

    source_variants = source.get("variants")
    source_variants = source_variants if isinstance(source_variants, list) else []
    variants_by_id = {
        item.get("id"): item
        for item in source_variants
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    package_files = package.get("files")
    package_files = package_files if isinstance(package_files, list) else []
    declared_paths: set[Path] = set()
    declared_variant_ids: set[str] = set()
    for item in package_files:
        if not isinstance(item, dict):
            errors.append("package file entry must be an object")
            continue
        file_id = item.get("id")
        prefix = f"{character_id}-"
        variant_id = file_id.removeprefix(prefix) if isinstance(file_id, str) else ""
        declared_variant_ids.add(variant_id)
        variant = variants_by_id.get(variant_id)
        if variant is None:
            errors.append(f"package file does not resolve to a declared variant: {file_id}")
        elif item.get("minimumWidth") != variant.get("minimumWidth"):
            errors.append(f"minimum width disagrees for variant: {variant_id}")
        try:
            path = safe_file(root, item.get("path"))
            declared_paths.add(path.resolve())
            if path.parent != (root / "assets/identity/mascot"):
                errors.append(f"packaged mascot file is outside the output directory: {item.get('path')}")
            if path.stat().st_size != item.get("sizeBytes"):
                errors.append(f"size does not match for packaged mascot: {item.get('path')}")
            if sha256(path) != item.get("sha256"):
                errors.append(f"digest does not match for packaged mascot: {item.get('path')}")
            info = inspect_rgba_png(path)
            if (info.width, info.height) != (item.get("width"), item.get("height")):
                errors.append(f"dimensions do not match for packaged mascot: {item.get('path')}")
            if info.alpha_min != 0 or info.alpha_max != 255:
                errors.append(f"packaged mascot lacks real transparency: {item.get('path')}")
            if variant_id == "full" and canonical_path is not None and path.read_bytes() != canonical_path.read_bytes():
                errors.append("full mascot projection must exactly preserve the canonical master")
        except (OSError, ValueError, zlib.error) as error:
            errors.append(f"package file {file_id}: {error}")

    if declared_variant_ids != set(variants_by_id):
        errors.append("package variants do not exactly match the canonical variant inventory")
    output_directory = root / "assets/identity/mascot"
    actual_pngs = {path.resolve() for path in output_directory.glob("*.png") if path.is_file()}
    if actual_pngs != declared_paths:
        errors.append("packaged PNG inventory does not exactly match the manifest")
    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    """Build the stable verifier interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root containing mascot/ and assets/identity/mascot/.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run verification and return a process status suitable for CI."""

    arguments = build_parser().parse_args(argv)
    errors = verify(arguments.repository_root)
    if errors:
        print("mascot verification failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("mascot verification passed: character=kern, variants=3, transparency=rgba")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
