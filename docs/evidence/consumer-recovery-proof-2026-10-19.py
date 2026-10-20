# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Replay the dated bounded Linux recovery proof with explicitly supplied trusted artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timezone

REPO: Path
WORKER: Path
WORKER_TEST = "compiler::filesystem::tests::inspection_tests::interrupted_consumer_worker"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    rows = []
    if not root.exists():
        return rows
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        assert not path.is_symlink(), relative
        if path.is_dir():
            rows.append({"path": relative, "kind": "directory"})
        else:
            data = path.read_bytes()
            rows.append({"path": relative, "kind": "file", "bytes": len(data), "sha256": digest(data)})
    return rows


def generated(root):
    return [{key: row[key] for key in ["path", "bytes", "sha256"]}
            for row in inventory(root) if row["kind"] == "file"]


def run(cli, root, output_root, command, commands, *, no_python=False, expected=0):
    env = dict(os.environ)
    if no_python:
        env["IDENTITY_PYTHON"] = str(root / "missing-python")
    args = [str(cli), command, "--repository-root", str(root), "--output-root", output_root]
    result = subprocess.run(args, cwd=root, env=env, capture_output=True, timeout=45)
    assert result.returncode == expected, (command, result.returncode, result.stdout, result.stderr)
    stdout = result.stdout.decode().replace(str(root), "<consumer>")
    stderr = result.stderr.decode().replace(str(root), "<consumer>")
    commands.append({"arguments": ["identity", command, "--repository-root", "<consumer>",
                                   "--output-root", output_root],
                     "pythonUnavailable": no_python, "exitCode": result.returncode,
                     "stdout": stdout, "stderr": stderr})
    return stdout, stderr


