# Bootstrap: Codex-ready harness templates for coding agents

[**English**](README.en.md) | [Tiếng Việt](README.md)

This repository is a **ready-made harness template library**, optimized for **Codex**. Users only provide the repository URL and a brief project description. The AI must inspect the target project, propose adaptations for approval, then copy and configure the selected templates itself. If the AI cannot access the project's files or terminal, it must provide precise commands for the user's OS, shell and project path, then verify the resulting output.

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
    knowledge/
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
    specs/
    HARNESS_SPEC.md
  lessons/
```

For Codex, the native role TOMLs and per-role model presets are already supplied, and verification/inventory are in `harness/common/`. File presence is **not** proof that subagents were loaded or that hooks, approvals, gates and review loops are active. Verify runtime features before claiming they work.

Claude Code agent and native skill layouts are prepackaged; Continue includes role-specific configs awaiting actual provider/model selection. For GitHub Copilot, Cline and other runtimes, preserve the generic role/skill logic and adapt the specific agent registration, skill discovery, config files, models, permissions, hooks, shell commands and approval channel to the supported runtime.

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

**The AI does the copying, not the user.** Preview with `python install.py --target PATH --tier Standard --runtime codex`; after approval add `--apply`. Valid runtimes: `codex`, `claude`, `continue`; tiers: `Lite`, `Standard`, `Full`. With permitted filesystem/terminal access, install the approved template contents into the target project root, preserve existing data, fill verified facts and inspect the diff. Without that access, give exact commands appropriate for the confirmed OS/shell/repository/path; ask the user to run them and inspect their output. Do not guess locations or provide unsafe blanket overwrite commands.

Reuse generic agents and skills unchanged wherever possible. Fill PROJECT_PROFILE with verified host/version/dialect/API/build/test commands. Bootstrap prepares CRITERIA/planning placeholders; Planner creates project-specific content after the relevant approvals. Final AGENTS instructions should reference only installed and functional roles, commands, hooks and gates. Apply existing Codex scripts where appropriate; implement missing native mechanisms from `harness/specs/`. Do not mark NOT_CONFIGURED as PASS.

#### Step 4. Validate

Test using a disposable copy and fake data, following [`harness/specs/TESTS.md`](project-template/harness/specs/TESTS.md). Each enforced boundary must demonstrate a prohibited operation that is blocked and a legitimate operation that passes. Check actual role/skill activation, verification, approvals, hooks and gates for the selected tier. Missing execution or host access means `UNVERIFIED`, never PASS.

#### Step 5. Report concisely

Report installed components and why they exist; actual enforcement versus guidance; role/model availability; exact tests and evidence; unverified items; how to use the harness day to day (no more than five lines); and any remaining user action.

---

## Tiers

| Tier | Suitable for | Intended scope |
| --- | --- | --- |
| **Lite** | Small, single-user projects | AGENTS, CRITERIA + GOALMAP framework, verify, snapshot, Stop hook where supported, lessons, evidence, journal, approval inbox, Coder + Reviewer |
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

## License

MIT. See [LICENSE](LICENSE).
