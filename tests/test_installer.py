#!/usr/bin/env python3
"""Cross-platform, non-destructive bootstrap installer and native adapter regressions."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "project-template"
INSTALLER = ROOT / "install.py"
INVENTORY = SOURCE / "harness/common/inventory.py"
TIERS = ("Lite", "Standard", "Full")
RUNTIMES = ("codex", "antigravity", "claude", "continue", "copilot", "generic")
EXPECTED = {
    "Lite": {"coder", "reviewer", "advisor"},
    "Standard": {"coder", "reviewer", "advisor", "planner", "tester", "critic", "explorer"},
    "Full": {"coder", "reviewer", "advisor", "planner", "tester", "critic", "explorer", "harness-fixer"},
}

def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)],
                          capture_output=True, text=True, timeout=40)

class InstallTests(unittest.TestCase):
    def test_all_fifteen_tier_runtime_installations(self):
        for tier in TIERS:
            for runtime in RUNTIMES:
                with self.subTest(tier=tier, runtime=runtime), tempfile.TemporaryDirectory() as d:
                    root = pathlib.Path(d)
                    flags = ("--target", root, "--tier", tier, "--runtime", runtime)
                    if runtime == "generic":
                        flags += ("--target-app", "cline")
                    preview = run(INSTALLER, *flags)
                    self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
                    self.assertFalse((root / "AGENTS.md").exists())
                    applied = run(INSTALLER, *flags, "--apply")
                    self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
                    again = run(INSTALLER, *flags, "--apply")
                    self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
                    self.assertIn("SAME", again.stdout)
                    self.assertFalse((root / "README.md").exists())
                    self.assertTrue((root / "harness/common/verify.py").is_file())
                    self.assertTrue((root / "harness/common/checks.json").is_file())
                    self.assertTrue((root / "harness/common/branch_authority.py").is_file())
                    self.assertTrue((root / "harness/config/branch-authority.example.json").is_file())
                    self.assertFalse((root / ".git/bootstrap/branch-authority.json").exists())
                    branch = run(root / "harness/common/branch_authority.py", "status")
                    self.assertEqual(branch.returncode, 2, branch.stdout + branch.stderr)
                    installed = {x.stem for x in (root / ".agents/roles").glob("*.md")}
                    self.assertEqual(installed, EXPECTED[tier])
                    for other in RUNTIMES:
                        path = {"codex": ".codex/agents", "antigravity": ".antigravity/agents", "claude": ".claude/agents",
                                "continue": ".continue/agents", "copilot": ".github/agents", "generic": ".generic/agents"}[other]
                        self.assertEqual((root / path).exists(), other == runtime)
                    if runtime == "antigravity":
                        native = {x.stem for x in (root / ".antigravity/agents").glob("*.md")}
                    elif runtime == "codex":
                        native = {x.stem for x in (root / ".codex/agents").glob("*.toml")}
                    elif runtime == "claude":
                        native = {x.stem for x in (root / ".claude/agents").glob("*.md")}
                    elif runtime == "continue":
                        native = {x.name for x in (root / ".continue/agents").iterdir()}
                    elif runtime == "copilot":
                        native = {("advisor" if x.name == "technical-advisor.agent.md" else x.name.removesuffix(".agent.md"))
                                  for x in (root / ".github/agents").glob("*.agent.md")}
                        self.assertTrue((root / ".github/hooks/criteria.json").is_file())
                        self.assertTrue((root / ".github/hooks/criteria-gate.cjs").is_file())
                    else:
                        native = {x.stem for x in (root / ".generic/agents").glob("*.md")}
                        self.assertIn("PORT_REQUIRED", preview.stdout)
                        self.assertTrue((root / ".generic/PORTING.md").is_file())
                    self.assertEqual(native, EXPECTED[tier])
                    self.assertEqual((root / ".generic/agents").exists(), runtime == "generic")
                    self.assertEqual((root / ".agents/hooks.json").exists(), runtime == "antigravity")
                    self.assertEqual((root / ".agents/MODEL_SELECTION.md").exists(), runtime == "antigravity")
                    if runtime == "claude":
                        generic = {x.parent.name for x in (root / ".agents/skills").glob("*/SKILL.md")}
                        native_skills = {x.parent.name for x in (root / ".claude/skills").glob("*/SKILL.md")}
                        self.assertEqual(native_skills, generic)
                    doctor = run(root / "harness/common/inventory.py", "--tier", tier, "--runtime", runtime)
                    self.assertEqual(doctor.returncode, 0, doctor.stdout + doctor.stderr)
                    verifier = run(root / "harness/common/verify.py")
                    self.assertEqual(verifier.returncode, 2, verifier.stdout + verifier.stderr)

    def test_explicit_runtime_required_without_interactive_terminal(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            for flags in ((), ("--apply",), ("--ask-first", "--apply")):
                with self.subTest(flags=flags):
                    p = run(INSTALLER, "--target", root, *flags)
                    self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
                    self.assertFalse((root / "AGENTS.md").exists())
                    self.assertFalse((root / ".antigravity").exists())
            questions = run(INSTALLER, "--ask-first")
            self.assertEqual(questions.returncode, 0, questions.stdout + questions.stderr)
            self.assertIn("ONE-BATCH SETUP QUESTIONS", questions.stdout)
            self.assertIn("Cline, Qwen Code, DeepSeek-based client", questions.stdout)
            self.assertIn("Continue: provider/model selection", questions.stdout)
            self.assertFalse((root / "AGENTS.md").exists())
            for flags in (("--runtime", "generic"), ("--runtime", "generic", "--apply"),
                          ("--runtime", "generic", "--target-app", "copilot"),
                          ("--runtime", "codex", "--target-app", "cline"),
                          ("--runtime", "generic", "--target-app", "../traversal")):
                with self.subTest(generic_flags=flags):
                    p = run(INSTALLER, "--target", root, *flags)
                    self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
                    self.assertFalse((root / ".generic").exists())
            for rel in ("harness/common/inventory.py", "harness/common/status.py"):
                result = run(SOURCE / rel)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_optional_discussion_decision_skill_and_planner_links_are_packaged(self):
        """Script-level packaging/contract test, not live conversational agent PASS."""
        secretary = SOURCE / ".agents/skills/record-decisions/SKILL.md"
        self.assertTrue(secretary.is_file())
        method = secretary.read_text(encoding="utf-8")
        planner = (SOURCE / ".agents/roles/planner.md").read_text(encoding="utf-8")
        plan_task = (SOURCE / ".agents/skills/plan-task/SKILL.md").read_text(encoding="utf-8")
        plan_template = (SOURCE / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
        instructions = (SOURCE / "AGENTS.md").read_text(encoding="utf-8")
        for value in ("Only a Human-chosen outcome", "read back", "SUPERSEDED",
                      "rejected alternatives", "UNRESOLVED", "NOT_VERIFIED"):
            self.assertIn(value, method)
        self.assertIn("Optional Discussion Job", planner)
        self.assertIn("record-decisions/SKILL.md", planner)
        self.assertIn("COVERAGE", plan_task)
        self.assertIn("full applicable Human-accepted decision records", plan_task)
        self.assertIn("Accepted Decision references", plan_template)
        self.assertIn("Decision coverage/conflicts/feasibility", plan_template)
        self.assertIn("record-decisions/SKILL.md", instructions)
        # The installer already copies skills via the existing layout. Verify
        # no separate installer/profile architecture change is required.
        for runtime in ("codex", "claude", "continue"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as d:
                target = pathlib.Path(d)
                installed = run(INSTALLER, "--target", target, "--tier",
                                "Standard", "--runtime", runtime, "--apply")
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                self.assertEqual((target / ".agents/skills/record-decisions/SKILL.md").read_text(encoding="utf-8"), method)
                if runtime in ("claude", "continue"):
                    self.assertEqual((target / ("." + runtime) / "skills/record-decisions/SKILL.md").read_text(encoding="utf-8"), method)
                self.assertIn("Accepted Decision references",
                              (target / "docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8"))

    def test_coder_precode_and_user_file_lifecycle_knowledge_are_packaged(self):
        """Static/source packaging contract only; native Coder performance remains unverified."""
        coder = (SOURCE / ".agents/roles/coder.md").read_text(encoding="utf-8")
        implementation = (SOURCE / ".agents/skills/implement-task/SKILL.md").read_text(encoding="utf-8")
        clarification = (SOURCE / ".agents/skills/solution-clarification/SKILL.md").read_text(encoding="utf-8")
        lifecycle = (SOURCE / ".agents/knowledge/operational-file-lifecycle.md").read_text(encoding="utf-8")
        self.assertIn("descriptive Pre-Code", coder)
        self.assertIn("whole related set", coder)
        self.assertIn("Stage A", implementation)
        self.assertIn("no empty", coder)
        self.assertIn("materially missing", clarification)
        self.assertIn("NOT a mandatory file-classifier", lifecycle)
        for example in ("Word:", "AutoCAD:", "CadGPT:", "OPERATION", "DEV",
                        "Temp Job", "DWL/DWL2", "SHA/GUID"):
            self.assertIn(example, lifecycle)
        # Skills/knowledge must use the current installer, no local Worker redesign.
        with tempfile.TemporaryDirectory() as d:
            target = pathlib.Path(d)
            result = run(INSTALLER, "--target", target, "--tier", "Standard",
                         "--runtime", "claude", "--apply")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for part in ("solution-clarification", "implement-task"):
                self.assertTrue((target / ".agents/skills" / part / "SKILL.md").is_file())
                self.assertTrue((target / ".claude/skills" / part / "SKILL.md").is_file())
            self.assertEqual(
                (target / ".agents/knowledge/operational-file-lifecycle.md").read_text(encoding="utf-8"),
                lifecycle)

    def test_reviewer_precode_cross_task_proportionality_contract_is_packaged(self):
        """Enforces shipped Reviewer guidance; not a native Reviewer verdict."""
        review = (SOURCE / ".agents/roles/reviewer.md").read_text(encoding="utf-8")
        skill = (SOURCE / ".agents/skills/goal-review/SKILL.md").read_text(encoding="utf-8")
        template = (SOURCE / "docs/reports/_REVIEW_TEMPLATE.md").read_text(encoding="utf-8")
        for concept in ("ALL related Task", "CHANGES_REQUIRED",
                        "HUMAN_ESCALATION", "Small Function",
                        "same proposal", "PENDING_HUMAN_TEST"):
            self.assertIn(concept, review)
        self.assertIn("PRE-CODE Code Structure Proposal", skill)
        self.assertIn("missing consumers", skill)
        self.assertIn("PRE-CODE design verdict", template)
        self.assertIn("Derived approved components", template)
        self.assertIn("CODE/TEST outcome: PASS / FAIL / UNVERIFIED", template)
        # Critic remains public-artifact-only; not a source or plan reviewer.
        critic = (SOURCE / ".agents/skills/critical-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("do not read private CRITERIA or plan", critic)
        with tempfile.TemporaryDirectory() as d:
            target = pathlib.Path(d)
            result = run(INSTALLER, "--target", target, "--tier",
                         "Standard", "--runtime", "codex", "--apply")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PRE-CODE design verdict",
                          (target / "docs/reports/_REVIEW_TEMPLATE.md").read_text(encoding="utf-8"))

    def test_portable_agent_contracts_remain_identical_to_canonical(self):
        for role in EXPECTED["Full"]:
            self.assertEqual(
                (SOURCE / ".generic/agents" / (role + ".md")).read_bytes(),
                (SOURCE / ".agents/roles" / (role + ".md")).read_bytes(), role)

    def test_continue_reuses_antigravity_shared_core_without_native_leak(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as c:
            ant = pathlib.Path(a)
            cont = pathlib.Path(c)
            for root, runtime in ((ant, "antigravity"), (cont, "continue")):
                result = run(INSTALLER, "--target", root, "--tier", "Standard",
                             "--runtime", runtime, "--apply")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for folder in (".agents/roles", ".agents/skills", ".agents/config", "harness/common"):
                left = sorted((p.relative_to(ant / folder).as_posix(), p.read_bytes())
                              for p in (ant / folder).rglob("*") if p.is_file())
                right = sorted((p.relative_to(cont / folder).as_posix(), p.read_bytes())
                               for p in (cont / folder).rglob("*") if p.is_file())
                self.assertEqual(left, right, folder)
            self.assertFalse((cont / ".agents/hooks.json").exists())
            self.assertFalse((cont / ".agents/MODEL_SELECTION.md").exists())
            self.assertFalse((cont / ".antigravity").exists())
            self.assertTrue((cont / ".continue/config.yaml").is_file())
            self.assertTrue((cont / ".continue/agents/coder/config.yaml").is_file())
            self.assertTrue((ant / ".agents/hooks.json").is_file())

    def test_dirty_project_merge(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            (root / "AGENTS.md").write_text("HUMAN", encoding="utf-8")
            (root / "README.md").write_text("PRODUCT README", encoding="utf-8")
            flags = ("--target", root, "--tier", "Standard", "--runtime", "codex")
            preview = run(INSTALLER, *flags)
            self.assertEqual(preview.returncode, 2)
            self.assertFalse((root / "AGENTS.bootstrap.md").exists())
            applied = run(INSTALLER, *flags, "--apply")
            self.assertEqual(applied.returncode, 2, applied.stdout + applied.stderr)
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), "HUMAN")
            self.assertEqual((root / "README.md").read_text(encoding="utf-8"), "PRODUCT README")
            self.assertTrue((root / "AGENTS.bootstrap.md").is_file())
            self.assertEqual(run(INSTALLER, *flags, "--apply").returncode, 2)

    def test_reject_source_repo_and_nested_target(self):
        for target in (ROOT, SOURCE, ROOT / "tests"):
            with self.subTest(target=str(target)):
                result = run(INSTALLER, "--target", target, "--runtime", "codex", "--apply")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("outside the bootstrap checkout", result.stderr)

    def test_parent_symlink_preflight_does_not_create_external_directory(self):
        with tempfile.TemporaryDirectory() as d:
            base = pathlib.Path(d)
            root, outside = base / "project", base / "outside"
            root.mkdir()
            outside.mkdir()
            try:
                (root / "docs").symlink_to(outside, target_is_directory=True)
            except (NotImplementedError, OSError):
                self.skipTest("Symlink privilege unavailable")
            applied = run(INSTALLER, "--target", root, "--runtime", "codex", "--apply")
            self.assertEqual(applied.returncode, 2, applied.stdout + applied.stderr)
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((root / "AGENTS.md").exists())

    def test_advisor_is_a_decision_stage_role_not_global_agent(self):
        source = (SOURCE / ".agents/roles/advisor.md").read_text(encoding="utf-8")
        self.assertIn("entire proposed CRITERIA", source)
        self.assertIn("human", source.lower())
        self.assertIn("no approval impersonation", source.lower())
        for rel in (".codex/agents/advisor.toml", ".claude/agents/advisor.md",
                    ".continue/agents/advisor/config.yaml"):
            self.assertTrue((SOURCE / rel).is_file(), rel)
        instructions = (SOURCE / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("No standing Advisor loop", instructions)

    def test_technical_advisor_feasibility_and_native_parity(self):
        advisor = (SOURCE / ".agents/roles/advisor.md").read_text(encoding="utf-8")
        required = (
            "Technical Advisor", "CRITERIA is the sole source",
            "current technical state", "limited relevant source code",
            "technical feasibility", "prerequisites", "complexity and cost",
            "completed capabilities", "multiple subsystems", "substantial redesign",
            "observed technical facts", "uncertain", "Plan/Code review",
            "not Reviewer/CR", "no PASS/FAIL verdict",
            "Tạm dùng", "Ổn", "Nâng cao", "OPTIONAL",
            "offline GitHub", "multi-user",
        )
        for phrase in required:
            self.assertIn(phrase.lower(), advisor.lower(), phrase)
        self.assertNotIn("ALWAYS present exactly three", advisor)
        self.assertIn("are OPTIONAL comparison levels", advisor)
        self.assertIn("Human must decide after the advice", advisor)
        self.assertIn("before any CRITERIA file write", advisor)
        self.assertIn("entire proposed CRITERIA", advisor)

        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        with (SOURCE / ".codex/agents/advisor.toml").open("rb") as f:
            codex = tomllib.load(f)
        self.assertEqual(codex["name"], "advisor")
        self.assertNotIn("sandbox_mode", codex)
        self.assertIn(advisor.strip(), codex["developer_instructions"])
        claude = (SOURCE / ".claude/agents/advisor.md").read_text(encoding="utf-8")
        self.assertIn(advisor.strip(), claude)
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML unavailable")
        continue_cfg = yaml.safe_load(
            (SOURCE / ".continue/agents/advisor/config.yaml").read_text(encoding="utf-8"))
        self.assertEqual(continue_cfg["schema"], "v1")
        self.assertIn(advisor.strip(), continue_cfg["rules"][0])
        assignment = yaml.safe_load(
            (SOURCE / ".agents/config/agent-assignment.yaml").read_text(encoding="utf-8"))
        self.assertIn("advisor", assignment["roles"])
        self.assertEqual(assignment["roles"]["advisor"]["optional_comparison"],
                         ["tam_dung", "on_dinh", "nang_cao"])
        self.assertNotIn("options", assignment["roles"]["advisor"])

        for rel in ("AGENTS.md", "docs/CRITERIA.md",
                    "harness/specs/APPROVAL.md", "SETUP.md"):
            value = (SOURCE / rel).read_text(encoding="utf-8")
            self.assertNotIn("\\n", value, rel)
            for label in ("Tạm dùng", "Ổn", "Nâng cao"):
                self.assertIn(label, value, rel)
            self.assertIn("when", value.lower(), rel)
        for rel in ("README.md", "docs/user-guide.en.md"):
            value = (ROOT / rel).read_text(encoding="utf-8")
            for label in ("CRITERIA", "Planner", "For AI"):
                self.assertIn(label, value, rel)
        self.assertFalse((ROOT / "README.en.md").exists())

    def test_planner_owns_intake_and_advisor_is_preapply_only(self):
        planner = (SOURCE / ".agents/roles/planner.md").read_text(encoding="utf-8")
        advisor = (SOURCE / ".agents/roles/advisor.md").read_text(encoding="utf-8")
        reviewer = (SOURCE / ".agents/roles/reviewer.md").read_text(encoding="utf-8")
        critic = (SOURCE / ".agents/roles/critic.md").read_text(encoding="utf-8")
        for phrase in ("Planner (not Advisor)", "personal-only", "commercial",
                       "lightweight pre-write advisor gate", "after seeing that advice",
                       "read-only proposed delta", "before the file write"):
            self.assertIn(phrase.lower(), planner.lower(), phrase)
        for phrase in ("entire proposed CRITERIA", "existing CRITERIA plus",
                       "pre-write checkpoint", "before any CRITERIA file write",
                       "not a review gate", "when feasibility or impact",
                       "do not read or review Plan", "no PASS/FAIL", "OPTIONAL"):
            self.assertIn(phrase.lower(), advisor.lower(), phrase)
        self.assertNotIn("ALWAYS present exactly three", advisor)
        self.assertIn("Human must decide after the advice", advisor)
        self.assertIn("no PASS/FAIL verdict", advisor)
        self.assertIn("OVERENGINEERING", reviewer)
        self.assertIn("UNDERSCOPING", reviewer)
        self.assertIn("approved CRITERIA", reviewer)
        self.assertIn("do not claim scope compliance", critic.lower())
        self.assertIn("No CRITERIA", critic)
        criteria = (SOURCE / "docs/CRITERIA.md").read_text(encoding="utf-8")
        for phrase in ("personal-only", "commercial", "proportional",
                       "complete coherent draft", "BEFORE modifying"):
            self.assertIn(phrase.lower(), criteria.lower(), phrase)
        approval = (SOURCE / "harness/specs/APPROVAL.md").read_text(encoding="utf-8")
        self.assertIn("whole draft", approval)
        self.assertIn("before any edit or merge", approval)
        self.assertIn("settle the exact theory delta", approval)

    def test_prewrite_advisor_decision_contract(self):
        planner = (SOURCE / ".agents/roles/planner.md").read_text(encoding="utf-8").lower()
        advisor = (SOURCE / ".agents/roles/advisor.md").read_text(encoding="utf-8").lower()
        criteria = (SOURCE / ".agents/skills/write-criteria/SKILL.md").read_text(encoding="utf-8").lower()
        for phrase in ("human's request to finalize/commit", "stop before the file write",
                       "after seeing that advice", "post-advice instruction"):
            self.assertIn(phrase, planner)
        self.assertIn("pre-write checkpoint", advisor)
        self.assertIn("human made a decision after the advice", criteria)
        self.assertIn("no approval, veto", planner)

    def test_role_adapter_instructions_match_generic_contract(self):
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        import yaml
        for role in ("planner", "advisor", "reviewer", "critic"):
            canonical = (SOURCE / ".agents/roles" / (role + ".md")).read_text(encoding="utf-8").strip()
            with (SOURCE / ".codex/agents" / (role + ".toml")).open("rb") as f:
                codex = tomllib.load(f)
            self.assertIn(canonical, codex["developer_instructions"])
            claude = (SOURCE / ".claude/agents" / (role + ".md")).read_text(encoding="utf-8")
            self.assertIn(canonical, claude)
            cont = yaml.safe_load((SOURCE / ".continue/agents" / role / "config.yaml").read_text(encoding="utf-8"))
            self.assertIn(canonical, cont["rules"][0])

    def test_installer_is_stable_after_python_cache_and_editor_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            dest = pathlib.Path(d)
            before, after, preview = dest / "before", dest / "after", dest / "preview"
            before.mkdir()
            after.mkdir()
            preview.mkdir()
            flags = ("--tier", "Standard", "--runtime", "codex")
            clean_preview = run(INSTALLER, "--target", preview, *flags)
            self.assertEqual(clean_preview.returncode, 0)
            first = run(INSTALLER, "--target", before, *flags, "--apply")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            probes = (
                SOURCE / "harness/common/__pycache__/__bootstrap_probe__.cpython-312.pyc",
                SOURCE / "harness/common/.pytest_cache/v/cache/__bootstrap_probe__.json",
                SOURCE / ".agents/skills/implement-task/__bootstrap_probe__.pyc",
                SOURCE / ".agents/skills/implement-task/__bootstrap_probe__.md~",
                SOURCE / ".codex/agents/__bootstrap_probe__.toml.bak",
                SOURCE / "docs/__bootstrap_probe__.swp",
            )
            created_dirs = []
            try:
                for probe in probes:
                    ancestor = probe.parent
                    missing_parents = []
                    while ancestor != SOURCE and not ancestor.exists():
                        missing_parents.append(ancestor)
                        ancestor = ancestor.parent
                    if missing_parents:
                        probe.parent.mkdir(parents=True)
                        created_dirs.extend(missing_parents)
                    self.assertFalse(probe.exists(), str(probe))
                    probe.write_bytes(b"not a release file")
                dirty_preview = run(INSTALLER, "--target", preview, *flags)
                self.assertEqual(dirty_preview.returncode, 0, dirty_preview.stdout + dirty_preview.stderr)
                self.assertEqual(clean_preview.stdout, dirty_preview.stdout)
                second = run(INSTALLER, "--target", after, *flags, "--apply")
                self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
                def installed(root):
                    return {str(p.relative_to(root)): p.read_bytes()
                            for p in root.rglob("*") if p.is_file()}
                self.assertEqual(installed(before), installed(after))
                self.assertFalse(any("__bootstrap_probe__" in p for p in installed(after)))
            finally:
                for probe in probes:
                    if probe.exists():
                        probe.unlink()
                for parent in sorted(set(created_dirs), key=lambda x: len(x.parts), reverse=True):
                    try:
                        parent.rmdir()
                    except OSError:
                        pass

    def test_codex_agent_sandbox_is_inherited_not_per_role(self):
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        for config in (SOURCE / ".codex/agents").glob("*.toml"):
            with config.open("rb") as f:
                agent = tomllib.load(f)
            self.assertNotIn("sandbox_mode", agent, config.name)
            self.assertNotIn("approval_policy", agent, config.name)
        policy = (SOURCE / "harness/specs/READINESS.md").read_text(encoding="utf-8")
        self.assertIn("inherit effective parent permission policy", policy)
        self.assertIn("GUIDED_ONLY", policy)

    def test_manual_coordination_is_not_authenticated_gate_approval(self):
        approval = (SOURCE / "harness/specs/APPROVAL.md").read_text(encoding="utf-8")
        maintenance = (SOURCE / "harness/specs/APPROVAL_MAINTENANCE.md").read_text(encoding="utf-8")
        for label in ("MANUAL_COORDINATION", "AUTHENTICATED_ADAPTER", "AWAITING_USER", "NOT_CONFIGURED", "G0/G11"):
            self.assertIn(label, approval)
            self.assertIn(label, maintenance)
        self.assertIn("specific, direct instruction", approval)
        self.assertIn("*not* independent identity authentication", approval)
        self.assertIn("not an authenticated gate answer", maintenance)
        self.assertIn("Precedence:", maintenance)

    def test_release_state_never_claims_full_harness(self):
        report = SOURCE / "harness/common/status.py"
        caps = json.loads((SOURCE / "harness/common/capabilities.json").read_text(encoding="utf-8"))
        self.assertEqual(caps["release_claim"], "INSTALLABLE_BASELINE_NOT_AUTOMATED_HARNESS")
        self.assertEqual(caps["capabilities"]["snapshot"], "SCRIPT_TESTED")
        self.assertEqual(caps["capabilities"]["codex_hook_bridge"], "SCRIPT_TESTED")
        self.assertEqual(caps["capabilities"]["native_hooks"], "READY_CONTENT")
        for missing in ("gate_engine", "trace", "orchestration", "authenticated_approval"):
            self.assertEqual(caps["capabilities"][missing], "NOT_CONFIGURED")
        for tier in TIERS:
            for runtime in RUNTIMES:
                result = run(report, "--tier", tier, "--runtime", runtime)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("NOT_CONFIGURED: not a fully operational automated harness", result.stdout)
                self.assertIn("REAL_HOST_SMOKE: UNVERIFIED", result.stdout)

    def test_manifest_and_native_configs(self):
        manifest = json.loads((SOURCE / "harness/specs/TIER_MANIFEST.json").read_text(encoding="utf-8"))
        for tier in TIERS:
            names = set()
            current = tier
            while current:
                entry = manifest["tiers"][current]
                names.update(entry["agents"])
                current = entry.get("inherits")
            self.assertEqual(names, EXPECTED[tier])
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        with (SOURCE / ".codex/config.toml").open("rb") as f:
            cfg = tomllib.load(f)
        self.assertNotIn("model", cfg)
        for p in (SOURCE / ".codex/agents").glob("*.toml"):
            with p.open("rb") as f:
                cfg = tomllib.load(f)
            self.assertTrue(cfg.get("model"))
            self.assertIn(cfg.get("model_reasoning_effort"), ("medium", "high"))
            self.assertNotIn("sandbox_mode", cfg, "custom subagent inherits parent sandbox")
        for p in (SOURCE / ".claude/agents").glob("*.md"):
            front = p.read_text(encoding="utf-8").split("---", 2)[1]
            self.assertIn("effort:", front)
            self.assertIn("model:", front)
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not available outside CI")
        configs = [SOURCE / ".continue/config.yaml"] + list(
            (SOURCE / ".continue/agents").glob("*/config.yaml"))
        for p in configs:
            parsed = yaml.safe_load(p.read_text(encoding="utf-8"))
            self.assertEqual(parsed["schema"], "v1", p)
            self.assertIsInstance(parsed["models"], list, p)
            if "/agents/" in p.as_posix():
                self.assertTrue(parsed["rules"], p)
                self.assertNotIn("\\n", parsed["rules"][0], p)

if __name__ == "__main__":
    unittest.main(verbosity=2)
