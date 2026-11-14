# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Exercise real shell/Make/Task routing with bounded synthetic tool protocols."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TASK = shutil.which('task')
MAKE = shutil.which('make')
PROTOCOL = '''#!{python}
import json, os, pathlib, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
with open(os.environ['IDENTITY_PROTOCOL_TRACE'], 'a') as trace:
    trace.write(json.dumps({{'tool': name, 'args': args, 'cwd': os.getcwd(),
        'prefix': os.environ.get('IDENTITY_DEV_PREFIX'),
        'cargoHome': os.environ.get('CARGO_HOME'),
        'corepackHome': os.environ.get('COREPACK_HOME'),
        'storeDir': os.environ.get('pnpm_config_store_dir'),
        'verifyDeps': os.environ.get('pnpm_config_verify_deps_before_run'),
        'globalVirtualStore': os.environ.get('pnpm_config_enable_global_virtual_store'),
        'path': os.environ['PATH']}}) + '\\n')
if name == 'corepack' and args == ['pnpm', '--version']:
    print(os.environ.get('IDENTITY_PROTOCOL_PNPM', '11.21.0'))
'''


@unittest.skipUnless(os.name == 'posix', 'POSIX installer harness; native CLI platforms are separate')
class EntryPointTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'consumer'
        self.root.mkdir()
        for name in ('scripts/dev-env.sh', 'Makefile', 'Taskfile.yml', 'rust-toolchain.toml', 'renderer/package.json'):
            output = self.root / name
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, output)
        (self.root / 'scripts/build_identity_validator.py').write_text('pass\n')
        (self.root / 'unrelated.txt').write_text('preserve this consumer file')
        self.inputs = self.inventory()
        fake = self.base / 'tools'
        fake.mkdir()
        for name in ('node', 'corepack', 'rustup', 'cargo', 'cc', 'curl'):
            path = fake / name
            path.write_text(PROTOCOL.format(python=sys.executable))
            path.chmod(0o755)
        self.prefix = self.base / 'owned-cache'
        self.trace = self.base / 'trace.jsonl'
        self.environment = dict(os.environ, PATH=str(fake) + os.pathsep + os.environ['PATH'],
            IDENTITY_DEV_PREFIX=str(self.prefix), IDENTITY_PROTOCOL_TRACE=str(self.trace),
            CARGO_HOME=str(self.prefix / 'cargo'), RUSTUP_HOME=str(self.prefix / 'rustup'),
            COREPACK_HOME=str(self.prefix / 'corepack-cache'))
        self.environment.pop('npm_config_store_dir', None)
        self.environment.pop('pnpm_config_store_dir', None)
        self.environment.pop('pnpm_config_verify_deps_before_run', None)
        self.environment.pop('pnpm_config_enable_global_virtual_store', None)
        self.environment.pop('IDENTITY_PROTOCOL_PNPM', None)

    def inventory(self):
        return {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob('*') if path.is_file()}

    def frontends(self, operation, arguments=()):
        commands = [('standalone', ['bash', 'scripts/dev-env.sh', operation, *arguments])]
        if MAKE:
            commands.append(('Make', [MAKE, operation, 'DEV_ARGS=' + ' '.join(arguments)]))
        if TASK:
            commands.append(('Task', [TASK, operation, '--', *arguments]))
        return commands

    def invoke(self, command):
        return subprocess.run(command, cwd=self.root, env=self.environment, capture_output=True, text=True)

    def records(self):
        return [json.loads(line) for line in self.trace.read_text().splitlines()] if self.trace.exists() else []

    def test_ci_has_actual_make_and_task_frontends(self):
        if os.environ.get('IDENTITY_REQUIRE_FRONTENDS') == '1':
            self.assertIsNotNone(MAKE, 'CI requires Make coverage')
            self.assertIsNotNone(TASK, 'CI requires Task coverage')

    def test_repeated_setup_uses_frozen_tools_activation_and_owned_cache(self):
        for label, command in self.frontends('setup'):
            with self.subTest(frontend=label):
                self.trace.unlink(missing_ok=True)
                for _ in range(2):
                    result = self.invoke(command)
                    self.assertEqual(result.returncode, 0, result.stderr)
                records = self.records()
                installs = [row for row in records if row['tool'] == 'corepack' and row['args'][:2] == ['pnpm', 'install']]
                self.assertEqual(len(installs), 2)
                self.assertTrue(all(row['args'] == ['pnpm', 'install', '--frozen-lockfile', '--store-dir', str(self.prefix / 'pnpm-store')] for row in installs))
                self.assertEqual(sum(row['tool'] == 'cargo' and row['args'] == ['fetch', '--locked'] for row in records), 2)
                self.assertEqual(sum(row['tool'] == 'cargo' and row['args'] == ['build', '--locked'] for row in records), 2)
                for row in records:
                    self.assertEqual(row['prefix'], str(self.prefix))
                    self.assertEqual(row['cargoHome'], str(self.prefix / 'cargo'))
                    self.assertEqual(row['corepackHome'], str(self.prefix / 'corepack-cache'))
                    self.assertEqual(row['storeDir'], str(self.prefix / 'pnpm-store'))
                    self.assertEqual(row['verifyDeps'], 'error')
                    self.assertEqual(row['globalVirtualStore'], 'false')
                    self.assertTrue(row['path'].startswith(str(self.prefix / 'bin') + os.pathsep))
                self.assertEqual(self.inventory(), self.inputs)
                self.assertEqual((self.prefix / 'bin').stat().st_uid, os.getuid())

    def test_browser_arguments_reach_the_shared_helper_without_installing(self):
        for label, command in self.frontends('browsers', ['--dry-run', '--with-deps']):
            with self.subTest(frontend=label):
                self.trace.unlink(missing_ok=True)
                result = self.invoke(command)
                self.assertEqual(result.returncode, 0, result.stderr)
                calls = [row for row in self.records() if row['tool'] == 'corepack']
                self.assertEqual(calls[-1]['args'], ['pnpm', 'exec', 'playwright', 'install', '--dry-run', '--with-deps', 'chromium'])
                self.assertEqual(self.inventory(), self.inputs)

    def test_wrong_activated_package_manager_fails_before_dependency_or_build_work(self):
        self.environment['IDENTITY_PROTOCOL_PNPM'] = '999.0.0'
        for label, command in self.frontends('setup'):
            with self.subTest(frontend=label):
                self.trace.unlink(missing_ok=True)
                result = self.invoke(command)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Activated pnpm 999.0.0 differs from required pnpm@11.21.0', result.stderr)
                self.assertFalse(any(row['tool'] == 'cargo' or row['args'][:2] == ['pnpm', 'install'] for row in self.records()))
                self.assertEqual(self.inventory(), self.inputs)

    def test_unknown_dispatch_fails_without_touching_consumer_files(self):
        result = self.invoke(['bash', 'scripts/dev-env.sh', 'unsupported-operation'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('Unknown command', result.stderr)
        self.assertEqual(self.inventory(), self.inputs)


if __name__ == '__main__':
    unittest.main()
