# Codex — change subagent model only when necessary

**Defaults already configured in `.codex/agents/*.toml` (quota-saving preset):**

| Role | Model | Effort | Why |
|---|---|---|---|
| Planner, Advisor | `gpt-6.1-sol` | high | Rare, decision-critical |
| Critic | `gpt-6.1-sol` | high | Final technical review; no frontier model needed |
| Reviewer | `gpt-6.1-sol` | medium | Runs on every Plan/Code/Test |
| Harness Fixer | `gpt-6.1-sol` | medium | Rare, mechanical |
| Coder, Tester | `gpt-6.1-terra` | medium | Highest-volume roles |
| Explorer | `gpt-6-luna` | medium | Read-only scanning |

No preset uses `gpt-6-astra` ("frontier intelligence"). Model list checked 2026-10-27 in the Codex model picker and `~/.codex/models_cache.json`: Astra (frontier) > Sol (workhorse) > Terra (balanced) > Luna (fast, affordable); relative quota cost is inferred from those descriptions, not measured. If Coder output quality drops on hard tasks, raise Coder to `gpt-6.1-sol` first. Concurrent subagents: 2. **Chat agent model/effort is user-selected and not pinned.**

If user plan lacks a preset, or user requests different speed/quality/quota: (1) verify available model IDs and effort in the active Codex account/version, only for active roles; (2) show the affected roles and trade-offs, obtain user choice, never silent fallback; (3) edit only `model` and `model_reasoning_effort` for those `.codex/agents/<role>.toml`; (4) parse TOML and smoke-test actual agent invocation. Do not edit chat model, approval policy, permissions or generic instructions. Unavailable/untested → UNAVAILABLE/UNVERIFIED.

Model preset is not evidence of availability, sandbox enforcement or Critic context isolation. Effective parent permissions and runtime trust must be checked.

Codex custom role TOML does not override the parent sandbox or approval policy. A prompt asking Advisor/Critic/Explorer not to modify files is GUIDED_ONLY; no separate enforced read-only role exists in this release. Verify effective host policy before delegating.
