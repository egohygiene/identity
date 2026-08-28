#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Create a deterministic public Identity Brand Kit archive and manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path


TAG_PATTERN = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--stage-directory", required=True, type=Path)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--release-commit", required=True)
    return parser.parse_args()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_files(asset_root: Path) -> list[Path]:
    return sorted(path for path in asset_root.rglob("*") if path.is_file())


def source_digest(records: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(str(record["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(record["sha256"]).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_archive(path: Path, asset_root: Path, records: list[dict[str, object]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for record in records:
            relative_path = Path(str(record["path"]))
            info = zipfile.ZipInfo(f"identity-brand-kit/{relative_path.as_posix()}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, (asset_root / relative_path).read_bytes())


def main() -> int:
    arguments = parse_arguments()
    if TAG_PATTERN.fullmatch(arguments.release_tag) is None:
        raise RuntimeError("release tag must be a stable semantic version, for example v1.0.0")
    if COMMIT_PATTERN.fullmatch(arguments.release_commit) is None:
        raise RuntimeError("release commit must be a lowercase 40-character Git SHA")

    source_root = arguments.source_root.resolve()
    asset_root = source_root / "assets" / "identity"
    if not asset_root.is_dir():
        raise RuntimeError(f"Identity asset root is missing: {asset_root}")

    stage_directory = arguments.stage_directory.resolve()
    package_directory = stage_directory / "packages"
    package_directory.mkdir(parents=True, exist_ok=True)

    records = []
    for path in source_files(asset_root):
        relative_path = path.relative_to(asset_root)
        contents = path.read_bytes()
        records.append(
            {
                "path": relative_path.as_posix(),
                "sha256": sha256_bytes(contents),
                "sizeBytes": len(contents),
            }
        )

    version = arguments.release_tag.removeprefix("v")
    archive_name = f"identity-brand-kit-v{version}.zip"
    manifest_name = f"identity-brand-kit-v{version}.manifest.json"
    checksums_name = f"identity-brand-kit-v{version}.SHA256SUMS"
    archive_path = package_directory / archive_name
    manifest_path = package_directory / manifest_name
    checksums_path = package_directory / checksums_name

    write_archive(archive_path, asset_root, records)
    archive_sha256 = sha256_bytes(archive_path.read_bytes())
    manifest = {
        "schema": "identity.public-brand-kit-manifest/v1",
        "release": {
            "repository": "https://github.com/egohygiene/identity",
            "tag": arguments.release_tag,
            "commit": arguments.release_commit,
            "url": "https://github.com/egohygiene/identity/releases/tag/"
            + arguments.release_tag,
        },
        "sourceDigest": source_digest(records),
        "archive": {
            "path": archive_name,
            "sha256": archive_sha256,
            "sizeBytes": archive_path.stat().st_size,
        },
        "files": records,
    }
    write_json(manifest_path, manifest)
    manifest_sha256 = sha256_bytes(manifest_path.read_bytes())
    checksums_path.write_text(
        f"{archive_sha256}  {archive_name}\n{manifest_sha256}  {manifest_name}\n",
        encoding="utf-8",
    )

    print(
        "packaged public Brand Kit: "
        f"release={arguments.release_tag}, files={len(records)}, sourceDigest={manifest['sourceDigest']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"public Brand Kit package failed: {error}")
        raise SystemExit(1) from error
