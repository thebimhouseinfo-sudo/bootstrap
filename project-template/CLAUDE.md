# Claude Code project instructions

Follow AGENTS.md for approved product scope, Planner/Advisor checkpoints and acceptance evidence. docs/CRITERIA.md is the theory authority. Native agents are in .claude/agents/.

The implemented lifecycle reference is **Codex-first**: `.codex/hooks.json` and `harness/codex/hook.py` invoke portable Python `harness/common/*.py`. Claude does NOT load Codex hooks. When converting, preserve behavior by translating native Claude hook events/schema/trust to the installed Python primitives, testing allow/fail/stop effects on the actual Claude Code version. Do not deploy a VM or background service merely for portability.

Until the native Claude adapter is actually implemented and verified, report NOT_CONFIGURED/GUIDED_ONLY. Codex Python fixture tests are not Claude Code host tests.
