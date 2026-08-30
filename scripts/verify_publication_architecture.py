#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Verify Identity's accepted publication architecture without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse


ARCHITECTURE_PATH = Path("publication/identity-experience.architecture.json")
SCHEMA_PATH = Path("contracts/v1/publication-architecture.schema.json")
EXPECTED_TOP_LEVEL = {
    "$schema",
    "schema",
    "status",
    "decision",
    "scope",
    "adapters",
    "artifacts",
    "contentSources",
    "routes",
    "releaseEvidence",
    "qualityRequirements",
    "lifecycle",
    "futureExpansion",
}
EXPECTED_ADAPTERS = {
    "launchkit",
    "zensical",
    "reference-renderer",
    "route-composer",
}
EXPECTED_ARTIFACTS = {
    "identity-landing",
    "identity-documentation",
    "identity-architecture",
    "identity-legal",
    "identity-experience",
    "identity-brand-kit",
}
REQUIRED_ARTIFACT_BOUNDARIES = {
    "identity-landing": ("launchkit", "organization", "/identity/"),
    "identity-documentation": ("zensical", "organization", "/identity/docs/"),
    "identity-architecture": ("zensical", "organization", "/identity/architecture/"),
    "identity-legal": ("zensical", "organization", "/identity/legal/"),
    "identity-experience": ("route-composer", "organization", "/identity/"),
    "identity-brand-kit": ("reference-renderer", "brand-kit", "/"),
}
EXPECTED_CONTENT_SOURCES = {
    "compiled-identity",
    "authored-documentation",
    "authored-product-copy",
    "adapter-configuration",
}
REQUIRED_EVIDENCE = {
    "releaseTag",
    "releaseCommit",
    "sourceDigest",
    "assetProvenance",
    "approvalEvidence",
}
REQUIRED_QUALITY = {
    "accessible-name-and-alt-text",
    "contrast",
    "deterministic-build",
    "focus-visible",
    "keyboard-navigation",
    "no-javascript-readable",
    "offline-source-inputs",
    "reduced-motion",
    "responsive-layout",
    "route-and-link-integrity",
    "semantic-html",
}
EXPECTED_LIFECYCLE = {
    "preview",
    "build",
    "verify",
    "handoff",
    "publish",
    "rollback",
    "upgrade",
}
REQUIRED_ROUTES = {
    "organization-identity": ("organization", "/identity/", "page", "launchkit"),
    "organization-identity-noslash": ("organization", "/identity", "redirect", "route-composer"),
    "organization-identity-docs": ("organization", "/identity/docs/", "page", "zensical"),
    "organization-identity-architecture": (
        "organization",
        "/identity/architecture/",
        "page",
        "zensical",
    ),
    "organization-identity-legal": (
        "organization",
        "/identity/legal/",
        "page",
        "zensical",
    ),
    "organization-identity-manifest": ("organization", "/identity/publication.json", "manifest", "route-composer"),
    "organization-identity-brand-kit": ("organization", "/identity/brand-kit/", "redirect", "route-composer"),
    "organization-brand-alias": ("organization", "/brand/", "redirect", "route-composer"),
    "organization-design-alias": ("organization", "/design/", "redirect", "route-composer"),
    "organization-brand-kit-alias": ("organization", "/brand-kit/", "redirect", "route-composer"),
    "brand-kit-root": ("brand-kit", "/", "page", "reference-renderer"),
    "brand-kit-site-manifest": ("brand-kit", "/site.json", "manifest", "reference-renderer"),
    "brand-kit-release-manifest": (
        "brand-kit",
        "/packages/identity-brand-kit-v{version}.manifest.json",
        "manifest",
        "reference-renderer",
    ),
    "brand-kit-release-download": (
        "brand-kit",
        "/packages/identity-brand-kit-v{version}.zip",
        "download",
        "reference-renderer",
    ),
    "brand-kit-release-checksums": (
        "brand-kit",
        "/packages/identity-brand-kit-v{version}.SHA256SUMS",
        "download",
        "reference-renderer",
    ),
    "brand-kit-local-alias": ("brand-kit", "/brand-kit/", "redirect", "reference-renderer"),
}
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
IDENTIFIER = re.compile(r"^[a-z][a-z0-9-]*$")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root containing the publication contract.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def records_by_id(value: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(value):
        if not isinstance(record, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        identifier = record.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            errors.append(f"{label}[{index}] has an invalid id")
            continue
        if identifier in result:
            errors.append(f"{label} contains duplicate id: {identifier}")
            continue
        result[identifier] = record
    return result


def require_exact_ids(
    records: dict[str, dict[str, Any]], expected: set[str], label: str, errors: list[str]
) -> None:
    missing = sorted(expected - records.keys())
    unexpected = sorted(records.keys() - expected)
    if missing:
        errors.append(f"{label} missing required ids: {', '.join(missing)}")
    if unexpected:
        errors.append(f"{label} contains unaccepted ids: {', '.join(unexpected)}")


def is_https_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def verify_adapter_pins(adapters: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for identifier, adapter in adapters.items():
        if adapter.get("canonicalBrandSource") is not False:
            errors.append(f"adapter {identifier} must explicitly deny canonical brand authority")
        if not isinstance(adapter.get("pin"), dict):
            errors.append(f"adapter {identifier} must have a pin object")

    launchkit = adapters.get("launchkit", {})
    launchkit_pin = launchkit.get("pin", {})
    expected_launchkit = {
        "repository": "https://github.com/egohygiene/holon",
        "commit": "2600baff6f6d944094da81b77e1a9a2e9e7a1cd6",
        "profile": "landing-launchkit",
        "version": "1.0.0",
        "path": "blueprints/launchkit/blueprint.json",
        "gitBlob": "3629339d25facb1e5b36cf6ab381c0744f1e3a14",
    }
    if launchkit.get("role") != "landing" or launchkit.get("implementationOwner") != "egohygiene/holon":
        errors.append("LaunchKit responsibility must remain with the Holon landing profile")
    if launchkit_pin != expected_launchkit:
        errors.append("LaunchKit must match the accepted immutable Holon profile pin")

    zensical = adapters.get("zensical", {})
    zensical_pin = zensical.get("pin", {})
    expected_zensical = {
        "repository": "https://github.com/egohygiene/holon",
        "commit": "2600baff6f6d944094da81b77e1a9a2e9e7a1cd6",
        "profile": "docs-zensical",
        "version": "1.0.0",
        "path": "blueprints/zensical/blueprint.json",
        "gitBlob": "5f6e385d54d6271c7fe89f441787d6b253cf9fb0",
        "upstreamRepository": "https://github.com/zensical/zensical",
        "upstreamVersion": "0.0.57",
        "upstreamTag": "v0.0.57",
        "upstreamTagObject": "ad8188ee60ae9187d64a4fe7c4970d3a1947028d",
        "upstreamCommit": "f18bb9957cb2740e5dd66d4a438c780b4e15d64c",
        "license": "MIT",
        "developmentStatus": "alpha",
    }
    if (
        zensical.get("role") != "documentation"
        or zensical.get("status") != "available"
        or zensical.get("implementationOwner") != "egohygiene/holon"
    ):
        errors.append("Zensical responsibility must remain with the Holon docs profile")
    if zensical_pin != expected_zensical:
        errors.append("Zensical must match the accepted immutable Holon profile and upstream pin")

    route_composer = adapters.get("route-composer", {})
    route_composer_pin = route_composer.get("pin", {})
    expected_route_composer = {
        "repository": "https://github.com/egohygiene/holon",
        "commit": "2600baff6f6d944094da81b77e1a9a2e9e7a1cd6",
        "profile": "site-suite",
        "version": "1.0.0",
        "path": "blueprints/site-suite/blueprint.json",
        "gitBlob": "2635781f74fd1ba5ee5e6d742dcfabdd0289606b",
        "input": "content-addressed-identity-experience-artifact",
        "publicationOwner": "egohygiene/relay",
        "networkAtBuild": False,
    }
    if (
        route_composer.get("role") != "publication-composer"
        or route_composer.get("status") != "dogfood-adapter"
        or route_composer.get("implementationOwner") != "egohygiene/identity"
    ):
        errors.append("route composition must remain a bounded Identity extension")
    if route_composer_pin != expected_route_composer:
        errors.append("route composition must extend the accepted immutable Holon site-suite pin")

    for identifier in ("launchkit", "zensical", "route-composer"):
        pin = adapters.get(identifier, {}).get("pin", {})
        commit = pin.get("commit")
        if not isinstance(commit, str) or not HEX_40.fullmatch(commit):
            errors.append(f"adapter {identifier} must pin a full commit SHA")
        version = pin.get("version")
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            errors.append(f"adapter {identifier} must pin an exact semantic version")
        for value in pin.values():
            if value in {"main", "master", "latest", "stable"}:
                errors.append(f"adapter {identifier} contains a moving reference")


def verify_content_sources(
    sources: dict[str, dict[str, Any]], repository_root: Path, errors: list[str]
) -> None:
    for identifier, source in sources.items():
        paths = source.get("paths")
        if not isinstance(paths, list) or not paths:
            errors.append(f"content source {identifier} must declare paths")
            continue
        for raw_path in paths:
            if not isinstance(raw_path, str) or raw_path.startswith("/") or ".." in Path(raw_path).parts:
                errors.append(f"content source {identifier} has an unsafe repository path")
                continue
            if source.get("mustExist") is True:
                target = repository_root / raw_path.rstrip("/")
                if not target.exists():
                    errors.append(f"content source {identifier} is missing required path: {raw_path}")

    compiled = sources.get("compiled-identity", {})
    if compiled.get("authority") != "identity-contracts" or compiled.get("consumption") != "read-only":
        errors.append("compiled Identity outputs must remain canonical and read-only to adapters")
    adapter = sources.get("adapter-configuration", {})
    if adapter.get("authority") != "adapter-only" or adapter.get("consumption") != "references-only":
        errors.append("adapter configuration must be noncanonical and references-only")


def verify_routes(
    routes: dict[str, dict[str, Any]],
    adapters: dict[str, dict[str, Any]],
    artifacts: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    seen_paths: set[tuple[str, str]] = set()
    for identifier, route in routes.items():
        host = route.get("host")
        path = route.get("path")
        if host not in {"organization", "brand-kit"}:
            errors.append(f"route {identifier} has an invalid host")
        if not isinstance(path, str) or not path.startswith("/") or ".." in path:
            errors.append(f"route {identifier} has an invalid path")
            continue
        path_key = (str(host), path)
        if path_key in seen_paths:
            errors.append(f"route collision on {host}:{path}")
        seen_paths.add(path_key)

        kind = route.get("kind")
        owner = route.get("owner")
        if owner not in adapters:
            errors.append(f"route {identifier} references unknown owner adapter: {owner}")
        if kind == "redirect":
            if not is_https_url(route.get("target")):
                errors.append(f"redirect route {identifier} must have an HTTPS target")
            if "adapter" in route or "artifact" in route:
                errors.append(f"redirect route {identifier} cannot claim a rendered artifact")
        else:
            artifact = route.get("artifact")
            if artifact not in artifacts:
                errors.append(f"route {identifier} references unknown artifact: {artifact}")
            if "target" in route:
                errors.append(f"non-redirect route {identifier} cannot have a target")
        if kind == "page" and route.get("adapter") not in adapters:
            errors.append(f"page route {identifier} must reference a known adapter")

    for identifier, expected in REQUIRED_ROUTES.items():
        route = routes.get(identifier)
        if route is None:
            continue
        actual = (route.get("host"), route.get("path"), route.get("kind"), route.get("owner"))
        if actual != expected:
            errors.append(f"route {identifier} does not match the accepted route map")

    brand_target = "https://identity.egohygiene.io/"
    for identifier in {
        "organization-identity-brand-kit",
        "organization-brand-alias",
        "organization-design-alias",
        "organization-brand-kit-alias",
        "brand-kit-local-alias",
    }:
        if routes.get(identifier, {}).get("target") != brand_target:
            errors.append(f"route {identifier} must redirect to the canonical Brand Kit")
    if routes.get("organization-identity-noslash", {}).get("target") != "https://egohygiene.io/identity/":
        errors.append("/identity must normalize to the canonical trailing-slash route")


def verify_release_and_quality(
    document: dict[str, Any], routes: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    evidence = document.get("releaseEvidence")
    if not isinstance(evidence, dict):
        errors.append("releaseEvidence must be an object")
    else:
        fields = evidence.get("requiredFields")
        if not isinstance(fields, list) or set(fields) != REQUIRED_EVIDENCE or len(fields) != len(set(fields)):
            errors.append("release evidence must contain each accepted inspectable field exactly once")
        for key in ("experienceManifestRoute", "brandKitManifestRoute"):
            route = routes.get(evidence.get(key), {})
            if route.get("kind") != "manifest":
                errors.append(f"releaseEvidence.{key} must reference a manifest route")
        if evidence.get("comparison") != "exact-release-binding":
            errors.append("the two public surfaces must use an exact release binding")

    quality = document.get("qualityRequirements")
    if not isinstance(quality, list) or set(quality) != REQUIRED_QUALITY or len(quality) != len(set(quality)):
        errors.append("qualityRequirements must contain every accepted quality gate exactly once")


def verify_lifecycle(document: dict[str, Any], errors: list[str]) -> None:
    lifecycle = document.get("lifecycle")
    if not isinstance(lifecycle, list):
        errors.append("lifecycle must be an array")
        return
    stages: list[str] = []
    for index, record in enumerate(lifecycle):
        if not isinstance(record, dict):
            errors.append(f"lifecycle[{index}] must be an object")
            continue
        stage = record.get("stage")
        if isinstance(stage, str):
            stages.append(stage)
        requirements = record.get("requirements")
        if not isinstance(requirements, list) or not requirements or not all(
            isinstance(requirement, str) and requirement.strip() for requirement in requirements
        ):
            errors.append(f"lifecycle stage {stage!r} must have non-empty requirements")
    if set(stages) != EXPECTED_LIFECYCLE or len(stages) != len(set(stages)):
        errors.append("lifecycle must define preview, build, verify, handoff, publish, rollback, and upgrade once")


def verify_document(document: Any, repository_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["publication architecture must be a JSON object"]
    if set(document) != EXPECTED_TOP_LEVEL:
        missing = sorted(EXPECTED_TOP_LEVEL - document.keys())
        unexpected = sorted(document.keys() - EXPECTED_TOP_LEVEL)
        if missing:
            errors.append(f"publication architecture missing keys: {', '.join(missing)}")
        if unexpected:
            errors.append(f"publication architecture contains unknown keys: {', '.join(unexpected)}")
    if document.get("$schema") != "../contracts/v1/publication-architecture.schema.json":
        errors.append("publication architecture must reference the local v1 schema")
    if document.get("schema") != "identity.publication-architecture/v1":
        errors.append("unexpected publication architecture schema identity")
    if document.get("status") != "accepted":
        errors.append("publication architecture must be accepted before implementation")

    decision = document.get("decision")
    if not isinstance(decision, str) or not (repository_root / decision).is_file():
        errors.append("publication architecture must reference an existing ADR")
    if not (repository_root / SCHEMA_PATH).is_file():
        errors.append(f"missing publication architecture schema: {SCHEMA_PATH}")

    expected_scope = {
        "repository": "https://github.com/egohygiene/identity",
        "experienceCanonicalUrl": "https://egohygiene.io/identity/",
        "brandKitCanonicalUrl": "https://identity.egohygiene.io/",
        "organizationHomepageOwnedHere": False,
    }
    if document.get("scope") != expected_scope:
        errors.append("scope must preserve the accepted two-host ownership boundary")

    adapters = records_by_id(document.get("adapters"), "adapters", errors)
    artifacts = records_by_id(document.get("artifacts"), "artifacts", errors)
    sources = records_by_id(document.get("contentSources"), "contentSources", errors)
    routes = records_by_id(document.get("routes"), "routes", errors)
    require_exact_ids(adapters, EXPECTED_ADAPTERS, "adapters", errors)
    require_exact_ids(artifacts, EXPECTED_ARTIFACTS, "artifacts", errors)
    require_exact_ids(sources, EXPECTED_CONTENT_SOURCES, "contentSources", errors)
    require_exact_ids(routes, set(REQUIRED_ROUTES), "routes", errors)

    verify_adapter_pins(adapters, errors)
    verify_content_sources(sources, repository_root, errors)
    for identifier, artifact in artifacts.items():
        actual_boundary = (
            artifact.get("owner"),
            artifact.get("host"),
            artifact.get("basePath"),
        )
        if actual_boundary != REQUIRED_ARTIFACT_BOUNDARIES.get(identifier):
            errors.append(f"artifact {identifier} does not match the accepted ownership boundary")
        inputs = artifact.get("inputs")
        if not isinstance(inputs, list) or not inputs:
            errors.append(f"artifact {identifier} must declare inputs")
            continue
        unknown = set(inputs) - sources.keys() - artifacts.keys()
        if unknown:
            errors.append(f"artifact {identifier} has unknown inputs: {', '.join(sorted(unknown))}")
        if not isinstance(artifact.get("rollback"), str) or not artifact["rollback"].strip():
            errors.append(f"artifact {identifier} must define rollback behavior")
    verify_routes(routes, adapters, artifacts, errors)
    verify_release_and_quality(document, routes, errors)
    verify_lifecycle(document, errors)

    expected_future = {
        "dogfoodIssue": "https://github.com/egohygiene/identity/issues/56",
        "implementationIssue": "https://github.com/egohygiene/identity/issues/57",
        "generalizationOwner": "https://github.com/egohygiene/holon/issues/4",
        "universalGeneratorOwnedHere": False,
    }
    if document.get("futureExpansion") != expected_future:
        errors.append("future expansion must stay bounded to #57 and Holon #4")
    return errors


def verify_repository(repository_root: Path) -> list[str]:
    architecture = repository_root / ARCHITECTURE_PATH
    if not architecture.is_file():
        return [f"missing publication architecture: {ARCHITECTURE_PATH}"]
    try:
        document = load_json(architecture)
        load_json(repository_root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as error:
        return [f"unable to parse publication architecture contract: {error}"]
    return verify_document(document, repository_root)


def main() -> int:
    arguments = parse_arguments()
    errors = verify_repository(arguments.repository_root.resolve())
    if errors:
        print("publication architecture verification failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("publication architecture verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
