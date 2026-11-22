# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Failure-boundary checks for the Docker qualification evidence reader."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location("qualify_dev_image", Path(__file__).resolve().parents[1] / "scripts/qualify_dev_image.py")
QUALIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUALIFY)


class QualificationBoundaryTests(unittest.TestCase):
    def test_storage_estimate_handles_vfs_boundaries_remote_and_explicit_bypass(self):
        storage = {"Driver": "vfs", "DockerRootDir": "/daemon-data"}
        usage = mock.Mock(free=24 * QUALIFY.GIB)
        with mock.patch.object(QUALIFY.shutil, "disk_usage", return_value=usage) as inspect:
            self.assertEqual(QUALIFY.storage_budget(storage, "unix:///socket", None)["status"], "sufficient-reserve")
            usage.free -= 1
            self.assertEqual(QUALIFY.storage_budget(storage, "unix:///socket", None)["status"], "insufficient")
            self.assertEqual(QUALIFY.storage_budget(storage, "unix:///socket", 1)["status"], "sufficient-reserve")
            usage.free = 8 * QUALIFY.GIB
            self.assertEqual(QUALIFY.storage_budget({**storage, "Driver": "overlay2"}, "unix:///socket", None)["status"], "sufficient-reserve")
            usage.free -= 1
            self.assertEqual(QUALIFY.storage_budget({**storage, "Driver": "overlay2"}, "unix:///socket", None)["status"], "insufficient")
            inspect.reset_mock()
            report = QUALIFY.storage_budget(storage, "ssh://remote", None)
            self.assertEqual(report["status"], "unknown")
            self.assertIsNone(report["available_bytes"])
            self.assertEqual(QUALIFY.storage_budget(storage, "ssh://remote", 0)["status"], "explicitly-bypassed")
            inspect.assert_not_called()
        with mock.patch.object(QUALIFY.shutil, "disk_usage", side_effect=PermissionError):
            self.assertEqual(QUALIFY.storage_budget(storage, "unix:///socket", None)["status"], "unknown")

    def test_insufficient_vfs_budget_writes_failure_receipt_before_pull_or_build(self):
        commands = []

        def docker(arguments, **kwargs):
            commands.append(arguments)
            if arguments[1] == "version":
                output = {"Os": "linux", "Arch": "amd64"}
            elif arguments[1] == "info":
                output = {"Driver": "vfs", "DockerRootDir": "/daemon-data"}
            else:
                self.fail("No pull, build or other mutation is permitted before storage preflight")
            return QUALIFY.subprocess.CompletedProcess(arguments, 0, json.dumps(output))

        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(temporary) / "qualification.json"
            with (mock.patch.object(QUALIFY.subprocess, "run", side_effect=docker),
                  mock.patch.object(QUALIFY, "source_evidence", return_value={}),
                  mock.patch.object(QUALIFY.shutil, "disk_usage", return_value=mock.Mock(free=8 * QUALIFY.GIB)),
                  mock.patch.dict(os.environ, {"DOCKER_HOST": "unix:///socket", "DOCKER_CONTEXT": ""}),
                  mock.patch("sys.argv", ["qualify_dev_image.py", "--receipt", str(receipt)])):
                self.assertEqual(QUALIFY.main(), 1)
            retained = json.loads(receipt.read_text())
            self.assertEqual(retained["status"], "failed")
            self.assertEqual(retained["storage_budget"]["status"], "insufficient")
            self.assertEqual(retained["storage_budget"]["minimum_free_bytes"], 24 * QUALIFY.GIB)
            self.assertNotIn("/daemon-data", receipt.read_text())
            self.assertEqual([command[1] for command in commands], ["version", "info"])

    def test_receipt_cannot_overwrite_source_or_a_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            repository.mkdir()
            source = repository / "Dockerfile"
            source.write_text("existing source\n")
            for destination in (repository, source, repository / "new-receipt.json", root):
                with self.subTest(destination=destination):
                    with self.assertRaises(ValueError):
                        QUALIFY.receipt_destination(destination, repository)
            outside = root / "receipt.json"
            self.assertEqual(QUALIFY.receipt_destination(outside, repository), outside.resolve())
            if os.name == "posix":
                alias = root / "receipt-link.json"
                alias.symlink_to(source)
                with self.assertRaises(ValueError):
                    QUALIFY.receipt_destination(alias, repository)
            self.assertEqual(source.read_text(), "existing source\n")

    def test_mutable_or_ambiguous_default_cannot_be_qualified(self):
        with tempfile.TemporaryDirectory() as temporary:
            dockerfile = Path(temporary) / "Dockerfile"
            for contents in (
                "ARG BASE_IMAGE=node:24-bookworm\n",
                "ARG BASE_IMAGE=node@sha256:abc\n",
                "ARG BASE_IMAGE=node@sha256:" + "a" * 64 + "\nARG BASE_IMAGE=other\n",
            ):
                with self.subTest(contents=contents):
                    dockerfile.write_text(contents)
                    with self.assertRaises(ValueError):
                        QUALIFY.default_base(dockerfile)
            expected = "docker.io/library/node:24-bookworm@sha256:" + "a" * 64
            dockerfile.write_text("ARG BASE_IMAGE=" + expected + "\nFROM ${BASE_IMAGE}\n")
            self.assertEqual(QUALIFY.default_base(dockerfile), expected)

    def test_inherited_user_command_and_entrypoint_are_required(self):
        base = {"os": "linux", "architecture": "amd64", "user": "1000:1000", "entrypoint": ["base-entrypoint"], "cmd": ["node"]}
        QUALIFY.verify_inheritance(base, dict(base))
        for key, value in (("user", ""), ("entrypoint", None), ("cmd", ["bash"]), ("architecture", "arm64")):
            with self.subTest(key=key):
                changed = dict(base, **{key: value})
                with self.assertRaises(RuntimeError):
                    QUALIFY.verify_inheritance(base, changed)

    def test_ambiguous_failed_or_wrong_platform_container_receipts_fail(self):
        valid = QUALIFY.CONTAINER_MARKER + json.dumps({"status": "passed", "platform": "linux/amd64"})
        self.assertEqual(QUALIFY.container_receipt("ordinary logs\n" + valid)["status"], "passed")
        for output in ("ordinary logs", valid + "\n" + valid, valid.replace("passed", "failed"), valid.replace("amd64", "arm64")):
            with self.subTest(output=output):
                with self.assertRaises(RuntimeError):
                    QUALIFY.container_receipt(output)

    def test_stale_registry_or_wrong_pulled_config_cannot_be_qualified(self):
        reference = "node:24-bookworm@sha256:" + "a" * 64
        identity = {"id": "sha256:" + "b" * 64, "os": "linux", "architecture": "amd64", "user": "", "entrypoint": ["docker-entrypoint.sh"], "cmd": ["node"]}
        registry = {"default_reference": reference, "qualified_platform_candidate": "linux/amd64", "image_config": {**identity, "digest": identity["id"]}}
        QUALIFY.verify_registry_binding(reference, identity, registry)
        with self.assertRaises(RuntimeError):
            QUALIFY.verify_registry_binding(reference + "0", identity, registry)
        with self.assertRaises(RuntimeError):
            QUALIFY.verify_registry_binding(reference, {**identity, "id": "sha256:" + "c" * 64}, registry)


if __name__ == "__main__":
    unittest.main()
