#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Run a tiny real pinned-uploader fixture before a long local act workflow.

The selected executable must match an explicit digest/version. This is a
synthetic, loopback-only transport proof, not original-workflow/hosted evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import signal
import socket
import stat
import subprocess


REPOSITORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("identity_action_sources", REPOSITORY / "scripts/prepare_local_actions.py")
SOURCES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCES)
UPLOADER = "actions/upload-artifact"
REVISION = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mirror_inventory(directory: Path) -> dict[str, tuple[int, bytes]]:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Uploader mirror must be a real directory")
    result = {}
    total = 0
    for root, directories, files in os.walk(directory, followlinks=False):
        for name in directories:
            if (Path(root) / name).is_symlink():
                raise ValueError("Uploader mirror contains a directory link")
        for name in files:
            path = Path(root) / name
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("Uploader mirror contains a link/special file")
            total += info.st_size
            if len(result) >= SOURCES.MAX_MEMBERS or total > SOURCES.MAX_EXTRACTED_BYTES:
                raise ValueError("Uploader mirror exceeds its bounds")
            data = path.read_bytes()
            if len(data) != info.st_size:
                raise ValueError("Uploader mirror changed during inventory")
            result[path.relative_to(directory).as_posix()] = (0o100755 if info.st_mode & 0o111 else 0o100644, data)
    return result


def sanitize_log(text: str, output: Path, mirror: Path, executable: Path) -> str:
    for path in sorted([str(output), str(mirror), str(executable), str(REPOSITORY), str(Path.home())], key=len, reverse=True):
        if path and path != "/":
            text = text.replace(path, "<local-path>")
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "GH_TOKEN", "GITHUB_TOKEN", "OPENAI_API_KEY"):
        value = os.environ.get(name)
        if value and len(value) >= 8:
            text = text.replace(value, "<redacted-environment>")
    return re.sub(r"https?://[^\s\"<>]+", "<url>", text)


def refuse_ambient_act_configuration(repository: Path) -> None:
    ambient = [Path.home() / ".actrc", repository / ".actrc"]
    ambient += [Path(p) / "act/actrc" for p in os.environ.get("XDG_CONFIG_DIRS", "/etc/xdg").split(os.pathsep) if p]
    ambient += [Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "act/actrc"]
    if any(p.exists() or p.is_symlink() for p in ambient):
        raise ValueError("This bounded caller refuses ambient act configuration")


