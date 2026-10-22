# Continue integration: complete project configuration with CLI hook support

The Bootstrap `--runtime continue` package now ships **Continue-native role configurations, rules, skills source, and CLI hooks**. The active host determines which guarantees apply. Read `HOOKS_SETUP.md` before declaring native enforcement.

`cn` **CLI in interactive TUI mode**: project-local `.continue/settings.json` registers Claude-compatible CLI events `PreToolUse`, `SessionStart`, `SubagentStop`, `UserPromptSubmit`, `Stop`. Native scripts in `.continue/hooks/` inspect actual CLI stdin event JSON and block recognized direct Criteria edits prior to any modification. A one-shot apply requires a real Advisor stop event and a later Human confirmation. Subagent orchestration is **not** automatically provided; where real events are unavailable the unlock correctly remains blocked.

**Continue extension in VS Code/JetBrains:** `.continue/rules/` works as project instructions and model/agent configs can be selected, but there is **no verified IDE-native interception** of its built-in editor write tools. The CLI hooks in `.continue/settings.json` must not be described as IDE hooks. Configure tool policies in the extension and verify the actual behavior; any protected write remains `GUIDED_ONLY` without live evidence.

Continue has separate role configs `.continue/agents/<role>/config.yaml` with the canonical full role text. Select the intended role config explicitly (or use `cn --config` for CLI) and configure a real user/provider model. `models: []` is intentionally an **unconfigured placeholder**, not a runnable or automatically selected model. Do not activate all role configs simultaneously; they aren't independent subagents just because their YAML files exist. Roles come from `.agents/roles/` and tier-filtered skills are **copied into `.continue/skills/<skill>/SKILL.md`** for the CLI's native Skills tool; where supported, Continue may use `.continue/rules/` in Chat/Agent/Edit mode. The mandatory `01-criteria-gate.md` is always included.

**Human/Advisor criteria checkpoint:**

- Greenfield: Planner shows the complete draft in chat, Human asks to save, Advisor advises, Human decides after the advice, then one-time apply of the exact result.
- Brownfield: Planner and Human settle the exact delta in chat, Human asks to update, Advisor advises on that delta, Human decides after the advice, then the same one-time apply.
- No Advisor in routine brainstorming. If the host cannot independently run and record Advisor, do not forge a receipt or bypass a protected write.

Native smoke checklist and host limitations: `HOOKS_SETUP.md`. Native scripts here are not Codex hooks, Copilot hooks, or Claude hooks; there is **no global hook schema** shared by those hosts. Avoid claiming authenticated Human approval, universal shell/MCP interception or automatic host permissions from these script fixtures.
