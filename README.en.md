# Bootstrap: coding-agent harness templates (baseline release)

[**English**](README.en.md) | [Tiếng Việt](README.md)

> **Release & Testing Status:** The template has **passed tests** when configured for **Google Antigravity IDE** (primary) and **Codex** (installer, baseline scripts, inventory, verify, snapshot, hooks/roles/skills have been verified). **Other coding agents (Claude Code, Continue, Copilot, Cline, etc.) have NOT yet reached READY status.** When setting up, the AI must **self-inspect and adapt/fix configuration following the template instructions** to fit its own platform. Check status using `python harness/common/status.py --tier Standard --runtime antigravity` (or `--runtime codex`). See `project-template/harness/specs/READINESS.md`.

This repository is a **ready-made harness template library** for coding agents. Currently, the template has **passed tests** when configured for **Google Antigravity IDE** (primary) and **Codex**; other coding agents are not yet ready and require the AI to self-inspect and adapt configuration according to its runtime. Users only provide the repository URL and a brief project description. The AI must inspect the target project, propose adaptations for approval, then copy and configure the selected templates itself. If the AI cannot access the project's files or terminal, it must provide precise commands for the user's OS, shell and project path, then verify the resulting output.

Do not redesign the harness from scratch or rewrite generic agents and skills. All claims of working functionality must be backed by actual tests. Protected decisions require a human-only **Approval Request with three choices: Agree / Disagree / Other**. The initial setup exception, when that channel has not yet been installed, must be explicitly disclosed.

---

## For users

Give your AI assistant the repository link and say:

> Read the README at `https://github.com/thebimhouseinfo-sudo/bootstrap`. Set up the coding-agent harness for my project using the ready-made templates. Copy and configure the files yourself if you have access; otherwise give me the exact terminal commands. Project: `<short description or path>`.

The AI inventories the project, asks only for missing information, presents an **adaptation and enforcement table** for your approval, then installs the selected components. You do not need to locate or copy files yourself.

---

## For AI agents: mandatory instructions

### Your role

You are the **Environment Architect**. Your job is to inspect, propose and, after authorization, configure the coding-agent environment in the **target project**. You are not its Product Planner and must not invent features, roadmaps, milestones or development tasks, or write product code during bootstrap. Do not modify this bootstrap repository while setting up another project.

Planner owns product discovery and CRITERIA. **Technical Advisor** independently advises the human: CRITERIA determines what is wanted; relevant existing architecture, environment and limited source can be read when needed to assess feasibility, prerequisites, complexity/cost and ripple effects. Advisor never reviews Plan/Code quality, issues PASS/FAIL or vetoes. It advises on the whole draft before initial approval, or the settled delta just before any approved CRITERIA edit. **Tạm dùng / Ổn / Nâng cao comparisons are optional**, used only where real choices exist. Human decides; Planner writes the authorized theory.

Planner handles product content in two modes: **Discovery**, brainstorming and researching with the user while recording unresolved theory as `OPEN` in CRITERIA; and **Delivery**, deriving approved goals, milestones and tasks. Bootstrap only installs the necessary environment.

### Canonical template structure

Only [`project-template/`](project-template/) is the installation source. Copy its **contents** into the target project's root, not into an extra nested directory, and only after inspecting existing files and obtaining the required authorization.

```text
project-template/
  AGENTS.md
  SETUP.md
  TASKS.md
  docs/
    CRITERIA.md
    PROJECT_PROFILE.md
    ARCHITECTURE.md
    MILESTONES.md
    BACKLOG.md
    TRACE.md
    reports/
  .agents/
    roles/
    skills/
    config/
    MODEL_SELECTION.md        # Antigravity model guide
    hooks.json                # Antigravity lifecycle hooks
  .antigravity/              # for Antigravity IDE
    agents/
  .codex/                   # for Codex
    config.toml
    agents/
  .claude/                  # for Claude Code
    agents/
    skills/
  .continue/                # for Continue
    agents/
  harness/
    common/                   # shared verify and inventory
    codex/                    # Codex preflight
    claude/                   # Claude Code adapter
    specs/
    HARNESS_SPEC.md
  lessons/
```

