# Bootstrap — Unified Bootstrap Upgrade Plan — Context, Decision Fidelity & Pre-Code Design (Draft v4)

**Status:** DRAFT — awaiting Planner/Reviewer review and Human approval  
**Repository:** `thebimhouseinfo-sudo/bootstrap`  
**Document authority:** Single canonical upgrade plan, updated in place. This v4 consolidates v3 with the accepted discussion, decision-fidelity, Coder/Reviewer and anti-overengineering design directions. Do not create competing context, discussion, coding or harness plans.  
**Scope:** context efficiency; optional Discussion Job and Secretary decision preservation; decision-referenced planning; Coder domain boundary; pre-code per-Task code-structure proposals and cross-Task Reviewer optimization; complexity escalation; Lead/Worker execution profiles; host-native enforcement; delegated workspaces; multi-model worker execution; testing and benchmarking.  
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

This is **horizontal architecture setup before detailed fill**, not blindly finish every feature vertically. **It begins only after the pre-code Code Structure Proposal has passed Reviewer.** A runnable source skeleton in this optional implementation strategy is not the pre-code proposal: pre-code creates only a descriptive proposal artifact, never application source files. Test at skeleton, module and integration boundaries—never wait until everything is filled to detect interface mistakes.

Do not require this pipeline for trivial changes. On a single M1 Max, sequential model switching may outperform simultaneous inference due to memory/bandwidth and model reload costs; benchmark before enabling parallel local models. If small-model rework exceeds savings, revert to direct 27B coding. No fixed task-complexity threshold without evidence.


## 6A. Human decisions must survive discussions, Plan revisions and handoffs

**Problem:** Repeated chat/Plan rewrites have lost accepted domain-expert workflows, algorithms, implementation mechanisms, constraints and rejected approaches. The next Coder then improvises a generic replacement and over-engineers. A short Plan summary must not become a substitute for the original accepted decision.

### Optional Discussion Job and Secretary — no new gate

- A **Discussion Job** is an optional documentation workspace, **not** a required project lifecycle state, Project Criteria change, bootstrap requirement or approval gate.
- If Human explicitly requests to open/create a Discussion Job, open it directly. If Human only says they want to discuss, ask **once** whether to open a Discussion Job to preserve decisions. If declined, continue ordinary chat; do not auto-open, triage intent by AI complexity scoring, repeatedly ask, or require Discussion Job for ordinary questions.
- **Secretary** is a focused recording role/action active for such a discussion, not a continuously running autonomous agent. As soon as Human actually accepts a decision, Secretary records it promptly in the GitHub-backed project discussion area. Secretary must distinguish *accepted*, *proposed* and *unresolved*; do not infer acceptance from a suggestion or silently rewrite Human reasoning.
- Proposed folder layout: docs/discussions/DISC-001-topic/INDEX.md and separate DEC-001.md, DEC-002.md, etc. Exact naming/layout is subject to M2 source-fit review, but **stable discussion/decision IDs, index, traceability and preserved history are required**.
- Each accepted record preserves exact operational/business rules, domain mechanisms, necessary technical steps, why chosen, examples, thresholds, exceptions, dependencies, forbidden alternatives and rejection rationale, provenance and links to affected Goals/Tasks. Avoid summarization that loses causal detail.
- Corrections produce traceable supersession (e.g. SUPERSEDED_BY) while historical decisions remain readable. Do not overwrite history silently. Keep unresolved questions explicitly unresolved.
- A user may settle decisions outside Discussion Job; the Planner/Reviewer still must use the agreed source context. Do not invent a forced discussion session.

### Reference-based planning and decision fidelity

