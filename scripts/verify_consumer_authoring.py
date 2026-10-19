#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Rehearse selected v1 output in disposable copies and record bounded evidence.

This development proof runs the explicitly supplied Identity binary and this
checkout's validator. It never runs consumer scripts, installs a tool, fetches a
repository, or changes the supplied consumer. Its receipt is an evidence record,
not a new source/report contract or an attestation of a binary's build origin.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any, Sequence

import release_smoke
import validate_identity as validator


IDENTITY_ROOT = Path(__file__).resolve().parents[1]
IGNORED_COPY_NAMES = {
    ".git", ".cache", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "target", "node_modules", "test-results", "playwright-report",
}
REVISION = re.compile(r"[0-9a-f]{40}")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
MANIFEST = ".identity-manifest.json"
COMMAND_TIMEOUT_SECONDS = 60


class ProofError(ValueError):
    """A bounded proof requirement failed; messages contain no local paths."""


def sha256(content: bytes) -> str:
    """Return the byte identity of one local input or artifact."""

    return hashlib.sha256(content).hexdigest()


def inventory(root: Path, *, excluded_names: frozenset[str] = frozenset()) -> dict[str, dict[str, Any]]:
    """Record names, entry kinds and bytes without following symbolic links.

    Empty directories are included so read-only verification also detects newly
    created cache directories. Link targets are hashed rather than disclosed.
    Special files are rejected before attempting to read their contents.
    """

    result: dict[str, dict[str, Any]] = {}

    def visit(directory: Path) -> None:
        for path in sorted(directory.iterdir()):
            if directory == root and path.name in excluded_names:
                continue
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[relative] = {"kind": "link", "targetSha256": sha256(os.fsencode(os.readlink(path)))}
            elif stat.S_ISDIR(mode):
                result[relative] = {"kind": "directory"}
                visit(path)
            elif stat.S_ISREG(mode):
                content = path.read_bytes()
                result[relative] = {"kind": "file", "sha256": sha256(content), "bytes": len(content)}
            else:
                raise ProofError("consumer inventory contains an unsupported special file")

    visit(root)
    return result


