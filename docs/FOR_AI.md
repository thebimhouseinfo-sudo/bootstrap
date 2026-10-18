# Bootstrap — instructions for AI setup agents

[Vietnamese](../README.md) | [English](user-guide.en.md) | [**For AI**](FOR_AI.md)

**Source of truth:** `../project-template/` is the distributable canonical template. This guide instructs the **Environment Architect** during bootstrap; the installed `AGENTS.md` controls normal product work. Follow the staged workflow below. The installer does not automatically research product requirements, approve theory, or guarantee native hook activation.

## First-install staged contract

1. Identify **new** (no code) vs **existing** (working code) project. Inventory its host, stack, Git and existing files. Batch only missing questions. Avoid touching existing product code.
2. **Preliminary install:** preview `python install.py --target PATH --tier Standard --runtime RUNTIME --staged`, obtain approval, then append `--apply`. Staged installs leave blocking hooks in BOOTSTRAPPING mode. Old installs without staged state retain legacy behavior; do not silently override them.
3. **Planner Discovery:** immediately check status of `docs/CRITERIA.md`. If new, brainstorm with human. If existing code, reconstruct verified observed behavior, distinguish CURRENT/REQUESTED/GAP, and ask what human wants. Never equate code to approved requirements; never overwrite an already approved CRITERIA without the settled-delta/Advisor/human process.
4. **Technical direction:** after CRITERIA approval, propose evidence-based stack/architecture for new projects or continuation/refactor options with compatibility/regression risks for existing ones. Discuss feasibility and costs with the human; obtain explicit technical direction approval. Record HOW in ARCHITECTURE and PROJECT_PROFILE, not product GOALMAP.
5. **Project specialization:** configure optional focused knowledge/skills for Coder (host SDK, dialect, API, build) and Tester (unit, integration, live-host, regression). Load relevant context per task; lack of optional packs does not disable normal generic agents. Configure `harness/common/checks.json` from real commands only.
6. **Configuration audit:** inspect every required installed artifact, unresolved placeholders, selected roles, interpreter paths, Git branch authority and recovery. Mark genuinely optional capabilities NOT_APPLICABLE/UNVERIFIED rather than claiming PASS.
7. **Self-generated smoke:** derive positive and negative test cases from installed hooks/scripts. Use safe disposable artifacts/worktrees and subprocess fixtures. Test legitimate operations are not incorrectly blocked and forbidden actions are blocked at the declared interception boundary. Fix approved configuration errors and rerun relevant regressions. Do not weaken an enforced rule to pass tests.
8. **Fresh real-host session:** provide an exact host-specific prompt/commands when the setup session cannot prove native event dispatch. **Warn loudly: NEVER CLOSE THE ORIGINAL SETUP TAB.** Save checkpoint/recovery guidance first; human opens a second tab in the same project, runs positive/negative live tests, and reports observations back. If the second tab BLOCKS, use the original setup tab/independent recovery, not a self-bypass.
9. **Final lock:** after real-host evidence and required config audit PASS, explicitly activate the staged hook state using `harness/common/setup_lifecycle.py` with a reviewed evidence file and real host verification; retest after lock. Policy-changing operations require specific human authorization and cannot produce authenticated approval signatures.
10. **Handoff:** report actual PASS/FAIL/UNVERIFIED and remaining limitations. Provide one **Planner** kickoff prompt to read approved CRITERIA and build **Implementation Plan + GOALMAP**, then Milestones for human approval; only then Tasks and development. This is the main workflow, not a second setup.

**GOALMAP lives in `docs/IMPLEMENTATION_PLAN.md`, never in CRITERIA.** Each Plan section begins with the **GOAL** (observable product outcome and why code exists), then CRITERIA IDs, implementation strategy, dependencies, acceptance and test evidence. No milestone or task is approved simply by existing in the template.

**Recovery:** do not treat text instructions as a trusted host bypass. Before activating blocking hooks, back up policies/configuration and confirm a separate human-authorized maintenance procedure; if hooks are broken, use host controls or offline repair. Automatic authenticated gates, user-only ledger signatures and universal shell interception are NOT_CONFIGURED.