- Planner remains responsible for research, critical reasoning, challenge and feasibility analysis **before decisions are settled**. It may propose alternatives and flag contradictions, but it must not silently replace a settled expert solution while writing or revising a Plan.
- Detailed Implementation Plan, Goals, Task List and Milestones **reference stable accepted decision IDs/source links** rather than repeatedly rewriting their content. Plan describes scope, dependencies, ordering, responsibility, deliverables and observable tests.
- Planner checks decision **coverage, conflicts and feasibility**, not just textual similarity. A real conflict returns to Human with evidence and a specific proposal; do not label uncertainty as impossible or invent a new Advisor gate.
- Coder opens the **full referenced decision**, not a lossy summary, when implementing a relevant Goal/Task.
- Reviewer checks **Decision Fidelity** for both technical proposals and completed code. An implementation that passes tests but changes accepted business logic is not PASS.
- Project Criteria, existing Human-approval rules and Technical Advisor triggers remain unchanged. These mechanisms do not authorize editing approved theory.

## 6B. Coder responsibility and Pre-Code Preparation

**Role boundary:** Coder is a **Software Engineer, not a Domain Expert**. Its duty is to faithfully implement the Detailed Implementation Plan, Task List and referenced expert decisions. It makes ordinary software-engineering choices independently. It must not invent domain rules, real-world workflows, calculations, classifications or accepted host behavior.

### Solution clarification — one focused skill, only when necessary

Introduce the **solution-clarification** skill for Lead and Worker Coders. This is **Goal/Job-Pack-level** understanding, not a question gate per function.

- Before proposing code, read the Goal, all related Tasks, Decision references, project/host profile, existing source and actual caller/dependency surfaces as relevant.
- If baseline facts or **operational logic** are materially missing (e.g. target AutoCAD version, supported platform, active host vs offline file, read vs write), ask Human/Lead a concise question that changes the solution.
- If **domain/professional solution** is missing (e.g. how HVAC systems are classified, business exception/authoritative data), ask the domain expert. Explain choices in operational language; do not ask Human to choose routine libraries, frameworks or internal data structures.
- **If the documents already define logic and professional solution, DO NOT ask again.** Proceed with the technical response.
- Clarify substantial unjustified complexity when found, rather than silently expanding the system. Distinguish missing facts from optional engineering ideas. No extra brainstorm/approval session by default.
- Scope applies to software-only projects as well as CAD/BIM; the boundary is expertise and consequential solution decisions, not an HVAC-specific rule.

### Pre-Code artifact — descriptive Code Structure Proposal, NOT implementation

The Coder receives the **existing Detailed Implementation Plan/Task List**; it does not invent a separate Technical Implementation Plan, rewrite the Planner's solution, or act as project architect.

**For every Task under the relevant Goal/task group, write a concrete technical response**: what existing/new files will be reused, modified or created; their intended responsibility; proposed functions, classes, gates, contracts, callers, APIs/interface names and significant shared fields; how files call each other; critical dependencies; expected inputs/outputs; integration point; verification approach; and the accepted decisions each implements. Mark unknowns and assumptions honestly. Include actual planned changes, not decorative component names.

- The Coder's normal output is **one descriptive proposal file with per-Task sections**, or an equivalent already-supported Task attachment. **Do not create empty application source files, stubs, compiled modules or a new technical registry during Pre-Code.** The file describes what WOULD be created or changed. A proposal document is not product code.
- The Coder **does not need to independently optimize the whole application** or produce an additional cross-Task architecture overview. Each Coder should do its assigned Task well and propose technical details. The Reviewer is responsible for looking across all proposals.
- **Greenfield:** list proposed source files/functions/contracts and relationships using the Plan/approved decisions; there is no existing source to protect. **Brownfield:** inspect real source and callers first; identify exact existing components to reuse/change/keep, and any strictly necessary new files. Never replace working source with blank skeletons or assume generic framework patterns are missing.
- Proposed symbol names are reviewable design candidates, not immutable control-plane IDs; unimportant local variable details may be left to implementation. Shared interfaces/contracts and cross-Task names need consistency.
- Use the **simplest sufficient implementation**, prefer existing verified host-native capabilities and avoid hypothetical future requirements. Justify material additional gates, contracts, services, state, adapters and new infrastructure.
- This is a **Pre-Code preparation step**, not a mandatory Human interview. A small independent Task may have a compact proposal, but it still must not leap past the relevant technical review.

### Reviewer — whole-proposal cross-Task technical design review

