# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Reject false-positive authoring receipts using deliberate faulty producers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_identity as validator
import verify_consumer_authoring as proof


class FakeCompiler:
    """Implement selected-output state with optional meaningful producer defects."""

    def __init__(self, defect: str | None = None):
        self.defect = defect
        self.generations = 0

    def __call__(self, binary: Path, operation: str, consumer: Path, output_root: str) -> subprocess.CompletedProcess[str]:
        del binary
        generated = consumer / output_root
        artifact = generated / "packages/metadata/metadata.json"
        manifest_path = generated / proof.MANIFEST
        if operation == "v1-generate":
            self.generations += 1
            artifact.parent.mkdir(parents=True, exist_ok=True)
            content = b"generated selected metadata\n"
            if self.defect == "nondeterministic":
                content += str(self.generations).encode()
            artifact.write_bytes(content)
            output = {
                "path": f"{output_root}/packages/metadata/metadata.json",
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
            if self.defect == "checksum":
                output["sha256"] = "0" * 64
            elif self.defect == "escape":
                output["path"] = f"{output_root}/../escaped.json"
            elif self.defect == "unmanifested":
                (generated / "unmanifested.txt").write_bytes(b"unselected file")
            manifest = {
                "schema": "identity.compiler-manifest/v1",
                "sourceDigest": validator.canonical_source_digest(consumer),
                "outputs": [output],
            }
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            if self.defect == "source-write":
                (consumer / ".identity/brief.md").write_bytes(b"changed by the producer\n")
            return subprocess.CompletedProcess([], 0, "", "")
        if self.defect == "verifier-write":
            (consumer / "verification-created-cache").mkdir(exist_ok=True)
            return subprocess.CompletedProcess([], 0, "", "")
        if self.defect == "always-fail":
            return subprocess.CompletedProcess([], 1, "", "PRIVATE LOCAL PATH THAT MUST NOT LEAK")
        if self.defect == "always-pass":
            return subprocess.CompletedProcess([], 0, "", "")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        current = artifact.read_bytes() if artifact.is_file() else b""
        valid = (
            artifact.is_file()
            and hashlib.sha256(current).hexdigest() == manifest["outputs"][0]["sha256"]
            and validator.canonical_source_digest(consumer) == manifest["sourceDigest"]
        )
        return subprocess.CompletedProcess([], 0 if valid else 1, "", "")


class ConsumerAuthoringProofTests(unittest.TestCase):
    """Test actual evidence boundaries rather than repeating compiler implementation."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.consumer = self.work / "consumer"
        shutil.copytree(SCRIPTS.parent / "examples/v1/minimal", self.consumer)
        self.binary = self.work / "explicit-identity"
        self.binary.write_bytes(b"explicit fake producer selected by test")
        self.receipt = self.work / "receipt.json"
        self.arguments = argparse.Namespace(
            repository_root=self.consumer,
            identity_binary=self.binary,
            consumer_repository="example/consumer",
            consumer_revision="a" * 40,
            identity_revision="b" * 40,
            output_root="assets/identity",
            receipt=self.receipt,
        )
        self.source_before = proof.inventory(self.consumer)

    def run_proof(self, defect: str | None = None) -> dict[str, object]:
        with (
            patch.object(proof, "run_binary", FakeCompiler(defect)),
            patch.object(proof, "checkout_revision", side_effect=lambda root, revision, paths: {"revision": revision, "revisionEvidence": "test assertion"}),
        ):
            return proof.prove(self.arguments)

    def test_success_requires_two_fresh_generations_and_three_nonrepairing_failures(self) -> None:
        # Old committed/optional output must never contaminate the fresh proof.
        old = self.consumer / "assets/identity/optional/old.json"
        old.parent.mkdir(parents=True)
        old.write_bytes(b"preserve this original optional projection")
        before = proof.inventory(self.consumer)
        result = self.run_proof()
        self.assertEqual(proof.inventory(self.consumer), before)
        self.assertEqual(result["baseline"]["independentGenerations"][0]["files"], 2)
        self.assertEqual(len(result["baseline"]["independentGenerations"]), 2)
        self.assertEqual([probe["verificationExit"] for probe in result["probes"]], [1, 1, 1])
        self.assertTrue(all(probe["verificationPreservedFiles"] for probe in result["probes"]))
        serialized = json.dumps(result)
        self.assertNotIn(str(self.work), serialized)
        self.assertNotIn(str(SCRIPTS.parent), serialized)
        self.assertNotIn("schema", result)

    def test_faulty_producers_cannot_create_a_success_receipt(self) -> None:
        for defect, reason in (
            ("verifier-write", "v1-verify changed"),
            ("always-fail", "expected success"),
            ("always-pass", "expected failure"),
            ("checksum", "checksum"),
            ("escape", "portable"),
            ("unmanifested", "exactly match"),
            ("nondeterministic", "different file trees"),
            ("source-write", "changed canonical"),
        ):
            with self.subTest(defect=defect):
                with self.assertRaisesRegex(proof.ProofError, reason):
                    self.run_proof(defect)
                self.assertEqual(proof.inventory(self.consumer), self.source_before)

    def test_output_removal_cannot_overlap_source_or_escape_the_consumer(self) -> None:
        for output in (".", "../outside", "/absolute", ".identity", ".identity/derived", "assets/../source", ".git/generated", "target/generated"):
            with self.subTest(output=output):
                self.arguments.output_root = output
                with self.assertRaises(proof.ProofError):
                    self.run_proof()
        self.assertEqual(proof.inventory(self.consumer), self.source_before)

    def test_declared_external_source_cannot_be_removed_or_omitted_from_copies(self) -> None:
        snapshot = validator.SourceSnapshot(self.consumer)
        snapshot.files = {"assets/identity/source.svg": "0" * 64}
        with self.assertRaisesRegex(proof.ProofError, "overlaps validated source"):
            proof.check_output_root("assets/identity", snapshot)
        snapshot.files = {".identity/target/source.svg": "0" * 64}
        with self.assertRaisesRegex(proof.ProofError, "cache exclusions"):
            proof.check_output_root("assets/identity", snapshot)

    def test_consumer_symlink_is_not_followed_when_clearing_generated_output(self) -> None:
        outside = self.work / "outside"
        outside.mkdir()
        sentinel = outside / "keep.txt"
        sentinel.write_bytes(b"must survive")
        try:
            (self.consumer / "assets").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("directory symlink creation is unavailable on this platform")
        before = proof.inventory(self.consumer)
        with self.assertRaisesRegex(proof.ProofError, "symbolic link"):
            self.run_proof()
        self.assertEqual(sentinel.read_bytes(), b"must survive")
        self.assertEqual(proof.inventory(self.consumer), before)

    def test_receipt_cannot_overwrite_consumer_or_trusted_identity_source(self) -> None:
        common = [
            "--repository-root", str(self.consumer), "--identity-binary", str(self.binary),
            "--consumer-repository", "example/consumer", "--consumer-revision", "a" * 40,
            "--identity-revision", "b" * 40,
        ]
        binary_before = self.binary.read_bytes()
        for receipt in (self.consumer / "receipt.json", SCRIPTS / "validate_identity.py", self.binary):
            with self.subTest(receipt=receipt.name):
                with patch.object(proof, "prove") as execute, patch("sys.stderr"):
                    self.assertEqual(proof.main(common + ["--receipt", str(receipt)]), 1)
                execute.assert_not_called()
        self.assertEqual(proof.inventory(self.consumer), self.source_before)
        self.assertEqual(self.binary.read_bytes(), binary_before)

    def test_explicit_binary_timeout_is_bounded_and_sanitized(self) -> None:
        with patch.object(proof.subprocess, "run", side_effect=subprocess.TimeoutExpired(["private/local/path"], 60)) as execute:
            with self.assertRaisesRegex(proof.ProofError, "exceeded the proof timeout") as failure:
                proof.run_binary(self.binary, "v1-verify", self.consumer, "assets/identity")
        self.assertEqual(execute.call_args.kwargs["timeout"], proof.COMMAND_TIMEOUT_SECONDS)
        self.assertNotIn("private/local/path", str(failure.exception))

    def test_negative_probe_rejects_invocation_and_signal_statuses(self) -> None:
        for code in (2, -9):
            with self.subTest(status=code), patch.object(proof, "run_binary", return_value=subprocess.CompletedProcess([], code, "", "")):
                with self.assertRaisesRegex(proof.ProofError, "expected failure exit 1"):
                    proof.verify_read_only(self.binary, self.consumer, "assets/identity", expect_success=False)

    def test_git_revision_comparison_reads_raw_blobs_without_consumer_content_filters(self) -> None:
        calls = []
        revision = "a" * 40
        source = self.consumer / ".identity/brief.md"
        blob = source.read_bytes()

        def fake_git(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess:
            calls.append(arguments)
            if "--show-toplevel" in arguments:
                return subprocess.CompletedProcess(arguments, 0, str(self.consumer) + "\n", "")
            if "rev-parse" in arguments:
                return subprocess.CompletedProcess(arguments, 0, revision + "\n", "")
            if "ls-tree" in arguments:
                return subprocess.CompletedProcess(arguments, 0, b"100644 blob " + b"c" * 40 + b"\t.identity/brief.md\0", b"")
            self.assertIn("cat-file", arguments)
            return subprocess.CompletedProcess(arguments, 0, blob, b"")

        with patch.object(proof.subprocess, "run", side_effect=fake_git):
            evidence = proof.checkout_revision(self.consumer, revision, [".identity/brief.md"])
        self.assertTrue(evidence["consumedFilesMatchRevision"])
        self.assertTrue(all("core.fsmonitor=false" in arguments for arguments in calls))
        self.assertFalse(any("diff" in arguments for arguments in calls))
        with patch.object(proof.subprocess, "run", return_value=subprocess.CompletedProcess([], 128, "", "private path")):
            asserted = proof.checkout_revision(self.consumer, revision, [".identity/brief.md"])
        self.assertIn("caller-asserted", asserted["revisionEvidence"])
        self.assertNotIn("private path", json.dumps(asserted))

    def test_real_git_checkout_checks_actual_revision_and_consumed_bytes(self) -> None:
        if shutil.which("git") is None:
            self.skipTest("Git is unavailable for the actual checkout integration proof")
        environment = os.environ.copy()
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        environment["GIT_CONFIG_GLOBAL"] = os.devnull
        prefix = [
            "git", "-c", "core.fsmonitor=false", "-c", "commit.gpgSign=false",
            "-c", "user.name=Identity Proof Test", "-c", "user.email=proof@example.invalid",
            "-C", str(self.consumer),
        ]

        def setup_git(*arguments: str) -> str:
            return subprocess.run(
                prefix + list(arguments), check=True, capture_output=True, text=True,
                env=environment, timeout=proof.COMMAND_TIMEOUT_SECONDS,
            ).stdout.strip()

        setup_git("init", "--quiet", "--template=")
        setup_git("add", "--", ".identity/brief.md")
        setup_git("commit", "--quiet", "--no-verify", "--message", "test: record authoring source")
        revision = setup_git("rev-parse", "HEAD")
        files = [".identity/brief.md"]
        evidence = proof.checkout_revision(self.consumer, revision, files)
        self.assertEqual(evidence["revisionEvidence"], "checkout HEAD verified")
        self.assertTrue(evidence["consumedFilesMatchRevision"])

        source = self.consumer / files[0]
        source.write_bytes(source.read_bytes() + b"\n")
        changed = proof.checkout_revision(self.consumer, revision, files)
        self.assertFalse(changed["consumedFilesMatchRevision"])
        untracked = proof.checkout_revision(self.consumer, revision, [".identity/identity.json"])
        self.assertFalse(untracked["consumedFilesMatchRevision"])
        with self.assertRaisesRegex(proof.ProofError, "does not match"):
            proof.checkout_revision(self.consumer, "b" * 40, files)

    def test_git_timeout_is_bounded_and_sanitized(self) -> None:
        with patch.object(proof.subprocess, "run", side_effect=subprocess.TimeoutExpired(["private/local/path"], 60)) as execute:
            with self.assertRaisesRegex(proof.ProofError, "Git revision comparison exceeded the proof timeout") as failure:
                proof.checkout_revision(self.consumer, "a" * 40, [".identity/brief.md"])
        self.assertEqual(execute.call_args.kwargs["timeout"], proof.COMMAND_TIMEOUT_SECONDS)
        self.assertNotIn("private/local/path", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
