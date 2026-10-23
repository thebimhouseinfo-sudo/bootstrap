# Bootstrap — Context Optimization Refactor Plan v2

**Status:** DRAFT — pending Planner/Reviewer review and Human approval  
**Repository:** `thebimhouseinfo-sudo/bootstrap`  
**Baseline:** `main` at `16dcd9dacab372fd63d868f5c49f1dac424369f9` (planning reference only)  
**Scope:** Context loading, discovery, role/phase/task routing, host integrations, handoff, and measurement  
**Criteria:** Unchanged. This draft is not an authorization to implement, merge, or deploy.

## 1. Purpose

Reduce irrelevant model context while retaining enough information to select the right capability, follow existing contracts, and complete the active task. Do **not** equate on-disk files with model-loaded context. Do **not** reduce tokens by omitting mandatory safety/approval/authority rules.

Guiding principle: **Minimum Useful Context**, scoped to **active phase + role + task + host + required dependencies**.

## 2. Context tiers

| Tier | Loading rule | Examples |
| --- | --- | --- |
| Universal Core | Preload full, kept small | Mandatory cross-role rules, active-state identification, context routing, basic authorization invariants |
| Active Context | Load full on activation | Current role instruction, active phase instructions, directly required task skills/contracts |
| Discoverable Context | Metadata only **within active scope** | Relevant skill/tool/instruction/capability name, precise description, activation trigger, path |
| Out-of-Scope | **Do not load, including names and metadata** | Tester skills during initial Setup, Coder skills during Planner work unless a genuine dependency exists |
| Evidence/Knowledge | Retrieve on demand | Targeted project source, logs, diffs, tests, references |

Universal is an evidence-based classification, not a permanent label for popular files. Candidate universal skills must be frequent across roles, genuinely shared, and cheap enough to preload. If long, split the universal core from task-specific extensions. Do not pre-classify `safe-change`, `report-evidence`, or `context-reload` without audit.

## 3. Scope-driven routing

Routing inputs: host, lifecycle phase, active role, active task, project state, verified dependency, and approval/branch state.

1. On startup load only Universal Core, minimal active project state, and routing.
2. Activate current phase and role instructions; do not load other roles.
3. Expose **only** relevant capability metadata inside this active scope.
4. Load full skill/instruction/harness contract when the task actually needs it.
5. Fetch focused code, knowledge, logs, and evidence only when necessary.
6. On role/task/session transition, hand off compact state and references. A host may retain earlier conversation context; do not claim the router can delete it.

Important: **cross-role handoff contract is not full cross-role context**. Planner needs to produce Tester-verifiable acceptance criteria; it does not need the Tester skill index. Tester needs a clear bug report contract; it does not need Coder implementation guidance.

## 4. Per-component loading policy

### Skills
- Universal: full preload only after audit.
- Specialized: metadata only if inside active role/task scope; full `SKILL.md` on activation; supporting files on demand.
- Outside scope: no metadata.
- Descriptions must express *when to invoke*, purpose, exclusions, and discoverable path without embedding the complete workflow.

### Instructions and roles
- Separate universal, phase, role, task, and host-specific instructions.
- Only universal + active instructions are full-loaded.
- No default broad index of inactive roles.

### Harness
- Distinguish **executable harness source** from **model-facing harness contracts**. Python/hook code residing on disk does not itself consume model context.
- Runtime enforcement runs independently of model instruction selection.
- Discover only active-role capabilities; read contracts when activated.
- Preserve `branch_authority.py`, snapshots, recovery, verification, and existing approval gates.

### Tools
- Distinguish Bootstrap-owned capability metadata from host/MCP-exposed tool schemas.
- Only scope Bootstrap's catalog to active role/task. Do **not** claim host-level schemas are hidden until verified for that host.
- Do not add proxy tools or duplicate native discovery without a demonstrated need.

### Knowledge and evidence
- Discover topics/files only when relevant.
- Retrieve narrow sections, source diffs, specific tests and logs rather than entire repositories or full test archives.

## 5. Illustrative scope matrix (audit must validate)

| Active phase / role | Full | Metadata only | Not loaded |
| --- | --- | --- | --- |
| Setup | Universal + setup instructions | Setup capabilities | Coder/Tester/Reviewer skills |
| Criteria / Planner | Universal + Planner, active criteria/plan contract | Planning, criteria, research capabilities | Implementation/debug/test skills |
| Technical Advisor | Universal + Advisor, applicable advisory contract | Feasibility and research capabilities | Coding/test details |
| Implementation / Coder | Universal + Coder, active work contract | Implementation/debugging capabilities | Setup/Planner/Tester-only details |
| Testing / Tester | Universal + Tester, active test contract | Verification/evidence capabilities | Criteria-writing and Coder-only details |
| Review / Reviewer | Universal + Reviewer, active review contract | Review/impact/evidence capabilities | Unrelated phase details |

