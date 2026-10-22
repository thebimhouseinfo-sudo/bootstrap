# Generic coding-agent contract — host adapter generated during setup

This folder is a **copy-and-adapt starter**, not a native registered extension for any IDE. It saves setup quota by shipping the **same full agent role contracts** found in `.agents/roles/` as standalone `.generic/agents/<role>.md` files. The installer filters roles according to Lite / Standard / Full.

**Two-stage install:** the Python installer distributes the platform-neutral requirements, roles, skills and scripts, **then the setup agent must implement the target host's native configuration and hooks** from `ADAPTER_REQUIREMENTS.md`. The installer intentionally ships zero *prebuilt* host-native hooks for generic. That is not permission to skip implementation or end setup with `PORT_REQUIRED`. If the host truly lacks a needed hook, report the technical evidence and reduced behavior. Human authorization/Advisor proof is never implied by a normal hook.

Use this only when your actual coding host does not have a ready runtime package. **Codex and Antigravity generic templates are already copy-ready; Claude Code is preconfigured but host-untested; Continue is nearly ready with model/provider selection.** Do not regenerate their contracts merely for compatibility.

For a new host:
1. Read **mandatory** `ADAPTER_REQUIREMENTS.md`, `PORTING.md` and the relevant `platforms/*.md` guide.
2. Reuse only installed role files (`.generic/agents/`) and shared procedures (`.agents/skills/`, `harness/common/`). Do not hallucinate native syntax.
3. Inspect the host's official role/skill/hook discovery, configuration schema, permissions, model/provider, and authorization. **Write and register host-native adapter files/scripts in the target project**; preserve role mandates and Human gates.
4. **Run real positive AND negative native host tests before handoff.** Record generated file paths and observed evidence; mark each unsupported path `UNVERIFIED` or `GUIDED_ONLY`.
5. Configure project-specific facts separately: CRITERIA, actual code/SDK, commands/tests, active Git branch, approved task and secrets only via host-approved secret storage.

Do not guess a native directory or silently change host permissions. The setup agent (not Human) performs documented porting after permission, tests it on a disposable copy, and reports actual coverage.

Setup choices belong in the IDE-native dialog or CLI numbered menu, never in plain chat. For the CLI fallback, run `project-template/harness/common/setup_intake.py --preinstall --runtime generic --output PRIVATE_TEMP_FILE` in a real TTY, then preview `install.py --target PATH --tier SELECTED_TIER --config-git SELECTED_GIT_MODE --runtime generic --target-app cline --staged --intake-file PRIVATE_TEMP_FILE`. Only apply after authorization. `--ask-first` is developer reference output, not the interactive questionnaire.
