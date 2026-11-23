#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Qualify local Linux source-candidate transport/install in disposable prefixes.

This is a development proof, not an installer or a released-artifact verifier.
It packages explicitly supplied trusted binaries, serves them only on loopback,
checks downloaded bytes before a bounded single-file extraction, and exercises
the installed CLI through PATH. Consumer work happens only in disposable copies.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import gzip
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import zlib

import verify_consumer_authoring as authoring


REPOSITORY = Path(__file__).resolve().parents[1]
MAX_BINARY = 128 * 1024 * 1024
MAX_ARCHIVE = MAX_BINARY + 1024 * 1024
MAX_TAR = MAX_BINARY + 10240
HEX = re.compile(r"[0-9a-f]{64}")
REVISION = re.compile(r"[0-9a-f]{40}")


class QualificationError(ValueError):
    """Public proof failures must not disclose private paths or environment."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def binary_bytes(path: Path, expected: str) -> bytes:
    if not HEX.fullmatch(expected):
        raise QualificationError("binary digest must be a full lowercase SHA256")
    try:
        if not stat.S_ISREG(path.lstat().st_mode) or path.stat().st_size > MAX_BINARY:
            raise QualificationError("supplied binary must be a bounded regular file")
        with path.open("rb") as stream:
            data = stream.read(MAX_BINARY + 1)
    except OSError as error:
        raise QualificationError("supplied binary cannot be read") from error
    if not data or len(data) > MAX_BINARY or sha256(data) != expected:
        raise QualificationError("supplied binary does not match its expected bytes")
    # This checkpoint is deliberately native Linux/amd64, not cross-platform.
    if len(data) < 20 or data[:6] != b"\x7fELF\x02\x01" or data[18:20] != b"\x3e\x00":
        raise QualificationError("supplied binary is not a Linux amd64 ELF64 candidate")
    return data


def candidate_archive(data: bytes, *, name: str = "identity", kind: bytes = tarfile.REGTYPE) -> bytes:
    tar = io.BytesIO()
    with tarfile.open(fileobj=tar, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        info = tarfile.TarInfo(name)
        info.type = kind
        info.mode, info.uid, info.gid, info.mtime = 0o755, 0, 0, 0
        info.size = len(data) if kind == tarfile.REGTYPE else 0
        if kind in (tarfile.SYMTYPE, tarfile.LNKTYPE):
            info.linkname = "outside-sentinel"
        archive.addfile(info, io.BytesIO(data) if info.size else None)
    compressed = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed, filename="", mode="wb", mtime=0) as stream:
        stream.write(tar.getvalue())
    return compressed.getvalue()


def archive_binary(archive: bytes, expected: str) -> bytes:
    """Read only the proof's one-file USTAR format; never call extractall."""
    if not HEX.fullmatch(expected) or not archive or len(archive) > MAX_ARCHIVE:
        raise QualificationError("archive metadata or size is invalid")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(archive)) as stream:
            expanded = stream.read(MAX_TAR + 1)
    except (OSError, EOFError, zlib.error) as error:
        raise QualificationError("archive compression is invalid") from error
    if len(expanded) < 1536 or len(expanded) > MAX_TAR or len(expanded) % 512:
        raise QualificationError("expanded archive is outside its bounded format")
    try:
        member = tarfile.TarInfo.frombuf(expanded[:512], "utf-8", "strict")
    except (tarfile.TarError, UnicodeError, ValueError) as error:
        raise QualificationError("archive header is invalid") from error
    if (expanded[156:157] not in (b"0", b"\0") or expanded[257:263] != b"ustar\0"
            or not member.isfile() or member.name != "identity" or member.linkname
            or member.mode != 0o755 or member.uid != 0 or member.gid != 0 or member.mtime != 0
            or not 0 < member.size <= MAX_BINARY):
        raise QualificationError("archive must contain one regular identity executable")
    end = 512 + member.size
    if end + 1024 > len(expanded) or any(expanded[end:]):
        raise QualificationError("archive has extra members, data or incomplete padding")
    data = expanded[512:end]
    if sha256(data) != expected:
        raise QualificationError("extracted executable digest differs")
    return data


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        raise QualificationError("local artifact redirects are unsupported")


