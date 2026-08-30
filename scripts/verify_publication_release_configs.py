#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify release-bound Brand Kit publication configurations offline."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


INDEX_PATH = Path("publication/release-configs/index.json")
INDEX_SCHEMA = "identity.public-brand-kit-release-config-index/v1"
CONFIG_SCHEMA = "identity.public-brand-kit-config/v1"
STABLE_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--release-tag")
    parser.add_argument("--release-commit")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_repository_path(repository_root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value or value.startswith("/"):
        return None
    relative = Path(value)
    if ".." in relative.parts:
        return None
    resolved_root = repository_root.resolve()
    resolved = (resolved_root / relative).resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        return None
    return resolved


def verify_config(
    config: Any,
    source_root: Path,
    release_tag: str,
    release_commit: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["publication config must be a JSON object"]
    if config.get("schema") != CONFIG_SCHEMA:
        errors.append("publication config has an unexpected schema identity")
    if config.get("canonicalUrl") != "https://identity.egohygiene.io/":
        errors.append("publication config must preserve the canonical Brand Kit URL")
    release = config.get("release")
    expected_release = {
        "defaultTag": release_tag,
        "defaultCommit": release_commit,
    }
    if release != expected_release:
        errors.append("publication config is not bound to the selected release tag and commit")

    assets = config.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("publication config must select at least one release-owned asset")
        return errors
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"asset {index} must be an object")
            continue
        asset_id = asset.get("id")
        source_path = asset.get("sourcePath")
        if not isinstance(asset_id, str) or not asset_id:
            errors.append(f"asset {index} must have an id")
        elif asset_id in seen_ids:
            errors.append(f"publication config contains duplicate asset id: {asset_id}")
        else:
            seen_ids.add(asset_id)
        if not isinstance(source_path, str) or source_path.startswith("/") or ".." in Path(source_path).parts:
            errors.append(f"asset {asset_id or index} has an unsafe source path")
            continue
        if source_path in seen_paths:
            errors.append(f"publication config contains duplicate asset path: {source_path}")
        seen_paths.add(source_path)
        release_asset = source_root / "assets" / "identity" / source_path
        if not release_asset.is_file() or release_asset.stat().st_size == 0:
            errors.append(f"selected release does not contain publication asset: {source_path}")
    return errors


def verify_index(repository_root: Path) -> list[str]:
    errors: list[str] = []
    index_path = repository_root / INDEX_PATH
    try:
        index = load_json(index_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"unable to parse release-config index: {error}"]
    if not isinstance(index, dict) or set(index) != {"schema", "releases"}:
        return ["release-config index must contain only schema and releases"]
    if index.get("schema") != INDEX_SCHEMA:
        errors.append("release-config index has an unexpected schema identity")
    releases = index.get("releases")
    if not isinstance(releases, dict) or not releases:
        errors.append("release-config index must contain at least one compatibility mapping")
        return errors

    seen_paths: set[Path] = set()
    for release_tag, record in sorted(releases.items()):
        if not STABLE_TAG.fullmatch(release_tag):
            errors.append(f"compatibility mapping has an invalid stable tag: {release_tag}")
            continue
        if not isinstance(record, dict) or set(record) != {"commit", "config", "sha256", "reason"}:
            errors.append(f"compatibility mapping {release_tag} has unexpected fields")
            continue
        release_commit = record.get("commit")
        expected_digest = record.get("sha256")
        if not isinstance(release_commit, str) or not HEX_40.fullmatch(release_commit):
            errors.append(f"compatibility mapping {release_tag} must pin a full commit SHA")
        if not isinstance(expected_digest, str) or not HEX_64.fullmatch(expected_digest):
            errors.append(f"compatibility mapping {release_tag} must pin a SHA-256 config digest")
        config_path = safe_repository_path(repository_root, record.get("config"))
        if config_path is None:
            errors.append(f"compatibility mapping {release_tag} has an unsafe config path")
            continue
        if config_path in seen_paths:
            errors.append(f"compatibility mappings reuse a config path: {config_path}")
        seen_paths.add(config_path)
        if not config_path.is_file():
            errors.append(f"compatibility mapping {release_tag} config is missing")
            continue
        if sha256(config_path) != expected_digest:
            errors.append(f"compatibility mapping {release_tag} config digest drifted")
        try:
            config = load_json(config_path)
        except json.JSONDecodeError as error:
            errors.append(f"compatibility mapping {release_tag} config is invalid JSON: {error}")
            continue
        errors.extend(verify_config(config, repository_root, release_tag, str(release_commit)))
        if not isinstance(record.get("reason"), str) or not record["reason"].strip():
            errors.append(f"compatibility mapping {release_tag} must explain why it exists")
    return errors


def verify_selected_config(
    config_path: Path,
    source_root: Path,
    release_tag: str | None,
    release_commit: str | None,
) -> list[str]:
    if not release_tag or not STABLE_TAG.fullmatch(release_tag):
        return ["selected publication config requires a stable --release-tag"]
    if not release_commit or not HEX_40.fullmatch(release_commit):
        return ["selected publication config requires a full --release-commit"]
    try:
        config = load_json(config_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"unable to parse selected publication config: {error}"]
    return verify_config(config, source_root.resolve(), release_tag, release_commit)


def verify_repository(
    repository_root: Path,
    *,
    config_path: Path | None = None,
    source_root: Path | None = None,
    release_tag: str | None = None,
    release_commit: str | None = None,
) -> list[str]:
    resolved_root = repository_root.resolve()
    errors = verify_index(resolved_root)
    if config_path is not None:
        errors.extend(
            verify_selected_config(
                config_path.resolve(),
                (source_root or resolved_root).resolve(),
                release_tag,
                release_commit,
            )
        )
    return errors


def main() -> int:
    arguments = parse_arguments()
    errors = verify_repository(
        arguments.repository_root,
        config_path=arguments.config,
        source_root=arguments.source_root,
        release_tag=arguments.release_tag,
        release_commit=arguments.release_commit,
    )
    if errors:
        print("publication release-config verification failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("publication release-config verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
