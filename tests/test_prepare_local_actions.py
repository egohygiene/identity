"""Actual Git-tree, source-lock and archive-boundary tests for local replay."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prepare_local_actions", ROOT / "scripts/prepare_local_actions.py")
assert SPEC is not None and SPEC.loader is not None
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


@unittest.skipUnless(shutil.which("git"), "Actual Git tree comparison requires Git")
class LocalActionPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "consumer"
        self.root.mkdir()
        self.upstream = self.base / "synthetic-upstream"
        self.upstream.mkdir()
        self.git("init", "--quiet")
        self.git("config", "user.name", "Local qualification fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        (self.upstream / "action.yml").write_text("name: fixture\nruns:\n  using: node24\n  main: run.sh\n")
        (self.upstream / "run.sh").write_text("#!/bin/sh\nexit 0\n")
        (self.upstream / "run.sh").chmod(0o755)
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "Synthetic action fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.tree = self.git("rev-parse", "HEAD^{tree}").strip()
        self.workflow = b"jobs:\n  validate:\n    steps:\n      - uses: fixture/action@" + self.revision.encode() + b"\n"
        self.workflow_path = self.root / ".github/workflows/local.yml"
        self.workflow_path.parent.mkdir(parents=True)
        self.workflow_path.write_bytes(self.workflow)
        self.files = {"action.yml": (0o100644, (self.upstream / "action.yml").read_bytes()),
                      "run.sh": (0o100755, (self.upstream / "run.sh").read_bytes())}
        self.archive = self.tar(self.files)
        self.action = {"repository": "fixture/action", "revision": self.revision, "gitTreeSha1": self.tree,
                       "archiveUrl": f"https://codeload.github.com/fixture/action/tar.gz/{self.revision}",
                       "archiveSha256": hashlib.sha256(self.archive).hexdigest(), "archiveBytes": len(self.archive)}
        self.lock = {"kind": "identity.local-action-mirror-lock/v1", "workflow": ".github/workflows/local.yml",
                     "workflowSha256": hashlib.sha256(self.workflow).hexdigest(), "actions": [self.action]}
        self.lock_path = self.root / "lock.json"
        self.lock_path.write_text(json.dumps(self.lock))
        self.cache = self.base / "archives"
        self.cache.mkdir()
        self.archive_path = self.cache / ("fixture--action--" + self.revision + ".tar.gz")
        self.archive_path.write_bytes(self.archive)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.upstream), *args], text=True, stderr=subprocess.DEVNULL)

    def tar(self, files, extra=None):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode="w:gz") as archive:
            for path, (mode, body) in files.items():
                member = tarfile.TarInfo(f"action-{self.revision}/{path}")
                member.mode, member.size = mode & 0o777, len(body)
                archive.addfile(member, io.BytesIO(body))
            if extra is not None:
                archive.addfile(extra, io.BytesIO(b"x") if extra.isfile() else None)
        return data.getvalue()

    def revised_action(self, data):
        return {**self.action, "archiveSha256": hashlib.sha256(data).hexdigest(), "archiveBytes": len(data)}

    def test_actual_git_tree_and_offline_mirror_are_exact_without_execution(self):
        self.assertEqual(PREPARE.tree_digest(self.files), self.tree)
        before = self.workflow_path.read_bytes(), self.lock_path.read_bytes()
        with patch.object(PREPARE.urllib.request, "urlopen", side_effect=AssertionError("offline must not acquire")):
            receipt = PREPARE.prepare(self.root, self.lock_path, self.base / "prepared", self.cache)
            repeated = PREPARE.prepare(self.root, self.lock_path, self.base / "prepared-again", self.cache)
        self.assertEqual(receipt, repeated)
        mirror = self.base / "prepared" / receipt["mirrors"][0]["directory"]
        for name, (_, body) in self.files.items():
            self.assertEqual((mirror / name).read_bytes(), body)
        self.assertEqual((mirror / "run.sh").stat().st_mode & 0o777, 0o755)
        self.assertEqual(receipt["mirrors"][0]["verifiedGitTree"], self.tree)
        self.assertNotIn(str(self.base), json.dumps(receipt))
        self.assertEqual((self.workflow_path.read_bytes(), self.lock_path.read_bytes()), before)

    def test_mutable_expression_or_nested_action_selector_is_rejected(self):
        for selector in ["fixture/action@main", "fixture/action@v1", "${{ inputs.action }}", "docker://alpine:latest",
                         "fixture/action/subdirectory@" + self.revision]:
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                PREPARE.workflow_actions(("- uses: " + selector).encode())

    def test_missing_extra_or_duplicate_locked_action_is_rejected(self):
        for actions in [[], [self.action, self.action], [{**self.action, "repository": "another/action"}]]:
            lock = {**self.lock, "actions": actions}
            with self.subTest(actions=actions), self.assertRaises(ValueError):
                PREPARE.validate_lock(lock, self.root)

    def test_workflow_drift_and_unsafe_lock_sources_are_rejected(self):
        self.workflow_path.write_bytes(self.workflow + b"# drift\n")
        with self.assertRaisesRegex(ValueError, "Workflow bytes"):
            PREPARE.validate_lock(self.lock, self.root)
        for path in ["../outside", "/outside", "a/./b", "a//b", None, "C:\\outside"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                PREPARE.source_path(self.root, path)

    def test_arbitrary_download_url_digest_or_size_is_rejected(self):
        for changes in [{"archiveUrl": "https://example.invalid/evil"}, {"archiveBytes": True},
                        {"archiveBytes": PREPARE.MAX_ARCHIVE_BYTES + 1}, {"gitTreeSha1": "bad"},
                        {"archiveSha256": "0"}]:
            lock = deepcopy(self.lock)
            lock["actions"][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                PREPARE.validate_lock(lock, self.root)

    def test_archive_checksum_and_size_are_enforced_before_extracting(self):
        for data in [self.archive + b"x", bytes([self.archive[0] ^ 1]) + self.archive[1:]]:
            with self.subTest(size=len(data)), self.assertRaisesRegex(ValueError, "SHA-256"):
                PREPARE.archive_files(data, self.action)

    def test_content_or_executable_mode_tamper_rejects_even_with_new_archive_checksum(self):
        for files in [{**self.files, "run.sh": (0o100755, b"#!/bin/sh\nexit 1\n")},
                      {**self.files, "run.sh": (0o100644, self.files["run.sh"][1])}]:
            data = self.tar(files)
            with self.subTest(files=files), self.assertRaisesRegex(ValueError, "Git tree"):
                PREPARE.archive_files(data, self.revised_action(data))

    def test_traversal_links_special_and_duplicate_members_are_rejected(self):
        bad = []
        for name in [f"action-{self.revision}/../escape", f"action-{self.revision}//escape", "/escape"]:
            entry = tarfile.TarInfo(name)
            entry.size = 1
            bad.append(entry)
        for kind in [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE]:
            entry = tarfile.TarInfo(f"action-{self.revision}/linked")
            entry.type, entry.linkname = kind, "../../escape"
            bad.append(entry)
        duplicate = tarfile.TarInfo(f"action-{self.revision}/run.sh")
        duplicate.size = 1
        bad.append(duplicate)
        collision = tarfile.TarInfo(f"action-{self.revision}/run.sh/nested")
        collision.size = 1
        bad.append(collision)
        for entry in bad:
            data = self.tar(self.files, extra=entry)
            with self.subTest(name=entry.name, kind=entry.type), self.assertRaises(ValueError):
                PREPARE.archive_files(data, self.revised_action(data))
        self.assertFalse((self.base / "escape").exists())

    def test_member_and_expansion_budgets_are_enforced(self):
        for constant in ["MAX_MEMBERS", "MAX_EXTRACTED_BYTES", "MAX_TAR_BYTES"]:
            with self.subTest(constant=constant), patch.object(PREPARE, constant, 1), self.assertRaises(ValueError):
                PREPARE.archive_files(self.archive, self.action)

    def test_source_existing_output_and_linked_archive_are_refused(self):
        for destination in [self.root, self.root / "new-output", self.cache]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                PREPARE.prepare(self.root, self.lock_path, destination, self.cache)
        target = self.base / "saved-archive.tar.gz"
        self.archive_path.rename(target)
        self.archive_path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "linked"):
            PREPARE.acquire(self.action, self.cache)

    def test_duplicate_json_lock_fields_fail_before_output_or_acquisition(self):
        original = self.lock_path.read_text()
        self.lock_path.write_text('{"kind":"shadow",' + original[1:])
        destination = self.base / "duplicate-lock-output"
        with patch.object(PREPARE, "acquire", side_effect=AssertionError("must not acquire")):
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                PREPARE.prepare(self.root, self.lock_path, destination, self.cache)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
