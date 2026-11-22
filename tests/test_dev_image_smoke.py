"""Refusal controls for actual repeated setup in the image qualifier."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("identity_dev_image_smoke", ROOT / "dev/qualification/smoke.py")
SMOKE = importlib.util.module_from_spec(SPEC)
with mock.patch.object(sys, "path", [str(ROOT / "dev/qualification"), *sys.path]):
    SPEC.loader.exec_module(SMOKE)


class RepeatSetupQualificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "renderer").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src/lib.rs").write_text("// product source\n")
        fixture = self.root / "tests/fixtures/v1/valid/minimal/.identity"
        fixture.mkdir(parents=True)
        (fixture / "identity.json").write_text('{"canonical":true}\n')
        for name in ("Cargo.toml", "Cargo.lock", "renderer/pnpm-lock.yaml"):
            (self.root / name).write_text("unchanged\n")
        (self.root / "rust-toolchain.toml").write_text('[toolchain]\nchannel = "1.97.1"\n')
        (self.root / "renderer/package.json").write_text(json.dumps({"packageManager": "pnpm@11.21.0"}))

    def runner(self, arguments, **_kwargs):
        if arguments == ["rustc", "--version"]:
            return "rustc 1.97.1 (qualification)"
        if arguments == ["corepack", "pnpm", "--version"]:
            return "11.21.0"
        self.assertEqual(arguments, ["bash", "scripts/dev-env.sh", "setup"])
        return "actual helper double completed"

    def test_success_requires_setup_and_post_setup_pins_with_preserved_inputs(self):
        before = SMOKE.inventory(self.root)
        with mock.patch.object(SMOKE, "run", side_effect=self.runner) as runner:
            receipt = SMOKE.repeat_setup(self.root)
        self.assertEqual(runner.call_args_list[0], mock.call(["bash", "scripts/dev-env.sh", "setup"], cwd=self.root))
        self.assertEqual(runner.call_count, 3)
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(receipt["runtime_pins_preserved"], {"rustc": "1.97.1", "pnpm": "11.21.0"})
        self.assertEqual(SMOKE.inventory(self.root), before)
        self.assertEqual(set(receipt["source_inputs_sha256"]), set(before))

    def test_successful_setup_cannot_rewrite_a_lockfile(self):
        def mutate(arguments, **kwargs):
            if arguments == ["bash", "scripts/dev-env.sh", "setup"]:
                (self.root / "Cargo.lock").write_text("silently changed by setup\n")
            return self.runner(arguments, **kwargs)

        with mock.patch.object(SMOKE, "run", side_effect=mutate) as runner:
            with self.assertRaisesRegex(RuntimeError, "changed a qualification source"):
                SMOKE.repeat_setup(self.root)
        self.assertEqual(runner.call_count, 1)

    def test_failed_setup_and_post_setup_pin_drift_never_emit_success(self):
        with mock.patch.object(SMOKE, "run", side_effect=RuntimeError("setup failed")):
            with self.assertRaisesRegex(RuntimeError, "setup failed"):
                SMOKE.repeat_setup(self.root)
        for changed_command, incorrect in ((["rustc", "--version"], "rustc 99.0.0 (wrong)"), (["corepack", "pnpm", "--version"], "99.0.0")):
            with self.subTest(command=changed_command):
                def drift(arguments, **kwargs):
                    return incorrect if arguments == changed_command else self.runner(arguments, **kwargs)
                with mock.patch.object(SMOKE, "run", side_effect=drift):
                    with self.assertRaisesRegex(RuntimeError, "runtime pins"):
                        SMOKE.repeat_setup(self.root)

    def test_setup_cannot_change_product_or_canonical_fixture_source(self):
        for relative in ("src/lib.rs", "tests/fixtures/v1/valid/minimal/.identity/identity.json"):
            with self.subTest(path=relative):
                before = (self.root / relative).read_bytes()
                def mutate(arguments, **kwargs):
                    if arguments == ["bash", "scripts/dev-env.sh", "setup"]:
                        (self.root / relative).write_text("changed source\n")
                    return self.runner(arguments, **kwargs)
                with mock.patch.object(SMOKE, "run", side_effect=mutate):
                    with self.assertRaisesRegex(RuntimeError, "changed a qualification source"):
                        SMOKE.repeat_setup(self.root)
                (self.root / relative).write_bytes(before)


if __name__ == "__main__":
    unittest.main()
