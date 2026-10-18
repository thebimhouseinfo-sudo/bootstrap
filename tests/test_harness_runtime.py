#!/usr/bin/env python3
"""Codex-first Python hook/snapshot/task tests on a disposable installed project."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
INSTALL = REPO / "install.py"

def process(argv, cwd, input_text=None, timeout=30):
    return subprocess.run(argv, cwd=str(cwd), input=input_text, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)

class HarnessRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        result = process([sys.executable, str(INSTALL), "--target", str(self.root),
                          "--tier", "Standard", "--runtime", "codex", "--apply"], self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.common = self.root / "harness/common"
        self.hook = self.root / "harness/codex/hook.py"

    def command(self, rel, *argv, input_text=None):
        return process([sys.executable, str(self.root / rel), *argv], self.root, input_text=input_text)

    def hook_call(self, event, **data):
        req = dict(hook_event_name=event, cwd=str(self.root), session_id="fixture", **data)
        result = process([sys.executable, str(self.hook)], self.root, json.dumps(req))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_snapshot_preview_restore_hash_and_symlink_refusal(self):
        source = self.root / "docs/ARCHITECTURE.md"
        original = source.read_bytes()
        made = self.command("harness/common/snapshot.py", "capture", "docs/ARCHITECTURE.md")
        self.assertEqual(made.returncode, 0, made.stdout + made.stderr)
        ident = made.stdout.strip().split("SNAPSHOT: ")[-1]
        source.write_text("changed document", encoding="utf-8")
        checksum = hashlib.sha256(source.read_bytes()).hexdigest()
        preview = self.command("harness/common/snapshot.py", "restore", ident)
        self.assertEqual(preview.returncode, 0)
        self.assertEqual(source.read_text(encoding="utf-8"), "changed document")
        invalid = self.command("harness/common/snapshot.py", "restore", ident, "--apply",
                               "--expect-current", "docs/ARCHITECTURE.md=" + "0"*64)
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(source.read_text(encoding="utf-8"), "changed document")
        restored = self.command("harness/common/snapshot.py", "restore", ident, "--apply",
                                "--expect-current", "docs/ARCHITECTURE.md=" + checksum)
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(self.command("harness/common/snapshot.py", "capture", "../oops").returncode, 2)
        self.assertEqual(self.command("harness/common/snapshot.py", "capture", ".env").returncode, 2)

    def test_snapshot_store_symlink_does_not_write_outside_project(self):
        outside = self.root.parent / (self.root.name + "-external")
        outside.mkdir()
        self.addCleanup(lambda: outside.rmdir() if outside.exists() and not list(outside.iterdir()) else None)
        storage = self.root / "harness/snapshots"
        try:
            storage.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink unavailable on this runner")
        taken = self.command("harness/common/snapshot.py", "capture", "docs/ARCHITECTURE.md")
        self.assertEqual(taken.returncode, 2, taken.stdout + taken.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        storage.unlink()

    def test_trace_requires_real_goal_links_and_evidence(self):
        self.assertEqual(self.command("harness/common/task.py").returncode, 2)
        criteria = self.root / "docs/CRITERIA.md"
        criteria.write_text(criteria.read_text(encoding="utf-8")+"\nREQ-123 approved scope\n", encoding="utf-8")
        task = self.root / "harness/active-task.json"
        value = dict(status="ACTIVE", goal_id="G-001", theory_ids=["REQ-123"],
                     tests=["tests/test_sample.py"], evidence=["docs/reports/proof.txt"])
        task.write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual(self.command("harness/common/task.py", "--stage", "plan").returncode, 0)
        self.assertEqual(self.command("harness/common/task.py", "--stage", "delivery").returncode, 2)
        (self.root / "tests").mkdir()
        (self.root / "tests/test_sample.py").write_text("# present", encoding="utf-8")
        (self.root / "docs/reports/proof.txt").write_text("observed result", encoding="utf-8")
        self.assertEqual(self.command("harness/common/task.py").returncode, 0)
        value["theory_ids"] = ["REQ-NOT-FOUND"]
        task.write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual(self.command("harness/common/task.py").returncode, 2)

    def test_codex_hook_json_and_subdir_command_resolution(self):
        hook_config = json.loads((self.root / ".codex/hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(set(hook_config["hooks"]), {"SessionStart", "PreToolUse", "Stop"})
        for event in hook_config["hooks"].values():
            for group in event:
                for entry in group["hooks"]:
                    self.assertEqual(entry["type"], "command")
                    self.assertIn("harness/codex/hook.py", entry["command"])
                    self.assertEqual(entry["command"], entry["commandWindows"])
        nested = self.root / "docs/reports"
        actual = subprocess.run(
            hook_config["hooks"]["SessionStart"][0]["hooks"][0]["command"],
            shell=True, cwd=str(nested),
            input=json.dumps({"hook_event_name":"SessionStart"}),
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        self.assertEqual(actual.returncode, 0, actual.stdout + actual.stderr)
        self.assertIn("hookSpecificOutput", json.loads(actual.stdout))

    def test_pretool_snapshots_known_apply_patch_only(self):
        response = self.hook_call("PreToolUse", tool_name="apply_patch",
            tool_input={"command":"*** Begin Patch\n*** Update File: docs/ARCHITECTURE.md\n@@\n*** End Patch"})
        self.assertIn("snapshot", response["hookSpecificOutput"]["additionalContext"].lower())
        snapshots = list((self.root / "harness/snapshots").glob("*/manifest.json"))
        self.assertEqual(len(snapshots), 1)
        self.assertIn("docs/ARCHITECTURE.md", snapshots[0].read_text(encoding="utf-8"))
        others = self.hook_call("PreToolUse", tool_name="Bash",
            tool_input={"command":"echo no edit"})
        self.assertEqual(others, {})
        self.assertEqual(len(list((self.root / "harness/snapshots").glob("*/manifest.json"))), 1)

    def test_pretool_snapshot_failure_denies_supported_apply_patch(self):
        denied = self.hook_call("PreToolUse", tool_name="apply_patch",
            tool_input={"command":"*** Begin Patch\n*** Update File: ../escape.md\n*** End Patch"})
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_runtime_files_and_status_match_installer(self):
        for name in ("harness/common/task.py", "harness/common/snapshot.py",
                     "harness/codex/hook.py", ".codex/hooks.json",
                     "harness/hook-policy.json", "harness/active-task.json"):
            self.assertTrue((self.root / name).is_file(), name)
        inv = self.command("harness/common/inventory.py","--tier","Standard","--runtime","codex")
        self.assertEqual(inv.returncode, 0, inv.stdout + inv.stderr)
        status = self.command("harness/common/status.py","--tier","Standard","--runtime","codex")
        self.assertEqual(status.returncode, 2)
        self.assertIn("REMAINING_CAPABILITIES:", status.stdout)

    def test_stop_bounded_when_checks_fail(self):
        self.assertEqual(self.hook_call("Stop"), {})
        source = self.root / "docs/CRITERIA.md"
        source.write_text(source.read_text(encoding="utf-8")+"\nREQ-123\n", encoding="utf-8")
        evidence = self.root / "docs/reports/proof.txt"
        evidence.write_text("observed", encoding="utf-8")
        task = dict(status="ACTIVE", goal_id="G-001", theory_ids=["REQ-123"],
                    tests=["docs/CRITERIA.md"], evidence=["docs/reports/proof.txt"])
        (self.root / "harness/active-task.json").write_text(json.dumps(task), encoding="utf-8")
        cfg = self.root / "harness/common/checks.json"
        cfg.write_text(json.dumps({"checks":[{"name":"fail","argv":[sys.executable,"-c",
                            "import sys; sys.exit(7)"],"timeout_seconds":10}]}), encoding="utf-8")
        self.assertEqual(self.hook_call("Stop").get("decision"), "block")
        retry = self.hook_call("Stop", stop_hook_active=True)
        self.assertNotIn("decision", retry)
        cfg.write_text(json.dumps({"checks":[{"name":"pass","argv":[sys.executable,"-c",
                            "print('ok')"],"timeout_seconds":10}]}), encoding="utf-8")
        self.assertIn("script checks passed", self.hook_call("Stop").get("systemMessage",""))

if __name__ == "__main__":
    unittest.main(verbosity=2)