def qualify(executable: Path, expected_hash: str, expected_version: str, mirror: Path, output: Path, timeout: int) -> dict:
    if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise ValueError("An explicit lowercase executable SHA256 is required")
    executable = executable.resolve(strict=True)
    if not executable.is_file() or sha256(executable.read_bytes()) != expected_hash:
        raise ValueError("Selected executable differs from the explicit digest")
    output = output.resolve()
    if output.exists() or output == REPOSITORY or REPOSITORY in output.parents:
        raise ValueError("Output must be new and outside the consumer checkout")
    mirror = mirror.resolve(strict=True)
    lock = json.loads((REPOSITORY / "dev/local-actions/reference-renderer.lock.json").read_text(), object_pairs_hook=SOURCES.unique_json_object)
    _, locked = SOURCES.validate_lock(lock, REPOSITORY)
    selected = [item for item in locked if item["repository"] == UPLOADER and item["revision"] == REVISION]
    if len(selected) != 1:
        raise ValueError("The original workflow must retain its exact uploader pin")
    before = mirror_inventory(mirror)
    if SOURCES.tree_digest(before) != selected[0]["gitTreeSha1"]:
        raise ValueError("Uploader source differs from the original full Git tree")
    refuse_ambient_act_configuration(REPOSITORY)
    version = subprocess.run([str(executable), "--version"], capture_output=True, text=True, check=True, timeout=10).stdout.strip()
    if version != expected_version:
        raise ValueError("Selected tool reports a different explicit version")
    output.mkdir(parents=True)
    fixture = output / "fixture"
    fixture.mkdir()
    nonce = secrets.token_hex(16)
    payloads = {"notes.txt": ("Identity local transport " + nonce + "\n").encode(), "media/sample.bin": bytes.fromhex(nonce) + bytes([0, 1, 2, 255, 127])}
    expected = {}
    for name, data in payloads.items():
        target = fixture / "input" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        expected[name] = {"bytes": len(data), "sha256": sha256(data)}
    manifest = {"kind": "identity.local-artifact-fixture/v1", "nonce": nonce, "files": expected}
    (fixture / "fixture-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    worker = (REPOSITORY / "scripts/local_artifact_roundtrip.py").read_bytes()
    (fixture / "roundtrip.py").write_bytes(worker)
    workflow = '''name: Actual local artifact transport fixture
on: [push]
permissions:
  contents: read
jobs:
  transport:
    runs-on: ubuntu-latest
    env:
      IDENTITY_TRANSPORT_FIXTURE: FIXTURE_PATH
    steps:
      - name: Stage exact synthetic fixture in the host executor workspace
        run: |
          cp -R "$IDENTITY_TRANSPORT_FIXTURE/input" .
          cp "$IDENTITY_TRANSPORT_FIXTURE/roundtrip.py" "$IDENTITY_TRANSPORT_FIXTURE/fixture-manifest.json" .
      - name: Upload actual sentinel files
        id: upload
        uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
        with:
          name: identity-transport-probe
          path: input/
          if-no-files-found: error
          archive: true
      - name: Download and verify actual archive
        env:
          FIXTURE_ARTIFACT_ID: ${{ steps.upload.outputs.artifact-id }}
          FIXTURE_ARTIFACT_DIGEST: ${{ steps.upload.outputs.artifact-digest }}
        run: python3 roundtrip.py --manifest fixture-manifest.json --output "$IDENTITY_TRANSPORT_FIXTURE/roundtrip.json"
'''
    workflow = workflow.replace("FIXTURE_PATH", json.dumps(str(fixture)))
    (fixture / "workflow.yml").write_text(workflow)
    git_env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    for arguments in (["git", "init", "--quiet", "--initial-branch=main"], ["git", "add", "."], ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "-c", "user.name=Identity transport fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "Synthetic transport fixture"]):
        subprocess.run(arguments, cwd=fixture, env=git_env, check=True, capture_output=True)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    env = {name: os.environ[name] for name in ("PATH", "HOME", "USER", "LOGNAME") if name in os.environ}
    env.update({"LANG": "C.UTF-8", "TZ": "UTC", "XDG_CONFIG_HOME": str(output / "config"), "XDG_CACHE_HOME": str(output / "cache"), "NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost"})
    arguments = [str(executable), "push", "--directory", str(fixture), "--workflows", str(fixture / "workflow.yml"), "--job", "transport", "--strict", "-P", "ubuntu-latest=-self-hosted", "--no-cache-server", "--action-cache-path", str(output / "action-cache"), "--artifact-server-path", str(output / "artifacts"), "--artifact-server-addr", "127.0.0.1", "--artifact-server-port", str(port), "--local-repository", UPLOADER + "@" + REVISION + "=" + str(mirror), "--secret-file", os.devnull, "--env-file", os.devnull, "--var-file", os.devnull, "--input-file", os.devnull, "--env", "GITHUB_RUN_ID=1"]
    timed_out = False
    process = subprocess.Popen(arguments, cwd=fixture, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    try:
        raw, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            raw, _ = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            raw, _ = process.communicate()
    private_log = output / "act.private.log"
    private_log.write_bytes(raw)
    private_log.chmod(0o600)
    public_log = sanitize_log(raw.decode(errors="replace"), output, mirror, executable).encode()
    (output / "act.sanitized.log").write_bytes(public_log)
    result = {"kind": "identity.local-artifact-preflight/v1", "status": "failed", "context": "explicit trusted host executor and loopback storage, synthetic fixture only", "toolVersion": version, "toolSha256": expected_hash, "uploader": UPLOADER + "@" + REVISION, "uploaderGitTree": selected[0]["gitTreeSha1"], "fixtureWorkflowSha256": sha256(workflow.encode()), "workerSha256": sha256(worker), "expectedFiles": expected, "actExitCode": process.returncode, "timedOut": timed_out, "rawLogBytes": len(raw), "rawLogSha256": sha256(raw), "sanitizedLogSha256": sha256(public_log), "officialActOverwritten": False, "hostedWorkflowClaim": False}
    receipt = fixture / "roundtrip.json"
    try:
        if timed_out or process.returncode != 0 or not receipt.is_file():
            raise ValueError("Actual uploader/worker did not complete")
        roundtrip = json.loads(receipt.read_text(), object_pairs_hook=SOURCES.unique_json_object)
        if roundtrip.get("status") != "passed" or roundtrip.get("nonce") != nonce or roundtrip.get("files") != expected or roundtrip.get("uploaderArchiveSha256") != roundtrip.get("downloadedArchiveSha256"):
            raise ValueError("Round-trip receipt does not match this actual fixture")
        from importlib.util import spec_from_file_location, module_from_spec
        spec = spec_from_file_location("local_artifact_worker", REPOSITORY / "scripts/local_artifact_roundtrip.py")
        worker_module = module_from_spec(spec)
        spec.loader.exec_module(worker_module)
        archive = (fixture / "roundtrip.zip").read_bytes()
        worker_module.verify_archive(archive, expected, roundtrip["uploaderArchiveSha256"])
        if mirror_inventory(mirror) != before or any((fixture / "input" / name).read_bytes() != content for name, content in payloads.items()) or (fixture / "roundtrip.py").read_bytes() != worker:
            raise ValueError("Source/fixture changed during transport")
        result.update({"status": "passed", "roundtrip": roundtrip, "sourceAndInputsPreserved": True})
    except (OSError, ValueError, KeyError):
        result["failure"] = "Actual local upload/download/inventory proof unavailable; inspect the sanitized log."
    (output / "preflight.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--act-executable", type=Path, required=True)
    parser.add_argument("--act-sha256", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--uploader-source", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    if not 5 <= args.timeout_seconds <= 300:
        parser.error("Timeout must be between5 and300seconds")
    try:
        result = qualify(args.act_executable, args.act_sha256, args.expected_version, args.uploader_source, args.output_directory, args.timeout_seconds)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        parser.exit(1, "Local artifact preflight refused; no private paths, tokens or signed URLs are printed.\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
