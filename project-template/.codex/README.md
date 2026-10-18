# Codex role configuration

The main chat model and reasoning are chosen by the user; .codex/config.toml does not override them.

Subagent model presets are set in .codex/agents/*.toml: Planner/Reviewer Sol high, Coder/Tester Sol medium, Critic/Harness Fixer Astra medium, Explorer Luna high.

If a preset is unavailable for the user's subscription or needs adjusting for speed, quality or quota, follow MODEL_SELECTION.md: inspect actual model availability, ask the user, update only affected subagents, then test. No silent fallback.

Do not confuse prompts or native TOML with tested sandbox/context isolation. Hooks, approval gates, trace and orchestration remain NOT_CONFIGURED until independently implemented and tested.
