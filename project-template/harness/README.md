# Harness — Codex-first Python baseline and remaining contracts

**Reference runtime: Codex.** Copy-ready native `.codex/hooks.json` delegates SessionStart, observed `apply_patch` PreToolUse and Stop to `harness/codex/hook.py`. Scripts in `harness/common/` are ordinary Python >=3.9 and may be reused by Claude/other IDE adapters, but each host's event/payload/trust semantics must be verified independently.

| Area | Actual executable | State |
|---|---|---|
| Inventory / configured checks | `common/inventory.py`, `common/verify.py` | SCRIPT_TESTED |
| Explicit file snapshot / guarded restore | `common/snapshot.py` | SCRIPT_TESTED; no Bash/MCP pre-edit coverage |
| Single-task link/evidence validation | `common/task.py` with `active-task.json` | SCRIPT_TESTED; not full trace or stale propagation |
| Codex hook bridge | `codex/hook.py` + `.codex/hooks.json` | SCRIPT_TESTED, runtime trust UNVERIFIED |
| Stop bounded retry | `codex/hook.py` | SCRIPT_TESTED; only for ACTIVE task with configured checks |
| Full gate engine, user-signed gate, journal | `specs/GATES.md`, `APPROVAL.md` | NOT_CONFIGURED |
| Auto Planner/Reviewer/Critic orchestration | `specs/REVIEW_LOOP.md` | NOT_CONFIGURED |
| Full trace generator/stale propagation | `specs/TRACE.md` | NOT_CONFIGURED |

Do not add a VM, server, background daemon or another framework. `specs/` defines what remains to be implemented for the approved tier, not automatic features simply because an instruction exists. The Python hook cannot substitute for real host trust/sandbox/user authentication. Run `python harness/common/status.py` and record actual CLI smoke results before claiming RUNTIME_VERIFIED or ENFORCED.
