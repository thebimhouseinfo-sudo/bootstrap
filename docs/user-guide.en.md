# Bootstrap — Coding agent setup

[Tiếng Việt](../README.md) | [**English**](user-guide.en.md) | [For AI](FOR_AI.md)

Bootstrap helps **Codex, Claude Code, Antigravity**, and compatible coding agents set up project-specific agents, skills, hooks, scripts and workflows.

**How to use:** open a coding agent with access to the project folder and a command execution tool. Copy **one** prompt below and replace **only the folder path**. You do not need to clone Bootstrap, copy templates or run the installer yourself; the agent handles these steps when authorized.

## 1. New project — no existing code

> Set up Bootstrap for my **new project** at `<PROJECT_FOLDER_PATH>`. Read and follow https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Orchestrate setup and Discovery; ask me only for missing information or decisions requiring approval.

## 2. Existing project — already has code

> Set up Bootstrap for my **existing codebase** at `<PROJECT_FOLDER_PATH>`. Read and follow https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Inspect and preserve current code, orchestrate setup, and ask me only for missing information or decisions requiring approval.

**Dialog UX:** Before setup, your host may show a **command permission dialog**. After you grant access, a **separate configuration questionnaire dialog** will appear. Read and answer it carefully: it is not another permission request. Answers are retained as trace; **configuration Q&A never happens in ordinary chat**.

## What the coding agent handles

The agent identifies the host runtime, inspects the project, obtains and runs the installer in **staged mode**, coordinates CRITERIA and technical approval, configures Coder/Tester, audits files and runs smoke tests. It then asks for real host verification before final hook activation and handoff. Detailed steps live in [For AI](FOR_AI.md), not in the user prompt.

**Environment:** Codex CLI/App, Claude Code and compatible coding agents can run shell/terminal commands **when permitted by the host and user**. A sandbox, blocked network, or missing filesystem access must be reported, not silently assumed away. **Web-only Claude sessions are not substitutes for coding agents with access to the target project.**

### ⚠️ Keep the setup session open

If instructed to open a fresh coding-agent session for hook testing, **do not close the original setup session**. Return errors there for diagnosis. **The Human personally runs** `activate` and `finalize` from an independent interactive terminal. Close the setup session only after post-lock verification and handoff.

## After handoff

The agent supplies the Planner kickoff prompt. If needed manually:

> Invoke **Planner** to review approved CRITERIA, draft/revise the Implementation Plan (GOALMAP inside the Plan, each section beginning with an outcome GOAL) and Milestones, then ask for my approval before Tasks or coding.

For `local/tracked` settings, upgrades, rollback, Lite limitations, and detailed tests, see [For AI](FOR_AI.md) and the [technical setup guide](../project-template/SETUP.md). Script PASS is not proof of native host enforcement.

[License](../LICENSE).
