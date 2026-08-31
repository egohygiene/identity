#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Project approved Identity inputs onto pinned Aether social-surface targets."""

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

import render_design_system as design_system
import channel_registry
import validate_identity as validator


PACKAGE_SCHEMA = "identity.social-surface-package/v1"
MANIFEST_SCHEMA = "identity.social-surface-package-manifest/v1"
HANDOFF_SCHEMA = "identity.social-surface-press-kit-handoff/v1"
PROJECTION_VERSION = "1.0.0"
OUTPUT_FILES = {
    "json": "social-surfaces.json",
    "markdown": "social-surfaces.md",
    "handoff": "press-kit-handoff.json",
    "manifest": "social-surfaces-manifest.json",
    "checksums": "SHA256SUMS",
    "archive": "social-surfaces.zip",
}
MIME_TYPES = {
    ".avif": "image/avif",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}
FRESHNESS_WARNING = (
    "This package uses a dated, offline Aether catalog. Verify consequential or changed "
    "requirements against the linked live official source before production use."
)


class ProjectionError(ValueError):
    """Raised when validated source cannot produce a safe social package."""


def load_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON document."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"document must be an object: {path}")
    return value


def render_json(value: object) -> str:
    """Render stable, human-diffable JSON."""

    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def normalized_catalog_digest(path: Path) -> str:
    """Return Aether's sha256-utf8-lf digest for one catalog artifact."""

    normalized = (
        path.read_text(encoding="utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .encode("utf-8")
    )
    return hashlib.sha256(normalized).hexdigest()


def require_valid_source(repository_root: Path) -> None:
    """Refuse projection if any canonical Identity source boundary is invalid."""

    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")


def approval_record(
    approvals: dict[str, dict[str, Any]],
    identifier: str,
    subject: str,
) -> dict[str, str]:
    """Resolve one exact approved decision without inheriting unrelated authority."""

    decision = approvals.get(identifier)
    if (
        not isinstance(decision, dict)
        or decision.get("status") != "approved"
        or decision.get("subject") != subject
    ):
        raise ProjectionError(f"approval {identifier!r} does not authorize {subject!r}")
    return {"id": identifier, "subject": subject}


def public_assets(
    usage: dict[str, Any],
    provenance: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Return active public usage and byte-provenance records keyed by asset ID."""

    usage_assets = {
        item["id"]: item
        for item in usage["assets"]
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item.get("status") == "active"
        and item.get("availability") == "public"
        and isinstance(item.get("governance"), dict)
        and item["governance"].get("state") == "approved"
        and item["governance"].get("visibility") == "public"
    }
    provenance_assets = {
        item["id"]: item
        for item in provenance["assets"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    return usage_assets, provenance_assets


def safe_input_name(asset_id: str, source_path: str) -> str:
    """Return a deterministic package filename for an approved source asset."""

    suffix = Path(source_path).suffix.lower()
    if not suffix or not validator.IDENTIFIER.fullmatch(asset_id):
        raise ProjectionError(f"cannot derive a safe package name for asset {asset_id!r}")
    return f"{asset_id}{suffix}"


def selected_value(project: dict[str, Any], source: Any) -> dict[str, str] | None:
    """Resolve one closed project metadata selector without accepting authored copy."""

    if source is None:
        return None
    mapping = {
        "project.displayName": "displayName",
        "project.tagline": "tagline",
        "project.repository": "repository",
    }
    field = mapping.get(source)
    if field is None:
        raise ProjectionError(f"unsupported Identity value selector: {source!r}")
    value = project.get(field)
    if not isinstance(value, str) or not value:
        raise ProjectionError(f"selected Identity value is missing: {source}")
    return {"source": source, "value": value}


def projected_surface(record: dict[str, Any]) -> dict[str, Any]:
    """Project one Aether record without dropping provenance or unknowns."""

    dimensions = record.get("dimensions")
    if not isinstance(dimensions, dict):
        raise ProjectionError(f"surface {record.get('id')!r} has no usable dimensions")
    lifecycle = record.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("state") != "stable":
        raise ProjectionError(f"surface {record.get('id')!r} is not stable")
    return {
        "id": record["id"],
        "platform": record["platform"],
        "placement": record["placement"],
        "use": record["use"],
        "contentType": record["content_type"],
        "mediaFormat": record["media_format"],
        "dimensions": {
            "widthPx": dimensions["width_px"],
            "heightPx": dimensions["height_px"],
        },
        "aspectRatio": record["aspect_ratio"],
        "fileTypes": record["file_types"],
        "fileSizeLimitBytes": record["file_size_limit_bytes"],
        "durationLimitSeconds": record["duration_limit_seconds"],
        "safeZone": record["safe_zone"],
        "verification": record["verification"],
        "source": record["source"],
        "lifecycle": lifecycle["state"],
    }


def constraint_state(surface: dict[str, Any]) -> dict[str, Any]:
    """Expose absent requirements without guessing values from nearby records."""

    unknown = []
    if surface["aspectRatio"] is None:
        unknown.append("aspectRatio")
    if surface["fileTypes"] is None:
        unknown.append("fileTypes")
    if surface["fileSizeLimitBytes"] is None:
        unknown.append("fileSizeLimitBytes")
    if surface["mediaFormat"] == "video" and surface["durationLimitSeconds"] is None:
        unknown.append("durationLimitSeconds")
    if surface["safeZone"].get("state") == "unknown":
        unknown.append("safeZone")
    return {
        "state": "partial" if unknown else "complete",
        "unknownFields": unknown,
    }


def artifact(
    identifier: str,
    label: str,
    path: str,
    media_type: str,
    intended_use: str,
) -> dict[str, str]:
    """Build one renderer-neutral package artifact descriptor."""

    return {
        "id": identifier,
        "label": label,
        "path": path,
        "mediaType": media_type,
        "intendedUse": intended_use,
    }


def build_projection(
    repository_root: Path,
) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    """Build the social package model, approved input bytes, and Press Kit handoff."""

    require_valid_source(repository_root)
    identity = load_json(repository_root / ".identity/identity.json")
    documents = identity["documents"]
    source_path = documents.get("socialSurfaces")
    if not isinstance(source_path, str):
        raise ProjectionError("social projection requires documents.socialSurfaces source")
    source = load_json(repository_root / source_path)
    channel_source = channel_registry.source_for_project(repository_root, identity)
    channel_index = (
        channel_registry.public_channel_by_platform(channel_source)
        if channel_source is not None
        else {}
    )
    catalog_lock = source["catalog"]
    catalog_path = repository_root / catalog_lock["path"]
    catalog = load_json(catalog_path)
    actual_catalog_digest = normalized_catalog_digest(catalog_path)
    if actual_catalog_digest != catalog_lock["digest"]["value"]:
        raise ProjectionError("pinned Aether catalog digest does not match local bytes")
    catalog_metadata = catalog["catalog"]
    if (
        catalog_metadata["id"] != catalog_lock["id"]
        or catalog_metadata["version"] != catalog_lock["version"]
    ):
        raise ProjectionError("pinned Aether catalog identity or version does not match")
    if (
        catalog_metadata["lifecycle"]["state"] != "stable"
        or catalog_metadata["rights_review"]["state"] != "approved"
        or catalog_metadata["release"]["included"] is not True
    ):
        raise ProjectionError("Aether catalog is not stable, rights-approved, and release-included")

    approvals_document = load_json(repository_root / documents["approvals"])
    approvals = {
        item["id"]: item
        for item in approvals_document["decisions"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    usage = load_json(repository_root / documents["guidance"]["usage"])
    provenance = load_json(repository_root / documents["provenance"])
    usage_assets, provenance_assets = public_assets(usage, provenance)
    records = {
        item["id"]: item
        for item in catalog["records"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    defaults = {item["id"]: item for item in source["organizationDefaults"]}
    project_selection = source["project"]
    adopted = {item["id"]: item for item in project_selection["adopt"]}
    excluded = {item["id"]: item for item in project_selection["exclude"]}
    overrides = {item["id"]: item for item in project_selection["overrides"]}

    targets = []
    input_bytes: dict[str, bytes] = {}
    target_payloads: dict[str, bytes] = {}
    dynamic_artifacts = []
    for identifier in sorted(set(adopted) - set(excluded)):
        default = dict(defaults[identifier])
        override = overrides.get(identifier)
        if override is not None:
            for field in ("sourceAssetId", "copySource", "linkSource"):
                if field in override:
                    default[field] = override[field]
        surface_record = records.get(default["surfaceId"])
        if surface_record is None:
            raise ProjectionError(f"surface does not resolve in pinned catalog: {default['surfaceId']}")
        surface = projected_surface(surface_record)
        asset_id = default["sourceAssetId"]
        usage_asset = usage_assets.get(asset_id)
        provenance_asset = provenance_assets.get(asset_id)
        if usage_asset is None or provenance_asset is None:
            raise ProjectionError(f"social input is not an approved public asset: {asset_id}")
        source_asset_path = str(usage_asset["path"])
        bytes_value = (repository_root / source_asset_path).read_bytes()
        actual_asset_digest = hashlib.sha256(bytes_value).hexdigest()
        if actual_asset_digest != provenance_asset["sha256"]:
            raise ProjectionError(f"approved social input digest changed: {source_asset_path}")
        input_path = f"inputs/{safe_input_name(asset_id, source_asset_path)}"
        if input_path in input_bytes and input_bytes[input_path] != bytes_value:
            raise ProjectionError(f"social input package path is duplicated: {input_path}")
        input_bytes[input_path] = bytes_value
        constraints = constraint_state(surface)
        notes = []
        if "safeZone" in constraints["unknownFields"]:
            notes.append("Safe-zone geometry is unknown; a renderer must not invent one.")
        if surface["verification"].get("state") != "official":
            notes.append("Surface requirements are not verified as an official-source record.")
        target = {
            "id": identifier,
            "surface": surface,
            "content": {
                "assetId": asset_id,
                "inputPath": input_path,
                "mediaType": MIME_TYPES.get(Path(source_asset_path).suffix.lower(), "application/octet-stream"),
                "sha256": actual_asset_digest,
                "altText": provenance_asset["accessibility"]["altText"],
                "license": provenance_asset["license"],
                "origin": provenance_asset["origin"],
                "copy": selected_value(identity["project"], default["copySource"]),
                "link": selected_value(identity["project"], default["linkSource"]),
            },
            "constraints": constraints,
            "approvals": {
                "organizationDefault": approval_record(
                    approvals,
                    default["governance"]["approval"],
                    f"social-surface-default:{identifier}",
                )["id"],
                "projectAdoption": approval_record(
                    approvals,
                    adopted[identifier]["approval"],
                    f"social-surface-adoption:{identifier}",
                )["id"],
                "override": (
                    approval_record(
                        approvals,
                        override["approval"],
                        f"social-surface-override:{identifier}",
                    )["id"]
                    if override is not None
                    else None
                ),
            },
            "status": {"state": "ready-for-rendering", "notes": notes},
        }
        if channel_source is not None:
            target["channel"] = channel_index.get(surface["platform"].casefold())
        targets.append(target)
        target_path = f"targets/{identifier}.json"
        target_payloads[target_path] = render_json(target).encode("utf-8")
        dynamic_artifacts.append(
            artifact(
                f"target-{identifier}",
                f"{surface['platform']} {surface['placement']} target",
                target_path,
                "application/json",
                "Exact renderer-neutral dimensions, media constraints, safe-zone state, content mapping, and provenance.",
            )
        )

    for input_path in sorted(input_bytes):
        asset_id = Path(input_path).stem
        dynamic_artifacts.append(
            artifact(
                f"input-{asset_id}",
                f"Approved source input {asset_id}",
                input_path,
                MIME_TYPES.get(Path(input_path).suffix.lower(), "application/octet-stream"),
                "Approved canonical Identity input copied by digest for a downstream renderer.",
            )
        )

    fixed_artifacts = [
        artifact("social-package-json", "Social package data", OUTPUT_FILES["json"], "application/json", "Complete machine-readable social-surface projection."),
        artifact("social-package-markdown", "Social package review", OUTPUT_FILES["markdown"], "text/markdown", "Human-readable review of selected surfaces and constraints."),
        artifact("social-package-handoff", "Press Kit handoff", OUTPUT_FILES["handoff"], "application/json", "Framework-neutral handoff for an immutable Press or Media Kit consumer."),
        artifact("social-package-manifest", "Social package manifest", OUTPUT_FILES["manifest"], "application/json", "Integrity index for every generated package file."),
        artifact("social-package-checksums", "Social package checksums", OUTPUT_FILES["checksums"], "text/plain", "SHA-256 checksums for immutable package contents."),
        artifact("social-package-archive", "Complete social package archive", OUTPUT_FILES["archive"], "application/zip", "Deterministic offline archive for reviewed human or renderer handoff."),
    ]
    source_digest = design_system.canonical_source_digest(repository_root)
    model = {
        "schema": PACKAGE_SCHEMA,
        "project": {
            key: identity["project"][key]
            for key in ("id", "displayName", "repository", "tagline", "kind")
        },
        "source": {
            "digest": source_digest,
            "sourceSchema": validator.SOCIAL_SURFACE_SOURCE_SCHEMA,
            "projectionVersion": PROJECTION_VERSION,
        },
        "catalog": {
            "id": catalog_metadata["id"],
            "version": catalog_metadata["version"],
            "digest": {"algorithm": "sha256-utf8-lf", "value": actual_catalog_digest},
            "lifecycle": catalog_metadata["lifecycle"]["state"],
            "rightsReview": catalog_metadata["rights_review"]["state"],
            "sourceSnapshot": catalog_metadata["source_snapshot"],
        },
        "inheritance": {
            "availableOrganizationDefaults": sorted(defaults),
            "adopted": sorted(adopted),
            "excluded": sorted(excluded),
            "overrides": [
                {
                    key: value[key]
                    for key in ("id", "sourceAssetId", "copySource", "linkSource", "reason", "approval")
                    if key in value
                }
                for value in sorted(overrides.values(), key=lambda item: item["id"])
            ],
        },
        "targets": targets,
        "artifacts": fixed_artifacts + sorted(dynamic_artifacts, key=lambda item: item["path"]),
        "handoff": {
            "state": "publish-ready-input",
            "publicationAuthorized": False,
            "publisher": "human-or-external-tool",
            "freshnessWarning": FRESHNESS_WARNING,
        },
    }
    if channel_source is not None:
        model["channelRegistry"] = {
            "registry": channel_source["registry"],
            "activeChannels": len(channel_registry.public_channels(channel_source)),
        }
    handoff = {
        "schema": HANDOFF_SCHEMA,
        "projectId": identity["project"]["id"],
        "sourceDigest": source_digest,
        "catalog": {
            "id": catalog_metadata["id"],
            "version": catalog_metadata["version"],
            "digest": actual_catalog_digest,
        },
        "package": {
            "manifest": OUTPUT_FILES["manifest"],
            "checksums": OUTPUT_FILES["checksums"],
            "archive": OUTPUT_FILES["archive"],
        },
        "targets": [
            {
                "id": target["id"],
                "platform": target["surface"]["platform"],
                "placement": target["surface"]["placement"],
                "path": f"targets/{target['id']}.json",
            }
            for target in targets
        ],
        "publicationAuthorized": False,
    }
    return model, {**input_bytes, **target_payloads}, handoff


def markdown_cell(value: str) -> str:
    """Render one safe Markdown table cell."""

    return value.replace("|", "\\|").replace("\n", "<br>")


def render_markdown(model: dict[str, Any]) -> str:
    """Render a compact review surface without inventing missing constraints."""

    lines = [
        f"# {model['project']['displayName']} social-surface package",
        "",
        "This is a deterministic projection of approved Identity inputs onto a pinned Aether catalog.",
        "",
        f"Identity source digest: `{model['source']['digest']}`",
        "",
        f"Catalog: `{model['catalog']['id']}@{model['catalog']['version']}`",
        "",
        f"Catalog digest: `{model['catalog']['digest']['value']}`",
        "",
        FRESHNESS_WARNING,
        "",
        "| Selection | Platform | Channel | Placement | Use | Dimensions | Safe zone | Constraints |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for target in model["targets"]:
        surface = target["surface"]
        dimensions = surface["dimensions"]
        unknown = target["constraints"]["unknownFields"]
        constraints = "complete" if not unknown else f"unknown: {', '.join(unknown)}"
        lines.append(
            "| "
            + " | ".join(
                markdown_cell(str(value))
                for value in (
                    target["id"],
                    surface["platform"],
                    (
                        target["channel"]["label"]
                        if isinstance(target.get("channel"), dict)
                        else (
                            "not active"
                            if "channelRegistry" in model
                            else "not declared"
                        )
                    ),
                    surface["placement"],
                    surface["use"],
                    f"{dimensions['widthPx']}×{dimensions['heightPx']}",
                    surface["safeZone"]["state"],
                    constraints,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Each target JSON retains source URLs, verification, catalog lock, approvals, media limits, and unknown fields.",
            "",
            "This package is publish-ready input for a renderer or human review. It is not an instruction or authorization to publish.",
            "",
        ]
    )
    return "\n".join(lines)


def checksum_entry(value: bytes) -> dict[str, Any]:
    """Return one stable integrity record."""

    return {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value)}


def deterministic_zip(entries: dict[str, bytes]) -> bytes:
    """Build a reproducible ZIP with normalized ordering, modes, and timestamps."""

    output = BytesIO()
    with zipfile.ZipFile(output, mode="w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(entries):
            normalized = PurePosixPath(name)
            if (
                normalized.is_absolute()
                or name != normalized.as_posix()
                or any(part in {"", ".", ".."} for part in normalized.parts)
            ):
                raise ProjectionError(f"archive entry path is unsafe: {name!r}")
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, entries[name])
    return output.getvalue()


def build_package(
    model: dict[str, Any],
    generated_inputs: dict[str, bytes],
    handoff: dict[str, Any],
) -> dict[str, bytes]:
    """Return deterministic view models, inputs, manifest, checksums, and archive."""

    outputs = {
        OUTPUT_FILES["json"]: render_json(model).encode("utf-8"),
        OUTPUT_FILES["markdown"]: render_markdown(model).encode("utf-8"),
        OUTPUT_FILES["handoff"]: render_json(handoff).encode("utf-8"),
        **generated_inputs,
    }
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": PROJECTION_VERSION,
        "projectionSchema": PACKAGE_SCHEMA,
        "projectId": model["project"]["id"],
        "sourceDigest": model["source"]["digest"],
        "catalog": {
            "id": model["catalog"]["id"],
            "version": model["catalog"]["version"],
            "digest": model["catalog"]["digest"]["value"],
        },
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


def generated_output_directory(repository_root: Path, value: Path) -> Path:
    """Resolve generated output without allowing canonical-source or symlink writes."""

    relative = value.as_posix()
    if not validator.valid_relative_path(relative):
        raise ProjectionError("output directory must be normalized and repository-relative")
    if relative == ".identity" or relative.startswith(".identity/"):
        raise ProjectionError("generated social output cannot be written into canonical .identity")
    current = repository_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionError("output directory may not traverse a symbolic link")
    return repository_root / relative


def atomic_write(path: Path, value: bytes) -> None:
    """Replace one generated file without exposing a partial write."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def write_outputs(
    repository_root: Path,
    output_directory: Path,
    payload: dict[str, bytes],
) -> list[Path]:
    """Write generated package files outside canonical source."""

    destination = generated_output_directory(repository_root, output_directory)
    written = []
    for name, value in sorted(payload.items()):
        relative = PurePosixPath(name)
        if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
            raise ProjectionError(f"generated output path is unsafe: {name!r}")
        path = destination / relative
        atomic_write(path, value)
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    """Build the stable offline social-package command interface."""

    parser = argparse.ArgumentParser(
        description="Generate approved social-surface inputs from a pinned Aether catalog."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Consumer repository root containing .identity/identity.json.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Single projection format printed when no output directory is selected.",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        help="Repository-relative generated directory for the complete social package.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run projection and return a stable command status."""

    arguments = build_parser().parse_args(argv)
    repository_root = arguments.repository_root.resolve()
    try:
        model, inputs, handoff = build_projection(repository_root)
        if arguments.output_directory is None:
            output = render_json(model) if arguments.format == "json" else render_markdown(model)
            print(output, end="")
        else:
            payload = build_package(model, inputs, handoff)
            for path in write_outputs(repository_root, arguments.output_directory, payload):
                print(path.relative_to(repository_root).as_posix())
    except (OSError, ProjectionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
