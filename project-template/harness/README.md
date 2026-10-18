# Harness — Google Antigravity IDE baseline (Python scripts + contracts)

**Primary runtime: Google Antigravity IDE.** Skills and roles are natively discovered from `.agents/skills/` and `.agents/roles/`. Antigravity lifecycle hooks are configured in `.agents/hooks.json`. Scripts in `harness/common/` are ordinary Python >=3.9 that run via `run_command` tool or terminal — not via Codex-specific hook bridges.

| Area | Actual executable | State |
|---|---|---|
| Inventory / configured checks | `common/inventory.py`, `common/verify.py` | SCRIPT_TESTED |
| Explicit file snapshot / guarded restore | `common/snapshot.py` | SCRIPT_TESTED; no pre-edit intercept coverage |
| Single-task link/evidence validation | `common/task.py` with `active-task.json` | SCRIPT_TESTED; not full trace or stale propagation |
| Stop verify hook (Antigravity) | `.agents/hooks.json` → `python harness/common/verify.py` | SCRIPT_TESTED; native Stop dispatch UNVERIFIED until smoke-tested |
| Codex hook bridge | `codex/hook.py` + `.codex/hooks.json` | SCRIPT_TESTED; runtime trust UNVERIFIED |
| Claude Code adapter | `claude/hook.py` + `.claude/settings.json` | SCRIPT_TESTED; runtime trust UNVERIFIED |
| Full gate engine, user-signed gate, journal | `specs/GATES.md`, `APPROVAL.md` | NOT_CONFIGURED |
| Auto Planner/Reviewer/Critic orchestration | `specs/REVIEW_LOOP.md` | NOT_CONFIGURED |
| Full trace generator/stale propagation | `specs/TRACE.md` | NOT_CONFIGURED |

Do not add a VM, server, background daemon or another framework. `specs/` defines what remains to be implemented for the approved tier, not automatic features simply because an instruction exists. Run `python harness/common/status.py` and record actual CLI smoke results before claiming RUNTIME_VERIFIED or ENFORCED.

### Active Git development branch
`harness/common/branch_authority.py` works across every tier and runtime as an explicit Git branch/merge/push **preflight**; `harness/specs/BRANCH_AUTHORITY.md` explains the authority model. This does not provide universal shell/MCP/remote Git enforcement.

