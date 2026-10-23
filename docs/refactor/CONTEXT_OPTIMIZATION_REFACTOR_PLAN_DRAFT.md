# Bootstrap — Unified Context & Hybrid Harness Upgrade Plan (Draft v3)

**Status:** DRAFT — awaiting Planner/Reviewer review and Human approval  
**Repository:** `thebimhouseinfo-sudo/bootstrap`  
**Document authority:** Single consolidated upgrade plan; supersedes the previous Context Optimization Refactor Plan v2 **in this same file**.  
**Scope:** context efficiency, Lead/Worker execution profiles, host-native enforcement, delegated workspaces, multi-model worker execution, testing and benchmarking.  
**Criteria:** Existing approved project Criteria remain unchanged. **This document is not approval to implement, merge implementation code, or deploy.**

## 1. Problem and desired operating model

Bootstrap must work for cloud and local coding hosts concurrently, across several projects:
- Cloud Codex may plan, review, independently test, **and code**. It is not restricted to governance roles.
- Local QwenCode (primarily Qwen ~27B on MacBook Pro M1 Max 64 GB; other available models/hosts may be used) may implement delegated tasks without waiting for cloud usage to refresh.
- Codex and QwenCode may work on **different branches/worktrees/projects** simultaneously. A cloud outage or usage exhaustion must not stop independent, already-authorized local tasks.
- Cloud usage efficiency and local **end-to-end completion time** are separate optimization objectives.
- Stronger API models may later be assigned to Worker tasks/roles; do not hardcode model quality, host, or role assignment.

Use a **senior/junior delegation analogy** but name the architecture **Lead Harness** (project-level authority) and **Worker Harness** (task-level authority). These are **execution profiles**, NOT Lite/Standard/Full installation tiers and NOT fixed labels for Codex/QwenCode.

## 2. Two authority scopes

### Lead Harness — Project scope
- Source of truth: approved **Project Criteria**, Project Goals, Plan, Milestones, governance and integration permissions.
- Assigns work, chooses host/model, prepares task contract and isolated workspace, reviews evidence and controls integration according to existing approval gates.
- Supports Planner, Technical Advisor (only under existing invocation rules), Coder, Tester and Reviewer; role availability is task-dependent.

### Worker Harness — Delegated task scope
- Source of truth for work: **Task Criteria**, **Task Goals**, precise implementation instructions, test plan, scope and assigned worktree/branch from Lead.
- Task Criteria/Goals are *derived subordinate contracts*, not a competing Project Criteria file or authority to alter project goals.
- Worker retains **Coder, Tester and Reviewer**, including native hooks and task-level self-verification/review; omission of project-level Planner, Technical Advisor and strategic brainstorm reduces irrelevant overhead.
- Worker Coder may reason about local implementation details and report contradictions/blockers; may not rewrite the parent contract, project approvals, scope, governance, or integration authority.
- Task-level Worker Tester/Reviewer checks do **not** replace independent Lead verification when required.

**Important:** Not every QwenCode session must behave as Worker; a profile is assigned per workstream. Codex may perform Coder work while QwenCode codes a different task.

## 3. Delegation contract, workspace and lifecycle

Lead prepares **before Worker launches**:
1. Approved source links/IDs (Project Goal/Criteria/Milestone and decision references).
2. Task Goals and Task Criteria with explicit acceptance cases, non-goals and failure reporting.
3. Implementation instructions; interfaces, dependencies and expected file areas.
4. Task branch + isolated Git worktree (from a recorded base commit); reserved ownership of files.
5. **Writable allowlist**, read-only shared contracts, forbidden governance/harness paths; safe commands and tests.
6. Evidence/report schema, integration rules and escalation path.
7. Known limits (e.g. available local model, tool and shell capabilities).

Example logical contract (format/schema to finalize during M2):
```yaml
task_id: TASK-014
parent: {goal: G-3, milestone: M-2, criteria_ids: [C-7]}
profile: worker
workspace: {branch: worker/TASK-014, base_commit: "<sha>", worktree: "<assigned-path>"}
task_goal: "Implement defined endpoint behavior"
task_criteria: ["Defined valid input succeeds", "Invalid input is rejected"]
writable: ["src/feature/**", "tests/feature/**"]
read_only: ["docs/CRITERIA.md", "docs/IMPLEMENTATION_PLAN.md"]
forbidden: ["harness/**", ".codex/**", ".github/workflows/**"]
checks: ["<actual project test command>"]
report: [changed_files, diff_reference, tests_executed, test_results, unresolved_issues]
on_blocked: report_to_lead
```
All values above are illustrative, not a deployed format or real command.

Lifecycle: `PREPARED → ASSIGNED → IMPLEMENTING → SELF_TESTED → SUBMITTED → LEAD_REVIEW → ACCEPTED / REWORK / REASSIGNED`, with `BLOCKED` for genuine inability to continue. A Worker **never self-assigns ACCEPTED**, merges to protected branches, or invents Human/Reviewer approval.