Reviewer receives the **entire Code Structure Proposal across relevant Tasks**, the Detailed Implementation Plan, accepted decisions and the source/dependency evidence needed (especially in Brownfield). Reviewer must not approve Task proposals in isolation when other proposals materially interact.

Reviewer checks:
1. **Plan and Decision Fidelity:** proposed behavior corresponds to the approved Goal/Tasks and preserved expert solution.
2. **Cross-Task consolidation:** duplicate files/gates/contracts/callers, shared mechanisms, naming/interface clashes, unnecessary adapters, dead-end contracts, dependency cycles, coupling and integration seams. Consolidate, remove, reuse or retain with justification; do **not** build a giant generic framework merely to reduce file count.
3. **System fit:** actual host/runtime/dialect, existing services/tools, caller and work ownership, permissions, current working subsystems and regression risk.
4. **Proportionality and verification:** feasible implementation, smallest adequate complexity, specific evidence/test strategy, and whether new infrastructure solves an actual requirement.
5. **Technical review decisions:** PASS; CHANGES_REQUIRED with precise findings to Coder; or HUMAN_ESCALATION for unresolvable domain/scope/proportionality issues. Coder revises affected Task proposals and Reviewer reviews the affected combined design again.

**Only after Reviewer PASS** does the consolidated proposal become the **single implementation reference/list of proposed files, interfaces and responsibilities**. Derive this list from the reviewed proposal; **do not require Coder to write a separate catalog or implement a new registry**. Real application source creation/modification starts after this step, under existing write authority. Material later design changes return to Reviewer; routine local coding details do not. Normal Tester → Coder repair → retest and post-code independent review remain intact.

**Authority:** This is an internal Coder–Reviewer technical preparation/review within the existing workflow, **not a new Human approval/Technical Advisor gate**. Human is involved only for a materially missing professional/operational decision, approved-scope change, or risk/complexity escalation.

### Lead/Worker and multi-model compatibility

- Lead has access to the Plan, decision records and combined proposals. Worker receives enough related Goal/Task proposals and accepted shared interfaces to avoid fragmented, incompatible work. A Worker Reviewer may review within delegated scope; **cross-workstream consolidation is Lead review's responsibility** when no Worker sees the complete relevant design.
- Codex/Lead may also code using the same Pre-Code logic. A powerful model is not required to re-plan user-approved behavior.
- The optional **27B actual-code skeleton → smaller-model module fill** from Section 6 is an **implementation strategy after PASS**, not permission to put source skeletons into the Pre-Code proposal stage.

## 6C. Disproportionate complexity, host-native reality and Human alternatives

### Named warning: SMALL FUNCTION → BIG SOLUTION → LARGER SYSTEM IMPACT

Technical feasibility alone is **insufficient** for Reviewer PASS. For a narrowly scoped function, challenge proposals that require multiple new contracts, gates, managers, services, state transitions, branch/binding changes or modifications to unrelated stable subsystems. Assess the *system-wide change cascade*, maintenance cost, regression/crash risk and value, not an arbitrary number of files or lines.

Reviewer action:
- If a **proven simpler approach** exists, return CHANGES_REQUIRED and require Coder to revise the design before code.
- If the proposed solution is technically possible **but disproportionate/high-risk**, and no adequately simple safe alternative is established, **ESCALATE to Human before coding**. Do not pass merely because it can be built. Do not invent another technical subsystem to compensate for an unexamined assumption.
- Escalation summarizes the **small original requirement, large proposed mechanism, affected larger system, concrete risk, and practical decision** in language the Human understands. Reviewer need not be a domain expert and must not pretend it knows a simpler host-specific solution.
- Human can accept bounded risk, supply a simpler domain/operational approach, reduce automation, elect **manual execution or manual verification**, postpone or remove the function. A manual step is a legitimate solution when it satisfies actual needs with less cost/risk.
- Coder updates its proposal; Reviewer re-evaluates fidelity/impact. Do not silently turn Human's manual choice into automated infrastructure.
- No blanket "zero risk" criterion or numerical complexity threshold. Only escalate real mismatch or material uncertainty; routine Task designs remain agent-internal.

