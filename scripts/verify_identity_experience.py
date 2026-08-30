#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Verify a composed Identity dogfood artifact without mutating it."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any
from urllib.parse import urlsplit
from urllib.request import urlopen


PUBLICATION_SCHEMA = "identity.experience-publication/v1"
STABLE_TAG = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
PUBLIC_PREFIX = "/identity/"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--expected-release-tag")
    parser.add_argument("--expected-release-commit")
    parser.add_argument("--verify-live-brand-kit", action="store_true")
    return parser.parse_args()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path, excluded: set[str]) -> list[dict[str, Any]]:
    return [
        {"path": path.relative_to(root).as_posix(), "sha256": sha256(path), "sizeBytes": path.stat().st_size}
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.relative_to(root).as_posix() not in excluded
    ]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.lang: str | None = None
        self.has_main = False
        self.has_h1 = False
        self.has_skip_link = False
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.has_h1 = True
        if tag == "a" and "skip" in values.get("class", "").split():
            self.has_skip_link = True
        if tag == "img":
            self.images.append(values)
        for attribute in ("href", "src"):
            if attribute in values:
                self.links.append((attribute, values[attribute]))


def local_target(identity_root: Path, page: Path, value: str) -> Path | None:
    split = urlsplit(value)
    if split.scheme or split.netloc or value.startswith(("#", "mailto:", "data:")):
        return None
    path = split.path
    if not path:
        return None
    if path.startswith(PUBLIC_PREFIX):
        relative = PurePosixPath(path.removeprefix(PUBLIC_PREFIX))
    elif path == "/identity":
        relative = PurePosixPath(".")
    elif path.startswith("/"):
        return None
    else:
        page_relative = PurePosixPath(page.relative_to(identity_root).as_posix())
        relative = page_relative.parent / PurePosixPath(path)
    normalized: list[str] = []
    for part in relative.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if normalized:
                normalized.pop()
            continue
        normalized.append(part)
    target = identity_root.joinpath(*normalized)
    if path.endswith("/") or target.is_dir() or not target.suffix:
        target /= "index.html"
    return target


def verify_links(identity_root: Path) -> list[str]:
    errors: list[str] = []
    for page in sorted(identity_root.rglob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if parser.lang != "en":
            errors.append(f"HTML page lacks lang=en: {page.relative_to(identity_root)}")
        if not parser.has_main or not parser.has_h1:
            errors.append(f"HTML page lacks semantic main/h1 structure: {page.relative_to(identity_root)}")
        for attribute, value in parser.links:
            target = local_target(identity_root, page, value)
            if target is not None and not target.is_file():
                errors.append(
                    f"broken local {attribute} in {page.relative_to(identity_root)}: {value}"
                )
    return errors


def verify_checksums(identity_root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    checksums_path = identity_root / str(manifest.get("artifact", {}).get("checksums", ""))
    if not checksums_path.is_file():
        return ["artifact checksum sidecar is missing"]
    expected = {
        record["path"]: record["sha256"]
        for record in manifest.get("artifact", {}).get("inventory", [])
        if record.get("path") != checksums_path.relative_to(identity_root).as_posix()
    }
    actual: dict[str, str] = {}
    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            errors.append(f"malformed checksum line: {line!r}")
            continue
        if match.group(2) in actual:
            errors.append(f"duplicate checksum path: {match.group(2)}")
        actual[match.group(2)] = match.group(1)
    if actual != expected:
        errors.append("SHA256SUMS does not match the emitted artifact inventory")
    return errors


def verify_live_binding(manifest: dict[str, Any]) -> list[str]:
    url = manifest.get("release", {}).get("brandKitEvidence")
    try:
        with urlopen(str(url), timeout=30) as response:  # noqa: S310 - accepted canonical HTTPS URL
            site = json.load(response)
    except Exception as error:  # network failure is evidence failure at this opt-in gate
        return [f"unable to read canonical Brand Kit evidence: {error}"]
    release = manifest["release"]
    brand_release = site.get("release", {}) if isinstance(site, dict) else {}
    if brand_release.get("tag") != release.get("tag") or brand_release.get("commit") != release.get("commit"):
        return ["canonical Brand Kit release binding does not match the composite"]
    return []


def verify_visual_baselines(repository_root: Path) -> list[str]:
    baseline_path = repository_root / "experience/visual-baselines.json"
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"unable to read visual baselines: {error}"]
    if baseline.get("schema") != "identity.experience-visual-baselines/v1":
        return ["visual baseline schema identity drifted"]
    errors: list[str] = []
    records = baseline.get("sourceDigests")
    if not isinstance(records, dict) or not records:
        return ["visual baselines do not pin reviewed sources"]
    for relative, expected in sorted(records.items()):
        path = repository_root / relative
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"reviewed visual source changed without baseline approval: {relative}")
    evidence = baseline.get("browserEvidence")
    expected_ids = {
        "landing-desktop",
        "landing-mobile",
        "docs-desktop",
        "architecture-desktop",
        "legal-mobile",
    }
    actual_ids = {record.get("id") for record in evidence} if isinstance(evidence, list) else set()
    if actual_ids != expected_ids:
        errors.append("visual baselines must require desktop, mobile, and docs browser evidence")
    return errors


