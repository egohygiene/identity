# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Failure-boundary checks for source-preserving browser qualification."""

import copy
from contextlib import redirect_stderr, redirect_stdout
import errno
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("qualify_browser", Path(__file__).resolve().parents[1] / "scripts/qualify_browser.py")
QUALIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUALIFY)


def inputs():
    image = "mcr.microsoft.com/playwright:v1.62.1-noble@sha256:" + "a" * 64
    profile = {
        "image": image, "platform": "linux/amd64", "playwright": "1.62.1",
        "packageManager": "pnpm@11.21.0", "chromium": {"colorProfile": "srgb", "version": "151.0.7922.34"},
        "settings": {"locale": "en-US", "timezoneId": "UTC"},
        "baseline": {"path": QUALIFY.BASELINE_PATH, "sha256": QUALIFY.APPROVED_BASELINE_SHA256, "approvalRevision": "b" * 40},
        "fontSourceReceipt": "docs/evidence/synthetic-font-source.json",
        "fontPackages": [{"name": name, "version": "2.37-8", "url": f"https://archive.ubuntu.com/ubuntu/pool/main/f/fonts-dejavu/{name}_2.37-8_all.deb", "sha256": "d" * 64, "bytes": 100} for name in ("fonts-dejavu-core", "fonts-dejavu-mono")],
        "fontFiles": [{"path": "/usr/share/fonts/truetype/dejavu/" + name, "sha256": "f" * 64} for name in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf", "DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf", "DejaVuSansMono-Oblique.ttf", "DejaVuSansMono-BoldOblique.ttf")],
    }
    package = {"devDependencies": {"@playwright/test": "1.62.1"}, "packageManager": "pnpm@11.21.0"}
    registry = {"image": image, "platform": "linux/amd64", "index_digest": "sha256:" + "a" * 64}
    return profile, package, registry


def font_source(profile):
    return {
        "packages": [{"package": package["name"], "architecture": "all", **{key: package[key] for key in ("version", "url", "sha256", "bytes")}} for package in profile["fontPackages"]],
        "installed_font_files": copy.deepcopy(profile["fontFiles"]),
    }


def proof(directory, profile):
    for phase in ("positive", "negative", "restored"):
        target = directory / phase
        target.mkdir()
        (target / "report.json").write_text("{}\n")
    diff = directory / "negative/brand-kit-page-diff.png"
    diff.write_bytes(b"synthetic difference fixture, not browser evidence")
    receipt = {
        "status": "passed", "platform": "linux/amd64",
        "baseline": dict(profile["baseline"], unchanged=True),
        "settings": profile["settings"],
        "runtimes": {"playwright": profile["playwright"], "pnpm": "11.21.0"},
        "browser": {"version": profile["chromium"]["version"], "executableSha256": "e" * 64, "commandLine": ["--force-color-profile=srgb"], "settings": profile["settings"], "renderedFonts": [{"selector": "h1", "fonts": [{"familyName": "Arial"}]}]},
        "fonts": {"packages": [{"name": package["name"], "version": package["version"]} for package in reversed(profile["fontPackages"])], "files": copy.deepcopy(profile["fontFiles"]), "configuration": [{"path": "/fonts.conf", "sha256": "d" * 64}]},
        "positive": {"exitCode": 0, "passed": 9, "failed": 0, "skipped": 0, "report": "positive/report.json"},
        "negative": {"exitCode": 1, "passed": 0, "failed": 1, "skipped": 0, "report": "negative/report.json", "expectedFailure": "screenshot-comparison", "baselineUnchanged": True, "diffArtifacts": [{"path": "negative/brand-kit-page-diff.png", "sha256": QUALIFY.sha256(diff.read_bytes())}]},
        "restored": {"exitCode": 0, "passed": 1, "failed": 0, "skipped": 0, "report": "restored/report.json"},
    }
    return receipt


def output(receipt, directory):
    (directory / "qualification.json").write_text(json.dumps(receipt))
    return QUALIFY.CONTAINER_MARKER + json.dumps(receipt)


class BrowserQualificationBoundaryTests(unittest.TestCase):
    def test_proxy_ca_environment_and_cli_precedence_reach_the_same_secret_boundary(self):
        # Stop at the actual build argument boundary, before a build/browser can
        # run. A selected bundle must use the existing secret transport and its
        # private path must not leak into the public receipt or printed output.
        registry = json.loads((QUALIFY.REPOSITORY / "docs/evidence/identity-browser-registry-2026-10-20.json").read_text())
        config = registry["image_config"]
        image = {"Id": registry["config_digest"], "Os": "linux", "Architecture": "amd64",
                 "RepoDigests": [registry["image"]], "Config": {"User": config["user"], "Entrypoint": config["entrypoint"], "Cmd": config["cmd"]}}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inherited, explicit = root / "inherited.pem", root / "explicit.pem"
            inherited.write_text("synthetic CA input; no TLS is performed\n")
            explicit.write_text("different synthetic CA input\n")
            for label, environment_value, cli, selected in (
                ("unset", None, [], None), ("empty", "", [], None),
                ("environment", str(inherited), [], inherited),
                ("cli-overrides-environment", str(root / "missing.pem"), ["--proxy-ca", str(explicit)], explicit),
            ):
                calls = []

                def stop_at_build(arguments, **options):
                    calls.append(arguments)
                    if arguments[1] == "version":
                        value = json.dumps({"Os": "linux", "Arch": "amd64"})
                    elif arguments[1] == "info":
                        value = json.dumps({"driver": "overlay2", "dataRoot": str(root)})
                    elif arguments[1:3] == ["image", "inspect"]:
                        value = json.dumps([image])
                    elif arguments[1] == "build":
                        return subprocess.CompletedProcess(arguments, 23, stdout="Synthetic stop before image build\n")
                    else:
                        value = ""
                    return subprocess.CompletedProcess(arguments, 0, stdout=value)

                environment = {"DOCKER_CONTEXT": "", "DOCKER_HOST": "unix:///synthetic/docker.sock"}
                if environment_value is not None:
                    environment["IDENTITY_BROWSER_PROXY_CA"] = environment_value
                destination = root / label
                printed = io.StringIO()
                with self.subTest(label=label), patch.dict(os.environ, environment, clear=True), \
                     patch.object(QUALIFY.sys, "argv", ["qualify_browser.py", "--output-directory", str(destination), *cli]), \
                     patch.object(QUALIFY, "source_evidence", return_value={"scope": "synthetic negative boundary"}), \
                     patch.object(QUALIFY.subprocess, "run", side_effect=stop_at_build), \
                     patch.object(QUALIFY.shutil, "disk_usage", return_value=SimpleNamespace(free=20 * QUALIFY.GIB)), \
                     redirect_stdout(printed), redirect_stderr(printed):
                    self.assertEqual(QUALIFY.main(), 1)
                build = next(call for call in calls if call[1] == "build")
                self.assertEqual([item for item in build if item.startswith("id=identity_proxy_ca,")],
                                 [f"id=identity_proxy_ca,src={selected}"] if selected else [])
                record = json.loads((destination / "host-qualification.json").read_text())
                self.assertEqual(record["build_network"]["ca_secret_selected"], selected is not None)
                self.assertNotIn("qualification", record)
                for private in (str(inherited), str(explicit), str(root / "missing.pem")):
                    self.assertNotIn(private, printed.getvalue())
                    self.assertNotIn(private, json.dumps(record))

    def test_missing_or_non_file_environment_ca_stops_before_output_or_docker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            private = root / "synthetic-private-author" / "private-ca" / "missing.pem"
            directory = root / "synthetic-private-directory"
            directory.mkdir()
            cases = [
                ("missing-env", private, []), ("directory-env", directory, []),
                ("missing-cli", None, ["--proxy-ca", str(private)]),
                ("directory-cli", None, ["--proxy-ca", str(directory)]),
            ]
            loop = root / "synthetic-private-loop.pem"
            try:
                loop.symlink_to(loop.name)
            except (OSError, NotImplementedError):
                pass
            else:
                cases.extend((("loop-env", loop, []), ("loop-cli", None, ["--proxy-ca", str(loop)])))
            # These regular files really exist: the selector must refuse the
            # canonical path's CSV delimiter/control bytes, not merely fail a
            # missing-file check. NUL is already rejected by pathlib itself.
            for number, character in enumerate([",", *map(chr, range(1, 32)), chr(127)]):
                unsafe = root / ("synthetic-private-ca" + character + "bundle.pem")
                unsafe.write_text("synthetic existing CA input\n")
                cases.extend(((f"unsafe-{number}-env", unsafe, []),
                              (f"unsafe-{number}-cli", None, ["--proxy-ca", str(unsafe)])))
            alias = root / "safe-ca-alias.pem"
            try:
                alias.symlink_to("synthetic-private-ca,bundle.pem")
            except (OSError, NotImplementedError):
                pass
            else:
                cases.extend((("unsafe-target-env", alias, []), ("unsafe-target-cli", None, ["--proxy-ca", str(alias)])))
            for label, value, cli in cases:
                destination = root / (label + "-evidence")
                environment = {"IDENTITY_BROWSER_PROXY_CA": str(value)} if value else {}
                printed = io.StringIO()
                with self.subTest(label=label), patch.dict(os.environ, environment, clear=True), \
                     patch.object(QUALIFY.sys, "argv", ["qualify_browser.py", "--output-directory", str(destination), *cli]), \
                     patch.object(QUALIFY.subprocess, "run") as execute, \
                     redirect_stdout(printed), redirect_stderr(printed):
                    with self.assertRaises(SystemExit) as error:
                        QUALIFY.main()
                    self.assertEqual(error.exception.code, 2)
                    execute.assert_not_called()
                self.assertFalse(destination.exists())
                self.assertIn("must select an existing regular CA bundle", printed.getvalue())
                for secret_path_part in (str(root), "synthetic-private-author", "private-ca", "synthetic-private-directory", "synthetic-private-loop"):
                    self.assertNotIn(secret_path_part, printed.getvalue())

    def test_vfs_disk_preflight_refuses_the_reproduced_small_store(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            info = {"driver": "vfs", "dataRoot": str(root)}
            with patch.object(QUALIFY.shutil, "disk_usage", return_value=SimpleNamespace(free=8 * QUALIFY.GIB)):
                result = QUALIFY.storage_preflight(info, "unix:///var/run/docker.sock", root, root)
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["minimumFreeBytes"], 16 * QUALIFY.GIB)
            with patch.object(QUALIFY.shutil, "disk_usage", return_value=SimpleNamespace(free=20 * QUALIFY.GIB)):
                self.assertEqual(QUALIFY.storage_preflight(info, "unix:///var/run/docker.sock", root, root)["status"], "passed")
            with patch.object(QUALIFY.shutil, "disk_usage", side_effect=FileNotFoundError):
                self.assertEqual(QUALIFY.storage_preflight(info, "unix:///var/run/docker.sock", root, root)["status"], "failed")
            for endpoint in ("ssh://example.invalid", "tcp://example.invalid:2375", "unix://relative", None):
                with self.subTest(endpoint=endpoint), patch.object(QUALIFY.shutil, "disk_usage") as inspect_disk:
                    self.assertEqual(QUALIFY.storage_preflight(info, endpoint, root, root)["status"], "failed")
                    inspect_disk.assert_not_called()

    def test_remote_context_cannot_use_a_coincident_local_data_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for context in ("remote", ""):
                destination = root / (context or "explicit-host")
                calls = []
                original_run = subprocess.run

                def selected_daemon(arguments, **options):
                    if arguments[0] != "docker":
                        return original_run(arguments, **options)
                    calls.append(arguments)
                    if arguments[1] == "version":
                        result = {"Os": "linux", "Arch": "amd64"}
                    elif arguments[1] == "info":
                        result = {"driver": "vfs", "dataRoot": str(root)}
                    elif arguments[1:3] == ["context", "inspect"]:
                        result = "ssh://example.invalid"
                    else:
                        raise AssertionError("A remote/unobservable preflight must stop before image acquisition")
                    return subprocess.CompletedProcess(arguments, 0, stdout=json.dumps(result))

                environment = {"DOCKER_CONTEXT": context, "DOCKER_HOST": "unix:///var/run/docker.sock" if context else "tcp://example.invalid:2375"}
                argv = ["qualify_browser.py", "--output-directory", str(destination)]
                with self.subTest(context=context), patch.dict(os.environ, environment), \
                     patch.object(QUALIFY.sys, "argv", argv), patch.object(QUALIFY.subprocess, "run", side_effect=selected_daemon), \
                     patch.object(QUALIFY.shutil, "disk_usage", return_value=SimpleNamespace(free=20 * QUALIFY.GIB)) as inspect_disk, \
                     redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(QUALIFY.main(), 1)
                    inspect_disk.assert_not_called()
                receipt = json.loads((destination / "host-qualification.json").read_text())
                self.assertEqual(receipt["storage_preflight"]["endpointKind"], "remote-or-unobservable")
                self.assertEqual(any(call[1:3] == ["context", "inspect"] for call in calls), bool(context))

    def test_failed_receipt_reuses_reserved_storage_without_creating_another_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            envelope = {"status": "failed", "failure": "Synthetic preparation storage exhaustion"}
            with QUALIFY.reserve_host_receipt(root) as reserved:
                self.assertEqual((root / "host-qualification.json").stat().st_size, QUALIFY.HOST_RECEIPT_BYTES)
                with patch.object(Path, "open", side_effect=OSError(errno.ENOSPC, "Synthetic no new file allocation")):
                    QUALIFY.write_host_receipt(reserved, root, envelope)
            self.assertEqual(json.loads((root / "host-qualification.json").read_text()), envelope)
            self.assertLess((root / "host-qualification.json").stat().st_size, QUALIFY.HOST_RECEIPT_BYTES)

    def test_local_act_receipts_do_not_claim_hosted_ci(self):
        # Exercise the real host-receipt writer in the same runner environment
        # exposed by act. Deliberately fail Docker preflight: no browser/image
        # execution is needed to prove truthful failure-context reporting.
        with tempfile.TemporaryDirectory() as temporary:
            for mode, expected in (("ci", "local-act-ci"), ("local", "local-act-local-entrypoint-replay")):
                destination = Path(temporary) / mode
                argv = ["qualify_browser.py", "--mode", mode, "--output-directory", str(destination)]
                failure = subprocess.CompletedProcess(["docker"], 19, stdout="Synthetic Docker preflight failure\n")
                original_run = subprocess.run

                def preflight_only(arguments, **options):
                    if arguments[0] == "docker":
                        return failure
                    return original_run(arguments, **options)

                with self.subTest(mode=mode), patch.dict(os.environ, {"ACT": "true", "GITHUB_ACTIONS": "true"}), \
                     patch.object(QUALIFY.sys, "argv", argv), patch.object(QUALIFY.subprocess, "run", side_effect=preflight_only), \
                     redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    self.assertEqual(QUALIFY.main(), 1)
                receipt = json.loads((destination / "host-qualification.json").read_text())
                self.assertEqual(receipt["status"], "failed")
                self.assertEqual(receipt["execution_context"], expected)
                self.assertNotIn("qualification", receipt)

    def test_output_cannot_overwrite_source_or_reuse_stale_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            source = parent / "repository"
            source.mkdir()
            clean = parent / "clean"
            clean.mkdir()
            self.assertEqual(QUALIFY.output_destination(clean, source), clean.resolve())
            stale = parent / "stale"
            stale.mkdir()
            (stale / "qualification.json").write_text("earlier evidence")
            file = parent / "file"
            file.write_text("unchanged")
            for destination in (source, source / "nested", stale, file, parent / "mount,option"):
                with self.subTest(destination=destination):
                    with self.assertRaises(ValueError):
                        QUALIFY.output_destination(destination, source)
            redirect = parent / "redirect"
            try:
                redirect.symlink_to(source, target_is_directory=True)
            except (OSError, NotImplementedError):
                pass
            else:
                with self.assertRaises(ValueError):
                    QUALIFY.output_destination(redirect, source)
            self.assertEqual(file.read_text(), "unchanged")
            self.assertEqual((stale / "qualification.json").read_text(), "earlier evidence")
            self.assertFalse((source / "nested").exists())

    def test_mutable_images_mismatched_pins_or_changed_baseline_are_rejected(self):
        profile, package, registry = inputs()
        QUALIFY.validate_profile(profile, package, registry)
        cases = []
        for key, value in (("image", "mcr.microsoft.com/playwright:latest"), ("playwright", "1.62.2"), ("packageManager", "pnpm@12.0.0"), ("platform", "linux/arm64"), ("chromium", {})):
            cases.append(dict(profile, **{key: value}))
        cases.append(dict(profile, baseline=dict(profile["baseline"], sha256="c" * 64)))
        cases.extend(dict(profile, **{key: []}) for key in ("fontPackages", "fontFiles"))
        cases.append(dict(profile, fontSourceReceipt="../external.json"))
        for key, value in (("name", "fonts-unreviewed"), ("version", "2.*"), ("url", "http://archive.ubuntu.com/font.deb"), ("url", profile["fontPackages"][0]["url"] + "?latest=true"), ("sha256", "unpinned"), ("bytes", 0), ("bytes", True)):
            candidate = copy.deepcopy(profile)
            candidate["fontPackages"][0][key] = value
            cases.append(candidate)
        candidate = copy.deepcopy(profile)
        candidate["fontPackages"][1] = copy.deepcopy(candidate["fontPackages"][0])
        cases.append(candidate)
        for key, value in (("path", "/usr/share/fonts/unreviewed.ttf"), ("sha256", "")):
            candidate = copy.deepcopy(profile)
            candidate["fontFiles"][0][key] = value
            cases.append(candidate)
        candidate = copy.deepcopy(profile)
        candidate["fontFiles"][1] = copy.deepcopy(candidate["fontFiles"][0])
        cases.append(candidate)
        for candidate in cases:
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    QUALIFY.validate_profile(candidate, package, registry)
        with self.assertRaises(ValueError):
            QUALIFY.validate_profile(profile, package, dict(registry, index_digest="sha256:" + "d" * 64))
        with self.assertRaises(ValueError):
            QUALIFY.validate_profile([], package, registry)
        source = font_source(profile)
        QUALIFY.verify_font_source_binding(profile, source)
        for key, value in (("version", "2.37-9"), ("sha256", "e" * 64), ("bytes", 101), ("architecture", "amd64")):
            candidate = copy.deepcopy(source)
            candidate["packages"][0][key] = value
            with self.subTest(font_source_key=key):
                with self.assertRaises(ValueError):
                    QUALIFY.verify_font_source_binding(profile, candidate)
        candidate = copy.deepcopy(source)
        candidate["installed_font_files"][0]["sha256"] = "e" * 64
        with self.assertRaises(ValueError):
            QUALIFY.verify_font_source_binding(profile, candidate)

    def test_pulled_config_platform_and_digest_must_match_the_registry(self):
        profile, _, registry = inputs()
        identity = {"id": "sha256:" + "c" * 64, "os": "linux", "architecture": "amd64", "user": "", "entrypoint": None, "cmd": ["bash"], "repo_digests": [profile["image"]]}
        registry.update(config_digest=identity["id"], image_config={key: identity[key] for key in ("os", "architecture", "user", "entrypoint", "cmd")})
        QUALIFY.verify_registry_binding(profile, registry, identity)
        for key, value in (("id", "sha256:" + "d" * 64), ("architecture", "arm64"), ("repo_digests", []), ("cmd", ["node"])):
            with self.subTest(key=key):
                with self.assertRaises(RuntimeError):
                    QUALIFY.verify_registry_binding(profile, registry, dict(identity, **{key: value}))

    def test_failed_or_ambiguous_receipts_cannot_count_as_qualification(self):
        profile, _, _ = inputs()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            valid = proof(directory, profile)
            line = output(valid, directory)
            self.assertEqual(QUALIFY.container_receipt("ordinary logs\n" + line, profile, directory), valid)
            for text in ("ordinary logs", line + "\n" + line, output(dict(valid, status="failed"), directory)):
                with self.subTest(text=text):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(text, profile, directory)
            for phase, key, value in (("positive", "passed", 5), ("negative", "exitCode", 0), ("negative", "expectedFailure", "timeout"), ("restored", "skipped", 1)):
                candidate = copy.deepcopy(valid)
                candidate[phase][key] = value
                with self.subTest(phase=phase, key=key):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            for missing in ("runtimes", "browser", "fonts", "settings"):
                candidate = copy.deepcopy(valid)
                candidate.pop(missing)
                with self.subTest(missing=missing):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            for field, value in (("packages", []), ("packages", [{"name": "fonts-dejavu-core", "version": "2.37-9"}]), ("packages", valid["fonts"]["packages"] * 2), ("files", valid["fonts"]["files"][1:]), ("files", valid["fonts"]["files"] * 2)):
                candidate = copy.deepcopy(valid)
                candidate["fonts"][field] = value
                with self.subTest(font_field=field, value=value):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            candidate = copy.deepcopy(valid)
            candidate["fonts"]["packages"][0]["version"] = "2.37-9"
            with self.assertRaises(RuntimeError):
                QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            candidate = copy.deepcopy(valid)
            candidate["fonts"]["files"][0]["sha256"] = "a" * 64
            with self.assertRaises(RuntimeError):
                QUALIFY.container_receipt(output(candidate, directory), profile, directory)

    def test_negative_difference_must_exist_inside_evidence_and_match_its_hash(self):
        profile, _, _ = inputs()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "evidence"
            directory.mkdir()
            valid = proof(directory, profile)
            for path, digest in (("../outside-diff.png", "a" * 64), ("negative/missing-diff.png", "a" * 64), ("negative/brand-kit-page-diff.png", "d" * 64)):
                candidate = copy.deepcopy(valid)
                candidate["negative"]["diffArtifacts"] = [{"path": path, "sha256": digest}]
                with self.subTest(path=path):
                    with self.assertRaises(RuntimeError):
                        QUALIFY.container_receipt(output(candidate, directory), profile, directory)
            line = output(valid, directory)
            (directory / "qualification.json").write_text("{}")
            with self.assertRaises(RuntimeError):
                QUALIFY.container_receipt(line, profile, directory)


if __name__ == "__main__":
    unittest.main()
