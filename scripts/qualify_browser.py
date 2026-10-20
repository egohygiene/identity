#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Run the same pinned browser qualification from a local Docker CLI or CI."""

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
PROFILE_PATH = "dev/browser/profile.json"
BASELINE_PATH = "renderer/tests/e2e/__snapshots__/brand-kit-page.png"
APPROVED_BASELINE_SHA256 = "53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543"
PLATFORM = "linux/amd64"
CONTAINER_MARKER = "IDENTITY_BROWSER_RECEIPT="
HOST_MARKER = "IDENTITY_BROWSER_HOST_RECEIPT="


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def output_destination(destination: Path, repository: Path = REPOSITORY) -> Path:
    resolved = destination.resolve()
    source = repository.resolve()
    if resolved == source or source in resolved.parents:
        raise ValueError("--output-directory must resolve outside the repository")
    if "," in str(resolved) or "\n" in str(resolved) or "\r" in str(resolved):
        raise ValueError("--output-directory cannot contain a comma or newline in a Docker bind mount")
    if resolved.exists() and not resolved.is_dir():
        raise ValueError("--output-directory must name a directory")
    if resolved.exists() and any(resolved.iterdir()):
        raise ValueError("--output-directory must be new or empty; retain earlier evidence separately")
    return resolved


def repository_path(relative: str, repository: Path = REPOSITORY) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("Profile source paths must be relative to the repository")
    path = (repository / relative).resolve()
    if repository.resolve() not in path.parents:
        raise ValueError("Profile source paths must remain inside the repository")
    return path


