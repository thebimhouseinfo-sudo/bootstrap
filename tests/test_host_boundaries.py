#!/usr/bin/env python3
"""Native Copilot files are packaged; never claim live interception without a host test."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"


def call(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True,
                          text=True, timeout=50)


class HostBoundaryTests(unittest.TestCase):
    def test_copilot_generic_has_explicit_missing_hook_warning_and_no_native_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            flags = ["--target", target, "--tier", "Standard", "--runtime",
                     "generic", "--target-app", "copilot", "--staged"]
            preview = call(INSTALL, *flags)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            for marker in ("native adapter NOT INSTALLED", "HOOKS", "GUIDED_ONLY",
                           "NATIVE_HOOKS_NOT_INSTALLED", "CRITERIA_WRITE_GUARD_NOT_CONFIGURED"):
                self.assertIn(marker, preview.stdout)
            applied = call(INSTALL, *flags, "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            self.assertTrue((target / ".github/hooks/bootstrap-criteria.json").is_file())
            self.assertTrue((target / ".github/hooks/criteria_guard.py").is_file())
            self.assertTrue((target / ".github/agents/planner.agent.md").is_file())
            self.assertTrue((target / ".github/agents/advisor.agent.md").is_file())
            self.assertIn("COPILOT_NATIVE_FILES", applied.stdout)
            self.assertTrue((target / ".generic/platforms/copilot.md").is_file())
            status = json.loads((target / "harness/setup-state.json").read_text())
            self.assertEqual(status["phase"], "BOOTSTRAPPING")

    def test_codex_cloud_same_task_checklist_never_fabricates_native_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            flags = ["--target", target, "--tier", "Standard",
                     "--runtime", "codex", "--staged"]
            done = call(INSTALL, *flags, "--apply")
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            state_path = target / "harness/setup-state.json"
            original = state_path.read_bytes()
            host = target / "harness/common/setup_lifecycle.py"
            result = call(host, "host-test", "--surface", "codex-cloud")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for marker in ("CODEX_CLOUD_LIMITED_VERIFICATION", "CURRENT cloud task",
                           "SCRIPT_TESTED", "MANUAL_HANDOFF_REQUIRED"):
                self.assertIn(marker, result.stdout)
            self.assertNotIn("Open a NEW coding agent tab", result.stdout)
            self.assertEqual(state_path.read_bytes(), original)
            ordinary = call(host, "host-test")
            self.assertEqual(ordinary.returncode, 0)
            self.assertIn("Open a NEW coding agent tab", ordinary.stdout)

    def test_codex_cloud_verification_is_not_claimed_by_generic_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp)
            applied = call(INSTALL, "--target", target, "--tier", "Standard",
                           "--runtime", "generic", "--target-app", "copilot", "--staged", "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            result = call(target / "harness/common/setup_lifecycle.py", "host-test",
                          "--surface", "codex-cloud")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("require primary runtime codex", result.stdout)


if __name__ == "__main__":
    unittest.main()
