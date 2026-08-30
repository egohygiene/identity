#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Build Identity's deterministic Holon site-suite dogfood composite."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Iterable


ARCHITECTURE_PATH = Path("publication/identity-experience.architecture.json")
CONTENT_PATH = Path("publication/identity-experience.content.json")
MASCOT_SOURCE_PATH = Path("mascot/kern.character.json")
MASCOT_PACKAGE_PATH = Path("assets/identity/mascot/manifest.json")
EXPERIENCE_PATH = Path("experience")
PUBLICATION_SCHEMA = "identity.experience-publication/v1"
STABLE_TAG = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
HOLON_ADAPTERS = ("launchkit", "zensical", "route-composer")


class BuildError(RuntimeError):
    """Raised when reviewed inputs cannot produce a verified composite."""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--holon-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--release-commit", required=True)
    parser.add_argument("--uv-executable", default="uv")
    parser.add_argument("--corepack-executable", default="corepack")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BuildError(f"unable to read JSON input {path}: {error}") from error
    if not isinstance(value, dict):
        raise BuildError(f"JSON input must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha1(
        f"blob {len(content)}\0".encode() + content,
        usedforsecurity=False,
    ).hexdigest()


def safe_source(repository_root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value or value.startswith("/"):
        raise BuildError(f"unsafe repository path: {value!r}")
    relative = Path(value)
    if ".." in relative.parts:
        raise BuildError(f"unsafe repository path: {value!r}")
    path = (repository_root / relative).resolve()
    root = repository_root.resolve()
    if root not in path.parents or not path.is_file():
        raise BuildError(f"required source file is missing or unsafe: {value}")
    return path


def command(arguments: list[str], *, cwd: Path) -> None:
    try:
        subprocess.run(arguments, cwd=cwd, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        raise BuildError(f"command failed in {cwd}: {' '.join(arguments)}") from error


def selected_adapter(architecture: dict[str, Any], adapter_id: str) -> dict[str, Any]:
    for adapter in architecture.get("adapters", []):
        if isinstance(adapter, dict) and adapter.get("id") == adapter_id:
            return adapter
    raise BuildError(f"accepted architecture does not define adapter {adapter_id}")


def verify_inventory(
    blueprint: dict[str, Any],
    source_root: Path,
    label: str,
) -> list[Path]:
    reviewed: list[Path] = []
    for record in blueprint.get("files", []):
        if not isinstance(record, dict):
            raise BuildError(f"Holon {label} file inventory is malformed")
        source = source_root / str(record.get("path"))
        if not source.is_file() or sha256_file(source) != record.get("sha256"):
            raise BuildError(f"Holon {label} source inventory drifted: {record.get('path')}")
        reviewed.append(source)
    if not reviewed:
        raise BuildError(f"Holon {label} file inventory is empty")
    return reviewed


def verify_holon_source(
    holon_source: Path,
    architecture: dict[str, Any],
) -> tuple[dict[str, Any], list[Path]]:
    pins = {
        adapter_id: selected_adapter(architecture, adapter_id).get("pin", {})
        for adapter_id in HOLON_ADAPTERS
    }
    commits = {pin.get("commit") for pin in pins.values()}
    if len(commits) != 1 or not all(
        isinstance(value, str) and COMMIT.fullmatch(value) for value in commits
    ):
        raise BuildError("Holon adapters must share one accepted immutable commit")
    accepted_commit = next(iter(commits))
    try:
        actual_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=holon_source,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise BuildError("Holon source must be an exact Git checkout") from error
    if actual_commit != accepted_commit:
        raise BuildError("Holon checkout does not match the accepted site-suite commit")

    blueprints: dict[str, dict[str, Any]] = {}
    reviewed: list[Path] = []
    roots = {
        "launchkit": holon_source / "blueprints/launchkit/files",
        "zensical": holon_source / "blueprints/zensical/files",
        "route-composer": holon_source / "blueprints/site-suite/files",
    }
    for adapter_id, pin in pins.items():
        blueprint_path = holon_source / str(pin.get("path"))
        blueprint = read_json(blueprint_path)
        if git_blob(blueprint_path) != pin.get("gitBlob"):
            raise BuildError(f"Holon {adapter_id} blueprint does not match its accepted Git blob")
        if blueprint.get("version") != pin.get("version"):
            raise BuildError(f"Holon {adapter_id} profile version drifted")
        blueprints[adapter_id] = blueprint
        reviewed.append(blueprint_path)
        reviewed.extend(verify_inventory(blueprint, roots[adapter_id], adapter_id))

    launchkit = blueprints["launchkit"]
    base_path = holon_source / str(launchkit.get("extends", {}).get("profile"))
    if (
        not base_path.is_file()
        or sha256_file(base_path) != launchkit.get("extends", {}).get("sha256")
    ):
        raise BuildError("Holon LaunchKit base profile digest drifted")
    base = read_json(base_path)
    reviewed.append(base_path)
    reviewed.extend(
        verify_inventory(
            base,
            holon_source / "blueprints/react-vite/files",
            "react-vite",
        )
    )

    suite = blueprints["route-composer"]
    if suite.get("schema") != "holon.site-suite-profile/v1":
        raise BuildError("Holon site-suite profile identity drifted")
    variant = suite.get("variants", {}).get("launchkit")
    if not isinstance(variant, dict) or variant.get("render_overlays") != [
        "blueprints/launchkit/files",
        "blueprints/zensical/files",
        "blueprints/site-suite/files",
    ]:
        raise BuildError("Holon LaunchKit site-suite composition order drifted")
    for profile in suite.get("profiles", {}).values():
        if not isinstance(profile, dict):
            raise BuildError("Holon site-suite profile references are malformed")
        profile_path = holon_source / str(profile.get("path"))
        if not profile_path.is_file() or sha256_file(profile_path) != profile.get("sha256"):
            raise BuildError(f"Holon site-suite profile digest drifted: {profile.get('path')}")
    schema_path = holon_source / "schemas/site-suite-content.v1.schema.json"
    if not schema_path.is_file():
        raise BuildError("Holon site-suite content schema is missing")
    reviewed.extend(
        [
            schema_path,
            holon_source / "tools/materialization/common.py",
            holon_source / "tools/launchkit_blueprint.py",
            holon_source / "tools/site_suite_blueprint.py",
        ]
    )
    return suite, reviewed


def verify_holon_content(
    holon_source: Path,
    launchkit: dict[str, Any],
    site_suite: dict[str, Any],
) -> None:
    tools_path = (holon_source / "tools").resolve()
    sys.path.insert(0, str(tools_path))
    try:
        launchkit_module = importlib.import_module("launchkit_blueprint")
        suite_module = importlib.import_module("site_suite_blueprint")
        errors = launchkit_module.validate_content(launchkit, "launchkit_content")
        errors.extend(suite_module.validate_site_content(site_suite, "site_suite_content"))
    finally:
        sys.path.pop(0)
    if errors:
        raise BuildError("compiled Holon content is invalid: " + "; ".join(errors))


def verify_dependency_locks(holon_source: Path, suite: dict[str, Any]) -> None:
    variant = suite["variants"]["launchkit"]
    materialized_roots = [variant["render_source"], *variant["render_overlays"]]
    node_lock = holon_source / "blueprints/react-vite/files/pnpm-lock.yaml"
    python_lock = holon_source / "blueprints/zensical/files/site-docs/requirements.lock.txt"
    if "blueprints/react-vite/files" not in materialized_roots or not node_lock.is_file():
        raise BuildError("the Holon site suite lacks its complete pnpm lock")
    lock_text = python_lock.read_text(encoding="utf-8") if python_lock.is_file() else ""
    if "zensical==0.0.57" not in lock_text or "--hash=sha256:" not in lock_text:
        raise BuildError("the Holon site suite lacks its hash-locked Zensical graph")


def mascot_projection(repository_root: Path, content: dict[str, Any]) -> dict[str, Any]:
    source = read_json(repository_root / MASCOT_SOURCE_PATH)
    package = read_json(repository_root / MASCOT_PACKAGE_PATH)
    if source.get("status") != "approved" or package.get("character") != source.get("id"):
        raise BuildError("Kern source and package are not an approved matching projection")
    variant_id = content.get("assets", {}).get("mascot")
    variant = next((item for item in source.get("variants", []) if item.get("id") == variant_id), None)
    file_record = next(
        (item for item in package.get("files", []) if item.get("id") == f"kern-{variant_id}"),
        None,
    )
    if not isinstance(variant, dict) or not isinstance(file_record, dict):
        raise BuildError(f"approved mascot variant is unavailable: {variant_id}")
    asset = safe_source(repository_root, file_record.get("path"))
    if sha256_file(asset) != file_record.get("sha256"):
        raise BuildError("selected Kern projection does not match its package checksum")
    accessibility = source.get("accessibility", {})
    if accessibility.get("neverSoleCarrier") is not True or not variant.get("altText"):
        raise BuildError("selected Kern projection lacks its accessibility contract")
    return {
        "id": source["id"],
        "variant": variant_id,
        "path": file_record["path"],
        "publicPath": f"/identity/{file_record['path']}",
        "sha256": file_record["sha256"],
        "altText": variant["altText"],
        "license": source["license"],
        "approval": source["approval"],
        "provenance": "mascot/provenance.json",
        "usage": "mascot/README.md",
    }


def compile_launchkit_content(
    content: dict[str, Any],
    mascot: dict[str, Any],
    release_tag: str,
    release_commit: str,
) -> dict[str, Any]:
    launchkit = deepcopy(content.get("launchkit"))
    if not isinstance(launchkit, dict):
        raise BuildError("experience content lacks its LaunchKit section")
    demo = launchkit.get("demo")
    if not isinstance(demo, dict) or demo.pop("assetRef", None) != "mascot":
        raise BuildError("LaunchKit demo must resolve the governed mascot reference")
    demo["asset"] = {"src": mascot["publicPath"], "alt": mascot["altText"]}
    demo["metrics"] = [
        {"label": "Release", "value": release_tag},
        {"label": "Commit", "value": release_commit[:12]},
    ]
    proof = launchkit.get("proof")
    if not isinstance(proof, dict) or not isinstance(proof.get("items"), list):
        raise BuildError("LaunchKit content must expose its evidence proof strip")
    proof["items"].extend([f"Release {release_tag}", f"Commit {release_commit[:12]}"])
    return launchkit


def render_holon_suite(
    holon_source: Path,
    suite: dict[str, Any],
    resolved_manifest: dict[str, Any],
    target: Path,
) -> None:
    tools_path = (holon_source / "tools").resolve()
    sys.path.insert(0, str(tools_path))
    try:
        common = importlib.import_module("materialization.common")
        render_source_bytes = common.render_source_bytes
    finally:
        sys.path.pop(0)
    variant = suite["variants"]["launchkit"]

    def apply(source_root: Path) -> None:
        for source in sorted(source_root.rglob("*")):
            if source.is_symlink():
                raise BuildError(f"Holon source contains a symlink: {source}")
            if not source.is_file():
                continue
            relative = source.relative_to(source_root)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(
                render_source_bytes(
                    source.read_bytes(),
                    resolved_manifest,
                    relative.as_posix(),
                )
            )

    apply(holon_source / variant["render_source"])
    for overlay in variant["render_overlays"]:
        apply(holon_source / overlay)


def apply_identity_inputs(
    repository_root: Path,
    site: Path,
    content: dict[str, Any],
    mascot: dict[str, Any],
) -> list[Path]:
    public_root = site / "public"
    selected = [
        mascot["path"],
        content["assets"]["socialImage"],
        content["assets"]["favicon"],
        content["assets"]["palette"],
    ]
    copied: list[Path] = []
    for relative in selected:
        source = safe_source(repository_root, relative)
        destination = public_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied.append(source)

    palette = safe_source(repository_root, content["assets"]["palette"])
    landing_style = repository_root / EXPERIENCE_PATH / "styles/identity-experience.css"
    docs_style = repository_root / EXPERIENCE_PATH / "styles/zensical-identity.css"
    (site / "src/styles/identity.css").write_bytes(
        palette.read_bytes().rstrip() + b"\n\n" + landing_style.read_bytes()
    )
    holon_docs_style = site / "site-docs/styles/extra.css"
    holon_docs_style.write_bytes(
        holon_docs_style.read_bytes().rstrip()
        + b"\n\n"
        + palette.read_bytes().rstrip()
        + b"\n\n"
        + docs_style.read_bytes()
    )

    # Identity's accepted offline/runtime boundary uses system fonts. Holon's
    # shared profile intentionally leaves this native Zensical theme setting
    # to consumers, so apply the exact bounded configuration before rendering.
    docs_builder = site / "site_docs.py"
    docs_builder_text = docs_builder.read_text(encoding="utf-8")
    setting = "            'custom_dir = \"overrides\"',\n"
    if docs_builder_text.count(setting) != 1:
        raise BuildError("Holon Zensical theme configuration boundary drifted")
    docs_builder.write_text(
        docs_builder_text.replace(setting, setting + '            "font = false",\n'),
        encoding="utf-8",
    )
    return [*copied, landing_style, docs_style]


def build_site_suite(
    repository_root: Path,
    holon_source: Path,
    suite: dict[str, Any],
    content: dict[str, Any],
    launchkit: dict[str, Any],
    mascot: dict[str, Any],
    work: Path,
    uv: str,
    corepack: str,
) -> tuple[Path, list[Path]]:
    site_config = content["site"]
    asset_base = site_config["canonicalUrl"]
    parameters = {
        "canonical_url": site_config["canonicalUrl"],
        "identity_favicon_url": f"{asset_base}{content['assets']['favicon']}",
        "identity_social_image_url": f"{asset_base}{content['assets']['socialImage']}",
        "identity_stylesheet": f"{asset_base}{content['assets']['palette']}",
        "launchkit_content": launchkit,
        "package_name": site_config["packageName"],
        "repository_url": "https://github.com/egohygiene/identity",
        "site_base_path": site_config["basePath"],
        "site_description": site_config["description"],
        "site_suite_content": content["siteSuite"],
        "site_title": site_config["title"],
    }
    accepted_commit = selected_adapter(
        read_json(repository_root / ARCHITECTURE_PATH),
        "route-composer",
    )["pin"]["commit"]
    resolved_manifest = {
        "schema_version": "1.0.0",
        "repository": "egohygiene/identity",
        "repository_class": "product",
        "security_level": "hardened",
        "pins": {"foundation": f"egohygiene/holon@{accepted_commit}"},
        "capabilities": ["site-react-vite", "landing-launchkit", "docs-zensical"],
        "sites": ["landing", "docs", "architecture", "legal"],
        "preserve_paths": [],
        "parameters": parameters,
        "ownership": {"generator": "egohygiene/holon", "preserve_paths": []},
    }
    site = work / "site-suite"
    site.mkdir()
    render_holon_suite(holon_source, suite, resolved_manifest, site)
    identity_inputs = apply_identity_inputs(repository_root, site, content, mascot)

    command([corepack, "pnpm", "install", "--frozen-lockfile"], cwd=site)
    environment = work / "zensical-environment"
    command([uv, "venv", "--python", sys.executable, str(environment)], cwd=site)
    python = environment / "bin/python"
    command(
        [
            uv,
            "pip",
            "install",
            "--python",
            str(python),
            "--require-hashes",
            "--requirement",
            "site-docs/requirements.lock.txt",
        ],
        cwd=site,
    )
    command(
        [
            str(python),
            str(repository_root / EXPERIENCE_PATH / "site_suite_adapter.py"),
            "--site-root",
            str(site),
            "--corepack-executable",
            corepack,
            "check",
        ],
        cwd=site,
    )
    return site / "dist", identity_inputs


def copy_tree_without_collisions(source: Path, destination: Path, owned: set[str]) -> None:
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source).as_posix()
        if relative in owned:
            raise BuildError(f"composite route collision: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        owned.add(relative)


def redirect_html(target: str) -> bytes:
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<meta http-equiv=\"refresh\" content=\"0; url={target}\">"
        f"<link rel=\"canonical\" href=\"{target}\"><title>Redirecting</title></head>"
        f"<body><main><h1>Identity Brand Kit</h1><p><a href=\"{target}\">Continue to the canonical Brand Kit</a>.</p>"
        "</main></body></html>\n"
    ).encode()


def inventory(root: Path, *, excluded: Iterable[str] = ()) -> list[dict[str, Any]]:
    exclusions = set(excluded)
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "sizeBytes": path.stat().st_size,
        }
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.relative_to(root).as_posix() not in exclusions
    ]


