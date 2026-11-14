#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Prepare a new, separate v1 source candidate using only supplied local data."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import tomllib
import types
from typing import Any

REQUEST_SCHEMA = "identity.initialization-request/v1"
REPORT_SCHEMA = "identity.initialization-report/v1"
SCHEMA_BASE = "https://egohygiene.github.io/identity/contracts/v1/"
REQUEST_KEYS = {"$schema", "schema", "project", "layers", "targets", "sourceRoot"}
PROJECT_KEYS = {"id", "displayName", "repository", "tagline", "kind"}
LAYER_KEYS = {"id", "kind", "priority", "tokens"}


def validator_module() -> tuple[types.ModuleType, dict[str, str]]:
    """Load trusted implementation code, never code from a consumer's directory."""
    if "__identity_validator_source" in globals():
        source = globals()["__identity_validator_source"]
        version = globals()["__identity_implementation_version"]
        initializer_digest = globals()["__identity_initializer_sha256"]
    else:
        script = Path(__file__).resolve()
        source = script.with_name("validate_identity.py").read_text(encoding="utf-8")
        version = tomllib.loads((script.parent.parent / "Cargo.toml").read_text())["package"]["version"]
        initializer_digest = digest(script.read_bytes())
    module = types.ModuleType("_identity_initialization_validator")
    sys.modules[module.__name__] = module
    exec(compile(source, "<trusted-identity-validator>", "exec"), module.__dict__)
    return module, {
        "packageVersion": version,
        "initializerSha256": initializer_digest,
        "validatorSha256": digest(source.encode("utf-8")),
    }


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def closed(value: Any, allowed: set[str], required: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - allowed or required - set(value):
        raise ValueError(f"{label} has missing, unknown or non-object fields")
    return value


def parse_json(content: bytes, label: str) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"{label} repeats a JSON key: {key}")
            result[key] = value
        return result

    def nonfinite(value: str) -> None:
        raise ValueError(f"{label} contains non-finite JSON: {value}")

    value = json.loads(content.decode("utf-8"), object_pairs_hook=pairs, parse_constant=nonfinite)
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def linked(metadata: os.stat_result) -> bool:
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def regular_path(path: Path, *, missing: bool = False) -> Path:
    """Inspect every existing component before using a local filesystem path."""
    for component in reversed((path, *path.parents)):
        try:
            metadata = component.lstat()
        except FileNotFoundError:
            if missing:
                continue
            raise
        if linked(metadata) or not (stat.S_ISDIR(metadata.st_mode) or stat.S_ISREG(metadata.st_mode)):
            raise ValueError("path traverses a link, reparse point or unsupported filesystem entry")
        if component != path and not stat.S_ISDIR(metadata.st_mode):
            raise ValueError("path parent is not a directory")
    return path


def local(root: Path, value: Any, validator: types.ModuleType, *, missing: bool = False) -> Path:
    if not validator.valid_canonical_source_path(value):
        raise ValueError("paths must be portable, normalized and repository-relative")
    return regular_path(root / value, missing=missing)


def read_input(path: Path, inputs: dict[Path, bytes]) -> bytes:
    regular_path(path)
    if not path.is_file():
        raise ValueError("supplied input is not a regular file")
    content = path.read_bytes()
    if path in inputs and inputs[path] != content:
        raise ValueError("supplied input changed during candidate preparation")
    inputs[path] = content
    return content


