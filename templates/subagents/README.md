# Portable subagents

Planner, Reviewer and Critic (CR) maintain project-independent role contracts; avoid per-project rewrites. Coder and Tester have fully usable generic defaults and may enrich themselves with project-specific skill **and knowledge** packs. Explorer and harness-fixer are optional.

Bootstrap verifies target runtime format/version then creates real subagent definitions, permissions, skill paths and model assignments; a copied markdown file alone does not activate an agent.

For **both Coder and Tester**, reload relevant optional context at session start, task start and verified project profile changes. Use `config/worker-context.example.yaml` as a project-local data model and `skills/context-reload/SKILL.md` as procedural guidance; real invocation/reload hooks need runtime adaptation and tests. Keep Tester independent.

Positive/negative simulations: generic coder/tester complete toy tasks with no custom packs; when valid project knowledge is added, both consume it; wrong-host packs are excluded; missing packs do not fail the task solely for absence; protected constraints and approval checks still block correctly. Label technical enforcement honestly.
