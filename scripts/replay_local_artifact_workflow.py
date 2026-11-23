#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Replay the unchanged reference workflow with observed real artifact integrity.

Run inside the explicitly prepared owned helper, with its measured Docker
endpoint, source/evidence mounts and private caller environment. No workflow,
action, browser or security step is rewritten or skipped by this caller.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREFLIGHT = load("artifact_preflight", "qualify_local_artifacts.py")
OBSERVATION = load("artifact_observation", "observe_local_artifacts.py")


def replay(binary: Path, binary_hash: str, version: str, revision: str, prepared: Path, output: Path, cache: Path, private_environment: Path, owned_roots: list[Path], timeout: int) -> dict:
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or actual != revision or subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT):
        raise ValueError("Original workflow replay requires the exact clean standalone source")
    PREFLIGHT.refuse_ambient_act_configuration(ROOT)
    binary = binary.resolve(strict=True)
    if not re.fullmatch(r"[0-9a-f]{64}", binary_hash) or not binary.is_file() or hashlib.sha256(binary.read_bytes()).hexdigest() != binary_hash:
        raise ValueError("Selected derivative differs from its explicit hash")
    reported = subprocess.check_output([str(binary), "--version"], text=True).strip()
    if reported != version:
        raise ValueError("Selected derivative version differs")
    if private_environment.is_symlink() or not private_environment.is_file() or private_environment.stat().st_mode & 0o077:
        raise ValueError("Caller environment must be a private regular file")
    if any(re.match(r"\s*(?:export\s+)?(?:HOME|ACTIONS_RUNTIME_URL|ACTIONS_RUNTIME_TOKEN|ACTIONS_RESULTS_URL)\s*=", line) for line in private_environment.read_text().splitlines()):
        raise ValueError("Private caller file may not override home or artifact identity")
    lock = json.loads((ROOT / "dev/local-actions/reference-renderer.lock.json").read_text(), object_pairs_hook=PREFLIGHT.SOURCES.unique_json_object)
    _, actions = PREFLIGHT.SOURCES.validate_lock(lock, ROOT)
    receipt = json.loads((prepared / "action-mirrors.json").read_text(), object_pairs_hook=PREFLIGHT.SOURCES.unique_json_object)
    mirrors = {}
    arguments = []
    for action in actions:
        records = [m for m in receipt["mirrors"] if m["repository"] == action["repository"] and m["revision"] == action["revision"]]
        if len(records) != 1:
            raise ValueError("Every original action must have one exact local mirror")
        directory = (prepared / records[0]["directory"]).resolve()
        if prepared.resolve() not in directory.parents:
            raise ValueError("Action mirror escapes its prepared directory")
        inventory = PREFLIGHT.mirror_inventory(directory)
        if PREFLIGHT.SOURCES.tree_digest(inventory) != action["gitTreeSha1"]:
            raise ValueError("Original action mirror bytes/modes differ")
        selection = action["repository"] + "@" + action["revision"]
        mirrors[selection] = {"directory": directory, "inventory": inventory}
        arguments += ["--local-repository", selection + "=" + str(directory)]
    output = output.resolve()
    cache = cache.resolve()
    if output.exists() or output == ROOT or ROOT in output.parents or cache == ROOT or ROOT in cache.parents:
        raise ValueError("Task evidence/cache must stay outside source; evidence must be new")
    roots = [p.resolve() for p in owned_roots]
    if not roots or any(not any(p == r or r in p.parents for r in roots) for p in [ROOT, output, cache]):
        raise ValueError("Source/evidence/cache must be under the explicit owned roots")
    output.mkdir(parents=True)
    cache.mkdir(parents=True, exist_ok=True)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    observer = OBSERVATION.ArtifactObserver(port, output, roots)
    env = dict(os.environ)
    for name in ("ACTIONS_RUNTIME_TOKEN", "ACTIONS_RESULTS_URL", "GH_TOKEN", "GITHUB_TOKEN"):
        env.pop(name, None)
    env["ACTIONS_RUNTIME_URL"] = observer.url
    command = [str(binary), "push", "--directory", str(ROOT), "--workflows", str(ROOT / ".github/workflows/reference-renderer.yml"), "--job", "validate", "--strict", "-P", "ubuntu-latest=-self-hosted", "--no-cache-server", "--action-cache-path", str(cache), "--artifact-server-path", str(output / "artifact-server"), "--artifact-server-addr", "127.0.0.1", "--artifact-server-port", str(port), "--env-file", str(private_environment), "--secret-file", os.devnull, "--var-file", os.devnull, "--input-file", os.devnull, "--env", "GITHUB_RUN_ID=1", "--env", "GITHUB_RUN_ATTEMPT=1", *arguments]
    timed_out = False
    try:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        observer.act_pid = process.pid
        try:
            raw, _ = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                raw, _ = process.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                raw, _ = process.communicate()
    finally:
        observer.close()
    log = output / "act.private.log"
    log.write_bytes(raw)
    log.chmod(0o600)
    sanitized = PREFLIGHT.sanitize_log(raw.decode(errors="replace"), output, prepared, binary)
    for root in roots:
        sanitized = sanitized.replace(str(root), "<owned-task-root>")
    (output / "act.sanitized.log").write_text(sanitized)
    output_digests = re.findall(rb"SHA256 digest of uploaded artifact is ([0-9a-f]{64})", raw)
    preserved = all(PREFLIGHT.mirror_inventory(v["directory"]) == v["inventory"] for v in mirrors.values())
    unchanged = not subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)
    success = not timed_out and process.returncode == 0 and len(observer.results) == 1 and observer.results[0].get("status") == "passed" and observer.results[0].get("archiveSha256", "").encode() in output_digests and preserved and unchanged
    result = {"kind": "identity.local-original-workflow-artifact-replay/v1", "status": "passed" if success else "failed", "context": "actual unmodified workflow via explicitly named local act derivative and observed loopback artifact backend; not hosted GitHub CI", "sourceRevision": revision, "sourceCleanBeforeAndAfter": unchanged, "workflowSha256": lock["workflowSha256"], "toolVersion": version, "toolSha256": binary_hash, "actionGitTrees": {a["repository"] + "@" + a["revision"]: a["gitTreeSha1"] for a in actions}, "actionSourcesPreserved": preserved, "actExitCode": process.returncode, "timedOut": timed_out, "artifactObservations": observer.results, "actualUploaderDigestMatchesDownload": success, "rawLogBytes": len(raw), "rawLogSha256": hashlib.sha256(raw).hexdigest(), "sanitizedLogSha256": hashlib.sha256(sanitized.encode()).hexdigest(), "runtimeTokenRecorded": False, "signedUrlRecorded": False, "originalWorkflowOrActionsEdited": False, "hostedWorkflowClaim": False}
    (output / "workflow-replay.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--act-executable", type=Path, required=True)
    parser.add_argument("--act-sha256", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--action-mirrors", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--action-cache", type=Path, required=True)
    parser.add_argument("--private-env-file", type=Path, required=True)
    parser.add_argument("--owned-root", type=Path, action="append", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args()
    if not 30 <= args.timeout_seconds <= 1800:
        parser.error("Timeout must be between 30 and 1800 seconds")
    try:
        result = replay(args.act_executable, args.act_sha256, args.expected_version, args.source_revision, args.action_mirrors, args.output_directory, args.action_cache, args.private_env_file, args.owned_root, args.timeout_seconds)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        parser.exit(1, "Local original-workflow replay refused; inspect private task state without disclosing tokens or paths.\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
