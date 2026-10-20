#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Build and qualify Identity's pinned default and one non-root custom base."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid


REPOSITORY = Path(__file__).resolve().parents[1]
PLATFORM = "linux/amd64"
HOST_MARKER = "IDENTITY_DEV_QUALIFICATION_RECEIPT="
CONTAINER_MARKER = "IDENTITY_DEV_CONTAINER_RECEIPT="
REGISTRY_RECEIPT = "docs/evidence/identity-development-base-registry-2026-10-20.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_base(dockerfile: Path) -> str:
    matches = re.findall(r"^ARG BASE_IMAGE=(\S+)\s*$", dockerfile.read_text(), re.MULTILINE)
    if len(matches) != 1 or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*@sha256:[0-9a-f]{64}", matches[0]):
        raise ValueError("dev/Dockerfile must declare exactly one immutable BASE_IMAGE digest")
    return matches[0]


def receipt_destination(destination: Path, repository: Path = REPOSITORY) -> Path:
    resolved = destination.resolve()
    source = repository.resolve()
    if resolved == source or source in resolved.parents:
        raise ValueError("--receipt must resolve outside the repository; use a temporary evidence path")
    if resolved.is_dir():
        raise ValueError("--receipt must name a JSON file, not a directory")
    return resolved


def image_identity(image: dict[str, object]) -> dict[str, object]:
    config = image["Config"]
    return {
        "id": image["Id"],
        "repo_digests": image.get("RepoDigests", []),
        "os": image["Os"], "architecture": image["Architecture"],
        "user": config.get("User", ""),
        "entrypoint": config.get("Entrypoint"), "cmd": config.get("Cmd"),
    }


def verify_inheritance(base: dict[str, object], addon: dict[str, object]) -> None:
    for label, image in (("base", base), ("add-on", addon)):
        if (image["os"], image["architecture"]) != ("linux", "amd64"):
            raise RuntimeError(f"The {label} does not match the qualified linux/amd64 platform")
    for name in ("user", "entrypoint", "cmd"):
        if addon[name] != base[name]:
            raise RuntimeError(f"The add-on changed the base image's {name}")


def verify_registry_binding(reference: str, identity: dict[str, object], registry: dict[str, object]) -> None:
    if registry["default_reference"] != reference:
        raise RuntimeError("The registry observation and Dockerfile default differ; refresh both together")
    if registry["qualified_platform_candidate"] != PLATFORM:
        raise RuntimeError("The registry observation selects another platform")
    config = registry["image_config"]
    if identity["id"] != config["digest"]:
        raise RuntimeError("The pulled image config differs from the recorded platform config digest")
    for field in ("os", "architecture", "user", "entrypoint", "cmd"):
        if identity[field] != config[field]:
            raise RuntimeError(f"The pulled image {field} differs from the registry observation")


def container_receipt(output: str) -> dict[str, object]:
    records = [line[len(CONTAINER_MARKER):] for line in output.splitlines() if line.startswith(CONTAINER_MARKER)]
    if len(records) != 1:
        raise RuntimeError("Container smoke must emit exactly one structured qualification receipt")
    receipt = json.loads(records[0])
    if receipt.get("status") != "passed" or receipt.get("platform") != PLATFORM:
        raise RuntimeError("Container smoke did not qualify linux/amd64 successfully")
    return receipt