Lead reviews actual diff and runs independent tests when required. FAIL produces specific findings → Worker repair → retest → review. Repeated or serious failure may cause tighter task subdivision, better instructions, model escalation, or reassignment. Lessons Learned must distinguish capability limits from vague instructions, missing tests, dependency issues, and environment failures.

**Isolation caveat:** A branch/worktree alone does not sandbox filesystem access or arbitrary shell commands; writable allowlists need host-native permission/hook checks or stronger OS isolation where appropriate. Do not claim policy text is technical enforcement.

## 4. Native hooks and shared enforcement

- Codex hook configuration is not QwenCode CLI enforcement.
- QwenCode may use its **own native hook and permission integration**, with Worker-specific task rules. Determine actual supported hook events, denial semantics, shell/tool coverage and bypasses on the installed version by real-host testing.
- Prefer reusing existing shared enforcement/checker logic where compatible, **not copying or replacing Codex hooks**.
- Guard branch, worktree identity, paths, dangerous Git operations, protected governance/configuration files, and scope. Protect across write mechanisms as far as actually supported.
- A read-only rule in a Markdown prompt is *behavioral guidance*, not a sandbox. Explicitly report enforcement gaps.
- Worker cannot weaken its own guards or edit host configuration/harness infrastructure in ordinary delegated tasks. Exceptional authorized harness-development work must use separate authority and a specifically approved workspace/contract.
- Never duplicate hook registration blindly when installing multiple hosts. Verify interaction with any existing native hooks.
- Keep `harness/common/branch_authority.py`, snapshot, recovery, and verification contracts intact unless an explicitly reviewed implementation is necessary. Preserve existing approval and branch authority rules.

## 5. Minimal Useful Context — scoped to active profile, phase, role and task

**No universal metadata catalog.** An inactive role's skills, tools, harness instructions and names are not automatically discoverable to the active agent.

| Context category | Policy |
| --- | --- |
| Universal Core | Full preload; only mandatory small shared rules and routing |
| Active role/phase | Full instructions necessary now |
| In-scope specialized skills/tools/instructions/harness | Precise metadata (name, description, activation condition, path) then full on activation |
| Out-of-scope components | **Not loaded, not even metadata** |
| Knowledge, source, tests, logs, diffs | Targeted on-demand reads |
| Session handoff | Compact task state + links to canonical evidence, not copied history |

- Apply scope to roles, skills, tools, knowledge **and model-facing harness instructions**. Executable hook/Python files on disk are not automatically model context.
- Universal skill candidates must be proven broadly shared and worth preloading. Split a large candidate into universal core + optional extension.
- Worker normally sees Coder/Tester/Reviewer capabilities for the current task, not Technical Advisor, project Criteria drafting or brainstorm skills.
- Cross-role interfaces are short contracts, not the receiving role's entire skill set.
- **Host limitations:** Tool schemas, native skills and earlier chat turns can be injected/retained independently of Bootstrap. Audit, do not promise control where unavailable.
- Use host-native skills/discovery/role settings first; fallback to small scoped metadata manifests only for hosts lacking the needed behavior. Avoid new global loader, proxy service, RAG or cache by default.

## 6. Worker execution strategies

### Default — Direct task implementation
Coder implements scoped task, performs self-checks; Worker Tester and Reviewer inspect behavior/diff within task scope; submit to Lead. Suitable for a small fix or well-bounded task.

### Optional — Architecture-first, contract-driven implementation
For suitable multi-module/job-pack work:
1. Lead defines task objective/criteria and interfaces/dependencies.
2. A capable model (e.g. local 27B) creates **system-wide skeleton**: module boundaries, signatures, data contracts, integration seams, test scaffolding and incomplete portions explicitly marked.
3. **Early skeleton validation**: basic parse/build, interface compatibility, dependency and test-fixture sanity.
4. A smaller model fills **well-defined, narrow modules** based on stable skeleton contracts; each module gets its own writable scope and unit tests.
5. Capable model integrates modules; Worker Tester and Reviewer verify contract/integration.
6. Lead independently reviews and accepts/reworks the delivered task.

This is **horizontal architecture setup before detailed fill**, not blindly finish every feature vertically. Test at skeleton, module and integration boundaries—never wait until everything is filled to detect interface mistakes.

Do not require this pipeline for trivial changes. On a single M1 Max, sequential model switching may outperform simultaneous inference due to memory/bandwidth and model reload costs; benchmark before enabling parallel local models. If small-model rework exceeds savings, revert to direct 27B coding. No fixed task-complexity threshold without evidence.

## 7. Relationship to existing installation tiers

Current repository `harness/specs/TIER_MANIFEST.json` contains **Lite / Standard / Full** as *installation/feature tiers* with existing requirements. These must **not** be renamed to Lead/Worker or silently repurposed.

Add profile-aware setup **orthogonally**:
- Existing installation tier answers *what shared files/capabilities are installed*.
- Lead/Worker execution profile answers *who owns what responsibility, what context is loaded, and what scope/authority applies*.
- Host adapter selection answers *which native integrations are installed/verified*.

