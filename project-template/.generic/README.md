# Generic coding-agent adapter source (PORT REQUIRED)

This folder is a **copy-and-adapt starter**, not a native registered extension for any IDE. It saves setup quota by shipping the **same full agent role contracts** found in `.agents/roles/` as standalone `.generic/agents/<role>.md` files. The installer filters roles according to Lite / Standard / Full.

Use this only when your actual coding host does not have a ready runtime package. **Codex and Antigravity generic templates are already copy-ready; Claude Code is preconfigured but host-untested; Continue is nearly ready with model/provider selection.** Do not regenerate their contracts merely for compatibility.

For a new host:
1. Read `PORTING.md` and the relevant `platforms/*.md` guide.
2. Reuse only installed role files (`.generic/agents/`) and shared procedures (`.agents/skills/`, `harness/common/`). Do not hallucinate native syntax.
3. Inspect the host's official role/skill/hook discovery, configuration schema, permissions, model/provider, and authorization. Convert native adapter files **only**, preserve role mandates and Human gates.
4. Verify positive AND negative smoke cases inside the actual host; mark `UNVERIFIED` or `GUIDED_ONLY` where unsupported.
5. Configure project-specific facts separately: CRITERIA, actual code/SDK, commands/tests, active Git branch, approved task and secrets only via host-approved secret storage.

Do not copy `.generic/agents/*.md` into a guessed native directory automatically. They are portable source text until a host-specific installation is explicitly validated. Human approval is required for runtime permission changes.

Setup choices belong in the IDE-native dialog or CLI numbered menu, never in plain chat. For the CLI fallback, run `project-template/harness/common/setup_intake.py --preinstall --runtime generic --output PRIVATE_TEMP_FILE` in a real TTY, then preview `install.py --target PATH --tier SELECTED_TIER --config-git SELECTED_GIT_MODE --runtime generic --target-app cline --staged --intake-file PRIVATE_TEMP_FILE`. Only apply after authorization. `--ask-first` is developer reference output, not the interactive questionnaire.
