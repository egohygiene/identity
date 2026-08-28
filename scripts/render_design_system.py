#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Project validated Identity v1 handbook source into human and AI-ready artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Any, Sequence

import validate_identity as validator

HANDBOOK_SCHEMA = "identity.design-system-handbook/v1"
CONTEXT_SCHEMA = "identity.design-context/v1"
PROJECTION_VERSION = "1.0.0"
OUTPUT_FILES = {
    "handbook-json": "design-system-handbook.json",
    "handbook-markdown": "design-system-handbook.md",
    "context-json": "design-context.json",
    "context-markdown": "design-context.md",
}


class ProjectionError(ValueError):
    """Raised when a validated Identity source cannot produce a projection."""


def load_json(path: Path) -> dict[str, Any]:
    """Load one validated, object-shaped JSON source document."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"document must be an object: {path}")
    return value


def is_public(value: dict[str, Any]) -> bool:
    """Return whether one governed source record is public and approved."""

    governance = value.get("governance")
    return (
        isinstance(governance, dict)
        and governance.get("state") == "approved"
        and governance.get("visibility") == "public"
    )


def canonical_source_digest(repository_root: Path) -> str:
    """Return the compiler-compatible digest of local canonical Identity source."""

    identity_root = repository_root / ".identity"
    if not identity_root.is_dir():
        raise ProjectionError("missing canonical .identity source directory")
    files = []
    for path in identity_root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative_to_identity = path.relative_to(identity_root)
        if path.name == "README.md" or relative_to_identity.parts[0] in {"candidates", "references"}:
            continue
        files.append(path)

    digest = hashlib.sha256()
    for path in sorted(files):
        relative = path.relative_to(repository_root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_alias_value(
    path: str,
    tokens: dict[str, validator.TokenRecord],
    visited: set[str] | None = None,
) -> Any:
    """Resolve a previously validated DTCG alias without changing its source layer."""

    token = tokens[path]
    value = token.value
    match = validator.ALIAS.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return value
    target = match.group(1)
    seen = set() if visited is None else visited
    if path in seen or target not in tokens:
        raise ProjectionError(f"validated token alias is not resolvable: {path}")
    seen.add(path)
    return resolve_alias_value(target, tokens, seen)


def resolved_tokens(
    project: dict[str, Any], repository_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, validator.TokenRecord]]:
    """Return context tokens, handbook entries, and resolved token metadata."""

    diagnostics: list[validator.Diagnostic] = []
    tokens, _ = validator.load_layers(project, repository_root, diagnostics)
    if diagnostics:
        first = sorted(set(diagnostics))[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")

    context: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    for path, token in sorted(tokens.items()):
        override = token.extension.get("override")
        override_reason = override.get("reason") if isinstance(override, dict) else None
        approval = override.get("approval") if isinstance(override, dict) else None
        value = resolve_alias_value(path, tokens)
        context_token = {
            "path": path,
            "type": token.token_type,
            "value": value,
            "sourceLayer": token.layer,
            "overrideReason": override_reason,
            "approval": approval,
        }
        context.append(context_token)
        entry_content = {
            **context_token,
            "constraints": token.extension,
        }
        entries.append(
            {
                "id": f"token:{path}",
                "kind": "token",
                "status": "declared",
                "content": entry_content,
                "rationale": "Resolved from the reviewed semantic token source.",
                "sourceLayer": token.layer,
            }
        )
    return context, entries, tokens


def public_voice_entries(voice: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return public context facts and handbook entries from reviewed voice source."""

    contexts: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    foundation = voice["foundation"]
    if is_public(foundation):
        entries.append(
            {
                "id": "voice:foundation",
                "kind": "voice",
                "status": "declared",
                "content": foundation,
                "rationale": foundation["positioning"],
                "sourceLayer": None,
            }
        )
    for characteristic in sorted(voice["characteristics"], key=lambda value: value["id"]):
        if is_public(characteristic):
            entries.append(
                {
                    "id": f"voice:characteristic:{characteristic['id']}",
                    "kind": "voice",
                    "status": "declared",
                    "content": characteristic,
                    "rationale": characteristic["description"],
                    "sourceLayer": None,
                }
            )
    for item in sorted(voice["contexts"], key=lambda value: value["id"]):
        if not is_public(item):
            continue
        context = {
            "context": item["id"],
            "tone": item["tone"],
            "preferredVocabulary": item["preferredVocabulary"],
            "avoidedLanguage": item["avoidedLanguage"],
        }
        contexts.append(context)
        entries.append(
            {
                "id": f"voice:{item['id']}",
                "kind": "voice",
                "status": "declared",
                "content": context,
                "rationale": item["intent"],
                "sourceLayer": None,
            }
        )
    localization = voice["localization"]
    if is_public(localization):
        entries.append(
            {
                "id": "voice:localization",
                "kind": "voice",
                "status": "declared",
                "content": localization,
                "rationale": localization["fallback"],
                "sourceLayer": None,
            }
        )
    return contexts, entries