---

## For AI agents: mandatory instructions

### Your role

You are the **Environment Architect**. Your job is to inspect, propose and, after authorization, configure the coding-agent environment in the **target project**. You are not its Product Planner and must not invent features, roadmaps, milestones or development tasks, or write product code during bootstrap. Do not modify this bootstrap repository while setting up another project.

Planner owns product discovery and CRITERIA. **Technical Advisor** independently advises the human: CRITERIA determines what is wanted; relevant existing architecture, environment and limited source can be read when needed to assess feasibility, prerequisites, complexity/cost and ripple effects. Advisor never reviews Plan/Code quality, issues PASS/FAIL or vetoes. It advises on the whole draft before initial approval, or the settled delta just before any approved CRITERIA edit. **Optional tier comparisons are allowed**, used only where real choices exist. Human decides; Planner writes the authorized theory.

Planner handles product content in two modes: **Discovery**, brainstorming and researching with the user while recording unresolved theory as `OPEN` in CRITERIA; and **Delivery**, deriving approved goals, milestones and tasks. Bootstrap only installs the necessary environment.

### Canonical template structure

Only [`project-template/`](../project-template/) is the installation source. Copy its **contents** into the target project's root, not into an extra nested directory, and only after inspecting existing files and obtaining the required authorization.

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

- **Codex and Google Antigravity IDE — GENERIC READY:** Installation and generic use have been tested. Copy the matching runtime package; do not rewrite prepared generic roles, skills or scripts merely to start using it. Codex: `.codex/agents/*.toml` and `.codex/hooks.json`; Antigravity: `.agents/skills/`, `.agents/hooks.json`, `.antigravity/agents/*.md`. Configure target-project facts separately.
- **Claude Code — configured, not tested inside Claude Code:** `.claude/agents/`, `.claude/settings.json`, `harness/claude/hook.py` and reused skills/rules are included. Lack of a host test is not a reason to rebuild the adapter. Smoke-test when Claude Code is available.
- **Continue — nearly ready:** `.continue/agents/` includes role configs/rules; it reuses the **same `.agents/roles/`, `.agents/skills/` and shared Python helpers as Antigravity**, differing only in native agent/model registration. Configure the actual provider/models, select a role config, and check Continue's own hook/subagent limitations in VS Code; do not assume Antigravity exposes identical APIs.
- **Cline, Qwen Code, DeepSeek-based clients, Copilot, Cursor and others:** Select `--runtime generic --target-app APP` to copy `.generic/agents` and porting guides. DeepSeek may be a model/provider, not the client; identify the actual host first. Start from the prepared contracts/files, consult the platform's documentation, and port only the necessary adapters or hooks. Report any `UNVERIFIED` / `GUIDED_ONLY` boundaries without treating absent host tests as lack of support.

### Core rules

1. **Maximize reuse to save quota.** Copy the Codex/Antigravity generic package as-is and configure project-specific facts. For Claude/Continue and other apps, change only genuine adapter or model-mapping gaps, not shared roles/skills/scripts; add files only when the template is missing a necessary component.
2. **Do not modify this source repository** when working on another project.
3. **Single source of product theory:** `docs/CRITERIA.md`; it defines approved product requirements only. GOALMAP belongs in `docs/IMPLEMENTATION_PLAN.md` and traces back to approved requirements. Do not create competing specifications.
4. **Human-only approvals:** agents cannot answer their own requests or write protected journals, decisions and approval ledgers. Chat “OK” is not formal authorization.
5. **Enforceable safeguards require actual mechanisms.** Use scripts/hooks for mechanical rules and Reviewer/Critic for judgment. Instruction-only protection is `GUIDED_ONLY`, never `ENFORCED`.
6. **Minimalism:** every retained component must prevent a specific failure.
7. **No default push or network access in hooks.** Avoid unauthorized `git init`, forced push, destructive reset, history rewrite, unknown-branch deletion or third-party dependency/MCP installation.
8. **No silent model substitutions.** Report missing choices as `UNAVAILABLE`.
9. **Do not spend setup quota re-researching already generic-ready presets without an actual issue.** On Codex/Antigravity, copy first and verify project-specific settings. Consult official runtime/host/API documentation when the version differs, errors appear or an untested platform needs adaptation; never mix native schemas.
10. **Escalate template conflicts** in the adaptation table; do not choose arbitrarily.
11. **Coder and Tester work with generic defaults** even without optional project-specific skill/knowledge packs. Mandatory host/dialect constraints still apply.
12. **Report actual readiness.** READY, CONFIGURE, IMPLEMENT, ENFORCED, GUIDED_ONLY, NOT_CONFIGURED and UNVERIFIED are different states.
13. **Evidence-specific compatibility:** Codex and Antigravity are GENERIC READY and Tested; Claude Code is fully configured but lacks host testing; Continue is nearly ready pending provider/model selection and host testing; other runtimes should port only necessary adapters. Never equate this generic readiness with `ENFORCED` or claim `RUNTIME_VERIFIED` without corresponding evidence.

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

