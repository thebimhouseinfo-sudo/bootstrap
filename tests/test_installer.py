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
            self.assertTrue((target/"AGENTS.bootstrap.md").is_file())
            self.assertFalse((target/"README.md").exists())
    def test_manifest_tiers_and_document_paths(self):
        project=ROOT/"project-template"
        manifest=json.loads((project/"harness/specs/TIER_MANIFEST.json").read_text())
        self.assertEqual(manifest["tiers"]["Lite"]["gates"],[])
        self.assertIn("G13",manifest["tiers"]["Standard"]["gates"])
        self.assertIn("G14",manifest["tiers"]["Full"]["gates"])
        for p in ("harness/HARNESS_SPEC.md","harness/specs/HARNESS_SPEC_TEMPLATE.md",
                  "harness/specs/READINESS.md","harness/codex/preflight.py"):
            self.assertTrue((project/p).is_file(),p)
    def test_tier_runtime_filtering(self):
        with tempfile.TemporaryDirectory() as d:
            dest=pathlib.Path(d)
            for tier,runtime in (("Lite","codex"),("Standard","claude"),("Full","continue")):
                result=subprocess.run([sys.executable,str(ROOT/"install.py"),"--target",str(dest),"--tier",tier,"--runtime",runtime],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stdout+result.stderr)
                included=[p.relative_to(installer.SOURCE).as_posix() for p in installer.entries(tier,runtime)]
                self.assertNotIn("README.md",included)
                if runtime!="codex": self.assertFalse(any(p.startswith(".codex/") for p in included))
                if runtime!="claude": self.assertFalse(any(p.startswith(".claude/") for p in included))
                if runtime!="continue": self.assertFalse(any(p.startswith(".continue/") for p in included))
                if tier=="Lite":
                    self.assertFalse(any("harness-fixer" in p for p in included))
                    self.assertNotIn("harness/specs/GATES.md",included)
    def test_agent_model_presets_and_read_only(self):
        project=ROOT/"project-template"
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                self.skipTest("TOML parser unavailable on this Python")
        with (project/".codex/config.toml").open("rb") as f: cfg=tomllib.load(f)
        self.assertNotIn("model",cfg)
        self.assertNotIn("approval_policy",cfg)
        for file in (project/".codex/agents").glob("*.toml"):
            with file.open("rb") as f: data=tomllib.load(f)
            self.assertTrue(data.get("model"), file.name)
            self.assertIn(data.get("model_reasoning_effort"), ("medium", "high"))
            if file.stem in ("critic","explorer"):
                self.assertEqual(data.get("sandbox_mode"),"read-only")
    def test_native_agent_toml(self):
        project=ROOT/"project-template"
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                self.skipTest("tomllib/tomli unavailable")
        for file in (project/".codex/agents").glob("*.toml"):
            with file.open("rb") as f: doc=tomllib.load(f)
            for key in ("name","description","developer_instructions"):
                self.assertTrue(doc.get(key),str(file)+": "+key)
if __name__=="__main__":
    unittest.main(verbosity=2)
