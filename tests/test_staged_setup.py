#!/usr/bin/env python3
"""Bootstrap staged first-install and split-doc regressions (no native host claims)."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]


def call(*args, cwd=None, payload=None):
    return subprocess.run([str(x) for x in args], cwd=cwd, input=payload,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=45)


class StagedSetupTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = pathlib.Path(tmp.name)
        self.installer = REPO / "install.py"

    def install(self, runtime="codex", staged=True):
        flags = [sys.executable, self.installer, "--target", self.root,
                 "--runtime", runtime, "--config-git", "tracked"]
        if staged:
            flags.append("--staged")
        preview = call(*flags)
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertFalse((self.root / "AGENTS.md").exists())
        applied = call(*flags, "--apply")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        return applied

    def test_staged_codex_does_not_self_block_when_git_branch_unconfigured(self):
        self.install()
        phase = json.loads((self.root / "harness/setup-state.json").read_text())
        self.assertEqual(phase["phase"], "BOOTSTRAPPING")
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "apply_patch",
                              "tool_input": {"command": "*** Begin Patch\n*** Add File: docs/fixture.md\n+yes\n*** End Patch"}})
        response = call(sys.executable, self.root / "harness/codex/hook.py", cwd=self.root,
                        payload=payload)
        self.assertEqual(response.returncode, 0, response.stdout + response.stderr)
        self.assertNotEqual(json.loads(response.stdout).get("hookSpecificOutput", {}).get("permissionDecision"),
                            "deny")
        self.assertIn("BOOTSTRAPPING", response.stdout)
        smoke = call(sys.executable, self.root / "harness/common/setup_lifecycle.py", "smoke", cwd=self.root)
        self.assertEqual(smoke.returncode, 0, smoke.stdout + smoke.stderr)
        self.assertIn("SMOKE_DENY: PASS", smoke.stdout)
        self.assertIn("SMOKE_ALLOW: PASS", smoke.stdout)

    def test_staged_claude_deferred_then_disposable_smoke(self):
        self.install("claude")
        payload = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Edit",
                              "tool_input": {"file_path": "docs/CRITERIA.md"}})
        p = call(sys.executable, self.root / "harness/claude/hook.py", cwd=self.root, payload=payload)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        smoke = call(sys.executable, self.root / "harness/common/setup_lifecycle.py", "smoke", cwd=self.root)
        self.assertEqual(smoke.returncode, 0, smoke.stdout + smoke.stderr)
        self.assertIn("SMOKE_DENY: PASS", smoke.stdout)

    def test_staged_antigravity_stop_hook_defers(self):
        self.install("antigravity")
        bridge = call(sys.executable, self.root / "harness/common/setup_hook.py", cwd=self.root)
        self.assertEqual(bridge.returncode, 0, bridge.stdout + bridge.stderr)
        self.assertIn("BOOTSTRAPPING", bridge.stdout)
        self.assertEqual(call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                              "smoke", cwd=self.root).returncode, 2)

    def test_audit_and_activation_block_when_not_verified(self):
        self.install()
        p = call(sys.executable, self.root / "harness/common/setup_lifecycle.py", "audit", cwd=self.root)
        self.assertEqual(p.returncode, 2)
        self.assertIn("NOT_CONFIGURED", p.stdout)
        bogus = self.root / "harness/setup-live-evidence.json"
        bogus.write_text(json.dumps({"runtime": "codex", "host_version": "test"}))
        activated = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                         "activate", "--evidence", bogus, "--human-approved", cwd=self.root)
        self.assertEqual(activated.returncode, 2)
        self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["phase"], "BOOTSTRAPPING")

    def test_legacy_install_cannot_be_silently_unlocked(self):
        self.install(staged=False)
        result = call(sys.executable, self.installer, "--target", self.root, "--runtime",
                      "codex", "--config-git", "tracked", "--staged", "--apply")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("existing legacy harness", result.stdout)
        self.assertFalse((self.root / "harness/setup-state.json").exists())

    def test_one_root_readme_and_plan_ownership(self):
        self.assertFalse((REPO / "README.en.md").exists())
        self.assertTrue((REPO / "docs/user-guide.en.md").is_file())
        self.assertTrue((REPO / "docs/FOR_AI.md").is_file())
        root = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/user-guide.en.md", root)
        self.assertIn("docs/FOR_AI.md", root)
        criteria = (REPO / "project-template/docs/CRITERIA.md").read_text(encoding="utf-8")
        plan = (REPO / "project-template/docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
        self.assertNotIn("\n## GOALMAP\n", criteria)
        self.assertIn("\n## GOALMAP\n", plan)
        self.assertIn("GOAL:", plan)


if __name__ == "__main__":
    unittest.main()