def download(url: str, expected: str) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or not parsed.port
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or not HEX.fullmatch(expected)):
        raise QualificationError("download must select a checksum-pinned loopback artifact")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(url, timeout=15) as response:
            lengths = response.headers.get_all("Content-Length", [])
            if len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].isdigit():
                raise QualificationError("local artifact length is missing or ambiguous")
            length = int(lengths[0])
            if not 0 < length <= MAX_ARCHIVE:
                raise QualificationError("local artifact length exceeds the proof budget")
            data = response.read(MAX_ARCHIVE + 1)
    except (OSError, urllib.error.URLError, ValueError) as error:
        if isinstance(error, QualificationError):
            raise
        raise QualificationError("local artifact download failed") from error
    if len(data) != length or sha256(data) != expected:
        raise QualificationError("downloaded artifact bytes do not match the expected digest")
    return data


@contextmanager
def artifact_server(artifacts: dict[str, bytes]):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            data = artifacts.get(self.path)
            if data is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/gzip")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *arguments):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        if thread.is_alive():
            raise QualificationError("local artifact server did not terminate")


def install(data: bytes, prefix: Path) -> Path:
    """A new private prefix only; never overwrite a user install or follow links."""
    try:
        prefix.mkdir(mode=0o700)
    except OSError as error:
        raise QualificationError("installation prefix must be new") from error
    target = prefix / "identity"
    try:
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o755)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        target.chmod(0o755)
        if sha256(target.read_bytes()) != sha256(data):
            raise QualificationError("installed executable differs from extracted bytes")
    except OSError as error:
        raise QualificationError("new isolated installation failed") from error
    return target


def expected_refusal(operation) -> None:
    try:
        operation()
    except QualificationError:
        return
    raise QualificationError("a deliberate negative control unexpectedly passed")


