# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Transport/extraction controls; real CLI qualification is retained separately."""
from contextlib import redirect_stderr
import errno
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tarfile
import tempfile
import threading
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import qualify_local_install as qualifier


class LocalInstallQualificationTests(unittest.TestCase):
    def _symlink_or_skip(self, link, target, *, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except NotImplementedError:
            self.skipTest("host does not implement symbolic links")
        except OSError as error:
            unsupported = {errno.EPERM, errno.EACCES, errno.ENOSYS,
                           getattr(errno, "EOPNOTSUPP", errno.ENOSYS),
                           getattr(errno, "ENOTSUP", errno.ENOSYS)}
            if error.errno in unsupported or getattr(error, "winerror", None) in {1, 50, 1314}:
                self.skipTest("host filesystem or permissions do not permit test symbolic links")
            raise

    def test_archive_is_deterministic_and_round_trips_exact_bytes(self):
        data = b"candidate executable\n"
        archive = qualifier.candidate_archive(data)
        self.assertEqual(archive, qualifier.candidate_archive(data))
        self.assertEqual(data, qualifier.archive_binary(archive, qualifier.sha256(data)))
        with self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(archive, "0" * 64)

    def test_real_loopback_download_checks_digest_without_environment_proxy(self):
        data = b"actual HTTP bytes\n"
        with qualifier.artifact_server({"/candidate": data}) as server:
            with mock.patch.dict(os.environ, {"HTTP_PROXY": "http://invalid.invalid:9", "http_proxy": "http://invalid.invalid:9", "NO_PROXY": ""}):
                self.assertEqual(data, qualifier.download(server + "/candidate", qualifier.sha256(data)))
            with self.assertRaises(qualifier.QualificationError):
                qualifier.download(server + "/candidate", "0" * 64)
        for url in ["https://127.0.0.1:80/candidate", "http://localhost:80/candidate", "http://127.0.0.1:80/candidate?token=example"]:
            with self.subTest(url=url), self.assertRaises(qualifier.QualificationError):
                qualifier.download(url, qualifier.sha256(data))

    def test_unsafe_names_and_link_or_extension_members_are_refused(self):
        for name in ["../identity", "/identity", "folder/identity", "identity/../identity"]:
            with self.subTest(name=name), self.assertRaises(qualifier.QualificationError):
                qualifier.archive_binary(qualifier.candidate_archive(b"data", name=name), qualifier.sha256(b"data"))
        for kind in [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.DIRTYPE, tarfile.FIFOTYPE, tarfile.XHDTYPE]:
            with self.subTest(kind=kind), self.assertRaises(qualifier.QualificationError):
                qualifier.archive_binary(qualifier.candidate_archive(b"data", kind=kind), qualifier.sha256(b"data"))

    def test_extra_member_and_nonzero_trailing_payload_are_refused(self):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            for name in ["identity", "unexpected.txt"]:
                member = tarfile.TarInfo(name)
                member.mode, member.size = 0o755, 4
                archive.addfile(member, io.BytesIO(b"data"))
        with self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(gzip.compress(buffer.getvalue(), mtime=0), qualifier.sha256(b"data"))
        expanded = bytearray(gzip.decompress(qualifier.candidate_archive(b"data")))
        expanded[-1] = 1
        with self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(gzip.compress(expanded, mtime=0), qualifier.sha256(b"data"))

    def test_corrupt_truncated_and_oversized_archives_fail_before_installation(self):
        original = qualifier.candidate_archive(b"data")
        invalid_deflate = bytes.fromhex("1f8b0800000000000003") + b"\x07" + b"\0" * 8
        for archive in [b"not gzip", original[:10], invalid_deflate]:
            with self.subTest(archive=archive), self.assertRaises(qualifier.QualificationError):
                qualifier.archive_binary(archive, qualifier.sha256(b"data"))
        with mock.patch.object(qualifier, "MAX_TAR", 64), self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(original, qualifier.sha256(b"data"))
        info = tarfile.TarInfo("identity")
        info.mode, info.size = 0o755, qualifier.MAX_BINARY + 1
        malicious = info.tobuf(format=tarfile.USTAR_FORMAT) + b"\0" * 1024
        with self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(gzip.compress(malicious, mtime=0), qualifier.sha256(b"data"))

    def test_new_install_refuses_clobber(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            prefix = work / "space µ=prefix"
            binary = qualifier.install(b"old", prefix)
            self.assertEqual(binary.read_bytes(), b"old")
            with self.assertRaises(qualifier.QualificationError):
                qualifier.install(b"replacement", prefix)
            self.assertEqual(binary.read_bytes(), b"old")

    @unittest.skipUnless(os.name == "posix", "POSIX permission bits are not a Windows file-mode contract")
    def test_new_install_preserves_posix_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = qualifier.install(b"old", Path(directory) / "bin")
            self.assertEqual(stat.S_IMODE(binary.stat().st_mode), 0o755)

    def test_symlink_install_prefix_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            prefix = work / "bin"
            binary = qualifier.install(b"old", prefix)
            link = work / "linked-prefix"
            self._symlink_or_skip(link, prefix, directory=True)
            with self.assertRaises(qualifier.QualificationError):
                qualifier.install(b"replacement", link)
            self.assertEqual(binary.read_bytes(), b"old")

    def test_input_requires_expected_regular_native_elf_bytes(self):
        elf = bytearray(b"\0" * 32)
        elf[:6], elf[18:20] = b"\x7fELF\x02\x01", b"\x3e\x00"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "binary"
            path.write_bytes(elf)
            self.assertEqual(bytes(elf), qualifier.binary_bytes(path, qualifier.sha256(elf)))
            with self.assertRaises(qualifier.QualificationError):
                qualifier.binary_bytes(path, "0" * 64)
            path.write_bytes(b"not a native binary")
            with self.assertRaises(qualifier.QualificationError):
                qualifier.binary_bytes(path, qualifier.sha256(path.read_bytes()))

    def test_symlink_binary_input_is_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "binary"
            path.write_bytes(b"input bytes")
            link = Path(directory) / "link"
            self._symlink_or_skip(link, path)
            with self.assertRaises(qualifier.QualificationError):
                qualifier.binary_bytes(link, qualifier.sha256(path.read_bytes()))

    def test_redirect_is_not_followed_even_to_another_loopback_resource(self):
        requested = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requested.append(self.path)
                self.send_response(302)
                self.send_header("Location", "/payload")
                self.end_headers()
            def log_message(self, *arguments):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with self.assertRaises(qualifier.QualificationError):
                qualifier.download(f"http://127.0.0.1:{server.server_port}/redirect", "0" * 64)
            self.assertEqual(requested, ["/redirect"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def _assert_receipt_refusal(self, work, output, retained):
        argv = []
        for name in ["candidate-binary", "baseline-binary", "consumer-root"]:
            argv += ["--" + name, str(work / name)]
        argv += ["--receipt", str(output)]
        for name in ["candidate-sha256", "baseline-sha256", "candidate-revision", "baseline-revision", "consumer-repository", "consumer-revision"]:
            argv += ["--" + name, "example"]
        stderr = io.StringIO()
        with mock.patch.object(qualifier, "qualify") as run, redirect_stderr(stderr):
            self.assertEqual(qualifier.main(argv), 1)
            run.assert_not_called()
        self.assertNotIn(str(work), stderr.getvalue())
        self.assertEqual(retained.read_bytes(), b"existing receipt\n")

    def test_existing_receipt_refuses_before_running_and_redacts_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            destination = work / "private-receipt"
            destination.write_bytes(b"existing receipt\n")
            self._assert_receipt_refusal(work, destination, destination)

    def test_linked_receipt_refuses_before_running_and_redacts_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            destination = work / "private-receipt"
            destination.write_bytes(b"existing receipt\n")
            linked = work / "linked-receipt"
            self._symlink_or_skip(linked, destination)
            self._assert_receipt_refusal(work, linked, destination)

    def test_successful_initializer_cannot_hide_unrelated_source_deletion(self):
        def mutate(prefix, arguments, consumer, commands, **options):
            if arguments[0] == "init":
                (consumer / ".identity").mkdir()
                (consumer / ".identity/legacy.json").write_bytes(b"legacy source\n")
            if arguments[0] == "v1-init":
                (consumer / "unrelated.txt").unlink(missing_ok=True)
                (consumer / "starter").mkdir(exist_ok=True)
                (consumer / "starter/initialization-report.json").write_text(json.dumps({"status": "incomplete", "sourceValid": False}))
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(qualifier, "invoke", side_effect=mutate):
            with self.assertRaisesRegex(qualifier.QualificationError, "existing or unrelated"):
                qualifier.candidate_cli_checks(Path(directory), Path(directory), [])

    @unittest.skipUnless(os.name == "posix" and Path("/usr/bin/env").is_file() and shutil.which("python3"),
                         "execution fixture requires POSIX shebang dispatch and env/python3")
    def test_installed_command_cannot_change_its_bound_executable(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            prefix = work / "bin"
            program = b"#!/usr/bin/env python3\nfrom pathlib import Path\nPath(__file__).write_bytes(b'changed')\n"
            qualifier.install(program, prefix)
            with self.assertRaisesRegex(qualifier.QualificationError, "changed its selected executable"):
                qualifier.invoke(prefix, [], work, [])


if __name__ == "__main__":
    unittest.main()
