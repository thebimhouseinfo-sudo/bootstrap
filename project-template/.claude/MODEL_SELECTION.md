# Claude Code subagent models

The main chat model and reasoning effort are chosen by the user and are not overridden by project settings.

Preset native agent models: Opus for Planner/Reviewer/Critic/Harness Fixer, Sonnet for Coder/Tester, Haiku for Explorer. Read only active tier roles.

1. Check model aliases, supported effort controls and account availability for the installed Claude Code release.
2. If any preset is unavailable or user needs a different quota/quality/latency balance, propose exact alternatives and obtain a user decision. Never silently fallback.
3. Change only `model:` frontmatter in the affected `.claude/agents/<role>.md`; add any effort setting only after verifying version-specific support. Do not modify main-chat model or effort in `.claude/settings.json`.
4. Verify agent discovery and an actual safe invocation. Report UNAVAILABLE/UNVERIFIED separately from role instruction validity.
5. Preserve all generic role instructions; adjust only adapter/configuration for runtime differences.
