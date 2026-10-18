# Readiness — Codex reference implementation

The authoritative machine-readable inventory is `harness/common/capabilities.json`; tier requirements are in `harness/specs/TIER_MANIFEST.json`.

**Implemented and Python CI-tested**: safe installer, role files, `common/verify.py` and `inventory.py`, scoped hash-checked `common/snapshot.py`, scoped one-task `common/task.py`, and Codex `SessionStart` / `PreToolUse` / `Stop` hook handler (including bounded single continuation). The `.codex/hooks.json` file is ready to request native registration; **actual host loading, hook trust, event semantics and active model remain UNVERIFIED until a real Codex smoke test**.

**Not fully implemented**: authenticated human-only approvals, secure journal/ledger, signed gate engine, full trace and STALE propagation, milestone management, autonomous review orchestration, Full-tier Git admin / repair. Therefore no Standard/Full tier may claim a complete autonomous harness. Lite includes actual explicit snapshot support, but also requires real-host verification before READY.

Run `python harness/common/status.py --tier Standard --runtime codex`. Exit 2 means missing tier capability or host smoke. For Claude and other IDEs, Python can be reused, but native hook adapters are not implied by Codex hooks.

Labels:
- READY_CONTENT = files/presets exist; no proof loaded.
- SCRIPT_TESTED = Python logic exercised on named CI OS/Python versions.
- RUNTIME_VERIFIED = host actually loaded/dispatched hooks and agents with observed trust and permissions.
- ENFORCED = actual negative tests prove bypass impossible for that declared boundary.
- GUIDED_ONLY = prompts/coordinated process with no technical guard.
- NOT_CONFIGURED = engine, task or required capability absent.
- UNVERIFIED = actual host behavior not tested.

Codex subagents inherit effective parent permission policy; a "read-only" instruction is not an isolated security boundary. A manual chat instruction authorizes bounded coordination through host controls only, not an authenticated gate signature. See `APPROVAL.md` and `APPROVAL_MAINTENANCE.md`.