def scenario(cli, consumer, output_root):
    shutil.copytree(REPO / "tests/fixtures/v1/valid/minimal", consumer)
    (consumer / "unrelated.txt").write_bytes(b"unrelated consumer sentinel\n")
    before = inventory(consumer)
    canonical = inventory(consumer / ".identity")
    commands = []
    stdout, _ = run(cli, consumer, output_root, "v1-inspect", commands, no_python=True)
    assert "Pending transactions: 0" in stdout and "uncoordinated" in stdout
    assert inventory(consumer) == before and not (consumer / ".cache").exists()
    env = dict(os.environ)
    env["IDENTITY_RECOVERY_TEST_ROOT"] = str(consumer)
    env["IDENTITY_RECOVERY_TEST_OUTPUT_ROOT"] = output_root
    child = subprocess.Popen([str(WORKER), "--exact", WORKER_TEST, "--ignored", "--nocapture",
                              "--test-threads=1"], env=env, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = queue.Queue()
    def drain():
        for line in child.stdout:
            lines.put(line)
    reader = threading.Thread(target=drain, daemon=True)
    reader.start()
    ready = []
    try:
        while True:
            line = lines.get(timeout=30)
            ready.append(line.strip())
            if "IDENTITY_PROCESS_READY" in line:
                break
        assert child.poll() is None
        journals = list((consumer / ".cache/identity/transactions").glob("*/journal.json"))
        assert len(journals) == 1
        journal = journals[0]
        retained = journal.read_bytes()
        active = inventory(consumer)
        assert generated(consumer / output_root), "first promotion must have occurred"
        for command in ["v1-inspect", "v1-recover"]:
            _, stderr = run(cli, consumer, output_root, command, commands, no_python=True, expected=1)
            assert "IDN2346" in stderr
            assert inventory(consumer) == active
        child.kill()
        assert child.wait(timeout=15) != 0
        assert inventory(consumer) == active and journal.read_bytes() == retained
    finally:
        if child.poll() is None:
            child.kill()
        child.wait(timeout=15)
        reader.join(timeout=5)
        assert not reader.is_alive(), "worker output reader did not terminate"
        child.stdin.close()
        child.stdout.close()

    stdout, _ = run(cli, consumer, output_root, "v1-inspect", commands, no_python=True)
    assert "Pending transactions: 1" in stdout and "shared lock held" in stdout
    assert inventory(consumer) == active and journal.read_bytes() == retained
    _, stderr = run(cli, consumer, output_root, "v1-generate", commands, expected=1)
    assert "IDN2301" in stderr and "v1-inspect" in stderr and "v1-recover" in stderr
    assert inventory(consumer) == active
    stdout, _ = run(cli, consumer, output_root, "v1-recover", commands, no_python=True)
    assert "Recovered 1 v1 Identity transactions" in stdout
    assert not journal.exists() and generated(consumer / output_root) == []
    assert inventory(consumer / ".identity") == canonical
    assert (consumer / "unrelated.txt").read_bytes() == b"unrelated consumer sentinel\n"
    assert (consumer / ".cache/identity/writer.lock").read_bytes() == b""
    recovered = inventory(consumer)
    stdout, _ = run(cli, consumer, output_root, "v1-recover", commands, no_python=True)
    assert "Recovered 0 v1 Identity transactions" in stdout and inventory(consumer) == recovered
    stdout, _ = run(cli, consumer, output_root, "v1-inspect", commands, no_python=True)
    assert "Pending transactions: 0" in stdout and inventory(consumer) == recovered
    run(cli, consumer, output_root, "v1-generate", commands)
    outputs = generated(consumer / output_root)
    assert len(outputs) == 14
    complete = inventory(consumer)
    for command in ["v1-verify", "v1-generate", "v1-verify"]:
        run(cli, consumer, output_root, command, commands)
        assert inventory(consumer) == complete
    assert inventory(consumer / ".identity") == canonical
    assert (consumer / "unrelated.txt").read_bytes() == b"unrelated consumer sentinel\n"
    prior = json.loads((REPO / "docs/evidence/identity-writer-serialization-2026-10-19.json").read_text())
    prior_match = outputs == prior["observations"][0]["generatedInventory"] if output_root == "assets/identity" else None
    assert prior_match is not False, "default output differs from prior reviewed shipping inventory"
    return {"outputRoot": output_root, "worker": WORKER_TEST,
            "coordination": "Explicit test-only first-mutation readiness; killed and reaped before inspection/recovery.",
            "publishedJournalSha256": digest(retained), "publishedJournalPreservedUntilExplicitRecovery": True,
            "activeContendersRejectedWithoutMutation": True, "inspectionChangesNoFilesOrDirectories": True,
            "canonicalFiles": len([r for r in canonical if r["kind"] == "file"]),
            "canonicalAndUnrelatedBytesPreserved": True, "repeatRecoveryIsZeroAndUnchanged": True,
            "generatedInventory": outputs, "generatedFilesIncludingHiddenManifest": len(outputs),
            "defaultInventoryMatchesPriorReviewedReceipt": prior_match,
            "verificationAndIncrementalGenerationPreserveCompleteConsumerInventory": True,
            "commands": commands}


def main():
    global REPO, WORKER
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--identity-binary", required=True, type=Path)
    parser.add_argument("--worker-executable", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("this dated replay is qualified for Linux; native platform checks use the integration suite")
    REPO = args.repository_root.resolve(strict=True)
    WORKER = args.worker_executable.resolve(strict=True)
    binary = args.identity_binary.resolve(strict=True)
    receipt_path = args.receipt.resolve()
    if receipt_path.is_relative_to(REPO):
        parser.error("--receipt must be outside the source checkout")
    with tempfile.TemporaryDirectory(prefix="identity-recovery-proof-") as location:
        root = Path(location)
        cli = root / "standalone" / "identity"
        cli.parent.mkdir()
        shutil.copy2(binary, cli)
        external = root / "external-sentinel"
        external.write_bytes(b"external sentinel\n")
        receipt = {"observedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                   "baseRevision": "44bf13bc45916d51ae5de10e9af2ce894d3be486",
                   "platform": "Linux", "replayHarnessSha256": digest(Path(__file__).read_bytes()), "scope": "Genuine published runtime journal from test-only interrupted compiler execution; copied unmodified shipping CLI performs all inspection/recovery/regeneration.",
                   "shippingBinarySha256": digest(cli.read_bytes()), "workerExecutableSha256": digest(WORKER.read_bytes()),
                   "sourceFiles": [{"path": str(p.relative_to(REPO)), "sha256": digest(p.read_bytes())}
                                   for p in [REPO / p for p in ["src/cli.rs", "src/commands.rs", "src/lib.rs",
                                              "src/compiler/mod.rs", "src/compiler/filesystem.rs",
                                              "src/compiler/filesystem/tests/inspection_tests.rs",
                                              "tests/consumer_recovery.rs"]]],
                   "scenarios": [scenario(cli, root / "default-consumer", "assets/identity"),
                                 scenario(cli, root / "custom-consumer", "generated/branding")],
                   "limits": ["Linux local execution only; native macOS/Windows behavior requires fresh hosted checks.",
                              "The producer is the real compiler under a cfg(test) checkpoint; this is not a pristine shipping CLI killed by spontaneous timing.",
                              "Shipping inspection/recovery binary has no test hook and runs from a separate copied location.",
                              "Inventories compare file bytes, paths and directories; timestamps, inode identity and read-access metadata are not asserted.",
                              "Participating local processes only; no hostile filesystem, network-filesystem or power-loss guarantee."]}
        assert external.read_bytes() == b"external sentinel\n"
        receipt["externalSentinelPreserved"] = True
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps({"scenarios": len(receipt["scenarios"]), "commands": sum(len(s["commands"]) for s in receipt["scenarios"]),
                          "allPassed": True, "shippingBinarySha256": receipt["shippingBinarySha256"]}))


if __name__ == "__main__":
    main()