def source_digest(paths: Iterable[Path], repository_root: Path, holon_source: Path) -> str:
    records = []
    for path in set(path.resolve() for path in paths):
        if path == repository_root or repository_root in path.parents:
            label = f"identity:{path.relative_to(repository_root).as_posix()}"
        elif path == holon_source or holon_source in path.parents:
            label = f"holon:{path.relative_to(holon_source).as_posix()}"
        else:
            raise BuildError(f"source digest input is outside reviewed roots: {path}")
        records.append(
            {"path": label, "sha256": sha256_file(path), "sizeBytes": path.stat().st_size}
        )
    records.sort(key=lambda record: record["path"])
    return sha256_bytes(canonical_bytes(records))


def compose(
    repository_root: Path,
    holon_source: Path,
    output: Path,
    suite_artifact: Path,
    content: dict[str, Any],
    architecture: dict[str, Any],
    mascot: dict[str, Any],
    release_tag: str,
    release_commit: str,
    source_paths: list[Path],
) -> dict[str, Any]:
    if output.exists():
        if output == Path(output.anchor) or output == repository_root:
            raise BuildError("refusing to replace a broad output path")
        shutil.rmtree(output)
    identity_root = output / "identity"
    identity_root.mkdir(parents=True)
    owned: set[str] = set()
    copy_tree_without_collisions(suite_artifact, identity_root, owned)
    (identity_root / "publication.json").unlink(missing_ok=True)
    redirect = identity_root / "brand-kit/index.html"
    redirect.parent.mkdir(parents=True, exist_ok=True)
    redirect.write_bytes(redirect_html("https://identity.egohygiene.io/"))

    checksummed = inventory(identity_root)
    checksums = identity_root / "SHA256SUMS"
    checksums.write_text(
        "".join(f"{record['sha256']}  {record['path']}\n" for record in checksummed),
        encoding="utf-8",
    )
    manifest_inventory = inventory(identity_root, excluded=("publication.json",))
    artifact_digest = sha256_bytes(canonical_bytes(manifest_inventory))
    frameworks = []
    for adapter_id in HOLON_ADAPTERS:
        adapter = selected_adapter(architecture, adapter_id)
        frameworks.append(
            {"id": adapter_id, "role": adapter["role"], "pin": adapter["pin"]}
        )
    manifest = {
        "$schema": "https://identity.egohygiene.io/contracts/v1/identity-experience-publication.schema.json",
        "schema": PUBLICATION_SCHEMA,
        "canonicalUrl": content["site"]["canonicalUrl"],
        "release": {
            "tag": release_tag,
            "commit": release_commit,
            "repository": "https://github.com/egohygiene/identity",
            "url": f"https://github.com/egohygiene/identity/releases/tag/{release_tag}",
            "brandKitEvidence": "https://identity.egohygiene.io/site.json",
        },
        "sourceDigest": source_digest(source_paths, repository_root, holon_source),
        "frameworks": frameworks,
        "mascot": mascot,
        "evidence": {
            "assetProvenance": [
                "assets/identity/manifest.json",
                "assets/identity/mascot/manifest.json",
                "mascot/provenance.json",
            ],
            "approvalEvidence": ["mascot/approval.json"],
            "rights": ["mascot/LICENSE.md"],
            "architecture": ARCHITECTURE_PATH.as_posix(),
            "visualBaselines": "experience/visual-baselines.json",
            "siteSuiteManifest": "site-suite.manifest.json",
        },
        "routes": [
            {"path": "/identity/", "kind": "page", "owner": "launchkit", "delivery": "artifact"},
            {"path": "/identity", "kind": "redirect", "owner": "route-composer", "delivery": "route-owner", "target": "https://egohygiene.io/identity/"},
            {"path": "/identity/docs/", "kind": "page", "owner": "zensical", "delivery": "artifact"},
            {"path": "/identity/architecture/", "kind": "page", "owner": "zensical", "delivery": "artifact"},
            {"path": "/identity/legal/", "kind": "page", "owner": "zensical", "delivery": "artifact"},
            {"path": "/identity/publication.json", "kind": "manifest", "owner": "route-composer", "delivery": "artifact"},
            {"path": "/identity/brand-kit/", "kind": "redirect", "owner": "route-composer", "delivery": "artifact", "target": "https://identity.egohygiene.io/"},
            {"path": "/brand/", "kind": "redirect", "owner": "route-composer", "delivery": "route-owner", "target": "https://identity.egohygiene.io/"},
            {"path": "/design/", "kind": "redirect", "owner": "route-composer", "delivery": "route-owner", "target": "https://identity.egohygiene.io/"},
            {"path": "/brand-kit/", "kind": "redirect", "owner": "route-composer", "delivery": "route-owner", "target": "https://identity.egohygiene.io/"},
        ],
        "artifact": {
            "algorithm": "sha256",
            "digest": artifact_digest,
            "inventory": manifest_inventory,
            "checksums": "SHA256SUMS",
        },
        "handoff": {
            "basePath": "/identity/",
            "installationOwner": "egohygiene/relay-and-organization-site",
            "reviewRequired": True,
            "rebuildAllowed": False,
            "candidate": True,
            "installationAuthorized": False,
            "rollback": "Reinstall the preceding verified composite without rebuilding it.",
        },
    }
    (identity_root / "publication.json").write_bytes(canonical_bytes(manifest))
    return manifest


