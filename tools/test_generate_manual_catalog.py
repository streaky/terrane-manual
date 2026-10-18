"""Behavioral regressions for authored manual YAML validation."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from generate_manual_catalog import load_yaml


class ManualYamlValidationTests(unittest.TestCase):
    def test_nested_duplicates_report_both_source_locations(self):
        for first, second in [("markdown", "markdown"), ("markdown", "'markdown'"), ("0x10", "16")]:
            with self.subTest(keys=(first, second)), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "record.yaml"
                path.write_text(f"blocks:\n  - type: example\n    {first}: null\n    {second}: changed\n", encoding="utf-8")
                with self.assertRaises(yaml.constructor.ConstructorError) as raised:
                    load_yaml(path)
                message = str(raised.exception)
                self.assertIn(str(path), message)
                self.assertIn("duplicate key", message)
                self.assertIn("line 3", message)
                self.assertIn("line 4", message)

    def test_aliases_and_merge_overrides_remain_supported(self):
        source = """base: &base
  title: original
  enabled: true
defaults: &defaults
  <<: *base
  title: default
page:
  <<: *defaults
  title: page
  '<<': literal
other:
  <<: *base
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.yaml"
            path.write_text(source, encoding="utf-8")
            value = load_yaml(path)
        self.assertEqual(value["page"], {"title": "page", "enabled": True, "<<": "literal"})
        self.assertEqual(value["defaults"], {"title": "default", "enabled": True})
        self.assertEqual(value["other"], value["base"])

    def test_generation_and_check_reject_duplicates_without_changing_files(self):
        tools = Path(__file__).resolve().parent
        for check in [False, True]:
            for invalid_manifest in [False, True]:
                with self.subTest(check=check, manifest=invalid_manifest), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    (root / "tools").mkdir()
                    (root / "reference").mkdir()
                    (root / "generated").mkdir()
                    for filename in ["generate_manual_catalog.py", "format_manual_content.py"]:
                        shutil.copyfile(tools / filename, root / "tools" / filename)
                    manifest = root / "reference/manual.yaml"
                    manifest.write_text("navigation:\n  - group: Test\n    children:\n      - source: record.yaml\n", encoding="utf-8")
                    record = root / "reference/record.yaml"
                    record.write_text("id: test\nblocks:\n  - markdown: null\n    markdown: null\n", encoding="utf-8")
                    if invalid_manifest:
                        manifest.write_text("navigation: []\nnavigation: []\n", encoding="utf-8")
                    artifact = root / "generated/catalog.yaml"
                    artifact.write_text("existing: unchanged\n", encoding="utf-8")
                    originals = {path: path.read_bytes() for path in [manifest, record, artifact]}
                    command = [sys.executable, str(root / "tools/generate_manual_catalog.py")]
                    if check:
                        command.append("--check")
                    # No formatter on PATH: duplicate validation must run before formatting.
                    result = subprocess.run(command, capture_output=True, text=True, env={"PATH": ""}, timeout=10)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("duplicate key", result.stderr)
                    self.assertIn(str(manifest if invalid_manifest else record), result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual({path: path.read_bytes() for path in originals}, originals)


if __name__ == "__main__":
    unittest.main()
