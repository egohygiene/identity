#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Prepare/review or explicitly build the pinned task-local ZIP-only act derivative.

No global tools are changed. --build explicitly permits checksum-verified Go
module acquisition; source/tool archives require --download or an offline cache.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import tarfile
import urllib.parse
import urllib.request
import zipfile


REPOSITORY = Path(__file__).resolve().parents[1]
LOCK = REPOSITORY / "dev/local-actions/act-artifact-compat/lock.json"
SPEC = importlib.util.spec_from_file_location("identity_action_sources", REPOSITORY / "scripts/prepare_local_actions.py")
SOURCES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCES)
MAX_SOURCE_FILES = 10000
MAX_SOURCE_BYTES = 128 * 1024 * 1024
MAX_TOOL_FILES = 50000
MAX_TOOL_BYTES = 1024 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular_bytes(path: Path, expected: dict) -> bytes:
    with open(path, "rb", opener=lambda p, f: os.open(p, f | os.O_NOFOLLOW | os.O_NONBLOCK)) as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size != expected["bytes"]:
            raise ValueError("Archive must be a regular file of its exact locked size")
        data = stream.read(expected["bytes"] + 1)
    if len(data) != expected["bytes"] or sha256(data) != expected["sha256"]:
        raise ValueError("Archive differs from its locked bytes")
    return data


def normalized_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name.rstrip("/"))
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name or "\0" in name:
        raise ValueError("Archive contains an unsafe member")
    if path.as_posix() != name.rstrip("/"):
        raise ValueError("Archive members must be normalized")
    return path


def source_entries(archive: Path, lock: dict) -> dict[str, tuple[int, bytes]]:
    """Validate all source bytes/modes, including the one exact upstream symlink."""
    entries = {}
    total = 0
    prefix = "act-" + lock["revision"]
    with tarfile.open(archive, "r:gz") as source:
        seen = set()
        for index, member in enumerate(source):
            if index >= MAX_SOURCE_FILES:
                raise ValueError("Source archive has too many members")
            path = normalized_member(member.name)
            if not path.parts or path.parts[0] != prefix:
                raise ValueError("Source archive root differs from the locked revision")
            relative = "/".join(path.parts[1:])
            if member.name.rstrip("/") in seen:
                raise ValueError("Source archive has duplicate members")
            seen.add(member.name.rstrip("/"))
            if member.isdir():
                continue
            if not relative:
                raise ValueError("Source archive root must be a directory")
            if member.isfile():
                total += member.size
                if total > MAX_SOURCE_BYTES:
                    raise ValueError("Source archive exceeds its extracted byte budget")
                data = source.extractfile(member).read(member.size + 1)
                if len(data) != member.size:
                    raise ValueError("Source member length differs")
                mode = 0o100755 if member.mode & 0o111 else 0o100644
            elif member.issym() and lock["knownSymlinks"].get(relative) == member.linkname:
                data = member.linkname.encode()
                mode = 0o120000
            else:
                raise ValueError("Unexpected link or special source member")
            if relative in entries:
                raise ValueError("Source archive has duplicate files")
            entries[relative] = (mode, data)
    if SOURCES.tree_digest(entries) != lock["gitTreeSha1"]:
        raise ValueError("Complete source Git tree differs from the locked commit")
    if {p: d.decode() for p, (m, d) in entries.items() if m == 0o120000} != lock["knownSymlinks"]:
        raise ValueError("Source link inventory differs from its lock")
    return entries


def write_source(destination: Path, entries: dict[str, tuple[int, bytes]]) -> None:
    destination.mkdir()
    for name, (mode, data) in entries.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if mode != 0o120000:
            target.write_bytes(data)
            target.chmod(0o755 if mode == 0o100755 else 0o644)
    for name, (mode, data) in entries.items():
        if mode == 0o120000:
            target = destination / name
            resolved = (target.parent / data.decode()).resolve()
            if destination.resolve() not in resolved.parents:
                raise ValueError("Locked source link escapes its source tree")
            target.symlink_to(data.decode())


