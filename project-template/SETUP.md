# SETUP — Instructions for Bootstrap and Planner

This folder is the **actual target project root**. Copy its contents to the project root (preserve tree; do not create an extra nested project-template directory). Never blindly overwrite existing project files: inspect, merge and get authorization for protected changes.

READY-TO-USE CONTENT: portable role prompts in .agents/roles, common .agents/skills/*/SKILL.md, report/lesson formats, .gitignore starter. These are immediately readable instructions/formats, though runtime activation still requires configuration.

NEEDS PROJECT WRITING: root AGENTS.md and README.md; docs/CRITERIA.md, ARCHITECTURE.md, PROJECT_PROFILE.md, MILESTONES.md, TASKS.md, and derived trace. **Planner rewrites AGENTS.md and project-specific planning after inspecting actual goals and repo**. Bootstrap handles verified environment/profile/harness scaffolding; Planner cannot invent product logic or bypass approval.

IMPLEMENT AFTER RUNTIME DISCOVERY: harness/specs/ documents are implementation guides for hooks, gates, review loop, snapshot, verify, approvals, trace, etc. Choose scripts, native configuration and policies for the actual platform, OS, host and agent runtime. Do not ship dummy executable scripts.

Coder & Tester default to generic operation. Optional project skills/knowledge from .agents/config/worker-context.yaml can improve first-pass accuracy; absence should lead to normal testing/debugging, not an automatic task failure.

Before claiming READY, test native agent/skill activation and relevant harness allow/deny scenarios. Mark NOT_CONFIGURED or GUIDED_ONLY honestly.

## Empty project — Discovery Mode
When no product theory exists, do not stop Planner. Install only the minimal Planner agent with brainstorm-theory and research-evidence skills, the CRITERIA placeholder and an available user dialogue/approval channel. Planner explores options and research with the user, recording OPEN hypotheses only in CRITERIA. Full harness setup, final stack selection, production milestones and coder tasks follow sufficient approved theory. Do not falsely claim approval mechanisms or native agents work before tested.

## Contract adoption from Claude's reorganized ZIP
The canonical destination is this already-laid-out project tree, not the ZIP's categorized `templates/` folder. Read `harness/specs/GATES.md`, `TESTS.md`, `APPROVAL.md`, `FIXER.md` and `HARNESS_SPEC_TEMPLATE.md` for the more detailed platform-neutral contracts before implementing. These files are specifications: implement only the approved tier for the verified runtime/host, then execute permitted and denied self-tests. Discovery Mode remains supported for projects without approved logic; it does not pretend that a full harness exists.