A capability may have multiple legitimate owners; scope by actual dependencies rather than a rigid one-role-per-skill assumption.

## 6. Host strategy

**Native first:** Inspect native skill discovery, activation, role configuration, instruction autoload, tool-schema exposure, hooks, and project file conventions.

**Fallback only where required:** Per-role metadata index + targeted file reads. Avoid globally preloading all capabilities.

Host coverage for investigation: Claude Code, Codex, GitHub Copilot, Continue, Antigravity, and generic host contracts. Actual native capability support is **unverified until tested**. Differences between adapters are not automatically design bugs.

## 7. Milestones and gates

### M1 — Audit and baseline (FIRST; no functional refactor)
- Inventory skills, instructions, roles, harness files, metadata, host adapters, and real entrypoints.
- Classify each as auto-loaded, explicitly read, runtime-only, or unknown **per host**.
- Trace duplicate instructions actually visible in the same model context.
- Measure baseline startup/task context (tokens when available; transparent proxy otherwise), file reads, latency, and tool calls.
- Test representative Setup, Planner, Coder, Tester/bug-fix flows.
- **Pass:** Reproducible inventory, host evidence, measurement methodology, and baseline; unknowns labeled.

### M2 — Dependency and classification
- Create phase → role → task → component matrix.
- Document universal candidates with frequency, shared use, size and safety evidence.
- Define minimal metadata schema (id, type, description, activation conditions, path, scope, dependencies).
- Identify mandatory cross-role handoff contracts.
- **Pass:** Each visible capability is justified for that scope; required dependencies remain reachable.

### M3 — Routing and progressive disclosure refactor
- Reduce startup instruction footprint without deleting mandatory protections.
- Implement role-scoped discovery; specialized skills and instructions metadata-first.
- Full-load only activated components; host-native mechanisms preferred.
- Add host-specific fallbacks only when necessary and verified.
- **Pass:** Setup does not receive Coder/Tester catalog; Planner does not receive unrelated coding skills; active tasks still resolve correct instructions/capabilities.

### M4 — Handoff and reload
- Define compact persisted state: project, goal, phase, role, task, branch, approval, blockers, evidence references.
- On new session / role switch, reload only active context and task dependencies.
- Avoid copies of entire history; respect host limits on context removal.
- **Pass:** Fresh-session continuation works without missing approvals or duplicating prior work.

### M5 — Benchmark and regression
- Compare before/after on greenfield Setup, brownfield bootstrap, Criteria, planning, coding, testing, bug-fix loop, Advisor activation, role switching, and session handoff.
- Measure startup and phase context, file-read count, repeated reads, latency, tool calls, discovery/selection accuracy, completion accuracy, and enforcement regressions.
- **Pass:** Measurable benefit without loss of correctness or required controls. Do not invent a percentage reduction threshold before M1.

Every milestone requires independent Tester evidence and uses the existing bug-fix loop on FAIL. No extra approval gates introduced by this optimization.

## 8. Non-negotiable invariants

- Approved Criteria stay unchanged unless Human explicitly requests a criteria change through the established process.
- Preserve Human approvals, Technical Advisor triggering rules, branch authority, snapshot/recovery/verification, and Planner → Coder → Tester → Reviewer workflow.
- Distinguish instruction-based behavior from independent runtime enforcement.
- No assumption that all Markdown files load, or that native hosts can unload already-inserted conversation tokens.
- No unconditional global skills/tools metadata list.
- No caching, vector DB/RAG, new router service, or large abstraction without benchmark evidence.
- Never hide a necessary safety rule behind a task-specific lazy-loaded skill.

## 9. Risks / verification points

- Overgrown Universal Core → measure and split.
- Incorrect discovery description → capability-selection tests.
- Omitted dependency → end-to-end role-task mapping and handoff tests.
- Host injects tool schemas automatically → record unavoidable overhead separately.
- Lazy-loaded safety contract → retain independent enforcement and minimum core instruction.
- Token savings displaced into extra reads/tool calls → compare total effort/latency.
- Cross-session state gaps → explicit minimal handoff and evidence references.

## 10. Review and execution policy

This file is a **planning draft**. Reviewer must challenge technical feasibility and host-specific assumptions before approval. Complete M1 and revisit M2/M3 implementation details against measured evidence. No code, Criteria, merge, deploy, or runtime behavior is changed by creating this file.

**Next authorized action within planning:** review this draft and execute read-only M1 audit once requested.
