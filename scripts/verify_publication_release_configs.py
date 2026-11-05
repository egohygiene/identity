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
import subprocess
import sys
import types
from typing import Any
from urllib.parse import unquote


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
    if config.get("sourceMode") == "native-v1":
        allowed = {"$schema", "schema", "sourceMode", "canonicalUrl", "release", "assetBaseUrl",
                   "browserAssets", "nativeInputs", "openGraphImage"}
        if set(config) - allowed:
            errors.append("native config must not restate project/token/asset/guidance facts")
        if release != {"defaultTag": release_tag, "binding": "selected-annotated-tag"}:
            errors.append("native config must select its stable annotated-tag binding")
        asset_root = source_root / "assets/identity"
        for relative in [".identity-manifest.json", "packages/renderer/brand-kit.view-model.json"]:
            path = native_input_path(asset_root, relative)
            if path is None or not path.is_file() or path.stat().st_size == 0:
                errors.append(f"native release artifact is absent: {relative}")
        inputs = config.get("nativeInputs", {})
        if not isinstance(inputs, dict) or set(inputs) - {"designSystem", "pressKit"}:
            errors.append("nativeInputs must contain only selected designSystem/pressKit directories")
        else:
            for role, value in inputs.items():
                path = native_input_path(source_root, value)
                if path is None or not path.is_dir():
                    errors.append(f"native input is unsafe or absent: {role}")
        browser = config.get("browserAssets", {})
        if not isinstance(browser, dict) or set(browser) - {"icon", "appleTouchIcon", "manifest"}:
            errors.append("native browserAssets contains unsupported roles")
        else:
            for role, value in [*browser.items(), *([("openGraphImage", config["openGraphImage"])] if "openGraphImage" in config else [])]:
                path = native_input_path(asset_root, value)
                if path is None or not path.is_file() or path.stat().st_size == 0:
                    errors.append(f"native browser/social asset is unsafe or absent: {role}")
        return errors
    if config.get("sourceMode") not in (None, "legacy-assets"):
        errors.append("publication config has an unsupported source mode")
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


def native_input_path(root: Path, value: Any) -> Path | None:
    """Native config selects confined generated artifacts, never canonical source."""
    if not isinstance(value, str) or not value or value.startswith("/"):
        return None
    parts = [unquote(part) for part in value.split("/")]
    if any(not part or part in {".", ".."} or part.casefold() in {".identity", ".git", ".aws", ".agents", ".codex"} or
           any(character in part for character in "\\/%:?#") or
           any(ord(character) < 32 or ord(character) == 127 for character in part) for part in parts):
        return None
    path = (root / Path(*parts)).resolve()
    return path if root.resolve() in path.parents else None


def verify_native_release_bytes(config: dict[str, Any], source_root: Path, release_commit: str) -> list[str]:
    """Bind generated inputs and config to selected Git blobs, not just checkout HEAD."""
    source_root = source_root.resolve()
    roots = [source_root / ".identity", source_root / "assets/identity",
             source_root / "publication/identity-brand-kit.config.json"]
    for value in config.get("nativeInputs", {}).values():
        path = native_input_path(source_root, value)
        if path is not None:
            roots.append(path)
    selected = [path.relative_to(source_root).as_posix() for path in roots]
    tree = subprocess.run(["git", "-C", str(source_root), "ls-tree", "-r", "-z", release_commit, "--", *selected],
                          check=True, capture_output=True).stdout
    blobs: dict[str, tuple[str, str]] = {}
    for record in tree.split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            if kind != "blob":
                raise ValueError("native release inputs must use ordinary committed files")
            blobs[name.decode("utf-8")] = (mode, oid)
    files: set[Path] = set()
    for root in roots:
        if root.is_dir():
            files.update(path for path in root.rglob("*") if path.is_file() or path.is_symlink())
        else:
            files.add(root)
    errors = []
    for path in sorted(files):
        relative = path.relative_to(source_root).as_posix()
        expected = blobs.get(relative)
        if path.is_symlink() or expected is None or expected[0] not in {"100644", "100755"}:
            errors.append(f"native release input is not an ordinary selected Git blob: {relative}")
            continue
        content = path.read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()
        if oid != expected[1]:
            errors.append(f"native release input differs from the selected commit: {relative}")
    for relative in set(blobs) - {path.relative_to(source_root).as_posix() for path in files}:
        errors.append(f"committed native release input is absent: {relative}")
    return errors


def verify_native_source_binding(source_root: Path) -> list[str]:
    """The release-source gate validates canonical source; renderers still read artifacts only."""
    validator_path = Path(__file__).with_name("validate_identity.py")
    validator = types.ModuleType("_identity_publication_validator")
    sys.modules[validator.__name__] = validator
    exec(compile(validator_path.read_text(encoding="utf-8"), str(validator_path), "exec"), validator.__dict__)
    diagnostics = validator.validate_identity(source_root)
    if diagnostics:
        return [f"native canonical source is invalid: {item.code} {item.path}: {item.message}" for item in diagnostics]
    expected = validator.canonical_source_digest(source_root)
    manifest = load_json(source_root / "assets/identity/.identity-manifest.json")
    if not isinstance(manifest, dict) or manifest.get("schema") != "identity.compiler-manifest/v1":
        return ["native compiler manifest has an unsupported shape/schema"]
    if manifest.get("sourceDigest") != expected:
        return ["native compiler manifest does not match the selected release's canonical source"]
    return []


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
        if isinstance(config, dict) and config.get("sourceMode") == "native-v1":
            errors.append("native configurations must be release-owned, never compatibility fallbacks")
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
    errors = verify_config(config, source_root.resolve(), release_tag, release_commit)
    if isinstance(config, dict) and config.get("sourceMode") == "native-v1":
        resolved_config = config_path.resolve()
        if resolved_config != (source_root / "publication/identity-brand-kit.config.json").resolve() or \
                source_root.resolve() not in resolved_config.parents:
            errors.append("native configuration must come from the selected release tree")
        try:
            head = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"],
                                  check=True, capture_output=True, text=True).stdout.strip()
            if head != release_commit:
                errors.append("native source checkout does not match the selected release commit")
            if not errors:
                errors.extend(verify_native_release_bytes(config, source_root, release_commit))
            if not errors:
                errors.extend(verify_native_source_binding(source_root.resolve()))
        except (OSError, ValueError, subprocess.CalledProcessError):
            errors.append("native publication requires the verified release Git checkout")
    return errors


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
