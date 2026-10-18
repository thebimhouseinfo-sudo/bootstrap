# Codex adapter — current release

Preconfigured `.codex/agents/*.toml` includes role prompts and per-role models/effort. Main chat model remains user-selected. No subagent TOML overrides the parent session's `sandbox_mode` or `approval_policy`. Advisor/Critic/Explorer **request read-only behavior in instructions**, but there is **no independent read-only sandbox** in the shipped adapter; do not claim isolation or an enforced read-only role. A separate isolated read-only environment needs an actual implemented and tested runtime mechanism.

`python harness/codex/preflight.py` checks local version/config and asks for effective session policy/trust evidence; this is NOT proof that hooks or agent permissions were activated.

Portable scripts installed for all runtimes:
- `python harness/common/inventory.py --tier Standard --runtime codex`: file/skill inventory
- `python harness/common/verify.py`: approved configured commands; empty configuration returns NOT_CONFIGURED (exit 2)
- `python harness/common/status.py --tier Standard --runtime codex`: reports release capability gaps and returns exit 2 until automated tier+host requirements are verified

**Release scope:** basic installer, inventory, verifier, preflight, role files. Native hooks, snapshot, authenticated approval, journal, gate engine, trace and review orchestration are currently **specifications, not implemented runtime code**. `harness/common/capabilities.json` is the machine-readable declaration. Process-tree timeout cleanup for verifier is best effort.
