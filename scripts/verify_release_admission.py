#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Admit an observed remote annotated release tag before packaging or publication.

This checks remote identity at each invocation; it cannot lock a remote ref or
make the subsequent GitHub operation atomic with that observation.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from verify_release import package_version, renderer_version


OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


def git(root: Path, *arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1", "GIT_TERMINAL_PROMPT": "0"},
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"Git admission read failed: {error}") from error
    if completed.returncode:
        raise RuntimeError(
            f"Git admission command {arguments[0]!r} failed: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def remote_selection(root: Path, remote: str, tag: str) -> dict[str, str]:
    requested = (f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}", "refs/heads/main")
    observed: dict[str, str] = {}
    for line in git(root, "ls-remote", "--", remote, *requested).splitlines():
        parts = line.split("\t")
        if len(parts) != 2 or parts[1] not in requested:
            raise RuntimeError("remote release selection contains an unexpected record")
        object_id, reference = parts
        if OBJECT_ID.fullmatch(object_id) is None or reference in observed:
            raise RuntimeError("remote release selection contains an invalid or duplicate record")
        observed[reference] = object_id
    if set(observed) != set(requested):
        raise RuntimeError("remote must advertise the annotated release tag and main branch")
    return observed


def admit_release(
    root: Path, *, tag: str, expected_commit: str, remote: str,
    expected_tag_object: str | None = None,
) -> dict[str, str]:
    if OBJECT_ID.fullmatch(expected_commit) is None:
        raise RuntimeError("expected commit must be a full lowercase Git object ID")
    if expected_tag_object is not None and OBJECT_ID.fullmatch(expected_tag_object) is None:
        raise RuntimeError("expected tag object must be a full lowercase Git object ID")
    version = package_version(root)
    if renderer_version(root) != version or tag != f"v{version}":
        raise RuntimeError("release tag, Cargo.toml and renderer/package.json versions must match")
    git(root, "check-ref-format", f"refs/tags/{tag}")
    if git(root, "rev-parse", "HEAD") != expected_commit:
        raise RuntimeError("checkout HEAD does not match the expected release commit")
    git(root, "diff", "--quiet", "HEAD", "--")
    if git(root, "rev-parse", "--is-shallow-repository") != "false":
        raise RuntimeError("release admission requires a full checkout for main ancestry")

    selected = remote_selection(root, remote, tag)
    tag_object = selected[f"refs/tags/{tag}"]
    main_commit = selected["refs/heads/main"]
    if expected_tag_object is not None and tag_object != expected_tag_object:
        raise RuntimeError("remote release tag object changed since packaging admission")
    if selected[f"refs/tags/{tag}^{{}}"] != expected_commit:
        raise RuntimeError("remote annotated tag does not select the expected release commit")

    # Fetch the advertised objects, never a mutable local tag or tracking ref.
    git(root, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head", "--",
        remote, tag_object, main_commit)
    if git(root, "cat-file", "-t", tag_object) != "tag":
        raise RuntimeError("release selection must be an annotated tag object")
    header = git(root, "cat-file", "-p", tag_object).split("\n\n", 1)[0].splitlines()
    if header[:3] != [f"object {expected_commit}", "type commit", f"tag {tag}"]:
        raise RuntimeError("annotated tag name and direct commit must match the release selection")
    if git(root, "cat-file", "-t", expected_commit) != "commit":
        raise RuntimeError("release tag must select a commit")
    git(root, "merge-base", "--is-ancestor", expected_commit, main_commit)
    if remote_selection(root, remote, tag) != selected:
        raise RuntimeError("remote release selection changed during admission")
    return {"tag": tag, "tag_object_sha": tag_object, "commit_sha": expected_commit,
            "main_sha": main_commit, "version": version}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--tag", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--expected-tag-object")
    parser.add_argument("--github-output", type=Path)
    arguments = parser.parse_args()
    admitted = admit_release(
        arguments.repository_root.resolve(), tag=arguments.tag,
        expected_commit=arguments.expected_commit, remote=arguments.remote,
        expected_tag_object=arguments.expected_tag_object,
    )
    if arguments.github_output is not None:
        with arguments.github_output.open("a", encoding="utf-8") as output:
            output.write(f"tag_object_sha={admitted['tag_object_sha']}\n")
    print(json.dumps(admitted, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError) as error:
        print(f"release admission failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