def public_usage_entries(usage: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return public usage facts and handbook entries from reviewed source."""

    rules = [
        rule
        for section in usage["sections"]
        for rule in section["rules"]
        if is_public(rule)
    ]
    context = [
        {
            "id": rule["id"],
            "kind": rule["kind"],
            "category": rule["category"],
            "instruction": rule["instruction"],
            "rationale": rule["rationale"],
            "contexts": rule["contexts"],
        }
        for rule in sorted(rules, key=lambda value: value["id"])
    ]
    entries: list[dict[str, Any]] = [
        {
            "id": f"usage:{rule['id']}",
            "kind": "usage",
            "status": "declared",
            "content": rule,
            "rationale": rule["rationale"],
            "sourceLayer": None,
        }
        for rule in sorted(rules, key=lambda value: value["id"])
    ]
    for asset in sorted(usage["assets"], key=lambda value: value["id"]):
        if not is_public(asset) or asset["status"] != "active":
            continue
        entries.append(
            {
                "id": f"asset:{asset['id']}",
                "kind": "asset",
                "status": "declared",
                "content": asset,
                "rationale": asset["notes"],
                "sourceLayer": None,
            }
        )
    for kind, value in (("accessibility", usage["accessibility"]), ("legal", usage["legal"])):
        if not is_public(value):
            continue
        rationale = value.get("summary") or value.get("attribution")
        if not isinstance(rationale, str) or not rationale:
            raise ProjectionError(f"public {kind} guidance has no renderer-safe rationale")
        entries.append(
            {
                "id": kind,
                "kind": kind,
                "status": "declared",
                "content": value,
                "rationale": rationale,
                "sourceLayer": None,
            }
        )
    return context, sorted(entries, key=lambda value: value["id"])


def source_sections(design_system: dict[str, Any]) -> list[dict[str, Any]]:
    """Project approved handbook principles without their source governance envelope."""

    result: list[dict[str, Any]] = []
    for section in sorted(design_system["sections"], key=lambda value: value["id"]):
        principles = [
            {
                key: principle[key]
                for key in ("id", "title", "guidance", "rationale", "appliesTo")
            }
            for principle in sorted(section["principles"], key=lambda value: value["id"])
            if is_public(principle)
        ]
        if principles:
            result.append(
                {
                    "id": section["id"],
                    "title": section["title"],
                    "summary": section["summary"],
                    "principles": principles,
                    "entries": [],
                }
            )
    return result


def public_capabilities(design_system: dict[str, Any]) -> list[dict[str, Any]]:
    """Return explicit reviewed capability boundaries without governance internals."""

    return [
        {key: item[key] for key in ("id", "label", "status", "owner", "notes")}
        for item in sorted(design_system["capabilities"], key=lambda value: value["id"])
        if is_public(item)
    ]


def public_references(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    """Return approved, public observations without fetching their external URLs."""

    fields = (
        "id",
        "url",
        "capturedAt",
        "patterns",
        "decision",
        "notes",
        "rights",
        "affectsCanonical",
    )
    return [
        {field: item[field] for field in fields}
        for item in sorted(catalog["references"], key=lambda value: value["id"])
        if is_public(item)
    ]


def inheritance(project: dict[str, Any], tokens: dict[str, validator.TokenRecord]) -> dict[str, Any]:
    """Record resolved organization layers and intentional product overrides."""

    layers = project["layers"]
    organization_layers = [
        item["id"] for item in layers if item["kind"] == "organization-defaults"
    ]
    product_layers = [item["id"] for item in layers if item["kind"] == "product-override"]
    if len(product_layers) != 1:
        raise ProjectionError("validated project must resolve exactly one product override layer")
    overrides = []
    for path, token in sorted(tokens.items()):
        override = token.extension.get("override")
        if isinstance(override, dict):
            overrides.append(
                {
                    "token": path,
                    "reason": override["reason"],
                    "approval": override["approval"],
                }
            )
    return {
        "organizationLayers": organization_layers,
        "productLayer": product_layers[0],
        "overrides": overrides,
    }


def build_projections(repository_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build deterministic handbook and AI-context models from valid local source."""

    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")

    project = load_json(repository_root / ".identity/identity.json")
    documents = project["documents"]
    handbook_paths = documents.get("handbook")
    if not isinstance(handbook_paths, dict):
        raise ProjectionError("design-system projection requires documents.handbook source")
    design_system = load_json(repository_root / handbook_paths["designSystem"])
    references = load_json(repository_root / handbook_paths["references"])
    voice = load_json(repository_root / documents["guidance"]["voice"])
    usage = load_json(repository_root / documents["guidance"]["usage"])
    targets = load_json(repository_root / documents["targets"])

    token_context, token_entries, tokens = resolved_tokens(project, repository_root)
    voice_context, voice_entries = public_voice_entries(voice)
    usage_context, usage_entries = public_usage_entries(usage)
    source_digest = canonical_source_digest(repository_root)
    profiles = [
        {"id": item["id"], "version": item["version"]}
        for item in sorted(targets["enabled"], key=lambda value: value["id"])
    ]
    profile_entries = [
        {
            "id": f"profile:{profile['id']}",
            "kind": "profile",
            "status": "declared",
            "content": profile,
            "rationale": "Enabled versioned output profile selected by the reviewed project source.",
            "sourceLayer": None,
        }
        for profile in profiles
    ]
    resolved_section = {
        "id": "resolved-source",
        "title": "Resolved identity source",
        "summary": "Validated local token, voice, usage, asset, accessibility, and legal facts.",
        "principles": [],
        "entries": sorted(
            token_entries + voice_entries + usage_entries + profile_entries,
            key=lambda value: value["id"],
        ),
    }
    sections = source_sections(design_system) + [resolved_section]
    sections.sort(key=lambda value: value["id"])
    inherited = inheritance(project, tokens)
    capabilities = public_capabilities(design_system)

    handbook = {
        "schema": HANDBOOK_SCHEMA,
        "project": {
            key: project["project"][key]
            for key in ("id", "displayName", "repository", "kind")
        },
        "source": {
            "digest": source_digest,
            "guidanceSchema": validator.DESIGN_SYSTEM_SCHEMA,
            "referenceCatalogSchema": validator.DESIGN_REFERENCES_SCHEMA,
        },
        "inheritance": inherited,
        "profiles": profiles,
        "sections": sections,
        "capabilities": capabilities,
        "references": public_references(references),
    }
    context = {
        "schema": CONTEXT_SCHEMA,
        "project": {
            key: project["project"][key] for key in ("id", "displayName", "kind")
        },
        "source": {
            "digest": source_digest,
            "handbookSchema": HANDBOOK_SCHEMA,
            "projectionVersion": PROJECTION_VERSION,
        },
        "applicability": {
            "organizationLayers": inherited["organizationLayers"],
            "productLayer": inherited["productLayer"],
            "contexts": [item["context"] for item in voice_context],
        },
        "profiles": profiles,
        "tokens": token_context,
        "voice": voice_context,
        "usage": usage_context,
        "capabilities": [
            {key: item[key] for key in ("id", "status", "owner", "notes")}
            for item in capabilities
        ],
    }
    return handbook, context


def render_json(value: dict[str, Any]) -> str:
    """Render one deterministic JSON projection."""

    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def markdown_value(value: Any) -> str:
    """Render structured entry content deterministically inside a Markdown code block."""

    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def render_handbook_markdown(handbook: dict[str, Any]) -> str:
    """Render the human handbook without adding brand claims beyond reviewed source."""

    project = handbook["project"]
    inheritance_value = handbook["inheritance"]
    lines = [
        f"# {project['displayName']} design-system handbook",
        "",
        "This is a deterministic projection of validated, reviewed local Identity source.",
        "",
        f"Source: {project['repository']}",
        "",
        f"Source digest: `{handbook['source']['digest']}`",
        "",
        "## Inheritance",
        "",
        f"- Organization layers: {', '.join(inheritance_value['organizationLayers'])}",
        f"- Product layer: `{inheritance_value['productLayer']}`",
        "",
    ]
    if inheritance_value["overrides"]:
        lines.extend(["### Reviewed overrides", ""])
        for override in inheritance_value["overrides"]:
            lines.extend(
                [
                    f"- `{override['token']}` — {override['reason']} (approval: `{override['approval']}`)",
                ]
            )
        lines.append("")

    lines.extend(["## Enabled output profiles", ""])
    for profile in handbook["profiles"]:
        lines.append(f"- `{profile['id']}@{profile['version']}`")
    lines.append("")

    lines.extend(["## Design principles", ""])
    for section in handbook["sections"]:
        if not section["principles"]:
            continue
        lines.extend([f"### {section['title']}", "", section["summary"], ""])
        for principle in section["principles"]:
            lines.extend(
                [
                    f"#### {principle['title']}",
                    "",
                    principle["guidance"],
                    "",
                    f"Why: {principle['rationale']}",
                    "",
                    f"Applies to: {', '.join(principle['appliesTo'])}",
                    "",
                ]
            )

    lines.extend(["## Resolved source facts", ""])
    for section in handbook["sections"]:
        for entry in section["entries"]:
            lines.extend(
                [
                    f"### {entry['id']}",
                    "",
                    f"Status: **{entry['status']}**",
                    "",
                    f"Rationale: {entry['rationale']}",
                    "",
                    "```json",
                    markdown_value(entry["content"]),
                    "```",
                    "",
                ]
            )

    lines.extend(
        [
            "## Capability boundaries",
            "",
            "| Capability | Owner | State | Notes |",
            "| --- | --- | --- | --- |",
        ]
    )
    for capability in handbook["capabilities"]:
        lines.append(
            f"| {capability['label']} | {capability['owner']} | {capability['status']} | {capability['notes']} |"
        )
    lines.extend(["", "## Reviewed external references", ""])
    for reference in handbook["references"]:
        lines.extend(
            [
                f"### {reference['id']}",
                "",
                f"Source: {reference['url']}",
                "",
                f"Captured: `{reference['capturedAt']}`",
                "",
                f"Decision: **{reference['decision']}**",
                "",
                "Patterns:",
                "",
                *[f"- {pattern}" for pattern in reference["patterns"]],
                "",
                f"Notes: {reference['notes']}",
                "",
                f"Rights: {reference['rights']}",
                "",
            ]
        )
    return "\n".join(lines)


def render_context_markdown(context: dict[str, Any]) -> str:
    """Render a concise agent context pack without requiring HTML scraping."""

    project = context["project"]
    applicability = context["applicability"]
    lines = [
        f"# {project['displayName']} design context",
        "",
        f"Schema: `{context['schema']}`",
        "",
        f"Source digest: `{context['source']['digest']}`",
        "",
        f"Projection version: `{context['source']['projectionVersion']}`",
        "",
        "## Applies to",
        "",
        f"- Organization layers: {', '.join(applicability['organizationLayers'])}",
        f"- Product layer: `{applicability['productLayer']}`",
        f"- Voice contexts: {', '.join(f'`{item}`' for item in applicability['contexts'])}",
        "",
        "## Enabled output profiles",
        "",
        *[f"- `{profile['id']}@{profile['version']}`" for profile in context["profiles"]],
        "",
        "## Capability boundaries",
        "",
        "| Capability | Owner | State | Notes |",
        "| --- | --- | --- | --- |",
        *[
            f"| `{capability['id']}` | {capability['owner']} | {capability['status']} | {capability['notes']} |"
            for capability in context["capabilities"]
        ],
        "",
        "## Tokens",
        "",
        "| Path | Type | Value | Source layer | Override |",
        "| --- | --- | --- | --- |",
    ]
    for token in context["tokens"]:
        value = json.dumps(token["value"], sort_keys=True, ensure_ascii=False)
        override = token["overrideReason"] or "—"
        lines.append(
            f"| `{token['path']}` | {token['type']} | `{value}` | `{token['sourceLayer']}` | {override} |"
        )
    lines.extend(["", "## Voice", ""])
    for voice in context["voice"]:
        lines.extend(
            [
                f"### {voice['context']}",
                "",
                f"Tone: {voice['tone']}",
                "",
                f"Prefer: {', '.join(voice['preferredVocabulary'])}",
                "",
                f"Avoid: {', '.join(voice['avoidedLanguage'])}",
                "",
            ]
        )
    lines.extend(["## Usage", ""])
    for usage in context["usage"]:
        lines.extend(
            [
                f"- **{usage['kind']} — {usage['category']}** (`{usage['id']}`): {usage['instruction']}",
                f"  Why: {usage['rationale']}",
                f"  Contexts: {', '.join(f'`{item}`' for item in usage['contexts'])}",
            ]
        )
    return "\n".join(lines) + "\n"


def render(projections: tuple[dict[str, Any], dict[str, Any]], output_format: str) -> str:
    """Render one named projection format."""

    handbook, context = projections
    if output_format == "handbook-json":
        return render_json(handbook)
    if output_format == "handbook-markdown":
        return render_handbook_markdown(handbook)
    if output_format == "context-json":
        return render_json(context)
    if output_format == "context-markdown":
        return render_context_markdown(context)
    raise ProjectionError(f"unsupported output format: {output_format}")


def output_directory(repository_root: Path, value: Path) -> Path:
    """Resolve an explicit generated-output directory without allowing source writes."""

    relative = value.as_posix()
    if not validator.valid_relative_path(relative):
        raise ProjectionError("output directory must be normalized and repository-relative")
    if relative == ".identity" or relative.startswith(".identity/"):
        raise ProjectionError("projection output cannot overwrite canonical .identity source")
    current = repository_root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ProjectionError("output directory may not traverse a symbolic link")
    return repository_root / relative


def atomic_write(path: Path, content: str) -> None:
    """Replace one generated text artifact without leaving a partial file behind."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def write_outputs(repository_root: Path, destination: Path, projections: tuple[dict[str, Any], dict[str, Any]]) -> list[Path]:
    """Write all deterministic artifacts only to an explicit generated directory."""

    root = output_directory(repository_root, destination)
    written = []
    for output_format, name in OUTPUT_FILES.items():
        path = root / name
        atomic_write(path, render(projections, output_format))
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    """Build the standalone deterministic projection command interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Consumer repository root containing .identity/identity.json.",
    )
    parser.add_argument(
        "--format",
        choices=tuple(OUTPUT_FILES),
        default="handbook-markdown",
        help="Projection to print when --output-directory is not set.",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        help="Repository-relative generated directory for all handbook and context artifacts.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the projection command and return a stable process status."""

    arguments = build_parser().parse_args(argv)
    repository_root = arguments.repository_root.resolve()
    try:
        projections = build_projections(repository_root)
        if arguments.output_directory is None:
            sys.stdout.write(render(projections, arguments.format))
        else:
            written = write_outputs(repository_root, arguments.output_directory, projections)
            for path in written:
                print(path.relative_to(repository_root).as_posix())
    except (OSError, UnicodeError, json.JSONDecodeError, ProjectionError) as error:
        print(f"projection failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
