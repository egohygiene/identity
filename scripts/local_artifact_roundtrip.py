#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Verify one actual local act upload through its authenticated download API.

This worker runs only inside the disposable fixture. It never records the
runtime token or signed URL, and accepts only the selected loopback server.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import urllib.parse
import urllib.request
import zipfile
import zlib


MAX_ARCHIVE = 2 * 1024 * 1024
MAX_EXPANDED = 1024 * 1024
SERVICE = "/twirp/github.actions.results.api.v1.ArtifactService/GetSignedArtifactURL"


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate local transport metadata key")
        result[key] = value
    return result


def local_origin(url: str) -> tuple[str, str, int]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "http" or parsed.hostname != "127.0.0.1" or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("Artifact transport must use the explicit loopback HTTP server")
    port = parsed.port
    if port is None or not 0 < port < 65536:
        raise ValueError("Artifact transport requires a real local port")
    return parsed.scheme, parsed.hostname, port


def verify_archive(data: bytes, expected: dict[str, dict], digest: str, *, max_archive: int = MAX_ARCHIVE, max_expanded: int = MAX_EXPANDED, max_files: int = 16, max_members: int = 64) -> dict:
    if not re.fullmatch(r"[0-9a-f]{64}", digest) or hashlib.sha256(data).hexdigest() != digest:
        raise ValueError("Downloaded archive differs from the uploader's SHA256")
    if not 0 < len(data) <= max_archive or not isinstance(expected, dict) or not expected or len(expected) > max_files:
        raise ValueError("Artifact inventory or archive exceeds its bound")
    for name, record in expected.items():
        path = PurePosixPath(name)
        if not isinstance(name, str) or path.is_absolute() or ".." in path.parts or path.as_posix() != name or "\\" in name or "\0" in name:
            raise ValueError("Invalid expected artifact path")
        if not isinstance(record, dict) or set(record) != {"bytes", "sha256"} or type(record["bytes"]) is not int or not 0 <= record["bytes"] <= max_expanded or not isinstance(record["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
            raise ValueError("Invalid expected artifact metadata")
    directories = {str(parent) + "/" for name in expected for parent in PurePosixPath(name).parents if str(parent) != "."}
    actual = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        if len(infos) > max_members or sum(i.file_size for i in infos) > max_expanded:
            raise ValueError("ZIP inventory exceeds its bounds")
        seen = set()
        for info in infos:
            name = info.filename
            path = PurePosixPath(name.rstrip("/"))
            if name != info.orig_filename or path.is_absolute() or ".." in path.parts or "\\" in name or "\0" in name or path.as_posix() != name.rstrip("/"):
                raise ValueError("ZIP has an unsafe member path")
            if name in seen or stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1:
                raise ValueError("ZIP has duplicate, symlink or encrypted members")
            seen.add(name)
            if info.is_dir():
                if name not in directories or info.file_size:
                    raise ValueError("ZIP contains an unexpected directory")
                continue
            if name not in expected or info.file_size != expected[name]["bytes"]:
                raise ValueError("ZIP contains unexpected file bytes")
            content = archive.read(info)
            if len(content) != expected[name]["bytes"] or hashlib.sha256(content).hexdigest() != expected[name]["sha256"]:
                raise ValueError("ZIP contents differ from the fixture inputs")
            actual[name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    if actual != expected:
        raise ValueError("ZIP omits required fixture files")
    return actual


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def bounded_request(opener, request: urllib.request.Request, limit: int) -> bytes:
    with opener.open(request, timeout=15) as response:
        if local_origin(response.geturl()) != local_origin(request.full_url):
            raise ValueError("Artifact response changed its local origin")
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Artifact response exceeds its byte budget")
    return data


def run(manifest: dict, environment: dict[str, str]) -> tuple[dict, bytes]:
    if set(manifest) != {"kind", "nonce", "files"} or manifest["kind"] != "identity.local-artifact-fixture/v1" or not re.fullmatch(r"[0-9a-f]{32}", manifest["nonce"]):
        raise ValueError("Unsupported artifact fixture")
    base = environment.get("ACTIONS_RESULTS_URL", "")
    origin = local_origin(base)
    parsed = urllib.parse.urlsplit(base)
    if parsed.path not in {"", "/"} or parsed.query:
        raise ValueError("Unexpected artifact API base path")
    token = environment.get("ACTIONS_RUNTIME_TOKEN", "")
    run_id = environment.get("GITHUB_RUN_ID", "")
    digest = environment.get("FIXTURE_ARTIFACT_DIGEST", "")
    artifact_id = environment.get("FIXTURE_ARTIFACT_ID", "")
    if not token or not re.fullmatch(r"[1-9][0-9]{0,18}", run_id) or not re.fullmatch(r"[1-9][0-9]*", artifact_id):
        raise ValueError("Actual uploader/runtime outputs are missing")
    body = json.dumps({"workflow_run_backend_id": run_id, "workflow_job_run_backend_id": run_id, "name": "identity-transport-probe"}).encode()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(base.rstrip("/") + SERVICE, data=body, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    signed = json.loads(bounded_request(opener, request, 65536), object_pairs_hook=unique_object)
    if set(signed) != {"signedUrl"} and set(signed) != {"signed_url"}:
        raise ValueError("Unexpected signed artifact response")
    url = signed.get("signedUrl", signed.get("signed_url"))
    if not isinstance(url, str) or local_origin(url) != origin:
        raise ValueError("Signed artifact URL escaped the local server")
    data = bounded_request(opener, urllib.request.Request(url), MAX_ARCHIVE)
    actual = verify_archive(data, manifest["files"], digest)
    return {"kind": "identity.local-artifact-roundtrip/v1", "status": "passed", "nonce": manifest["nonce"], "context": "actual loopback HTTP upload/download; not GitHub-hosted storage", "artifactId": artifact_id, "uploaderArchiveSha256": digest, "downloadedArchiveSha256": hashlib.sha256(data).hexdigest(), "archiveBytes": len(data), "files": actual, "signedUrlRecorded": False, "runtimeTokenRecorded": False}, data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(), object_pairs_hook=unique_object)
        result, data = run(manifest, dict(os.environ))
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
        with args.output.with_suffix(".zip").open("xb") as stream:
            stream.write(data)
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, zipfile.BadZipFile, zlib.error):
        parser.exit(1, "Actual local artifact round trip failed; no token or signed URL is printed.\n")
    print("Actual local artifact upload/download/SHA256/ZIP inventory passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
