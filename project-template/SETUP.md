# SETUP — Instructions for Bootstrap and Planner

This folder is the **actual target project root**. Copy its contents to the project root (preserve tree; do not create an extra nested project-template directory). Never blindly overwrite existing project files: inspect, merge and get authorization for protected changes.

READY-TO-USE CONTENT: portable role prompts in .agents/roles, common .agents/skills/*/SKILL.md, report/lesson formats, .gitignore starter. These are immediately readable instructions/formats, though runtime activation still requires configuration.

NEEDS PROJECT WRITING: root AGENTS.md and README.md; docs/CRITERIA.md, ARCHITECTURE.md, PROJECT_PROFILE.md, MILESTONES.md, TASKS.md, and derived trace. **Planner rewrites AGENTS.md and project-specific planning after inspecting actual goals and repo**. Bootstrap handles verified environment/profile/harness scaffolding; Planner cannot invent product logic or bypass approval.

IMPLEMENT AFTER RUNTIME DISCOVERY: harness/specs/ documents are implementation guides for hooks, gates, review loop, snapshot, verify, approvals, trace, etc. Choose scripts, native configuration and policies for the actual platform, OS, host and agent runtime. Do not ship dummy executable scripts.

Coder & Tester default to generic operation. Optional project skills/knowledge from .agents/config/worker-context.yaml can improve first-pass accuracy; absence should lead to normal testing/debugging, not an automatic task failure.

Before claiming READY, test native agent/skill activation and relevant harness allow/deny scenarios. Mark NOT_CONFIGURED or GUIDED_ONLY honestly.
