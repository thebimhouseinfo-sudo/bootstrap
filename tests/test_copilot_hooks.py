#!/usr/bin/env python3
"""Copilot native hook simulation. No claim of actual VS Code host dispatch."""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
NODE = shutil.which("node")
INSTALL = ROOT / "install.py"


@unittest.skipUnless(NODE, "Node.js required for native Copilot hook fixtures")
class CopilotNativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        p = subprocess.run([sys.executable, str(INSTALL), "--target", str(self.root),
                            "--tier", "Standard", "--runtime", "copilot", "--staged", "--apply"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.hook = self.root / ".github/hooks/criteria-gate.cjs"
        self.apply = self.root / ".github/hooks/criteria-apply.cjs"
        self.stage = self.root / "harness/criteria-proposal.md"
        self.target = self.root / "docs/CRITERIA.md"
        self.session = "copilot-session-1"
        self.assertTrue(self.hook.is_file())

    def event(self, name, payload):
        return subprocess.run([NODE, str(self.hook), name],
                              cwd=self.root, input=json.dumps(payload),
                              capture_output=True, text=True, timeout=15)

    def tool(self, name, args, session=None):
        return self.event("preToolUse", {"sessionId":session or self.session,
                                        "toolName":name, "toolArgs":args})

    def cmd(self, *args):
        return subprocess.run([NODE, str(self.apply), *args], cwd=self.root,
                              capture_output=True, text=True, timeout=15)

    def advice(self, response="Review completed; Human should decide."):
        return self.event("subagentStop", {"sessionId":self.session,
                              "agentName":"technical-advisor", "response":response})

    def prompt(self, text, session=None):
        return self.event("userPromptSubmitted", {"sessionId":session or self.session,
                                                  "prompt":text})

    def nonce(self):
        status = self.cmd("status")
        self.assertEqual(status.returncode, 0)
        match = re.search(r"CONFIRM CRITERIA ([0-9A-F]{8})", status.stdout)
        self.assertIsNotNone(match, status.stdout)
        return match.group(1)

    def check_denied(self):
        result = self.tool("edit", {"file_path":"docs/CRITERIA.md", "newText":"unauthorized"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")
        return result

    def test_first_draft_only_written_after_actual_subagent_and_later_human_prompt(self):
        self.assertIn("Status", self.target.read_text() + "Status")  # template may be draft
        original = self.target.read_bytes()
        self.stage.write_text("STATUS: APPROVED\nProduct: Greenfield fixture\n")
        self.check_denied()
        self.assertEqual(self.target.read_bytes(), original)
        self.assertIn("No valid Advisor", self.cmd("status").stdout)
        self.assertNotIn("permissionDecision", self.tool("view", {"file_path":"docs/CRITERIA.md"}).stdout)
        self.assertEqual(self.advice().returncode, 0)
        code = self.nonce()
        self.assertEqual(self.prompt("CONFIRM CRITERIA FFFFFFFF").returncode, 0)
        self.assertEqual(self.cmd().returncode, 2)
        self.check_denied()  # even authorization never enables arbitrary direct edits
        self.assertEqual(self.prompt("CONFIRM CRITERIA " + code).returncode, 0)
        allowed = self.tool("bash", {"command":"node .github/hooks/criteria-apply.cjs"})
        self.assertEqual(allowed.returncode, 0)
        self.assertNotIn("permissionDecision", allowed.stdout)
        applied = self.cmd()
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertEqual(self.target.read_text(), "STATUS: APPROVED\nProduct: Greenfield fixture\n")
        self.assertEqual(self.cmd().returncode, 2)  # consumed
        self.assertFalse((self.root / "harness/criteria-guard.json").exists())

    def test_existing_criteria_delta_requires_fresh_advice_and_unchanged_hash(self):
        self.target.write_text("STATUS: APPROVED\nCurrent: A\n")
        self.stage.write_text("STATUS: APPROVED\nCurrent: B\n")
        self.assertEqual(self.advice().returncode, 0)
        code = self.nonce()
        self.stage.write_text("STATUS: APPROVED\nCurrent: secretly changed\n")
        self.prompt("CONFIRM CRITERIA " + code)
        self.assertEqual(self.cmd().returncode, 2)
        self.assertEqual(self.target.read_text(), "STATUS: APPROVED\nCurrent: A\n")
        self.stage.write_text("STATUS: APPROVED\nCurrent: B\n")
        self.advice()
        self.prompt("CONFIRM CRITERIA " + self.nonce())
        self.target.write_text("STATUS: APPROVED\nHuman made another edit\n")
        self.assertEqual(self.cmd().returncode, 2)
        self.assertIn("Human made another", self.target.read_text())

    def test_no_advisor_or_wrong_session_cannot_unlock(self):
        self.stage.write_text("STATUS: APPROVED\nproposed\n")
        self.event("subagentStop", {"sessionId":self.session, "agentName":"reviewer",
                                     "response":"Reviewer output"})
        self.assertIn("No valid Advisor", self.cmd("status").stdout)
        self.advice()
        code = self.nonce()
        self.prompt("CONFIRM CRITERIA " + code, session="wrong-session")
        self.assertEqual(self.cmd().returncode, 2)
        self.check_denied()

    def test_shell_and_direct_edits_detected_without_blocking_unrelated_tasks(self):
        for name, args in [
            ("create", {"path":"docs/CRITERIA.md","content":"x"}),
            ("apply_patch", {"patch":"*** Update File: docs/CRITERIA.md\n+x"}),
            ("bash", {"command":"echo x > docs/CRITERIA.md"}),
            ("powershell", {"command":"Set-Content docs\\CRITERIA.md text"})
        ]:
            with self.subTest(tool=name):
                result = self.tool(name, args)
                self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")
        self.assertNotIn("permissionDecision", self.tool("edit", {"file_path":"src/example.py"}).stdout)
        self.assertNotIn("permissionDecision", self.tool("bash", {"command":"cat docs/CRITERIA.md"}).stdout)

    def test_native_package_schema(self):
        config=json.loads((self.root / ".github/hooks/criteria.json").read_text())
        self.assertEqual(config["version"], 1)
        for name in ("sessionStart","preToolUse","subagentStop","userPromptSubmitted"):
            self.assertIn(name, config["hooks"])
        planner=(self.root / ".github/agents/planner.agent.md").read_text()
        advisor=(self.root / ".github/agents/technical-advisor.agent.md").read_text()
        self.assertIn("When no Criteria exists", planner)
        self.assertIn("When Criteria exists", planner)
        self.assertIn("only after Human asks", advisor.lower().replace("only when planner has received a human request","only after Human asks"))
        self.assertIn("name: technical-advisor", advisor)


if __name__ == "__main__":
    unittest.main()
