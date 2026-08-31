#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Project reviewed Identity Press Kit source into deterministic public artifacts."""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
from typing import Any, Sequence
import zipfile

import render_design_system as design_system
import channel_registry
import validate_identity as validator

PRESS_KIT_SCHEMA = "identity.press-kit/v1"
PACKAGE_SCHEMA = "identity.press-kit-package/v1"
PROJECTION_VERSION = "1.0.0"
SOCIAL_HANDOFF_SCHEMA = "identity.social-surface-press-kit-handoff/v1"
SOCIAL_MANIFEST_SCHEMA = "identity.social-surface-package-manifest/v1"
OUTPUT_FILES = {
    "json": "press-kit.json",
    "markdown": "press-kit.md",
    "manifest": "press-kit-manifest.json",
    "checksums": "SHA256SUMS",
    "archive": "press-kit.zip",
}
MIME_TYPES = {
    ".avif": "image/avif",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
}


class ProjectionError(ValueError):
    """Raised when validated source cannot produce a safe Press Kit projection."""


def load_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON document."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"document must be an object: {path}")
    return value


def is_public(value: dict[str, Any]) -> bool:
    """Return whether a governed record is approved for public projection."""

    governance = value.get("governance")
    return (
        isinstance(governance, dict)
        and governance.get("state") == "approved"
        and governance.get("visibility") == "public"
        and isinstance(governance.get("approval"), str)
    )


