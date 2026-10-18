# Codex subagent model selection

The main chat model and reasoning remain entirely the user's choice. Only the native role TOMLs in `.codex/agents/` set subagent model and effort.

1. Inventory installed Codex version, actually available model IDs and supported reasoning efforts for the signed-in account. Do not infer subscription entitlements from product documentation.
2. Start from the supplied role defaults: Planner/Reviewer Sol high, Coder/Tester Sol medium, Critic/Harness Fixer Astra medium, Explorer Luna high. Check only active roles for the selected tier; avoid exhaustive model probes.
3. If a model is unavailable, or the user prefers faster/cheaper or stronger results, provide a concise affected-role table with model, effort, alternatives and tradeoffs. Ask the user to choose. Never silently fallback.
4. Modify only `model` and `model_reasoning_effort` for affected `.codex/agents/<role>.toml`. Do not modify the main chat model/effort in `.codex/config.toml`, approval policy or runtime sandbox.
5. Validate TOML, verify actual native agent discovery, invoke a safe role-specific smoke task and record observed model/access plus any missing capability. If unavailable, report `UNAVAILABLE`/`UNVERIFIED`, not PASS.
6. Keep the approved mapping for later runs; recheck only on account, version or user preference change. Never rewrite generic instructions solely for model selection.

Preset names are defaults, not a guarantee of account availability. Tera is not pinned without a verified exact model ID. Parent runtime restrictions remain authoritative.