def source_evidence() -> dict[str, object]:
    critical = (
        "dev/Dockerfile", "dev/qualification/Dockerfile", "dev/qualification/smoke.py",
        "scripts/qualify_dev_image.py", "scripts/dev-env.sh", ".dockerignore",
        ".github/workflows/development-image.yml", "Cargo.toml", "Cargo.lock",
        "rust-toolchain.toml", "renderer/package.json", "renderer/pnpm-lock.yaml",
        REGISTRY_RECEIPT,
    )
    files = subprocess.check_output(["git", "ls-files", "--cached", "-z"], cwd=REPOSITORY).decode().split("\0")
    selected = sorted({path for path in files if path and (
        path in critical or path.startswith("tests/fixtures/")
        or (not path.startswith("docs/") and not path.endswith(".md"))
    )})
    inventory = {path: sha256((REPOSITORY / path).read_bytes()) for path in selected}
    payload = b"".join(path.encode() + b"\0" + digest.encode() + b"\n" for path, digest in inventory.items())
    return {
        "git_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip(),
        "git_worktree_clean": not bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=REPOSITORY)),
        "critical_files_sha256": {path: sha256((REPOSITORY / path).read_bytes()) for path in critical},
        "build_source_inventory": {
            "files": len(inventory), "sha256": sha256(payload),
            "encoding": "sorted UTF-8 relative path, NUL, lowercase SHA-256, newline",
            "scope": "Critical files; all tracked non-Markdown files outside docs; all tracked fixture files including canonical Markdown. Includes assets/publication/profiles/defaults/packages where present. Documentation-only changes outside fixtures and the critical registry receipt are excluded.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True, help="Destination for public qualification JSON")
    args = parser.parse_args()
    try:
        args.receipt = receipt_destination(args.receipt)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    commands: list[dict[str, object]] = []
    images: list[dict[str, object]] = []
    receipt: dict[str, object] = {
        "kind": "dated development-image qualification receipt",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "platform": PLATFORM, "status": "failed", "commands": commands,
        "images": images,
        "limits": [
            "Only the pinned default and recorded derived non-root base are qualified on linux/amd64.",
            "No browser/font/screenshot environment or all-entrypoint CI matrix is qualified.",
            "No private proxy environment, credentials or certificate bytes are recorded.",
            "No release, registry push, deployment or creative approval occurs.",
        ],
    }
    tags = []

    def run(arguments: list[str], *, capture: bool = False) -> str:
        print("Running: " + " ".join(arguments), flush=True)
        result = subprocess.run(arguments, cwd=REPOSITORY, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if not capture or result.returncode:
            print(result.stdout, end="", flush=True)
        commands.append({"command": arguments, "exit_code": result.returncode, "output_sha256": sha256(result.stdout.encode())})
        if result.returncode:
            raise RuntimeError(f"Command failed with exit code {result.returncode}: {arguments[0]}")
        return result.stdout

    def inspect(reference: str) -> dict[str, object]:
        objects = json.loads(run(["docker", "image", "inspect", reference], capture=True))
        if len(objects) != 1:
            raise RuntimeError("Docker image inspection returned an unexpected object count")
        return image_identity(objects[0])

    try:
        base = default_base(REPOSITORY / "dev/Dockerfile")
        registry = json.loads((REPOSITORY / REGISTRY_RECEIPT).read_text())
        if registry["default_reference"] != base:
            raise RuntimeError("The registry observation and Dockerfile default differ; refresh both together")
        receipt["default_base"] = base
        receipt["registry_observation"] = {
            "path": REGISTRY_RECEIPT, "index_digest": registry["index_digest"],
            "platform_manifest_digest": registry["platform_manifest"]["digest"],
            "config_digest": registry["image_config"]["digest"],
        }
        receipt["source"] = source_evidence()
        server = json.loads(run(["docker", "version", "--format", "{{json .Server}}"], capture=True))
        receipt["docker_server"] = {key: server.get(key) for key in ("Version", "Os", "Arch", "KernelVersion")}
        if (server.get("Os"), server.get("Arch")) != ("linux", "amd64"):
            raise RuntimeError("The qualification requires a native Linux amd64 Docker engine")
        run(["docker", "pull", "--platform", PLATFORM, base])
        pinned_identity = inspect(base)
        verify_registry_binding(base, pinned_identity, registry)
        if not any(value.rsplit("@", 1)[-1] == base.rsplit("@", 1)[-1] for value in pinned_identity["repo_digests"]):
            raise RuntimeError("The pulled base does not retain its expected immutable repository digest")
        receipt["pinned_base_identity"] = pinned_identity
        nonce = uuid.uuid4().hex[:12]
        default_tag = f"identity-qualification-default:{nonce}"
        custom_base_tag = f"identity-qualification-custom-base:{nonce}"
        custom_tag = f"identity-qualification-custom:{nonce}"
        tags.extend((custom_tag, custom_base_tag, default_tag))
        run(["docker", "build", "--pull", "--platform", PLATFORM, "--file", "dev/Dockerfile", "--tag", default_tag, "."])
        default_identity = inspect(default_tag)
        verify_inheritance(pinned_identity, default_identity)
        default_output = run([
            "docker", "run", "--rm", "--platform", PLATFORM, default_tag,
            "bash", "/opt/identity/scripts/dev-env.sh", "exec", "python3", "dev/qualification/smoke.py",
            "--expected-uid", "0", "--expected-gid", "0",
        ])
        default_smoke = container_receipt(default_output)
        images.append({"kind": "default", "base": pinned_identity, "addon": default_identity, "metadata_preserved": True, "smoke": default_smoke})
        run([
            "docker", "build", "--pull", "--platform", PLATFORM, "--file", "dev/qualification/Dockerfile",
            "--build-arg", f"BASE_IMAGE={base}", "--tag", custom_base_tag, ".",
        ])
        custom_base_identity = inspect(custom_base_tag)
        if custom_base_identity["user"] != "1000:1000":
            raise RuntimeError("The custom base did not declare the intended non-root development user")
        run([
            "docker", "build", "--platform", PLATFORM, "--file", "dev/Dockerfile",
            "--build-arg", f"BASE_IMAGE={custom_base_tag}",
            "--build-arg", "IDENTITY_DEV_UID=1000", "--build-arg", "IDENTITY_DEV_GID=1000",
            "--tag", custom_tag, ".",
        ])
        custom_identity = inspect(custom_tag)
        verify_inheritance(custom_base_identity, custom_identity)
        custom_output = run([
            "docker", "run", "--rm", "--platform", PLATFORM, custom_tag,
            "bash", "/opt/identity/scripts/dev-env.sh", "exec", "python3", "dev/qualification/smoke.py",
            "--expected-uid", "1000", "--expected-gid", "1000",
        ])
        custom_smoke = container_receipt(custom_output)
        images.append({"kind": "custom-non-root", "base": custom_base_identity, "addon": custom_identity, "metadata_preserved": True, "smoke": custom_smoke})
        if default_smoke["complete_output_inventory"] != custom_smoke["complete_output_inventory"]:
            raise RuntimeError("Default and custom-base CLI outputs differ")
        receipt["default_custom_output_equal"] = True
        receipt["status"] = "passed"
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as error:
        receipt["failure"] = f"{type(error).__name__}: {error}"
        print(receipt["failure"], file=sys.stderr, flush=True)
    finally:
        # Delete only images created by this invocation; never prune shared caches.
        for tag in tags:
            try:
                result = subprocess.run(["docker", "image", "rm", tag], cwd=REPOSITORY, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
                if result.returncode:
                    print(f"Cleanup retained {tag}; image removal exit {result.returncode}", flush=True)
            except OSError:
                print(f"Cleanup retained {tag}; Docker is unavailable", flush=True)
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        print(HOST_MARKER + json.dumps(receipt, sort_keys=True, separators=(",", ":")), flush=True)
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
