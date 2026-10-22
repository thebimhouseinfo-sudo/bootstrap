#!/usr/bin/env python3
"""Bootstrap staged first-install and split-doc regressions (no native host claims)."""
import json
import runpy
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]


def call(*args, cwd=None, payload=None):
    return subprocess.run([str(x) for x in args], cwd=cwd, input=payload,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=45)



def fixture_action(tool, action, evidence, cwd):
    """Exercise internal transitions in CI, without claiming human confirmation."""
    code = ("import runpy,sys; m=runpy.run_path(sys.argv[1]);"
            "sys.exit(m[sys.argv[2]](sys.argv[3]))")
    return call(sys.executable, "-c", code, tool, action, evidence, cwd=cwd)


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

    def record_native_dialog_fixture(self, runtime="codex"):
        """Synthetic trace validates format only; it is not a real host dialog."""
        record = {"schema_version": 1, "channel": "native_dialog", "runtime": runtime,
                  "host_event_ref": None,
                  "responses": [
                      {"id": "tier", "value": "Standard", "source": "native_dialog"},
                      {"id": "git_mode", "value": "tracked", "source": "native_dialog"}]}
        (self.root / "harness/setup-intake.json").write_text(
            json.dumps(record), encoding="utf-8")

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
        result = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                      "smoke", cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SMOKE_DENY: PASS", result.stdout)

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


    def test_activation_postlock_handoff_and_hash_drift_fixture(self):
        """Mechanical fixture only: do not mislabel these JSON files as actual host testimony."""
        self.install()
        self.record_native_dialog_fixture("codex")
        (self.root / "docs/CRITERIA.md").write_text("Status: APPROVED\nREQ-1: expected behavior\n", encoding="utf-8")
        (self.root / "docs/ARCHITECTURE.md").write_text("# Accepted architecture\nUses Python.\n", encoding="utf-8")
        (self.root / "docs/PROJECT_PROFILE.md").write_text("# Verified host profile\nPython SDK identified.\n", encoding="utf-8")
        (self.root / "harness/common/checks.json").write_text(json.dumps(
            {"checks": [{"name": "fixture", "argv": [sys.executable, "-c", "print('fixture')"]}]}),
            encoding="utf-8")
        evidence = self.root / "harness/setup-live-evidence.json"
        evidence.write_text(json.dumps({
            "runtime": "codex", "host_version": "fixture-only",
            "fresh_session": True, "hook_dispatched": True,
            "allow_observed": True, "deny_observed": True,
            "notes": "CI synthetic data, NOT real host verification"}), encoding="utf-8")
        command = self.root / "harness/common/setup_lifecycle.py"
        blocked = call(sys.executable, command, "activate", "--evidence", evidence, cwd=self.root)
        self.assertEqual(blocked.returncode, 2)
        locked = fixture_action(command, "activate", evidence, self.root)
        self.assertEqual(locked.returncode, 0, locked.stdout + locked.stderr)
        self.assertIn("POST-LOCK", locked.stdout)
        self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["phase"], "READY")
        self.assertEqual(call(sys.executable, command, "status", cwd=self.root).returncode, 0)
        self.assertEqual(call(sys.executable, command, "finalize", "--post-lock-evidence",
                              evidence, "--human-approved", cwd=self.root).returncode, 2)
        post = self.root / "harness/setup-postlock-evidence.json"
        post.write_text(json.dumps({
            "runtime": "codex", "host_version": "fixture-only",
            "fresh_session": True, "hook_dispatched": True,
            "post_lock_allow": True, "post_lock_deny": True,
            "notes": "Synthetic CI fixture, not attested host"}), encoding="utf-8")
        handoff = fixture_action(command, "finalize", post, self.root)
        self.assertEqual(handoff.returncode, 0, handoff.stdout + handoff.stderr)
        self.assertIn("GOALMAP", handoff.stdout)
        self.assertEqual(json.loads((self.root / "harness/setup-state.json").read_text())["phase"],
                         "HANDOFF_COMPLETE")
        hook = self.root / "harness/hook-policy.json"
        hook.write_text(hook.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        status = call(sys.executable, command, "status", cwd=self.root)
        self.assertEqual(status.returncode, 2)
        self.assertIn("DRIFT", status.stdout)


    def test_continue_handoff_remains_guided_only(self):
        self.install("continue")
        self.record_native_dialog_fixture("continue")
        (self.root / "docs/CRITERIA.md").write_text("Status: APPROVED\nREQ-1: expected behavior\n", encoding="utf-8")
        (self.root / "docs/ARCHITECTURE.md").write_text("# Approved architecture\nRuntime selected.\n", encoding="utf-8")
        (self.root / "docs/PROJECT_PROFILE.md").write_text("# Verified profile\nChosen provider and models.\n", encoding="utf-8")
        (self.root / "harness/common/checks.json").write_text(json.dumps(
            {"checks": [{"name": "fixture", "argv": [sys.executable, "-c", "pass"]}]}), encoding="utf-8")
        tool = self.root / "harness/common/setup_lifecycle.py"
        evidence = self.root / "harness/setup-live-evidence.json"
        evidence.write_text(json.dumps({
            "runtime": "continue", "host_version": "CI fixture",
            "fresh_session": True, "roles_loaded": True, "checks_executed": True,
            "native_hook_available": False, "notes": "Synthetic observations only"}), encoding="utf-8")
        active = fixture_action(tool, "activate", evidence, self.root)
        self.assertEqual(active.returncode, 0, active.stdout + active.stderr)
        self.assertIn("READY_WITH_LIMITATIONS", active.stdout)
        status = call(sys.executable, tool, "status", cwd=self.root)
        self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
        self.assertIn("HASHES_MATCH", status.stdout)
        post = self.root / "harness/setup-postlock-evidence.json"
        post.write_text(json.dumps({
            "runtime": "continue", "host_version": "CI fixture",
            "fresh_session": True, "roles_loaded": True, "checks_executed": True,
            "post_lock_allow": True, "notes": "Synthetic observations only"}), encoding="utf-8")
        handoff = fixture_action(tool, "finalize", post, self.root)
        self.assertEqual(handoff.returncode, 0, handoff.stdout + handoff.stderr)
        self.assertIn("GUIDED_ONLY", handoff.stdout)


    def test_activation_refuses_agent_run_even_with_human_approved_flag(self):
        self.install()
        tool = self.root / "harness/common/setup_lifecycle.py"
        evidence = self.root / "harness/setup-live-evidence.json"
        evidence.write_text('{"runtime":"codex"}', encoding="utf-8")
        for action, name in (("activate", "--evidence"),
                             ("finalize", "--post-lock-evidence")):
            for flags in ([], ["--human-approved"]):
                result = call(sys.executable, tool, action, name, evidence,
                              *flags, cwd=self.root)
                self.assertEqual(result.returncode, 2)
                self.assertIn("interactive terminal", result.stdout)

    def test_host_test_prints_keep_setup_tab_open(self):
        self.install()
        result = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                      "host-test", cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DO NOT CLOSE", result.stdout)
        self.assertIn("DISPOSABLE", result.stdout)


    def test_packaged_gitkeep_and_versioned_install_manifest(self):
        self.install()
        self.assertTrue((self.root / "docs/reports/.gitkeep").is_file())
        path = self.root / "harness/.bootstrap-manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertIn("docs/reports/.gitkeep", data["files"])
        self.assertEqual(len(data["files"]["AGENTS.md"]["installed_sha256"]), 64)
        again = call(sys.executable, self.installer, "--target", self.root, "--runtime",
                     "codex", "--config-git", "tracked", "--staged", "--apply")
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertEqual(json.loads(path.read_text()), data)

    def test_recovery_requires_interactive_terminal_and_does_not_change_hooks(self):
        self.install()
        hook = self.root / ".codex/hooks.json"
        before = hook.read_bytes()
        recovery = self.root / "harness/common/recover.py"
        info = call(sys.executable, recovery, "--runtime", "codex", "inspect", cwd=self.root)
        self.assertEqual(info.returncode, 0, info.stdout + info.stderr)
        denied = call(sys.executable, recovery, "--runtime", "codex", "disable", cwd=self.root)
        self.assertEqual(denied.returncode, 2)
        self.assertIn("interactive", denied.stdout)
        self.assertEqual(hook.read_bytes(), before)
        backups = self.root / "harness/recovery-backups"
        self.assertFalse(backups.exists())



    def test_manual_recovery_mechanics_with_synthetic_confirmation(self):
        """CI bypass is ONLY for testing the mechanics, never human authentication."""
        self.install()
        hook = self.root / ".codex/hooks.json"
        before = hook.read_bytes()
        script = self.root / "harness/common/recover.py"
        code = (
            "import runpy,sys\n"
            "m=runpy.run_path(sys.argv[1])\n"
            "g=m['main'].__globals__\n"
            "g['confirm']=lambda action: None\n"
            "sys.exit(m['main'](sys.argv[2:]))\n"
        )
        disabled = call(sys.executable, "-c", code, script, "--runtime", "codex",
                        "disable", cwd=self.root)
        self.assertEqual(disabled.returncode, 0, disabled.stdout + disabled.stderr)
        self.assertFalse(hook.exists())
        backup_id = disabled.stdout.split("RECOVERY_BACKUP: ")[1].splitlines()[0].replace(chr(92), "/").split("/")[-1]
        restored = call(sys.executable, "-c", code, script, "--runtime", "codex",
                        "restore", "--backup", backup_id, cwd=self.root)
        self.assertEqual(restored.returncode, 0, restored.stdout + restored.stderr)
        self.assertEqual(hook.read_bytes(), before)

    def test_explicit_upgrade_preserves_user_modified_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkout = pathlib.Path(tmp) / "bootstrap-copy"
            checkout.mkdir()
            shutil.copy2(REPO / "install.py", checkout / "install.py")
            shutil.copytree(REPO / "project-template", checkout / "project-template")
            installer = checkout / "install.py"
            flags = [sys.executable, installer, "--target", self.root, "--runtime",
                     "codex", "--config-git", "tracked", "--staged"]
            first = call(*flags, "--apply")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            source = checkout / "project-template/docs/ARCHITECTURE.md"
            target = self.root / "docs/ARCHITECTURE.md"
            modified_source = source.read_text(encoding="utf-8") + "\n# Compatible update\n"
            source.write_text(modified_source, encoding="utf-8")
            without = call(*flags)
            self.assertIn("CONFLICT docs/ARCHITECTURE.md", without.stdout)
            preview = call(*flags, "--upgrade")
            self.assertIn("UPGRADE docs/ARCHITECTURE.md", preview.stdout)
            upgraded = call(*flags, "--upgrade", "--apply")
            self.assertEqual(upgraded.returncode, 0, upgraded.stdout + upgraded.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), modified_source)
            target.write_text("HUMAN EDIT\n", encoding="utf-8")
            source.write_text(modified_source + "further change\n", encoding="utf-8")
            rejected = call(*flags, "--upgrade", "--apply")
            self.assertEqual(rejected.returncode, 2, rejected.stdout + rejected.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "HUMAN EDIT\n")


    def test_missing_template_gitignore_fails_cleanly_without_partial_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkout = pathlib.Path(tmp) / "clone"
            checkout.mkdir()
            shutil.copy2(REPO / "install.py", checkout / "install.py")
            shutil.copytree(REPO / "project-template", checkout / "project-template")
            (checkout / "project-template/.gitignore").unlink()
            result = call(sys.executable, checkout / "install.py", "--target", self.root,
                          "--runtime", "codex", "--staged", "--apply")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("missing required .gitignore source", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((self.root / "AGENTS.md").exists())
            self.assertFalse((self.root / ".gitignore").exists())

    def test_mid_install_failure_rolls_back_files_and_gitignore(self):
        with tempfile.TemporaryDirectory() as temp:
            checkout = pathlib.Path(temp) / "checkout"
            checkout.mkdir()
            shutil.copy2(REPO / "install.py", checkout / "install.py")
            shutil.copytree(REPO / "project-template", checkout / "project-template")
            program = (
                "import runpy,sys\n"
                "ns=runpy.run_path(sys.argv[1])\n"
                "g=ns['main'].__globals__\n"
                "orig=g['safe_copy']\n"
                "counter=[0]\n"
                "def fail_after_one(root,source,target):\n"
                "    counter[0]+=1\n"
                "    if counter[0]==2: raise OSError('fixture injected failure')\n"
                "    return orig(root,source,target)\n"
                "g['safe_copy']=fail_after_one\n"
                "sys.argv=[sys.argv[1]]+sys.argv[2:]\n"
                "sys.exit(ns['main']())\n"
            )
            result = call(sys.executable, "-c", program, checkout / "install.py",
                          "--target", self.root, "--runtime", "codex", "--staged", "--apply")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("ROLLBACK", result.stdout)
            self.assertFalse((self.root / ".gitignore").exists())
            self.assertFalse((self.root / "harness/setup-state.json").exists())
            self.assertFalse((self.root / "harness/.bootstrap-manifest.json").exists())
            self.assertFalse((self.root / "AGENTS.md").exists())

    def test_user_guides_target_coding_agents_not_web_reviewers(self):
        vi = (REPO / "README.md").read_text(encoding="utf-8")
        en = (REPO / "docs/user-guide.en.md").read_text(encoding="utf-8")
        ai = (REPO / "docs/FOR_AI.md").read_text(encoding="utf-8")
        for guide in (vi, en):
            self.assertNotIn("git clone --depth", guide)
            self.assertNotIn("python install.py --target", guide)
            self.assertIn("raw.githubusercontent.com", guide)
        self.assertIn("Coding-agent execution and capability boundary", ai)
        self.assertIn("do not claim setup was performed", ai)
        self.assertIn("CONFIRM", (REPO / "project-template/harness/common/setup_lifecycle.py").read_text(encoding="utf-8"))

    def test_user_guides_have_two_compact_onboarding_prompts(self):
        vi = (REPO / "README.md").read_text(encoding="utf-8")
        en = (REPO / "docs/user-guide.en.md").read_text(encoding="utf-8")
        a, b = vi.split("## 1. Greenfield")[1].split("## 2. Brownfield")
        prompt_a = a.splitlines()[2]
        prompt_b = b.splitlines()[2]
        self.assertLess(len(prompt_a), 450)
        self.assertLess(len(prompt_b), 450)
        self.assertIn("<ĐƯỜNG_DẪN_DỰ_ÁN>", prompt_a)
        self.assertIn("<ĐƯỜNG_DẪN_DỰ_ÁN>", prompt_b)
        self.assertIn("raw.githubusercontent.com", prompt_a)
        self.assertIn("raw.githubusercontent.com", prompt_b)
        english_a, english_b = en.split("## 1. Greenfield")[1].split("## 2. Brownfield")
        self.assertLess(len(english_a.splitlines()[2]), 380)
        self.assertLess(len(english_b.splitlines()[2]), 380)
        self.assertIn("<PROJECT_FOLDER_PATH>", english_a)
        self.assertIn("<PROJECT_FOLDER_PATH>", english_b)

    def test_staged_audit_requires_interactive_intake_trace(self):
        self.install()
        tool = self.root / "harness/common/setup_lifecycle.py"
        absent = call(sys.executable, tool, "audit", cwd=self.root)
        self.assertEqual(absent.returncode, 2)
        self.assertIn("IDE-dialog/CLI-menu setup-intake trace missing", absent.stdout)
        self.record_native_dialog_fixture()
        valid = call(sys.executable, tool, "audit", cwd=self.root)
        self.assertIn("SETUP_INTAKE: RECORDED", valid.stdout)
        # Other intentionally unconfigured components still prevent final readiness.
        self.assertEqual(valid.returncode, 2)
        path = self.root / "harness/setup-intake.json"
        for corruption in (
            {"schema_version": 1, "channel": "permission_dialog", "runtime": "codex",
             "responses": [{"id": "git_mode", "value": "tracked", "source": "native_dialog"}]},
            {"schema_version": 1, "channel": "native_dialog", "runtime": "claude",
             "responses": [{"id": "git_mode", "value": "tracked", "source": "native_dialog"}]},
            {"schema_version": 1, "channel": "native_dialog", "runtime": "codex",
             "responses": [{"id": "git_mode", "value": "tracked", "source": "chat"}]},
        ):
            path.write_text(json.dumps(corruption), encoding="utf-8")
            invalid = call(sys.executable, tool, "audit", cwd=self.root)
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("IDE-dialog/CLI-menu setup-intake trace missing", invalid.stdout)

    def test_permission_notice_and_ide_cli_documentation(self):
        vi = (REPO / "README.md").read_text(encoding="utf-8")
        en = (REPO / "docs/user-guide.en.md").read_text(encoding="utf-8")
        ai = (REPO / "docs/FOR_AI.md").read_text(encoding="utf-8")
        spec = (REPO / "project-template/harness/specs/SETUP_INTAKE.md").read_text(encoding="utf-8")
        for guide in (vi, en):
            self.assertIn("dialog", guide.lower())
            self.assertIn("raw.githubusercontent.com", guide)
        self.assertIn("chat notification", ai)
        self.assertIn("CLI numbered", ai)
        self.assertIn("setup-intake.json", spec)
        self.assertIn("INTERACTIVE_INTAKE_UNAVAILABLE", ai)

    def test_cli_numbered_menu_records_real_choice_values_in_local_trace(self):
        self.install("codex")
        path = self.root / "harness/common/setup_intake.py"
        self.assertTrue(path.is_file())
        no_tty = call(sys.executable, path, cwd=self.root)
        self.assertEqual(no_tty.returncode, 2)
        self.assertIn("INTERACTIVE_INTAKE_UNAVAILABLE", no_tty.stdout)
        self.assertFalse((self.root / "harness/setup-intake.json").exists())
        module = runpy.run_path(str(path))
        answers = iter(["1", "1", "1", "2", "2", "2", "upgrade/v5"])
        output = []
        result = module["collect"]("codex", input_fn=lambda prompt: next(answers),
                                    output_fn=output.append)
        self.assertEqual(result["channel"], "cli_menu")
        self.assertEqual(result["runtimes"], ["codex"])
        self.assertEqual([r["value"] for r in result["responses"]],
                         ["Standard", "tracked", "upgrade/v5"])
        self.assertTrue(any("1) Lite" in row for row in output))
        self.assertTrue(any("2) Standard" in row for row in output))
        created = module["write_trace"](self.root, result)
        self.assertEqual(json.loads(created.read_text(encoding="utf-8")), result)
        with self.assertRaises(ValueError):
            module["write_trace"](self.root, result)
        audit = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                     "audit", cwd=self.root)
        self.assertIn("SETUP_INTAKE: RECORDED", audit.stdout)
        self.assertNotIn("setup-intake trace missing", audit.stdout)
        self.assertEqual(audit.returncode, 2)  # Other mandatory choices still OPEN

    def test_preinstall_cli_choices_are_imported_before_tier_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            ref = pathlib.Path(tmp) / "preinstall-intake.json"
            src = runpy.run_path(str(REPO / "project-template/harness/common/setup_intake.py"))
            answers = iter(["1", "1", "1", "3", "2", "1"])
            selected = src["collect"]("codex", input_fn=lambda prompt: next(answers),
                                     output_fn=lambda message: None)
            ref.write_text(json.dumps(selected), encoding="utf-8")
            flags = [sys.executable, self.installer, "--target", self.root,
                     "--runtime", "codex", "--tier", "Full",
                     "--config-git", "tracked", "--intake-file", ref, "--staged"]
            preview = call(*flags)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertFalse((self.root / "harness/setup-state.json").exists())
            applied = call(*flags, "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            self.assertIn("SETUP_INTAKE: copied", applied.stdout)
            state = json.loads((self.root / "harness/setup-state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["tier"], "Full")
            saved = json.loads((self.root / "harness/setup-intake.json").read_text(encoding="utf-8"))
            self.assertEqual(saved, selected)
            self.assertEqual(saved["runtimes"], ["codex"])
            audit = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                         "audit", cwd=self.root)
            self.assertIn("SETUP_INTAKE: RECORDED", audit.stdout)

    def test_installed_tier_and_runtime_cannot_change_without_migration(self):
        self.install("codex")
        trace = self.root / "harness/.bootstrap-manifest.json"
        state = self.root / "harness/setup-state.json"
        old_manifest = trace.read_bytes()
        old_state = state.read_bytes()
        for other_tier, other_runtime in (("Lite", "codex"),
                                          ("Full", "codex"),
                                          ("Standard", "claude")):
            for optional in ([], ["--upgrade"]):
                flags = [sys.executable, self.installer, "--target", self.root,
                         "--runtime", other_runtime, "--tier", other_tier,
                         "--config-git", "tracked", "--staged", *optional, "--apply"]
                failure = call(*flags)
                self.assertEqual(failure.returncode, 2, failure.stdout + failure.stderr)
                self.assertIn("MIGRATION_REQUIRED", failure.stdout)
                self.assertEqual(trace.read_bytes(), old_manifest)
                self.assertEqual(state.read_bytes(), old_state)
        self.assertFalse((self.root / ".claude/settings.json").exists())

    def test_preinstall_mismatched_tier_or_git_choice_blocks_before_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            ref = pathlib.Path(tmp) / "intake.json"
            ref.write_text(json.dumps({
                "schema_version": 1, "channel": "cli_menu", "runtime": "codex",
                "responses": [
                    {"id": "tier", "value": "Full", "source": "cli_menu"},
                    {"id": "git_mode", "value": "tracked", "source": "cli_menu"}
                ]}), encoding="utf-8")
            flags = [sys.executable, self.installer, "--target", self.root,
                     "--runtime", "codex", "--staged", "--intake-file", ref, "--apply"]
            rejected = call(*flags)
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("disagree with selected questionnaire", rejected.stdout)
            self.assertFalse((self.root / "AGENTS.md").exists())
            self.assertFalse((self.root / "harness/setup-state.json").exists())

    def test_malformed_staged_state_must_not_disable_hook_guards(self):
        self.install("codex")
        tool = self.root / "harness/common/setup_lifecycle.py"
        state = self.root / "harness/setup-state.json"
        for bad in ('{bad json', '{"schema_version":1,"phase":"NOT_A_PHASE","runtime":"codex"}'):
            state.write_text(bad, encoding="utf-8")
            module = runpy.run_path(str(tool))
            self.assertFalse(module["stage_active"]())
            audit = call(sys.executable, tool, "audit", cwd=self.root)
            self.assertEqual(audit.returncode, 2)
            self.assertIn("setup-state.json malformed", audit.stdout)

    def test_cli_menu_invalid_answers_or_cancel_are_not_saved(self):
        self.install("codex")
        path = self.root / "harness/common/setup_intake.py"
        module = runpy.run_path(str(path))
        answers = iter(["invalid", "4", "q"])
        with self.assertRaises(ValueError):
            module["collect"]("codex", input_fn=lambda prompt: next(answers),
                              output_fn=lambda msg: None)
        self.assertFalse((self.root / "harness/setup-intake.json").exists())
        self.assertFalse(module["branch_name"]("../escape"))
        self.assertTrue(module["branch_name"]("upgrade/v5"))

    def test_cli_menu_rejects_invalid_source_and_mismatched_runtime(self):
        self.install("codex")
        path = self.root / "harness/setup-intake.json"
        for channel, source, runtime in (
            ("cli_menu", "permission_dialog", "codex"),
            ("cli_menu", "cli_menu", "claude"),
            ("chat", "chat", "codex"),
        ):
            path.write_text(json.dumps({
                "schema_version": 1, "channel": channel, "runtime": runtime,
                "responses": [{"id": "git_mode", "value": "local", "source": source}],
            }), encoding="utf-8")
            audit = call(sys.executable, self.root / "harness/common/setup_lifecycle.py",
                         "audit", cwd=self.root)
            self.assertIn("setup-intake trace missing", audit.stdout)
            self.assertEqual(audit.returncode, 2)

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
