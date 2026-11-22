#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Build and qualify Identity's pinned default and one non-root custom base."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
import uuid


REPOSITORY = Path(__file__).resolve().parents[1]
PLATFORM = "linux/amd64"
HOST_MARKER = "IDENTITY_DEV_QUALIFICATION_RECEIPT="
CONTAINER_MARKER = "IDENTITY_DEV_CONTAINER_RECEIPT="
REGISTRY_RECEIPT = "docs/evidence/identity-development-base-registry-2026-10-20.json"
GIB = 1024 ** 3
PROXY_VARIABLES = ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy")
CONTAINER_PROXY_CA = "/run/identity-development-proxy-ca.pem"
INPUTS_SPEC = importlib.util.spec_from_file_location(
    "identity_development_source_inputs", REPOSITORY / "dev/qualification/source_inputs.py",
)
SOURCE_INPUTS = importlib.util.module_from_spec(INPUTS_SPEC)
INPUTS_SPEC.loader.exec_module(SOURCE_INPUTS)


def selected_proxy_ca(explicit: Path | None, environment: dict[str, str]) -> Path | None:
    """Trust is selected only by the scoped option, with explicit CLI precedence."""
    selected = explicit if explicit is not None else environment.get("IDENTITY_DEVELOPMENT_PROXY_CA")
    if not selected:
        return None
    if re.search(r'[,"\x00-\x1f\x7f]', str(selected)):
        raise ValueError("--proxy-ca must select a regular CA bundle with a Docker-mount-safe path")
    try:
        resolved = Path(selected).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ValueError("--proxy-ca must select an existing readable regular CA bundle") from error
    if not resolved.is_file() or re.search(r'[,"\x00-\x1f\x7f]', str(resolved)):
        raise ValueError("--proxy-ca must select a regular CA bundle with a Docker-mount-safe path")
    return resolved


def network_arguments(proxy_ca: Path | None, environment: dict[str, str]) -> tuple[list[str], list[str], dict[str, object]]:
    """Forward proxy names, never values, using Docker's predefined proxy support."""
    names = [name for name in PROXY_VARIABLES if environment.get(name)]
    build = [part for name in names for part in ("--build-arg", name)]
    runtime = [part for name in names for part in ("--env", name)]
    if proxy_ca is not None:
        build.extend(["--secret", f"id=identity_proxy_ca,src={proxy_ca}"])
        runtime.extend(["--mount", f"type=bind,source={proxy_ca},target={CONTAINER_PROXY_CA},readonly"])
        for name in ("CURL_CA_BUNDLE", "SSL_CERT_FILE", "CARGO_HTTP_CAINFO", "NODE_EXTRA_CA_CERTS"):
            runtime.extend(["--env", f"{name}={CONTAINER_PROXY_CA}"])
    return build, runtime, {
        "proxy_variables": names,
        "ca_secret_selected": proxy_ca is not None,
        "runtime_ca_readonly_bind_selected": proxy_ca is not None,
        "system_trust_modified": False,
    }


def storage_budget(storage: dict[str, object], endpoint: str, minimum_gib: int | None) -> dict[str, object]:
    """Bound known local disk pressure; an estimate never proves enough capacity."""
    driver = storage.get("Driver")
    minimum = minimum_gib if minimum_gib is not None else (24 if driver == "vfs" else 8)
    report: dict[str, object] = {
        "driver": driver, "minimum_free_bytes": minimum * GIB,
        "available_bytes": None,
        "basis": "Conservative local operational reserve, not a sufficient-capacity guarantee.",
    }
    if minimum == 0:
        return {**report, "status": "explicitly-bypassed"}
    directory = storage.get("DockerRootDir")
    if not isinstance(endpoint, str) or not endpoint.startswith("unix://") or not isinstance(directory, str) or not Path(directory).is_absolute():
        return {**report, "status": "unknown", "reason": "Daemon storage is not locally observable; measure it on the daemon host or use --minimum-free-gib 0 with an independently checked budget."}
    try:
        available = shutil.disk_usage(directory).free
    except OSError:
        return {**report, "status": "unknown", "reason": "Daemon storage cannot be inspected locally; measure it on the daemon host or use --minimum-free-gib 0 with an independently checked budget."}
    report["available_bytes"] = available
    return {**report, "status": "sufficient-reserve" if available >= minimum * GIB else "insufficient",
            "reason": "Reserve checked on the locally observable Docker data filesystem; concurrent jobs and VFS copies can require more."}


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
    if not isinstance(receipt, dict) or receipt.get("status") != "passed" or receipt.get("platform") != PLATFORM:
        raise RuntimeError("Container smoke did not qualify linux/amd64 successfully")
    repeat = receipt.get("repeat_setup")
    if not isinstance(repeat, dict) or repeat.get("status") != "passed" or repeat.get("source_inputs_preserved") is not True:
        raise RuntimeError("Container smoke did not qualify actual repeated setup")
    expected_pins = {
        "rustc": tomllib.loads((REPOSITORY / "rust-toolchain.toml").read_text())["toolchain"]["channel"],
        "pnpm": json.loads((REPOSITORY / "renderer/package.json").read_text())["packageManager"].split("@", 1)[1],
    }
    if repeat.get("runtime_pins_preserved") != expected_pins:
        raise RuntimeError("Repeated setup runtime pins differ from the selected source")
    if repeat.get("source_inputs_sha256") != SOURCE_INPUTS.source_inventory(REPOSITORY):
        raise RuntimeError("Repeated setup input inventory differs from the selected source")
    commands = receipt.get("commands")
    if not isinstance(commands, list):
        raise RuntimeError("Container smoke must record its repeated setup command")
    setups = [row for row in commands if isinstance(row, dict) and row.get("command") == ["bash", "scripts/dev-env.sh", "setup"]]
    if (len(setups) != 1 or type(setups[0].get("exit_code")) is not int
            or setups[0].get("exit_code") != 0 or setups[0].get("expected_exit_codes") != [0]):
        raise RuntimeError("Container smoke must record exactly one successful repeated setup command")
    return receipt


