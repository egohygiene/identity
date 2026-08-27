#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Fail when a Markdown link targets a missing repository file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


MARKDOWN_LINK = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
EXTERNAL_SCHEMES = ("http:", "https:", "mailto:", "tel:")
IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "target",
    "test-results",
    "playwright-report",
    "tests",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Identity repository root containing Markdown documentation.",
    )
    return parser.parse_args()


def link_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if destination.startswith("<") and destination.endswith(">"):
        destination = destination[1:-1]
    else:
        destination = destination.split(maxsplit=1)[0]
    return destination.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]


def verify_markdown_file(document: Path) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(document.read_text(encoding="utf-8").splitlines(), start=1):
        for match in MARKDOWN_LINK.finditer(line):
            destination = link_destination(match.group(1))
            if not destination or destination.startswith(EXTERNAL_SCHEMES):
                continue
            if destination.startswith("/"):
                errors.append(
                    f"{document}:{line_number}: absolute repository link is not portable: {destination}"
                )
                continue
            target = (document.parent / unquote(destination)).resolve()
            if not target.exists():
                errors.append(f"{document}:{line_number}: missing link target: {destination}")
    return errors


def verify_repository(repository_root: Path) -> list[str]:
    documents = sorted(
        document
        for document in repository_root.rglob("*.md")
        if not IGNORED_DIRECTORIES.intersection(document.relative_to(repository_root).parts)
    )
    return [error for document in documents for error in verify_markdown_file(document)]


def main() -> int:
    arguments = parse_arguments()
    errors = verify_repository(arguments.repository_root.resolve())
    if errors:
        print("documentation link check failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("documentation link check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
