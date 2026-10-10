# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Exercise consumer alias composition and source-bound live byte verification."""

import importlib.util
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock
from urllib import error, request

SPEC = importlib.util.spec_from_file_location(
    "publication", Path(__file__).parents[1] / "scripts/identity_decisions_publication.py")
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site, self.evidence = self.root / "site", self.root / "evidence"
        self.evidence.mkdir()
        self.consumer = {"repository": "egohygiene/identity", "revision": "a" * 40}
        self.put("index.html", b"release-bound Brand Kit")
        self.put("brand-kit/index.html", b"Brand Kit alias")
        self.put(".nojekyll", b"")
        self.put("CNAME", b"identity.egohygiene.io")
        baseline = {"consumer": self.consumer, "files": [
            self.record(path) for path in ("index.html", "brand-kit/index.html", ".nojekyll", "CNAME")]}
        self.write_json("consumer-route-baseline.json", baseline)
        self.write_json("source-binding.json", {"repository": "egohygiene/identity",
            "intelligence_revision": "a" * 40, "relay_revision": "b" * 40})
        self.put("intelligence/decisions/index.html", b"accepted Decisions")
        self.put("intelligence/index.html", b"Intelligence home")
        manifest = {"consumer": self.consumer, "generator": {"revision": "b" * 40},
            "bundle": {"files": [self.record("decisions/index.html", "intelligence"),
                                  self.record("index.html", "intelligence")]}}
        self.put(publication.MANIFEST, json.dumps(manifest).encode())

    def put(self, path, data):
        destination = self.site / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    def record(self, path, prefix=""):
        data = (self.site / prefix / path).read_bytes()
        return {"path": path, "bytes": len(data), "sha256": publication.digest(data)}

    def write_json(self, path, data):
        (self.evidence / path).write_text(json.dumps(data))

    def report(self):
        return json.loads((self.evidence / "live-verification.json").read_text())

    def run_live(self, effect=None, attempts=1):
        publication.compose(self.site)
        with mock.patch.object(publication, "fetch", side_effect=effect or self.served) as fetch:
            result = publication.verify_live(self.site, self.evidence, attempts=attempts, delay=0)
        return result, fetch

    def served(self, path, size, timeout):
        return (self.site / path).read_bytes()

    def test_compose_preserves_existing_bytes_and_rejects_collision(self):
        before = {p: p.read_bytes() for p in self.site.rglob("*") if p.is_file()}
        publication.compose(self.site)
        self.assertEqual((self.site / publication.ALIAS).read_bytes(), publication.ALIAS_HTML)
        self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))
        with self.assertRaisesRegex(ValueError, "already exists"):
            publication.compose(self.site)

    def test_compose_requires_target_and_rejects_symlinks_and_escape(self):
        target = self.site / "intelligence/decisions/index.html"
        target.unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            publication.compose(self.site)
        target.symlink_to(self.site / "index.html")
        with self.assertRaisesRegex(ValueError, "symbolic link"):
            publication.compose(self.site)
        for path in ("../outside", "/outside", "a/../b", "a\\b", "a//b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                publication.safe_path(self.site, path)

    def test_all_files_and_manifest_are_checked_before_success(self):
        passed, fetch = self.run_live()
        self.assertTrue(passed)
        paths = [call.args[0] for call in fetch.call_args_list]
        self.assertEqual(paths[0], publication.MANIFEST)
        self.assertEqual(set(paths), {p.relative_to(self.site).as_posix()
                                    for p in self.site.rglob("*") if p.is_file()})
        self.assertEqual(self.report()["expected_source"], self.consumer)
        self.assertEqual(self.report()["result"], "passed")

    def test_tampered_intelligence_and_brand_kit_bytes_fail(self):
        publication.compose(self.site)
        for corrupt in ("intelligence/decisions/index.html", "index.html", publication.ALIAS):
            with self.subTest(path=corrupt), mock.patch.object(publication, "fetch", side_effect=
                    lambda path, size, timeout: b"tampered" if path == corrupt else self.served(path, size, timeout)):
                self.assertFalse(publication.verify_live(self.site, self.evidence, attempts=1))
                failures = [r["path"] for r in self.report()["checked_files"] if r["result"] == "failed"]
                self.assertEqual(failures, [corrupt])
                self.assertEqual(self.report()["result"], "failed")

    def test_source_manifest_drift_fails_before_network(self):
        self.write_json("source-binding.json", {"repository": "egohygiene/identity",
            "intelligence_revision": "c" * 40, "relay_revision": "b" * 40})
        passed, fetch = self.run_live()
        self.assertFalse(passed)
        fetch.assert_not_called()
        self.assertIn("revision drift", self.report()["error"])

    def test_local_bundle_drift_fails_before_network(self):
        self.put("intelligence/decisions/index.html", b"local changed bytes")
        passed, fetch = self.run_live()
        self.assertFalse(passed)
        fetch.assert_not_called()
        self.assertIn("local composition drift", self.report()["error"])

    def test_manifest_readiness_retry_precedes_remaining_files(self):
        calls = []
        def eventual(path, size, timeout):
            calls.append(path)
            return b"previous deployment" if len(calls) == 1 else self.served(path, size, timeout)
        passed, _ = self.run_live(eventual, attempts=3)
        self.assertTrue(passed)
        self.assertEqual(calls[:2], [publication.MANIFEST] * 2)
        self.assertEqual(self.report()["attempts"], 2)

    def test_unavailable_pages_control_files_are_explicitly_optional(self):
        def served(path, size, timeout):
            if path in (".nojekyll", "CNAME"):
                raise error.HTTPError(publication.CANONICAL_URL + path, 404, "not served", {}, None)
            return self.served(path, size, timeout)
        passed, _ = self.run_live(served)
        self.assertTrue(passed)
        unavailable = [r for r in self.report()["checked_files"] if r["result"] == "unavailable"]
        self.assertEqual({r["path"] for r in unavailable}, {".nojekyll", "CNAME"})
        self.assertTrue(all(r["optional"] and r["http_status"] == 404 for r in unavailable))

    def test_network_failure_is_bounded_and_reported(self):
        passed, fetch = self.run_live(lambda *args: (_ for _ in ()).throw(TimeoutError("timeout")), attempts=3)
        self.assertFalse(passed)
        self.assertEqual(fetch.call_count, 3)
        self.assertEqual(self.report()["attempts"], 3)

    def test_report_cannot_be_written_into_site(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            publication.verify_live(self.site, self.site / "evidence", attempts=1)

    def test_redirect_rejects_other_origins_and_https_downgrade(self):
        handler = publication.CanonicalRedirect()
        req = request.Request(publication.CANONICAL_URL)
        for url in ("http://identity.egohygiene.io/", "https://example.org/",
                    "https://identity.egohygiene.io@evil.example/", "https://identity.egohygiene.io:444/"):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "canonical"):
                handler.redirect_request(req, None, 302, "redirect", {}, url)

    def test_fetch_quotes_reserved_path_characters(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.geturl.return_value = publication.CANONICAL_URL + "assets/a%3F%23%27.png"
        response.read1.side_effect = [b"image", b""]
        with mock.patch.object(publication.request, "build_opener") as opener:
            opener.return_value.open.return_value = response
            self.assertEqual(publication.fetch("assets/a?#'.png", 5, 10), b"image")
        req = opener.return_value.open.call_args.args[0]
        self.assertEqual(req.full_url, publication.CANONICAL_URL + "assets/a%3F%23%27.png")
        self.assertEqual(response.read1.call_args_list, [mock.call(6), mock.call(1)])

    def rollback_record(self, paths=("index.html", "brand-kit/index.html")):
        files = [self.record(path) for path in paths]
        data = {"schema": "identity.decisions-publication-rollback/v1",
                "deploymentUrl": publication.CANONICAL_URL, "consumerRevision": "a" * 40,
                "capturedFiles": len(files), "files": files}
        return self.save_rollback_record(data)

    def save_rollback_record(self, data):
        inventory = (json.dumps(data["files"], ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode()
        data["siteDigest"] = publication.digest(inventory)
        path = self.root / "rollback.json"
        path.write_text(json.dumps(data))
        return path

    def test_rollback_archive_is_deterministic_and_preserves_exact_record(self):
        record = self.rollback_record()
        with mock.patch.object(publication, "fetch", side_effect=self.served):
            publication.capture_rollback(record, self.evidence, self.site)
            other = self.root / "other-evidence"
            publication.capture_rollback(record, other, self.site)
        archive = self.evidence / "rollback-site.tar"
        self.assertEqual(archive.read_bytes(), (other / archive.name).read_bytes())
        self.assertEqual((self.evidence / "rollback-record.json").read_bytes(), record.read_bytes())
        with tarfile.open(archive) as captured:
            self.assertEqual(captured.getnames(), ["index.html", "brand-kit/index.html"])
            self.assertEqual(captured.extractfile("index.html").read(), (self.site / "index.html").read_bytes())
        self.assertFalse(list(self.evidence.glob(".rollback-*")))

    def test_rollback_tampered_old_file_leaves_no_archive(self):
        record = self.rollback_record(paths=("index.html",))
        with mock.patch.object(publication, "fetch", return_value=b"changed") as fetch, self.assertRaisesRegex(ValueError, "differ"):
            publication.capture_rollback(record, self.evidence, self.site)
        self.assertEqual(fetch.call_count, 1)
        self.assertFalse((self.evidence / "rollback-site.tar").exists())
        self.assertFalse((self.evidence / "rollback-record.json").exists())
        self.assertFalse(list(self.evidence.glob(".rollback-*")))

    def test_rollback_retries_transient_timeout_then_retains_exact_bytes(self):
        record = self.rollback_record(paths=("index.html",))
        expected = (self.site / "index.html").read_bytes()
        with mock.patch.object(publication, "fetch", side_effect=[TimeoutError("timeout"), expected]) as fetch:
            publication.capture_rollback(record, self.evidence, self.site)
        self.assertEqual(fetch.call_count, 2)
        self.assertTrue(all(0 < call.args[2] <= 30 for call in fetch.call_args_list))
        with tarfile.open(self.evidence / "rollback-site.tar") as captured:
            self.assertEqual(captured.extractfile("index.html").read(), expected)

    def test_rollback_bounds_transient_retries_and_rejects_permanent_errors(self):
        record = self.rollback_record(paths=("index.html",))
        for status, expected_attempts in ((429, 3), (503, 3), (404, 1)):
            problem = error.HTTPError(publication.CANONICAL_URL, status, "unavailable", {}, None)
            with self.subTest(status=status), mock.patch.object(publication, "fetch", side_effect=problem) as fetch:
                with self.assertRaises(error.HTTPError):
                    publication.capture_rollback(record, self.evidence, self.site)
                self.assertEqual(fetch.call_count, expected_attempts)
                self.assertFalse((self.evidence / "rollback-site.tar").exists())

    def test_rollback_rejects_path_escape_and_symlink_before_fetch(self):
        record = self.rollback_record()
        data = json.loads(record.read_text())
        data["files"][0]["path"] = "../outside"
        self.save_rollback_record(data)
        with mock.patch.object(publication, "fetch") as fetch, self.assertRaisesRegex(ValueError, "unsafe"):
            publication.capture_rollback(record, self.evidence, self.site)
        fetch.assert_not_called()
        record = self.rollback_record()
        (self.evidence / "rollback-site.tar").symlink_to(self.root / "outside")
        with mock.patch.object(publication, "fetch") as fetch, self.assertRaisesRegex(ValueError, "symbolic link"):
            publication.capture_rollback(record, self.evidence, self.site)
        fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
