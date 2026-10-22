# Bootstrap — Coding agent setup

[Tiếng Việt](../README.md) | [**English**](user-guide.en.md) | [For AI](FOR_AI.md)

Bootstrap helps **Codex, Claude Code, Antigravity**, and compatible coding agents set up project-specific agents, skills, hooks, scripts and workflows.

**How to use:** open a coding agent with access to the project folder and a command execution tool. Copy **one** prompt below and replace **only the folder path**. You do not need to clone Bootstrap, copy templates or run the installer yourself; the agent handles these steps when authorized.

## 1. Greenfield — new project

> Set up Bootstrap for my **greenfield project (new, no code yet)** at `<PROJECT_FOLDER_PATH>`. Read and follow https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Before any tool permission request, warn that setup questions are separate from permissions. Handle setup; ask only for approvals.

## 2. Brownfield — existing codebase

> Set up Bootstrap for my **brownfield project (existing codebase)** at `<PROJECT_FOLDER_PATH>`. Read and follow https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Before any tool permission request, warn that setup questions are separate from permissions. Preserve code; handle setup and approvals.

**Permission and setup questions are different:** The AI gives a short advance notice. After command permission, **IDE users get a configuration dialog**, while **CLI users see numbered choices in their terminal**. Read the question before selecting 1/2: these are setup answers, **not further permission approvals**. Answers are saved as trace; setup questions are not collected in ordinary chat.

**VS Code Copilot:** select `--runtime copilot` for the native `.github/agents` and `.github/hooks` package; do not use generic targeting Copilot for a fresh install. In the Copilot Session Target select Planner; first show draft/settled delta in chat, summon Technical Advisor **only after Human requests writing**, and require a separate post-advice Human confirmation before the one-shot staged Criteria apply. See `.github/COPILOT_SETUP.md`. Hook coverage and chat-origin confirmation are not OS-level authentication.

**Generic hosts (OpenCode, Qwen Code and other CLI/IDEs):** `--runtime generic` copies portable requirements, **then the installing agent must read `.generic/ADAPTER_REQUIREMENTS.md` and migrate the active `.generic` configuration into the actual host-native settings directories (see `.generic/HOST_NATIVE_LAYOUT.md`) and write/register/test the host-native adapters and hooks** during setup. Do not ask the Human to write scripts or finish the setup at `PORT_REQUIRED` when the host supports the mechanisms. Unsupported controls require evidence and honest `GUIDED_ONLY` labeling; `Standard` alone is not proof of native hooks or authenticated Human approval.

**Codex Cloud:** when a separate fresh session or Human-operated terminal cannot be opened, run disposable checks in the **current task** and report `SCRIPT_TESTED / HOOK_RUNTIME_UNVERIFIED`, not a fabricated host-ready state. See [For AI](FOR_AI.md).

## What the coding agent handles

The agent identifies the host runtime, inspects the project and runs the installer in **staged mode**. Greenfield uses `brainstorm-theory` with its scope questions; brownfield uses `write-criteria` to consolidate Human decisions and reconstruct observed CURRENT behavior from code without treating it as automatically approved DESIRED behavior. On Human request to finalize initial Criteria or change existing Criteria, Planner pauses **just before the file write** for Technical Advisor consultation (unless the exact proposal was already advised). Human decides after advice; only Planner edits Criteria. Advisor never approves or vetoes. Then the agent coordinates technical direction, Coder/Tester setup, audit and smoke tests. It then asks for real host verification before final hook activation and handoff. Detailed steps live in [For AI](FOR_AI.md), not in the user prompt.

**Environment:** Codex CLI/App, Claude Code and compatible coding agents can run shell/terminal commands **when permitted by the host and user**. A sandbox, blocked network, or missing filesystem access must be reported, not silently assumed away. **Web-only Claude sessions are not substitutes for coding agents with access to the target project.**

### ⚠️ Keep the setup session open

If instructed to open a fresh coding-agent session for hook testing, **do not close the original setup session**. Return errors there for diagnosis. **The Human personally runs** `activate` and `finalize` from an independent interactive terminal. Close the setup session only after post-lock verification and handoff.

## After handoff

The agent supplies the Planner kickoff prompt. If needed manually:

> Invoke **Planner** to review approved CRITERIA, draft/revise the Implementation Plan (GOALMAP inside the Plan, each section beginning with an outcome GOAL) and Milestones, then ask for my approval before Tasks or coding.

For `local/tracked` settings, upgrades, rollback, Lite limitations, and detailed tests, see [For AI](FOR_AI.md) and the [technical setup guide](../project-template/SETUP.md). Script PASS is not proof of native host enforcement.

[License](../LICENSE).
