# Codex adapter — actual behavior and limits

- Native role TOML files live in `.codex/agents/`. They **inherit the parent model**; optional Sol/Astra/Luna/effort presets are in `MODEL_PRESETS.md` and must be applied only after account/model availability is confirmed.
- `.codex/config.toml` enables agents and sets a concurrency limit. It **does not set approval_policy, approvals_reviewer or permissions**. Parent-session and managed overrides remain authoritative.
- Critic and Explorer have `sandbox_mode = "read-only"` requested in their TOML. Verify that the installed Codex version recognizes this and that the **effective session sandbox** enforces it. Prompt-only isolation (Critic restricted document context) is still `GUIDED_ONLY` until tested.
- Bootstrap installer: `python install.py --target PATH --tier Standard --runtime codex` previews changes; add `--apply` only after review and authorization. The installer never overwrites existing files. Existing AGENTS conflicts export `AGENTS.bootstrap.md` for manual merge. Project product README is NOT installed.
- `python harness/codex/doctor.py` is an **inventory check**, not a runtime doctor.
- `python harness/codex/test_baseline.py` tests verifier behavior only.

**Working baseline:** installer, inventory check, preflight report and configured command verification. Snapshot/Stop hook/journal/authenticated approvals/gates/trace/orchestration are not active merely because contract files exist. Mark them NOT_CONFIGURED until independently implemented and tested.
