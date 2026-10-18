# Bootstrap — instructions for AI setup agents

[Vietnamese](../README.md) | [English](user-guide.en.md) | [**For AI**](FOR_AI.md)

**Source of truth:** `../project-template/` is the distributable canonical template. This guide instructs the **Environment Architect** during bootstrap; the installed `AGENTS.md` controls normal product work. Follow the staged workflow below. The installer does not automatically research product requirements, approve theory, or guarantee native hook activation.

## Short-prompt entrypoint

User Guides intentionally provide exactly **two short prompts**: **new project** or **existing codebase**, both specifying only a target folder and a link to this guide. Treat the selected project kind and folder as authoritative intake, then **self-orchestrate the complete workflow below**; do not ask the Human to paste the workflow back into chat or enumerate steps. For a new project with no product description, begin Planner Discovery by asking the Human about their idea **after safe preliminary installation**, not by inventing requirements. For existing projects, inspect the actual code and approved CRITERIA before asking what the Human wants changed. Ask a compact set of questions only for genuinely missing facts, high-impact choices and required approvals. The AI performs technical steps when tools and permission allow; it does not impersonate Human-operated terminal confirmation or fabricate host tests. If a new project's folder is absent, ask permission to create it before running the installer.

## Single authoritative first-install workflow

**Mandatory setup source:** Bootstrap must be available as a local checkout; `install.py` reads `project-template/` relative to itself, not from a GitHub page. With human approval, clone using `git clone --depth 1 https://github.com/thebimhouseinfo-sudo/bootstrap.git <temporary-checkout>` into a safe, separate folder **outside the target project**, or reuse a verified existing checkout. Inspect local files from that checkout. GitHub's `blob` URL is for a file; GitHub's `tree` URL is for a folder. For just the English instructions, fetch `https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md`; the full installer cannot run from a raw-file URL alone. Preserve target project Git history and source.

**Tier prerequisite:** Standard or Full is required for the full Planner and Tester workflow. Lite is a lightweight, manually guided mode; do not promise autonomous Planner/Tester operation, hooks or approvals absent from its installed tier.

**Use this ONE sequence; the reference material below is not a second setup process:**

1. **Intake and project classification.** Run `python install.py --ask-first` to gather genuinely missing choices in one message. Determine new idea/no code vs existing code, host/runtime, tier, actual target folder, OS, Git active/frozen branches, target Git config mode, working build/test tools, and approval channel. Inventory the target before proposing writes.
2. **Preliminary staged install.** From the verified local Bootstrap checkout, preview `python install.py --target TARGET --tier Standard --runtime RUNTIME --config-git local --staged` (or `tracked`, with `--target-app CLIENT` for generic), show the diff, resolve conflicts and obtain authorization. Then rerun with `--apply`. `--staged` is mandatory for a first setup with blocking hooks; if it was omitted do not reopen a new agent tab before inspection. Never use an unstaged install merely to bypass this step.
3. **CRITERIA Discovery and approval.** Check the existing CRITERIA status first. For a new idea: brainstorm and research with Human. For existing code: inspect actual behavior, tests and source; distinguish CURRENT, DESIRED and GAP before revising the draft. An already-approved CRITERIA requires settled-delta, Advisor consultation and explicit approval for changes.
4. **Technical direction.** After CRITERIA approval, recommend an appropriate stack/architecture for new projects or compatible continuation/refactor options based on existing code. State tradeoffs and regression risks. Human approves before changing the technical direction; record the selected HOW in ARCHITECTURE and PROJECT_PROFILE.
5. **Specialize Coder/Tester and complete audit.** Configure focused SDK/dialect/API knowledge, verified build/test commands, working Git branch policy, real host integration and regression procedure. Optional packs do not block generic agents. Run `python TARGET/harness/common/setup_lifecycle.py audit` and repair all mandatory gaps without weakening guards.
6. **Automatic smoke and recovery readiness.** Derive positive ALLOW and negative DENY cases for **installed** hooks/scripts; run `python TARGET/harness/common/setup_lifecycle.py smoke` and additional safe disposable fixtures. Verify isolated rollback/recovery and preserve existing product files. Do not mistake script PASS for native host hook evidence.
7. **Real fresh-session host verification.** Run `python TARGET/harness/common/setup_lifecycle.py host-test` for host-specific actions. **WARNING: NEVER CLOSE THE ORIGINAL SETUP TAB.** Keep it as the repair coordinator. Open a separate tab, perform safe positive tests and forbidden-action tests only in a disposable clone/worktree, and report precise logs/version. If BLOCKED, return to original tab or a verified offline recovery tool.
8. **Human-operated final lock.** Save real observations to `harness/setup-live-evidence.json`. Ask the Human to personally open an independent terminal and run `python harness/common/setup_lifecycle.py activate --evidence harness/setup-live-evidence.json` **without automated input**, review prompts and type the requested confirmation. A regular agent tool execution or non-interactive pipe is refused. This is friction against accidental self-approval, not a cryptographic identity guarantee; a tool with terminal control can spoof a TTY, so do not claim ENFORCED human authentication.
9. **Post-lock host test.** Test again after activation on a new agent session with the original setup tab retained. Record actual `harness/setup-postlock-evidence.json`; Human personally runs `python harness/common/setup_lifecycle.py finalize --post-lock-evidence harness/setup-postlock-evidence.json` in an independent interactive terminal, with confirmation. Leave defects BLOCKED and preserve recovery access.
10. **Handoff.** Only after post-lock validation, report DONE/READY_WITH_LIMITATIONS and what was truly tested. Provide the single kickoff prompt calling Planner to read approved CRITERIA and create/revise `docs/IMPLEMENTATION_PLAN.md` (**GOALMAP is inside this Plan, not CRITERIA; each Plan section starts with user-observable GOAL**), then Milestones. Human approves plan before Tasks and coding.

