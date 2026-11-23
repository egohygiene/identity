#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Prepare digest/tree-verified public action mirrors for an explicit local act run.

This never executes actions, rewrites a workflow or claims hosted runner proof.
Network acquisition requires --download; --archive-directory is offline-only.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
import urllib.request


REPOSITORY = Path(__file__).resolve().parents[1]
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_EXTRACTED_BYTES = 128 * 1024 * 1024
MAX_TAR_BYTES = MAX_EXTRACTED_BYTES + 32 * 1024 * 1024
MAX_MEMBERS = 20000
PIN = re.compile(r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:/([A-Za-z0-9_./-]+))?@([0-9a-f]{40})")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_json_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Action lock contains a duplicate JSON key")
        result[key] = value
    return result


def git_object(kind: str, data: bytes) -> bytes:
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).digest()


def tree_digest(files: dict[str, tuple[int, bytes]]) -> str:
    tree: dict = {}
    for path, (mode, data) in files.items():
        parts = path.split("/")
        directory = tree
        for part in parts[:-1]:
            child = directory.setdefault(part, {})
            if not isinstance(child, dict):
                raise ValueError("Action archive contains a file/directory collision")
            directory = child
        if parts[-1] in directory:
            raise ValueError("Action archive contains a file/directory collision")
        directory[parts[-1]] = (mode, git_object("blob", data))

    def digest(directory: dict) -> bytes:
        entries = []
        for name in sorted(directory, key=lambda key: key.encode() + (b"/" if isinstance(directory[key], dict) else b"")):
            value = directory[name]
            mode, oid = (0o40000, digest(value)) if isinstance(value, dict) else value
            entries.append(f"{mode:o} ".encode() + name.encode() + b"\0" + oid)
        return git_object("tree", b"".join(entries))

    return digest(tree).hex()


def workflow_actions(data: bytes) -> set[tuple[str, str]]:
    """Read only literal scalar action uses; refuse unsupported remote selectors."""
    actions = set()
    for line in data.decode().splitlines():
        match = re.match(r"^\s*(?:-\s*)?uses:\s*(.*?)\s*$", line)
        if not match:
            continue
        value = re.split(r"\s+#", match[1], maxsplit=1)[0].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if value.startswith("./"):
            if ".." in PurePosixPath(value).parts:
                raise ValueError("Local action selector escapes its repository")
            continue
        pinned = PIN.fullmatch(value)
        if pinned is None or any(part in {".", ".."} for part in pinned.group(1).split("/")):
            raise ValueError("Every remote action must use a literal full GitHub commit pin")
        subpath = pinned.group(2)
        if subpath:
            raise ValueError("This bounded preparer supports root GitHub actions only")
        actions.add((pinned.group(1), pinned.group(3)))
    if not actions or len(actions) > 64:
        raise ValueError("The selected workflow must declare between one and 64 pinned actions")
    return actions


def source_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative or "\0" in relative:
        raise ValueError("Lock source paths must be normalized repository-relative paths")
    path = PurePosixPath(relative)
    if path.is_absolute() or path.as_posix() != relative or not path.parts or any(part in {".", ".."} for part in path.parts):
        raise ValueError("Lock source paths must be normalized repository-relative paths")
    result = root.joinpath(*path.parts)
    if root.resolve() not in result.resolve().parents or not result.is_file():
        raise ValueError("Lock source path is missing or outside the repository")
    return result


def validate_lock(lock: dict, root: Path) -> tuple[bytes, list[dict]]:
    if not isinstance(lock, dict) or lock.get("kind") != "identity.local-action-mirror-lock/v1":
        raise ValueError("Unsupported local action mirror lock")
    workflow = source_path(root, lock.get("workflow", "")).read_bytes()
    if sha256(workflow) != lock.get("workflowSha256"):
        raise ValueError("Workflow bytes differ from the reviewed local action lock")
    selected = workflow_actions(workflow)
    actions = lock.get("actions")
    if not isinstance(actions, list) or len(actions) != len(selected):
        raise ValueError("Lock must bind every selected remote action exactly once")
    observed = set()
    keys = {"repository", "revision", "gitTreeSha1", "archiveUrl", "archiveSha256", "archiveBytes"}
    for action in actions:
        if not isinstance(action, dict) or set(action) != keys:
            raise ValueError("Each action lock requires exact archive and Git tree identities")
        repo, revision = action["repository"], action["revision"]
        if not isinstance(repo, str) or not isinstance(revision, str) or PIN.fullmatch(repo + "@" + revision) is None:
            raise ValueError("Invalid locked action selector")
        pair = (repo, revision)
        if pair in observed:
            raise ValueError("Duplicate locked action selector")
        observed.add(pair)
        if action["archiveUrl"] != f"https://codeload.github.com/{repo}/tar.gz/{revision}":
            raise ValueError("Action acquisition must use its exact public codeload URL")
        if not re.fullmatch(r"[0-9a-f]{40}", str(action["gitTreeSha1"])) or not re.fullmatch(r"[0-9a-f]{64}", str(action["archiveSha256"])):
            raise ValueError("Action archive and Git tree digests are required")
        if type(action["archiveBytes"]) is not int or not 0 < action["archiveBytes"] <= MAX_ARCHIVE_BYTES:
            raise ValueError("Locked archive size exceeds the bounded acquisition limit")
    if observed != selected:
        raise ValueError("Locked actions differ from the workflow's exact selected pins")
    return workflow, actions


