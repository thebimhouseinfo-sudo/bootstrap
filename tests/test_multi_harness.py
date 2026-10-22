#!/usr/bin/env python3
"""Multi-host installer integration and Planner skill packaging regression."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"
TEMPLATE = ROOT / "project-template"

def invoke(*args):
    return subprocess.run([sys.executable, str(INSTALL), *map(str, args)],
                          capture_output=True, text=True, timeout=45)

class MultiHarnessTests(unittest.TestCase):
    def test_new_project_has_both_native_adapters_and_one_shared_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            args = ["--target", root, "--tier", "Standard", "--runtime", "codex",
                    "--runtime", "claude", "--config-git", "local", "--staged"]
            preview = invoke(*args)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            installed = invoke(*args, "--apply")
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            self.assertTrue((root / ".codex/agents/planner.md").is_file())
            self.assertTrue((root / ".claude/agents/planner.md").is_file())
            for skill in ("challenge-feasibility", "write-criteria"):
                self.assertTrue((root / ".agents/skills" / skill / "SKILL.md").is_file())
                self.assertTrue((root / ".claude/skills" / skill / "SKILL.md").is_file())
            manifest = json.loads((root / "harness/.bootstrap-manifest.json").read_text())
            self.assertEqual(manifest["runtimes"], ["codex", "claude"])
            state = json.loads((root / "harness/setup-state.json").read_text())
            self.assertEqual(state["runtime"], "codex")

    def test_explicit_extension_preserves_original_primary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            args = ["--target", root, "--tier", "Standard", "--runtime", "codex"]
            self.assertEqual(invoke(*args, "--apply").returncode, 0)
            extended = invoke(*args, "--runtime", "claude", "--apply")
            self.assertEqual(extended.returncode, 0, extended.stdout + extended.stderr)
            self.assertTrue((root / ".claude/agents/planner.md").exists())
            manifest = json.loads((root / "harness/.bootstrap-manifest.json").read_text())
            self.assertEqual(manifest["runtimes"], ["codex", "claude"])
            forbidden = invoke("--target", root, "--tier", "Standard",
                               "--runtime", "claude", "--runtime", "codex", "--apply")
            self.assertNotEqual(forbidden.returncode, 0)

    def test_generic_cannot_mix_with_native(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = invoke("--target", tmp, "--tier", "Standard",
                          "--runtime", "codex", "--runtime", "generic", "--target-app", "other")
            self.assertNotEqual(proc.returncode, 0)

if __name__ == "__main__":
    unittest.main()
