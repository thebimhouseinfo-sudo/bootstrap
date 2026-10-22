# Bootstrap — instructions for AI setup agents

[Vietnamese](../README.md) | [English](user-guide.en.md) | [**For AI**](FOR_AI.md)

**Source of truth:** `../project-template/` is the distributable canonical template. This guide instructs the **Environment Architect** during bootstrap; the installed `AGENTS.md` controls normal product work. Follow the staged workflow below. The installer does not automatically research product requirements, approve theory, or guarantee native hook activation.

## Short-prompt entrypoint

User Guides intentionally provide exactly **two short prompts**: **greenfield (new project)** or **brownfield (existing codebase)**, both specifying only a target folder and a link to this guide. They are addressed to an installed coding agent that can inspect and operate on that folder, not a web-only reviewer. Treat the selected project kind and folder as authoritative intake, then **self-orchestrate the complete workflow below**; do not ask the Human to paste the workflow back into chat or enumerate steps. For a greenfield project with no product description, begin Planner Discovery by asking the Human about their idea **after safe preliminary installation**, not by inventing requirements. For brownfield projects, inspect the actual code and approved CRITERIA before asking what the Human wants changed. Gather genuinely missing choices through host-appropriate interactive UI after command permission: an IDE-native dialog, or a CLI-native numbered menu / verified interactive terminal wizard. Keep answers in the local intake trace; no freeform chat Q&A. The AI performs technical steps when tools and permission allow; it does not impersonate Human-operated terminal confirmation or fabricate host tests. If a new project's folder is absent, ask permission to create it before running the installer.

## Crucial host distinction: native Copilot, generic porting and Codex Cloud

**Native Copilot is now packaged.** For a new VS Code Copilot harness project choose `--runtime copilot`, never `--runtime generic --target-app copilot`. The native package includes `.github/agents/*.agent.md`, `.github/hooks/criteria.json` and Node.js hook scripts; follow `.github/COPILOT_SETUP.md`. Select the **Copilot** Session Target rather than the Local/Claude/Codex harness, verify Node.js and real hook dispatch. Do not treat a model selected inside Copilot as the current harness.

**Two required Criteria flows (same guarded write):** (A) absent/unapproved Criteria: Planner presents entire human-readable draft **in chat**; only if Human requests finalization does Planner stage a proposal and invoke `technical-advisor` as a real subagent. (B) existing Criteria: Planner discusses and settles add/remove changes **in chat**; only when Human requests update does Planner stage the complete resulting content and invoke Advisor on the delta. In both cases Advisor only advises. Planner presents the advice; a **new post-advice Human message** containing the nonce is needed; then `criteria-apply.cjs` applies exactly the unchanged staged contents. Direct edits to `docs/CRITERIA.md` are denied by observed preToolUse. If advisor dispatch or prompt events cannot be verified, **leave the file unchanged**; never fabricate a consultation or confirmation.

**Limit:** agent-controlled local receipt and supported tool interception do not authenticate Human identity or block every indirect shell/MCP route. Never claim a universal Criteria lock from script tests. The native host must be tested on a disposable project with allow/deny evidence.

**Standard is a tier, not a native hook promise.** A setup executed with `--runtime generic --target-app copilot` installs only portable role/skill sources, NOT a Copilot-native `.github/hooks/*.json` hook, and NOT an authenticated Criteria-change gate. An observed empty Hooks panel is consistent with the install. Never call a generic Standard project `HOOKS_ENFORCED` or pretend its Advisor handoff is an OS/host file-write restriction. Even Codex's packaged hook currently gives protected-Criteria warnings for recognized patches; it does not authenticate a Human decision or deny every possible write tool.

**Staged setup is not a protected Criteria-edit mode:** while `harness/setup-state.json` is in `BOOTSTRAPPING`, shipped Codex/Claude hook handlers defer blocking for installation/repair. Human/Advisor pre-write instructions still apply, but they are **not enforced by those staged hook handlers**. Never interpret a successful staged install, visible hook, or an `AGENTS.md` instruction as independent authorization to modify approved Criteria. If Human requires technical prevention during setup, stop and report the missing gate rather than editing the Criteria file automatically.