### Anchoring examples — review examples, not new CadGPT product requirements

**Example A — Create Job (Brownfield).** Human: invoke Create Job, describe a workflow, record it, execute, check native results, then save/publish the Job for later use. An earlier generic approach invented repeated draft folders, checkout, copying to final, promote and cleanup. This multiplied states and source-of-truth failures on each update. Source-verified CadGPT V5 already has jobcreate skills, v5_source_create/update, direct final managed JOB.md, job_runtime_prepare(source_path), real CAD/FILE tools, bound Save and explicit v5_source_publish for Registry discovery. Reviewer should prefer appropriate reuse, **not build a parallel Job engine or mandatory draft lifecycle**. Distinguish writing source, saving DWG and publishing Registry. Actual native runtime PASS is still unverified until tested.

**Example B — AutoLISP host testing.** AutoLISP is code executed in the actual AutoCAD host; ordinary standalone mock/sandbox does not establish correctness. A new DWG opened **inside the same AutoCAD process** does not isolate process crash, but can require switching CadGPT's bound drawing and disrupt other Jobs bound to the original drawing. Creating a sandbox runner, isolated drawing-binding manager, state restoration service and cross-Job orchestration merely to test one Lisp can be a textbook **small function → big solution → larger system impact**.
- Candidate real-host approach: run on the authorized currently bound drawing with relevant static checks, AutoCAD-compatible error handling and **UNDO Group** for supported reversible DWG edits, inspect actual output, then undo when the test requires restoration.
- **UNDO Group is NOT process-crash isolation, external-file rollback, or a guarantee that all effects can be undone.** Use saved-data/recovery precautions suitable to the actual operation.
- If even automated native testing is disproportionate or not safe in this environment, Human may say **"give me the Lisp; I will load/run/test it manually"**. Respect that choice and report native verification as Human-pending, not PASS.
- Reviewer **must ask Human** when it cannot resolve such disproportionate host-specific complexity, even if the proposed engineering system is buildable. No mandatory new test drawing or invented sandbox.

**These are transferable engineering judgment cases; do not modify CadGPT Criteria or copy CadGPT-specific storage/command rules into all Bootstrap projects.**

## 6D. Why this is expected to reduce rework — measurement, not promise

Early proposals and Reviewer analysis consume extra initial tokens. Their purpose is to avoid discovering duplicated interfaces, unnecessary lifecycle states, wrong host assumptions and brittle architecture **after** code and tests exist.

Measure by completed Goal: **total cost = pre-code proposal/review + implementation + testing + rework**, including context, cloud tokens, local wall-clock, native test failures and regression effort. Do not claim universal savings; for tiny isolated changes extra review may outweigh benefits. Benchmark relevant greenfield/brownfield and host-dependent examples. The objective is *lowest justified end-to-end cost and bug risk*, not maximum automation or minimum first-step tokens.


## 7. Relationship to existing installation tiers

Current repository `harness/specs/TIER_MANIFEST.json` contains **Lite / Standard / Full** as *installation/feature tiers* with existing requirements. These must **not** be renamed to Lead/Worker or silently repurposed.

Add profile-aware setup **orthogonally**:
- Existing installation tier answers *what shared files/capabilities are installed*.
- Lead/Worker execution profile answers *who owns what responsibility, what context is loaded, and what scope/authority applies*.
- Host adapter selection answers *which native integrations are installed/verified*.

A project may have Codex Lead and QwenCode Worker installed together without two independent sources of project authority. Check the existing multi-host installer for ownership/conflicts; do not assume it already supports QwenCode or scoped Worker provisioning.


## 8. Upgrade milestones — one implementation sequence, no new Human gates

The following are **delivery work packages**, not additional product lifecycle/approval gates. For an existing/brownfield Bootstrap project, preserve any already valid Criteria, Plan, Milestones and installed skills; do not restart Bootstrap or force re-approval. The readiness check remains: (1) approved Criteria, (2) Plan aligned with Criteria, (3) Milestones aligned with Plan, (4) Coder/Tester skills, knowledge and tools ready. Reuse evidence rather than fabricate new registration/SHA gates.