- **Google Antigravity IDE (primary — test passed):** skills and roles are discovered natively from `.agents/skills/` and `.agents/roles/`; model assignments by role reside in `.antigravity/agents/*.md` (with Gemini 3.8 Flash High fallback); lifecycle hooks are in `.agents/hooks.json` (Stop dispatches to `harness/common/verify.py`).
- **Codex (test passed):** native role TOMLs and model presets at `.codex/agents/*.toml` are preconfigured; native hook adapter in `.codex/hooks.json` dispatches to `harness/codex/hook.py`; verifier/inventory runs via `harness/common/`.
- **Other coding agents (NOT yet READY):** Claude Code (adapter `.claude/` + `harness/claude/hook.py`), Continue (`.continue/agents/`), GitHub Copilot, Cline, etc., have not yet reached READY status. **AIs operating on these platforms must self-inspect the platform's actual capabilities and adapt/complete configuration following the instructions in the template** (see `project-template/SETUP.md`, `project-template/AGENTS.md`, `project-template/harness/specs/READINESS.md`): adjusting agent registration, config format, skill paths, model mapping, native lifecycle hooks (or stating `GUIDED_ONLY` if the platform lacks enforcement hooks), and approval channels. File presence alone does not prove subagents are loaded or hooks are active. Verify runtime features with real tests before claiming readiness.

### Core rules

1. **Copy and adapt, never rebuild generic content.** Add a new file only if the reusable template genuinely lacks a needed component; explain why.
2. **Do not modify this source repository** when working on another project.
3. **Single source of product theory:** `docs/CRITERIA.md`; GOALMAP is inside it. Do not create competing specifications.
4. **Human-only approvals:** agents cannot answer their own requests or write protected journals, decisions and approval ledgers. Chat “OK” is not formal authorization.
5. **Enforceable safeguards require actual mechanisms.** Use scripts/hooks for mechanical rules and Reviewer/Critic for judgment. Instruction-only protection is `GUIDED_ONLY`, never `ENFORCED`.
6. **Minimalism:** every retained component must prevent a specific failure.
7. **No default push or network access in hooks.** Avoid unauthorized `git init`, forced push, destructive reset, history rewrite, unknown-branch deletion or third-party dependency/MCP installation.
8. **No silent model substitutions.** Report missing choices as `UNAVAILABLE`.
9. **Verify official documentation** for the actual runtime, OS, host and version. Never mix Codex, Claude Code, Copilot or Cline schemas.
10. **Escalate template conflicts** in the adaptation table; do not choose arbitrarily.
11. **Coder and Tester work with generic defaults** even without optional project-specific skill/knowledge packs. Mandatory host/dialect constraints still apply.
12. **Report actual readiness.** READY, CONFIGURE, IMPLEMENT, ENFORCED, GUIDED_ONLY, NOT_CONFIGURED and UNVERIFIED are different states.
13. **AI self-inspection and platform adaptation:** The template is test-passed for Antigravity IDE and Codex. For other platforms (not yet READY), the AI is responsible for inspecting its own runtime mechanisms and adapting/fixing the configuration following the template instructions, without shifting technical configuration burdens to the user.

### Setup workflow

#### Step 0. Classify the project

- **A — Existing code:** inspect source, configuration, tests and documentation. If operating theory is absent, record that fact; do not invent its behavior.
- **B — New project with approved specifications:** use approved information to identify product and technical constraints. Planner consolidates theory into CRITERIA; Bootstrap does not approve or rewrite its product logic.
- **C — New project without approved theory:** enable a **minimal Planner Discovery Mode** (brainstorming, research, CRITERIA placeholder, available conversation and approval channel). Do not force the user to finish requirements first. Do not choose the final stack, start product tasks or claim a full harness exists yet.

#### Step 1. Collect only missing information

