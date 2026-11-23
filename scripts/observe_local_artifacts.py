#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Read-only loopback artifact observer for an unchanged actual act workflow.

The forwarding observer preserves backend responses. At successful finalize,
it verifies the actual backend download while the uploader/workspace still
exist. Tokens and signed URLs remain only in process memory, never receipts.
"""
from __future__ import annotations

import hashlib
import http.client
import http.server
import importlib.util
import json
import os
from pathlib import Path
import re
import threading
import urllib.parse
import urllib.request
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("artifact_worker", ROOT / "scripts/local_artifact_roundtrip.py")
WORKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKER)
MAX_ARCHIVE = 128 * 1024 * 1024
MAX_EXPANDED = 512 * 1024 * 1024
MAX_FILES = 4096
UPLOADER = "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a/dist/upload/index.js"
SERVICE = "/twirp/github.actions.results.api.v1.ArtifactService/"


def descendants(pid: int) -> list[int]:
    # This kernel can omit /proc/PID/task/TID/children. Read only bounded
    # PID/PPID metadata to establish ownership; inspect command/env/cwd only
    # after a process is proven to descend from the exact launched act PID.
    parents = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        if len(parents) >= 8192:
            raise ValueError("Process metadata inventory exceeds its bound")
        try:
            fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
            parents[int(entry.name)] = int(fields[1])
        except (FileNotFoundError, PermissionError, IndexError, ValueError):
            continue
    result = {pid}
    while True:
        added = {child for child, parent in parents.items() if parent in result} - result
        if not added:
            return sorted(result)
        result.update(added)
        if len(result) > 512:
            raise ValueError("Owned process inventory exceeds its bound")


def uploader_inputs(act_pid: int, allowed_roots: list[Path]) -> dict:
    candidates = []
    for pid in descendants(act_pid):
        try:
            args = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
            executable = Path(os.readlink(f"/proc/{pid}/exe")).name
            if executable != "node" or not any(UPLOADER.encode() in value for value in args):
                continue
            environment = dict(v.split(b"=", 1) for v in Path(f"/proc/{pid}/environ").read_bytes().split(b"\0") if b"=" in v)
            cwd = Path(os.readlink(f"/proc/{pid}/cwd")).resolve()
            candidates.append((cwd, environment))
        except FileNotFoundError:
            continue
    if len(candidates) != 1:
        raise ValueError("Cannot identify the one owned pinned uploader process")
    cwd, environment = candidates[0]
    roots = [p.resolve() for p in allowed_roots]

    def contained(path: Path) -> bool:
        return any(path == root or root in path.parents for root in roots)

    if not contained(cwd):
        raise ValueError("Uploader workspace is outside caller-owned roots")
    patterns = environment.get(b"INPUT_PATH", b"").decode().splitlines()
    if not 1 <= len(patterns) <= 16:
        raise ValueError("Unexpected original uploader input selection")
    include_hidden = environment.get(b"INPUT_INCLUDE-HIDDEN-FILES", b"false").strip().lower() == b"true"
    paths = []
    search_roots = []
    for raw in patterns:
        raw = raw.strip()
        if not raw or any(ch in raw for ch in "*?[]!"):
            raise ValueError("This observer supports the original literal directory selections only")
        path = Path(raw) if Path(raw).is_absolute() else cwd / raw
        if path.is_symlink():
            raise ValueError("Uploader input is an alias")
        path = path.resolve()
        if not contained(path):
            raise ValueError("Uploader input escaped its caller-owned roots")
        search_roots.append(path if path.is_dir() else path.parent)
        if not path.exists():
            continue
        selected = [path] if path.is_file() else list(path.rglob("*"))
        for item in selected:
            if item.is_symlink():
                raise ValueError("Uploader inventory contains a source link")
            if not item.is_file():
                continue
            relative = item.relative_to(path) if path.is_dir() else Path(item.name)
            if not include_hidden and any(part.startswith(".") for part in relative.parts):
                continue
            paths.append(item)
    common = Path(os.path.commonpath(search_roots))
    files = {}
    total = 0
    for path in sorted(set(paths)):
        if len(files) >= MAX_FILES:
            raise ValueError("Uploader inventory exceeds its file budget")
        size = path.stat().st_size
        total += size
        if total > MAX_EXPANDED:
            raise ValueError("Uploader inventory exceeds its byte budget")
        data = path.read_bytes()
        if len(data) != size:
            raise ValueError("Uploader source changed while hashing")
        files[path.relative_to(common).as_posix()] = {"bytes": size, "sha256": hashlib.sha256(data).hexdigest()}
    if not files:
        raise ValueError("Actual original uploader input inventory is empty")
    return files


class ArtifactObserver:
    def __init__(self, backend_port: int, output: Path, allowed_roots: list[Path]):
        self.backend_port = backend_port
        self.output = output
        self.allowed_roots = allowed_roots
        self.act_pid = None
        self.results = []
        owner = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def forward(self):
                connection = None
                try:
                    parsed = urllib.parse.urlsplit(self.path)
                    endpoint = parsed.path.removeprefix(SERVICE)
                    if not parsed.path.startswith(SERVICE) or endpoint not in {"CreateArtifact", "FinalizeArtifact", "GetSignedArtifactURL", "ListArtifacts", "DeleteArtifact", "UploadArtifact", "DownloadArtifact"} or parsed.scheme or parsed.netloc or self.headers.get("Host") != urllib.parse.urlsplit(owner.url).netloc:
                        self.send_error(400)
                        return
                    length = int(self.headers.get("Content-Length", "0"))
                    if self.headers.get("Transfer-Encoding") or not 0 <= length <= MAX_ARCHIVE:
                        self.send_error(413)
                        return
                    body = self.rfile.read(length)
                    headers = {k: v for k, v in self.headers.items() if k.lower() not in {"connection", "transfer-encoding"}}
                    connection = http.client.HTTPConnection("127.0.0.1", owner.backend_port, timeout=120)
                    connection.request(self.command, self.path, body=body, headers=headers)
                    response = connection.getresponse()
                    data = response.read(MAX_ARCHIVE + 1)
                    if len(data) > MAX_ARCHIVE:
                        self.send_error(413)
                        return
                    if self.command == "POST" and parsed.path == SERVICE + "FinalizeArtifact" and response.status == 200:
                        # Observe before returning the unchanged response so the
                        # uploader/workspace and actual backend are still alive.
                        owner.finalized(body, self.headers.get("Authorization", ""))
                    self.send_response(response.status)
                    for key, value in response.getheaders():
                        if key.lower() not in {"connection", "transfer-encoding", "content-length"}:
                            self.send_header(key, value)
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                except (OSError, ValueError, http.client.HTTPException):
                    self.send_error(502)
                finally:
                    if connection is not None:
                        connection.close()

            do_POST = forward
            do_PUT = forward
            do_GET = forward
            do_HEAD = forward

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.server.server_port}/"

    def finalized(self, body: bytes, authorization: str) -> None:
        record = {"status": "failed", "runtimeTokenRecorded": False, "signedUrlRecorded": False}
        try:
            request = json.loads(body, object_pairs_hook=WORKER.unique_object)
            digest = request.get("hash", "")
            if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", digest) or not authorization.startswith("Bearer "):
                raise ValueError("Finalization lacks actual digest/authentication")
            if self.act_pid is None:
                raise ValueError("Owned actual act process is unavailable")
            expected = uploader_inputs(self.act_pid, self.allowed_roots)
            data = json.dumps({key: request[key] for key in ("workflow_run_backend_id", "workflow_job_run_backend_id", "name")}).encode()
            api = urllib.request.Request(self.url.rstrip("/") + SERVICE + "GetSignedArtifactURL", data=data, headers={"Authorization": authorization, "Content-Type": "application/json"})
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), WORKER.NoRedirect())
            signed = json.loads(WORKER.bounded_request(opener, api, 65536), object_pairs_hook=WORKER.unique_object)
            signed_url = signed.get("signedUrl", signed.get("signed_url"))
            if WORKER.local_origin(signed_url) != WORKER.local_origin(self.url):
                raise ValueError("Actual backend returned a different origin")
            archive = WORKER.bounded_request(opener, urllib.request.Request(signed_url), MAX_ARCHIVE)
            actual = WORKER.verify_archive(archive, expected, digest[7:], max_archive=MAX_ARCHIVE, max_expanded=MAX_EXPANDED, max_files=MAX_FILES, max_members=MAX_FILES * 2)
            destination = self.output / ("downloaded-" + str(len(self.results)) + ".zip")
            with destination.open("xb") as stream:
                stream.write(archive)
            destination.chmod(0o600)
            record.update({"status": "passed", "archiveBytes": len(archive), "archiveSha256": hashlib.sha256(archive).hexdigest(), "actualFinalizeSha256": digest[7:], "files": actual, "fileCount": len(actual), "downloadContext": "authenticated actual backend API and signed loopback download before unmodified workflow cleanup", "rawArchiveRetention": "task-local private file; hash/inventory are public-safe evidence"})
        except (OSError, ValueError, TypeError, KeyError, RuntimeError, http.client.HTTPException, zipfile.BadZipFile, zlib.error):
            record["failure"] = "Actual full artifact download/inventory could not be established; backend response was preserved."
        self.results.append(record)

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
