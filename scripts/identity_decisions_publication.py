#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Compose Identity's Decisions alias and verify the exact deployed site bytes."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from http.client import HTTPException
import json
from pathlib import Path
import re
import tarfile
import tempfile
import time
from urllib import error, parse, request

CANONICAL_URL = "https://identity.egohygiene.io/"
MANIFEST = "intelligence/build-manifest.json"
ALIAS = "decisions/index.html"
ALIAS_HTML = b'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Identity Decisions</title>
<link rel="icon" type="image/png" href="/intelligence/egohygiene.png">
<meta http-equiv="refresh" content="0; url=/intelligence/decisions/">
<link rel="canonical" href="https://identity.egohygiene.io/intelligence/decisions/">
</head><body><p><a href="/intelligence/decisions/">Read Identity Decisions</a></p></body></html>
'''
MAX_BYTES = 32 * 1024 * 1024
MAX_FILES = 512


def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    if (not isinstance(relative, str) or len(relative) > 1024 or "\\" in relative
            or any(part in ("", ".", "..") for part in relative.split("/"))):
        raise ValueError("unsafe relative path")
    path = root.absolute() / relative
    if any(item.is_symlink() for item in (path, *path.parents)):
        raise ValueError(f"symbolic link rejected: {relative}")
    return path


def read_bytes(path):
    if not path.is_file():
        raise ValueError(f"regular file required: {path.name}")
    with path.open("rb") as source:
        data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("file exceeds verification byte limit")
    return data


def compose(site):
    target = safe_path(site, "intelligence/decisions/index.html")
    alias = safe_path(site, ALIAS)
    if not target.is_file():
        raise ValueError("generated Decisions target is missing")
    if alias.parent.exists():
        raise ValueError("consumer Decisions route already exists")
    alias.parent.mkdir()
    with alias.open("xb") as output:
        output.write(ALIAS_HTML)


def canonical_origin(url):
    parsed = parse.urlsplit(url)
    return (parsed.scheme, parsed.netloc) == ("https", "identity.egohygiene.io")


class CanonicalRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not canonical_origin(newurl):
            raise ValueError("redirect outside canonical HTTPS origin rejected")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(path, size, timeout):
    url = CANONICAL_URL + parse.quote(path, safe="/")
    req = request.Request(url, headers={"Accept-Encoding": "identity", "Cache-Control": "no-cache"})
    deadline = time.monotonic() + timeout
    with request.build_opener(CanonicalRedirect()).open(req, timeout=timeout) as response:
        if not canonical_origin(response.geturl()):
            raise ValueError("response outside canonical HTTPS origin rejected")
        data = bytearray()
        while len(data) <= size:
            if time.monotonic() >= deadline:
                raise TimeoutError("response deadline exceeded")
            chunk = response.read1(min(65536, size + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        return bytes(data)


def expectations(site, evidence):
    manifest_bytes = read_bytes(safe_path(site, MANIFEST))
    manifest = json.loads(manifest_bytes)
    baseline = json.loads(read_bytes(safe_path(evidence, "consumer-route-baseline.json")))
    binding = json.loads(read_bytes(safe_path(evidence, "source-binding.json")))
    consumer = {"repository": "egohygiene/identity", "revision": binding["intelligence_revision"]}
    if (not re.fullmatch(r"[0-9a-f]{40}", consumer["revision"])
            or binding["repository"] != consumer["repository"]
            or manifest["consumer"] != consumer or baseline["consumer"] != consumer
            or manifest["generator"]["revision"] != binding["relay_revision"]):
        raise ValueError("source binding, baseline, or build manifest revision drift")
    records = [{"path": MANIFEST, "bytes": len(manifest_bytes), "sha256": digest(manifest_bytes)}]
    records += [{**item, "path": "intelligence/" + item["path"]} for item in manifest["bundle"]["files"]]
    records += [{"path": ALIAS, "bytes": len(ALIAS_HTML), "sha256": digest(ALIAS_HTML)}]
    records += baseline["files"]
    if not 1 <= len(records) <= MAX_FILES or len({r["path"] for r in records}) != len(records):
        raise ValueError("invalid or duplicate deployment inventory")
    for item in records:
        data = read_bytes(safe_path(site, item["path"]))
        if not 0 <= item["bytes"] <= MAX_BYTES or len(data) != item["bytes"] or digest(data) != item["sha256"]:
            raise ValueError(f"local composition drift: {item['path']}")
    return consumer, digest(manifest_bytes), records


def check_live(item, deadline):
    checked = {"path": item["path"], "expected_sha256": item["sha256"], "result": "failed"}
    try:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("live verification deadline exceeded")
        data = fetch(item["path"], item["bytes"], min(10, remaining))
        checked.update(observed_sha256=digest(data), observed_bytes=len(data))
        if len(data) != item["bytes"] or digest(data) != item["sha256"]:
            raise ValueError("deployed bytes differ from expected bytes")
        checked["result"] = "passed"
    except error.HTTPError as exc:
        if item["path"] in (".nojekyll", "CNAME") and exc.code == 404:
            checked.update(result="unavailable", http_status=404, optional=True)
        else:
            checked["error"] = f"HTTP {exc.code}"
    except (OSError, ValueError, HTTPException) as exc:
        checked["error"] = str(exc)[:300]
    return checked


def verify_live(site, evidence, attempts=6, delay=5):
    report_path = safe_path(evidence, "live-verification.json")
    if site.resolve() == evidence.resolve() or site.resolve() in evidence.resolve().parents:
        raise ValueError("verification evidence must remain outside the public site")
    report = {"schema": "identity.decisions-live-verification/v1", "canonical_url": CANONICAL_URL,
              "result": "failed", "attempts": 0, "checked_files": []}
    deadline = time.monotonic() + 180
    try:
        consumer, manifest_digest, records = expectations(site, evidence)
        report.update(expected_source=consumer, expected_manifest_sha256=manifest_digest)
        for attempt in range(attempts):
            # Admit this deployment's manifest before checking the remaining bounded inventory.
            checked = [check_live(records[0], deadline)]
            report.update(attempts=attempt + 1, checked_files=checked)
            if checked[0]["result"] == "passed":
                with ThreadPoolExecutor(max_workers=8) as pool:
                    checked.extend(pool.map(lambda item: check_live(item, deadline), records[1:]))
            if len(checked) == len(records) and all(r["result"] in ("passed", "unavailable") for r in checked):
                report["result"] = "passed"
                break
            if time.monotonic() + delay >= deadline:
                break
            if attempt + 1 < attempts and time.monotonic() + delay < deadline:
                time.sleep(delay)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report["error"] = str(exc)[:300]
    report["observed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    evidence.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report["result"] == "passed"


def capture_rollback(record_path, evidence, site):
    """Retain a new archive of exact previously observed bytes, never a rebuilt site."""
    archive_path = safe_path(evidence, "rollback-site.tar")
    copied_record = safe_path(evidence, "rollback-record.json")
    if site.resolve() == evidence.resolve() or site.resolve() in evidence.resolve().parents:
        raise ValueError("rollback evidence must remain outside the public site")
    if archive_path.exists() or copied_record.exists():
        raise ValueError("rollback capture already exists")
    record_bytes = read_bytes(safe_path(record_path.parent, record_path.name))
    record = json.loads(record_bytes)
    files = record["files"]
    if (record.get("schema") != "identity.decisions-publication-rollback/v1"
            or record.get("deploymentUrl") != CANONICAL_URL
            or not re.fullmatch(r"[0-9a-f]{40}", record.get("consumerRevision", ""))
            or not isinstance(files, list) or not 1 <= len(files) <= MAX_FILES
            or record.get("capturedFiles") != len(files)):
        raise ValueError("invalid rollback source record")
    seen = set()
    for item in files:
        path = item["path"]
        safe_path(evidence, path)
        if (path in seen or path.split("/")[0] in ("intelligence", "decisions")
                or not isinstance(item["bytes"], int) or not 0 <= item["bytes"] <= MAX_BYTES
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", item["sha256"])):
            raise ValueError("invalid rollback file inventory")
        seen.add(path)
    inventory = (json.dumps(files, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode()
    if digest(inventory) != record.get("siteDigest") or sum(item["bytes"] for item in files) > 128 * 1024 * 1024:
        raise ValueError("rollback inventory digest or byte limit mismatch")
    evidence.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 180
    with tempfile.TemporaryDirectory(prefix=".rollback-", dir=evidence) as temporary:
        staging = Path(temporary)
        def capture(item):
            for attempt in range(3):
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("rollback capture deadline exceeded")
                try:
                    data = fetch(item["path"], item["bytes"], min(30, remaining))
                except error.HTTPError as exc:
                    if (exc.code != 429 and not 500 <= exc.code < 600) or attempt == 2:
                        raise
                except (OSError, HTTPException):
                    if attempt == 2:
                        raise
                else:
                    break
            if len(data) != item["bytes"] or digest(data) != item["sha256"]:
                raise ValueError(f"rollback bytes differ: {item['path']}")
            destination = safe_path(staging / "site", item["path"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(capture, files))
        archive = staging / "rollback-site.tar"
        with tarfile.open(archive, "w", format=tarfile.PAX_FORMAT) as output:
            for item in files:  # Preserve the source helper's inventory order and digest semantics.
                info = tarfile.TarInfo(item["path"])
                info.size, info.mode, info.mtime = item["bytes"], 0o644, 0
                with safe_path(staging / "site", item["path"]).open("rb") as source:
                    output.addfile(info, source)
        captured = {"schema": "identity.decisions-rollback-capture/v1", "result": "passed",
                    "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "consumer_revision": record["consumerRevision"], "site_digest": record["siteDigest"],
                    "files": len(files), "archive_sha256": digest(archive.read_bytes()),
                    "archive_provenance": "new capture; not the original expired Pages artifact"}
        archive.replace(archive_path)
        copied_record.write_bytes(record_bytes)
        safe_path(evidence, "rollback-capture.json").write_text(json.dumps(captured, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--operation", choices=("compose", "verify-live", "capture-rollback"), required=True)
    parser.add_argument("--site-directory", type=Path, default=Path("renderer/dist"))
    parser.add_argument("--canonical-url", required=True)
    parser.add_argument("--evidence-directory", type=Path, default=Path(".relay/repository-intelligence-deployment"))
    parser.add_argument("--rollback-record", type=Path)
    args = parser.parse_args()
    try:
        if args.canonical_url != CANONICAL_URL:
            raise ValueError("only the configured Identity HTTPS origin is supported")
        if args.operation == "capture-rollback":
            if args.rollback_record is None:
                raise ValueError("--rollback-record is required for capture-rollback")
            capture_rollback(args.rollback_record, args.evidence_directory, args.site_directory)
            return 0
        if args.operation == "compose":
            compose(args.site_directory)
            return 0
        return 0 if verify_live(args.site_directory, args.evidence_directory) else 1
    except (OSError, ValueError, KeyError, TypeError, HTTPException) as exc:
        parser.exit(1, f"Publication verification failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
