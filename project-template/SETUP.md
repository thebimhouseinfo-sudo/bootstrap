# Bootstrap project setup — reuse first

AI installs from repo root using `python install.py --target PATH --tier Standard --runtime codex --apply` **after preview and user approval**. This copies only missing files; it does not overwrite existing work. A conflicting `AGENTS.md` produces `AGENTS.bootstrap.md` for manual reconciliation, and exit 2 means unresolved conflict.

- **READY / copy as-is:** generic agents, skill procedures, native Codex/Claude role and Claude skill configurations, shared contracts, Codex baseline scripts.
- **CONFIGURE only for actual project facts:** CRITERIA, profile, approved plan/tasks, verified build/check commands in `harness/common/checks.json`, optional skill/knowledge. Never invent facts.
- **If user plan/model access differs:** Codex `.codex/MODEL_SELECTION.md`; Claude `.claude/MODEL_SELECTION.md`; Continue `.continue/README.md` (provider-dependent setup). **Main chat model is always user-selected**. Do not rewrite generic roles or consult these model guides when presets work.
- **Runtime capability limits:** native hooks, authenticated approval, snapshot/restore, gates, trace and orchestration are specified under `harness/specs/` but are NOT_CONFIGURED unless actually installed and tested. `harness/common/inventory.py --tier TIER --runtime RUNTIME` checks inventory only; `harness/common/verify.py` checks configured commands, not real-host acceptance.
- **Advisor on theory decisions only:** invoke for initial criteria approval or proposed change to approved criteria; expose minimum solution, complexity and downstream impact before asking human. Human may override.\n- **Discovery:** empty project starts with Planner brainstorm/research and OPEN entries in CRITERIA, not invented development tasks. Approved theory stays in CRITERIA only.
- **Runtime switch:** install just one selected adapter. Continue workspace rules are not isolated named subagents.

Only open detailed `harness/specs/` contracts for mechanisms being implemented. Keep setup bounded and report tested vs unverified honestly.
