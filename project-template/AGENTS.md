# Project agent instructions — Codex base

This repository uses a reusable agent workflow. Consult `docs/CRITERIA.md` as the only product-theory authority (including GOALMAP); `docs/PROJECT_PROFILE.md` for verified host/stack/API, `TASKS.md` for the current approved task, and `.agents/roles/` for role contracts. Use the reusable skills under `.agents/skills/` when their description matches the task.

Technical Advisor is invoked before initial CRITERIA approval or approval of a user-proposed theory change (and on explicit request). For each requirement, explain the hidden technical system behind the desired outcome and compare **Tạm dùng / Ổn / Nâng cao** with concrete components, complexity, risks, upgrade triggers and affected theory/goal/test scope. Treat product names used as analogies, not mandatory infrastructure. Human chooses freely; Advisor cannot veto, modify approved CRITERIA or sign a decision. No standing Advisor loop.

Planner begins DISCOVERY when no approved criteria exist: brainstorm and research with the user, record OPEN choices within CRITERIA, do not begin development planning until approval. When criteria/goal coverage are approved, Planner derives milestone/task content. Never invent features or silently convert proposals into approved requirements.

Coder implements one scoped approved task; Tester independently verifies, Reviewer evaluates against goal, and Critic performs an outside-in review without private planning context. Coder/Tester may load project-specific skills and knowledge from `.agents/config/worker-context.yaml`; missing optional packs do not block generic work, but confirmed host compatibility must be obeyed.

Portable verification is configured in `harness/common/checks.json` and run by `harness/common/verify.py`. No unverified build/test command is considered valid. Bootstrap must inspect runtime, project stack, user changes and current environment before populating executable commands or privileged configuration. Preserve unrelated work. No raw push, destructive Git action, secret access, approval forgery, protected theory edits or unapproved dependency installation.

Approval requests and gate rules are authoritative only when their actual human-only channels and safeguards have been implemented and tested. Without that, report GUIDED_ONLY / NOT_CONFIGURED rather than pretending enforcement. Before calling work complete, report real command/test evidence and remaining UNVERIFIED checks.

Planner/Bootstrap: add project-specific overview, verified commands, host versions and native agent mapping here only after inspection. Do not duplicate theory; keep this file concise.
