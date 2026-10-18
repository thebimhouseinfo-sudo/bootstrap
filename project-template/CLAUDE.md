# Claude Code project instructions

Follow AGENTS.md for approved product scope, Planner/Advisor checkpoints and acceptance evidence. docs/CRITERIA.md is the theory authority. Native subagents are in .claude/agents/.

**Native Claude Code hooks are implemented** in `harness/claude/hook.py`, invoked from `.claude/settings.json`. The adapter reuses portable Python `harness/common/*.py` and translates Claude hook events (`UserPromptSubmit`, `PreToolUse`, `Stop`) to the same branch-authority, snapshot and verify primitives used by the Codex reference.

Hook event mapping vs Codex:
- `UserPromptSubmit` ← injects project context (analogous to Codex `SessionStart`)
- `PreToolUse` matcher `Edit|Write|Create|MultiEdit|str_replace_editor|Bash` ← branch check + snapshot (analogous to Codex `PreToolUse` on `apply_patch`)
- `Stop` ← task trace + verify (analogous to Codex `Stop`)

The adapter passes `CLAUDE_HOOK_EVENT` env var and JSON stdin from Claude. Exit 2 blocks the operation; stderr text is returned to Claude as context.

**Verified capability:** hook files exist and Python logic is portable. **UNVERIFIED:** actual Claude Code host loading, event dispatch, exit-code semantics and permission enforcement must be confirmed on the installed Claude Code version before claiming ENFORCED. Branch coverage for Bash tool is best-effort only (no universal shell-write protection). Update `harness/common/capabilities.json` → `"claude"` entry to `RUNTIME_VERIFIED` after a real smoke test.

**Setup steps for Claude Code:**
1. Install template: `python install.py --target PATH --tier Standard --runtime claude --apply`
2. Configure branch authority (Git projects): `python harness/common/branch_authority.py configure --active BRANCH --freeze main --apply`
3. Fill `harness/common/checks.json` with actual project build/test commands.
4. Open project in Claude Code; verify hooks fire by checking session context message.
5. Run `python harness/common/status.py --tier Standard --runtime claude` and confirm no NOT_CONFIGURED blockers.