def build(
    repository_root: Path,
    holon_source: Path,
    output: Path,
    release_tag: str,
    release_commit: str,
    uv: str = "uv",
    corepack: str = "corepack",
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    holon_source = holon_source.resolve()
    output = output.resolve()
    if output.parent != repository_root or not output.name.startswith(".identity-experience-"):
        raise BuildError(
            "--output must be a dedicated .identity-experience-* directory in the repository root"
        )
    if STABLE_TAG.fullmatch(release_tag) is None:
        raise BuildError("--release-tag must be a stable semantic version tag")
    if COMMIT.fullmatch(release_commit) is None:
        raise BuildError("--release-commit must be a full lowercase commit SHA")
    architecture = read_json(repository_root / ARCHITECTURE_PATH)
    content = read_json(repository_root / CONTENT_PATH)
    if (
        architecture.get("status") != "accepted"
        or content.get("schema") != "identity.experience-content/v1"
    ):
        raise BuildError("experience inputs are not the accepted v1 contracts")
    if content.get("site", {}).get("canonicalUrl") != architecture.get("scope", {}).get(
        "experienceCanonicalUrl"
    ):
        raise BuildError("experience content canonical URL diverges from the accepted architecture")

    suite, holon_inputs = verify_holon_source(holon_source, architecture)
    verify_dependency_locks(holon_source, suite)
    mascot = mascot_projection(repository_root, content)
    launchkit = compile_launchkit_content(content, mascot, release_tag, release_commit)
    site_suite_content = content.get("siteSuite")
    if not isinstance(site_suite_content, dict):
        raise BuildError("experience content lacks its Holon site-suite section")
    verify_holon_content(holon_source, launchkit, site_suite_content)

    with tempfile.TemporaryDirectory(prefix="identity-experience-") as temporary:
        work = Path(temporary)
        suite_artifact, identity_inputs = build_site_suite(
            repository_root,
            holon_source,
            suite,
            content,
            launchkit,
            mascot,
            work,
            uv,
            corepack,
        )
        source_paths = [
            repository_root / ARCHITECTURE_PATH,
            repository_root / CONTENT_PATH,
            repository_root / MASCOT_SOURCE_PATH,
            repository_root / MASCOT_PACKAGE_PATH,
            repository_root / "mascot/approval.json",
            repository_root / "mascot/provenance.json",
            repository_root / "mascot/LICENSE.md",
            repository_root / "assets/identity/manifest.json",
            repository_root / EXPERIENCE_PATH / "site_suite_adapter.py",
            repository_root / EXPERIENCE_PATH / "visual-baselines.json",
            repository_root / "contracts/v1/identity-experience-content.schema.json",
            repository_root / "contracts/v1/identity-experience-publication.schema.json",
            repository_root / "scripts/build_identity_experience.py",
            repository_root / "scripts/verify_identity_experience.py",
            *holon_inputs,
            *identity_inputs,
        ]
        return compose(
            repository_root,
            holon_source,
            output,
            suite_artifact,
            content,
            architecture,
            mascot,
            release_tag,
            release_commit,
            source_paths,
        )


def main() -> int:
    arguments = parse_arguments()
    try:
        manifest = build(
            arguments.repository_root,
            arguments.holon_source,
            arguments.output,
            arguments.release_tag,
            arguments.release_commit,
            arguments.uv_executable,
            arguments.corepack_executable,
        )
    except BuildError as error:
        print(f"identity experience build failed: {error}", file=sys.stderr)
        return 1
    print(f"built Identity experience {manifest['artifact']['digest']} at {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
