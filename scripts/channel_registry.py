#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Shared read-only projection helpers for the governed channel registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SOURCE_SCHEMA = "identity.channel-registry-source/v1"
PACKAGE_SCHEMA = "identity.channel-registry-package/v1"
PROJECTION_VERSION = "1.0.0"


class ChannelRegistryError(ValueError):
    """Raised when a registry cannot produce a safe public projection."""


def load_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON document."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ChannelRegistryError(f"document must be an object: {path}")
    return value


def source_for_project(
    repository_root: Path,
    project: dict[str, Any],
) -> dict[str, Any] | None:
    """Load the optional repository-local channel registry source."""

    documents = project.get("documents")
    if not isinstance(documents, dict):
        return None
    path_value = documents.get("channelRegistry")
    if path_value is None:
        return None
    if not isinstance(path_value, str):
        raise ChannelRegistryError("documents.channelRegistry must be a local path")
    source = load_json(repository_root / path_value)
    if source.get("schema") != SOURCE_SCHEMA:
        raise ChannelRegistryError(f"channel registry must use {SOURCE_SCHEMA}")
    return source


def governed_channels(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Return approved public registry records in stable order."""

    result = []
    for value in source.get("channels", []):
        if not isinstance(value, dict):
            continue
        governance = value.get("governance")
        if (
            isinstance(governance, dict)
            and governance.get("state") == "approved"
            and governance.get("visibility") == "public"
            and isinstance(governance.get("approval"), str)
        ):
            result.append(value)
    return sorted(result, key=lambda item: str(item["id"]))


def public_channels(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Project only active, badge-approved channels with canonical HTTPS URLs."""

    result = []
    for value in governed_channels(source):
        lifecycle = value.get("lifecycle")
        badge = value.get("badge")
        url = value.get("canonicalUrl")
        if (
            not isinstance(lifecycle, dict)
            or lifecycle.get("state") != "active"
            or not isinstance(badge, dict)
            or badge.get("approved") is not True
            or not isinstance(url, str)
            or not url.startswith("https://")
        ):
            continue
        result.append(
            {
                "id": value["id"],
                "platformId": value["platform"]["id"],
                "platform": value["platform"]["label"],
                "url": url,
                "handle": value["handle"],
                "label": value["accessibility"]["label"],
                "verification": value["verification"]["state"],
                "badge": {
                    "label": badge["label"],
                    "icon": badge["icon"],
                },
            }
        )
    return result


def public_channel_by_platform(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index active public channels by stable platform ID and case-folded label."""

    result: dict[str, dict[str, Any]] = {}
    for value in public_channels(source):
        for key in (value["platformId"], value["platform"].casefold()):
            existing = result.get(key)
            if existing is not None and existing["id"] != value["id"]:
                raise ChannelRegistryError(
                    f"active public channels ambiguously share platform key {key!r}"
                )
            result[key] = value
    return result