def inventory_digest(entries: dict[str, dict[str, Any]]) -> str:
    """Hash this proof's complete entry inventory, not the canonical source digest."""

    return sha256(json.dumps(entries, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def portable_path(value: str, label: str) -> PurePosixPath:
    """Reject normalization, absolute paths and platform-specific path escapes."""

    if not validator.valid_relative_path(value):
        raise ProofError(f"{label} must be a normalized portable repository-relative path")
    return PurePosixPath(value)


def overlaps(left: PurePosixPath, right: PurePosixPath) -> bool:
    """Return whether two local paths overlap at any depth."""

    return left == right or left in right.parents or right in left.parents


def check_output_root(output_root: str, snapshot: validator.SourceSnapshot) -> PurePosixPath:
    """Constrain removal in copies to a generated tree disjoint from all source."""

    selected = portable_path(output_root, "output root")
    if any(part.casefold() in {name.casefold() for name in IGNORED_COPY_NAMES | {".identity"}} for part in selected.parts):
        raise ProofError("output root overlaps source, repository metadata or excluded cache names")
    for value in {*snapshot.files, *snapshot.directories, ".identity"}:
        source = portable_path(value, "source path")
        if overlaps(selected, source):
            raise ProofError("output root overlaps validated source")
        if any(part in IGNORED_COPY_NAMES for part in source.parts):
            raise ProofError("validated source would be omitted by disposable-copy cache exclusions")
    return selected


def source_inventory(root: Path, snapshot: validator.SourceSnapshot) -> dict[str, dict[str, Any]]:
    """Bind the entire .identity tree and all declared external input directories."""

    entries = inventory(root, excluded_names=frozenset({".git"}))
    roots = [PurePosixPath(value) for value in {*snapshot.files, *snapshot.directories, ".identity"}]
    return {
        path: metadata for path, metadata in entries.items()
        if any(PurePosixPath(path) == source or source in PurePosixPath(path).parents for source in roots)
    }


def run_binary(binary: Path, operation: str, consumer: Path, output_root: str) -> subprocess.CompletedProcess[str]:
    """Run only the caller-selected binary, using the trusted Python interpreter."""

    environment = os.environ.copy()
    environment["IDENTITY_PYTHON"] = sys.executable
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    # Consumer Python modules must not shadow the embedded authoritative validator.
    environment.pop("PYTHONPATH", None)
    environment["PYTHONSAFEPATH"] = "1"
    try:
        return subprocess.run(
            [str(binary), operation, "--repository-root", str(consumer), "--output-root", output_root],
            cwd=IDENTITY_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise ProofError("the supplied Identity command exceeded the proof timeout") from error
    except OSError as error:
        raise ProofError("the supplied Identity binary could not be executed") from error


def verify_read_only(binary: Path, consumer: Path, output_root: str, *, expect_success: bool) -> int:
    """Check actual exit behavior and preserve the complete pre-verification state."""

    before = inventory(consumer)
    completed = run_binary(binary, "v1-verify", consumer, output_root)
    if inventory(consumer) != before:
        raise ProofError("v1-verify changed consumer files or directories")
    expected_exit = 0 if expect_success else 1
    if completed.returncode != expected_exit:
        expectation = "success exit 0" if expect_success else "failure exit 1"
        raise ProofError(f"v1-verify did not report the expected {expectation}")
    return completed.returncode


def manifest_outputs(consumer: Path, output_root: str, source_digest: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Independently verify exact manifested paths, bytes and checksums."""

    generated = consumer.joinpath(*PurePosixPath(output_root).parts)
    if not generated.is_dir() or generated.is_symlink():
        raise ProofError("generation did not produce a regular generated directory")
    entries = inventory(generated)
    if any(value["kind"] == "link" for value in entries.values()):
        raise ProofError("generated output contains a symbolic link")
    try:
        manifest = json.loads((generated / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ProofError("generated compiler manifest is missing or malformed") from error
    if not isinstance(manifest, dict) or manifest.get("schema") != "identity.compiler-manifest/v1":
        raise ProofError("generated compiler manifest has an unsupported shape")
    if manifest.get("sourceDigest") != source_digest:
        raise ProofError("generated compiler manifest does not bind the validated source digest")
    outputs = manifest.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise ProofError("generated compiler manifest has no selected outputs")
    actual = {
        f"{output_root}/{path}": value for path, value in entries.items()
        if value["kind"] == "file" and path != MANIFEST
    }
    expected: dict[str, Any] = {}
    for output in outputs:
        if not isinstance(output, dict) or not isinstance(output.get("path"), str):
            raise ProofError("compiler manifest output has a malformed path")
        path = output["path"]
        selected = portable_path(path, "manifest output path")
        if PurePosixPath(output_root) not in selected.parents or path in expected:
            raise ProofError("compiler manifest output escapes its root or duplicates a path")
        metadata = actual.get(path)
        if metadata is None or output.get("sha256") != metadata["sha256"] or output.get("bytes") != metadata["bytes"]:
            raise ProofError("compiler manifest output does not match actual bytes and checksum")
        expected[path] = metadata
    if set(expected) != set(actual):
        raise ProofError("generated files do not exactly match compiler manifest outputs")
    evidence = [{"path": path, "sha256": value["sha256"], "bytes": value["bytes"]} for path, value in sorted(expected.items())]
    return manifest, evidence


def run_git(arguments: list[str], *, text: bool = False) -> subprocess.CompletedProcess:
    """Bound read-only Git plumbing and keep timeout details out of receipts."""

    try:
        return subprocess.run(
            arguments, check=False, capture_output=True, text=text,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise ProofError("Git revision comparison exceeded the proof timeout") from error


def checkout_revision(root: Path, claimed_revision: str, consumed_files: Sequence[str]) -> dict[str, Any]:
    """Compare consumed bytes with raw Git blobs without running content filters.

    Even diff with external drivers/textconv disabled can consult a configured
    clean filter. Reading raw ls-tree/cat-file objects avoids all consumer content
    transformations. Untracked inputs remain explicit instead of inheriting the
    checkout's revision merely because HEAD matches.
    """

    prefix = ["git", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-C", str(root)]
    try:
        head = run_git(prefix + ["rev-parse", "--verify", "HEAD"], text=True)
        top = run_git(prefix + ["rev-parse", "--show-toplevel"], text=True)
    except OSError:
        return {"revision": claimed_revision, "revisionEvidence": "caller-asserted; Git metadata unavailable"}
    if head.returncode or top.returncode or Path(top.stdout.strip()).resolve() != root.resolve():
        return {"revision": claimed_revision, "revisionEvidence": "caller-asserted; supplied directory has no root Git checkout"}
    if head.stdout.strip() != claimed_revision:
        raise ProofError("claimed revision does not match the supplied checkout HEAD")
    tree = run_git(
        prefix + ["ls-tree", "-r", "--full-tree", "-z", claimed_revision, "--", *consumed_files],
    )
    if tree.returncode:
        raise ProofError("Git could not read the claimed revision's consumed-file inventory")
    tracked: dict[str, tuple[str, str]] = {}
    for record in tree.stdout.split(b"\0"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        _, kind, identifier = header.decode("ascii").split(" ")
        tracked[path.decode("utf-8")] = (kind, identifier)
    matches = True
    for path in consumed_files:
        entry = tracked.get(path)
        if entry is None or entry[0] != "blob":
            matches = False
            continue
        blob = run_git(prefix + ["cat-file", "blob", entry[1]])
        if blob.returncode:
            raise ProofError("Git could not read a consumed file's revision blob")
        local = root.joinpath(*PurePosixPath(path).parts)
        if local.is_symlink() or not local.is_file() or blob.stdout != local.read_bytes():
            matches = False
    return {
        "revision": claimed_revision,
        "revisionEvidence": "checkout HEAD verified",
        "consumedFilesMatchRevision": matches,
        "consumedFilesCompared": len(consumed_files),
        "contentComparison": "raw Git blobs; no consumer clean/smudge filters, diff drivers or textconv",
    }


def copy_consumer(original: Path, destination: Path, output_root: str) -> None:
    """Copy local files, omit Git/cache entries, and remove only disposable outputs."""

    shutil.copytree(
        original, destination, symlinks=True,
        ignore=lambda directory, names: set(names) & IGNORED_COPY_NAMES,
    )
    output = destination
    for part in PurePosixPath(output_root).parts:
        output /= part
        if output.is_symlink():
            raise ProofError("output root traverses a symbolic link in the disposable copy")
    if output.exists():
        if not output.is_dir():
            raise ProofError("existing output root is not a directory")
        shutil.rmtree(output)


def prove(arguments: argparse.Namespace) -> dict[str, Any]:
    """Execute this bounded rehearsal without changing the supplied consumer."""

    root = arguments.repository_root.resolve()
    binary = arguments.identity_binary.resolve()
    if not root.is_dir() or not binary.is_file():
        raise ProofError("consumer directory and explicit Identity binary must exist")
    if root in binary.parents:
        raise ProofError("the supplied Identity binary must be outside the consumer")
    if not REPOSITORY.fullmatch(arguments.consumer_repository):
        raise ProofError("consumer repository must use owner/name")
    for revision in (arguments.consumer_revision, arguments.identity_revision):
        if not REVISION.fullmatch(revision):
            raise ProofError("implementation and consumer revisions must be full lowercase 40-character Git SHAs")
    before = inventory(root, excluded_names=frozenset({".git"}))
    try:
        return _prove(arguments, root, binary)
    finally:
        if inventory(root, excluded_names=frozenset({".git"})) != before:
            raise ProofError("the supplied original consumer changed during the proof")


def _prove(arguments: argparse.Namespace, root: Path, binary: Path) -> dict[str, Any]:
    """Run after the original consumer's preservation snapshot has been captured."""

    diagnostics, snapshot = validator.validate_snapshot(root)
    if diagnostics:
        codes = ", ".join(sorted({value.code for value in diagnostics}))
        raise ProofError(f"consumer source validation failed ({codes})")
    output_root = check_output_root(arguments.output_root, snapshot).as_posix()
    source_before = source_inventory(root, snapshot)
    source_digest = validator.canonical_source_digest(root)
    manifest_source = json.loads((root / ".identity/identity.json").read_text(encoding="utf-8"))
    profiles = json.loads((root / manifest_source["documents"]["targets"]).read_text(encoding="utf-8"))["enabled"]
    consumer_revision = checkout_revision(root, arguments.consumer_revision, [path for path, value in source_before.items() if value["kind"] == "file"])
    script_names = ("validate_identity.py", "release_smoke.py")
    identity_revision = checkout_revision(IDENTITY_ROOT, arguments.identity_revision, [f"scripts/{name}" for name in script_names])
    binary_digest = sha256(binary.read_bytes())
    script_digests = [
        {"path": f"scripts/{name}", "sha256": sha256((IDENTITY_ROOT / "scripts" / name).read_bytes())}
        for name in script_names
    ]
    with tempfile.TemporaryDirectory(prefix="identity-authoring-proof-") as temporary:
        work = Path(temporary)
        generations: list[dict[str, Any]] = []
        first: Path | None = None
        for index in (1, 2):
            consumer = work / f"generation-{index}"
            copy_consumer(root, consumer, output_root)
            if source_inventory(consumer, snapshot) != source_before:
                raise ProofError("disposable copy does not preserve the complete validated source")
            completed = run_binary(binary, "v1-generate", consumer, output_root)
            if source_inventory(consumer, snapshot) != source_before:
                raise ProofError("v1-generate changed canonical or declared source")
            if completed.returncode:
                raise ProofError("selected-output generation failed")
            manifest, outputs = manifest_outputs(consumer, output_root, source_digest)
            generated = consumer.joinpath(*PurePosixPath(output_root).parts)
            digest, count = release_smoke.tree_digest(generated)
            verify_exit = verify_read_only(binary, consumer, output_root, expect_success=True)
            generations.append({"generationExit": 0, "verificationExit": verify_exit, "inventorySha256": digest, "files": count})
            if first is None:
                first = consumer
                first_manifest_sha256 = sha256((generated / MANIFEST).read_bytes())
                first_outputs = outputs
            elif inventory(generated) != inventory(first.joinpath(*PurePosixPath(output_root).parts)):
                raise ProofError("independent fresh generations produced different file trees")
        assert first is not None
        probes = []
        target = first_outputs[0]["path"]
        for case in ("selected-output-missing", "selected-output-drift", "canonical-source-changed"):
            consumer = work / case
            shutil.copytree(first, consumer, symlinks=True)
            if case == "canonical-source-changed":
                # JSON whitespace changes byte identity without inventing facts
                # or relying on the brief living inside the digest inventory.
                probe = consumer / ".identity/identity.json"
                probe.write_bytes(probe.read_bytes() + b"\n")
                probe_diagnostics, _ = validator.validate_snapshot(consumer)
                if probe_diagnostics or validator.canonical_source_digest(consumer) == source_digest:
                    raise ProofError("canonical-source probe did not create a distinct valid source")
            else:
                probe = consumer.joinpath(*PurePosixPath(target).parts)
                if case == "selected-output-missing":
                    probe.unlink()
                else:
                    probe.write_bytes(probe.read_bytes() + b"\nDisposable output drift probe.\n")
            if inventory(consumer) == inventory(first):
                raise ProofError("negative verification probe did not change the disposable state")
            code = verify_read_only(binary, consumer, output_root, expect_success=False)
            probes.append({"case": case, "verificationExit": code, "expectedFailureObserved": True, "verificationPreservedFiles": True})
    if sha256(binary.read_bytes()) != binary_digest:
        raise ProofError("the supplied Identity binary changed during the proof")
    if source_inventory(root, snapshot) != source_before:
        raise ProofError("the supplied original source changed during the proof")
    return {
        "observedAt": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "scope": "Offline selected-output authoring rehearsal in disposable copies; no release, publication, approval or public-kit attestation.",
        "implementation": {
            "repository": "egohygiene/identity", **identity_revision,
            "binarySha256": binary_digest,
            "binaryBuildOrigin": "caller-selected binary; build-to-revision provenance is not verified by this harness",
            "scripts": script_digests,
        },
        "proofTool": {
            "path": "scripts/verify_consumer_authoring.py",
            "sha256": sha256(Path(__file__).read_bytes()),
            "source": "actual candidate checkout bytes; separate from the runtime implementation revision",
        },
        "consumer": {
            "repository": arguments.consumer_repository, **consumer_revision,
            "sourceRevisionBinding": (
                "consumed bytes match raw revision blobs"
                if consumer_revision.get("consumedFilesMatchRevision")
                else "source bytes are inventory-bound; revision association requires caller review"
            ),
            "sourceDigest": source_digest,
            "sourceInventorySha256": inventory_digest(source_before),
            "sourceInventoryMethod": "SHA-256 of sorted JSON entry inventory; includes full .identity and declared external inputs; distinct from canonical sourceDigest",
            "sourceFiles": sum(value["kind"] == "file" for value in source_before.values()),
            "sourceUnchanged": True,
            "originalConsumerUnchanged": True,
            "originalInventoryExcludes": [".git"],
            "selectedProfiles": profiles,
        },
        "baseline": {
            "validationDiagnostics": [],
            "independentGenerations": generations,
            "independentGenerationsEqual": True,
            "generatedInventoryMethod": "release_smoke.tree_digest; length-framed relative file names and raw bytes; includes hidden compiler manifest",
            "manifestSha256": first_manifest_sha256,
            "manifestDigestMethod": "SHA-256 of actual compiler manifest file bytes",
            "manifestChecksumsMatch": True,
            "manifestOutputSetExact": True,
            "verificationPreservedFiles": True,
            "outputs": first_outputs,
        },
        "probes": probes,
        "limits": [
            "Only selected core outputs are verified; separately generated optional packages need their own checks.",
            "Public/review guidance selection and nullable omissions require their separately recorded probes.",
            "Generic internal asset selection G03 and advertised unselected archive G04 remain #101/#105.",
            "Git metadata and consumed-file comparisons are reported explicitly; binary build origin requires separate review.",
            "No network, consumer scripts, installation, source authoring, creative approval, release or deployed-site verification is performed.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    """Expose explicit input selection and a separate evidence destination."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--identity-binary", required=True, type=Path)
    parser.add_argument("--consumer-repository", required=True)
    parser.add_argument("--consumer-revision", required=True)
    parser.add_argument("--identity-revision", required=True)
    parser.add_argument("--output-root", default="assets/identity")
    parser.add_argument("--receipt", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Write a public-safe receipt only after every proof requirement succeeds."""

    arguments = build_parser().parse_args(argv)
    try:
        receipt = arguments.receipt.resolve()
        original = arguments.repository_root.resolve()
        if receipt == arguments.identity_binary.resolve():
            raise ProofError("receipt must not overwrite the supplied Identity binary")
        if receipt == original or original in receipt.parents:
            raise ProofError("receipt must be outside the original consumer")
        if receipt == IDENTITY_ROOT or IDENTITY_ROOT in receipt.parents:
            raise ProofError("receipt must be outside the trusted Identity source checkout")
        result = prove(arguments)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (ProofError, OSError, ValueError, KeyError, TypeError) as error:
        message = str(error) if isinstance(error, ProofError) else "proof input or filesystem operation failed"
        print(f"authoring proof failed: {message}", file=sys.stderr)
        return 1
    print("authoring proof passed; bounded receipt written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
