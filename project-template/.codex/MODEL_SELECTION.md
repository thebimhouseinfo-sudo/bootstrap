# Codex — change subagent model only when necessary

**Defaults already configured in `.codex/agents/*.toml`:** Planner/Reviewer: `gpt-6.1-sol` high; Coder/Tester: `gpt-6.1-sol` medium; Critic/Harness Fixer: `gpt-6-astra` medium; Explorer: `gpt-6-luna` high. Concurrent subagents: 2. **Chat agent model/effort is user-selected and not pinned.**

If user plan lacks a preset, or user requests different speed/quality/quota: (1) verify available model IDs and effort in the active Codex account/version, only for active roles; (2) show the affected roles and trade-offs, obtain user choice, never silent fallback; (3) edit only `model` and `model_reasoning_effort` for those `.codex/agents/<role>.toml`; (4) parse TOML and smoke-test actual agent invocation. Do not edit chat model, approval policy, permissions or generic instructions. Unavailable/untested → UNAVAILABLE/UNVERIFIED.

Model preset is not evidence of availability, sandbox enforcement or Critic context isolation. Effective parent permissions and runtime trust must be checked. Tera ID is not pinned without verification.