def import_source(root: Path, request: dict[str, Any], validator: types.ModuleType,
                  inputs: dict[Path, bytes]) -> tuple[dict[str, bytes], set[str], list[str]]:
    source_value = request["sourceRoot"]
    source = root if source_value == "." else local(root, source_value, validator)
    if not source.is_dir():
        raise ValueError("sourceRoot must be a local consumer directory")
    manifest = parse_json(read_input(source / ".identity/identity.json", inputs), "source manifest")
    if manifest.get("schema") != "identity.project/v1":
        raise ValueError("sourceRoot must contain v1 source; v0 is never implicitly migrated")
    diagnostics, snapshot = validator.validate_snapshot(source)
    if diagnostics:
        raise ValueError("sourceRoot is invalid; repair it explicitly before import: " +
                         "; ".join(f"{item.code} {item.path}: {item.message}" for item in diagnostics))
    snapshot.verify()
    files: dict[str, bytes] = {}
    directories: set[str] = set()

    def walk(directory: Path) -> None:
        regular_path(directory)
        relative = directory.relative_to(source).as_posix()
        if not validator.valid_canonical_source_path(relative):
            raise ValueError("sourceRoot contains a nonportable source directory")
        directories.add(relative)
        for path in sorted(directory.iterdir()):
            regular_path(path)
            relative = path.relative_to(source).as_posix()
            if not validator.valid_canonical_source_path(relative):
                raise ValueError("sourceRoot contains a nonportable source file")
            if path.is_dir():
                walk(path)
            else:
                files[relative] = read_input(path, inputs)

    walk(source / ".identity")
    # Declared local policy/default/document inputs can live outside .identity.
    # Preserve their relative locations; generated and unrelated files are not imported.
    for relative, expected in snapshot.files.items():
        content = read_input(local(source, relative, validator), inputs)
        if digest(content) != expected:
            raise ValueError("sourceRoot changed after its validation snapshot")
        files[relative] = content
    for relative in snapshot.directories:
        local(source, relative, validator)
        directories.add(relative)
    return files, directories, []