**The AI does the copying, not the user.** Preview with `python install.py --target PATH --tier Standard --runtime RUNTIME --config-git local` (or `--config-git tracked`) (choose `antigravity`, `codex`, `claude`, `continue`, or `generic` explicitly; for `generic`, also pass `--target-app cline` or another actual client); after approval add `--apply`. Valid runtimes: `antigravity`, `codex`, `claude`, `continue`; tiers: `Lite`, `Standard`, `Full`. With permitted filesystem/terminal access, install the approved template contents into the target project root, preserve existing data, fill verified facts and inspect the diff. Without that access, give exact commands appropriate for the confirmed OS/shell/repository/path; ask the user to run them and inspect their output. Do not guess locations or provide unsafe blanket overwrite commands.

For Codex and Antigravity, **the GENERIC READY template can be copied and used for generic agent work without modifying shared roles/skills/scripts**. Then fill PROJECT_PROFILE with verified host/version/dialect/API/build/test commands for the **specific project**. Claude Code has its generic configuration prepared but needs host testing; Continue primarily needs provider/model mapping and host testing. Other platforms should adapt only necessary adapters following `project-template/SETUP.md` and `harness/specs/`, saving setup quota rather than rebuilding. Bootstrap prepares CRITERIA/planning placeholders; Planner creates project-specific content after the relevant approvals. Final AGENTS instructions should reference only installed and functional roles, commands, hooks and gates. Do not mark NOT_CONFIGURED as PASS.

#### Step 4. Validate

Test using a disposable copy and fake data, following [`harness/specs/TESTS.md`](../project-template/harness/specs/TESTS.md). Each enforced boundary must demonstrate a prohibited operation that is blocked and a legitimate operation that passes. Check actual role/skill activation, verification, approvals, hooks and gates for the selected tier. Missing execution or host access means `UNVERIFIED`, never PASS.

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

## Keeping harness configuration in Git

The installer supports two modes through `--config-git`:

- **`local` (default):** keep agent configuration and runtime state on the local machine, as before.
- **`tracked`:** allow harness configuration to be committed to Git and shared across machines, while **keeping private runtime and approval state out of Git**.

**CONFIG (eligible for tracking in `tracked` mode):** `AGENTS.md`, `AGENTS.bootstrap.md`, `CLAUDE.md`, `TASKS.md`, the `.agents/`, `.antigravity/`, `.codex/`, `.claude/`, `.continue/`, `.generic/`, `harness/`, and `lessons/` directories, `docs/PROJECT_PROFILE.md`, and report templates under `docs/reports/`. Eligible for tracking does not mean every file must be committed.

**STATE (always local, including in `tracked` mode):** `harness/chat-journal.jsonl`, `harness/decisions.jsonl`, `harness/approvals.jsonl`, `harness/state.json`, `harness/last-block.json`, `harness/inbox.html`, `harness/snapshots/`, `harness/requests/`, `docs/TRACE.md`, and `.claude/settings.local.json`.

The approvals ledger remains specific to **one Human**. Multi-person approval authentication or synchronization through Git is not supported. Product documentation such as `docs/CRITERIA.md`, `ARCHITECTURE.md`, `MILESTONES.md`, and `BACKLOG.md` remains trackable in either mode.

