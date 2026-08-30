#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Render offline README banner and evidence-badge presentation packages."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
from pathlib import PurePosixPath
import struct
import sys
from typing import Any, Sequence
from urllib.parse import urlsplit
import zlib

import validate_identity as validator


SOURCE_SCHEMA = "identity.repository-presentation-source/v1"
PACKAGE_SCHEMA = "identity.repository-presentation-package/v1"
MANIFEST_SCHEMA = "identity.repository-presentation-package-manifest/v1"
HYGIENE_PROFILE_SCHEMA = "egohygiene.repository-presentation-profile/v1"
HYGIENE_EVIDENCE_SCHEMA = "egohygiene.repository-presentation-evidence/v1"
PROJECTION_VERSION = "1.0.0"
THEMES = {
    "light": {"background": "#f8f5ff", "panel": "#ffffff", "ink": "#171827", "accent": "#6b33b8"},
    "dark": {"background": "#171827", "panel": "#24243a", "ink": "#fff8eb", "accent": "#a78bfa"},
    "high-contrast": {"background": "#000000", "panel": "#000000", "ink": "#ffffff", "accent": "#ffde59"},
}
BANNER_WIDTHS = (640, 1000, 1600)
STATE_COLORS = {
    "unknown": "#667085",
    "evaluating": "#6941c6",
    "advisory": "#b54708",
    "passing": "#067647",
    "failing": "#b42318",
    "partial": "#b54708",
    "stale": "#475467",
    "exempt": "#344054",
    "not_applicable": "#475467",
    "blocked": "#b42318",
}
MEDIA_TYPES = {".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml"}
FONT = {
    "A": "0111010001111111000110001", "B": "1111010001111101000111110",
    "C": "0111110000100001000001111", "D": "1111010001100011000111110",
    "E": "1111110000111101000011111", "F": "1111110000111101000010000",
    "G": "0111110000101111000101111", "H": "1000110001111111000110001",
    "I": "1111100100001000010011111", "J": "0011100010000101001001100",
    "K": "1000110010111001001010001", "L": "1000010000100001000011111",
    "M": "1000111011101011000110001", "N": "1000111001101011001110001",
    "O": "0111010001100011000101110", "P": "1111010001111101000010000",
    "Q": "0111010001100011010101111", "R": "1111010001111101001010001",
    "S": "0111110000011100000111110", "T": "1111100100001000010000100",
    "U": "1000110001100011000101110", "V": "1000110001100010101000100",
    "W": "1000110001101011101110001", "X": "1000101010001000101010001",
    "Y": "1000101010001000010000100", "Z": "1111100010001000100011111",
    "0": "0111010011101011100101110", "1": "0010001100001000010001110",
    "2": "0111010001000100010011111", "3": "1111000001011100000111110",
    "4": "1000110001111110000100001", "5": "1111110000111100000111110",
    "6": "0111010000111101000101110", "7": "1111100010001000100001000",
    "8": "0111010001011101000101110", "9": "0111010001011110000101110",
    "-": "0000000000111110000000000", ".": "0000000000000000011000110",
    ":": "0000000100000000010000000", "/": "0000100010001000100010000",
    "_": "0000000000000000000011111", " ": "0000000000000000000000000",
}


class ProjectionError(ValueError):
    """Raised when reviewed inputs cannot produce an honest package."""


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"document must be an object: {path}")
    return value


def render_json(value: object) -> bytes:
    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n".encode("utf-8")


def normalized_digest(path: Path) -> str:
    value = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def require_relative_path(value: str) -> None:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts or "\\" in value:
        raise ProjectionError(f"path is not a safe repository-relative path: {value!r}")


def approved_decision(approvals: dict[str, Any], identifier: str, subject: str) -> None:
    decisions = {item.get("id"): item for item in approvals.get("decisions", []) if isinstance(item, dict)}
    decision = decisions.get(identifier)
    if not isinstance(decision, dict) or decision.get("status") != "approved" or decision.get("subject") != subject:
        raise ProjectionError(f"approval {identifier!r} does not authorize {subject!r}")


