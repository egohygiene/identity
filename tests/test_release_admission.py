# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Exercise release admission against disposable, actual local Git remotes."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ADMISSION = Path(__file__).resolve().parents[1] / "scripts" / "verify_release_admission.py"


class ReleaseAdmissionTests(unittest.TestCase):
    def git(self, root: Path, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments], capture_output=True, text=True, check=True,
        )
        return completed.stdout.strip()

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.remote = self.root / "origin.git"
        self.consumer = self.root / "consumer"
        self.git(self.source, "init", "--initial-branch=main")
        for name, value in (("user.email", "release-test@example.invalid"),
                            ("user.name", "Release admission test"),
                            ("commit.gpgsign", "false"), ("tag.gpgsign", "false"),
                            ("core.autocrlf", "false")):
            self.git(self.source, "config", name, value)
        (self.source / "renderer").mkdir()
        self.version = "1.0.0-rc.1"
        self.tag = f"v{self.version}"
        self.write_versions(self.version)
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "--message", "release source")
        self.commit = self.git(self.source, "rev-parse", "HEAD")
        self.git(self.source, "tag", "--annotate", self.tag, "--message", "candidate")
        self.tag_object = self.git(self.source, "rev-parse", f"refs/tags/{self.tag}")
        self.git(self.root, "clone", "--bare", str(self.source), str(self.remote))
        self.git(self.root, "clone", str(self.remote), str(self.consumer))
        self.git(self.consumer, "config", "core.autocrlf", "false")

    def write_versions(self, version: str) -> None:
        (self.source / "Cargo.toml").write_text(
            f'[package]\nname = "identity"\nversion = "{version}"\n', encoding="utf-8",
        )
        (self.source / "renderer" / "package.json").write_text(
            json.dumps({"version": version}) + "\n", encoding="utf-8",
        )

    def admit(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ADMISSION), "--repository-root", str(self.consumer),
             "--tag", self.tag, "--expected-commit", self.commit, *arguments],
            capture_output=True, text=True, check=False,
        )

    def assert_rejected(self, completed: subprocess.CompletedProcess[str], message: str) -> None:
        self.assertEqual(completed.returncode, 1, completed.stdout)
        self.assertIn(message, completed.stderr)
        self.assertEqual(completed.stdout, "")

    def test_annotated_candidate_emits_selected_identity_without_updating_local_refs(self) -> None:
        before = self.git(self.consumer, "show-ref")
        output = self.root / "github-output"
        completed = self.admit("--github-output", str(output))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout), {
            "tag": self.tag, "tag_object_sha": self.tag_object,
            "commit_sha": self.commit, "main_sha": self.commit, "version": self.version,
        })
        self.assertEqual(output.read_text(), f"tag_object_sha={self.tag_object}\n")
        self.assertEqual(self.git(self.consumer, "show-ref"), before)

    def test_matching_stable_version_is_admitted(self) -> None:
        self.write_versions("1.0.0")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "--message", "stable version")
        self.commit = self.git(self.source, "rev-parse", "HEAD")
        self.tag = "v1.0.0"
        self.git(self.source, "tag", "--annotate", self.tag, "--message", "stable")
        self.git(self.source, "push", str(self.remote), "main", f"refs/tags/{self.tag}")
        self.git(self.consumer, "pull", "--ff-only")
        completed = self.admit()
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_lightweight_tag_is_rejected_even_when_commit_matches(self) -> None:
        self.git(self.source, "tag", "--delete", self.tag)
        self.git(self.source, "tag", self.tag)
        self.git(self.source, "push", "--force", str(self.remote), f"refs/tags/{self.tag}")
        self.assert_rejected(self.admit(), "annotated release tag")

    def test_tag_commit_must_match_event_commit(self) -> None:
        (self.source / "extra.txt").write_text("new main source\n", encoding="utf-8")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "--message", "advance main")
        self.commit = self.git(self.source, "rev-parse", "HEAD")
        self.git(self.source, "push", str(self.remote), "main")
        self.git(self.consumer, "pull", "--ff-only")
        self.assert_rejected(self.admit(), "expected release commit")

    def test_release_commit_may_be_an_ancestor_of_current_remote_main(self) -> None:
        (self.source / "extra.txt").write_text("later main source\n", encoding="utf-8")
        self.git(self.source, "add", ".")
        self.git(self.source, "commit", "--message", "advance main")
        self.git(self.source, "push", str(self.remote), "main")
        before = self.git(self.consumer, "show-ref")
        completed = self.admit()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotEqual(json.loads(completed.stdout)["main_sha"], self.commit)
        self.assertEqual(self.git(self.consumer, "show-ref"), before)

    def test_annotation_must_name_the_actual_remote_tag(self) -> None:
        self.git(self.source, "tag", "--annotate", "different-name", "--message", "other tag")
        other = self.git(self.source, "rev-parse", "refs/tags/different-name")
        self.git(self.source, "push", "--force", str(self.remote), f"{other}:refs/tags/{self.tag}")
        self.assert_rejected(self.admit(), "annotated tag name and direct commit")

    def test_version_mismatch_is_rejected(self) -> None:
        self.tag = "v2.0.0"
        self.assert_rejected(self.admit(), "versions must match")

    def test_different_checkout_is_rejected(self) -> None:
        self.assert_rejected(self.admit("--expected-commit", "0" * 40), "checkout HEAD")

    def test_uncommitted_source_change_is_rejected(self) -> None:
        with (self.consumer / "Cargo.toml").open("a", encoding="utf-8") as source:
            source.write("# changed after checkout\n")
        self.assert_rejected(self.admit(), "'diff' failed")

    def test_commit_off_remote_main_is_rejected(self) -> None:
        self.git(self.source, "checkout", "--orphan", "other-main")
        self.git(self.source, "commit", "--message", "unrelated main history")
        self.git(self.source, "push", "--force", str(self.remote), "HEAD:refs/heads/main")
        self.assert_rejected(self.admit(), "'merge-base' failed")

    def test_tag_replacement_after_build_is_rejected_without_trusting_stale_local_tag(self) -> None:
        completed = self.admit()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        selected = json.loads(completed.stdout)["tag_object_sha"]
        self.git(self.source, "tag", "--force", "--annotate", self.tag,
                 "--message", "replacement annotation, same commit")
        self.git(self.source, "push", "--force", str(self.remote), f"refs/tags/{self.tag}")
        self.assertEqual(self.git(self.consumer, "rev-parse", self.tag), selected)
        output = self.root / "rejected-github-output"
        self.assert_rejected(
            self.admit("--expected-tag-object", selected, "--github-output", str(output)),
            "changed since packaging admission",
        )
        self.assertFalse(output.exists())

    def test_deleted_remote_tag_is_rejected(self) -> None:
        self.git(self.source, "push", str(self.remote), f":refs/tags/{self.tag}")
        self.assert_rejected(self.admit(), "remote must advertise")

    def test_unknown_remote_fails_closed(self) -> None:
        self.assert_rejected(self.admit("--remote", "does-not-exist"), "'ls-remote' failed")

    def test_unreadable_remote_fails_closed(self) -> None:
        self.git(self.consumer, "remote", "set-url", "origin", str(self.root / "missing.git"))
        self.assert_rejected(self.admit(), "'ls-remote' failed")


if __name__ == "__main__":
    unittest.main()