Inspect known information first. Determine: Lite/Standard/Full tier (Standard is the typical default), agent runtime/version (Codex by default), OS and shell, Git/remote/branch, product type and host, existing stack, real integration test availability, models/tools actually supported, language dialect and API version requirements, reporting language, and the available human approval channel.

For case C, collect only what is necessary to begin Discovery. If a runtime has no hooks or human-only approval controls, disclose any journal and authorization integrity that remains `GUIDED_ONLY`.

#### Step 2. Propose changes before writing files

Inventory the canonical project tree and current target files. Show:

| Source template | Target path | Action | Reason / failure prevented | Adaptation needed |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | `AGENTS.md` | Keep / adapt / omit | Agent workflow | Verified project commands |
| `.agents/skills/*` | Runtime-native skill paths | Keep / adapt / omit | Repeatable skills | Registration if required |
| `harness/specs/*` | `harness/specs/` | Keep contract / implement | Hooks, gates and approvals | Runtime-specific scripts |

Include the tier, a role → model/reasoning/permission matrix, the enforcement table (`ENFORCED` / `GUIDED_ONLY` / `UNVERIFIED` / `NOT_CONFIGURED`), conflicts, rollback approach and tests. Submit a `HARNESS_PATCH` Approval Request, then stop before modifying protected files. If the approval mechanism itself is not yet installed, present the initial setup proposal in chat and state explicitly that this exception is **not technically enforced authorization**.

#### Step 3. The AI installs and customizes

**The AI does the copying, not the user.** Preview with `python install.py --target PATH --tier Standard --runtime antigravity` (or `--runtime codex`, `claude`, `continue`); after approval add `--apply`. Valid runtimes: `antigravity`, `codex`, `claude`, `continue`; tiers: `Lite`, `Standard`, `Full`. With permitted filesystem/terminal access, install the approved template contents into the target project root, preserve existing data, fill verified facts and inspect the diff. Without that access, give exact commands appropriate for the confirmed OS/shell/repository/path; ask the user to run them and inspect their output. Do not guess locations or provide unsafe blanket overwrite commands.

Reuse generic agents and skills unchanged wherever possible. Fill PROJECT_PROFILE with verified host/version/dialect/API/build/test commands. For Antigravity IDE and Codex, configurations are test-passed and ready for use once project parameters are filled. For other coding agents not yet READY, the AI must self-inspect and adapt configuration following `project-template/SETUP.md` and `harness/specs/` to suit its platform. Bootstrap prepares CRITERIA/planning placeholders; Planner creates project-specific content after the relevant approvals. Final AGENTS instructions should reference only installed and functional roles, commands, hooks and gates. Do not mark NOT_CONFIGURED as PASS.

#### Step 4. Validate

Test using a disposable copy and fake data, following [`harness/specs/TESTS.md`](project-template/harness/specs/TESTS.md). Each enforced boundary must demonstrate a prohibited operation that is blocked and a legitimate operation that passes. Check actual role/skill activation, verification, approvals, hooks and gates for the selected tier. Missing execution or host access means `UNVERIFIED`, never PASS.

#### Step 5. Report concisely

Report installed components and why they exist; actual enforcement versus guidance; role/model availability; exact tests and evidence; unverified items; how to use the harness day to day (no more than five lines); and any remaining user action.

---

## Tiers

| Tier | Suitable for | Intended scope |
| --- | --- | --- |
| **Lite** | Small, single-user projects | Target: AGENTS, CRITERIA, verify, snapshot, evidence, trusted native Stop and proportional approvals. **Currently shipped**: snapshot/verify scripts and Codex hook files; authenticated journal/approval inbox remains unimplemented. |
| **Standard** | Most projects | Lite + Planner/Tester/Critic, milestones and G0–G11, trigger-based review/repair, G13 trace, full decision log |
| **Full** | Larger or higher-risk projects | Standard + G14, G12 Git Admin, harness-fixer, doctor/self-tests, weakening detection |

Install only the approved tier's mechanisms. Listing a component does not prove installation. A later upgrade requires an approved `HARNESS_PATCH`.