def resolve_public_asset(repository_root: Path, documents: dict[str, Any], asset_id: str) -> tuple[Path, dict[str, str]]:
    usage = load_json(repository_root / documents["guidance"]["usage"])
    provenance = load_json(repository_root / documents["provenance"])
    usage_asset = next((item for item in usage.get("assets", []) if item.get("id") == asset_id), None)
    record = next((item for item in provenance.get("assets", []) if item.get("id") == asset_id), None)
    if not isinstance(usage_asset, dict) or not isinstance(record, dict):
        raise ProjectionError(f"banner asset does not resolve: {asset_id}")
    governance = usage_asset.get("governance", {})
    if usage_asset.get("status") != "active" or usage_asset.get("availability") != "public" or governance.get("state") != "approved" or governance.get("visibility") != "public":
        raise ProjectionError(f"banner asset is not active, approved, and public: {asset_id}")
    asset_path = repository_root / usage_asset["path"]
    if hashlib.sha256(asset_path.read_bytes()).hexdigest() != record.get("sha256"):
        raise ProjectionError(f"banner asset digest changed: {usage_asset['path']}")
    license_record = record.get("license", {})
    if license_record.get("status") != "approved":
        raise ProjectionError(f"banner asset license is not approved: {asset_id}")
    return asset_path, {"spdx": license_record["spdx"], "attribution": license_record["attribution"]}


def validate_profile(source: dict[str, Any], repository_root: Path) -> tuple[dict[str, Any], Path]:
    lock = source.get("profile")
    if not isinstance(lock, dict):
        raise ProjectionError("repository-presentation source has no profile lock")
    required = {"path", "id", "version", "status", "owner", "repository", "commit", "digest"}
    if set(lock) != required:
        raise ProjectionError("profile lock fields are incomplete or unknown")
    if lock["id"] != HYGIENE_PROFILE_SCHEMA or lock["owner"] != "egohygiene/hygiene":
        raise ProjectionError("profile lock does not identify the Hygiene presentation profile")
    if lock["repository"] != "https://github.com/egohygiene/hygiene":
        raise ProjectionError("profile lock repository is not canonical")
    if (
        not isinstance(lock["commit"], str)
        or len(lock["commit"]) != 40
        or any(character not in "0123456789abcdef" for character in lock["commit"])
    ):
        raise ProjectionError("profile lock commit must be 40 lowercase hexadecimal characters")
    require_relative_path(lock["path"])
    profile_path = repository_root / lock["path"]
    profile = load_json(profile_path)
    digest = lock.get("digest", {})
    if digest.get("algorithm") != "sha256-utf8-lf" or digest.get("value") != normalized_digest(profile_path):
        raise ProjectionError("pinned Hygiene profile digest does not match local bytes")
    for field in ("schema", "version", "status", "owner"):
        if profile.get(field) != lock.get(field if field != "schema" else "id"):
            raise ProjectionError(f"pinned Hygiene profile {field} does not match")
    policy = profile.get("claim_policy", {})
    if policy.get("badge_label") != "Hygienic" or policy.get("unknown_fails_closed") is not True:
        raise ProjectionError("Hygiene claim policy is unsupported")
    if set(profile.get("evidence_states", [])) != set(STATE_COLORS):
        raise ProjectionError("Hygiene evidence-state vocabulary is unsupported")
    return profile, profile_path


def validate_evidence(evidence: dict[str, Any], profile: dict[str, Any], source: dict[str, Any]) -> dict[str, str]:
    if evidence.get("schema") != HYGIENE_EVIDENCE_SCHEMA:
        raise ProjectionError("evidence does not use the supported Hygiene contract")
    evidence_profile = evidence.get("profile", {})
    lock = source["profile"]
    for field in ("id", "version", "status"):
        if evidence_profile.get(field) != lock.get(field):
            raise ProjectionError(f"evidence profile {field} differs from the pinned profile")
    badge = evidence.get("badge")
    repository = evidence.get("repository")
    assessment = evidence.get("assessment")
    if not all(isinstance(value, dict) for value in (badge, repository, assessment)):
        raise ProjectionError("evidence badge, repository, and assessment must be objects")
    state = badge.get("state")
    if state not in STATE_COLORS or assessment.get("state") != state:
        raise ProjectionError("explicit badge and assessment states must match a Hygiene state")
    messages = profile["claim_policy"]["state_messages"]
    if badge.get("label") != "Hygienic" or badge.get("message") != messages[state]:
        raise ProjectionError("badge label or message differs from the pinned Hygiene claim policy")
    if badge.get("profile_version") != lock["version"]:
        raise ProjectionError("badge profile version differs from the pinned profile")
    represented_commit = badge.get("represented_commit")
    if represented_commit != repository.get("represented_commit") or not isinstance(represented_commit, str) or len(represented_commit) != 40 or any(char not in "0123456789abcdef" for char in represented_commit):
        raise ProjectionError("badge must bind the repository's full represented commit")
    evidence_url = badge.get("evidence_url")
    if not isinstance(evidence_url, str) or not evidence_url.strip():
        raise ProjectionError("badge must provide an evidence URL")
    destination = urlsplit(evidence_url)
    if destination.scheme and destination.scheme != "https":
        raise ProjectionError("badge evidence URL must be HTTPS or repository-relative")
    if not destination.scheme:
        require_relative_path(destination.path)
    prohibited = profile["claim_policy"]["prohibited_claim_terms"]
    rendered_claim = f"{badge['label']} {badge['message']}".lower()
    if any(term.lower() in rendered_claim for term in prohibited):
        raise ProjectionError("badge claim contains a prohibited certification term")
    return {"state": state, "label": badge["label"], "message": badge["message"], "representedCommit": represented_commit, "evidenceUrl": evidence_url}


def rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))  # type: ignore[return-value]


def png_bytes(width: int, height: int, pixels: bytearray) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    stride = width * 3
    rows = b"".join(b"\x00" + bytes(pixels[y * stride:(y + 1) * stride]) for y in range(height))
    return signature + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")


def canvas(width: int, height: int, color: str) -> bytearray:
    return bytearray(rgb(color) * (width * height))


def fill_rect(pixels: bytearray, width: int, height: int, x: int, y: int, box_width: int, box_height: int, color: str) -> None:
    red, green, blue = rgb(color)
    for row in range(max(0, y), min(height, y + box_height)):
        for column in range(max(0, x), min(width, x + box_width)):
            index = (row * width + column) * 3
            pixels[index:index + 3] = bytes((red, green, blue))


def fill_diamond(pixels: bytearray, width: int, height: int, center_x: int, center_y: int, radius: int, color: str) -> None:
    red, green, blue = rgb(color)
    for row in range(max(0, center_y - radius), min(height, center_y + radius + 1)):
        span = radius - abs(row - center_y)
        for column in range(max(0, center_x - span), min(width, center_x + span + 1)):
            index = (row * width + column) * 3
            pixels[index:index + 3] = bytes((red, green, blue))


def draw_text(pixels: bytearray, width: int, height: int, x: int, y: int, value: str, color: str, scale: int) -> None:
    cursor = x
    for character in value.upper():
        glyph = FONT.get(character, FONT["-"])
        for row in range(5):
            for column in range(5):
                if glyph[row * 5 + column] == "1":
                    fill_rect(pixels, width, height, cursor + column * scale, y + row * scale, scale, scale, color)
        cursor += 6 * scale


