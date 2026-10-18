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
Copy/install success is NOT a fully working harness. Use `python harness/common/status.py --tier Standard --runtime codex` (or chosen tier/runtime); exit 2 means required mechanisms remain NOT_CONFIGURED or real-host smoke UNVERIFIED. Currently supported: copy-safe installer, role files, shared inventory/verify, Codex preflight. Not shipped as active engines: snapshot, hooks, gate, journal/authenticated approval, trace, orchestration. `harness/common/capabilities.json` is the definitive list. Codex Advisor/Critic/Explorer are prompt-level read-only only; inherit the parent sandbox.