def approval_record(value: dict[str, Any], approvals: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Return the reviewed decision identity for one approved public record."""

    governance = value.get("governance")
    if not isinstance(governance, dict) or not isinstance(governance.get("approval"), str):
        raise ProjectionError("public Press Kit record has no approval identifier")
    approval_id = governance["approval"]
    decision = approvals.get(approval_id)
    if not isinstance(decision, dict) or decision.get("status") != "approved":
        raise ProjectionError(f"public Press Kit record references a missing approval: {approval_id}")
    subject = decision.get("subject")
    if not isinstance(subject, str) or not subject:
        raise ProjectionError(f"approval {approval_id!r} has no stable subject")
    return {"id": approval_id, "subject": subject}


def require_valid_source(repository_root: Path) -> None:
    """Refuse projection if any canonical source boundary is invalid."""

    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")


def public_records(
    source: dict[str, Any],
    field: str,
    approvals: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return reviewed public records in stable identifier order."""

    records = source.get(field)
    if not isinstance(records, list):
        raise ProjectionError(f"Press Kit source field must be an array: {field}")
    result = []
    for value in records:
        if not isinstance(value, dict) or not is_public(value):
            continue
        result.append({**value, "approval": approval_record(value, approvals)})
    return sorted(result, key=lambda value: str(value["id"]))


def media_type(path: Path) -> str:
    """Return a conservative media type for one approved source asset."""

    return MIME_TYPES.get(path.suffix.lower(), "application/octet-stream")


def archive_name(download_name: Any, source_path: str) -> str:
    """Return one safe archive name without accepting path traversal."""

    candidate = download_name if isinstance(download_name, str) and download_name else Path(source_path).name
    normalized = PurePosixPath(candidate)
    if (
        normalized.is_absolute()
        or len(normalized.parts) != 1
        or normalized.name in {"", ".", ".."}
        or "\\" in candidate
    ):
        raise ProjectionError(f"Press Kit download name is not a filename: {candidate!r}")
    return normalized.name


def public_usage_rules(usage: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only approved public usage rules relevant to release consumers."""

    result = []
    for section in usage.get("sections", []):
        if not isinstance(section, dict):
            continue
        for rule in section.get("rules", []):
            if not isinstance(rule, dict) or not is_public(rule):
                continue
            result.append(
                {
                    key: rule[key]
                    for key in ("id", "kind", "category", "instruction", "rationale", "contexts")
                }
            )
    return sorted(result, key=lambda value: value["id"])


def public_legal(usage: dict[str, Any]) -> dict[str, Any]:
    """Project public legal guidance or expose its absence explicitly."""

    legal = usage.get("legal")
    if not isinstance(legal, dict) or not is_public(legal):
        return {"status": "not-declared", "value": None}
    return {
        "status": "declared",
        "value": {
            key: legal[key]
            for key in ("trademark", "copyright", "attribution", "thirdPartyLicenses")
        },
    }


def build_projection(repository_root: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Build one public Press Kit model and its selected approved asset bytes."""

    require_valid_source(repository_root)
    project_document = load_json(repository_root / ".identity/identity.json")
    documents = project_document["documents"]
    press_path = documents.get("pressKit")
    if not isinstance(press_path, str):
        raise ProjectionError("Press Kit projection requires documents.pressKit source")
    source = load_json(repository_root / press_path)
    usage = load_json(repository_root / documents["guidance"]["usage"])
    provenance = load_json(repository_root / documents["provenance"])
    approvals_document = load_json(repository_root / documents["approvals"])
    approvals = {
        item["id"]: item
        for item in approvals_document["decisions"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    boilerplates = public_records(source, "boilerplates", approvals)
    boilerplate_kinds = {value["kind"] for value in boilerplates}
    if boilerplate_kinds != {"short", "long"}:
        raise ProjectionError(
            "Press Kit projection requires approved public short and long boilerplates"
        )
    facts = public_records(source, "facts", approvals)
    links = public_records(source, "links", approvals)
    channel_source = channel_registry.source_for_project(repository_root, project_document)
    projected_channels: list[dict[str, Any]] = []
    if channel_source is not None:
        if any(value.get("kind") == "social" for value in links):
            raise ProjectionError(
                "Press Kit social links must derive from documents.channelRegistry"
            )
        projected_channels = channel_registry.public_channels(channel_source)
        governed = {
            value["id"]: value for value in channel_registry.governed_channels(channel_source)
        }
        authored_ids = {value["id"] for value in links}
        authored_urls = {value["url"] for value in links}
        for value in projected_channels:
            if f"channel-{value['id']}" in authored_ids or value["url"] in authored_urls:
                raise ProjectionError(
                    f"Press Kit link duplicates channel registry record: {value['id']}"
                )
        links.extend(
            {
                "id": f"channel-{value['id']}",
                "label": value["label"],
                "url": value["url"],
                "kind": "social",
                "approval": approval_record(governed[value["id"]], approvals),
            }
            for value in projected_channels
        )
        links.sort(key=lambda value: str(value["id"]))
    contacts = public_records(source, "contacts", approvals)
    team = public_records(source, "team", approvals)
    selections = public_records(source, "assets", approvals)

    usage_assets = {
        item["id"]: item
        for item in usage["assets"]
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and item.get("status") == "active"
        and item.get("availability") == "public"
        and is_public(item)
    }
    provenance_assets = {
        item["id"]: item
        for item in provenance["assets"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    selected_assets: list[dict[str, Any]] = []
    asset_bytes: dict[str, bytes] = {}
    for selection in selections:
        asset_id = selection["assetId"]
        usage_asset = usage_assets.get(asset_id)
        provenance_asset = provenance_assets.get(asset_id)
        if usage_asset is None or provenance_asset is None:
            raise ProjectionError(
                f"Press Kit asset {asset_id!r} is not an active approved public source asset"
            )
        source_path = str(usage_asset["path"])
        source_file = repository_root / source_path
        bytes_value = source_file.read_bytes()
        expected_digest = provenance_asset.get("sha256")
        actual_digest = hashlib.sha256(bytes_value).hexdigest()
        if expected_digest != actual_digest:
            raise ProjectionError(f"approved Press Kit asset digest changed: {source_path}")
        relative_path = f"assets/{archive_name(usage_asset.get('downloadName'), source_path)}"
        if relative_path in asset_bytes:
            raise ProjectionError(f"Press Kit asset download path is duplicated: {relative_path}")
        asset_bytes[relative_path] = bytes_value
        selected_assets.append(
            {
                "id": selection["id"],
                "assetId": asset_id,
                "label": selection["label"],
                "notes": selection["notes"],
                "downloadPath": relative_path,
                "mediaType": media_type(source_file),
                "sha256": actual_digest,
                "altText": provenance_asset["accessibility"]["altText"],
                "license": provenance_asset["license"],
                "origin": provenance_asset["origin"],
                "usage": provenance_asset["usage"],
                "approval": selection["approval"],
            }
        )

    artifacts = [
        {
            "id": "press-kit-json",
            "label": "Press Kit data",
            "path": OUTPUT_FILES["json"],
            "mediaType": "application/json",
            "intendedUse": "Machine-readable, approved Press Kit projection.",
        },
        {
            "id": "press-kit-markdown",
            "label": "Press Kit",
            "path": OUTPUT_FILES["markdown"],
            "mediaType": "text/markdown",
            "intendedUse": "Human-readable, approved Press and Media Kit.",
        },
        {
            "id": "press-kit-manifest",
            "label": "Press Kit manifest",
            "path": OUTPUT_FILES["manifest"],
            "mediaType": "application/json",
            "intendedUse": "Source, file, and integrity record for this immutable package.",
        },
        {
            "id": "press-kit-checksums",
            "label": "Press Kit checksums",
            "path": OUTPUT_FILES["checksums"],
            "mediaType": "text/plain",
            "intendedUse": "SHA-256 checksums for the archive contents and manifest.",
        },
        {
            "id": "press-kit-archive",
            "label": "Complete Press Kit archive",
            "path": OUTPUT_FILES["archive"],
            "mediaType": "application/zip",
            "intendedUse": "Versioned offline archive of approved Press and Media Kit materials.",
        },
    ]
    tokens = design_system.resolved_tokens(project_document, repository_root)[2]
    model = {
        "schema": PRESS_KIT_SCHEMA,
        "project": {
            key: project_document["project"][key]
            for key in ("id", "displayName", "repository", "tagline", "kind")
        },
        "source": {
            "digest": design_system.canonical_source_digest(repository_root),
            "sourceSchema": validator.PRESS_KIT_SOURCE_SCHEMA,
            "projectionVersion": PROJECTION_VERSION,
        },
        "inheritance": design_system.inheritance(project_document, tokens),
        "boilerplates": [
            {key: value[key] for key in ("id", "kind", "text", "approval")}
            for value in boilerplates
        ],
        "facts": [
            {key: value[key] for key in ("id", "label", "value", "approval")}
            for value in facts
        ],
        "links": [
            {key: value[key] for key in ("id", "label", "url", "kind", "approval")}
            for value in links
        ],
        "contacts": [
            {key: value[key] for key in ("id", "label", "kind", "value", "notes", "approval")}
            for value in contacts
        ],
        "team": [
            {
                key: value[key]
                for key in ("id", "name", "role", "approval")
                if key in value
            }
            | ({"bio": value["bio"]} if "bio" in value else {})
            for value in team
        ],
        "assets": sorted(selected_assets, key=lambda value: value["id"]),
        "guidance": {
            "usageRules": public_usage_rules(usage),
            "legal": public_legal(usage),
        },
        "artifacts": artifacts,
    }
    if channel_source is not None:
        model["channelRegistry"] = {
            "registry": channel_source["registry"],
            "channels": projected_channels,
        }
    return model, asset_bytes


def verified_social_package(
    repository_root: Path,
    model: dict[str, Any],
    asset_bytes: dict[str, bytes],
    directory: Path,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Attach one integrity-checked social archive through its generated handoff."""

    source_directory = generated_output_directory(repository_root, directory)
    handoff_path = source_directory / "press-kit-handoff.json"
    manifest_path = source_directory / "social-surfaces-manifest.json"
    checksums_path = source_directory / "SHA256SUMS"
    archive_path = source_directory / "social-surfaces.zip"
    for path in (handoff_path, manifest_path, checksums_path, archive_path):
        if not path.is_file() or path.is_symlink():
            raise ProjectionError(f"social-surface handoff file is missing or unsafe: {path.name}")
    handoff = load_json(handoff_path)
    manifest = load_json(manifest_path)
    if handoff.get("schema") != SOCIAL_HANDOFF_SCHEMA:
        raise ProjectionError("social-surface handoff uses an unsupported schema")
    if manifest.get("schema") != SOCIAL_MANIFEST_SCHEMA:
        raise ProjectionError("social-surface manifest uses an unsupported schema")
    if handoff.get("publicationAuthorized") is not False:
        raise ProjectionError("social-surface handoff must not grant publication authority")
    if handoff.get("projectId") != model["project"]["id"]:
        raise ProjectionError("social-surface handoff belongs to a different project")
    if handoff.get("sourceDigest") != model["source"]["digest"]:
        raise ProjectionError("social-surface handoff is stale for the current Identity source")
    if (
        manifest.get("projectId") != handoff["projectId"]
        or manifest.get("sourceDigest") != handoff["sourceDigest"]
        or manifest.get("catalog") != handoff.get("catalog")
    ):
        raise ProjectionError("social-surface manifest and handoff disagree")
    expected_package = {
        "manifest": "social-surfaces-manifest.json",
        "checksums": "SHA256SUMS",
        "archive": "social-surfaces.zip",
    }
    if handoff.get("package") != expected_package:
        raise ProjectionError("social-surface handoff package paths are unsupported")

    archive_bytes = archive_path.read_bytes()
    try:
        archive_file = zipfile.ZipFile(BytesIO(archive_bytes))
    except zipfile.BadZipFile as error:
        raise ProjectionError("social-surface archive is not a valid ZIP") from error
    with archive_file as archive:
        names = archive.namelist()
        if names != sorted(names) or len(names) != len(set(names)):
            raise ProjectionError("social-surface archive paths are duplicated or unordered")
        for name in names:
            normalized = PurePosixPath(name)
            if (
                normalized.is_absolute()
                or name != normalized.as_posix()
                or any(part in {"", ".", ".."} for part in normalized.parts)
            ):
                raise ProjectionError(f"social-surface archive path is unsafe: {name!r}")
        required_names = {
            "press-kit-handoff.json",
            "social-surfaces-manifest.json",
            "SHA256SUMS",
        }
        if not required_names.issubset(names):
            raise ProjectionError("social-surface archive omits required integrity files")
        if archive.read("press-kit-handoff.json") != handoff_path.read_bytes():
            raise ProjectionError("social-surface archive handoff differs from its sidecar")
        if archive.read("social-surfaces-manifest.json") != manifest_path.read_bytes():
            raise ProjectionError("social-surface archive manifest differs from its sidecar")
        if archive.read("SHA256SUMS") != checksums_path.read_bytes():
            raise ProjectionError("social-surface archive checksums differ from their sidecar")
        expected_checksums = (
            "\n".join(
                f"{hashlib.sha256(archive.read(name)).hexdigest()}  {name}"
                for name in names
                if name != "SHA256SUMS"
            )
            + "\n"
        ).encode("utf-8")
        if archive.read("SHA256SUMS") != expected_checksums:
            raise ProjectionError("social-surface checksums do not match archive contents")
        files = manifest.get("files")
        if not isinstance(files, dict):
            raise ProjectionError("social-surface manifest has no file integrity map")
        for name, evidence in files.items():
            if not isinstance(name, str) or not isinstance(evidence, dict) or name not in names:
                raise ProjectionError("social-surface manifest references a missing archive file")
            value = archive.read(name)
            if evidence.get("sha256") != hashlib.sha256(value).hexdigest():
                raise ProjectionError(f"social-surface archive digest differs: {name}")
            if evidence.get("bytes") != len(value):
                raise ProjectionError(f"social-surface archive byte count differs: {name}")

    target_records = handoff.get("targets")
    if not isinstance(target_records, list) or not target_records:
        raise ProjectionError("social-surface handoff has no selected targets")
    social_path = "social/social-surfaces.zip"
    if social_path in asset_bytes:
        raise ProjectionError("Press Kit social-surface archive path is duplicated")
    updated_assets = {**asset_bytes, social_path: archive_bytes}
    updated_model = {
        **model,
        "socialSurfaces": {
            "status": "included",
            "archivePath": social_path,
            "sha256": hashlib.sha256(archive_bytes).hexdigest(),
            "catalog": handoff["catalog"],
            "targets": target_records,
            "publicationAuthorized": False,
        },
        "artifacts": model["artifacts"]
        + [
            {
                "id": "social-surface-package",
                "label": "Social-surface creative inputs",
                "path": social_path,
                "mediaType": "application/zip",
                "intendedUse": "Pinned, renderer-neutral social targets and approved Identity inputs.",
            }
        ],
    }
    return updated_model, updated_assets


def render_json(value: dict[str, Any]) -> str:
    """Render one stable JSON document."""

    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def markdown_cell(value: str) -> str:
    """Render a safe Markdown table cell."""

    return value.replace("|", "\\|").replace("\n", "<br>")


def render_markdown(model: dict[str, Any]) -> str:
    """Render an honest human-facing Press Kit without adding new claims."""

    project = model["project"]
    boilerplates = {value["kind"]: value for value in model["boilerplates"]}
    lines = [
        f"# {project['displayName']} Press Kit",
        "",
        "This is a deterministic projection of approved public Identity source.",
        "",
        f"Source: {project['repository']}",
        "",
        f"Source digest: `{model['source']['digest']}`",
        "",
        "## Short boilerplate",
        "",
        boilerplates["short"]["text"],
        "",
        f"Approval: `{boilerplates['short']['approval']['id']}`",
        "",
        "## Long boilerplate",
        "",
        boilerplates["long"]["text"],
        "",
        f"Approval: `{boilerplates['long']['approval']['id']}`",
        "",
        "## Key facts",
        "",
    ]
    if model["facts"]:
        lines.extend(["| Fact | Value |", "| --- | --- |"])
        lines.extend(
            f"| {markdown_cell(value['label'])} | {markdown_cell(value['value'])} |"
            for value in model["facts"]
        )
    else:
        lines.append("No public facts are declared in the current source.")
    lines.extend(["", "## Links", ""])
    if model["links"]:
        lines.extend(
            f"- [{value['label']}]({value['url']}) — {value['kind']}"
            for value in model["links"]
        )
    else:
        lines.append("No additional public links are declared in the current source.")
    lines.extend(["", "## Media contact", ""])
    if model["contacts"]:
        for value in model["contacts"]:
            notes = f" — {value['notes']}" if value["notes"] else ""
            lines.append(f"- **{value['label']}**: {value['value']}{notes}")
    else:
        lines.append("No public media contact is declared in the current source.")
    lines.extend(["", "## Team", ""])
    if model["team"]:
        for value in model["team"]:
            lines.extend([f"### {value['name']}", "", value["role"], ""])
            if "bio" in value:
                lines.extend([value["bio"], ""])
    else:
        lines.append("No public team bios are declared in the current source.")
    lines.extend(["", "## Approved assets", ""])
    if model["assets"]:
        lines.extend(["| Asset | Use | Download |", "| --- | --- | --- |"])
        lines.extend(
            f"| {markdown_cell(value['label'])} | {markdown_cell(value['notes'])} | [{value['downloadPath']}]({value['downloadPath']}) |"
            for value in model["assets"]
        )
    else:
        lines.append("No Press Kit assets are selected in the current source.")
    lines.extend(["", "## Usage and legal guidance", ""])
    if model["guidance"]["usageRules"]:
        for rule in model["guidance"]["usageRules"]:
            lines.extend([f"- **{rule['kind']} · {rule['category']}**: {rule['instruction']}"])
    else:
        lines.append("No public usage rules are declared in the current source.")
    legal = model["guidance"]["legal"]
    if legal["status"] == "declared":
        value = legal["value"]
        lines.extend(
            [
                "",
                f"Trademark: {value['trademark']}",
                "",
                f"Copyright: {value['copyright']}",
                "",
                f"Attribution: {value['attribution']}",
            ]
        )
    else:
        lines.extend(["", "No public legal guidance is declared in the current source."])
    social = model.get("socialSurfaces")
    if isinstance(social, dict) and social.get("status") == "included":
        lines.extend(
            [
                "",
                "## Social-surface creative inputs",
                "",
                f"- [Download the pinned social package]({social['archivePath']})",
                f"- Catalog: `{social['catalog']['id']}@{social['catalog']['version']}`",
                f"- Selected targets: {len(social['targets'])}",
                "- Publication authorized: no",
            ]
        )
    lines.extend(["", "## Downloads", ""])
    lines.extend(
        f"- [{value['label']}]({value['path']}) — {value['intendedUse']}"
        for value in model["artifacts"]
    )
    lines.extend(
        [
            "",
            "This projection includes only approved public records. It does not authorize publication, alter source facts, or imply endorsement.",
            "",
        ]
    )
    return "\n".join(lines)


def checksum_entry(value: bytes) -> dict[str, Any]:
    """Return a stable checksum record for one generated file."""

    return {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value)}


def deterministic_zip(entries: dict[str, bytes]) -> bytes:
    """Build a reproducible ZIP archive with normalized ordering and timestamps."""

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


def build_package(model: dict[str, Any], asset_bytes: dict[str, bytes]) -> dict[str, bytes]:
    """Return all deterministic downloads, manifest, checksums, and archive bytes."""

    outputs = {
        OUTPUT_FILES["json"]: render_json(model).encode("utf-8"),
        OUTPUT_FILES["markdown"]: render_markdown(model).encode("utf-8"),
        **asset_bytes,
    }
    manifest = {
        "schema": PACKAGE_SCHEMA,
        "version": PROJECTION_VERSION,
        "projectionSchema": PRESS_KIT_SCHEMA,
        "projectId": model["project"]["id"],
        "sourceDigest": model["source"]["digest"],
        "files": {name: checksum_entry(value) for name, value in sorted(outputs.items())},
    }
    outputs[OUTPUT_FILES["manifest"]] = render_json(manifest).encode("utf-8")
    checksum_lines = [
        f"{checksum_entry(value)['sha256']}  {name}"
        for name, value in sorted(outputs.items())
    ]
    outputs[OUTPUT_FILES["checksums"]] = ("\n".join(checksum_lines) + "\n").encode("utf-8")
    outputs[OUTPUT_FILES["archive"]] = deterministic_zip(outputs)
    return outputs


def generated_output_directory(repository_root: Path, value: Path) -> Path:
    """Resolve a generated directory without allowing source or symlink writes."""

    relative = value.as_posix()
    if not validator.valid_relative_path(relative):
        raise ProjectionError("output directory must be normalized and repository-relative")
    if relative == ".identity" or relative.startswith(".identity/"):
        raise ProjectionError("generated Press Kit output cannot be written into canonical .identity")
    current = repository_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionError("output directory may not traverse a symbolic link")
    return repository_root / relative


def atomic_write(path: Path, value: bytes) -> None:
    """Replace one generated artifact without leaving a partial file behind."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def write_outputs(
    repository_root: Path,
    output_directory: Path,
    payload: dict[str, bytes],
) -> list[Path]:
    """Write deterministic artifacts outside canonical Identity source only."""

    destination = generated_output_directory(repository_root, output_directory)
    written: list[Path] = []
    for name, value in sorted(payload.items()):
        relative = PurePosixPath(name)
        if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
            raise ProjectionError(f"generated output path is unsafe: {name!r}")
        path = destination / relative
        atomic_write(path, value)
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    """Build the stable Press Kit projection command interface."""

    parser = argparse.ArgumentParser(
        description="Generate an approved Identity Press Kit without network access."
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
        help="Repository-relative generated directory for the complete Press Kit package.",
    )
    parser.add_argument(
        "--social-surfaces-directory",
        type=Path,
        help="Repository-relative generated social package to verify and include.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run projection and return a stable command status."""

    arguments = build_parser().parse_args(argv)
    repository_root = arguments.repository_root.resolve()
    try:
        model, assets = build_projection(repository_root)
        if arguments.social_surfaces_directory is not None:
            model, assets = verified_social_package(
                repository_root,
                model,
                assets,
                arguments.social_surfaces_directory,
            )
        if arguments.output_directory is None:
            output = render_json(model) if arguments.format == "json" else render_markdown(model)
            print(output, end="")
        else:
            payload = build_package(model, assets)
            for path in write_outputs(repository_root, arguments.output_directory, payload):
                print(path.relative_to(repository_root).as_posix())
    except (OSError, ProjectionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
