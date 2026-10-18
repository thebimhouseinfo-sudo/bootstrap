#!/usr/bin/env python3
"""Safe installer/manifest regression, no modification of real project."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
def module(filename):
    spec=importlib.util.spec_from_file_location("installed",ROOT/filename)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
installer=module("install.py")
class InstallationTests(unittest.TestCase):
    def test_dry_run_and_repeat(self):
        with tempfile.TemporaryDirectory() as d:
            target=pathlib.Path(d)
            self.assertEqual(installer.main if False else 0,0)
            preview=subprocess.run([sys.executable,str(ROOT/"install.py"),"--target",str(target)],capture_output=True,text=True)
            self.assertEqual(preview.returncode,0,preview.stdout+preview.stderr)
            self.assertFalse((target/"AGENTS.md").exists())
            applied=subprocess.run([sys.executable,str(ROOT/"install.py"),"--target",str(target),"--apply"],capture_output=True,text=True)
            self.assertEqual(applied.returncode,0,applied.stdout+applied.stderr)
            again=subprocess.run([sys.executable,str(ROOT/"install.py"),"--target",str(target),"--apply"],capture_output=True,text=True)
            self.assertEqual(again.returncode,0,again.stdout+again.stderr)
            self.assertIn("SAME",again.stdout)
    def test_conflict_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            target=pathlib.Path(d)
            (target/"AGENTS.md").write_text("HUMAN CONTENT",encoding="utf-8")
            applied=subprocess.run([sys.executable,str(ROOT/"install.py"),"--target",str(target),"--apply"],capture_output=True,text=True)
            self.assertEqual(applied.returncode,2,applied.stdout+applied.stderr)
            self.assertEqual((target/"AGENTS.md").read_text(encoding="utf-8"),"HUMAN CONTENT")
    def test_manifest_tiers_and_document_paths(self):
        project=ROOT/"project-template"
        manifest=json.loads((project/"harness/specs/TIER_MANIFEST.json").read_text())
        self.assertEqual(manifest["tiers"]["Lite"]["gates"],[])
        self.assertIn("G13",manifest["tiers"]["Standard"]["gates"])
        self.assertIn("G14",manifest["tiers"]["Full"]["gates"])
        for p in ("harness/HARNESS_SPEC.md","harness/specs/HARNESS_SPEC_TEMPLATE.md",
                  "harness/specs/READINESS.md","harness/codex/preflight.py"):
            self.assertTrue((project/p).is_file(),p)
    def test_native_agent_toml(self):
        project=ROOT/"project-template"
        try:
            import tomllib
        except ImportError:
            self.skipTest("tomllib requires Python 3.11+")
        for file in (project/".codex/agents").glob("*.toml"):
            with file.open("rb") as f: doc=tomllib.load(f)
            for key in ("name","description","developer_instructions"):
                self.assertTrue(doc.get(key),str(file)+": "+key)
if __name__=="__main__":
    unittest.main(verbosity=2)