---

## Ordinary and protected modifications

| May be configured for the project | Requires approved `HARNESS_PATCH` |
| --- | --- |
| Project name, paths and verified build/test/lint commands | Role permissions, deny-lists, protected paths |
| Technical profile, host/dialect/API and version | Gate semantics and escalation thresholds |
| Runtime-specific agent and hook syntax | Push policy and approval verification |
| Optional specialist skill and knowledge selection | Changes weakening protection or verified model assignments |
| Reporting language | Protected hook settings and approval ledger integrity |

A change that grants additional agent authority or weakens a guard must not be disguised as a placeholder edit.

---

## When blocked

Read the `BLOCK` code, rule, definition location, reason, evidence and authorized unlock requirement. When configuration seems defective, run the inventory/preflight or Full-tier harness-fixer, reproduce the issue and test the repair. **Fix the mechanism to match approved intent; do not weaken rules to bypass the block.** Exceptional one-time unlocks require a scoped `BREAK_GLASS` request.

---

## Local agent setup and GitHub

The installer appends or updates one marked block at the end of the target project's
`.gitignore`, preserving existing product rules. Agent directories (`.agents/`,
`.codex/`, `.claude/`, `.continue/`, `harness/`, `lessons/`), local instruction/task
files and agent profile/trace/report templates stay local. Product source, README,
CRITERIA, ARCHITECTURE, MILESTONES, BACKLOG and other product docs remain trackable;
the installer does not blanket-ignore `docs/`.

Preview reports `UPDATE .gitignore`; only `--apply` writes it. Already tracked local
setup is reported as `TRACKED_LOCAL_SETUP` with exit 2 for reconciliation before
publication. No files, index entries or Git history are removed automatically.
Ignore rules protect normal `git add`, not forced adds or existing tracked content.
In this bootstrap repository, `project-template/` remains versioned distributable
source: the local-only block is generated only in the installed target project.

For Git projects, the installer checks effective rules using `git check-ignore`
after updating the block. Nested exceptions exposing local files produce
`LOCAL_SETUP_NOT_IGNORED` and stop before setup files are copied. Git access/index/
metadata errors are not treated as an absent repository. For projects without
Git, rerun the installer after repository initialization to verify actual rules.

## License

MIT. See [LICENSE](LICENSE).

**Google Antigravity IDE (primary) & Codex (test passed):**
- **Antigravity IDE:** `.agents/hooks.json` declares Stop hook → `harness/common/verify.py`; roles and skills natively loaded from `.agents/roles/` and `.agents/skills/`; role model assignments in `.antigravity/agents/*.md` (Gemini 3.8 Flash High fallback).
- **Codex:** `.codex/hooks.json` dispatches to `harness/codex/hook.py`; subagents loaded from `.codex/agents/*.toml`.
- Shared Python lives in `harness/common/` (inventory, status, verify, snapshot, task, branch_authority).

**Other coding agents (NOT yet READY):**
- **Claude Code:** `.claude/settings.json` + `harness/claude/hook.py` (baseline adapter).
- **Continue, Copilot, Cline, Cursor...:** native configs not finalized or unverified.
- **Requirement for AI:** When deploying on these platforms, the AI must self-inspect and adapt configurations according to the template instructions (`project-template/SETUP.md`, `project-template/harness/README.md`, `project-template/harness/specs/READINESS.md`) to suit its own platform, then verify with smoke tests before declaring READY.

### Active development branch and frozen main

Bootstrap includes `harness/common/branch_authority.py` in every Git-enabled tier. Human chooses the active development branch (e.g. `v5`), frozen branches (`main`) and registered work branches. Canonical policy is stored in the Git common directory, independent of checkout. Planner/Coder check it before coding, creating branches, merging and pushing; Git default `main` must never be assumed. Codex PreToolUse can deny observed direct apply_patch on wrong branches, but is not universal shell/MCP/API or server protection. See [BRANCH_AUTHORITY.md](project-template/harness/specs/BRANCH_AUTHORITY.md).
