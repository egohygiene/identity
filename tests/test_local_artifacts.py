# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
from contextlib import contextmanager
import hashlib
import errno
import http.server
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock
import urllib.error
import http.client
import queue
import subprocess
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


worker = load("artifact_roundtrip", "local_artifact_roundtrip.py")
builder = load("local_act_builder", "prepare_local_act.py")
observer_module = load("local_artifact_observer", "observe_local_artifacts.py")
preflight = load("local_artifact_preflight", "qualify_local_artifacts.py")


def archive(entries):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as bundle:
        for name, content in entries:
            bundle.writestr(name, content)
    return stream.getvalue()


@contextmanager
def server(data, signed_override=None):
    requests = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            requests.append(("POST", self.path))
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.headers.get("Authorization") != "Bearer fixture-token" or body != {"workflow_run_backend_id": "1", "workflow_job_run_backend_id": "1", "name": "identity-transport-probe"}:
                self.send_error(403)
                return
            url = signed_override or f"http://127.0.0.1:{self.server.server_port}/archive.zip?sig=fixture"
            payload = json.dumps({"signedUrl": url}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            requests.append(("GET", self.path))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(data)

    instance = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        yield instance, requests
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join()


class ArtifactTransportTests(unittest.TestCase):
    def test_caller_refuses_ambient_configuration_before_running_act(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repository = root / "source"
            repository.mkdir()
            with mock.patch.object(preflight.Path, "home", return_value=root), mock.patch.dict(os.environ, {"XDG_CONFIG_HOME": str(root / "config"), "XDG_CONFIG_DIRS": str(root / "system")}):
                preflight.refuse_ambient_act_configuration(repository)
                for target in (root / ".actrc", repository / ".actrc", root / "config/act/actrc", root / "system/act/actrc"):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("--job unauthorized\n")
                    with self.assertRaises(ValueError):
                        preflight.refuse_ambient_act_configuration(repository)
                    target.unlink()

    def setUp(self):
        self.payloads = {"notes.txt": b"nonce-bound text\n", "media/sample.bin": b"\0\xff\x7f"}
        self.expected = {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in self.payloads.items()}
        self.data = archive(self.payloads.items())
        self.digest = hashlib.sha256(self.data).hexdigest()
        self.manifest = {"kind": "identity.local-artifact-fixture/v1", "nonce": "1" * 32, "files": self.expected}

    def environment(self, port):
        return {"ACTIONS_RESULTS_URL": f"http://127.0.0.1:{port}/", "ACTIONS_RUNTIME_TOKEN": "fixture-token", "GITHUB_RUN_ID": "1", "FIXTURE_ARTIFACT_ID": "7", "FIXTURE_ARTIFACT_DIGEST": self.digest}

    def test_real_http_download_preserves_digest_and_exact_zip_inventory(self):
        with server(self.data) as (instance, requests):
            result, downloaded = worker.run(self.manifest, self.environment(instance.server_port))
        self.assertEqual(result["status"], "passed")
        self.assertEqual(downloaded, self.data)
        self.assertEqual(result["files"], self.expected)
        self.assertEqual([r[0] for r in requests], ["POST", "GET"])
        serialized = json.dumps(result)
        self.assertNotIn("fixture-token", serialized)
        self.assertNotIn("sig=", serialized)

    def test_correct_files_cannot_override_actual_uploader_digest(self):
        with server(self.data) as (instance, _):
            env = self.environment(instance.server_port)
            env["FIXTURE_ARTIFACT_DIGEST"] = "0" * 64
            with self.assertRaises(ValueError):
                worker.run(self.manifest, env)

    def test_signed_url_cannot_escape_loopback_origin(self):
        with server(self.data, "https://example.invalid/archive?sig=private") as (instance, requests):
            with self.assertRaises(ValueError):
                worker.run(self.manifest, self.environment(instance.server_port))
        self.assertEqual([r[0] for r in requests], ["POST"])

    def test_matching_archive_hash_does_not_hide_missing_extra_changed_or_unsafe_entries(self):
        cases = [
            [("notes.txt", self.payloads["notes.txt"])],
            [*self.payloads.items(), ("extra.txt", b"extra")],
            [("notes.txt", b"changed"), ("media/sample.bin", self.payloads["media/sample.bin"])],
            [("../notes.txt", b"escape")],
            [("notes.txt", b"a"), ("notes.txt", b"a")],
        ]
        link = zipfile.ZipInfo("notes.txt")
        link.create_system = 3
        link.external_attr = (0o120777 << 16)
        cases.append([(link, b"target")])
        for entries in cases:
            data = archive(entries)
            with self.subTest(entries=str(entries)[:60]), self.assertRaises(ValueError):
                worker.verify_archive(data, self.expected, hashlib.sha256(data).hexdigest())

    def test_metadata_type_and_expanded_budgets_are_enforced(self):
        expected = {"a": {"bytes": True, "sha256": hashlib.sha256(b"x").hexdigest()}}
        data = archive([("a", b"x")])
        with self.assertRaises(ValueError):
            worker.verify_archive(data, expected, hashlib.sha256(data).hexdigest())
        data = archive([("large", b"x" * (worker.MAX_EXPANDED + 1))])
        expected = {"large": {"bytes": worker.MAX_EXPANDED + 1, "sha256": "0" * 64}}
        with self.assertRaises(ValueError):
            worker.verify_archive(data, expected, hashlib.sha256(data).hexdigest())

    def test_missing_actual_uploader_outputs_never_supply_a_pass(self):
        with server(self.data) as (instance, requests):
            for key in ("ACTIONS_RUNTIME_TOKEN", "GITHUB_RUN_ID", "FIXTURE_ARTIFACT_ID"):
                env = self.environment(instance.server_port)
                del env[key]
                with self.subTest(key=key), self.assertRaises(ValueError):
                    worker.run(self.manifest, env)
        self.assertEqual(requests, [])

    @unittest.skipUnless(all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK")), "Local Linux builder requires no-follow/nonblocking file descriptors")
    def test_archive_cache_rejects_wrong_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "archive"
            p.write_bytes(b"archive")
            expected = {"bytes": 7, "sha256": hashlib.sha256(b"archive").hexdigest()}
            self.assertEqual(builder.regular_bytes(p, expected), b"archive")
            p.write_bytes(b"changed")
            with self.assertRaises(ValueError):
                builder.regular_bytes(p, expected)

    @unittest.skipUnless(all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK", "symlink")), "No-follow symbolic-link rejection requires POSIX link support")
    def test_archive_cache_rejects_symbolic_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "archive"
            p.write_bytes(b"archive")
            expected = {"bytes": 7, "sha256": hashlib.sha256(b"archive").hexdigest()}
            alias = Path(tmp) / "alias"
            try:
                alias.symlink_to(p)
            except NotImplementedError:
                self.skipTest("Symbolic links are unavailable on this host")
            except OSError as error:
                if error.errno in {errno.EPERM, errno.EACCES, errno.ENOSYS, errno.ENOTSUP}:
                    self.skipTest("This host does not permit symbolic-link creation")
                raise
            with self.assertRaises(OSError):
                builder.regular_bytes(alias, expected)

    @unittest.skipUnless(all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK", "mkfifo")), "Special-file rejection requires POSIX FIFO support")
    def test_archive_cache_rejects_special_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            expected = {"bytes": 7, "sha256": hashlib.sha256(b"archive").hexdigest()}
            fifo = Path(tmp) / "fifo"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                builder.regular_bytes(fifo, expected)

    def test_descriptor_proof_rejects_every_change_beyond_the_one_typed_field(self):
        def wire(n, data):
            return builder.encode_varint((n << 3) | 2) + builder.encode_varint(len(data)) + data

        name = wire(1, b"CreateArtifactRequest")
        mime = wire(1, b"mime_type") + bytes([24, 6, 32, 1, 40, 11]) + wire(6, b".google.protobuf.StringValue") + wire(10, b"mimeType")
        original = wire(1, b"artifact.proto") + wire(4, name)
        patched = wire(1, b"artifact.proto") + wire(4, name + wire(2, mime))
        builder.prove_typed_mime_delta(original, patched)
        for wrong in [patched.replace(b"artifact.proto", b"modified.proto"), patched.replace(bytes([24, 6]), bytes([24, 7])), patched.replace(b".google.protobuf.StringValue", b".google.protobuf.Int64Value"), wire(1, b"artifact.proto") + wire(4, name + wire(2, mime) + wire(2, mime)), patched[:-1]]:
            with self.subTest(wrong=len(wrong)), self.assertRaises(ValueError):
                builder.prove_typed_mime_delta(original, wrong)

    def test_observer_preserves_backend_reply_and_independently_downloads_full_inventory(self):
        final_body = json.dumps({"workflow_run_backend_id": "1", "workflow_job_run_backend_id": "1", "name": "identity-transport-probe", "hash": "sha256:" + self.digest}).encode()
        response_body = b'{"ok":true,"artifactId":"7"}'
        payload = self.data
        received = []

        class Backend(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"]))
                received.append((self.path, body, self.headers.get("Authorization")))
                if self.path.endswith("/FinalizeArtifact"):
                    data = response_body
                else:
                    data = json.dumps({"signedUrl": "http://" + self.headers["Host"] + observer_module.SERVICE + "DownloadArtifact?sig=fixture"}).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(payload)

        backend = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Backend)
        thread = threading.Thread(target=backend.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                observation = observer_module.ArtifactObserver(backend.server_port, Path(tmp), [Path(tmp)])
                observation.act_pid = os.getpid()
                try:
                    with mock.patch.object(observer_module, "uploader_inputs", return_value=self.expected):
                        connection = http.client.HTTPConnection("127.0.0.1", observation.server.server_port)
                        connection.request("POST", observer_module.SERVICE + "FinalizeArtifact", final_body, {"Authorization": "Bearer fixture-token", "Content-Type": "application/json"})
                        result = connection.getresponse()
                        self.assertEqual(result.status, 200)
                        self.assertEqual(result.read(), response_body)
                        connection.close()
                    self.assertEqual(observation.results[0]["status"], "passed")
                    self.assertEqual(observation.results[0]["archiveSha256"], self.digest)
                    self.assertEqual((Path(tmp) / "downloaded-0.zip").read_bytes(), self.data)
                    self.assertEqual(received[0][1:], (final_body, "Bearer fixture-token"))
                    self.assertNotIn("fixture-token", json.dumps(observation.results))
                    # An observer failure must fail its own proof, without
                    # rewriting the real backend's successful final response.
                    with mock.patch.object(observer_module, "uploader_inputs", side_effect=ValueError("unavailable")):
                        connection = http.client.HTTPConnection("127.0.0.1", observation.server.server_port)
                        connection.request("POST", observer_module.SERVICE + "FinalizeArtifact", final_body, {"Authorization": "Bearer fixture-token"})
                        result = connection.getresponse()
                        self.assertEqual(result.status, 200)
                        self.assertEqual(result.read(), response_body)
                        connection.close()
                    self.assertEqual(observation.results[-1]["status"], "failed")
                finally:
                    observation.close()
        finally:
            backend.shutdown()
            backend.server_close()
            thread.join()

    @unittest.skipUnless(Path("/proc/self/task").is_dir() and shutil.which("node"), "Linux owned-process observation requires Node")
    def test_owned_thread_child_input_capture_is_exact_and_refuses_aliases_or_foreign_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, content in self.payloads.items():
                p = root / "input" / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(content)
            ready = queue.Queue()
            stop = threading.Event()

            def launch():
                process = subprocess.Popen([shutil.which("node"), "-e", "setInterval(()=>{},1000)", observer_module.UPLOADER], cwd=root, env={"PATH": os.environ["PATH"], "INPUT_PATH": "input/"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                ready.put(process)
                stop.wait()
                process.terminate()
                process.wait(timeout=5)

            thread = threading.Thread(target=launch)
            thread.start()
            process = ready.get(timeout=5)
            try:
                self.assertIn(process.pid, observer_module.descendants(os.getpid()))
                self.assertEqual(observer_module.uploader_inputs(os.getpid(), [root]), self.expected)
                with self.assertRaises(ValueError):
                    observer_module.uploader_inputs(os.getpid(), [root / "foreign"])
                (root / "input" / "alias").symlink_to(root / "input/notes.txt")
                with self.assertRaises(ValueError):
                    observer_module.uploader_inputs(os.getpid(), [root])
            finally:
                stop.set()
                thread.join(timeout=10)


if __name__ == "__main__":
    unittest.main()
