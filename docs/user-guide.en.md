# Bootstrap — Coding agent harness template

[Tiếng Việt](../README.md) | [**English**](user-guide.en.md) | [For AI](FOR_AI.md)

Bootstrap is a reusable harness of agent roles, skills, workflows, scripts and hooks for Codex, Google Antigravity, Claude Code, Continue and other coding agents. Give your agent **one of the setup prompts below**.

## Choose one of two short setup prompts

**Copy one prompt and replace only the project folder path.** The AI follows [For AI](FOR_AI.md) to handle discovery, configuration, testing and handoff; you provide missing information and approve decisions when requested.

### A. New project (no code yet)

> Set up Bootstrap for my **new project** at `<PROJECT_FOLDER_PATH>`. Follow the complete AI instructions: https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Run setup and Discovery autonomously; ask me only for missing information or decisions requiring approval.

### B. Existing project (has code)

> Set up Bootstrap for my **existing codebase** at `<PROJECT_FOLDER_PATH>`. Follow the complete AI instructions: https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md. Inspect and preserve the current code; manage setup autonomously and ask me only for missing information or decisions requiring approval.

The AI needs a local checkout of Bootstrap, separate from your project: `git clone --depth 1 https://github.com/thebimhouseinfo-sudo/bootstrap.git <temporary-folder>`. A raw documentation URL alone cannot run the installer. Clone only after approval (or ask the user to run it when no terminal access is available).

Use `python install.py --target PATH --runtime codex --tier Standard --staged` to preview, then append `--apply` **only after approval**. Choose your actual runtime. `--config-git local|tracked` selects whether non-private harness configuration can be committed; private approvals/state are never included in tracked mode.

## First-use sequence

Preliminary setup → CRITERIA discovery and approval → technical direction and approval → Coder/Tester specialization → complete configuration audit → simulated smoke tests → fresh host session test → final hook lock → post-lock live test → handoff.

**WARNING: DO NOT CLOSE THE SETUP TAB.** When asked to open a new coding-agent tab to validate native hooks, keep the original setup tab open. Return to it with any BLOCK/error for repair. Close it only after post-lock verification and successful handoff. The Human personally runs interactive `activate` and `finalize` from an independent terminal; the agent prepares evidence but does not attest its own approval. Use `python harness/common/setup_lifecycle.py host-test` for the host-specific instructions. A saved checkpoint and independent recovery instructions must be available.

## Prompt after successful handoff

> Invoke Planner following `AGENTS.md`. Read approved CRITERIA, create/review the Implementation Plan (GOALMAP and a GOAL at the start of every section), derive Milestones and ask for my approval before creating Tasks or coding.

Open future sessions in the installed project folder and follow `AGENTS.md`. You do not need to run the Bootstrap installer again.

## Lightweight Lite mode

For very small projects choose `--tier Lite --staged`; Lite lacks the full Planner and Tester roles, so it cannot promise the guided CRITERIA → Plan → Milestone sequence. Standard is recommended for the complete setup flow.

## Technical details and status

Bootstrap supports `local` (default) and `tracked` Git config. Switching modes requires `--change-config-git`; ignore rules cannot untrack previously committed files. Script tests are not native-host proof: distinguish SCRIPT_TESTED, RUNTIME_VERIFIED and ENFORCED. For setup scripts, actual hooks, adapter constraints and safe recovery see [For AI](FOR_AI.md).

For controlled upgrades, review `--upgrade`: only unchanged, manifest-owned files may update. Unrecognized or edited files remain conflicts. A separate interactive `harness/common/recover.py` will preserve backups for hook repairs.

[License](../LICENSE).
