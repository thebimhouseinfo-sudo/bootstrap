# Bootstrap project setup — reuse first

AI installs from repo root using `python install.py --target PATH --tier Standard --runtime codex --apply` **after preview and user approval**. This copies only missing files; it does not overwrite existing work. A conflicting `AGENTS.md` produces `AGENTS.bootstrap.md` for manual reconciliation, and exit 2 means unresolved conflict.

- **READY / copy as-is:** generic agents, skill procedures, native Codex/Claude role and Claude skill configurations, shared contracts, Codex baseline scripts.
- **CONFIGURE only for actual project facts:** CRITERIA, profile, approved plan/tasks, verified build/check commands in `harness/common/checks.json`, optional skill/knowledge. Never invent facts.
- **If user plan/model access differs:** Codex `.codex/MODEL_SELECTION.md`; Claude `.claude/MODEL_SELECTION.md`; Continue `.continue/README.md` (provider-dependent setup). **Main chat model is always user-selected**. Do not rewrite generic roles or consult these model guides when presets work.
- **Runtime capability limits:** native hooks, authenticated approval, snapshot/restore, gates, trace and orchestration are specified under `harness/specs/` but are NOT_CONFIGURED unless actually installed and tested. `harness/common/inventory.py --tier TIER --runtime RUNTIME` checks inventory only; `harness/common/verify.py` checks configured commands, not real-host acceptance.
- **Planner first:** clarify whether personal/internal/commercial/market, current and committed scale, actual data/trust risk, needed safeguards, observable result and non-goals; write these to the **initial CRITERIA draft**. For approved theory changes, discuss and settle delta with human **without editing CRITERIA**.
- **Advisor at approval gates only:** review the **full initial draft** before first approval; or **approved CRITERIA plus settled amendment** only after human asks to apply and **before editing** it. Compare Tạm dùng / Ổn / Nâng cao and impact; human chooses. Then Planner writes only authorized scope. No continuous Advisor, no assumption advanced is better.
- **Vibe coder decision:** show result / intentionally omitted scope / burden and risks / choice; do not require reading diffs or P1/P2/P3 technical plans.
- **Discovery:** empty project starts with Planner brainstorm/research and OPEN entries in CRITERIA, not invented development tasks. Approved theory stays in CRITERIA only.
- **Runtime switch:** install just one selected adapter. Continue workspace rules are not isolated named subagents.

Only open detailed `harness/specs/` contracts for mechanisms being implemented. Keep setup bounded and report tested vs unverified honestly.

## Actual release capabilities
Copy/install success is NOT a fully working harness. Use `python harness/common/status.py --tier Standard --runtime codex` (or chosen tier/runtime); exit 2 means required mechanisms remain NOT_CONFIGURED or real-host smoke UNVERIFIED. Now shipped and script-tested for Codex: project-local native hook JSON/Python adapter, scoped explicit hash snapshot/restore, single-task trace-link validator and bounded Stop verification, in addition to installer/roles/verify/preflight. Still NOT_CONFIGURED: authenticated approval/gate signing, full trace/STale propagation and automatic reviewer orchestration; native Codex hook trust/smoke must be verified on the user's version. `harness/common/capabilities.json` is the definitive list. Codex Advisor/Critic/Explorer are prompt-level read-only only; inherit the parent sandbox.

## Codex-first setup and migration
For Codex, copy the supplied `.codex/hooks.json` and Python scripts through the installer; start Codex in the project, inspect `/hooks` and trust the exact definitions if approved. Configure actual project commands in `harness/common/checks.json` and an explicitly approved `harness/active-task.json`; no fabricated goal ID. Snapshot/restore supports only explicit regular files. Stop checks activate for configured tasks only.

Claude and other clients use the Codex implementation as a behavior reference: reuse Python `harness/common/*.py` where compatible; write a native adapter after confirming that client's actual events, JSON payload, permissions and stop semantics. A copied Codex hook JSON does not work automatically in Claude/Continue. Unsupported events must be reported GUIDED_ONLY, not passed as enforced. Do not build a VM/daemon merely for compatibility.
