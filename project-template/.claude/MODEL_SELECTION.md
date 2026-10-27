# Claude Code: optional model adjustment

Presets already set in native `.claude/agents/*.md` use only models included in a standard Claude Pro/Max subscription: **Opus** for Planner, Advisor, Reviewer, Critic and Harness Fixer; **Sonnet** for Coder and Tester; **Haiku** for Explorer. Model picker verified 2026-10-27 on a Claude Pro account: Opus 5.5, Sonnet 5.5 and Haiku 5.5 are included; **Fable 5.1 shows "Requires usage credits"**, so no preset depends on it (a `fable` subagent fails or spends credits when extra usage is off). The main conversation model and effort remain user-selected.

Optional upgrades/downgrades (user decision only): with usage credits enabled, Reviewer or Critic may be set to `fable`; on tight Pro limits, Reviewer may be set to `sonnet` because Critic remains the final technical review.

Only if a preset is unavailable or the user requests a different quality/quota tradeoff: verify available models; ask the user; edit `model:` on the affected role only; verify actual subagent invocation. Do not silently substitute or rewrite generic role instructions. Subagent effort defaults: high for Planner/Advisor/Reviewer/Critic/Fixer, medium for Coder/Tester, low for Explorer. Validate support for the installed version/model before using or adapting.

The native Claude Code hook adapter is implemented in `harness/claude/hook.py`. `.claude/settings.json` contains `UserPromptSubmit`, `PreToolUse` and `Stop` hooks. Verify actual hook dispatch, exit-code blocking and Stop behavior on the installed Claude Code version before marking RUNTIME_VERIFIED. Do not call it Claude-ready on file presence alone; a real smoke test is required.
