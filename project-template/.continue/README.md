# Continue: ready-made role configuration templates

Seven **separate Continue config.yaml files** are prewritten in `agents/<role>/config.yaml`. Each contains the matching full generic role instructions as Continue `rules:`, plus schema v1 fields. The only missing account-specific configuration is `models` (provider/model and supported credentials/capabilities). Set a tool-capable model for agent work.

For each role to use: copy/select its prewritten config via Continue's supported configuration selector or `cn --config <path-to-role-config>`; complete `models` using the user's actual provider connection. Do not simultaneously activate every role's rules as global rules. This is **role-specific configuration selection**, not multiple concurrently isolated native Codex-style subagents.

The regular workspace `config.yaml` and `rules/` remain reusable for ordinary Continue operation. No fake API keys. For a user plan change, update only its role config model mapping; never rewrite the role procedure.