def seed_source(root: Path, request: dict[str, Any], validator: types.ModuleType,
                inputs: dict[Path, bytes]) -> tuple[dict[str, bytes], set[str], list[str]]:
    project = closed(request.get("project", {}), PROJECT_KEYS, set(), "project")
    for key, value in project.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"project.{key} must be a supplied nonempty string")
    if "id" in project and validator.IDENTIFIER.fullmatch(project["id"]) is None:
        raise ValueError("project.id must be a stable lowercase identifier")
    if "kind" in project and project["kind"] not in {"organization", "product", "repository"}:
        raise ValueError("project.kind is unsupported")
    if "repository" in project and (not project["repository"].startswith("https://") or
                                    any(character.isspace() for character in project["repository"])):
        raise ValueError("project.repository must be a supplied HTTPS URL")
    missing = [f"project.{key}" for key in sorted(PROJECT_KEYS - set(project))]
    missing.extend(["reviewed brief", "actual source assets, rights and same-subject human decisions"])
    directories = {f".identity/{name}" for name in
                   ("sources", "candidates", "references", "defaults", "overrides", "targets", "governance")}
    files = {
        ".identity/brief.md": b"# Identity candidate\n\nSupply and review the actual project intent before adoption.\n",
        ".identity/governance/approvals.json": json_bytes({
            "$schema": SCHEMA_BASE + "approvals.schema.json", "schema": "identity.approvals/v1", "decisions": []}),
        ".identity/governance/provenance.json": json_bytes({
            "$schema": SCHEMA_BASE + "provenance.schema.json", "schema": "identity.provenance/v1", "assets": []}),
    }
    layers = request.get("layers", [])
    if not isinstance(layers, list):
        raise ValueError("layers must be an array")
    result_layers = []
    seen: set[str] = set()
    priorities: set[int] = set()
    for layer in layers:
        layer = closed(layer, LAYER_KEYS, LAYER_KEYS, "layer")
        identifier = layer["id"]
        if not isinstance(identifier, str) or validator.IDENTIFIER.fullmatch(identifier) is None or identifier in seen:
            raise ValueError("layer id is invalid or duplicated")
        priority = layer["priority"]
        if type(priority) is not int or priority < 0 or priority in priorities:
            raise ValueError("layer priorities must be unique nonnegative integers")
        if layer["kind"] not in {"organization-defaults", "product-override"}:
            raise ValueError("layer kind is unsupported")
        content = read_input(local(root, layer["tokens"], validator), inputs)
        tokens = parse_json(content, "token layer")
        extension = tokens.get("$extensions", {}).get("org.egohygiene.identity", {})
        if extension.get("schema") != "identity.tokens/v1" or extension.get("layer") != {
            key: layer[key] for key in ("id", "kind", "priority")
        }:
            raise ValueError("token source schema/layer metadata must match the supplied layer")
        destination = f".identity/{'defaults' if layer['kind'] == 'organization-defaults' else 'overrides'}/{identifier}.tokens.json"
        files[destination] = content
        result_layers.append({**layer, "tokens": destination, "sha256": digest(content)})
        seen.add(identifier)
        priorities.add(priority)
    if layers and ([item["priority"] for item in layers] != sorted(priorities) or
                   [item["kind"] for item in layers].count("product-override") != 1 or
                   layers[-1]["kind"] != "product-override"):
        raise ValueError("layers must be ordered with exactly one final product override")
    if not layers:
        missing.append("reviewed local token layers and their explicit layer metadata")
    if "targets" in request:
        target_bytes = read_input(local(root, request["targets"], validator), inputs)
        targets = parse_json(target_bytes, "targets")
        closed(targets, {"$schema", "schema", "enabled", "inapplicable"},
               {"$schema", "schema", "enabled", "inapplicable"}, "targets")
        if targets["schema"] != "identity.targets/v1" or not isinstance(targets["enabled"], list) or not targets["enabled"]:
            raise ValueError("targets must explicitly enable supported versioned v1 profiles")
        selected = set()
        for item in targets["enabled"]:
            item = closed(item, {"id", "version"}, {"id", "version"}, "target profile")
            if not isinstance(item["id"], str) or not isinstance(item["version"], str) or \
               validator.V1_PROFILE_VERSIONS.get(item["id"]) != item["version"] or item["id"] in selected:
                raise ValueError("target profile is unsupported or duplicated")
            selected.add(item["id"])
        inapplicable = targets["inapplicable"]
        if not isinstance(inapplicable, list) or any(not isinstance(item, str) or
            validator.IDENTIFIER.fullmatch(item) is None for item in inapplicable) or \
            len(set(inapplicable)) != len(inapplicable) or selected.intersection(inapplicable):
            raise ValueError("target dispositions are invalid or conflicting")
        files[".identity/targets/profiles.json"] = target_bytes
    else:
        files[".identity/targets/profiles.json"] = json_bytes({
            "$schema": SCHEMA_BASE + "targets.schema.json", "schema": "identity.targets/v1",
            "enabled": [], "inapplicable": []})
        missing.append("explicit target-profile selection")
    files[".identity/identity.json"] = json_bytes({
        "$schema": SCHEMA_BASE + "project.schema.json", "schema": "identity.project/v1",
        "project": project, "layers": result_layers,
        "documents": {"brief": ".identity/brief.md", "targets": ".identity/targets/profiles.json",
                      "provenance": ".identity/governance/provenance.json",
                      "approvals": ".identity/governance/approvals.json",
                      "guidance": {"voice": None, "usage": None}},
        "directories": {key: f".identity/{key}" for key in ("sources", "candidates", "references")},
        "compatibility": {"acceptedSchemaMajor": 1, "migrationFrom": []},
    })
    return files, directories, missing


