# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Candidate preparation must preserve source, expose missing facts and fail closed."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/initialize_identity.py'
FIXTURE = ROOT / 'tests/fixtures/v1/valid/minimal'
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_identity as validator


def snapshot(root):
    return {p.relative_to(root).as_posix(): ('link', os.readlink(p)) if p.is_symlink()
            else ('directory',) if p.is_dir() else ('file', p.read_bytes())
            for p in root.rglob('*')}


class InitializationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'notes.txt').write_text('unrelated consumer input')

    def request(self, value):
        path = self.root / 'request.json'
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def run_initializer(self, value, output='candidate', *, succeeds=True):
        self.request(value)
        before = snapshot(self.root)
        result = subprocess.run([sys.executable, '-I', '-S', str(SCRIPT),
            '--repository-root', str(self.root), '--request', 'request.json',
            '--output-directory', output], capture_output=True, text=True, cwd=self.root)
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stderr)
            after = snapshot(self.root)
            self.assertTrue(all(after[key] == data for key, data in before.items()))
            report = json.loads((self.root / output / 'initialization-report.json').read_text())
            for relative, record in report['files'].items():
                content = (self.root / output / relative).read_bytes()
                self.assertEqual(record, {'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)})
            return report
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(snapshot(self.root), before)
        return result

    def import_fixture(self):
        shutil.copytree(FIXTURE / '.identity', self.root / '.identity')

    def test_absent_source_produces_explicitly_incomplete_candidate(self):
        report = self.run_initializer({'schema': 'identity.initialization-request/v1'})
        self.assertEqual(report['status'], 'incomplete')
        self.assertFalse(report['sourceValid'])
        self.assertIn('project.id', report['missing'])
        candidate = self.root / 'candidate'
        self.assertFalse((self.root / '.identity').exists())
        self.assertFalse((self.root / 'assets').exists())
        approvals = json.loads((candidate / '.identity/governance/approvals.json').read_text())
        self.assertEqual(approvals['decisions'], [])
        self.assertEqual(validator.validate_identity(candidate) == [], report['sourceValid'])

    def test_v0_source_is_preserved_and_never_implicitly_migrated(self):
        source = self.root / '.identity'
        source.mkdir()
        (source / 'identity.toml').write_text('schema = "identity.intent/v0"\n')
        self.run_initializer({'schema': 'identity.initialization-request/v1'})
        self.assertFalse((source / 'identity.json').exists())
        self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': '.'},
                             output='imported', succeeds=False)

    def test_validated_v1_import_preserves_exact_approval_and_source_bytes(self):
        self.import_fixture()
        original = snapshot(self.root / '.identity')
        report = self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': '.'})
        self.assertEqual(report['status'], 'ready-for-review')
        self.assertTrue(report['sourceValid'])
        self.assertEqual(report['missing'], [])
        self.assertEqual(snapshot(self.root / 'candidate/.identity'), original)
        self.assertEqual(validator.validate_identity(self.root / 'candidate'), [])
        self.assertNotIn('notes.txt', report['files'])

    def test_external_declared_input_is_copied_at_its_relative_path(self):
        self.import_fixture()
        shutil.move(self.root / '.identity/brief.md', self.root / 'brief.md')
        path = self.root / '.identity/identity.json'
        project = json.loads(path.read_text())
        project['documents']['brief'] = 'brief.md'
        path.write_text(json.dumps(project))
        report = self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': '.'})
        self.assertTrue(report['sourceValid'])
        self.assertEqual((self.root / 'candidate/brief.md').read_bytes(), (self.root / 'brief.md').read_bytes())

    def test_supplied_facts_layers_and_targets_are_preserved_without_invented_approval(self):
        supplied = self.root / 'supplied'
        shutil.copytree(FIXTURE / '.identity', supplied / '.identity')
        project = json.loads((supplied / '.identity/identity.json').read_text())
        request = {'schema': 'identity.initialization-request/v1', 'project': project['project'],
                   'layers': [{key: layer[key] for key in ('id', 'kind', 'priority')} |
                              {'tokens': 'supplied/' + layer['tokens']} for layer in project['layers']],
                   'targets': 'supplied/' + project['documents']['targets']}
        report = self.run_initializer(request)
        self.assertEqual(report['status'], 'incomplete')
        result = json.loads((self.root / 'candidate/.identity/identity.json').read_text())
        self.assertEqual(result['project'], project['project'])
        for source, target in zip(project['layers'], result['layers']):
            content = (supplied / source['tokens']).read_bytes()
            self.assertEqual((self.root / 'candidate' / target['tokens']).read_bytes(), content)
            self.assertEqual(target['sha256'], hashlib.sha256(content).hexdigest())
        self.assertTrue(report['missing'])

    def test_malformed_unknown_and_unsupported_requests_preserve_all_inputs(self):
        cases = ['{"schema":"identity.initialization-request/v1","schema":"duplicate"}',
                 '{"schema":"identity.initialization-request/v1","project":{"id":NaN}}',
                 {'schema': 'identity.initialization-request/v2'},
                 {'schema': 'identity.initialization-request/v1', 'unknown': True},
                 {'schema': 'identity.initialization-request/v1', 'sourceRoot': '.', 'project': {}},
                 {'schema': 'identity.initialization-request/v1', 'project': {'id': '../unsafe'}},
                 {'schema': 'identity.initialization-request/v1', 'project': {'rights': 'invented'}}]
        for value in cases:
            with self.subTest(request=value):
                self.run_initializer(value, succeeds=False)

    def test_invalid_or_unsupported_imports_never_publish_a_candidate(self):
        self.import_fixture()
        path = self.root / '.identity/identity.json'
        project = json.loads(path.read_text())
        for schema in ('identity.project/v0', 'identity.project/v2'):
            project['schema'] = schema
            path.write_text(json.dumps(project))
            self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': '.'}, succeeds=False)
        project['schema'] = 'identity.project/v1'
        path.write_text(json.dumps(project))
        (self.root / '.identity/governance/approvals.json').unlink()
        self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': '.'}, succeeds=False)

    def test_unsupported_profile_is_rejected(self):
        (self.root / 'targets.json').write_text(json.dumps({'$schema': 'local',
            'schema': 'identity.targets/v1', 'enabled': [{'id': 'core', 'version': '99.0.0'}], 'inapplicable': []}))
        self.run_initializer({'schema': 'identity.initialization-request/v1', 'targets': 'targets.json'}, succeeds=False)

    def test_unsafe_reserved_missing_parent_and_existing_destinations_are_refused(self):
        (self.root / 'existing').mkdir()
        for path in ('.identity/candidate', '.git/candidate', 'assets/candidate', '../escape',
                     'candidate/../escape', 'missing-parent/candidate', 'existing', r'C:\candidate'):
            with self.subTest(path=path):
                self.run_initializer({'schema': 'identity.initialization-request/v1'}, output=path, succeeds=False)

    def test_repeat_invocation_is_not_an_overwrite(self):
        request = {'schema': 'identity.initialization-request/v1'}
        self.run_initializer(request)
        self.run_initializer(request, succeeds=False)

    def test_output_may_not_overlap_a_supplied_import(self):
        shutil.copytree(FIXTURE, self.root / 'consumer')
        self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': 'consumer'},
                             output='consumer/candidate', succeeds=False)

    def test_symlink_inputs_sources_and_output_parents_fail_without_writes(self):
        try:
            (self.root / 'linked').symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('symlink creation unavailable on this platform')
        self.run_initializer({'schema': 'identity.initialization-request/v1'}, output='linked/candidate', succeeds=False)
        self.run_initializer({'schema': 'identity.initialization-request/v1', 'sourceRoot': 'linked'}, succeeds=False)
        self.request({'schema': 'identity.initialization-request/v1'})
        (self.root / 'request-link.json').symlink_to(self.root / 'request.json')
        before = snapshot(self.root)
        result = subprocess.run([sys.executable, '-I', '-S', str(SCRIPT), '--repository-root', str(self.root),
            '--request', 'request-link.json', '--output-directory', 'candidate'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.root), before)

    def test_preparation_is_deterministic_and_fingerprints_the_implementation(self):
        request = {'schema': 'identity.initialization-request/v1'}
        first = self.run_initializer(request, output='first')
        second = self.run_initializer(request, output='second')
        self.assertEqual(first, second)
        self.assertEqual(snapshot(self.root / 'first'), snapshot(self.root / 'second'))
        self.assertEqual(first['implementation']['initializerSha256'], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(first['implementation']['validatorSha256'], hashlib.sha256((ROOT / 'scripts/validate_identity.py').read_bytes()).hexdigest())

    def test_publication_failure_retains_only_explicit_partial_output(self):
        spec = importlib.util.spec_from_file_location('initializer_failure', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.request({'schema': 'identity.initialization-request/v1'})
        before = snapshot(self.root)
        move = shutil.move
        calls = 0
        def fail_after_source(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('injected final publication failure')
            return move(source, destination)
        with mock.patch.object(module.shutil, 'move', side_effect=fail_after_source):
            with self.assertRaises(OSError):
                module.prepare(argparse.Namespace(repository_root=str(self.root), request='request.json', output_directory='candidate'))
        after = snapshot(self.root)
        self.assertTrue(all(after[key] == data for key, data in before.items()))
        self.assertTrue((self.root / 'candidate/.identity').is_dir())
        self.assertFalse((self.root / 'candidate/initialization-report.json').exists())
        self.assertFalse(list(self.root.glob('.identity-init-*')))


if __name__ == '__main__':
    unittest.main()