**Safe upgrades:** never overwrite product or customized harness files as a side effect of reinstall. Use the source-file hash manifest and an explicit `--upgrade` preview. A file modified since the prior install is CONFLICT and requires manual reconciliation. Use `harness/common/recover.py` from an independent terminal for exceptional hook repair; it must back up affected files and request explicit human confirmation. Both tools are coordination and integrity checks, not OS sandboxing or authenticated approvals.

---
## For AI agents: mandatory instructions

### Your role

You are the **Environment Architect**. Your job is to inspect, propose and, after authorization, configure the coding-agent environment in the **target project**. You are not its Product Planner and must not invent features, roadmaps, milestones or development tasks, or write product code during bootstrap. Do not modify this bootstrap repository while setting up another project.

Planner owns product discovery and CRITERIA. **Technical Advisor** independently advises the human: CRITERIA determines what is wanted; relevant existing architecture, environment and limited source can be read when needed to assess feasibility, prerequisites, complexity/cost and ripple effects. Advisor never reviews Plan/Code quality, issues PASS/FAIL or vetoes. It advises on the whole draft before initial approval, or the settled delta just before any approved CRITERIA edit. **Optional tier comparisons are allowed**, used only where real choices exist. Human decides; Planner writes the authorized theory.

Planner handles product content in two modes: **Discovery**, brainstorming and researching with the user while recording unresolved theory as `OPEN` in CRITERIA; and **Delivery**, deriving approved goals, milestones and tasks. Bootstrap only installs the necessary environment.

### Canonical template structure

Only [`project-template/`](https://github.com/thebimhouseinfo-sudo/bootstrap/tree/main/project-template) is the installation source. Copy its **contents** into the target project's root, not into an extra nested directory, and only after inspecting existing files and obtaining the required authorization.

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

### Setup reference (not another sequence)

Use the ten-step **Single authoritative first-install workflow** above. `--ask-first` prints the one-batch intake questions; use the installer preview and staged apply exactly as described there. When in doubt, do not start coding, mark host-specific checks UNVERIFIED and request missing evidence. The configuration table below describes artifacts, not an additional Step 0–5 process.

| Artifact | Target | Purpose |
| --- | --- | --- |
| `AGENTS.md` | Project root | Agent operating contract |
| `.agents/skills/*` | Runtime-native skill paths | Reusable skills, host registration when supported |
| `harness/specs/*` | `harness/specs/` | Contracts; NOT_CONFIGURED components are not functioning tools |


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

**STATE (always local, including in `tracked` mode):** `harness/chat-journal.jsonl`, `harness/decisions.jsonl`, `harness/approvals.jsonl`, `harness/state.json`, `harness/last-block.json`, `harness/inbox.html`, `harness/snapshots/`, `harness/requests/`, `harness/recovery-backups/`, `harness/setup-state.json`, `harness/setup-live-evidence.json`, `harness/setup-postlock-evidence.json`, `docs/TRACE.md`, and `.claude/settings.local.json`.

The approvals ledger remains specific to **one Human**. Multi-person approval authentication or synchronization through Git is not supported. Product documentation such as `docs/CRITERIA.md`, `ARCHITECTURE.md`, `MILESTONES.md`, and `BACKLOG.md` remains trackable in either mode.

```bash
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --staged
python install.py --target PATH --tier Standard --runtime codex --config-git tracked --staged --apply
# To switch modes, add --change-config-git to both preview and --apply
```

The managed `.gitignore` block keeps its existing `BEGIN/END` markers and adds `# mode: local|tracked` inside. Legacy blocks without a `# mode:` line are treated as `local`; running `--apply` updates the marker block without requiring a migration. Changing modes without `--change-config-git` is blocked as `MODE_CHANGE_REQUIRES_APPROVAL` (exit 2). Preview the change and get Human approval before applying.

The installer checks the real Git index (`TRACKED_LOCAL_SETUP` in `local` mode or `TRACKED_LOCAL_STATE` in `tracked` mode) and effective ignore rules with `git check-ignore` (`LOCAL_SETUP_NOT_IGNORED` / `LOCAL_STATE_NOT_IGNORED`). These checks never automatically delete files or change the index. **Note:** `--apply` updates `.gitignore` before verifying nested ignore exceptions, so a BLOCK at that point leaves `.gitignore` updated but copies no template files. Because Git cannot re-include individual children of a fully ignored parent directory, `tracked` mode ignores specific STATE paths rather than using a blanket `/harness/` rule.

The legacy `-y/--yes` flag is accepted but **ignored**; only `--apply` writes. New installs must use `--staged`; an unstaged legacy invocation emits `WARNING_UNSTAGED_INSTALL`, but stays available for compatibility. Projects without Git should recheck effective ignore rules after `git init`. In the Bootstrap repository, `project-template/` remains versioned distributable source; the managed block is generated only in target projects.

### Installer upgrades and recovery

A successful install saves `harness/.bootstrap-manifest.json` with the installed file hashes (schema version 1). Preview `--upgrade` only after inspecting this file: unchanged tracked-by-manifest files can be replaced, edited target files stay `CONFLICT`; this is not an automatic project migration. Unexpected copy/apply failures attempt a hash-aware rollback of added files, staged state, and managed `.gitignore`, reporting any concurrent-change cases requiring manual intervention. A legacy install with no manifest must be reconciled manually. Hook recovery for Codex, Claude and Antigravity is available as `python harness/common/recover.py --runtime RUNTIME inspect|disable|restore`; `disable` and `restore` need a separate interactive OS terminal and keep a backup under `harness/recovery-backups/`. This is manual coordination, not an OS permission boundary.

## License

MIT. See [LICENSE](../LICENSE).

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
