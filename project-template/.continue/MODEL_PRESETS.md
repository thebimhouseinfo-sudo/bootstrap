# Continue: prebuilt model/provider fill-in guide

The checked-in `.continue/config.yaml` is a valid schema-v1 starting point with deliberately empty model connections. Fill the **actual available** provider name, model ID, API auth via supported secrets, and role/tool capabilities after inspecting the user's Continue installation.

Recommended division: strongest available tool-capable model for planning/deep review, balanced tool-capable model for Coder/Tester, fast model for exploration. OpenAI Codex model IDs and Claude Code aliases cannot be assumed available in Continue. Continue workspace rules under `.continue/rules/` reuse the full generic workflows, but rules are not isolated named subagents.

Do not overwrite connected user config. Present exact changes, verify configuration loads in Continue, test a normal role task and report unavailable capabilities.