**Generic runtime — mandatory host-native port:** The installer copies reusable contracts because OpenCode, Qwen Code, Copilot, DeepSeek-based clients and other IDE/CLI hosts do not share one API. The **setup agent** must read `TARGET/.generic/ADAPTER_REQUIREMENTS.md` and `HOST_NATIVE_LAYOUT.md` plus referenced specs, inspect the actual host/version/harness, **rename/convert the host-facing `.generic` configuration to native directories and write/register native roles, skills and hooks**, and test supported allow/deny paths in a disposable project. This is part of the same installation workflow, **not something the Human must code**. `PORT_REQUIRED` means start porting, not finish setup. If a host lacks the needed API, cite actual evidence and mark that specific boundary `GUIDED_ONLY` rather than pretending an adapter exists.

**Before installing:** identify the **actual session harness**, not the chosen model name. For VS Code Copilot sessions, follow `project-template/.generic/platforms/copilot.md`: have the **setup agent** write the documented native role/hook port, verify registration, and test allowed and denied actions. For other generic clients follow the same host-native requirements, using their own official API. If a capability is genuinely unsupported or permission is unavailable, report the evidence and `CRITERIA_WRITE_GUARD_NOT_CONFIGURED` before protected edits. `READY_WITH_LIMITATIONS` must explicitly say `GUIDED_ONLY`, never imply the requested gate is present.

**Codex Cloud / no parallel chat:** The generic ten-step lifecycle assumes a fresh host session and a Human-operated independent terminal. When the Cloud task cannot provide either, **do not make up a new chat, fake fresh-session evidence or type the Human confirmation on their behalf**. In the existing task, use a disposable worktree/temporary copy for safe script smoke and invoke `python harness/common/setup_lifecycle.py host-test --surface codex-cloud`. Submit the exact observed checks plus limitations for Human review (e.g. a PR); native fresh-session dispatch, post-lock verification and authenticated Human gate remain `UNVERIFIED` until supported verification occurs. Do not label task-local smoke `READY` or `HANDOFF_COMPLETE`. This is a supported **limited verification path**, not an equivalent native hook test.

## Greenfield and brownfield contract

- **Greenfield**: the target has no established product code or approved theory. Planner calls `brainstorm-theory` and preserves all questions on intended users, real scale, deployment, trust, risk, future commitments and explicit non-goals. Do not invent scope or overengineer the first version. Use `challenge-feasibility` for uncertain technical dependencies; `write-criteria` turns Human decisions into readable theory.
- **Brownfield**: inspect existing source/tests/docs, protect Human-owned files and reconstruct verified **CURRENT** behavior independently of confirmed Human **DESIRED** behavior. Record gaps as OPEN; existing code alone never proves Human approval. `write-criteria` consolidates evidence and confirmed decisions without re-running irrelevant greenfield questions.
- **Both**: prepare a read-only proposed whole Criteria (initial finalization) or before/after delta (edits). When Human requests the actual file change, check whether Technical Advisor has advised on the exact proposal and Human decided afterward. If not, stop before the write, consult Advisor and return to Human; write only the post-advice authorized content. Advisor has neither veto nor approval authority. Never confuse a draft, pre-advice request or host permission dialog with final Human approval.
- **Multi-host**: each selected native adapter requires real-host verification. A primary staged lifecycle does not establish equivalent hooks on other selected hosts.

## Coding-agent execution and capability boundary

This Bootstrap is designed for an **installed coding agent** with project filesystem access and a shell/terminal execution tool (subject to host permissions), **not for a web-only document-review session**. In supported Codex/Claude Code/Antigravity host configurations, the agent should perform permitted shell operations itself: inspect the project, obtain a clean temporary checkout of Bootstrap, run `install.py` preview, and request consent before `--apply`. Do not send generic `git clone` / installer instructions to the user as routine manual prerequisites. Use the full local checkout of `project-template/`, not the limited content visible through GitHub web pages.

The raw `FOR_AI.md` URL is a lightweight **entrypoint** so the agent can read instructions before cloning; it is not the installation source. First check whether the host has command execution, network access, Git and permission to read/write the target folder. If the host requires command authorization, ask for it. If a sandbox blocks network or project filesystem access, explain the specific blocker and request the necessary host permission. If the current client fundamentally has no shell/filesystem tools (e.g. a web-only chat), **do not claim setup was performed**, and recommend using a supported coding agent in the actual project workspace. Human-only terminal confirmation for `activate`/`finalize` remains mandatory regardless of the agent's shell permissions.