def invoke(prefix: Path, arguments: list[str], consumer: Path, commands: list[dict], *, missing_python: bool = False, expected: int = 0) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment["PATH"] = str(prefix) + os.pathsep + environment.get("PATH", "")
    environment["IDENTITY_PYTHON"] = str(consumer / "missing-python") if missing_python else sys.executable
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.pop("PYTHONPATH", None)
    environment["PYTHONSAFEPATH"] = "1"
    if shutil.which("identity", path=environment["PATH"]) != str(prefix / "identity"):
        raise QualificationError("PATH did not select the isolated installation")
    selected_digest = sha256((prefix / "identity").read_bytes())
    try:
        result = subprocess.run(["identity", *arguments], cwd=consumer, env=environment, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise QualificationError("installed command could not complete") from error
    if sha256((prefix / "identity").read_bytes()) != selected_digest:
        raise QualificationError("installed command changed its selected executable")
    if result.returncode != expected:
        raise QualificationError("installed command returned an unexpected exit status")
    commands.append({"arguments": ["identity", *[part.replace(str(consumer), "<consumer>") for part in arguments]],
                     "exitCode": result.returncode, "pythonUnavailable": missing_python, "installedBinarySha256": selected_digest,
                     "stdoutSha256": sha256(result.stdout), "stderrSha256": sha256(result.stderr)})
    return result


def generated_state(binary_prefix: Path, consumer: Path, commands: list[dict]) -> dict:
    source = authoring.inventory(consumer / ".identity")
    invoke(binary_prefix, ["v1-generate", "--repository-root", str(consumer)], consumer, commands)
    invoke(binary_prefix, ["v1-verify", "--repository-root", str(consumer)], consumer, commands)
    if authoring.inventory(consumer / ".identity") != source:
        raise QualificationError("installed generation changed canonical source")
    return authoring.inventory(consumer / "assets/identity")


def candidate_cli_checks(prefix: Path, work: Path, commands: list[dict]) -> dict:
    consumer = work / "candidate-init"
    consumer.mkdir()
    (consumer / "request.json").write_text('{"schema":"identity.initialization-request/v1"}\n')
    (consumer / "unrelated.txt").write_bytes(b"isolated install sentinel\n")
    (consumer / "json.py").write_text("raise RuntimeError('consumer module must not execute')\n")
    invoke(prefix, ["init", "--repository-root", str(consumer), "--project-id", "install-legacy", "--display-name", "Install Legacy"], consumer, commands)
    legacy = authoring.inventory(consumer / ".identity")
    invoke(prefix, ["validate", "--repository-root", str(consumer)], consumer, commands)
    before_init = authoring.inventory(consumer)
    invoke(prefix, ["v1-init", "--repository-root", str(consumer), "--request", "request.json", "--output-directory", "starter"], consumer, commands)
    outside_candidate = {path: value for path, value in authoring.inventory(consumer).items()
                         if path != "starter" and not path.startswith("starter/")}
    if outside_candidate != before_init:
        raise QualificationError("candidate initialization changed existing or unrelated source")
    report = json.loads((consumer / "starter/initialization-report.json").read_text())
    if report.get("status") != "incomplete" or report.get("sourceValid") is not False:
        raise QualificationError("partial initialization was not honestly incomplete")
    preserved = authoring.inventory(consumer)
    for destination, missing in [("starter", False), ("missing-runtime", True)]:
        invoke(prefix, ["v1-init", "--repository-root", str(consumer), "--request", "request.json", "--output-directory", destination], consumer, commands, missing_python=missing, expected=1)
        if authoring.inventory(consumer) != preserved:
            raise QualificationError("refused initialization changed existing files")
    if authoring.inventory(consumer / ".identity") != legacy or (consumer / "assets").exists():
        raise QualificationError("candidate initialization changed legacy source or generated output")
    return {"v0Preserved": True, "unrelatedSourcePreserved": True, "v1CandidateStatus": "incomplete", "existingDestinationRefusedWithoutMutation": True,
            "missingPythonRefusedWithoutMutation": True, "consumerPythonModulesNotExecuted": True}


def qualify(arguments: argparse.Namespace) -> dict:
    if sys.platform != "linux" or platform.machine().lower() not in {"x86_64", "amd64"}:
        raise QualificationError("this proof requires native Linux amd64")
    for value in [arguments.candidate_revision, arguments.baseline_revision, arguments.consumer_revision]:
        if not REVISION.fullmatch(value):
            raise QualificationError("source selections must be full lowercase Git revisions")
    candidate = binary_bytes(arguments.candidate_binary, arguments.candidate_sha256)
    baseline = binary_bytes(arguments.baseline_binary, arguments.baseline_sha256)
    if candidate == baseline:
        raise QualificationError("replacement requires two distinct actual source-candidate binaries")
    root = arguments.consumer_root.resolve(strict=True)
    original = authoring.inventory(root, excluded_names=frozenset({".git"}))
    archives = {"/candidate.tar.gz": candidate_archive(candidate), "/baseline.tar.gz": candidate_archive(baseline),
                "/unsafe.tar.gz": candidate_archive(b"negative archive", name="../escape")}
    artifact_rows = []
    commands: list[dict] = []
    try:
        with tempfile.TemporaryDirectory(prefix="identity-local-install-") as directory, artifact_server(archives) as url:
            work = Path(directory)
            prefixes = {}
            for label, binary, expected in [("baseline", baseline, arguments.baseline_sha256), ("candidate", candidate, arguments.candidate_sha256)]:
                archive = archives[f"/{label}.tar.gz"]
                received = download(f"{url}/{label}.tar.gz", sha256(archive))
                prefixes[label] = work / f"{label} install µ"
                installed = install(archive_binary(received, expected), prefixes[label])
                artifact_rows.append({"selection": label, "archiveSha256": sha256(archive), "archiveBytes": len(archive),
                                      "binarySha256": sha256(installed.read_bytes()), "binaryBytes": len(binary), "mode": "0755"})
            # These are real loopback transfers and existing-prefix/link controls.
            expected_refusal(lambda: download(f"{url}/candidate.tar.gz", "0" * 64))
            unsafe = download(f"{url}/unsafe.tar.gz", sha256(archives["/unsafe.tar.gz"]))
            expected_refusal(lambda: archive_binary(unsafe, sha256(b"negative archive")))
            before = authoring.inventory(prefixes["baseline"])
            expected_refusal(lambda: install(candidate, prefixes["baseline"]))
            outside = work / "outside-sentinel"
            outside.mkdir()
            (outside / "sentinel").write_bytes(b"do not replace\n")
            linked = work / "linked-install"
            linked.symlink_to(outside, target_is_directory=True)
            expected_refusal(lambda: install(candidate, linked))
            if authoring.inventory(prefixes["baseline"]) != before or (outside / "sentinel").read_bytes() != b"do not replace\n":
                raise QualificationError("installation refusal changed retained or unrelated files")
            consumer = work / "active consumer µ"
            authoring.copy_consumer(root, consumer, "assets/identity")
            for label in ["baseline", "candidate"]:
                invoke(prefixes[label], ["--version"], consumer, commands)
                invoke(prefixes[label], ["--help"], consumer, commands)
            baseline_outputs = generated_state(prefixes["baseline"], consumer, commands)
            saved = work / "baseline-output-snapshot"
            shutil.copytree(consumer / "assets/identity", saved)
            candidate_outputs = generated_state(prefixes["candidate"], consumer, commands)
            snapshot = authoring.inventory(consumer)
            invoke(prefixes["candidate"], ["v1-generate", "--repository-root", str(consumer)], consumer, commands, missing_python=True, expected=1)
            if authoring.inventory(consumer) != snapshot:
                raise QualificationError("missing Python changed consumer state")
            invoke(prefixes["candidate"], ["v1-inspect", "--repository-root", str(consumer)], consumer, commands, missing_python=True)
            if authoring.inventory(consumer) != snapshot:
                raise QualificationError("inspection changed consumer state")
            invoke(prefixes["candidate"], ["v1-recover", "--repository-root", str(consumer)], consumer, commands, missing_python=True)
            if authoring.inventory(consumer) != snapshot:
                raise QualificationError("idle recovery changed completed consumer state")
            initializer = candidate_cli_checks(prefixes["candidate"], work, commands)
            shutil.rmtree(consumer / "assets/identity")
            shutil.copytree(saved, consumer / "assets/identity")
            invoke(prefixes["baseline"], ["v1-verify", "--repository-root", str(consumer)], consumer, commands)
            if authoring.inventory(consumer / "assets/identity") != baseline_outputs:
                raise QualificationError("rollback did not restore exact prior output bytes")
            current_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
            authoring_receipt = authoring.prove(argparse.Namespace(
                repository_root=root, identity_binary=prefixes["candidate"] / "identity",
                consumer_repository=arguments.consumer_repository, consumer_revision=arguments.consumer_revision,
                identity_revision=current_revision, output_root="assets/identity"))
    finally:
        if authoring.inventory(root, excluded_names=frozenset({".git"})) != original:
            raise QualificationError("original consumer changed")
        if binary_bytes(arguments.candidate_binary, arguments.candidate_sha256) != candidate or binary_bytes(arguments.baseline_binary, arguments.baseline_sha256) != baseline:
            raise QualificationError("supplied binary changed during qualification")
    return {"recordKind": "local source-candidate download/install/replacement proof; not released artifact acceptance",
            "observedAt": datetime.now(timezone.utc).isoformat(), "platform": {"system": platform.system(), "machine": platform.machine(), "python": platform.python_version()},
            "qualificationTool": {"path": "scripts/qualify_local_install.py", "sha256": sha256(Path(__file__).read_bytes()), "checkoutRevision": current_revision},
            "candidateSourceRevision": arguments.candidate_revision, "baselineSourceRevision": arguments.baseline_revision,
            "binaryBuildOrigin": "Caller-selected binaries; pair with separate source/build receipts. Archive transport does not attest compilation or release authenticity.",
            "transport": "Actual loopback HTTP, proxy-disabled, no redirects; explicit archive and executable SHA256 before isolated installation.",
            "artifacts": artifact_rows, "negativeControls": {"wrongDownloadDigest": "rejected", "unsafeArchivePath": "rejected", "existingPrefix": "preserved/refused", "symlinkPrefix": "preserved/refused"},
            "commands": commands, "initialization": initializer, "replacement": {"distinctBinaryHashes": True, "selection": "isolated PATH prefixes; no system installation", "baselineOutputFiles": sum(v["kind"] == "file" for v in baseline_outputs.values()), "candidateOutputFiles": sum(v["kind"] == "file" for v in candidate_outputs.values()), "outputBytesEqual": baseline_outputs == candidate_outputs, "rollbackRestoresExactPriorOutputs": True},
            "candidateConsumerProof": authoring_receipt, "originalConsumerAndSuppliedBinariesPreserved": True,
            "limits": ["Native Linux amd64 on this host only; no macOS/Windows/minimum-libc availability inferred.", "Both source candidates may print the same package version; this proves byte-bound replacement, not a published semantic-version upgrade.", "No official download, signing, attestation, stable release, deployment or creative approval is established.", "Recovery checks inspect and completed/empty state only; interrupted-process recovery remains separately exercised by native integration proofs."]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["candidate-binary", "baseline-binary", "consumer-root", "receipt"]:
        parser.add_argument("--" + name, required=True, type=Path)
    for name in ["candidate-sha256", "baseline-sha256", "candidate-revision", "baseline-revision", "consumer-repository", "consumer-revision"]:
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    try:
        destination = args.receipt.resolve()
        for forbidden in [REPOSITORY, args.consumer_root.resolve(), args.candidate_binary.resolve(), args.baseline_binary.resolve()]:
            if destination == forbidden or forbidden in destination.parents:
                raise QualificationError("receipt must be new and outside source, consumer and binaries")
        if not destination.parent.is_dir() or destination.exists() or args.receipt.is_symlink():
            raise QualificationError("receipt destination must be new")
        result = qualify(args)
        with destination.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    except (QualificationError, authoring.ProofError, OSError, ValueError, RuntimeError):
        print("local install qualification failed; inspect the selected inputs and retained private command log", file=sys.stderr)
        return 1
    print("local source-candidate install qualification passed; bounded receipt written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
