#!/usr/bin/env python3
"""Continue CLI native event contract. Does not claim IDE or live cn dispatch."""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1]
NODE = shutil.which("node")


@unittest.skipUnless(NODE, "Node.js unavailable; host must not claim native Continue hooks")
class ContinueHooksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        cmd = [sys.executable, str(SOURCE / "install.py"), "--target", str(self.root),
               "--tier", "Standard", "--runtime", "continue", "--staged", "--apply"]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.hook = self.root / ".continue/hooks/criteria-gate.cjs"
        self.apply = self.root / ".continue/hooks/criteria-apply.cjs"
        self.criteria = self.root / "docs/CRITERIA.md"
        self.proposal = self.root / "harness/criteria-proposal.md"
        self.session = "continue-cli-session"
        self.assertTrue(self.hook.is_file())

    def event(self, event, **kwargs):
        payload = {"hook_event_name": event, "session_id": self.session,
                   "transcript_path": "/tmp/fake-transcript", "cwd": str(self.root)}
        payload.update(kwargs)
        return subprocess.run([NODE, str(self.hook)], input=json.dumps(payload),
                              capture_output=True, text=True, cwd=self.root, timeout=15)

    def tool(self, name, args):
        return self.event("PreToolUse", tool_name=name, tool_input=args, tool_use_id="test")

    def subagent(self, who="technical-advisor"):
        return self.event("SubagentStop", agent_type=who, agent_id="advisor-fixture",
                          agent_transcript_path="/tmp/advisor-fixture",
                          last_assistant_message="Feasibility and impact advice for Human.",
                          stop_hook_active=False)

    def prompt(self, body):
        return self.event("UserPromptSubmit", prompt=body)

    def apply_command(self, arg="apply"):
        return subprocess.run([NODE, str(self.apply), arg],
                              capture_output=True, text=True, cwd=self.root, timeout=15)

    def nonce(self):
        status = self.apply_command("status")
        match = re.search(r"CONFIRM CRITERIA ([A-F0-9]{8})", status.stdout)
        self.assertIsNotNone(match, status.stdout)
        return match.group(1)

    def test_installation_native_settings_schema_and_discovery(self):
        settings = json.loads((self.root / ".continue/settings.json").read_text())
        for event in ("SessionStart", "PreToolUse", "SubagentStop", "UserPromptSubmit"):
            groups = settings["hooks"][event]
            self.assertTrue(groups and groups[0]["hooks"][0]["type"] == "command")
            self.assertIn(".continue/hooks/criteria-gate.cjs", groups[0]["hooks"][0]["command"])
        self.assertTrue((self.root / ".continue/rules/01-criteria-gate.md").exists())
        self.assertTrue((self.root / ".continue/rules/roles/advisor.md").exists())
        shared = {p.parent.name for p in (self.root / ".agents/skills").glob("*/SKILL.md")}
        native = {p.parent.name for p in (self.root / ".continue/skills").glob("*/SKILL.md")}
        self.assertEqual(shared, native)
        self.assertIn("write-criteria", native)
        inv = subprocess.run([sys.executable, str(self.root / "harness/common/inventory.py"),
                              "--tier", "Standard", "--runtime", "continue"],
                             capture_output=True, text=True)
        self.assertEqual(inv.returncode, 0, inv.stdout + inv.stderr)
        session = self.event("SessionStart", source="startup")
        self.assertEqual(session.returncode, 0)
        self.assertEqual(json.loads(session.stdout)["hookSpecificOutput"]["hookEventName"], "SessionStart")

    def test_pretool_blocks_criteria_and_allows_safe_changes(self):
        for name, args in (
            ("edit_existing_file", {"path":"docs/CRITERIA.md", "replacement":"bad"}),
            ("create_new_file", {"path":"docs/CRITERIA.md", "content":"bad"}),
            ("run_terminal_command", {"command":"echo bad > docs/CRITERIA.md"}),
            ("Bash", {"command":"cat docs/CRITERIA.md; echo bad > docs/CRITERIA.md"}),
            ("Bash", {"command":"cat docs/CRITERIA.md\necho bad > docs/CRITERIA.md"})):
            with self.subTest(name=name, args=args):
                res = self.tool(name, args)
                self.assertEqual(res.returncode, 2, res.stdout + res.stderr)
                self.assertEqual(json.loads(res.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(self.tool("edit_existing_file", {"path":"README.md", "replacement":"ok"}).returncode, 0)
        self.assertEqual(self.tool("Bash", {"command":"cat docs/CRITERIA.md"}).returncode, 0)

    def test_no_consultation_no_write_and_post_advice_human_confirmation(self):
        previous = self.criteria.read_bytes()
        self.proposal.write_text("STATUS: APPROVED\nGreenfield desired behavior\n")
        self.assertEqual(self.apply_command().returncode, 2)
        self.assertEqual(self.subagent("reviewer").returncode, 0)
        self.assertIn("No valid Advisor", self.apply_command("status").stdout)
        self.assertEqual(self.subagent().returncode, 0)
        code = self.nonce()
        self.assertEqual(self.apply_command().returncode, 2)
        self.prompt("CONFIRM CRITERIA BADBAD00")
        self.assertEqual(self.apply_command().returncode, 2)
        self.assertEqual(self.tool("run_terminal_command", {"command":"node .continue/hooks/criteria-apply.cjs"}).returncode, 2)
        self.prompt("CONFIRM CRITERIA " + code)
        self.assertEqual(self.tool("run_terminal_command", {"command":"node .continue/hooks/criteria-apply.cjs"}).returncode, 0)
        self.assertEqual(self.apply_command().returncode, 0)
        self.assertEqual(self.criteria.read_text(), "STATUS: APPROVED\nGreenfield desired behavior\n")
        self.assertNotEqual(previous, self.criteria.read_bytes())
        self.assertEqual(self.apply_command().returncode, 2)

    def test_existing_criteria_stale_advice_or_changed_proposal_cannot_unlock(self):
        self.criteria.write_text("STATUS: APPROVED\nOld feature\n")
        self.proposal.write_text("STATUS: APPROVED\nNew feature\n")
        self.subagent()
        code = self.nonce()
        self.proposal.write_text("STATUS: APPROVED\nDifferent feature\n")
        self.prompt("CONFIRM CRITERIA " + code)
        self.assertEqual(self.apply_command().returncode, 2)
        self.assertIn("Old feature", self.criteria.read_text())
        self.proposal.write_text("STATUS: APPROVED\nNew feature\n")
        self.subagent()
        self.prompt("CONFIRM CRITERIA " + self.nonce())
        self.criteria.write_text("STATUS: APPROVED\nEdited concurrently\n")
        self.assertEqual(self.apply_command().returncode, 2)

    def test_stop_only_checks_an_active_task_and_blocks_failed_validation(self):
        settings = json.loads((self.root / ".continue/settings.json").read_text())
        self.assertEqual(settings["hooks"]["Stop"][0]["hooks"][0]["type"], "command")
        stop = self.root / ".continue/hooks/stop-verify.cjs"
        def stop_event(active=False):
            return subprocess.run([NODE, str(stop)], cwd=self.root,
                input=json.dumps({"hook_event_name": "Stop", "session_id": self.session,
                                  "cwd": str(self.root), "stop_hook_active": active}),
                capture_output=True, text=True, timeout=15)
        # A default NOT_CONFIGURED task never triggers verification or a retry.
        self.assertEqual(json.loads(stop_event().stdout), {})
        (self.root / "harness/setup-state.json").unlink()
        self.assertEqual(json.loads(stop_event().stdout), {})
        (self.root / "harness/active-task.json").write_text(json.dumps(
            {"status":"ACTIVE", "goal_id":"GOAL-1", "theory_ids": [],
             "tests":[], "evidence":[]}))
        self.assertEqual(json.loads(stop_event(active=True).stdout), {})
        check = stop_event()
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(json.loads(check.stdout)["decision"], "block")

    def test_missing_native_event_never_claims_an_advisor(self):
        self.proposal.write_text("STATUS: APPROVED\nDraft\n")
        self.prompt("CONFIRM CRITERIA FFFFFFFF")
        self.assertEqual(self.apply_command().returncode, 2)
        self.assertEqual(self.tool("run_terminal_command", {"command":"node .continue/hooks/criteria-apply.cjs"}).returncode, 2)


if __name__ == "__main__":
    unittest.main()