A project may have Codex Lead and QwenCode Worker installed together without two independent sources of project authority. Check the existing multi-host installer for ownership/conflicts; do not assume it already supports QwenCode or scoped Worker provisioning.

## 8. Upgrade milestones

### M1 — Read-only code/runtime audit and baseline
Inspect actual installer, host adapters (including missing QwenCode support), native hook behavior, tiers, context entrypoints, task/branch state and multi-host conflicts. Establish baselines on user-relevant workflows using Codex and QwenCode local ~27B (Continue/Gemma optional comparison): context loaded, prompt processing, generation latency, tool calls, total task time, test quality, cloud usage, and task completion. Distinguish measurements from assumptions.

**PASS:** Reproducible evidence and gap matrix, including verified native enforcement limitations; no code refactor needed to establish baseline unless measurement infrastructure is separately reviewed.

### M2 — Design approval: profiles, delegation and context scopes
Finalize Lead/Worker responsibility and authority map; parent Project Criteria ↔ Task Criteria/Goals traceability; task schema; role/skill/instruction/tool/harness dependency matrix; Universal Core candidates; hook policy; worktree/branch ownership; acceptance and lessons taxonomy. Review compatibility with existing tiers and contracts.

**PASS:** Every Worker permission and dependency mapped; no invented project-level governance or conflicting source of truth; implementation design reviewed.

### M3 — Profile-aware setup and safe workspace provisioning
Implement profile selection and host-specific config only where needed. Lead may prepare independent Worker branch/worktree and task contract; QwenCode native hooks/permission rules enforce task scope to the verified extent. Reuse shared enforcement and skill files; no duplicated or overwritten Codex hook config. Keep Codex able to code. Implement role-scoped metadata/full loading according to real host capabilities.

**PASS:** Dual-host setup usable without configuration conflict; Worker cannot silently modify protected paths through tested write surfaces; actual gaps documented, no false guarantees.

### M4 — Worker Coder/Tester/Reviewer and reliable delegation
Implement task intake, scoped coding, unit/regression testing, Worker review, evidence and submission; Lead independent review/rework/reassignment; blocked handling, compact handoffs and resume. Different branches/worktrees allow concurrent nonconflicting work. Project governance unchanged.

**PASS:** End-to-end delegated task with real diff/test evidence, FAIL→fix loop, protected integration, and continuation of approved Worker tasks when Codex unavailable.

### M5 — Optional multi-model execution experiment
Implement or prototype 27B skeleton → smaller model module fill → skeleton/module/integration checks → Worker review. Use a representative job pack and include direct-single-model comparator; do **not** force this path for every task.

**PASS:** Evidence of reduced *total* task time and acceptable correction/test rate on at least one representative task class; otherwise leave strategy optional/disabled without blocking basic Worker capability.

### M6 — Full regression and performance evaluation
Test greenfield/brownfield Bootstrap, Criteria approval, Technical Advisor activation rules, Planning, Codex Coder, QwenCode Worker, native hooks, scope violations, multi-project parallel branches, cloud usage exhaustion, handoffs, independent Tester/Reviewer, task repair and lessons learning. Measure cloud usage per delivered task; local end-to-end time; model-switch overhead; correctness and regression rates.

**PASS:** No regressions in governance/authority; measurable context/usage or time gains; no extra gates invented. Exact optimization threshold set only after baseline and human review.

Each implementation milestone contains real independent verification, evidence, and existing tester→bug-fix→retest behavior. Approval checks remain those of the **existing** Bootstrap Criteria/process; this plan does not create a new advisory gate.

## 9. Non-negotiable invariants and risks

1. Approved Project Criteria, Human authority, existing Technical Advisor trigger, branch permissions and approval gates remain intact.
2. Worker Task Criteria/Goals are subordinate, traceable and immutable by Worker unless Lead reissues the contract.
3. Worker has its own scoped Coder, Tester and Reviewer; Worker PASS is **not** final Project acceptance.
4. Lead/Codex may code; Worker assignment is not synonymous with local model or reduced capabilities.
5. Separate branch/worktree and explicit writable scope for delegated work; protect shared state. Existing `active-task.json` may assume one task per checkout—investigate before parallelization.
6. Do not silently relax hooks or claim Codex hooks protect QwenCode.
7. Optimize **total throughput and correctness**, not token count in isolation.
8. Keep only one **canonical upgrade plan file**; avoid separate competing context/worker/multi-model plans.
9. Lessons Learned should tune delegation scope, instruction detail, test quality and future model assignment; never conflate tool faults with model weakness.
10. Preserve original installation tier labels until independent, explicit criteria change is authorized.

## 10. Immediate next step and stop condition

Review **this single draft** against source and operational constraints, then perform M1 audit. Do not begin M3 code work merely because this document was saved. Revise milestone design based on measured evidence, pass Reviewer and obtain normal authorization before coding.

**Recorded decision:** One unified plan, Lead/Worker profiles, full native controls per host where verified, scoped Task Criteria/Goals, senior-prepared isolated workspaces, Worker Coder/Tester/Reviewer, minimal role-scoped context, optional 27B-skeleton/small-model fill, and cloud/local parallel continuity.