def source_evidence() -> dict[str, object]:
    critical = (
        "dev/Dockerfile", "dev/qualification/Dockerfile", "dev/qualification/smoke.py",
        "dev/qualification/source_inputs.py",
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
    parser.add_argument("--minimum-free-gib", type=int, help="Local Docker data free-space reserve (default: 24 GiB for vfs, 8 otherwise); 0 explicitly bypasses for independently budgeted or remote engines")
    parser.add_argument("--proxy-ca", type=Path, help="Optional public CA bundle: ephemeral BuildKit secret and read-only smoke bind; defaults to IDENTITY_DEVELOPMENT_PROXY_CA")
    args = parser.parse_args()
    if args.minimum_free_gib is not None and args.minimum_free_gib < 0:
        parser.error("--minimum-free-gib must be nonnegative")
    try:
        args.receipt = receipt_destination(args.receipt)
        proxy_ca = selected_proxy_ca(args.proxy_ca, os.environ)
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
    build_network, runtime_network, receipt["network"] = network_arguments(proxy_ca, os.environ)

    def public_text(value: str) -> str:
        return value.replace(str(proxy_ca), "<proxy-ca>") if proxy_ca else value

    def run(arguments: list[str], *, capture: bool = False) -> str:
        public_arguments = [public_text(item) for item in arguments]
        print("Running: " + " ".join(public_arguments), flush=True)
        result = subprocess.run(arguments, cwd=REPOSITORY, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if not capture or result.returncode:
            print(public_text(result.stdout), end="", flush=True)
        commands.append({"command": public_arguments, "exit_code": result.returncode, "output_sha256": sha256(result.stdout.encode())})
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
        storage = json.loads(run(["docker", "info", "--format", "{{json .}}"], capture=True))
        endpoint = None if os.environ.get("DOCKER_CONTEXT") else os.environ.get("DOCKER_HOST")
        if not endpoint:
            endpoint = json.loads(run(["docker", "context", "inspect", "--format", "{{json .Endpoints.docker.Host}}"], capture=True))
        receipt["storage_budget"] = storage_budget(storage, endpoint, args.minimum_free_gib)
        if receipt["storage_budget"]["status"] in ("insufficient", "unknown"):
            raise RuntimeError("Docker storage preflight refused pull/build: " + str(receipt["storage_budget"]))
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
        run(["docker", "build", "--pull", "--platform", PLATFORM, "--file", "dev/Dockerfile", *build_network, "--tag", default_tag, "."])
        default_identity = inspect(default_tag)
        verify_inheritance(pinned_identity, default_identity)
        default_output = run([
            "docker", "run", "--rm", "--platform", PLATFORM, *runtime_network, default_tag,
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
            *build_network,
            "--build-arg", f"BASE_IMAGE={custom_base_tag}",
            "--build-arg", "IDENTITY_DEV_UID=1000", "--build-arg", "IDENTITY_DEV_GID=1000",
            "--tag", custom_tag, ".",
        ])
        custom_identity = inspect(custom_tag)
        verify_inheritance(custom_base_identity, custom_identity)
        custom_output = run([
            "docker", "run", "--rm", "--platform", PLATFORM, *runtime_network, custom_tag,
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
