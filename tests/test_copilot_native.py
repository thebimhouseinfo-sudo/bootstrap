#!/usr/bin/env python3
"""Native Copilot payload/installer simulations. Not proof of actual host dispatch."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"

def invoke(*args, input=None):
    return subprocess.run([sys.executable, *map(str, args)],
                          input=input, capture_output=True, text=True, timeout=35)

class CopilotNativeTests(unittest.TestCase):
    def install(self, tier="Standard", app="copilot"):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dest = pathlib.Path(tmp.name)
        result = invoke(INSTALL, "--target", dest, "--tier", tier,
                        "--runtime", "generic", "--target-app", app, "--staged", "--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return dest

    def test_native_copilot_package_is_tier_scoped(self):
        for tier, count in (("Lite", 3), ("Standard", 7), ("Full", 8)):
            with self.subTest(tier=tier):
                root = self.install(tier)
                agents = sorted((root / ".github/agents").glob("*.agent.md"))
                self.assertEqual(len(agents), count)
                self.assertIn("user-invocable: false",
                              (root / ".github/agents/advisor.agent.md").read_text())
                self.assertIn("ONLY AFTER Human requests",
                              (root / ".github/agents/planner.agent.md").read_text())
                cfg = json.loads((root / ".github/hooks/bootstrap-criteria.json").read_text())
                self.assertEqual(cfg["version"], 1)
                self.assertEqual(cfg["hooks"]["preToolUse"][0]["type"], "command")
                self.assertTrue((root / ".github/copilot-instructions.md").exists())

    def test_copilot_host_test_describes_installed_native_hooks(self):
        root = self.install()
        report = invoke(root / "harness/common/setup_lifecycle.py", "host-test")
        self.assertEqual(report.returncode, 0, report.stdout + report.stderr)
        self.assertIn("packaged native .github/agents", report.stdout)
        self.assertIn("Test DENY before review, ASK", report.stdout)
        self.assertNotIn("WRITE AND REGISTER", report.stdout)

    def test_other_generic_clients_are_not_given_copilot_files(self):
        root = self.install(app="qwen-code")
        self.assertFalse((root / ".github").exists())

    def test_hook_denies_initial_and_existing_before_advisor(self):
        root = self.install()
        hook = root / ".github/hooks/criteria_guard.py"
        events = [
            {"toolName":"edit","toolArgs":{"filePath":"docs/CRITERIA.md","newText":"x"}},
            {"toolName":"apply_patch","toolArgs":{"patch":"*** Update File: docs/CRITERIA.md\n+change"}},
            {"toolName":"powershell","toolArgs":{"command":"Set-Content docs\\CRITERIA.md hello"}},
        ]
        for event in events:
            with self.subTest(event=event):
                got = invoke(hook, input=json.dumps(event))
                self.assertEqual(got.returncode, 0)
                value = json.loads(got.stdout)
                self.assertEqual(value["permissionDecision"], "deny")
                self.assertIn("CRITERIA_PREWRITE_BLOCKED", value["permissionDecisionReason"])
        self.assertEqual(json.loads(invoke(hook, input=json.dumps(
            {"toolName":"view","toolArgs":{"filePath":"docs/CRITERIA.md"}})).stdout), {})
        self.assertEqual(json.loads(invoke(hook, input=json.dumps(
            {"toolName":"edit","toolArgs":{"filePath":"src/a.py"}})).stdout), {})

    def test_post_advice_receipt_requires_native_ask_not_allow(self):
        root = self.install()
        hook = root / ".github/hooks/criteria_guard.py"
        criteria = root / "docs/CRITERIA.md"
        receipt = root / "harness/criteria-write-authorization.json"
        payload={"toolName":"edit","toolArgs":{"filePath":"docs/CRITERIA.md","newText":"new"}}
        for scope in ("initial", "amendment"):
            got = invoke(root / ".github/hooks/prepare_criteria_request.py",
                         "--scope", scope, "--proposal-id", "discussion-v1")
            self.assertEqual(got.returncode, 0, got.stdout+got.stderr)
            out = json.loads(invoke(hook, input=json.dumps(payload)).stdout)
            self.assertEqual(out.get("permissionDecision"), "ask")
            self.assertIn("Human", out["permissionDecisionReason"])
        criteria.write_text("changed baseline\n", encoding="utf-8")
        changed = json.loads(invoke(hook, input=json.dumps(payload)).stdout)
        self.assertEqual(changed["permissionDecision"], "deny")

    def test_receipt_not_enough_without_post_advice_claim_and_expiry(self):
        root=self.install()
        hook=root/".github/hooks/criteria_guard.py"
        receipt=root/"harness/criteria-write-authorization.json"
        invoke(root/".github/hooks/prepare_criteria_request.py", "--scope", "initial",
               "--proposal-id", "v1")
        original=json.loads(receipt.read_text())
        event={"toolName":"edit","toolArgs":{"file_path":"docs/CRITERIA.md"}}
        for change in ({"human_decided_after_advice":False},
                       {"advisor_consulted":False},
                       {"expires_utc":"2000-01-01T00:00:00Z"}):
            bad=dict(original,**change)
            receipt.write_text(json.dumps(bad))
            got=json.loads(invoke(hook,input=json.dumps(event)).stdout)
            self.assertEqual(got["permissionDecision"],"deny")
        # Shows a documented coverage gap: an indirect shell call with no Criteria path
        # cannot be attributed to Criteria by preToolUse event fields alone.
        unknown=json.loads(invoke(hook,input=json.dumps(
            {"toolName":"bash","toolArgs":{"command":"python ./unrelated-script.py"}})).stdout)
        self.assertEqual(unknown, {})

if __name__ == "__main__":
    unittest.main()
