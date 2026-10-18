# Codex — reference adapter for the Python harness

The main chat model/effort and effective sandbox/approval are chosen by the user/host. `.codex/agents/*.toml` already contains role presets; no independent sandbox is promised for Advisor/Critic/Explorer.

**Executable project-local native hooks:** `.codex/hooks.json` → `harness/codex/hook.py`. The hooks discover the project root even when Codex starts in a subfolder; Python 3.9+ must be available as `python` on PATH. Project hooks and each changed definition need the user's review/trust in Codex `/hooks`. Do NOT bypass hook trust automatically.

- `SessionStart` supplies short project instructions.
- `PreToolUse` validates recognized direct `apply_patch` Add/Update/Delete and Move-to paths, snapshotting existing source/destination files. No all-shell/MCP prevention.
- `Stop` checks `harness/active-task.json` and `harness/common/checks.json`; if ACTIVE and tests fail, asks Codex for one bounded repair turn. No goal or no checks → does not fake PASS. It does not sign user gates or automatically call reviewers.

Run `python harness/common/snapshot.py capture <relative-file>`, `python harness/common/task.py --stage delivery`, and `python harness/common/status.py --tier Standard --runtime codex`. Snapshot restore is preview-only until `--apply --expect-current path=sha256` is supplied.

Python CI regression verifies the adapter contract, not that a signed-in Codex CLI has trusted and actually executed the native events; record real CLI smoke separately. Authenticated approvals, full gate engine, full STALE trace, review orchestration remain NOT_CONFIGURED.
