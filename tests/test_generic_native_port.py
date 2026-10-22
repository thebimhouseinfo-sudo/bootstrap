#!/usr/bin/env python3
"""Generic setup: platform-neutral scripts require a real host-specific port."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.py"


def call(*args):
    return subprocess.run([sys.executable, *map(str, args)],
                          capture_output=True, text=True, timeout=50)


def fixture_transition(tool, action, evidence):
    # A CI fixture exercises state transitions, NOT a trusted Human terminal.
    code = "import runpy,sys; m=runpy.run_path(sys.argv[1]); sys.exit(m[sys.argv[2]](sys.argv[3]))"
    return subprocess.run([sys.executable, "-c", code, str(tool), action, str(evidence)],
                          capture_output=True, text=True, timeout=50)


class GenericNativePortTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        flags = [INSTALL, "--target", self.root, "--tier", "Standard", "--runtime",
                 "generic", "--target-app", "opencode", "--staged"]
        preview = call(*flags)
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn("ADAPTER_REQUIREMENTS.md", preview.stdout)
        result = call(*flags, "--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PORT_REQUIRED", result.stdout)
        self.assertTrue((self.root / ".generic/ADAPTER_REQUIREMENTS.md").is_file())
        manifest = json.loads((self.root / "harness/.bootstrap-manifest.json").read_text())
        self.assertEqual(manifest["target_app"], "opencode")
        self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["target_app"], "opencode")
        self.tool = self.root / "harness/common/setup_lifecycle.py"

    def configure(self):
        intake = {"schema_version": 1, "channel": "native_dialog", "runtime": "generic",
                  "responses": [{"id": "tier", "value": "Standard", "source": "native_dialog"},
                                {"id": "git_mode", "value": "local", "source": "native_dialog"}]}
        (self.root / "harness/setup-intake.json").write_text(json.dumps(intake))
        (self.root / "docs/CRITERIA.md").write_text("STATUS: APPROVED\nREQ1: test\n")
        (self.root / "docs/ARCHITECTURE.md").write_text("# Verified stack\nLocal runtime.\n")
        (self.root / "docs/PROJECT_PROFILE.md").write_text("# Verified host\nOpenCode.\n")
        (self.root / "harness/common/checks.json").write_text(json.dumps(
            {"checks": [{"name": "test", "argv": [sys.executable, "-c", "print('fixture')"]}]}))

    def evidence(self, **changes):
        data = {"runtime": "generic", "host_version": "CI fixture—not a real host",
                "fresh_session": True, "roles_loaded": True, "checks_executed": True,
                "target_app": "opencode",
                "port_attempted": True, "host_api_evidence": "Synthetic fixture observed host schema",
                "native_hook_available": True, "hook_dispatched": True,
                "allow_observed": True, "deny_observed": True,
                "native_adapter_paths": [".opencode/bootstrap-hooks.py"],
                "notes": "Synthetic fixture only; not trustworthy authorization"}
        data.update(changes)
        file = self.root / "harness/setup-live-evidence.json"
        file.write_text(json.dumps(data))
        return file

    def test_agent_generated_hook_can_be_registered_and_hash_tracked(self):
        self.configure()
        hook = self.root / ".opencode/bootstrap-hooks.py"
        hook.parent.mkdir()
        hook.write_text("# fixture generated host hook\n")
        guidance = call(self.tool, "host-test")
        self.assertEqual(guidance.returncode, 0)
        self.assertIn("WRITE AND REGISTER", guidance.stdout)
        success = fixture_transition(self.tool, "activate", self.evidence())
        self.assertEqual(success.returncode, 0, success.stdout + success.stderr)
        self.assertIn("READY:", success.stdout)
        state = json.loads((self.root / "harness/setup-state.json").read_text())
        self.assertEqual(state["native_adapter_paths"], [".opencode/bootstrap-hooks.py"])
        self.assertIn(".opencode/bootstrap-hooks.py", state["locked_files"])
        hook.write_text("# mutated after registration\n")
        changed = call(self.tool, "status")
        self.assertEqual(changed.returncode, 2, changed.stdout)
        self.assertIn("DRIFT", changed.stdout)

    def test_port_step_cannot_be_skipped_at_activation(self):
        self.configure()
        hook = self.root / ".opencode/bootstrap-hooks.py"
        hook.parent.mkdir()
        hook.write_text("# fixture")
        result = fixture_transition(self.tool, "activate", self.evidence(port_attempted=False))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("must attempt host-native port", result.stdout)

    def test_installer_requires_native_directory_migration(self):
        flags = [INSTALL, "--target", self.root, "--tier", "Standard", "--runtime",
                 "generic", "--target-app", "opencode", "--staged"]
        preview = call(*flags)
        self.assertIn("HOST_NATIVE_MIGRATION_REQUIRED", preview.stdout)
        self.assertTrue((self.root / ".generic/HOST_NATIVE_LAYOUT.md").is_file())
        guidance = call(self.tool, "host-test")
        self.assertIn("WRITE AND REGISTER", guidance.stdout)

    def test_generic_source_file_cannot_pass_as_native_adapter(self):
        self.configure()
        result = fixture_transition(self.tool, "activate", self.evidence(
            native_adapter_paths=[".generic/agents/planner.md"]))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("NOT host-native adapter paths", result.stdout)
        self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["phase"],
                         "BOOTSTRAPPING")

    def test_native_claim_must_match_actual_installed_host(self):
        self.configure()
        hook = self.root / ".opencode/bootstrap-hooks.py"
        hook.parent.mkdir()
        hook.write_text("# fixture\n")
        result = fixture_transition(self.tool, "activate", self.evidence(target_app="copilot"))
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("target_app differs", result.stdout)

    def test_unregistered_or_traversal_paths_rejected(self):
        self.configure()
        for bad in ([".opencode/missing.py"], ["../escape.py"], [], ["/tmp/outside.py"]):
            result = fixture_transition(self.tool, "activate",
                                        self.evidence(native_adapter_paths=bad))
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["phase"],
                             "BOOTSTRAPPING")

    def test_unsupported_host_falls_back_only_with_explicit_limitations(self):
        self.configure()
        result = fixture_transition(self.tool, "activate", self.evidence(
            native_hook_available=False, native_adapter_paths=[],
            hook_dispatched=False, allow_observed=False, deny_observed=False))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("READY_WITH_LIMITATIONS", result.stdout)
        state = json.loads((self.root / "harness/setup-state.json").read_text())
        self.assertEqual(state["phase"], "READY_WITH_LIMITATIONS")


if __name__ == "__main__":
    unittest.main()