**Multiple coding hosts:** select one primary host for the staged/hook-lock lifecycle and additional clients such as Codex and Claude Code. Repeat `--runtime` in selected order (e.g. `--runtime codex --runtime claude`); the first host remains primary during upgrades. Shared files install once, native adapters remain separate, and each host requires its own real-host verification. Never silently switch the primary or bypass Human approval.

## Mandatory setup intake UX: IDE dialog or CLI numbered menu

**Emit exactly ONE ordinary chat notification before the installer/tool permission request; it informs the user of the next interaction and contains NO questions.**

For English sessions:

> Bootstrap setup will request command permission first. **After permission**, read the configuration questions carefully: in an IDE they appear in a dialog; in a CLI they appear as numbered options in the terminal. Selecting 1/2 for a setup question is NOT granting tool permission. Your choices are recorded.

For Vietnamese sessions:

> Bootstrap sẽ xin quyền chạy lệnh trước. **Sau khi cấp quyền**, hãy đọc kỹ các câu hỏi cấu hình: trong IDE là dialog, trong CLI là các dòng lựa chọn đánh số ở terminal. Chọn 1/2 ở bước này là trả lời câu hỏi, KHÔNG phải cấp thêm quyền. Các lựa chọn sẽ được lưu để truy vết.

**After permission, choose input UI based on the actual host:**

- **IDE:** use the coding host's native structured question dialog if exposed. Record returned selections with `channel: "native_dialog"` and each response's `source: "native_dialog"`. Do not mistake a tool-permission dialog for a questionnaire.
- **CLI:** use the CLI coding host's own interactive numbered-choice selector/menu where supported. Record selections with `channel: "cli_menu"`, `source: "cli_menu"`, plus the available session/event reference. If it has no dedicated selector, use `python <BOOTSTRAP_CHECKOUT>/project-template/harness/common/setup_intake.py --preinstall --runtime RUNTIME --output <PRIVATE_TEMP_FILE>` in a **real interactive terminal with TTY**, **before the staged install**. The wizard prints numbered options and saves answers to an exclusive temporary file. Then run `install.py` using the explicitly selected `--tier`, `--config-git` and `--intake-file <PRIVATE_TEMP_FILE>`; the installer rejects contradictory choices and copies the trace into the project only during approved `--apply`. The agent may instruct the user to run this terminal command when the agent's shell tool is noninteractive; it may NOT silently synthesize answers or emulate a fake TTY.
- **Noninteractive environment:** if neither a host-native dialog/menu nor a real interactive terminal can be used, report `INTERACTIVE_INTAKE_UNAVAILABLE` and explain the limitation. Do not switch to chat Q&A or declare READY.

Trace must preserve non-secret choices in `harness/setup-intake.json` (project-local, ignored by Git) with actual source, question IDs and selections. Structured responses in the coding session or the terminal wizard are the provenance; the JSON schema is auditable but **not proof of identity**. Only ask what remains unresolved, and never infer that quickly pressing option 1/2 in a **permission dialog** has answered a configuration question. See `project-template/harness/specs/SETUP_INTAKE.md`. `install.py --ask-first` prints developer reference text only; it is not the questionnaire.

## Single authoritative first-install workflow

**Mandatory setup source:** Bootstrap must be available as a local checkout; `install.py` reads `project-template/` relative to itself, not from a GitHub page. Once the agent has the necessary command/network permission, the **agent itself** clones via `git clone --depth 1 https://github.com/thebimhouseinfo-sudo/bootstrap.git <temporary-checkout>` into a safe, separate folder **outside the target project**, or reuses a verified existing checkout. Inspect local files from that checkout. GitHub's `blob` URL is for a file; GitHub's `tree` URL is for a folder. For initial instructions, read `https://raw.githubusercontent.com/thebimhouseinfo-sudo/bootstrap/main/docs/FOR_AI.md`; the full installer cannot run from a raw-file URL alone. Do not rely on an unrelated web chat's ability to traverse GitHub directories to determine the coding host's capabilities. Preserve target project Git history and source.