def prepare(arguments: argparse.Namespace) -> dict[str, Any]:
    validator, implementation = validator_module()
    root = regular_path(Path(os.path.abspath(arguments.repository_root)))
    if not root.is_dir():
        raise ValueError("repository root must be an existing directory")
    inputs: dict[Path, bytes] = {}
    request_path = local(root, arguments.request, validator)
    request = closed(parse_json(read_input(request_path, inputs), "request"), REQUEST_KEYS, {"schema"}, "request")
    if request["schema"] != REQUEST_SCHEMA:
        raise ValueError("unsupported initialization request schema")
    if "$schema" in request and not isinstance(request["$schema"], str):
        raise ValueError("request $schema must be a string")
    if "sourceRoot" in request and set(request).intersection({"project", "layers", "targets"}):
        raise ValueError("sourceRoot import is exclusive with seed facts/layers/targets")
    output = local(root, arguments.output_directory, validator, missing=True)
    if os.path.lexists(output):
        raise ValueError("candidate output already exists; select a new destination")
    relative_parts = output.relative_to(root).parts
    if relative_parts[0].casefold() in {".identity", ".git", ".agents", ".codex", ".aws", "assets"}:
        raise ValueError("candidate output cannot occupy canonical, generated or repository-control paths")
    for parent in output.parents:
        if parent == root:
            break
        if os.path.lexists(parent / ".identity-manifest.json") or os.path.lexists(parent / ".identity"):
            raise ValueError("candidate output cannot be nested in another consumer or generated root")
    imported = "sourceRoot" in request
    files, directories, missing = (import_source if imported else seed_source)(root, request, validator, inputs)
    source_root = root if request.get("sourceRoot", ".") == "." else root / request["sourceRoot"]
    input_directories = [root / ".identity"]
    if imported:
        input_directories.extend(source_root / relative for relative in directories)
    for source in [*inputs, *input_directories]:
        if output == source or output in source.parents or source in output.parents:
            raise ValueError("candidate output overlaps supplied source")
    for relative in [*files, *directories]:
        if relative.split("/")[0].casefold() in {".git", ".agents", ".codex", ".aws", "initialization-report.json"}:
            raise ValueError("imported source collides with repository-control or report paths")
    # Requiring an existing parent avoids leaving new directory trees on failed preparation.
    regular_path(output.parent)
    if not output.parent.is_dir():
        raise ValueError("create the candidate parent directory explicitly before initialization")
    with tempfile.TemporaryDirectory(prefix=".identity-init-", dir=output.parent) as temporary:
        staged = Path(temporary)
        for relative in sorted(directories):
            local(staged, relative, validator, missing=True).mkdir(parents=True, exist_ok=True)
        for relative, content in sorted(files.items()):
            destination = local(staged, relative, validator, missing=True)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        diagnostics = validator.validate_identity(staged)
        report = {
            "schema": REPORT_SCHEMA,
            "status": "incomplete" if diagnostics or missing else "ready-for-review",
            "sourceValid": not diagnostics, "missing": sorted(missing),
            "diagnostics": [asdict(item) for item in diagnostics],
            "implementation": implementation,
            "compatibility": {"sourceSchema": "identity.project/v1", "acceptedSchemaMajor": 1,
                              "availableProfiles": validator.V1_PROFILE_VERSIONS},
            "inputs": {path.relative_to(root).as_posix(): {"sha256": digest(content), "bytes": len(content)}
                       for path, content in sorted(inputs.items())},
            "files": {relative: {"sha256": digest(content), "bytes": len(content)}
                      for relative, content in sorted(files.items())},
            "directories": sorted(directories),
            "limitations": ["Preparation is not human approval, producer capability or output verification.",
                            "The package version does not identify a reviewed Git revision; pin that separately.",
                            "Canonical adoption, generation and recovery are separate explicit operations."],
        }
        (staged / "initialization-report.json").write_bytes(json_bytes(report))
        for path, content in inputs.items():
            regular_path(path)
            if path.read_bytes() != content:
                raise ValueError("supplied input changed; no candidate was published")
        regular_path(output, missing=True)
        # Exclusive reservation prevents repeat invocation from replacing even an empty directory.
        # If a subsequent I/O failure occurs, retain this explicitly selected partial output
        # for inspection; cleanup is limited to our private staging directory.
        output.mkdir()
        for entry in sorted(staged.iterdir()):
            shutil.move(str(entry), str(output / entry.name))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--request", required=True)
    parser.add_argument("--output-directory", required=True)
    arguments = parser.parse_args()
    try:
        if sys.version_info < (3, 11):
            raise ValueError("Python 3.11 or newer is required")
        report = prepare(arguments)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"v1 initialization failed: {error}", file=sys.stderr)
        return 1
    print(f"Prepared v1 candidate: {arguments.output_directory} ({report['status']})")
    print("Review initialization-report.json; no canonical source was adopted or generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
