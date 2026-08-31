#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Render the governed channel registry into deterministic public artifacts."""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Any, Sequence
import zipfile

import channel_registry
import render_design_system as design_system
import validate_identity as validator


OUTPUT_FILES = {
    "json": "channel-registry.json",
    "markdown": "channel-registry.md",
    "badges": "badges.md",
    "footer": "footer-links.json",
    "manifest": "channel-registry-manifest.json",
    "checksums": "SHA256SUMS",
    "archive": "channel-registry.zip",
}


class ProjectionError(channel_registry.ChannelRegistryError):
    """Raised when source cannot produce a safe channel package."""


def render_json(value: object) -> str:
    """Render stable, human-diffable JSON."""

    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def markdown_cell(value: str) -> str:
    """Render one safe Markdown table cell."""

    return value.replace("|", "\\|").replace("\n", "<br>")


def build_projection(repository_root: Path) -> dict[str, Any]:
    """Build the complete reviewed registry and active public channel views."""

    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")
    project = channel_registry.load_json(repository_root / ".identity/identity.json")
    source = channel_registry.source_for_project(repository_root, project)
    if source is None:
        raise ProjectionError("channel projection requires documents.channelRegistry source")
    channels = channel_registry.governed_channels(source)
    public = channel_registry.public_channels(source)
    artifacts = [
        {"id": "channel-registry-json", "label": "Channel registry data", "path": OUTPUT_FILES["json"], "mediaType": "application/json", "intendedUse": "Machine-readable reviewed channel lifecycle and public-link data."},
        {"id": "channel-registry-markdown", "label": "Channel registry review", "path": OUTPUT_FILES["markdown"], "mediaType": "text/markdown", "intendedUse": "Human-readable lifecycle and verification review."},
        {"id": "channel-registry-badges", "label": "Approved channel badges", "path": OUTPUT_FILES["badges"], "mediaType": "text/markdown", "intendedUse": "Markdown links for approved active channels only."},
        {"id": "channel-registry-footer", "label": "Approved footer links", "path": OUTPUT_FILES["footer"], "mediaType": "application/json", "intendedUse": "Accessible footer-link adapter for approved active channels only."},
        {"id": "channel-registry-manifest", "label": "Channel registry manifest", "path": OUTPUT_FILES["manifest"], "mediaType": "application/json", "intendedUse": "Source and file integrity evidence."},
        {"id": "channel-registry-checksums", "label": "Channel registry checksums", "path": OUTPUT_FILES["checksums"], "mediaType": "text/plain", "intendedUse": "SHA-256 checksums for immutable package contents."},
        {"id": "channel-registry-archive", "label": "Complete channel registry archive", "path": OUTPUT_FILES["archive"], "mediaType": "application/zip", "intendedUse": "Reproducible offline channel registry handoff."},
    ]
    return {
        "schema": channel_registry.PACKAGE_SCHEMA,
        "project": {
            key: project["project"][key]
            for key in ("id", "displayName", "repository", "tagline", "kind")
        },
        "source": {
            "digest": design_system.canonical_source_digest(repository_root),
            "sourceSchema": channel_registry.SOURCE_SCHEMA,
            "projectionVersion": channel_registry.PROJECTION_VERSION,
        },
        "registry": source["registry"],
        "channels": channels,
        "publicChannels": public,
        "artifacts": artifacts,
    }


def render_markdown(model: dict[str, Any]) -> str:
    """Render a maintainer-facing registry without hiding non-active states."""

    lines = [
        f"# {model['project']['displayName']} channel registry",
        "",
        f"Registry: `{model['registry']['id']}@{model['registry']['version']}`",
        "",
        "| Channel | Platform | Lifecycle | Verification | Handle | Canonical URL | Badge |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for value in model["channels"]:
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(str(item))
                for item in (
                    value["id"],
                    value["platform"]["label"],
                    value["lifecycle"]["state"],
                    value["verification"]["state"],
                    value["handle"] or "—",
                    value["canonicalUrl"] or "—",
                    "approved" if value["badge"]["approved"] else "withheld",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"Approved active public channels: {len(model['publicChannels'])}",
            "",
            "Credentials, recovery codes, private contact details, and authentication material are outside this public contract.",
            "",
        ]
    )
    return "\n".join(lines)


