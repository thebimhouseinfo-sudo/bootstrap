# Continue: near-generic-ready role configuration templates

Eight **separate Continue config.yaml files** are prewritten in `agents/<role>/config.yaml`. Each contains the matching full generic role instructions as Continue `rules:`, plus schema v1 fields. The main remaining account-specific setup for a generic Continue workflow is `models` (provider/model and supported credentials/capabilities). Set a tool-capable model for agent work.

For each role to use: copy/select its prewritten config via Continue's supported configuration selector or `cn --config <path-to-role-config>`; complete `models` using the user's actual provider connection. Do not simultaneously activate every role's rules as global rules. This is **role-specific configuration selection**, not multiple concurrently isolated native Codex-style subagents.

The regular workspace `config.yaml` and `rules/` remain reusable for ordinary Continue operation. No fake API keys. For a user plan change, update only its role config model mapping; never rewrite the role procedure.

Continue is near generic-ready but has not been host-tested on the Human's machine; do not equate VS Code compatibility with Antigravity's native hook/subagent discovery. The reference implementation of hooks and task checks is now Codex-first (`.codex/hooks.json`, `harness/codex/hook.py`, `harness/common/*.py`). Continue needs a verified host-specific hook/CLI adapter; selecting a role config does not activate Codex hooks. Reuse Python scripts where possible, adapt event schema and trust, and report unsupported enforcement as GUIDED_ONLY.
