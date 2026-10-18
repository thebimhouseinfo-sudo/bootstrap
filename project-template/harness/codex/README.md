# Codex runtime adapter

Codex-only preflight: `python harness/codex/preflight.py`.

Shared scripts for **all runtimes** live in `harness/common/`:
- `python harness/common/inventory.py --tier Standard --runtime codex`: file/skill inventory only
- `python harness/common/verify.py`: run approved checks from `harness/common/checks.json`; empty means NOT_CONFIGURED, exit 2
- `python harness/common/test_verify.py`: regression suite

Native Codex role TOMLs exist in `.codex/agents/`; their actual runtime discovery and permissions require smoke tests. Hooks, gate engine and authenticated approvals are not supplied by these baseline scripts. Do not claim ENFORCED without evidence. Timeout cleanup is best effort for owned process trees.