def render_badges(model: dict[str, Any]) -> str:
    """Render accessible Markdown links for active approved channels only."""

    lines = ["# Approved social and community links", ""]
    if not model["publicChannels"]:
        lines.append("No channels are currently approved for public badges.")
    else:
        lines.extend(
            f"- [{value['badge']['label']}]({value['url']})"
            for value in model["publicChannels"]
        )
    lines.append("")
    return "\n".join(lines)


def checksum_entry(value: bytes) -> dict[str, Any]:
    """Return one stable integrity record."""

    return {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value)}


def deterministic_zip(entries: dict[str, bytes]) -> bytes:
    """Build a reproducible ZIP with normalized ordering and metadata."""

    output = BytesIO()
    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(entries):
            normalized = PurePosixPath(name)
            if normalized.is_absolute() or name != normalized.as_posix() or any(
                part in {"", ".", ".."} for part in normalized.parts
            ):
                raise ProjectionError(f"archive entry path is unsafe: {name!r}")
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, entries[name])
    return output.getvalue()


def build_package(model: dict[str, Any]) -> dict[str, bytes]:
    """Build deterministic registry, adapters, integrity evidence, and archive."""

    outputs = {
        OUTPUT_FILES["json"]: render_json(model).encode("utf-8"),
        OUTPUT_FILES["markdown"]: render_markdown(model).encode("utf-8"),
        OUTPUT_FILES["badges"]: render_badges(model).encode("utf-8"),
        OUTPUT_FILES["footer"]: render_json(model["publicChannels"]).encode("utf-8"),
    }
    manifest = {
        "schema": "identity.channel-registry-package-manifest/v1",
        "version": channel_registry.PROJECTION_VERSION,
        "projectionSchema": channel_registry.PACKAGE_SCHEMA,
        "projectId": model["project"]["id"],
        "registry": model["registry"],
        "sourceDigest": model["source"]["digest"],
        "files": {name: checksum_entry(value) for name, value in sorted(outputs.items())},
    }
    outputs[OUTPUT_FILES["manifest"]] = render_json(manifest).encode("utf-8")
    outputs[OUTPUT_FILES["checksums"]] = (
        "\n".join(
            f"{checksum_entry(value)['sha256']}  {name}"
            for name, value in sorted(outputs.items())
        )
        + "\n"
    ).encode("utf-8")
    outputs[OUTPUT_FILES["archive"]] = deterministic_zip(outputs)
    return outputs


def output_directory(repository_root: Path, value: Path) -> Path:
    """Resolve generated output without allowing canonical-source writes."""

    relative = value.as_posix()
    if not validator.valid_relative_path(relative):
        raise ProjectionError("output directory must be normalized and repository-relative")
    if relative == ".identity" or relative.startswith(".identity/"):
        raise ProjectionError("generated channel output cannot be written into canonical .identity")
    current = repository_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionError("generated channel output cannot traverse a symbolic link")
    return repository_root / relative


def write_outputs(repository_root: Path, directory: Path, outputs: dict[str, bytes]) -> list[Path]:
    """Write a complete generated package atomically per file."""

    destination = output_directory(repository_root, directory)
    destination.mkdir(parents=True, exist_ok=True)
    written = []
    for name, value in sorted(outputs.items()):
        path = destination / name
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_bytes(value)
        os.replace(temporary, path)
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    """Build the stable offline command interface."""

    parser = argparse.ArgumentParser(description="Render approved Identity channel projections.")
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--format", choices=("json", "markdown", "badges", "footer"), default="json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Render one view to stdout or write the complete deterministic package."""

    arguments = build_parser().parse_args(argv)
    repository_root = arguments.repository_root.resolve()
    try:
        model = build_projection(repository_root)
        if arguments.output_directory is not None:
            write_outputs(repository_root, arguments.output_directory, build_package(model))
        elif arguments.format == "markdown":
            sys.stdout.write(render_markdown(model))
        elif arguments.format == "badges":
            sys.stdout.write(render_badges(model))
        elif arguments.format == "footer":
            sys.stdout.write(render_json(model["publicChannels"]))
        else:
            sys.stdout.write(render_json(model))
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ProjectionError) as error:
        print(f"channel registry projection failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
