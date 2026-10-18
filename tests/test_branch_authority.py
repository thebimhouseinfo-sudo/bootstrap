#!/usr/bin/env python3
"""Disposable Git branch authority, freeze, merge, push and Codex hook regressions."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.py"

def call(args, cwd, data=None):
    return subprocess.run(args, cwd=str(cwd), input=data, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=30)

class BranchAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        r = call([sys.executable, str(INSTALL), "--target", str(self.root),
                  "--tier", "Lite", "--runtime", "codex", "--apply"], self.root)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.tool = self.root / "harness/common/branch_authority.py"
        self.hook = self.root / "harness/codex/hook.py"
        self.git("init", "-q")
        self.git("config", "user.name", "Test Human")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("add", ".")
        self.git("commit", "-qm", "test fixture")
        self.git("branch", "-m", "main")
        self.git("branch", "v5")
        self.git("remote", "add", "origin", "https://example.invalid/fixture.git")

    def git(self, *args):
        r = call(["git", *args], self.root)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout.strip()

    def check(self, *args, expected=0):
        r = call([sys.executable, str(self.tool), *args], self.root)
        self.assertEqual(r.returncode, expected, r.stdout + r.stderr)
        return r

    def configure(self):
        flags = ("--active", "v5", "--freeze", "main",
                 "--remote", "origin", "--work", "feat/task-x")
        preview = self.check("configure", *flags)
        self.assertIn("PREVIEW_ONLY", preview.stdout)
        self.assertFalse((self.root / ".git/bootstrap/branch-authority.json").exists())
        applied = self.check("configure", *flags, "--apply")
        self.assertIn("CONFIGURED", applied.stdout)

    def hook_call(self):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "apply_patch",
                   "tool_input": {"command": "*** Begin Patch\n*** Update File: docs/ARCHITECTURE.md\n@@\n*** End Patch"}}
        r = call([sys.executable, str(self.hook)], self.root, json.dumps(payload))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def test_missing_authority_fails_closed_and_main_is_not_inferred(self):
        self.check("status", expected=2)
        self.check("check-write", expected=2)
        self.assertEqual(self.hook_call()["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertFalse((self.root / "harness/snapshots").exists())

    def test_frozen_main_active_v5_and_registered_feature_branch(self):
        self.configure()
        self.assertIn("FROZEN", self.check("status", expected=2).stdout) # main checkout
        self.check("check-write", expected=2)
        self.git("checkout", "-q", "v5")
        self.assertIn("MERGE_TARGET: v5", self.check("status").stdout)
        self.check("check-write")
        self.check("check-create", "--base", "v5", "--new", "feat/task-x")
        self.check("check-create", "--base", "main", "--new", "feat/task-x", expected=2)
        self.check("check-create", "--base", "v5", "--new", "feat/unregistered", expected=2)
        self.git("checkout", "-qb", "feat/task-x")
        self.check("check-write")
        self.check("check-merge", "--source", "feat/task-x", "--target", "v5")
        self.check("check-merge", "--source", "feat/task-x", "--target", "main", expected=2)
        self.check("check-merge", "--source", "main", "--target", "v5", expected=2)
        self.check("check-push", "--source", "feat/task-x", "--target", "feat/task-x", "--remote", "origin")
        self.check("check-push", "--source", "feat/task-x", "--target", "main", "--remote", "origin", expected=2)
        self.check("check-push", "--source", "feat/task-x", "--target", "feat/task-x", "--remote", "upstream", expected=2)
        self.git("checkout", "-q", "main")
        self.check("check-write", expected=2)
        self.assertEqual(self.hook_call()["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_hook_allows_registered_work_and_blocks_unknown(self):
        self.configure()
        self.git("checkout", "-q", "v5")
        allowed = self.hook_call()
        self.assertIn("snapshot", allowed["hookSpecificOutput"]["additionalContext"].lower())
        self.git("checkout", "-qb", "feat/unregistered")
        self.check("check-write", expected=2)
        self.assertEqual(self.hook_call()["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_missing_remote_and_authority_update_require_explicit_choice(self):
        self.configure()
        self.check("configure", "--active", "main", "--remote", "origin", expected=2)
        self.check("configure", "--active", "main", "--remote", "origin", "--replace")
        self.check("configure", "--active", "v5", "--freeze", "main",
                   "--remote", "bogus", "--replace", "--apply", expected=2)
        self.assertIn("v5", (self.root / ".git/bootstrap/branch-authority.json").read_text(encoding="utf-8"))
        self.git("checkout", "-q", "v5")
        self.git("checkout", "--detach", "-q")
        self.check("check-write", expected=2)

    def test_policy_does_not_follow_checkout_of_old_branch(self):
        self.configure()
        self.git("checkout", "-q", "v5")
        self.assertEqual(self.check("status").returncode, 0)
        self.git("checkout", "-q", "main")
        self.check("check-write", expected=2)
        data = json.loads((self.root / ".git/bootstrap/branch-authority.json").read_text(encoding="utf-8"))
        self.assertEqual(data["active_development_branch"], "v5")

if __name__ == "__main__":
    unittest.main(verbosity=2)
