# Archive — historical design records

These files are **historical records**, not current instructions. Agents installing or operating Bootstrap follow [`../FOR_AI.md`](../FOR_AI.md) and the installed `project-template/` contracts; do not load this folder as context unless a task explicitly asks for design history.

| Path | What it records | Status when archived (2026-10-27) |
|---|---|---|
| `refactor/CONTEXT_OPTIMIZATION_REFACTOR_PLAN_DRAFT.md` | v7 upgrade plan (P0–P2, B1–B5) | P0/P1 merged (PR #21, #22); kept for decision history |
| `refactor/FUNCTIONAL_DOGFOOD_LESSONS.md` | Lessons from functional dogfooding (v7) | Reference |
| `refactor/B1_INSTALLER_HOST_FIT_PROPOSAL.md` | Installer host-fit design | Pre-code design candidate (per its own status line) |
| `refactor/B2_PROFILE_INSTALLATION_PROPOSAL.md` | Profile installation design | Pre-code design candidate (per its own status line) |
| `refactor/B3_WORKER_DELEGATION_PROPOSAL.md` | Worker delegation design | Implemented (PR #26) |
| `refactor/B4_LOCAL_MODEL_BENCHMARK_PROTOCOL.md` | Optional local-model benchmark protocol | Protocol only (PR #27) |
| `refactor/B5_HOST_INTEGRATION_REGRESSION.md` | Host regression matrix | Script-tested; real-host acceptance pending (PR #28) |
| `superpowers/specs/2026-10-18-codex-ready-design.md` | Codex-ready design (2026-10-18) | Reference; current Codex adapter lives in `project-template/harness/codex/` |
| `reports/2026-10-18-setup-smoke.md` | Original installed-app smoke evidence | Cited by `project-template/harness/specs/READINESS.md` |

To revive a design candidate (B1, B2), copy the relevant part into a new proposal rather than editing the archived file.