**Tier prerequisite:** Standard or Full is required for the full Planner and Tester workflow. Lite is a lightweight, manually guided mode; do not promise autonomous Planner/Tester operation, hooks or approvals absent from its installed tier.

**Use this ONE sequence; the reference material below is not a second setup process:**

1. **Pre-notice → command permission → IDE dialog / CLI numbered menu.** Notify the user once, request only the needed command permission, then use the host-appropriate selection UI above. IDE-native dialogs and CLI-native numbered choices are both valid and traceable. When the CLI has no native selector, run the checkout `setup_intake.py --preinstall --runtime RUNTIME --output PRIVATE_TEMP_FILE` wizard in a real TTY **before installing**; consume its saved choices through `install.py --intake-file PRIVATE_TEMP_FILE` and matching `--tier`/`--config-git`. The short user prompt already defines project folder and new/existing status; only ask unresolved facts. Never use chat questions or treat a permission choice as a configuration answer.
2. **Preliminary staged install using the chosen configuration.** From the verified Bootstrap checkout, preview `python install.py --target TARGET --tier SELECTED_TIER --runtime RUNTIME --config-git SELECTED_GIT_MODE --staged --intake-file PRIVATE_TEMP_FILE` (or omit `--intake-file` only when an actual host-native questionnaire will produce a matching trace later; use `--target-app CLIENT` for generic). Never install a default tier and subsequently ask the Human to choose another one. The installer validates any provided trace against the CLI options; resolve contradictions before showing the diff and requesting authorization. Then rerun with `--apply`. `--staged` is mandatory for a first setup with blocking hooks; if it was omitted do not reopen a new agent tab before inspection. Never use an unstaged install merely to bypass this step.
2a. **Required native folder migration and port for `--runtime generic`.** After `--apply` and before modifying Criteria, read `TARGET/.generic/ADAPTER_REQUIREMENTS.md`, `HOST_NATIVE_LAYOUT.md`, `PORTING.md`, plus referenced hook/gate/approval specifications. **Change the active configuration directory from generic staging to the host's own discovery paths** (e.g. `.opencode/agents`, `.qwen/agents`, `.github/agents` for Copilot), moving/converting the relevant files. Retain `.generic` only as manifest-owned inactive source if deletion would break upgrades; do not leave its portable agents as the only configuration. Research the real IDE/CLI, generate compatible agent/skill/hook scripts and register them; run real-host positive and negative tests including bypass checks on a disposable copy. Record observed native adapter paths and evidence. Never stop at `PORT_REQUIRED` merely because no prebuilt adapter shipped; Environment Architect **implements it**. Mark a capability `GUIDED_ONLY` only after establishing the actual host limitation. Human approval/Advisor decisions cannot be authenticated from prompt text alone.
3. **CRITERIA Discovery and approval.** Check the existing CRITERIA status first. For greenfield: preserve `brainstorm-theory` scope discovery and research with Human. For brownfield: inspect actual behavior, tests and source; distinguish CURRENT, DESIRED and GAP before proposing revisions. When Human asks to finalize an initial CRITERIA or edit an existing one, invoke Advisor **just before writing** if advice for the exact proposal and a subsequent Human decision are not already present. Never treat the pre-advice instruction to write as post-advice approval.
4. **Technical direction.** After CRITERIA approval, recommend an appropriate stack/architecture for new projects or compatible continuation/refactor options based on existing code. State tradeoffs and regression risks. Human approves before changing the technical direction; record the selected HOW in ARCHITECTURE and PROJECT_PROFILE.
5. **Specialize Coder/Tester and complete audit.** Configure focused SDK/dialect/API knowledge, verified build/test commands, working Git branch policy, real host integration and regression procedure. Optional packs do not block generic agents. Run `python TARGET/harness/common/setup_lifecycle.py audit` and repair all mandatory gaps without weakening guards.
6. **Automatic smoke and recovery readiness.** Derive positive ALLOW and negative DENY cases for **installed** hooks/scripts; run `python TARGET/harness/common/setup_lifecycle.py smoke` and additional safe disposable fixtures. Verify isolated rollback/recovery and preserve existing product files. Do not mistake script PASS for native host hook evidence.
7. **Real fresh-session host verification (where supported).** Run `python TARGET/harness/common/setup_lifecycle.py host-test` for host-specific actions. **WARNING: NEVER CLOSE THE ORIGINAL SETUP TAB for local/IDE setup.** Keep it as the repair coordinator. Open a separate tab, perform safe positive tests and forbidden-action tests only in a disposable clone/worktree, and report precise logs/version. If BLOCKED, return to original tab or a verified offline recovery tool.
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
- **OpenCode, Qwen Code, DeepSeek-based clients, Copilot, Cursor, Cline and others:** Select `--runtime generic --target-app APP` to copy requirements. **In the same setup, the agent must create/register/test the actual native adapter** from `.generic/ADAPTER_REQUIREMENTS.md` and verified host documentation. A model/provider named DeepSeek is not necessarily the actual host; identify the harness. Do not label a capability unsupported merely because Bootstrap ships no universal prebuilt script.

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

