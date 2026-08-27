# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Tests for local Markdown-link verification."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VERIFY_DOCS = REPOSITORY_ROOT / "scripts" / "verify_docs.py"


def load_verify_docs_module():
    specification = importlib.util.spec_from_file_location("verify_docs", VERIFY_DOCS)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class VerifyDocsTests(unittest.TestCase):
    def test_repository_documentation_has_no_broken_relative_links(self) -> None:
        verify_docs = load_verify_docs_module()
        self.assertEqual(verify_docs.verify_repository(REPOSITORY_ROOT), [])

    def test_missing_relative_target_is_reported(self) -> None:
        verify_docs = load_verify_docs_module()
        with tempfile.TemporaryDirectory() as temporary:
            document = Path(temporary) / "README.md"
            document.write_text("[missing](does-not-exist.md)\n", encoding="utf-8")
            errors = verify_docs.verify_markdown_file(document)

        self.assertEqual(len(errors), 1)
        self.assertIn("missing link target", errors[0])


if __name__ == "__main__":
    unittest.main()