def archive_files(data: bytes, action: dict) -> dict[str, tuple[int, bytes]]:
    if len(data) != action["archiveBytes"] or sha256(data) != action["archiveSha256"]:
        raise ValueError("Action archive size or SHA-256 differs from its lock")
    prefix = action["repository"].split("/")[1] + "-" + action["revision"]
    files: dict[str, tuple[int, bytes]] = {}
    seen = set()
    total = 0
    # Bound decompression before tarfile can parse large extended headers.
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as compressed:
        decoded = compressed.read(MAX_TAR_BYTES + 1)
    if len(decoded) > MAX_TAR_BYTES:
        raise ValueError("Action archive exceeds its decompressed tar budget")
    with tarfile.open(fileobj=io.BytesIO(decoded), mode="r:") as archive:
        for count, member in enumerate(archive, start=1):
            if count > MAX_MEMBERS:
                raise ValueError("Action archive exceeds its member budget")
            name = member.name.rstrip("/")
            parts = name.split("/")
            if not name or "\\" in name or "\0" in name or parts[0] != prefix or any(part in {"", ".", ".."} for part in parts):
                raise ValueError("Action archive contains an unsafe or unexpected path")
            name.encode("utf-8", errors="strict")
            if name in seen:
                raise ValueError("Action archive contains duplicate paths")
            seen.add(name)
            if member.isdir():
                continue
            if not member.isfile() or len(parts) < 2:
                raise ValueError("Action archive links and special files are unsupported")
            total += member.size
            if member.size < 0 or total > MAX_EXTRACTED_BYTES:
                raise ValueError("Action archive exceeds its extracted byte budget")
            handle = archive.extractfile(member)
            if handle is None:
                raise ValueError("Action archive file is unavailable")
            body = handle.read(member.size + 1)
            if len(body) != member.size:
                raise ValueError("Action archive member size is inconsistent")
            files["/".join(parts[1:])] = (0o100755 if member.mode & 0o111 else 0o100644, body)
    if tree_digest(files) != action["gitTreeSha1"]:
        raise ValueError("Action archive file bytes/modes differ from the selected Git tree")
    if not any(name in files for name in ("action.yml", "action.yaml")):
        raise ValueError("Action mirror lacks its root action definition")
    return files


def acquire(action: dict, archive_directory: Path | None) -> bytes:
    if archive_directory is not None:
        path = archive_directory / (action["repository"].replace("/", "--") + "--" + action["revision"] + ".tar.gz")
        if path.is_symlink() or not path.is_file() or path.stat().st_size != action["archiveBytes"]:
            raise ValueError("Offline action archive is missing, linked or has the wrong size")
        return path.read_bytes()
    request = urllib.request.Request(action["archiveUrl"], headers={"User-Agent": "Identity-local-action-qualification"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(action["archiveBytes"] + 1)


def prepare(root: Path, lock_path: Path, destination: Path, archive_directory: Path | None) -> dict:
    root = root.resolve()
    lock_data = lock_path.read_bytes()
    lock = json.loads(lock_data, object_pairs_hook=unique_json_object)
    workflow, actions = validate_lock(lock, root)
    destination = destination.resolve()
    if destination == root or root in destination.parents or destination.exists():
        raise ValueError("Action mirror output must be a new directory outside the repository")
    destination.mkdir(mode=0o700, parents=True)
    mirrors = []
    for action in actions:
        data = acquire(action, archive_directory)
        files = archive_files(data, action)
        relative = Path("actions") / (action["repository"].replace("/", "--") + "--" + action["revision"])
        directory = destination / relative
        for name, (mode, body) in files.items():
            path = directory / name
            path.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
            path.write_bytes(body)
            path.chmod(mode & 0o777)
        mirrors.append({**action, "directory": relative.as_posix(), "files": len(files),
                        "extractedBytes": sum(len(body) for _, body in files.values()), "verifiedGitTree": tree_digest(files)})
    receipt = {"kind": "identity.local-action-mirror-preparation/v1", "workflow": lock["workflow"],
               "workflowSha256": sha256(workflow), "lockSha256": sha256(lock_data),
               "preparerSha256": sha256(Path(__file__).read_bytes()), "mirrors": mirrors,
               "scope": "Verified local action source substitution only; no action execution, hosted hardening or workflow qualification."}
    (destination / "action-mirrors.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=REPOSITORY / "dev/local-actions/reference-renderer.lock.json")
    parser.add_argument("--output-directory", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--archive-directory", type=Path, help="Read only already acquired archives; never download")
    mode.add_argument("--download", action="store_true", help="Explicitly acquire the lock's public HTTPS archives")
    args = parser.parse_args()
    receipt = prepare(REPOSITORY, args.lock, args.output_directory, args.archive_directory)
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, tarfile.TarError) as error:
        print(f"Local action preparation failed: {type(error).__name__}: {error}")
        raise SystemExit(1) from error