### M1 — Read-only baseline, source fit and decision-loss audit

Inspect real Bootstrap installer/roles/skills/harness, approved-criteria protections, native host adapters and hook events, Lite/Standard/Full tiers, Branch Authority, Worktree behavior, session/handoff, Planner/Reviewer coordination, present Coder sequence, and existing decision storage. Characterize greenfield and brownfield needs and missing support for QwenCode. Establish reproducible Codex/QwenCode baseline: context injected/loaded, latency, tool calls, token use, total time, correctness, test/rework and material scope drift.

**PASS:** Real-source gap map and baseline; evidence separates verified operation from instruction-only guidance, identifies decision loss and pre-code gaps. Measurement instrumentation, if needed, receives an appropriately reviewed minimal design before code.

### M2 — Single solution design and Reviewer check

Finalize optional Discussion Job activation, Secretary decision schema/index/supersession, stable reference links, Planner coverage/conflict/feasibility behavior, Coder domain boundary and solution-clarification skill, Code Structure Proposal file format and per-Task fields, combined Reviewer protocol, complexity escalation and manual alternative. At the same time finalize Lead/Worker authority, Task Criteria/Goals, delegation schema, profile/role/context dependency matrix, native hook/worktree policy, Universal Core, existing tiers compatibility and non-goals.

**PASS:** One reviewed design; all user-accepted decisions above traceable, no rewriting of domain decisions, no proposed universal manager/registry/sandbox, no additional Human approval or Technical Advisor gate, clear host enforcement limitations.

### M3 — Decision preservation and Pre-Code workflow implementation

Implement **only necessary changes** to optional Discussion Job/Secretary record-keeping and Planner decision references. Add/modify Coder Instruction and the scoped solution-clarification skill; align implement-task and Reviewer instructions/adapters across supported hosts. Enable **descriptive** per-Task Code Structure Proposal and **whole-relevant-proposal** Reviewer consolidation, CHANGES_REQUIRED repair and HUMAN_ESCALATION. Reuse document/task stores and existing reviewer dispatch as far as feasible; do not create a second planning engine or source registry.

**PASS:** (a) Accepted expert decision survives Plan rewrite/handoff with provenance and exceptions; (b) clear Task needs no repeated Human interview; (c) no source files modified during pre-code; (d) Reviewer detects needless duplicate gate/contract and requests simplification; (e) disproportionate feasible small function escalates to Human, manual-test choice respected; (f) only accepted reviewed proposal authorizes implementation under existing source-write rules.

### M4 — Profile-aware setup, native hooks and minimal context

Implement Lead/Worker profile-aware setup orthogonal to installation tiers, host-specific native rules (especially QwenCode), shared branch/path authority and isolated worktree provisioning. Preserve Codex Lead and Coder capability. Configure full role-scoped instructions + in-scope metadata, targeted activation and compact handoffs; do not promise control over platform-injected schemas or chat history. Verify existing multi-host installation, permission event semantics, bypass limitations, direct shell/MCP edit surfaces and conflicts.

**PASS:** Concurrent Codex/QwenCode profiles without corrupting shared config; verified scope protections and explicit gaps; Worker sees only relevant skills/instructions; Code Structure Proposal and decision links available to correct Reviewer/Coder.

### M5 — End-to-end delegated Coder/Tester/Reviewer operation

Lead prepares task contract/branch/worktree; Worker Coders receive accepted task and reviewed design, implement within allowed source scope; Worker Tester/Reviewer verify, then Lead cross-workstream review/integration checks. Exercise concurrent disjoint Tasks, Reviewer cross-Task consolidation before coding, discrepancy escalation, FAIL→Coder fix→Tester retest, blocked/stop, compact handoff and continuation of authorized local tasks while cloud quota unavailable. Preserve independent Lead verification and existing approval rules.

**PASS:** One full delegated greenfield and one brownfield representative Goal with real diffs, review evidence, regression tests and protected integration; accepted domain decisions and shared contracts survive role/session changes.

### M6 — Optional multi-model code implementation benchmark