```bash
python install.py --target PATH --tier Standard --runtime codex --config-git tracked
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --apply
# To switch modes, add --change-config-git to both preview and --apply
```

The managed `.gitignore` block keeps its existing `BEGIN/END` markers and adds `# mode: local|tracked` inside. Legacy blocks without a `# mode:` line are treated as `local`; running `--apply` updates the marker block without requiring a migration. Changing modes without `--change-config-git` is blocked as `MODE_CHANGE_REQUIRES_APPROVAL` (exit 2). Preview the change and get Human approval before applying.

The installer checks the real Git index (`TRACKED_LOCAL_SETUP` in `local` mode or `TRACKED_LOCAL_STATE` in `tracked` mode) and effective ignore rules with `git check-ignore` (`LOCAL_SETUP_NOT_IGNORED` / `LOCAL_STATE_NOT_IGNORED`). These checks never automatically delete files or change the index. **Note:** `--apply` updates `.gitignore` before verifying nested ignore exceptions, so a BLOCK at that point leaves `.gitignore` updated but copies no template files. Because Git cannot re-include individual children of a fully ignored parent directory, `tracked` mode ignores specific STATE paths rather than using a blanket `/harness/` rule.

The legacy `-y/--yes` flag is accepted but **ignored**; only `--apply` writes. Projects without Git should recheck effective ignore rules after `git init`. In the Bootstrap repository, `project-template/` remains versioned distributable source; the managed block is generated only in target projects.

## License

MIT. See [LICENSE](LICENSE).

### Generic runtime adapter readiness

| Coding agent | Generic template readiness | After copying to a project |
| --- | --- | --- |
| **Codex** | **GENERIC READY — Tested** | Use the generic package; fill in target-project settings and verification |
| **Google Antigravity IDE** | **GENERIC READY — Tested** | Same as Codex; no generic rewrite required |
| **Claude Code** | **Fully configured, not host-tested** | Smoke-test in Claude Code when available; configure the target project |
| **Continue** | **Near GENERIC READY, not host-tested** | Select provider/models and role config; verify native host constraints |
| **Cline / Qwen Code / DeepSeek-based client / Copilot / Cursor / others** | **`.generic/` portable role source (not host-tested)** | Copy tier-filtered roles and porting guide; adapt only the native adapter |

Adapter files: Codex `.codex/` and `harness/codex/`; Antigravity `.agents/` and `.antigravity/`; Claude Code `.claude/` and `harness/claude/`; Continue `.continue/` plus shared Antigravity-like `.agents/roles`/`.agents/skills` (not Antigravity native hooks); other apps `.generic/`. Shared Python is in `harness/common/`.

**Scope of READY here:** copy-and-use generic coding-agent configuration, **not** a claim that the signed-gate engine, authenticated approvals or host-level enforcement are fully operational. Product-specific setup is still required.

### Active development branch and frozen main

Bootstrap includes `harness/common/branch_authority.py` in every Git-enabled tier. Human chooses the active development branch (e.g. `v5`), frozen branches (`main`) and registered work branches. Canonical policy is stored in the Git common directory, independent of checkout. Planner/Coder check it before coding, creating branches, merging and pushing; Git default `main` must never be assumed. Codex PreToolUse can deny observed direct apply_patch on wrong branches, but is not universal shell/MCP/API or server protection. See [BRANCH_AUTHORITY.md](../project-template/harness/specs/BRANCH_AUTHORITY.md).

### Generic adapter setup flow

Run `python install.py --ask-first` to display all setup questions together for one AI chat message, never a sequence of terminal configuration dialogs. With the Human's answers, preview `python install.py --target PATH --tier Standard --runtime generic --target-app qwen-code` and use `--apply` only after approval. `.generic/` supplies portable role contracts and host porting instructions; it does **not** automatically register untested native agents. Continue receives the same shared `.agents/roles`, `.agents/skills`, and `harness/common` content as Antigravity, but uses `.continue/` for its native agent/model configurations; Antigravity `.agents/hooks.json` is not copied into Continue.
