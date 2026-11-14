"""Synthetic regression controls; no workflow dispatch or provider writes."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("retired_guidance", Path(__file__).resolve().parents[1] / "scripts/verify_retired_guidance.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class RetirementTests(unittest.TestCase):
    def test_current_repository_preserves_retirement(self):
        self.assertEqual(module.verify(Path(__file__).resolve().parents[1]), [])

    def test_reintroduced_definitions_and_renamed_branch_writers_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows = root / ".github/workflows"
            workflows.mkdir(parents=True)
            for name, body in (("refine-guidance-docs.yml", "name: old"),
                               ("refine-guidance-docs-v2.yaml", "name: old"),
                               ("renamed.yml", "ref: feat/13-brand-guidance-v1")):
                with self.subTest(name=name):
                    path = workflows / name
                    path.write_text(body)
                    self.assertEqual(len(module.verify(root)), 1)
                    path.unlink()

    def test_release_writers_and_historical_documentation_remain_allowed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/release.yml").write_text("permissions:\n  contents: write\n")
            (root / ".github/workflows/history.md").write_text(module.HISTORICAL_BRANCH)
            self.assertEqual(module.verify(root), [])