Only **after Pre-Code Reviewer PASS**, prototype capable ~27B model constructing an **actual source skeleton** for a suitable multi-module Goal, smaller local model filling narrow approved modules and running tests, then integration/Reviewer. Compare to one capable model implementing directly. Test syntax/build, interface compatibility, native host suitability, model-switch costs, regression and rework. **Do not confuse actual code skeleton with pre-code descriptive document.**

**PASS:** Representative evidence of lower total completion time with acceptable quality, otherwise leave disabled/optional; no extra gate on basic Coder execution.

### M7 — Full regression, efficacy and release decision

Regression cover greenfield and brownfield bootstrap, Criteria/Advisor trigger and human authority, Plan/Milestones, Decision Ledger including supersession, refusal of unsanctioned theory change, Reviewer preservation of professional solutions, Coder solution clarification, source-free pre-code proposals, cross-Task deduplication, disproportionate-risk escalation/manual option, genuine AutoCAD Lisp host limitations as an example, Worker role/skill boundaries, branch/worktree/path hooks, parallel projects, cloud exhaustion, resume/handoff, Tester→Coder retest, installation tiers and independent checks.

Compare **end-to-end Goal cost** with baseline (cloud tokens and request sizes, local latency and total time, rework iterations, bugs/regressions, missed user decisions and complexity introduced). Never claim a universal percentage gain without data. Do not push a release/deployment until the ordinary reviewed authorization and real host evidence are complete.

**PASS:** No governance/decision drift; no unreviewed code-scope escalation; normal short Tasks remain friction-light; measurable benefits or explicitly documented neutral/negative results; deployment only by separate authorized action.

Every milestone uses the already defined evidence and Reviewer/Tester/repair loop. **No new Advisor, Criteria re-approval, artificial lifecycle stage, mandatory Discussion Job, mandatory mock CAD test, or Human code approval is introduced.**

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
11. Secretary records accepted expert decisions with stable provenance; Plan and Coder read the decisions by reference and cannot silently redesign them.
12. Coder is not Domain Expert. Missing operational/domain decisions trigger focused clarification; adequate Plan/decisions trigger proposal, not Human questioning.
13. Pre-Code Coder produces only a descriptive file of planned changes per Task (new/modified/reused file, functions, gates, contracts, callers, tests); **no application source file creation/modification** before relevant cross-Task Reviewer PASS.
14. Reviewer consolidates the complete relevant design, produces the reviewed technical reference/list as a derived result (not a new registry) and prevents undue complexity.
15. **Small Function → Big Solution → Larger System Impact** is an explicit escalation signal even if technically feasible. Human may choose host-native direct execution, UNDO-protected verification, manual testing, scope reduction or dropping the function. Do not promise crash isolation from UNDO.
16. Greenfield and Brownfield follow the same proposal/review workflow; Brownfield must ground all decisions in existing source and callers. Separate descriptive Pre-Code from optional actual-source skeleton implementation after review.

## 10. Immediate next step and stop condition

Review **this single draft** against the current source, Decision references and operational constraints, then perform M1 audit. Do not begin implementation work merely because this document was saved. Existing Criteria/Plan/Milestones and already-verified Bootstrap readiness remain authoritative; use the normal Reviewer and Human authorization path for actual changes.

**Recorded decisions consolidated in this draft:** One unified plan; optional Discussion Job + Secretary with precise accepted-decision records and supersession; reference-based Planner with decision fidelity; Coder as Software Engineer (not Domain Expert) plus focused solution-clarification only for missing consequential logic; per-Task descriptive Pre-Code Code Structure Proposal without source writes; Reviewer whole-proposal consolidation and PASS/rework/escalation; explicit **Small Function → Big Solution → Larger System Impact** review; Human option of manual work/verification; greenfield/brownfield source-fit; Lead/Worker profiles and authority; verified native controls per host; scoped Task Criteria/Goals; Lead-prepared worktrees; Worker Coder/Tester/Reviewer; minimal role-scoped context; optional post-review actual 27B-skeleton/small-model implementation; cloud/local parallel continuity. These are design decisions recorded in a **DRAFT plan**, not an implementation completion claim.