def extract_tool(archive: Path, destination: Path, *, zipped: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    if zipped:
        with zipfile.ZipFile(archive) as bundle:
            infos = bundle.infolist()
            if len(infos) > MAX_TOOL_FILES or sum(i.file_size for i in infos) > MAX_TOOL_BYTES:
                raise ValueError("Tool archive exceeds its bounds")
            seen = set()
            for info in infos:
                name = normalized_member(info.filename)
                if name.as_posix() in seen or stat.S_ISLNK(info.external_attr >> 16):
                    raise ValueError("Tool archive has duplicate/link members")
                seen.add(name.as_posix())
            bundle.extractall(destination)
    else:
        with tarfile.open(archive, "r:gz") as bundle:
            members = bundle.getmembers()
            if len(members) > MAX_TOOL_FILES or sum(m.size for m in members) > MAX_TOOL_BYTES:
                raise ValueError("Tool archive exceeds its bounds")
            seen = set()
            for member in members:
                name = normalized_member(member.name)
                if name.as_posix() in seen or not (member.isfile() or member.isdir()):
                    raise ValueError("Tool archive has duplicate/link/special members")
                seen.add(name.as_posix())
            bundle.extractall(destination, filter="data")


def descriptor(data: bytes) -> bytes:
    text = data.decode()
    match = re.search(r"var file_artifact_proto_rawDesc = \[\]byte\{(.*?)\n\}", text, re.S)
    if match is None:
        raise ValueError("Pinned generated source lacks its expected descriptor")
    return bytes(int(value, 16) for value in re.findall(r"0x([0-9a-f]{2})", match[1]))


def descriptor_set_member(data: bytes) -> bytes:
    if not data or data[0] != 10:
        raise ValueError("Expected one FileDescriptorProto")
    pos, length, shift = 1, 0, 0
    while True:
        if pos >= len(data) or shift >= 70:
            raise ValueError("Invalid descriptor length")
        byte = data[pos]
        pos += 1
        length |= (byte & 127) << shift
        if byte < 128:
            break
        shift += 7
    if pos + length != len(data):
        raise ValueError("Expected exactly one FileDescriptorProto")
    return data[pos:]


def protobuf_fields(data: bytes) -> list[tuple[int, int, bytes | int, bytes]]:
    """Read bounded descriptor wire fields while preserving every original byte."""
    if len(data) > 1024 * 1024:
        raise ValueError("Descriptor exceeds its bound")
    pos = 0

    def varint() -> int:
        nonlocal pos
        value, shift = 0, 0
        while pos < len(data) and shift < 70:
            byte = data[pos]
            pos += 1
            value |= (byte & 127) << shift
            if byte < 128:
                return value
            shift += 7
        raise ValueError("Invalid descriptor varint")

    result = []
    while pos < len(data):
        start = pos
        tag = varint()
        number, wire = tag >> 3, tag & 7
        if number == 0:
            raise ValueError("Invalid descriptor field")
        if wire == 0:
            value = varint()
        elif wire in {1, 2, 5}:
            length = varint() if wire == 2 else (8 if wire == 1 else 4)
            if pos + length > len(data):
                raise ValueError("Descriptor field is truncated")
            value = data[pos:pos + length]
            pos += length
        else:
            raise ValueError("Unsupported descriptor wire type")
        result.append((number, wire, value, data[start:pos]))
    return result


def encode_varint(value: int) -> bytes:
    out = bytearray()
    while value >= 128:
        out.append((value & 127) | 128)
        value >>= 7
    out.append(value)
    return bytes(out)


def prove_typed_mime_delta(original: bytes, patched: bytes) -> None:
    """Removing only the exact typed field6 must recover all upstream bytes."""
    result = bytearray()
    removed = 0
    messages = 0
    for number, wire, value, raw in protobuf_fields(patched):
        if number != 4 or wire != 2:
            result.extend(raw)
            continue
        message = protobuf_fields(value)
        names = [v for n, w, v, _ in message if n == 1 and w == 2]
        if names != [b"CreateArtifactRequest"]:
            result.extend(raw)
            continue
        messages += 1
        restored = bytearray()
        for n, w, v, field_raw in message:
            if n == 2 and w == 2:
                fields = protobuf_fields(v)
                field_names = [fv for fn, fw, fv, _ in fields if fn == 1 and fw == 2]
                if field_names == [b"mime_type"]:
                    exact = [(1, 2, b"mime_type"), (3, 0, 6), (4, 0, 1), (5, 0, 11), (6, 2, b".google.protobuf.StringValue"), (10, 2, b"mimeType")]
                    if [(fn, fw, fv) for fn, fw, fv, _ in fields] != exact:
                        raise ValueError("MIME descriptor differs from the typed sender field6")
                    removed += 1
                    continue
            restored.extend(field_raw)
        result.extend(encode_varint((4 << 3) | 2) + encode_varint(len(restored)) + restored)
    if messages != 1 or removed != 1 or bytes(result) != original:
        raise ValueError("Descriptor changes more than the one typed MIME field")


def acquire(expected: dict, destination: Path, cache: Path | None, download: bool) -> Path:
    name = expected["name"]
    if PurePosixPath(name).name != name or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("Unsafe archive filename")
    target = destination / name
    if cache is not None:
        data = regular_bytes(cache / name, expected)
    elif download:
        parsed = urllib.parse.urlsplit(expected["url"])
        if parsed.scheme != "https" or parsed.hostname not in {"codeload.github.com", "go.dev", "github.com", "registry.npmjs.org"} or parsed.username or parsed.password:
            raise ValueError("Archive URL is not an approved public source")
        with urllib.request.urlopen(expected["url"], timeout=60) as response:
            data = response.read(expected["bytes"] + 1)
        if len(data) != expected["bytes"] or sha256(data) != expected["sha256"]:
            raise ValueError("Downloaded archive differs from locked bytes")
    else:
        raise ValueError("Choose explicit --download or --archive-directory")
    target.write_bytes(data)
    return target


def prepare(output: Path, cache: Path | None, download: bool, build: bool) -> dict:
    lock = json.loads(LOCK.read_text(), object_pairs_hook=SOURCES.unique_json_object)
    if lock.get("kind") != "identity.local-act-artifact-compat-lock/v1":
        raise ValueError("Unsupported local compatibility lock")
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
        raise ValueError("This locked compiler profile is Linux/amd64 only")
    output = output.resolve()
    if output == REPOSITORY or REPOSITORY in output.parents or output.exists():
        raise ValueError("Output must be a new directory outside the repository")
    patch = SOURCES.source_path(REPOSITORY, lock["patch"]["path"])
    if len(patch.read_bytes()) != lock["patch"]["bytes"] or sha256(patch.read_bytes()) != lock["patch"]["sha256"]:
        raise ValueError("Compatibility patch differs from its reviewed lock")
    output.mkdir(parents=True)
    archives = output / "archives"
    archives.mkdir()
    selected = [lock["upstream"]["archive"], lock["sender"]["archive"], lock["toolchains"]["go"]["archive"], lock["toolchains"]["protoc"]["archive"]]
    for item in selected:
        acquire(item, archives, cache, download)
    sender = (archives / lock["sender"]["archive"]["name"]).read_bytes()
    if "sha512-" + base64.b64encode(hashlib.sha512(sender).digest()).decode() != lock["sender"]["integrity"]:
        raise ValueError("Sender archive differs from the pinned uploader dependency")
    with tarfile.open(archives / lock["sender"]["archive"]["name"], "r:gz") as package:
        candidates = [item for item in package if item.name == lock["sender"]["schemaPath"]]
        if len(candidates) != 1 or not candidates[0].isfile() or candidates[0].size > 2 * 1024 * 1024:
            raise ValueError("Sender schema member is absent or invalid")
        schema_bytes = package.extractfile(candidates[0]).read(candidates[0].size + 1)
        if sha256(schema_bytes) != lock["sender"]["schemaSha256"]:
            raise ValueError("Sender schema differs from the locked library")
    entries = source_entries(archives / lock["upstream"]["archive"]["name"], lock["upstream"])
    original_descriptor = descriptor(entries["pkg/artifacts/artifact.pb.go"][1])
    if sha256(original_descriptor) != lock["generated"]["originalDescriptorSha256"]:
        raise ValueError("Original schema differs from the reviewed descriptor")
    source = output / "source"
    write_source(source, entries)
    tools = output / "toolchains"
    extract_tool(archives / lock["toolchains"]["go"]["archive"]["name"], tools)
    extract_tool(archives / lock["toolchains"]["protoc"]["archive"]["name"], tools / "protoc", zipped=True)
    (tools / "protoc/bin/protoc").chmod(0o755)
    commands = []

    def run(arguments: list[str], name: str, environment: dict | None = None) -> str:
        result = subprocess.run(arguments, cwd=source, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
        raw = result.stdout.encode()
        (output / (name + ".private.log")).write_bytes(raw)
        (output / (name + ".private.log")).chmod(0o600)
        commands.append({"name": name, "exitCode": result.returncode, "rawLogBytes": len(raw), "rawLogSha256": sha256(raw)})
        if result.returncode:
            raise RuntimeError("Local preparation/build command failed: " + name)
        return result.stdout

    run(["git", "apply", "--check", str(patch)], "patch-check")
    run(["git", "apply", str(patch)], "patch-apply")
    changed = {name for name, (_, data) in entries.items() if not (source / name).exists() or (not (source / name).is_symlink() and (source / name).read_bytes() != data)}
    added = {p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file() and p.relative_to(source).as_posix() not in entries}
    if changed | added != set(lock["patchedFiles"]):
        raise ValueError("Patch changes an unexpected source inventory")
    for name, digest in lock["patchedFiles"].items():
        if sha256((source / name).read_bytes()) != digest:
            raise ValueError("Patched source differs from its reviewed lock")
    prove_typed_mime_delta(original_descriptor, descriptor((source / "pkg/artifacts/artifact.pb.go").read_bytes()))
    receipt = {"kind": "identity.local-act-artifact-compat-build/v1", "name": lock["derivative"]["name"], "version": lock["derivative"]["version"], "upstreamRevision": lock["upstream"]["revision"], "sourceGitTreeVerified": True, "patchSha256": lock["patch"]["sha256"], "typedFieldSixOnlyDescriptorDelta": True, "officialActModified": False, "buildStatus": "unrun", "commands": commands}
    if build:
        if shutil.disk_usage(output).free < 2 * 1024 ** 3:
            raise RuntimeError("Build requires a real 2GiB free local reserve")
        env = os.environ.copy()
        env.update({"GOENV": "off", "GOTOOLCHAIN": "local", "GOBIN": str(tools / "bin"), "GOCACHE": str(output / "gocache"), "GOMODCACHE": str(output / "gomodcache"), "GOPATH": str(output / "gopath"), "GOSUMDB": "sum.golang.org", "GOPROXY": "https://proxy.golang.org", "GOINSECURE": "", "GOPRIVATE": "", "GONOPROXY": "", "GONOSUMDB": "", "GOMAXPROCS": "2", "GOFLAGS": "-trimpath -p=2", "CGO_ENABLED": "0", "GOOS": "linux", "GOARCH": "amd64"})
        go = str(tools / "go/bin/go")
        plugin = lock["toolchains"]["protocGenGo"]
        run([go, "install", plugin["module"] + "@" + plugin["version"]], "plugin-build", env)
        module_hash = output / "gomodcache/cache/download/google.golang.org/protobuf/@v" / (plugin["version"] + ".ziphash")
        if module_hash.read_text().strip() != plugin["moduleZipHash"]:
            raise ValueError("Generator module differs from the reviewed checksum")
        env["PATH"] = str(tools / "bin") + os.pathsep + env.get("PATH", "")
        protoc = str(tools / "protoc/bin/protoc")
        schema = source / "pkg/artifacts/artifact.proto"
        legacy = output / "legacy-schema"
        legacy.mkdir()
        old_text = schema.read_text()
        line = "  google.protobuf.StringValue mime_type = 6;\n"
        if old_text.count(line) != 1:
            raise ValueError("Expected the one typed MIME declaration")
        (legacy / "artifact.proto").write_text(old_text.replace(line, ""))
        run([protoc, "--proto_path=" + str(legacy), "--proto_path=" + str(tools / "protoc/include"), "--descriptor_set_out=" + str(legacy / "set.pb"), "artifact.proto"], "legacy-schema-proof", env)
        if descriptor_set_member((legacy / "set.pb").read_bytes()) != original_descriptor:
            raise ValueError("Restored legacy schema changes upstream semantics")
        regenerated = output / "regenerated"
        regenerated.mkdir()
        run([protoc, "--proto_path=" + str(schema.parent), "--proto_path=" + str(tools / "protoc/include"), "--go_out=" + str(regenerated), "--go_opt=paths=source_relative", "--go_opt=Martifact.proto=github.com/nektos/act/pkg/artifacts", "artifact.proto"], "protobuf-regeneration", env)
        if sha256((regenerated / "artifact.pb.go").read_bytes()) != lock["generated"]["patchedGoSha256"]:
            raise ValueError("Generated Go source differs from the reviewed patch")
        run([go, "test", "-short", "-json", "-p", "2", "./pkg/artifacts"], "artifact-tests", env)
        binary = output / "bin" / lock["derivative"]["name"]
        binary.parent.mkdir()
        run([go, "build", "-trimpath", "-buildvcs=false", "-mod=readonly", "-p", "2", "-ldflags", "-X main.version=" + lock["derivative"]["version"], "-o", str(binary), "."], "derivative-build", env)
        version = run([str(binary), "--version"], "derivative-version", env).strip()
        if version != "act version " + lock["derivative"]["version"]:
            raise ValueError("Built derivative does not identify its local version")
        receipt.update({"buildStatus": "passed", "legacyDescriptorByteIdentical": True, "generatedSourceMatches": True, "binarySha256": sha256(binary.read_bytes()), "binaryBytes": binary.stat().st_size, "reportedVersion": version})
    (output / "build-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--archive-directory", type=Path)
    group.add_argument("--download", action="store_true")
    parser.add_argument("--build", action="store_true", help="Explicitly acquire verified Go modules, regenerate/prove the schema, test and build the named local derivative")
    args = parser.parse_args()
    try:
        result = prepare(args.output_directory, args.archive_directory, args.download, args.build)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired):
        parser.exit(1, "Local act preparation/build failed; inspect the task-local private logs. No official tool was replaced.\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
