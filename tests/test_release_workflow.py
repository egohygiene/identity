# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Execute the checked-in publication Bash against local command doubles."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "release.yml"


def publication_run_block() -> str:
    """Extract this workflow's literal indented run scalar using only stdlib."""
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    step = "      - name: Create GitHub release from the annotated tag"
    if lines.count(step) != 1:
        raise AssertionError("expected one release publication step")
    start = lines.index(step) + 1
    while lines[start] != "        run: |":
        if lines[start].strip() and not lines[start].startswith("        "):
            raise AssertionError("publication step must have a literal run block")
        start += 1
    block = []
    for line in lines[start + 1:]:
        if line.strip() and not line.startswith("          "):
            break
        block.append(line)
    if not block:
        raise AssertionError("publication run block is empty")
    return textwrap.dedent("\n".join(block))


@unittest.skipUnless(os.name == "posix" and shutil.which("bash"),
                     "publication runs on Linux and this regression requires POSIX Bash")
class ReleaseWorkflowTests(unittest.TestCase):
    def run_publication(self, root: Path, tag: str, *, admission_exit: int = 0):
        commands = root / "bin"
        commands.mkdir()
        scripts = {
            "python3": ('printf "%s\\0" "$@" > "$ADMISSION_ARGUMENTS_FILE"\n'
                        'printf "admission\\n" >> "$CALL_ORDER_FILE"\n'
                        'exit "$ADMISSION_EXIT"\n'),
            "gh": ('printf "%s\\0" "$@" > "$GH_ARGUMENTS_FILE"\n'
                   'printf "gh\\n" >> "$CALL_ORDER_FILE"\n'),
        }
        for command, body in scripts.items():
            executable = commands / command
            executable.write_text("#!/usr/bin/env bash\n" + body, encoding="utf-8")
            executable.chmod(0o755)
        (root / "release-assets").mkdir()
        (root / "release-assets" / "example.tar.gz").write_bytes(b"local test artifact")
        environment = {
            **os.environ, "PATH": str(commands) + os.pathsep + os.environ.get("PATH", ""),
            "GITHUB_REF_NAME": tag, "GITHUB_SHA": "a" * 40,
            "EXPECTED_TAG_OBJECT": "b" * 40, "ADMISSION_EXIT": str(admission_exit),
            "ADMISSION_ARGUMENTS_FILE": str(root / "admission-arguments"),
            "GH_ARGUMENTS_FILE": str(root / "gh-arguments"),
            "CALL_ORDER_FILE": str(root / "call-order"),
        }
        return subprocess.run(
            ["bash", "--noprofile", "--norc", "-c", publication_run_block()],
            cwd=root, env=environment, capture_output=True, text=True, check=False,
        )

    def test_actual_publication_block_classifies_prereleases_without_build_metadata(self) -> None:
        for tag, prerelease in (
            ("v1.0.0", False), ("v1.0.0+linux-x64", False), ("v1.0.0+build.7", False),
            ("v1.0.0-rc.1", True), ("v1.0.0-rc.1+linux-x64", True),
            ("v1.0.0-alpha-beta+build.7", True),
        ):
            with self.subTest(tag=tag), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                completed = self.run_publication(root, tag)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                expected = ["release", "create", tag, "--verify-tag", "--title",
                            f"Identity {tag}", "--generate-notes"]
                if prerelease:
                    expected.append("--prerelease")
                expected.append("release-assets/example.tar.gz")
                self.assertEqual((root / "gh-arguments").read_bytes().split(b"\0")[:-1],
                                 [argument.encode() for argument in expected])
                self.assertEqual((root / "call-order").read_text(), "admission\ngh\n")
                self.assertEqual(
                    (root / "admission-arguments").read_bytes().split(b"\0")[:-1],
                    [argument.encode() for argument in (
                        "scripts/verify_release_admission.py", "--repository-root", ".",
                        "--tag", tag, "--expected-commit", "a" * 40,
                        "--expected-tag-object", "b" * 40,
                    )],
                )

    def test_failed_admission_prevents_publication_in_actual_run_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed = self.run_publication(root, "v1.0.0", admission_exit=7)
            self.assertEqual(completed.returncode, 7, completed.stderr)
            self.assertEqual((root / "call-order").read_text(), "admission\n")
            self.assertFalse((root / "gh-arguments").exists())


if __name__ == "__main__":
    unittest.main()