def render_banner_svg(name: str, alt_text: str, asset_path: Path, width: int, theme: str) -> bytes:
    palette = THEMES[theme]
    height = width // 4
    embedded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    image_size = max(72, height * 2 // 5)
    title_size = max(28, height // 7)
    subtitle_size = max(14, height // 16)
    title = html.escape(name)
    alt = html.escape(alt_text)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <title id="title">{alt}</title>
  <desc id="desc">{html.escape(name)} repository identity. Text remains available as a README fallback.</desc>
  <rect width="{width}" height="{height}" rx="{max(18, height // 12)}" fill="{palette['background']}"/>
  <path d="M0 {height * 3 // 4} Q {width // 2} {height // 2} {width} {height // 5} V {height} H0Z" fill="{palette['panel']}"/>
  <image href="data:image/svg+xml;base64,{embedded}" x="{width // 12}" y="{(height - image_size) // 2}" width="{image_size}" height="{image_size}"/>
  <text x="{width // 12 + image_size + width // 24}" y="{height // 2}" dominant-baseline="middle" fill="{palette['ink']}" font-family="ui-sans-serif,system-ui,sans-serif" font-size="{title_size}" font-weight="700">{title}</text>
  <text x="{width // 12 + image_size + width // 24}" y="{height // 2 + title_size}" fill="{palette['accent']}" font-family="ui-sans-serif,system-ui,sans-serif" font-size="{subtitle_size}" letter-spacing="1">EGO HYGIENE REPOSITORY</text>
</svg>
'''
    return svg.encode("utf-8")


def render_banner_png(name: str, width: int, theme: str) -> bytes:
    palette = THEMES[theme]
    height = width // 4
    pixels = canvas(width, height, palette["background"])
    fill_rect(pixels, width, height, 0, height * 3 // 4, width, height // 4, palette["panel"])
    radius = max(28, height // 5)
    fill_diamond(pixels, width, height, width // 10 + radius, height // 2, radius, palette["accent"])
    scale = max(2, width // 320)
    available = max(1, (width - (width // 10 + radius * 2 + width // 20)) // (6 * scale))
    draw_text(pixels, width, height, width // 10 + radius * 2 + width // 20, height // 2 - 3 * scale, name[:available], palette["ink"], scale)
    return png_bytes(width, height, pixels)


def render_badge_svg(label: str, message: str, state: str) -> bytes:
    label_width = max(76, len(label) * 7 + 18)
    message_width = max(100, len(message) * 7 + 18)
    width = label_width + message_width
    color = STATE_COLORS[state]
    title = html.escape(f"{label}: {message}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}" width="{width}" height="24" viewBox="0 0 {width} 24">
  <title>{title}</title>
  <rect width="{label_width}" height="24" rx="5" fill="#24243a"/>
  <rect x="{label_width}" width="{message_width}" height="24" rx="5" fill="{color}"/>
  <path d="M{label_width - 5} 0h10v24h-10z" fill="{color}"/>
  <g fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11" text-anchor="middle">
    <text x="{label_width // 2}" y="16">{html.escape(label)}</text>
    <text x="{label_width + message_width // 2}" y="16">{html.escape(message)}</text>
  </g>
</svg>
'''.encode("utf-8")


def render_badge_png(label: str, message: str, state: str) -> bytes:
    scale = 2
    label_value = label.upper()
    message_value = message.upper()
    label_width = len(label_value) * 6 * scale + 16
    message_width = len(message_value) * 6 * scale + 16
    width = label_width + message_width
    height = 24
    pixels = canvas(width, height, "#24243a")
    fill_rect(pixels, width, height, label_width, 0, message_width, height, STATE_COLORS[state])
    draw_text(pixels, width, height, 8, 7, label_value, "#ffffff", scale)
    draw_text(pixels, width, height, label_width + 8, 7, message_value, "#ffffff", scale)
    return png_bytes(width, height, pixels)


def build_projection(repository_root: Path, evidence_path: Path) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise ProjectionError(f"[{first.code}] {first.path}: {first.message}")
    identity = load_json(repository_root / ".identity/identity.json")
    documents = identity["documents"]
    source_path_value = documents.get("repositoryPresentation")
    if not isinstance(source_path_value, str):
        raise ProjectionError("projection requires documents.repositoryPresentation source")
    source_path = repository_root / source_path_value
    source = load_json(source_path)
    if source.get("schema") != SOURCE_SCHEMA:
        raise ProjectionError(f"source schema must be {SOURCE_SCHEMA}")
    profile, profile_path = validate_profile(source, repository_root)
    evidence = load_json(evidence_path)
    badge_input = validate_evidence(evidence, profile, source)
    approvals = load_json(repository_root / documents["approvals"])
    default = source.get("organizationDefault")
    project_selection = source.get("project")
    if not isinstance(default, dict) or not isinstance(project_selection, dict):
        raise ProjectionError("organizationDefault and project must be objects")
    approved_decision(approvals, default["bannerApproval"], "repository-presentation-banner-default")
    approved_decision(approvals, default["badgeApproval"], "repository-presentation-badge-profile")
    asset_id = default["bannerAssetId"]
    alt_text = default["altText"]
    override = project_selection.get("override")
    inherited = True
    if override is not None:
        if not isinstance(override, dict):
            raise ProjectionError("project override must be an object or null")
        approved_decision(approvals, override["approval"], f"repository-presentation-banner-override:{identity['project']['id']}")
        asset_id = override.get("bannerAssetId", asset_id)
        alt_text = override.get("altText", alt_text)
        inherited = False
    asset_path, asset_license = resolve_public_asset(repository_root, documents, asset_id)
    if default.get("license") != asset_license:
        raise ProjectionError("selected banner license differs from governed asset provenance")
    if not isinstance(alt_text, str) or identity["project"]["displayName"].lower() not in alt_text.lower():
        raise ProjectionError("banner alt text must identify the project by display name")
    visibility = project_selection.get("visibility")
    if visibility not in {"public", "internal", "private"}:
        raise ProjectionError("project visibility is unsupported")
    if evidence.get("repository", {}).get("visibility") != visibility:
        raise ProjectionError("evidence repository visibility differs from reviewed Identity source")

    files: dict[str, bytes] = {}
    banner_variants = []
    for theme in THEMES:
        for width in BANNER_WIDTHS:
            height = width // 4
            variant_id = f"{theme}-{width}"
            svg_path = f"assets/banner-{variant_id}.svg"
            png_path = f"assets/banner-{variant_id}.png"
            files[svg_path] = render_banner_svg(identity["project"]["displayName"], alt_text, asset_path, width, theme)
            files[png_path] = render_banner_png(identity["project"]["displayName"], width, theme)
            banner_variants.append({"id": variant_id, "theme": theme, "width": width, "height": height, "narrow": width == min(BANNER_WIDTHS), "svg": svg_path, "raster": png_path})
    state = badge_input["state"]
    badge_svg_path = f"assets/hygienic-{state}.svg"
    badge_png_path = f"assets/hygienic-{state}.png"
    files[badge_svg_path] = render_badge_svg(badge_input["label"], badge_input["message"], state)
    files[badge_png_path] = render_badge_png(badge_input["label"], badge_input["message"], state)

    model = {
        "schema": PACKAGE_SCHEMA,
        "version": PROJECTION_VERSION,
        "project": {**{field: identity["project"][field] for field in ("id", "displayName", "repository")}, "visibility": visibility},
        "source": {
            "path": source_path_value,
            "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "bannerAsset": {"id": asset_id, "path": asset_path.relative_to(repository_root).as_posix(), "sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(), "inheritedFromOrganization": inherited},
            "approval": {"organizationBanner": default["bannerApproval"], "badgeProfile": default["badgeApproval"], "projectOverride": override.get("approval") if isinstance(override, dict) else None},
        },
        "profile": {"id": source["profile"]["id"], "version": source["profile"]["version"], "status": source["profile"]["status"], "owner": source["profile"]["owner"], "repository": source["profile"]["repository"], "commit": source["profile"]["commit"], "path": source["profile"]["path"], "sha256": normalized_digest(profile_path), "activationClaimed": False},
        "banner": {"altText": alt_text, "fallbackText": default["fallbackText"], "destinationUrl": identity["project"]["repository"], "license": asset_license, "variants": banner_variants},
        "badge": {
            "label": badge_input["label"],
            "message": badge_input["message"],
            "textFallback": f"{badge_input['label']}: {badge_input['message']}",
            "state": state,
            "profileVersion": source["profile"]["version"],
            "representedCommit": badge_input["representedCommit"],
            "evidenceUrl": badge_input["evidenceUrl"],
            "svg": badge_svg_path,
            "raster": badge_png_path,
            "hostedProviderRequired": False,
            "visualProfile": {
                "id": "hygienic-evidence-v1",
                "textColor": "#ffffff",
                "states": [
                    {
                        "state": candidate_state,
                        "message": profile["claim_policy"]["state_messages"][candidate_state],
                        "color": STATE_COLORS[candidate_state],
                        "passing": candidate_state == "passing",
                    }
                    for candidate_state in profile["evidence_states"]
                ],
            },
        },
        "consumerBoundary": {"editsReadme": False, "evaluatesEvidence": False, "networkRequired": False, "generatedRegionsOnly": True},
    }
    files["repository-presentation.json"] = render_json(model)
    evidence_digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "version": PROJECTION_VERSION,
        "projectionSchema": PACKAGE_SCHEMA,
        "projectId": identity["project"]["id"],
        "sourceDigest": model["source"]["sha256"],
        "profile": {"id": source["profile"]["id"], "version": source["profile"]["version"], "status": source["profile"]["status"], "commit": source["profile"]["commit"], "digest": normalized_digest(profile_path)},
        "evidence": {"state": state, "representedCommit": badge_input["representedCommit"], "url": badge_input["evidenceUrl"], "digest": evidence_digest},
        "files": {},
    }
    for path, value in sorted(files.items()):
        suffix = Path(path).suffix
        manifest["files"][path] = {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value), "mediaType": MEDIA_TYPES[suffix]}
    return model, files, manifest


def write_projection(output: Path, files: dict[str, bytes], manifest: dict[str, Any]) -> None:
    if ".identity" in output.resolve().parts:
        raise ProjectionError("generated output cannot be written beneath canonical .identity source")
    complete = dict(files)
    complete["repository-presentation-manifest.json"] = render_json(manifest)
    checksums = "".join(f"{hashlib.sha256(value).hexdigest()}  {path}\n" for path, value in sorted(complete.items()))
    complete["SHA256SUMS"] = checksums.encode("utf-8")
    for relative_path, value in sorted(complete.items()):
        destination = output / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render deterministic offline repository-presentation assets.")
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--evidence", type=Path, required=True, help="Explicit Hygiene evidence-state document; Identity never derives it.")
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        _, files, manifest = build_projection(arguments.repository_root.resolve(), arguments.evidence.resolve())
        write_projection(arguments.output.resolve(), files, manifest)
    except (OSError, json.JSONDecodeError, ProjectionError) as error:
        print(f"repository-presentation projection failed: {error}", file=sys.stderr)
        return 1
    print(f"Rendered repository-presentation package to {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
