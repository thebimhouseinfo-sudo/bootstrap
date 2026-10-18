# Bootstrap: coding-agent harness templates (baseline release)

[**English**](README.en.md) | [Tiếng Việt](README.md)

> **Goal:** Bootstrap is a **reusable project-setup template for popular coding agents**, designed to **reduce setup token/quota consumption and time**. Reuse prepared roles, skills, scripts, hooks and instructions instead of rediscovering or rebuilding an agent harness for every project or IDE.
>
> **Generic template readiness (distinct from project-specific setup):**
> - **Codex and Google Antigravity IDE — GENERIC READY:** The Human has installed and tested both on real machines. Choose the correct runtime and tier, **copy the template and start the generic coding-agent workflow without modifying the generic package**.
> - **Claude Code — CONFIGURED, NOT HOST-TESTED:** Role/skill configuration, native settings and hook adapter are prepared. The Human has not installed Claude Code for a real-host smoke test; **this does not mean its generic configuration is missing**.
> - **Continue — NEAR GENERIC READY, NOT HOST-TESTED:** Role configurations and rules are prepared. Its provider/**model mapping** must be set for the user's VS Code environment. Similarity to Antigravity does not prove identical native hook or subagent behavior; verify on the actual host.
> - **Other coding agents:** Use prepared **`.generic/` roles and porting guides** for Cline, Qwen Code, DeepSeek-based clients and other platforms; adapt only native registration/config formats, not the whole harness.
>
> **Two separate notions of ready:** GENERIC READY means the reusable coding-agent template is usable without rewriting its generic files. **The target project still needs its own configuration** (CRITERIA, stack/host/API, paths, verified build/tests, Git branch and any required model choices). This does **not** certify all gates, hooks or isolation as `ENFORCED`. `harness/common/status.py` reports technical capability states; it is not the standalone measure of *generic template usability*.
>
This repo is **runtime-neutral**, with no primary app. Users supply a repo link and brief project context. The AI chooses the matching package, gathers only missing information, obtains approval, then copies and **configures project-specific facts or the adapter gaps of an as-yet unsupported host**. When it lacks filesystem/terminal access, it provides exact OS/shell/path-specific commands rather than making the human locate files.

Do not redesign the harness from scratch or rewrite generic agents and skills. All claims of working functionality must be backed by actual tests. Protected decisions require a human-only **Approval Request with three choices: Agree / Disagree / Other**. The initial setup exception, when that channel has not yet been installed, must be explicitly disclosed.

---

**No runtime is primary or selected by default.** The AI must identify the actual host in one pre-install configuration step and pass an explicit `--runtime` to the installer. Human testing on Codex and Antigravity does not automatically certify host hooks, signed gates or orchestration on every version.

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
  .generic/                 # for other coding clients
    agents/                 # portable tier-filtered role contracts
    platforms/              # Cline / Qwen Code / DeepSeek client guidance
    PORTING.md
  harness/
    common/                   # shared verify and inventory
    codex/                    # Codex preflight
    claude/                   # Claude Code adapter
    specs/
    HARNESS_SPEC.md
  lessons/
```

- **Codex and Google Antigravity IDE — GENERIC READY:** The Human has tested installation and generic use on machines with the respective apps. Copy the matching runtime package; do not rewrite prepared generic roles, skills or scripts merely to start using it. Codex: `.codex/agents/*.toml` and `.codex/hooks.json`; Antigravity: `.agents/skills/`, `.agents/hooks.json`, `.antigravity/agents/*.md`. Configure target-project facts separately.
- **Claude Code — configured, not tested inside Claude Code:** `.claude/agents/`, `.claude/settings.json`, `harness/claude/hook.py` and reused skills/rules are included. Lack of a host test is not a reason to rebuild the adapter. Smoke-test when Claude Code is available.
- **Continue — nearly ready:** `.continue/agents/` includes role configs/rules; it reuses the **same `.agents/roles/`, `.agents/skills/` and shared Python helpers as Antigravity**, differing only in native agent/model registration. Configure the actual provider/models, select a role config, and check Continue's own hook/subagent limitations in VS Code; do not assume Antigravity exposes identical APIs.
- **Cline, Qwen Code, DeepSeek-based clients, Copilot, Cursor and others:** Select `--runtime generic --target-app APP` to copy `.generic/agents` and porting guides. DeepSeek may be a model/provider, not the client; identify the actual host first. Start from the prepared contracts/files, consult the platform's documentation, and port only the necessary adapters or hooks. Report any `UNVERIFIED` / `GUIDED_ONLY` boundaries without treating absent host tests as lack of support.

### Core rules

1. **Maximize reuse to save quota.** Copy the Codex/Antigravity generic package as-is and configure project-specific facts. For Claude/Continue and other apps, change only genuine adapter or model-mapping gaps, not shared roles/skills/scripts; add files only when the template is missing a necessary component.
2. **Do not modify this source repository** when working on another project.
3. **Single source of product theory:** `docs/CRITERIA.md`; GOALMAP is inside it. Do not create competing specifications.
4. **Human-only approvals:** agents cannot answer their own requests or write protected journals, decisions and approval ledgers. Chat “OK” is not formal authorization.
5. **Enforceable safeguards require actual mechanisms.** Use scripts/hooks for mechanical rules and Reviewer/Critic for judgment. Instruction-only protection is `GUIDED_ONLY`, never `ENFORCED`.
6. **Minimalism:** every retained component must prevent a specific failure.
7. **No default push or network access in hooks.** Avoid unauthorized `git init`, forced push, destructive reset, history rewrite, unknown-branch deletion or third-party dependency/MCP installation.
8. **No silent model substitutions.** Report missing choices as `UNAVAILABLE`.
9. **Do not spend setup quota re-researching already generic-ready presets without an actual issue.** On Codex/Antigravity, copy first and verify project-specific settings. Consult official runtime/host/API documentation when the version differs, errors appear or an untested platform needs adaptation; never mix native schemas.
10. **Escalate template conflicts** in the adaptation table; do not choose arbitrarily.
11. **Coder and Tester work with generic defaults** even without optional project-specific skill/knowledge packs. Mandatory host/dialect constraints still apply.
12. **Report actual readiness.** READY, CONFIGURE, IMPLEMENT, ENFORCED, GUIDED_ONLY, NOT_CONFIGURED and UNVERIFIED are different states.
13. **Evidence-specific compatibility:** Codex and Antigravity are GENERIC READY and Human-tested; Claude Code is fully configured but lacks host testing; Continue is nearly ready pending provider/model selection and host testing; other runtimes should port only necessary adapters. Never equate this generic readiness with `ENFORCED` or claim `RUNTIME_VERIFIED` without corresponding evidence.

### Setup workflow

**One-message Pre-Ask:** `python install.py --ask-first` prints the whole question set only (never installs and never asks sequential terminal questions). Before running setup tools or mixing in host tool-permission dialogs, gather all genuinely missing choices (project path, tier, runtime, Git branch, model, host/testing needs and approval channel) **in one chat message**, reusing context already known. After the human responds, inspect and install; do not drip-feed setup questions across command authorization prompts. This saves interaction time and quota.

#### Step 0. Classify the project

- **A — Existing code:** inspect source, configuration, tests and documentation. If operating theory is absent, record that fact; do not invent its behavior.
- **B — New project with approved specifications:** use approved information to identify product and technical constraints. Planner consolidates theory into CRITERIA; Bootstrap does not approve or rewrite its product logic.
- **C — New project without approved theory:** enable a **minimal Planner Discovery Mode** (brainstorming, research, CRITERIA placeholder, available conversation and approval channel). Do not force the user to finish requirements first. Do not choose the final stack, start product tasks or claim a full harness exists yet.

#### Step 1. Collect only missing information

Inspect known information first. Determine: Lite/Standard/Full tier (Standard is the typical default), agent runtime/version (chosen from the actual installed app, never presumed), OS and shell, Git/remote/branch, product type and host, existing stack, real integration test availability, models/tools actually supported, language dialect and API version requirements, reporting language, and the available human approval channel.

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

**The AI does the copying, not the user.** Preview with `python install.py --target PATH --tier Standard --runtime RUNTIME` (choose `antigravity`, `codex`, `claude`, `continue`, or `generic` explicitly; for `generic`, also pass `--target-app cline` or another actual client); after approval add `--apply`. Valid runtimes: `antigravity`, `codex`, `claude`, `continue`, `generic` (with `--target-app`); tiers: `Lite`, `Standard`, `Full`. With permitted filesystem/terminal access, install the approved template contents into the target project root, preserve existing data, fill verified facts and inspect the diff. Without that access, give exact commands appropriate for the confirmed OS/shell/repository/path; ask the user to run them and inspect their output. Do not guess locations or provide unsafe blanket overwrite commands.

For Codex and Antigravity, **the GENERIC READY template can be copied and used for generic agent work without modifying shared roles/skills/scripts**. Then fill PROJECT_PROFILE with verified host/version/dialect/API/build/test commands for the **specific project**. Claude Code has its generic configuration prepared but needs host testing; Continue primarily needs provider/model mapping and host testing. Other platforms should adapt only necessary adapters following `project-template/SETUP.md` and `harness/specs/`, saving setup quota rather than rebuilding. Bootstrap prepares CRITERIA/planning placeholders; Planner creates project-specific content after the relevant approvals. Final AGENTS instructions should reference only installed and functional roles, commands, hooks and gates. Do not mark NOT_CONFIGURED as PASS.

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

### Generic runtime adapter readiness

| Coding agent | Generic template readiness | After copying to a project |
| --- | --- | --- |
| **Codex** | **GENERIC READY — Human-tested** | Use the generic package; fill in target-project settings and verification |
| **Google Antigravity IDE** | **GENERIC READY — Human-tested** | Same as Codex; no generic rewrite required |
| **Claude Code** | **Fully configured, not host-tested** | Smoke-test in Claude Code when available; configure the target project |
| **Continue** | **Near GENERIC READY, not host-tested** | Select provider/models and role config; verify native host constraints |
| **Cline / Qwen Code / DeepSeek-based client / Copilot / Cursor / others** | **`.generic/` portable role source (not host-tested)** | Copy tier-filtered roles and porting guide; adapt only the native adapter |

Adapter files: Codex `.codex/` and `harness/codex/`; Antigravity `.agents/` and `.antigravity/`; Claude Code `.claude/` and `harness/claude/`; Continue `.continue/` plus shared Antigravity-like `.agents/roles`/`.agents/skills` (not Antigravity native hooks); other apps `.generic/`. Shared Python is in `harness/common/`.

**Scope of READY here:** copy-and-use generic coding-agent configuration, **not** a claim that the signed-gate engine, authenticated approvals or host-level enforcement are fully operational. Product-specific setup is still required.

### Active development branch and frozen main

Bootstrap includes `harness/common/branch_authority.py` in every Git-enabled tier. Human chooses the active development branch (e.g. `v5`), frozen branches (`main`) and registered work branches. Canonical policy is stored in the Git common directory, independent of checkout. Planner/Coder check it before coding, creating branches, merging and pushing; Git default `main` must never be assumed. Codex PreToolUse can deny observed direct apply_patch on wrong branches, but is not universal shell/MCP/API or server protection. See [BRANCH_AUTHORITY.md](project-template/harness/specs/BRANCH_AUTHORITY.md).

### Generic adapter setup flow

Run `python install.py --ask-first` to display all setup questions together for one AI chat message, never a sequence of terminal configuration dialogs. With the Human's answers, preview `python install.py --target PATH --tier Standard --runtime generic --target-app qwen-code` and use `--apply` only after approval. `.generic/` supplies portable role contracts and host porting instructions; it does **not** automatically register untested native agents. Continue receives the same shared `.agents/roles`, `.agents/skills`, and `harness/common` content as Antigravity, but uses `.continue/` for its native agent/model configurations; Antigravity `.agents/hooks.json` is not copied into Continue.
