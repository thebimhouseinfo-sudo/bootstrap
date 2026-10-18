# Claude Code: optional model adjustment

Presets already set in native `.claude/agents/*.md`: **Opus** for Planner, Critic and Harness Fixer; **Fable** for Reviewer; **Sonnet** for Coder and Tester; **Haiku** for Explorer. These four aliases are supported by Claude Code, though access depends on account/plan. The main conversation model and effort remain user-selected.

Only if a preset is unavailable or the user requests a different quality/quota tradeoff: verify available models; ask the user; edit `model:` on the affected role only; verify actual subagent invocation. Do not silently substitute or rewrite generic role instructions. Per-agent effort is optional and should only be set if supported by the installed runtime.