Use the ten-step **Single authoritative first-install workflow** above. The user-facing setup intake is IDE dialog **or** CLI numbered menu; `--ask-first` is a developer reference, not interactive intake. For CLI fallback, run the `--preinstall` wizard **before** staged installation and pass its trace through `--intake-file`; legacy post-install invocation is only for a tier already correctly chosen. Continue to audit only after the recorded tier/Git choices match the installed manifest. When in doubt, do not start coding, mark host-specific checks UNVERIFIED and request missing evidence. The configuration table below describes artifacts, not an additional Step 0–5 process.

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

A successful install saves `harness/.bootstrap-manifest.json` with the installed file hashes (schema version 1). Preview `--upgrade` only after inspecting this file: unchanged tracked-by-manifest files can be replaced, edited target files stay `CONFLICT`; a tier/runtime change requires a reviewed manual migration; --upgrade refuses to mix adapters or role tiers. Unexpected copy/apply failures attempt a hash-aware rollback of added files, staged state, and managed `.gitignore`, reporting any concurrent-change cases requiring manual intervention. A legacy install with no manifest must be reconciled manually. Hook recovery for Codex, Claude and Antigravity is available as `python harness/common/recover.py --runtime RUNTIME inspect|disable|restore`; `disable` and `restore` need a separate interactive OS terminal and keep a backup under `harness/recovery-backups/`. This is manual coordination, not an OS permission boundary.

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

### Generic adapter setup flow — the agent writes the native scripts

After staged generic installation, **read `.generic/ADAPTER_REQUIREMENTS.md` plus `.generic/HOST_NATIVE_LAYOUT.md`, migrate/rename active `.generic` configuration into documented host-native directories, and implement the native files** using the actual host's documented APIs; don't ask the Human to implement them. Perform native positive/negative checks before claiming readiness; record actual `native_adapter_paths` when tested. Continue with Criteria only under its separate Advisor/Human approval rule. Truly unsupported surfaces may remain `GUIDED_ONLY`.

Collect unresolved choices through the **IDE's native dialog or CLI's interactive numbered menu** (with the bundled TTY wizard when needed). `python install.py --ask-first` is a developer-only reference, not the survey. With the Human's answers, preview `python install.py --target PATH --tier Standard --runtime generic --target-app qwen-code` and use `--apply` only after approval. `.generic/` supplies portable role contracts and host porting instructions; it does **not** automatically register untested native agents. Continue receives the same shared `.agents/roles`, `.agents/skills`, and `harness/common` content as Antigravity, but uses `.continue/` for its native agent/model configurations; Antigravity `.agents/hooks.json` is not copied into Continue.

## Planner skills (mandatory)

The Planner must invoke `.agents/skills/challenge-feasibility/SKILL.md` to challenge new capabilities with evidence and classify feasible / unknown / infeasible before making commitments. It uses `.agents/skills/write-criteria/SKILL.md` to write the *human-readable product theory*, never a disguised architecture or technical task plan. These skills do not alter the restricted Advisor activation gate.

When the CLI wizard records `runtimes`, pass the same ordered repeated `--runtime` flags to the installer. Do not silently pick one host after the human selected multiple. Host-native menus must record the same ordered list. For existing installs, keep the primary host first. Shared source and state remain single-project; each native hook adapter needs independent real-host verification.
