"""Native adapter boundaries in disposable projects; no real host/approval claims."""
import contextlib
import io
import json
import pathlib
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
NODE = shutil.which("node")


class MultiHarnessGuardTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        command = [sys.executable, str(REPO / "install.py"), "--target", str(self.root),
                   "--tier", "Standard", "--staged", "--apply"]
        for runtime in ("codex", "continue", "copilot"):
            command += ["--runtime", runtime]
        result = subprocess.run(command, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def hook(self, runtime, event, **fields):
        if not NODE:
            self.skipTest("Node.js required")
        if runtime == "copilot":
            script = self.root / ".github/hooks/criteria-gate.cjs"
            command = [NODE, str(script), event]
            payload = {"sessionId": "fixture", "cwd": str(self.root), **fields}
        else:
            script = self.root / ".continue/hooks/criteria-gate.cjs"
            command = [NODE, str(script)]
            payload = {"hook_event_name": event, "session_id": "fixture",
                       "cwd": str(self.root), **fields}
        return subprocess.run(command, input=json.dumps(payload), cwd=self.root,
                              capture_output=True, text=True, timeout=15)

    def apply(self, runtime):
        prefix = ".github" if runtime == "copilot" else ".continue"
        return subprocess.run([NODE, str(self.root / prefix / "hooks/criteria-apply.cjs")],
                              cwd=self.root, capture_output=True, text=True, timeout=15)

    def authorize(self, runtime):
        # Mechanical event fixtures only; these do not represent a Human decision.
        (self.root / "harness/criteria-proposal.md").write_text("STATUS: APPROVED\nFixture\n")
        if runtime == "copilot":
            advice = self.hook(runtime, "subagentStop", agentName="technical-advisor", response="Fixture advice")
        else:
            advice = self.hook(runtime, "SubagentStop", agent_type="technical-advisor",
                               last_assistant_message="Fixture advice")
        self.assertEqual(advice.returncode, 0, advice.stderr)
        prefix = ".github" if runtime == "copilot" else ".continue"
        status = subprocess.run([NODE, str(self.root / prefix / "hooks/criteria-apply.cjs"), "status"],
                                cwd=self.root, capture_output=True, text=True, timeout=15)
        nonce = status.stdout.split("CONFIRM CRITERIA ", 1)[1].strip()
        prompt_event = "userPromptSubmitted" if runtime == "copilot" else "UserPromptSubmit"
        prompt = self.hook(runtime, prompt_event, prompt="CONFIRM CRITERIA " + nonce)
        self.assertEqual(prompt.returncode, 0, prompt.stderr)

    def test_shell_read_exception_does_not_allow_writing_or_exec_options(self):
        original = (self.root / "docs/CRITERIA.md").read_bytes()
        for runtime in ("copilot", "continue"):
            for command in ("sed -n 'w docs/CRITERIA.md' input.txt",
                            "sed -n -i 's/a/b/' docs/CRITERIA.md",
                            "rg --pre 'touch marker' x docs/CRITERIA.md",
                            "cat\nrm docs/CRITERIA.md",
                            "cat\r\nrm docs/CRITERIA.md",
                            "less docs/CRITERIA.md"):
                with self.subTest(runtime=runtime, command=command):
                    fields = ({"toolName": "bash", "toolArgs": {"command": command}}
                              if runtime == "copilot" else
                              {"tool_name": "run_terminal_command", "tool_input": {"command": command}})
                    result = self.hook(runtime, "preToolUse" if runtime == "copilot" else "PreToolUse", **fields)
                    output = json.loads(result.stdout)
                    decision = output if runtime == "copilot" else output.get("hookSpecificOutput", {})
                    self.assertEqual(decision.get("permissionDecision"), "deny", result.stdout)
        self.assertEqual((self.root / "docs/CRITERIA.md").read_bytes(), original)

    def test_receipt_cannot_be_consumed_by_another_runtime(self):
        for owner, other in (("copilot", "continue"), ("continue", "copilot")):
            with self.subTest(owner=owner):
                self.authorize(owner)
                before = (self.root / "docs/CRITERIA.md").read_bytes()
                rejected = self.apply(other)
                self.assertEqual(rejected.returncode, 2, rejected.stdout + rejected.stderr)
                self.assertEqual((self.root / "docs/CRITERIA.md").read_bytes(), before)
                accepted = self.apply(owner)
                self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)

    def test_receipt_owner_is_checked_even_if_copied_to_other_runtime_path(self):
        self.authorize("copilot")
        source = self.root / "harness/criteria-guard.copilot.json"
        # On an old install the receipt is unscoped; use that path to expose the bug too.
        if not source.exists():
            source = self.root / "harness/criteria-guard.json"
        (self.root / "harness/criteria-guard.continue.json").write_bytes(source.read_bytes())
        self.assertEqual(self.apply("continue").returncode, 2)

    def test_advisor_turn_in_other_runtime_does_not_replace_pending_receipt(self):
        self.authorize("copilot")
        self.hook("continue", "SubagentStop", agent_type="technical-advisor",
                  last_assistant_message="Other independent fixture advice")
        applied = self.apply("copilot")
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)

    def test_receipts_remain_local_in_tracked_mode(self):
        command = [sys.executable, str(REPO / "install.py"), "--target", str(self.root),
                   "--runtime", "codex", "--runtime", "continue", "--runtime", "copilot",
                   "--config-git", "tracked", "--change-config-git", "--apply"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.authorize("copilot")
        private = ["harness/criteria-guard.copilot.json", "harness/criteria-guard.continue.json",
                   "harness/criteria-guard.json", "harness/criteria-guard.copilot.json.new",
                   "harness/criteria-guard.continue.json.new"]
        result = subprocess.run(["git", "check-ignore", *private],
                                cwd=self.root, capture_output=True, text=True, timeout=15)
        self.assertEqual(set(result.stdout.splitlines()), set(private))

    def test_secondary_adapter_and_continue_stop_drift_are_detected(self):
        module = runpy.run_path(str(self.root / "harness/common/setup_lifecycle.py"))
        for runtime, relative in (("codex", ".continue/hooks/criteria-gate.cjs"),
                                  ("codex", ".github/hooks/criteria.json"),
                                  ("continue", ".continue/hooks/stop-verify.cjs")):
            with self.subTest(runtime=runtime, relative=relative):
                expected = module["locked_files"](runtime)
                target = self.root / relative
                before = target.read_bytes()
                target.write_bytes(before + b"\n")
                with contextlib.redirect_stdout(io.StringIO()):
                    intact = module["check_lock"]({"runtime": runtime, "locked_files": expected})
                self.assertFalse(intact)
                target.write_bytes(before)

    def test_changing_installed_runtime_manifest_is_lock_drift(self):
        module = runpy.run_path(str(self.root / "harness/common/setup_lifecycle.py"))
        expected = module["locked_files"]("codex")
        target = self.root / "harness/.bootstrap-manifest.json"
        manifest = json.loads(target.read_text())
        manifest["runtimes"] = ["codex"]
        target.write_text(json.dumps(manifest))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(module["check_lock"]({"runtime": "codex", "locked_files": expected}))

    def test_copilot_can_be_selected_as_additional_host_in_wizard(self):
        module = runpy.run_path(str(REPO / "project-template/harness/common/setup_intake.py"))
        labels = []
        def display(value):
            if isinstance(value, str) and value.startswith(("Also install", "Which harness", "Should Bootstrap", "Is the active")):
                labels.append(value)
        def answer(_):
            if labels[-1] == "Also install Copilot harness?":
                return "2"
            if labels[-1].startswith("Which harness"):
                return "2"
            return "1"
        intake = module["collect"]("codex", input_fn=answer, output_fn=display)
        self.assertEqual(intake["runtimes"], ["codex", "copilot"])
        record = self.root / "intake.json"
        record.write_text(json.dumps(intake))
        preview = subprocess.run([sys.executable, str(REPO / "install.py"), "--target", str(self.root),
                                  "--runtime", "codex", "--runtime", "copilot", "--intake-file", str(record)],
                                 capture_output=True, text=True, timeout=45)
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)


if __name__ == "__main__":
    unittest.main()
