#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Render an optional release-announcement draft from governed public source."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any, Sequence
from urllib.parse import quote, urlsplit

import render_press_kit as press_kit
import validate_identity as validator

REQUEST_SCHEMA = "identity.launch-document-request/v1"
RECEIPT_SCHEMA = "identity.launch-document/v1"
DOCUMENT = "release-announcement.md"
RECEIPT = "launch-document.json"
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]*\Z")
VERSION = re.compile(r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?\Z")


class ProjectionError(ValueError):
    """An explicit request or projection boundary is invalid."""


def closed(value: Any, required: set[str], optional: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict) or not required.issubset(value) or set(value) - required - (optional or set()):
        raise ProjectionError(f"expected exactly required fields {sorted(required)} and optional fields {sorted(optional or set())}")
    return value


def text(value: Any, label: str, *, limit: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise ProjectionError(f"{label} must be a non-empty text string of at most {limit} characters")
    return value


def validate_request(value: Any, project_id: str) -> dict[str, Any]:
    request = closed(value, {"schema", "template", "projectId", "boilerplateId", "release"}, {"assetIds"})
    if request["schema"] != REQUEST_SCHEMA or request["template"] != "release-announcement":
        raise ProjectionError("unsupported launch-document schema or template")
    if request["projectId"] != project_id:
        raise ProjectionError("launch request belongs to a different project")
    for key in ("projectId", "boilerplateId"):
        if not isinstance(request[key], str) or not IDENTIFIER.fullmatch(request[key]):
            raise ProjectionError(f"{key} must be a stable identifier")
    release = closed(request["release"], {"version", "date", "url", "highlights"})
    if not isinstance(release["version"], str) or not VERSION.fullmatch(release["version"]):
        raise ProjectionError("release.version must be an explicit semantic version")
    if not isinstance(release["date"], str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", release["date"]):
        raise ProjectionError("release.date must be an explicit YYYY-MM-DD date")
    date.fromisoformat(release["date"])
    url = text(release["url"], "release.url")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or any(c.isspace() or ord(c) < 32 for c in url) or any(c in url for c in '<>"\\'):
        raise ProjectionError("release.url must be an absolute HTTPS URL without credentials or whitespace")
    highlights = release["highlights"]
    if not isinstance(highlights, list) or not 1 <= len(highlights) <= 20:
        raise ProjectionError("release.highlights must contain one to twenty supplied claims")
    for item in highlights:
        text(item, "release highlight")
    assets = request.get("assetIds", [])
    if not isinstance(assets, list) or len(assets) > 20 or any(not isinstance(item, str) or not IDENTIFIER.fullmatch(item) for item in assets) or len(set(assets)) != len(assets):
        raise ProjectionError("assetIds must be at most twenty unique stable identifiers")
    return request


def markdown(value: str) -> str:
    """Keep supplied prose literal rather than interpreting embedded HTML/Markdown."""
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([\\`*_{}\[\]()#+.!|~\-])", r"\\\1", value)


def asset_path(asset: dict[str, Any]) -> str:
    identifier = asset.get("id")
    relative = asset.get("downloadPath")
    if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier) or not validator.valid_relative_path(relative):
        raise ProjectionError("selected Press Kit asset has an unsafe identity/path")
    return f"assets/{identifier}/{PurePosixPath(relative).name}"


def render_markdown(projection: dict[str, Any], request: dict[str, Any]) -> str:
    project = projection["project"]
    boilerplate = projection["boilerplate"]
    release = request["release"]
    lines = [
        f"# {markdown(project['displayName'])} {markdown(release['version'])}", "",
        "> Announcement draft — review supplied facts and wording before publication.", "",
        f"Release date: {markdown(release['date'])}", "", markdown(boilerplate["text"]), "",
        "## What changed", "",
    ]
    lines.extend(f"- {markdown(item).replace(chr(10), ' ')}" for item in release["highlights"])
    lines.extend(["", f"[Read the supplied release notes](<{release['url']}>)", ""])
    if projection["assets"]:
        lines.extend(["## Selected brand assets", ""])
        for asset in projection["assets"]:
            lines.extend([
                f"### {markdown(asset['label'])}", "",
                f"[Download approved source asset](<{quote(asset_path(asset), safe='/')}>)", "",
                f"Alternative text: {markdown(asset['altText'])}", "",
                f"License and attribution: {markdown(json.dumps(asset['license'], sort_keys=True, ensure_ascii=False))}", "",
                f"Usage: {markdown(json.dumps(asset['usage'], sort_keys=True, ensure_ascii=False))}", "",
                markdown(asset["notes"]), "",
            ])
    lines.extend([
        "## Source and review", "",
        f"Brand source digest: `{projection['sourceDigest']}`.",
        f"Public boilerplate: `{boilerplate['id']}`; source approval: `{boilerplate['approval']['id']}`.", "",
        "Brand copy and selected assets retain their source rights and approval. Release version, date, link and claims are supplied by the project owner and remain draft material. This tool does not verify a release, approve changing claims, publish or post anything.", "",
    ])
    return "\n".join(lines)


def build_package(repository_root: Path, request: Any) -> dict[str, bytes]:
    model, asset_bytes = press_kit.build_projection(repository_root)
    request = validate_request(request, model["project"]["id"])
    boilerplate = next((item for item in model["boilerplates"] if item["id"] == request["boilerplateId"]), None)
    if boilerplate is None:
        raise ProjectionError("selected boilerplate is absent from the approved public Press Kit")
    by_id = {item["id"]: item for item in model["assets"]}
    selected = []
    files = {}
    for identifier in request.get("assetIds", []):
        asset = by_id.get(identifier)
        if asset is None:
            raise ProjectionError(f"asset is absent from the approved public Press Kit: {identifier}")
        contents = asset_bytes[asset["downloadPath"]]
        if hashlib.sha256(contents).hexdigest() != asset["sha256"]:
            raise ProjectionError("selected asset bytes disagree with their source digest")
        selected.append(asset)
        files[asset_path(asset)] = contents
    projection = {
        "project": {key: model["project"][key] for key in ("id", "displayName")},
        "sourceDigest": model["source"]["digest"],
        "boilerplate": boilerplate,
        "assets": selected,
    }
    files[DOCUMENT] = render_markdown(projection, request).encode("utf-8")
    receipt = {
        "schema": RECEIPT_SCHEMA, "status": "draft", "request": request,
        "projection": projection,
        "files": {name: press_kit.checksum_entry(raw) for name, raw in sorted(files.items())},
    }
    files[RECEIPT] = press_kit.render_json(receipt).encode("utf-8")
    return files


def read_owned(root: Path, relative: str) -> bytes:
    if not validator.valid_relative_path(relative):
        raise ProjectionError("unsafe launch-document file path")
    file = root / relative
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ProjectionError("launch-document inputs may not be symbolic links")
    if not file.is_file() or not file.resolve().is_relative_to(root):
        raise ProjectionError("launch-document artifact escapes its directory")
    return file.read_bytes()


def verify_directory(directory: Path) -> dict[str, Any]:
    if directory.is_symlink():
        raise ProjectionError("launch-document root may not be a symbolic link")
    root = directory.resolve(strict=True)
    receipt = closed(json.loads(read_owned(root, RECEIPT), object_pairs_hook=validator.object_without_duplicates), {"schema", "status", "request", "projection", "files"})
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["status"] != "draft":
        raise ProjectionError("unknown launch-document receipt or non-draft status")
    projection = closed(receipt["projection"], {"project", "sourceDigest", "boilerplate", "assets"})
    project = closed(projection["project"], {"id", "displayName"})
    text(project["displayName"], "project display name")
    if not isinstance(projection["sourceDigest"], str) or not re.fullmatch(r"[a-f0-9]{64}", projection["sourceDigest"]):
        raise ProjectionError("invalid brand source digest")
    request = validate_request(receipt["request"], project["id"])
    boilerplate = projection["boilerplate"]
    if not isinstance(boilerplate, dict) or boilerplate.get("id") != request["boilerplateId"] or not isinstance(boilerplate.get("approval"), dict):
        raise ProjectionError("selected boilerplate identity/approval is missing")
    text(boilerplate.get("text"), "boilerplate text", limit=100000)
    text(boilerplate["approval"].get("id"), "boilerplate approval")
    assets = projection["assets"]
    if not isinstance(assets, list) or any(not isinstance(item, dict) for item in assets) or [item.get("id") for item in assets] != request.get("assetIds", []):
        raise ProjectionError("receipt assets differ from the explicit selection")
    expected = {DOCUMENT: render_markdown(projection, request).encode("utf-8")}
    for asset in assets:
        relative = asset_path(asset)
        raw = read_owned(root, relative)
        if hashlib.sha256(raw).hexdigest() != asset.get("sha256"):
            raise ProjectionError("selected launch-document asset checksum mismatch")
        expected[relative] = raw
    checksums = {name: press_kit.checksum_entry(raw) for name, raw in sorted(expected.items())}
    if receipt["files"] != checksums:
        raise ProjectionError("launch-document inventory/checksums differ")
    actual = set()
    for item in root.rglob("*"):
        if item.is_symlink() or (not item.is_dir() and not item.is_file()):
            raise ProjectionError("unsupported entry in launch-document directory")
        if item.is_file():
            actual.add(item.relative_to(root).as_posix())
    if actual != set(expected) | {RECEIPT}:
        raise ProjectionError("launch-document directory contains missing or extra files")
    for relative, raw in expected.items():
        if read_owned(root, relative) != raw:
            raise ProjectionError("launch-document prose differs from its supplied source/request")
    return receipt


def write_outputs(repository_root: Path, value: Path, outputs: dict[str, bytes]) -> Path:
    target = press_kit.generated_output_directory(repository_root, value)
    target.mkdir(parents=True, exist_ok=False)
    # A receipt is written last. Interrupted output is incomplete and is never
    # silently overwritten or accepted by verification.
    for relative in sorted(outputs, key=lambda item: (item == RECEIPT, item)):
        file = target / relative
        file.parent.mkdir(parents=True, exist_ok=True)
        with file.open("xb") as stream:
            stream.write(outputs[relative])
    return target


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--verify-directory", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.verify_directory is not None:
            if any(value is not None for value in (args.repository_root, args.request, args.output_directory)):
                parser.error("--verify-directory cannot be combined with generation arguments")
            verify_directory(args.verify_directory)
            print("Launch-document draft inventory verified; approval/publication are separate.")
            return 0
        if any(value is None for value in (args.repository_root, args.request, args.output_directory)):
            parser.error("generation requires --repository-root, --request and --output-directory")
        if args.request.stat().st_size > 128 * 1024:
            raise ProjectionError("launch request exceeds 128 KiB")
        request = json.loads(args.request.read_text(encoding="utf-8"), object_pairs_hook=validator.object_without_duplicates)
        root = args.repository_root.resolve(strict=True)
        target = write_outputs(root, args.output_directory, build_package(root, request))
        print(f"Wrote announcement draft to {target}; review before publication.")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Launch document: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
