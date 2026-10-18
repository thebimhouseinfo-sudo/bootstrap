# Claude Code project instructions

Follow AGENTS.md for approved product scope, Planner/Advisor checkpoints and acceptance evidence. docs/CRITERIA.md is the theory authority. Native subagents are in .claude/agents/.

**Native Claude Code hooks are implemented** in `harness/claude/hook.py`, invoked from `.claude/settings.json`. The adapter reuses portable Python `harness/common/*.py` and translates Claude hook events (`UserPromptSubmit`, `PreToolUse`, `Stop`) to the same branch-authority, snapshot and verify primitives used by the Codex reference.

Hook event mapping vs Codex:
- `UserPromptSubmit` ← injects project context (analogous to Codex `SessionStart`)
- `PreToolUse` matcher `Edit|Write|Create|MultiEdit|str_replace_editor|Bash` ← branch check + snapshot (analogous to Codex `PreToolUse` on `apply_patch`)
- `Stop` ← task trace + verify (analogous to Codex `Stop`)

The adapter reads `hook_event_name` and tool data from Claude's JSON stdin. `CLAUDE_HOOK_EVENT` is an optional override for custom wrappers, not a required native variable. Exit 2 blocks supported events; stderr text is returned to Claude. PreToolUse guidance uses native `hookSpecificOutput.additionalContext` JSON.

**Verified capability:** installed Python adapter regression tests. **UNVERIFIED:** actual Claude Code host loading, event dispatch, exit-code semantics and permission enforcement must be confirmed on the installed Claude Code version before claiming ENFORCED. Branch coverage for Bash tool is best-effort only (no universal shell-write protection). Preserve real smoke evidence with project/client/version and exact source hashes; editing a capability label alone is not runtime evidence.

**Setup steps for Claude Code:**
1. Install template: `python install.py --target PATH --tier Standard --runtime claude --apply`
2. Configure branch authority (Git projects): `python harness/common/branch_authority.py configure --active BRANCH --freeze main --apply`
3. Fill `harness/common/checks.json` with actual project build/test commands.
4. Open project in Claude Code; verify hooks fire by checking session context message.
5. Run `python harness/common/status.py --tier Standard --runtime claude`. Expect NOT_CONFIGURED while Standard approval/gate/trace/orchestration engines are absent; a successful install cannot clear these blockers.
