# Claude Code — native adapter for the Python harness

The main chat model/effort and effective sandbox/approval are chosen by the user/host. `.claude/agents/*.md` already contains role presets; no independent sandbox is promised for Advisor/Critic/Explorer.

**Executable project-local native hooks:** `.claude/settings.json` → `harness/claude/hook.py`. The adapter discovers the project root at `parents[2]` relative to this file. Python 3.9+ must be available as `python` on PATH. The `CLAUDE_HOOK_EVENT` env var must be set by Claude Code when invoking each hook; JSON payload arrives on stdin.

- `UserPromptSubmit` (all tools) — injects short project context on each prompt.
- `PreToolUse` (matcher `Edit|Write|Create|MultiEdit|str_replace_editor|Bash`) — checks Git branch authority for write tools; snapshots recognized file paths when policy enables it; warns on protected paths. Bash coverage is best-effort; no universal shell-write protection.
- `Stop` (all) — validates `harness/active-task.json` trace and runs `harness/common/checks.json`; blocks with exit 2 and requests one repair turn if checks fail. `stop_hook_active` prevents looping.

**Differences from Codex adapter:**
- Tool identification uses Claude tool names (`Edit`, `Write`, `Bash`, etc.) not `apply_patch`.
- Blocking uses exit code 2 + stderr (not `permissionDecision: deny` JSON).
- `UserPromptSubmit` replaces `SessionStart` for context injection.
- No `commandWindows` field needed; command string is used directly.

**Setup:** install with `python install.py --runtime claude --apply`, open project in Claude Code, verify hook fires (context message on first prompt), then smoke-test block and stop behaviors. Record results; do not claim RUNTIME_VERIFIED without observation.

Run `python harness/common/status.py --tier Standard --runtime claude` and `python harness/claude/preflight.py` to check file presence and policy. Update `harness/common/capabilities.json` → `runtime_smoke.claude` to `RUNTIME_VERIFIED` after confirmed smoke test.