def verify_artifact(
    artifact_root: Path,
    *,
    repository_root: Path = Path("."),
    expected_release_tag: str | None = None,
    expected_release_commit: str | None = None,
    verify_live_brand_kit: bool = False,
) -> list[str]:
    errors: list[str] = []
    identity_root = artifact_root.resolve() / "identity"
    publication_path = identity_root / "publication.json"
    try:
        manifest = json.loads(publication_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"unable to read publication.json: {error}"]
    if not isinstance(manifest, dict) or manifest.get("schema") != PUBLICATION_SCHEMA:
        return ["publication.json has an unexpected schema identity"]
    if manifest.get("canonicalUrl") != "https://egohygiene.io/identity/":
        errors.append("publication canonical URL drifted")
    release = manifest.get("release", {})
    if STABLE_TAG.fullmatch(str(release.get("tag", ""))) is None:
        errors.append("publication release tag is not a stable semantic version")
    if COMMIT.fullmatch(str(release.get("commit", ""))) is None:
        errors.append("publication release commit is not a full commit SHA")
    if expected_release_tag is not None and release.get("tag") != expected_release_tag:
        errors.append("publication release tag differs from the expected release")
    if expected_release_commit is not None and release.get("commit") != expected_release_commit:
        errors.append("publication release commit differs from the expected release")

    required_routes = {
        "/identity/": identity_root / "index.html",
        "/identity/docs/": identity_root / "docs/index.html",
        "/identity/architecture/": identity_root / "architecture/index.html",
        "/identity/legal/": identity_root / "legal/index.html",
        "/identity/brand-kit/": identity_root / "brand-kit/index.html",
        "/identity/publication.json": publication_path,
    }
    declared_routes = {record.get("path") for record in manifest.get("routes", [])}
    for route, path in required_routes.items():
        if route not in declared_routes or not path.is_file():
            errors.append(f"required route is missing: {route}")
    required_handoff_routes = {
        "/identity",
        "/brand/",
        "/design/",
        "/brand-kit/",
    }
    if not required_handoff_routes <= declared_routes:
        errors.append("route-owner compatibility redirects are missing from the handoff")

    expected_inventory = inventory(identity_root, {"publication.json"})
    declared_inventory = manifest.get("artifact", {}).get("inventory")
    if declared_inventory != expected_inventory:
        errors.append("publication inventory does not match emitted files")
    digest = hashlib.sha256(canonical_bytes(expected_inventory)).hexdigest()
    if manifest.get("artifact", {}).get("digest") != digest:
        errors.append("publication artifact digest does not match its inventory")
    errors.extend(verify_checksums(identity_root, manifest))
    errors.extend(verify_links(identity_root))

    suite_manifest_path = identity_root / "site-suite.manifest.json"
    try:
        suite_manifest = json.loads(suite_manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"unable to read the Holon site-suite manifest: {error}")
        suite_manifest = {}
    if suite_manifest.get("schema") != "holon.site-suite-artifact/v1" or set(
        suite_manifest.get("routes", {})
    ) != {"landing", "documentation", "architecture", "legal"}:
        errors.append("Holon site-suite evidence is missing or incomplete")

    framework_ids = {record.get("id") for record in manifest.get("frameworks", [])}
    if framework_ids != {"launchkit", "zensical", "route-composer"}:
        errors.append("publication does not bind all accepted Holon profiles")
    handoff = manifest.get("handoff", {})
    if handoff.get("candidate") is not True or handoff.get("installationAuthorized") is not False:
        errors.append("candidate handoff must not claim route-installation authority")

    landing_path = identity_root / "index.html"
    docs_path = identity_root / "docs/index.html"
    landing = landing_path.read_text(encoding="utf-8") if landing_path.is_file() else ""
    docs = docs_path.read_text(encoding="utf-8") if docs_path.is_file() else ""
    if "data-launchkit-static=\"true\"" not in landing or "Skip to content" not in landing:
        errors.append("landing page is not the pre-rendered, keyboard-navigable LaunchKit output")
    mascot = manifest.get("mascot", {})
    if f'alt="{str(mascot.get("altText", "")).replace("'", "&#x27;")}"' not in landing:
        errors.append("landing page does not use the governed Kern alternative text")
    if str(release.get("tag")) not in landing or str(release.get("commit", ""))[:12] not in landing:
        errors.append("landing page does not visibly expose its release binding")
    if "Holon docs-zensical@1.0.0" not in docs or "zensical-0.0.57" not in docs:
        errors.append("documentation output does not expose the accepted Holon and Zensical versions")
    if "fonts.googleapis.com" in docs or "fonts.gstatic.com" in docs:
        errors.append("documentation output depends on external runtime fonts")
    stylesheet_text = "\n".join(path.read_text(encoding="utf-8") for path in identity_root.rglob("*.css"))
    for media in ("prefers-color-scheme", "prefers-contrast", "prefers-reduced-motion"):
        if media not in stylesheet_text:
            errors.append(f"composite styles lack {media} behavior")
    errors.extend(verify_visual_baselines(repository_root.resolve()))
    if verify_live_brand_kit:
        errors.extend(verify_live_binding(manifest))
    return sorted(set(errors))


def main() -> int:
    arguments = parse_arguments()
    errors = verify_artifact(
        arguments.artifact_root,
        repository_root=arguments.repository_root,
        expected_release_tag=arguments.expected_release_tag,
        expected_release_commit=arguments.expected_release_commit,
        verify_live_brand_kit=arguments.verify_live_brand_kit,
    )
    if errors:
        print("identity experience verification failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("identity experience verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
