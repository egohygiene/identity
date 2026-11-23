# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Transport/extraction controls; real CLI qualification is retained separately."""
from contextlib import redirect_stderr
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import os
from pathlib import Path
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
        for archive in [b"not gzip", original[:10]]:
            with self.subTest(archive=archive), self.assertRaises(qualifier.QualificationError):
                qualifier.archive_binary(archive, qualifier.sha256(b"data"))
        with mock.patch.object(qualifier, "MAX_TAR", 64), self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(original, qualifier.sha256(b"data"))
        info = tarfile.TarInfo("identity")
        info.mode, info.size = 0o755, qualifier.MAX_BINARY + 1
        malicious = info.tobuf(format=tarfile.USTAR_FORMAT) + b"\0" * 1024
        with self.assertRaises(qualifier.QualificationError):
            qualifier.archive_binary(gzip.compress(malicious, mtime=0), qualifier.sha256(b"data"))

    def test_new_install_preserves_mode_and_refuses_clobber_or_symlink_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            prefix = work / "space µ=prefix"
            binary = qualifier.install(b"old", prefix)
            self.assertEqual(binary.read_bytes(), b"old")
            self.assertEqual(stat.S_IMODE(binary.stat().st_mode), 0o755)
            with self.assertRaises(qualifier.QualificationError):
                qualifier.install(b"replacement", prefix)
            self.assertEqual(binary.read_bytes(), b"old")
            link = work / "linked-prefix"
            link.symlink_to(prefix, target_is_directory=True)
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
            link = Path(directory) / "link"
            link.symlink_to(path)
            with self.assertRaises(qualifier.QualificationError):
                qualifier.binary_bytes(link, qualifier.sha256(elf))
            path.write_bytes(b"not a native binary")
            with self.assertRaises(qualifier.QualificationError):
                qualifier.binary_bytes(path, qualifier.sha256(path.read_bytes()))

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

    def test_existing_or_linked_receipt_refuses_before_running_and_redacts_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            destination = work / "private-receipt"
            destination.write_bytes(b"existing receipt\n")
            linked = work / "linked-receipt"
            linked.symlink_to(destination)
            for output in [destination, linked]:
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
                self.assertEqual(destination.read_bytes(), b"existing receipt\n")


if __name__ == "__main__":
    unittest.main()