def validate_profile(profile: dict[str, object], package: dict[str, object], registry: dict[str, object]) -> None:
    if not all(isinstance(item, dict) for item in (profile, package, registry)):
        raise ValueError("Profile, renderer package and registry evidence must be JSON objects")
    image = profile.get("image", "")
    if not isinstance(image, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*@sha256:[0-9a-f]{64}", image):
        raise ValueError("The browser profile must select an immutable image digest")
    if profile.get("platform") != PLATFORM or registry.get("platform") != PLATFORM:
        raise ValueError("Browser qualification currently selects linux/amd64")
    if registry.get("image") != image or registry.get("index_digest") != image.rsplit("@", 1)[1]:
        raise ValueError("The browser profile and registry image identities differ")
    dependencies = package.get("devDependencies", {})
    if not isinstance(dependencies, dict) or not re.fullmatch(r"\d+\.\d+\.\d+", str(profile.get("playwright", ""))) or profile.get("playwright") != dependencies.get("@playwright/test"):
        raise ValueError("The profile Playwright version differs from the renderer package pin")
    if not re.fullmatch(r"pnpm@\d+\.\d+\.\d+", str(profile.get("packageManager", ""))) or profile.get("packageManager") != package.get("packageManager"):
        raise ValueError("The profile package manager differs from the renderer package pin")
    baseline = profile.get("baseline", {})
    if not isinstance(baseline, dict) or baseline.get("path") != BASELINE_PATH or baseline.get("sha256") != APPROVED_BASELINE_SHA256:
        raise ValueError("Qualification must preserve the existing approved screenshot identity")
    if not re.fullmatch(r"[0-9a-f]{40}", baseline.get("approvalRevision", "")):
        raise ValueError("The screenshot approval revision must be an immutable Git revision")
    if not isinstance(profile.get("chromium"), dict) or profile["chromium"].get("colorProfile") != "srgb":
        raise ValueError("The qualified Chromium color profile must be explicit sRGB")


def image_identity(image: dict[str, object]) -> dict[str, object]:
    config = image["Config"]
    return {
        "id": image["Id"], "repo_digests": image.get("RepoDigests", []),
        "os": image["Os"], "architecture": image["Architecture"],
        "user": config.get("User", ""), "entrypoint": config.get("Entrypoint"),
        "cmd": config.get("Cmd"),
    }


def verify_registry_binding(profile: dict[str, object], registry: dict[str, object], image: dict[str, object]) -> None:
    if image["id"] != registry["config_digest"]:
        raise RuntimeError("The pulled browser image config does not match the registry receipt")
    if (image["os"], image["architecture"]) != ("linux", "amd64"):
        raise RuntimeError("The pulled image does not match linux/amd64")
    config = registry["image_config"]
    for field in ("os", "architecture", "user", "entrypoint", "cmd"):
        if image[field] != config[field]:
            raise RuntimeError(f"The pulled image's {field} differs from the registry observation")
    if not any(value.rsplit("@", 1)[-1] == profile["image"].rsplit("@", 1)[-1] for value in image["repo_digests"]):
        raise RuntimeError("Docker did not retain the profile's immutable browser repository digest")


def evidence_file(relative: str, output: Path) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise RuntimeError("Browser artifact paths must be relative evidence paths")
    resolved = (output / relative).resolve()
    if output.resolve() not in resolved.parents or not resolved.is_file():
        raise RuntimeError("Browser proof artifact is missing or outside its evidence directory")
    return resolved


def container_receipt(output: str, profile: dict[str, object], directory: Path) -> dict[str, object]:
    records = [line[len(CONTAINER_MARKER):] for line in output.splitlines() if line.startswith(CONTAINER_MARKER)]
    if len(records) != 1:
        raise RuntimeError("Browser qualification must emit exactly one structured container receipt")
    receipt = json.loads(records[0])
    if not isinstance(receipt, dict) or receipt.get("status") != "passed" or receipt.get("platform") != PLATFORM:
        raise RuntimeError("The container did not qualify the selected browser environment")
    baseline = receipt.get("baseline", {})
    if not isinstance(baseline, dict) or baseline.get("path") != BASELINE_PATH or baseline.get("sha256") != profile["baseline"]["sha256"] or baseline.get("approvalRevision") != profile["baseline"]["approvalRevision"] or baseline.get("unchanged") is not True:
        raise RuntimeError("The container receipt does not preserve the approved baseline")
    runtimes = receipt.get("runtimes", {})
    browser = receipt.get("browser", {})
    fonts = receipt.get("fonts", {})
    if receipt.get("settings") != profile["settings"] or not isinstance(runtimes, dict) or runtimes.get("playwright") != profile["playwright"] or "pnpm@" + str(runtimes.get("pnpm")) != profile["packageManager"]:
        raise RuntimeError("The browser receipt lacks matching rendering/package settings")
    if not isinstance(browser, dict) or browser.get("version") != profile["chromium"]["version"] or not re.fullmatch(r"[0-9a-f]{64}", str(browser.get("executableSha256", ""))) or "--force-color-profile=srgb" not in browser.get("commandLine", []):
        raise RuntimeError("The browser receipt lacks its qualified executable and color-profile evidence")
    if not all(browser.get("settings", {}).get(key) == value for key, value in profile["settings"].items()):
        raise RuntimeError("The observed browser settings differ from the qualified profile")
    if not isinstance(fonts, dict) or not fonts.get("files") or not fonts.get("configuration") or not browser.get("renderedFonts"):
        raise RuntimeError("The browser receipt lacks font/runtime provenance")
    phases = (("positive", 0, 6, 0), ("negative", 1, 0, 1), ("restored", 0, 1, 0))
    for name, exit_code, passed, failed in phases:
        phase = receipt.get(name, {})
        if not isinstance(phase, dict) or any(type(phase.get(key)) is not int or phase.get(key) != value for key, value in (
            ("exitCode", exit_code), ("passed", passed), ("failed", failed), ("skipped", 0),
        )):
            raise RuntimeError(f"The {name} browser proof did not produce the required result")
        evidence_file(phase.get("report"), directory)
    negative = receipt["negative"]
    if negative.get("expectedFailure") != "screenshot-comparison" or negative.get("baselineUnchanged") is not True:
        raise RuntimeError("The negative browser proof must fail screenshot comparison without changing its baseline")
    differences = negative.get("diffArtifacts", [])
    if not isinstance(differences, list) or not differences:
        raise RuntimeError("The negative proof did not retain a screenshot difference")
    for artifact in differences:
        if not isinstance(artifact, dict):
            raise RuntimeError("Screenshot-difference evidence must name a file and checksum")
        path = evidence_file(artifact.get("path"), directory)
        if not path.name.endswith("-diff.png") or sha256(path.read_bytes()) != artifact.get("sha256"):
            raise RuntimeError("The screenshot-difference artifact is missing or has changed")
    retained = json.loads(evidence_file("qualification.json", directory).read_text())
    if retained != receipt:
        raise RuntimeError("The retained qualification receipt differs from its successful process output")
    return receipt


def source_evidence(profile: dict[str, object]) -> dict[str, object]:
    critical = {
        PROFILE_PATH, "dev/browser/Dockerfile", "scripts/qualify_browser.py",
        "renderer/playwright.config.js", "renderer/scripts/qualify-browser.mjs",
        "renderer/tests/e2e/renderer.spec.js", BASELINE_PATH,
        "renderer/package.json", "renderer/pnpm-lock.yaml", ".dockerignore",
        profile["registryReceipt"],
    }
    critical.update(path.relative_to(REPOSITORY).as_posix() for path in (REPOSITORY / ".github/workflows").glob("*.yml"))
    files = subprocess.check_output(["git", "ls-files", "--cached", "-z"], cwd=REPOSITORY).decode().split("\0")
    selected = sorted(critical | {path for path in files if path and (
        path.startswith("tests/fixtures/") or (not path.startswith("docs/") and not path.endswith(".md"))
    )})
    inventory = {path: sha256((REPOSITORY / path).read_bytes()) for path in selected}
    payload = b"".join(path.encode() + b"\0" + digest.encode() + b"\n" for path, digest in inventory.items())
    return {
        "git_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip(),
        "git_worktree_clean": not bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=REPOSITORY)),
        "critical_files_sha256": {path: inventory[path] for path in sorted(critical)},
        "build_source_inventory": {
            "files": len(inventory), "sha256": sha256(payload),
            "encoding": "sorted UTF-8 relative path, NUL, lowercase SHA-256, newline",
            "scope": "Critical browser/profile/registry/workflow files; tracked non-Markdown inputs outside docs; all tracked fixtures. Documentation-only changes are excluded except the critical registry receipt.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, required=True, help="New or empty evidence directory outside the checkout")
    parser.add_argument("--mode", choices=("local", "ci"), default="local", help="Invocation label only; both modes use the same fixed environment")
    args = parser.parse_args()
    try:
        destination = output_destination(args.output_directory)
        destination.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    hosted = os.environ.get("GITHUB_ACTIONS") == "true"
    context = "hosted-local-entrypoint-replay" if hosted and args.mode == "local" else "github-actions-ci" if hosted else "local-host"
    commands: list[dict[str, object]] = []
    envelope: dict[str, object] = {
        "kind": "dated browser-environment qualification host receipt",
        "observed_at": datetime.now(timezone.utc).isoformat(), "status": "failed",
        "mode": args.mode, "execution_context": context, "platform": PLATFORM,
        "commands": commands,
        "limits": [
            "The invocation mode labels a caller; both use identical image/rendering settings.",
            "A hosted local-entrypoint replay is not an actual Docker run in an unavailable developer workspace.",
            "Only the recorded image/platform/fonts/settings and unchanged approved baseline are qualified.",
            "No baseline regeneration, tolerance relaxation, release, deployment or human approval occurs.",
        ],
    }
    tag: str | None = None

    def public_text(value: str) -> str:
        return value.replace(str(destination), "<output-directory>").replace(str(REPOSITORY), "<repository>")

    def run(arguments: list[str], *, capture: bool = False, timeout: int = 1800) -> str:
        public_arguments = [public_text(item) for item in arguments]
        print("Running: " + " ".join(public_arguments), flush=True)
        try:
            result = subprocess.run(arguments, cwd=REPOSITORY, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as error:
            commands.append({"command": public_arguments, "outcome": "unavailable-or-interrupted", "failure": type(error).__name__})
            raise
        if not capture or result.returncode:
            print(public_text(result.stdout), end="", flush=True)
        commands.append({"command": public_arguments, "exit_code": result.returncode, "output_sha256": sha256(result.stdout.encode())})
        if result.returncode:
            raise RuntimeError(f"Command failed with exit code {result.returncode}: {arguments[0]}")
        return result.stdout

    def inspect(reference: str) -> dict[str, object]:
        objects = json.loads(run(["docker", "image", "inspect", reference], capture=True, timeout=60))
        if len(objects) != 1:
            raise RuntimeError("Docker inspection returned an unexpected image count")
        return image_identity(objects[0])

    try:
        profile = json.loads((REPOSITORY / PROFILE_PATH).read_text())
        registry = json.loads(repository_path(profile["registryReceipt"]).read_text())
        package = json.loads((REPOSITORY / "renderer/package.json").read_text())
        validate_profile(profile, package, registry)
        defaults = re.findall(r"^ARG BROWSER_IMAGE=(\S+)\s*$", (REPOSITORY / "dev/browser/Dockerfile").read_text(), re.MULTILINE)
        if defaults != [profile["image"]]:
            raise RuntimeError("The browser Dockerfile default differs from its immutable profile")
        if sha256((REPOSITORY / BASELINE_PATH).read_bytes()) != APPROVED_BASELINE_SHA256:
            raise RuntimeError("The approved screenshot differs before qualification; no regeneration is allowed")
        envelope["profile"] = profile
        envelope["source"] = source_evidence(profile)
        envelope["registry"] = {key: registry[key] for key in ("image", "platform", "index_digest", "manifest_digest", "config_digest")}
        server = json.loads(run(["docker", "version", "--format", "{{json .Server}}"], capture=True, timeout=60))
        envelope["docker_server"] = {key: server.get(key) for key in ("Version", "Os", "Arch", "KernelVersion")}
        if server.get("Os") != "linux":
            raise RuntimeError("The qualification requires a Linux Docker engine")
        envelope["engine_platform_relation"] = "native-amd64" if server.get("Arch") == "amd64" else "non-native-engine; requested amd64 image may use emulation"
        run(["docker", "pull", "--platform", PLATFORM, profile["image"]], timeout=900)
        base_image = inspect(profile["image"])
        verify_registry_binding(profile, registry, base_image)
        envelope["base_image"] = base_image
        tag = "identity-browser-qualification:" + uuid.uuid4().hex[:12]
        run(["docker", "build", "--pull", "--platform", PLATFORM, "--file", "dev/browser/Dockerfile", "--build-arg", "BROWSER_IMAGE=" + profile["image"], "--tag", tag, "."])
        built_image = inspect(tag)
        if (built_image["os"], built_image["architecture"]) != ("linux", "amd64"):
            raise RuntimeError("The built browser image does not match the selected platform")
        envelope["built_image"] = built_image
        stdout = run([
            "docker", "run", "--rm", "--init", "--platform", PLATFORM,
            "--network", "none", "--shm-size", "1gb",
            "--env", "CI=1", "--env", "TZ=UTC", "--env", "LANG=C.UTF-8", "--env", "LC_ALL=C.UTF-8",
            "--mount", f"type=bind,source={destination},target=/evidence", tag,
            "node", "scripts/qualify-browser.mjs", "--output-directory", "/evidence",
        ])
        qualification = container_receipt(stdout, profile, destination)
        if qualification.get("profileSha256") != envelope["source"]["critical_files_sha256"][PROFILE_PATH]:
            raise RuntimeError("The container profile bytes differ from the source-bound host profile")
        envelope["qualification"] = qualification
        envelope["status"] = "passed"
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as error:
        envelope["failure"] = public_text(f"{type(error).__name__}: {error}")
        print(envelope["failure"], file=sys.stderr, flush=True)
    finally:
        if tag:
            try:
                cleanup = subprocess.run(["docker", "image", "rm", tag], cwd=REPOSITORY, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False, timeout=60)
                envelope["own_image_cleanup_exit_code"] = cleanup.returncode
            except (OSError, subprocess.SubprocessError) as error:
                envelope["own_image_cleanup_failure"] = type(error).__name__
        try:
            after = sha256((REPOSITORY / BASELINE_PATH).read_bytes())
            envelope["approved_baseline_after_sha256"] = after
            if after != APPROVED_BASELINE_SHA256:
                envelope["status"] = "failed"
                envelope["failure"] = "The approved screenshot changed; qualification cannot approve or restore it"
        except OSError as error:
            envelope["status"] = "failed"
            envelope["failure"] = public_text(f"Approved screenshot unavailable: {error}")
        inventory = {}
        for artifact in sorted(destination.rglob("*")):
            if artifact.is_file():
                resolved = artifact.resolve()
                if destination not in resolved.parents:
                    envelope["status"] = "failed"
                    envelope["failure"] = "An evidence artifact redirects outside its output directory"
                    continue
                inventory[artifact.relative_to(destination).as_posix()] = sha256(artifact.read_bytes())
        envelope["artifact_files_sha256"] = inventory
        envelope["artifact_inventory_excludes_host_receipt"] = True
        (destination / "host-qualification.json").write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")
        print(HOST_MARKER + json.dumps(envelope, sort_keys=True, separators=(",", ":")), flush=True)
    return 0 if envelope["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
