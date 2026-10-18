# Release capability and readiness (authoritative status)

The current **release kind** is `BASELINE_AGENT_TEMPLATE_AND_SCRIPTS`. Its single machine-readable capability inventory is `harness/common/capabilities.json`; `harness/specs/TIER_MANIFEST.json` remains authoritative for which capabilities each tier *requires*, not which capabilities are implemented.

The installer, portable verifier/inventory, Codex preflight and generic role/model configuration are packaged. They are **not** native hook installation, gate engine, journal, authenticated approval, snapshot, trace or orchestration. These advanced contracts are written in `harness/specs/` but **not installed as working mechanisms**. No tier is certified as an autonomous harness today because even Lite's snapshot requirement is not implemented.

Run `python harness/common/status.py --tier Standard --runtime codex` (or choose Lite/Full and Claude/Continue). Exit **2** means mandatory tier capabilities or real-host smoke tests remain `NOT_CONFIGURED` / `UNVERIFIED`; do not report READY just because `install.py --apply` copied files successfully. Script testing is separate from actual tool availability, approval/trust mode and subagent discovery.

Definitions:
- `READY_CONTENT`: copyable instruction/configuration files; no proof runtime loaded them.
- `SCRIPT_TESTED`: supporting Python script behavior checked by regression on the named CI platforms.
- `RUNTIME_VERIFIED`: recorded real target CLI/version/OS sandbox and effective permissions smoke test.
- `ENFORCED`: negative tests prove required safeguards cannot be bypassed and real user-only authorizations work.
- `GUIDED_ONLY`: model follows instructions without technical prevention.
- `NOT_CONFIGURED`: feature missing or no valid runtime binding; no PASS allowed.
- `UNVERIFIED`: actual host/scope not tested.

All Codex subagents inherit the parent sandbox and approval settings. A role instruction "read-only" is **GUIDED_ONLY**, not a separate sandbox. Verify model availability and permissions in the signed-in session, and do not infer them from TOML syntax. See https://learn.chatgpt.com/docs/agent-configuration/subagents

Explicit user scope can permit **manual coordination** under actual host controls, but that never creates a user-authenticated gate signature. See `APPROVAL.md` and `APPROVAL_MAINTENANCE.md`; the former defines ledger/gate requirements, the latter defines the authorization mode.
