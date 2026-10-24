# Bootstrap — Unified Context, Decision Preservation & Pre-Code Engineering Upgrade Plan (Draft v6)

**Status:** DRAFT — awaiting Planner/Reviewer review and Human approval  
**Repository:** `thebimhouseinfo-sudo/bootstrap`  
**Document authority:** Single canonical upgrade plan, updated in place. Draft v6 retains every operational rule of the earlier Context/Lead/Worker/Decision/Pre-Code plan while replacing the default retirement algorithm with scope-wide Phase/Plan retirement and adding full user-triggered behavioral simulation plus bounded three-cycle bug fixing. A heading alone is NOT preservation of its solution.
**Scope:** context efficiency; optional Discussion Job and Secretary decision preservation; reference-linked expert decisions; Coder solution clarification and descriptive Pre-Code proposals; cross-Task Reviewer and disproportionate complexity escalation; **scope-wide RETIRED for replaced Plan/Phase/Milestone/Job/Task and exclusive source branch**; **Tester user-entrypoint simulation through multi-flow interleaving/adversarial behavior**; **maximum three Coder-fix/independent Tester-retest cycles then advanced root-cause skill**; Lead/Worker profiles; host-native enforcement, worktrees, multi-model benchmark and regression.
**Criteria:** Existing approved project Criteria remain unchanged. **This document is not approval to implement, merge implementation code, or deploy.**


## 0. How this plan prevents decision loss and accidental redesign

This file is not a list of topic names. Its requirements consist of (1) the concrete rules and examples below, (2) explicit role and artifact boundaries, (3) decision-by-decision traceability, and (4) observable acceptance cases. **Future editing must preserve these semantics, including negative cases and Human alternatives.** A revision that keeps a heading but drops its operational meaning is PLAN DRIFT.

### Authority and vocabulary — do not collapse different things

| Term | Meaning, author and boundary |
| --- | --- |
| Project Criteria | Human-approved description of WHAT/WHY, existing source of product authority; unchanged by this upgrade |
| Accepted Expert Decision | A particular Human-settled operational/professional solution with original rationale and exceptions; the full source remains readable |
| Discussion Job | Optional workspace for discussions and decisions, not a coding Job, permanent agent, or bootstrap gate |
| Secretary | Focused function/role that accurately records accepted decisions; no independent right to decide for the Human |
| Detailed Implementation Plan | Planner's delivery decomposition of approved goals into related Tasks, sequencing, dependencies, acceptance and source decision references |
| **Code Structure Proposal** | **One descriptive file of the Coder's intended source-level work for each assigned Task, written BEFORE any application source changes** |
| Technical Reviewer findings | Cross-Task, whole-proposal review of proposed file/module/function/contract/caller/dependency design and host fit; decides PASS, CHANGES_REQUIRED or HUMAN_ESCALATION |
| Reviewed technical component list | **Derived only AFTER Reviewer PASS**, from the corrected proposal; a usable reference to future source changes, NOT a new Registry or Coder deliverable before review |
| Implemented source | Actual application code, created/changed only after the relevant proposal review and through existing authorized write tools |
| Optional actual code skeleton (multi-model experiment) | Real source stubs/modules built DURING implementation after design PASS; NOT the Code Structure Proposal and NOT a mandatory step |

**Document status:** These are discussion-settled design rules recorded in an upgrade PLAN that is still DRAFT. Writing this file does not itself implement role/skill/runtime changes or claim formal approval of a new product Criteria.

### Anti-drift editing procedure for future Planner/Secretary/Reviewer work

1. Preserve the original complete source for every accepted expert decision. Do not replace an 8-step expert algorithm with a generic phrase such as "use the approved HVAC logic."
2. When revising a Plan, inspect referenced accepted decisions, previous Plan decisions and still-active Task dependencies. Record which decisions remain COVERED, are missing, contradict one another or require explicit Human correction.
3. A shortened human-facing summary is allowed, but it **must never replace the canonical operational specification** or delete exceptions, rejected alternatives and escalation behavior.
4. A missing reference is an unresolved coverage issue, not permission for Coder to invent a new solution.
5. Do not create new Criteria, Technical Advisor calls, job stages, approvals, registries or enforcement mechanisms merely to make this documentation process appear rigorous.
6. Reviewer must flag a proposal or revised Plan as DECISION_FIDELITY_FAIL when it retains topic labels but loses the actual solution, caller semantics, trigger, output or exceptions.


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

Lead prepares **before Worker launches**, using the **already reviewed cross-Task Code Structure Proposal** where implementation is about to begin:
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

Lifecycle: `PREPARED → ASSIGNED → IMPLEMENTING → SELF_TESTED → SUBMITTED → LEAD_REVIEW → ACCEPTED / REWORK / REASSIGNED`, with `BLOCKED` for genuine inability to continue. This is a **delegation execution sequence, NOT the authoritative Task/Job lifecycle**: reviewed Plan changes must reconcile RETIRED/SUPERSEDED obsolete READY and IN_PROGRESS work through Section 6G before new dispatch. **Pre-Code Coder Proposal → Reviewer design review occurs within preparation before IMPLEMENTING; it does not add a separate approval authority or project lifecycle state.** A Worker **never self-assigns ACCEPTED**, merges to protected branches, or invents Human/Reviewer approval.

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
After the applicable descriptive Pre-Code Proposal has been reviewed across the relevant Tasks, Coder implements the scoped task, performs self-checks; Worker Tester and Reviewer inspect behavior/diff within task scope; submit to Lead. Suitable for a small fix or well-bounded task.

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

**Only after Reviewer PASS** does the consolidated proposal become the **single implementation reference/list of proposed files, interfaces and responsibilities**. If a later reviewed Plan revision retires relevant Tasks, old proposal PASS cannot authorize implementation; apply Section 6G and re-review. Derive this list from the reviewed proposal; **do not require Coder to write a separate catalog or implement a new registry**. Real application source creation/modification starts after this step, under existing write authority. Material later design changes return to Reviewer; routine local coding details do not. Normal Tester → Coder repair → retest and post-code independent review remain intact.

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



## 6E. Operational specification — from accepted discussion to reviewed code design

This section is the **detailed behavior contract** for implementation, not a shorthand recap. It explains exactly what each role receives, writes, checks and hands off. Sections 1–6D and 7–10 remain binding.

### E1. End-to-end flow, deliverables and real write boundaries

~~~text
Human / Domain Expert
  ├─ normal chat, or optional explicit Discussion Job
  └─ accepts an operational/professional decision
       ↓
Secretary (only when a discussion recording context is active)
  └─ writes full accepted decision, why, examples, exclusions and supersession links
       ↓
Planner
  ├─ reads approved Criteria + full decisions
  └─ derives Detailed Implementation Plan, Goals, Tasks, acceptance and references
       ↓
Coder — Pre-Code preparation (not source implementation)
  ├─ reads Plan/Task list, relevant full decisions, verified code/host context
  ├─ asks Human/Lead ONLY if essential real-world logic or domain solution is missing
  └─ writes one Code Structure Proposal file:
       Task T1: would CREATE/MODIFY/REUSE file A; planned caller/functions/contracts...
       Task T2: would CREATE/MODIFY/REUSE file B; planned caller/functions/contracts...
       Task T3: ...
       [NO application source files created or modified]
       ↓
Reviewer — whole-relevant-design technical review
  ├─ reads every affected Task proposal together + actual existing source in brownfield
  ├─ finds duplicates, unnecessary contracts/gates, caller gaps, host conflicts, coupling
  ├─ challenges disproportionate small-function → big-system changes
  ├─ CHANGES_REQUIRED: Coder adjusts proposals and re-submits affected combined scope
  ├─ HUMAN_ESCALATION: asks Human for missing domain choice or unacceptable risk trade-off
  └─ PASS: accepts consolidated structure
       ↓
Derived implementation reference / component list
  └─ extracted from reviewed proposals; same artifact or view; no second registry
       ↓
Coder — Implementation (authorized application source changes start HERE)
       ↓
Actual host tests / Tester / independent code review / repair loop
       ↓
Integration through existing branch and Human authority
~~~

**Files in Pre-Code:** A Markdown/text proposal record is allowed. **No new empty .ts/.py/.lsp/.cs application files, code stubs, created fake implementation, modified product files or written tests** merely to "show the structure." "Empty shell of the app" refers to *descriptive intended structure in the proposal*, not to a checked-in code skeleton. A future approved implementation stage may actually create source files; this is a different time and purpose.

**Granularity:** Coder answers the already assigned Tasks. One proposal file can contain the relevant Task sections; if several Workers submit Task-level sections separately, Reviewer reads the combined relevant set. Do not force the Coder to become project Architect, to author an independent technical implementation plan or to maintain a global Registry.

### E2. Discussion Job and Secretary — exact event and record behavior

**Entry rule:**
- Human explicitly says "open/create Discussion Job": create/open the discussion workspace, without an extra question or a new advisor/approval gate.
- Human merely says they want a discussion: ask ONCE whether they want a Discussion Job to record decisions. "No" means continue talking without a Discussion Job; do not keep prompting.
- A normal question, suggestion, technical brainstorm or Coder task is **not** by itself a Discussion Job trigger. Do not use AI complexity scoring to decide whether to open one.

**During an open Discussion Job:**
- Discussion may include proposed ideas, disagreement, experimentation and unresolved questions. **Secretary records a DEC only upon a genuine accepted Human decision**, not every assistant sentence.
- Recording must occur at the decision point, rather than hoping the next Planner can reconstruct it from a long conversation.
- Exact User terminology, professional data rules, examples, input/output constraints, decision rationale, exceptions, risks and rejected alternatives must be retained. Preserve the **solution**, not merely its topic name.
- If a decision is corrected, the previous decision stays readable and points to the successor (SUPERSEDED_BY); the index shows active/superseded/unresolved states.
- Secretary can note unknowns, but must not mark them ACCEPTED, silently settle a disagreement or create missing algorithms.
- Do not claim a GitHub decision was saved unless the write actually succeeded. If the connector is unavailable, retain the proposed full record in the current interaction and explicitly mark persistence NOT_VERIFIED; do not fabricate a path or SHA.
- A Discussion Job can end without triggering Criteria modification, Plan update, Coder execution or publication. Human chooses what to do next.

**Illustrative folder, not proof that files exist today:**
~~~text
docs/discussions/DISC-001-job-workflow/
  INDEX.md                    # active DEC IDs, current/superseded state, linked Goals
  DEC-001.md                  # one complete accepted decision
  DEC-002.md                  # another complete accepted decision
~~~

**Minimum content of an accepted decision record:**
~~~md
# DEC-001 — Job source ownership and authoring
Status: ACCEPTED
Discussion: DISC-001
Source: <specific Human message / chat / approved document link>
Accepted by: Human
Applies to: <affected feature / Goal / Task IDs>
Decision in Human terms:
  <full accepted behavior, exact ordered workflow, known inputs and outputs>
Reason:
  <why this is useful or simpler in real operation>
Professional/host constraints:
  <versions, environment, original data rules, exceptions, risks>
Examples:
  <at least the concrete cases the Human gave; preserve their values and meaning>
Rejected alternative(s):
  <what was rejected, and why>
Unresolved:
  <no silent assumptions>
Supersedes / Superseded by:
  <IDs or none>
~~~

This format is a documentation contract, not a new product data model or permission engine. Do not reproduce every unrelated chat message, only complete accepted decisions and their necessary context.

### E3. Planner — how to write a referenced Detailed Implementation Plan without losing decisions

Planner keeps the approved **WHAT/WHY** from Project Criteria separate from the accepted **HOW/DOMAIN LOGIC** in Expert Decisions. It remains free to research and critically evaluate proposals before Human acceptance.

For a decided Goal, Planner must:
1. Read the complete applicable Decision records and verify their status and provenance (including later supersession), not a previous short recap.
2. Identify the outcome, observable acceptance, Tasks, order and shared dependencies.
3. Link Task/Goal directly to those decisions. Include only the short orientation needed to navigate; do not replace the full algorithm/procedure with a rewritten one.
4. Check **COVERAGE** (each accepted in-scope decision reached), **CONFLICTS** (two active instructions incompatible), and **FEASIBILITY** (host/tool constraints observed versus assumed).
5. If a genuine conflict or infeasibility is found, provide evidence and a specific Human-facing decision to make. Do not silently change the solution, automatically trigger Technical Advisor or edit Criteria without existing authorization.
6. Keep original decision links during every Plan revision. When revising scope, explicitly identify what remains unchanged and what Human settled as revised.

**Example Goal/Task entry (illustrative, not a second plan):**
~~~md
Goal G-JOB: Create and run a user-defined CadGPT Job
Decision references: DEC-JOB-001, DEC-JOB-002
Acceptance: Given a user workflow, the authorized Job source is recorded,
  actual steps run with real CAD/file tools, effects verified and saved when
  appropriate; reusable discovery occurs when explicitly requested.

Task T-JOB-1: Interpret the supplied workflow and map existing capabilities
Task T-JOB-2: Record the final managed Job source and any required helper
Task T-JOB-3: Run on the exact bound drawing, verify and retain repair evidence
Task T-JOB-4: Publish the saved Job for future invocation when requested

[The full host-specific solution, rejected draft/promote lifecycle and
exceptions live at linked decisions, not in a lossy rewritten paragraph.]
~~~

A Plan has a **delivery structure**, not an invented full replacement for the accepted domain solution. Planner must not dilute a Human-approved solution just to make the Plan shorter.

### E4. Coder — what "solution clarification" means and when NOT to ask

**Coder is an engineer implementing code, not a Domain Expert or product Planner.**

Before proposing code for a Goal/Job Pack, Coder reads the Goal, related Tasks, existing Plan, the **full** referenced Human decisions, the verified host profile, the relevant source/callers and the applicable focused skill/knowledge.

There are **two material categories** of questions:
1. **Missing operational logic / foundational constraints** — e.g. whether the app works on live AutoCAD or offline DWGs, AutoCAD version/platform, read/write scope, what the user experiences and what observable result is required.
2. **Missing professional/domain solution** — e.g. which attributes determine HVAC device classification, how a professional exception works, what measurement is authoritative, or what specific workflow must be preserved.

Ask only if the information is material to choosing a correct overall solution. The question should be about the **real outcome or host operation**, not "which framework, database, algorithm library or interface should I use?" Coder may nominate a reasonable operational choice when there is genuine ambiguity, but must not pass off an invented domain rule as accepted.

**Counterexample:** If the Detailed Implementation Plan and Decision records already specify the CAD binding rule, the Lisp executor, the workflow steps and the professional data mapping, Coder must NOT ask Human again. Coder directly writes its per-Task source-level proposal.

**Coder does not ask** about ordinary file organization, variable names, control flow, test helper implementation, error-handling idioms or minor technical choices. Coder decides these as a competent software engineer and gives Reviewer an evidence-based proposal.

**Exception:** A seemingly small Task that requires extensive extra infrastructure and affects unrelated subsystems should be highlighted in the proposal; Reviewer then challenges and escalates when necessary (E8), rather than Coder writing code first.

The solution-clarification skill supports this **single pre-code analysis**, not repeated forms, a separate user approval ceremony, a Job-stage gate or a forced brainstorming loop. It applies in software-only and domain-heavy projects alike.

### E5. Code Structure Proposal — precise file contract

**Definition:** A Code Structure Proposal is **a real descriptive text/Markdown file** produced by the Coder in the existing task/document workspace. It describes, task by task, **which application source files the Coder would create, modify, reuse, keep or remove, what code each would contain, who would call it, which dependencies it needs and what would prove it works**. Its described files do NOT yet exist if marked CREATE. Its described existing files are not modified.

**Input:** a specific Detailed Implementation Plan/Task List with Goal/Task IDs, accepted decisions, real existing source/host metadata where applicable, and the permitted workspace.

**Audience:** **Reviewer only** (and other implementing agents who need the reviewed design). Human should not be required to review this technical file. Human may receive a short outcome/risk question only in a legitimate escalation.

**Storage:** Prefer a single Task/Goal-owned .md file within the *already permitted documentation/work area*. No new dedicated document database, global architecture registry, source staging directory, separate Planning phase or permanent framework. If host supports Task attachments instead of files, use the host-native equivalent without changing the semantics. **The proposal file itself is not a source code file.**

**Per-Task minimum fields, all meaningful and concrete:**
- Task ID, Goal link, short actual Task requirement, decision/acceptance references.
- Existing code evidence: where Coder looked; relevant file names, current callers and functions that truly exist; label unverified guesses **PROPOSED**, not **EXISTING**.
- For each planned affected file: exact proposed path; action **CREATE | MODIFY | REUSE_AS_IS | KEEP | REMOVE**; role of file; actual expected code elements such as important named function/class/gate/contract/caller/interface/field; responsibility; inputs/outputs; other file(s) that will call/use it.
- Integration/call flow across the specific Task, including when existing runtime components are invoked.
- Reuse vs new implementation justification: why an existing capability is insufficient before proposing infrastructure.
- Verification: observable tests and host/fixture needs, which changes are read-only vs stateful/destructive and which outcomes need native proof.
- Coupling, assumptions, uncertainties and any unexpectedly large solution or larger-system impact.
- Small set of **explicit exclusions** so Reviewer sees the simpler route, e.g. "No new draft lifecycle; no new CAD process manager."

**What NOT to write:** long synthetic source code, fake function bodies, empty compilable files, speculative whole-system architecture not required by Tasks, a registry of all project symbols, an invented test framework or an extra "technical plan" unrelated to Detailed Implementation Plan. Local variable names may be proposed when useful for shared interfaces, but are not frozen if they are only implementation details.

**Template — literally the form of the descriptive file:**
~~~md
# Code Structure Proposal — Goal G-XXX
Status: PROPOSED, NOT CODED
Plan / Task List: <real links, versions>
Decision references: <actual accepted records / provenance>
Environment read: <verified profile and relevant host facts>
Application source changes so far: NONE

## Task T-001 — <task title>
Requirement/acceptance: <what Planner already defined>
Professional decisions consulted: <full references, not pasted generic summary>
Current source inspected:
- src/existing-a.ts — verified existing function foo(); callers: bar()

Proposed file impact:
- MODIFY src/existing-a.ts
  Why: add behavior already required by T-001
  Planned code: function checkX(request), return allow/deny reason
  Called by: src/existing-b.ts
  Contract/data: reuse current request structure; no new permission schema
- REUSE_AS_IS src/existing-c.ts
  Why: existing helper already resolves current branch/work authority
- CREATE src/new-helper.ts (only if existing components cannot be extended)
  Planned code: small helper for <precise missing behavior>
  Caller: existing-a.ts
  Why new rather than reuse: <concrete source evidence>

Call path: existing-b → checkX → existing-c → original operation
Tests/evidence: <actual success, failure and regression cases>
Dependencies/risks: <material impacts, especially other Task interfaces>
No new components needed: <named exclusions>
Unresolved professional/operational decision: NONE / <specific question>

## Task T-002 — <task title>
[same fields]

No product source or test code is changed by this proposal.
~~~

**Important ownership rule:** Coder is **not responsible for generating a second project-wide architecture diagram or merging all proposals**. It completes per-Task engineering responses. Reviewer has the whole-bundle responsibility.

### E6. Greenfield and Brownfield — same artifact, different evidence

**Greenfield:**
- The Planner's approved Goal/Task list and professional/operational decisions establish intended behaviors and constraints; there may be no existing source.
- Coder describes **proposed future files** in the proposal file. Example: "CREATE src/tool-handler.ts — register the tool, call input validation, invoke the execution function"; "CREATE tests/tool-handler.test.ts — cover valid/invalid input".
- Describing a future file does not create it; Reviewer can reorder, merge or remove proposed files before implementation.
- Do not build a standalone bootstrap framework, full enterprise platform or unnecessary architecture simply because the project is new.

**Brownfield:**
- Before proposing changes, **inspect the current actual source and callers**. Determine whether a function/contract/gate already exists, whether its semantics match the Task, and what working consumers depend on it.
- Use **REUSE_AS_IS** or narrow **MODIFY** wherever the existing capability suffices. CREATE only for concrete missing functionality, not because a pattern is common in generic software engineering.
- A proposed change to a small function may cascade into existing background Job state, bound host identity, API compatibility, deployment or safety contracts; include those dependencies for Reviewer even though Coder need not globally optimize them.
- NEVER blank or replace existing source to turn it into a proposed skeleton. No unrequested migration, forked workflow, draft tree or duplicate canonical source-of-truth.
- Source audit distinguishes code behavior from tool selection/routing mistakes; a user-facing bug is not automatically evidence that a new subsystem is needed.

### E7. Fully worked Brownfield example — CadGPT "Create Job"

**Human outcome:** invoke Create Job; Human supplies intended workflow; Builder records it faithfully; execute on actual capabilities/host; inspect whether real steps work; save the Job so it can be run again. This is an illustration of a Coder response, **not authorization to change CadGPT**.

**Existing source surfaces verified during this discussion:**
- src/cadgpt/tools/control.ts: Create Job control/Builder entry.
- skills/jobcreate/SKILL.md, skills/jobcreate/job-skills/workflow-planning.md and tool-mapping.md: authoring and capability mapping.
- src/cadgpt/tools/v5-builder-source.ts: V5 owned source create/update/publish.
- src/cadgpt/tools/jobs.ts: runtime preparation, real execution, Job save/finish.
- src/cadgpt/tools/registry.ts: capability discovery.
- knowledge/jobs/JOB_RULES.md: actual V5 ownership, bound drawing, source-vs-Registry semantics.
These paths are **existing evidence at the time of reading**, not claims that a native CAD run has already succeeded.

**What the Coder's proposal file should actually say:**

~~~md
# Code Structure Proposal — CadGPT Create Job
Status: PROPOSED_NOT_CODED
Goal/Tasks: user-defined Create Job, workflow record, native run, save for reuse
Existing CAD runtime result: NOT YET VERIFIED

## T1 — Accept Create Job and record workflow
REUSE_AS_IS / VERIFY src/cadgpt/tools/control.ts
  Already exposes Create Job and Builder capability selection.
  Proposed change: NONE until end-to-end routing test shows a defect.
MODIFY skills/jobcreate/SKILL.md or workflow-planning.md ONLY IF a verified
  behavior gap causes loss of User business steps or unnecessary questions.
  Desired behavior: faithfully preserve input steps; ask only a missing
  consequential business/operational decision.
No new CreateJobManager, workflow lifecycle state or user questionnaire.

## T2 — Choose capabilities and write the managed Job source
REUSE_AS_IS skills/jobcreate/job-skills/tool-mapping.md
  Locate verified existing tool/Lisp/Job capabilities first.
REUSE_AS_IS src/cadgpt/tools/v5-builder-source.ts
  Call existing v5_source_create (or authorized update for existing source).
  Future user package includes JOB.md; optional lisp/ or tools/ only if needed.
  Do NOT build JobDraftManager, CheckoutContract, copy-to-final,
  new Publisher service or per-update draft folder.
Source creation and Registry publication are different events.

## T3 — Run, inspect and repair the real Job
REUSE_AS_IS src/cadgpt/tools/jobs.ts
  Call job_runtime_prepare(source_path) on final managed JOB.md.
  Follow actual steps with verified tools; native AutoCAD actions use the
  bound drawing. Check LOAD/run outcomes separately if Lisp is used.
  Save actual DWG only when modified; actual Save failure is not DONE.
  A failed run retains repairable evidence; do not blindly replay uncertain
  non-idempotent changes.
No mock-only "TEST PASS", automatic rebind or new runtime state engine.

## T4 — Save for future invocation
REUSE_AS_IS src/cadgpt/tools/v5-builder-source.ts
  The source already resides in the managed final folder before the test;
  after actual success and the User's request to retain/reuse the Job,
  call v5_source_publish for registry discovery.
  Publication is NOT copying draft files into final source.
  Job source persistence, DWG Save and Registry publish are distinct.
  If publish fails, report it; do not falsely report registered.
No new staging, promote gate, compatibility check or cleanup subsystem.

Cross-Task execution:
Create Job control → jobcreate workflow mapping → v5_source_create →
job_runtime_prepare → actual CAD/file executors → verified Save/finish →
explicit v5_source_publish.

Evidence required:
- Create Job reaches Builder with the intended Work context
- JOB.md preserves user's workflow
- Direct run from final source works without publication prerequisite
- CAD mutations verified on exact drawing; read-only job avoids needless save
- Failed run remains diagnostically repairable; no fabricated completion
- Successful publish makes Job discoverable
- Existing Job update does not create another draft folder
~~~

**Reviewer expected evaluation:** "A new draft/checkout/promote tree for each edit is an unrequested lifecycle, extra state/ownership ambiguity and a source of regressions. Existing final-source authoring and publish/discovery should be reused." Reviewer checks source evidence and real runner limitations, not merely whether a generic draft architecture *could* work.

**Important semantic edge:** "Save Job after testing" does **not** imply writing source for the first time after native execution. The V5 source must exist to be run and is written to its final managed owner location first; **publishing it for future discovery** is a distinct later action. Do not silently delete a failed unpublished source if repair is expected. If actual Human intent conflicts with this distinction, ask the consequential question instead of inventing a new source lifecycle.

### E8. Reviewer — cross-Task review, findings, derived inventory and implementation handoff

Reviewer input is **all relevant Task proposals together**, not just one local Task. Reviewer may be a Lead/independent Reviewer with the full relevant view; a Worker Reviewer restricted to one Task cannot falsely claim to have consolidated an unseen multi-Task design.

**Reviewer reads, in this order:**
1. The Goal, all affected Tasks, their acceptance and direct full accepted decision references.
2. Each Coder-proposed future file, important symbol, caller, contract, gate, state, dependency and planned test.
3. Relevant existing source, existing callers, host execution path, hooks/permissions, shared interfaces and integration boundaries (especially brownfield).
4. Cross-Task overlap: where two proposed things do the same work, where a new contract is not consumed, where an existing hook/helper suffices, and where a change causes a cascade in another subsystem.
5. Architecture/risk proportionality, testing feasibility and genuine host constraints.

**Reviewer decisions (with specific findings):**
- **PASS:** whole applicable design is sufficiently simple, feasible and faithful; Reviewer records/derives the final approved file/interface responsibility list from corrected proposals. PASS does not certify future code or test execution.
- **CHANGES_REQUIRED:** specify Task/file, exact problem, source/decision evidence, impact and the proposed simplification when known. Coder edits the descriptive proposal, **not source**; Reviewer re-evaluates the affected combined design. Avoid an unbounded speculative redesign loop.
- **HUMAN_ESCALATION:** consequential missing operational/domain input, change of accepted scope, or a technically feasible but disproportionate/high-risk large-system change that cannot be responsibly simplified. Ask Human in ordinary practical language, not to select programming frameworks. After Human chooses, Coder updates the proposal, then Reviewer re-evaluates.

**What cross-Task consolidation actually does:** If T1 proposes ReadGate and T2 proposes WriteGate, Reviewer inspects semantics and may recommend one permission mechanism or existing authority checker. If separation has a real necessity, retain it; do not force arbitrary code reduction. If T1 adds a request contract and no caller accepts it, Reviewer requests deletion or a real call path. If several Tasks need a common helper, Reviewer can coordinate ownership and names **before** code exists.

**Derived technical component list — only after PASS:**
~~~md
# Reviewed technical components — Goal G-XXX
Source: Code Structure Proposal <link and reviewed revision>
Review: PASS <review evidence>
- src/authority.ts      MODIFY     owner T1; checkX(); callers tool-handler
- src/tool-handler.ts   MODIFY     owner T2; invokes checkX()
- tests/authority.test.ts  CREATE  owner T3; allowed/denied/edge checks
Explicitly excluded: separate GateRegistry, new approval daemon
Known host limits: <verified facts, not assumed test results>
~~~

This can be a section/view of the **same reviewed proposal** or existing task artifact. **No second coder-authored catalog, index database or automatic registry sync is required.** Proposed names are useful lookup targets for later Coders and cross-worktree handoff, not a freeze on local variable spelling.

**Once PASS:** Coder implements within the already authorized branch/worktree and file scope, using accepted reviewed interfaces and direct decisions. Routine private refactors and local variable names do not need fresh Human input. Material new modules, contracts, shared interfaces, changed host behavior or expanded system impact require updated technical review; decisions requiring Human authority go through existing paths. Tester verifies the actual result and post-code Reviewer still checks code/test/decision fidelity. Do not confuse proposal PASS with native runtime PASS.

### E9. Small Function → Big Solution → Larger System Impact: actual decision procedure

**Trigger is a disproportion, not technical impossibility:** one small Task/function appears to require many new services, contracts/gates, binding switches, lifecycle stages, state recovery rules or modifications to healthy unrelated subsystems. Even if it **can be programmed**, it may be an unsafe or wasteful decision.

1. Coder's ordinary per-Task response exposes the proposed file/caller/dependency chain. Coder does not conceal it or implement first.
2. Reviewer examines **the original small outcome, proposed large mechanism and larger-system consequences**, including possibility of catastrophic bugs, multi-Job interactions, host crash, maintaining more states, new branches/gates and future regression.
3. When grounded in existing code/host evidence, Reviewer requests a **simpler concrete proposal** from Coder.
4. **If no proportionate/sufficiently safe alternative has been established, Reviewer MUST escalate to Human BEFORE code**, even if implementation is feasible. Reviewer must not force itself to invent a domain-specific fix or add yet another subsystem to make the original overlarge solution work.
5. Human may **choose direct execution with understood risk; provide domain/host knowledge; select reversible execution where practical; reduce automation; manually perform/test a step; postpone; or drop the function**. Human does not have to approve gates/contracts or understand internal class names.
6. Coder updates the same proposal based on that practical decision. Reviewer confirms the new architecture is consistent with Plan, source and host limitations; implementation begins only then.

**Human-facing escalation should be concise, for example:**
~~~text
Original request: Test one AutoLISP on CadGPT.
Proposed solution: open another drawing and change the bound-drawing context.
Impact: affects other running Jobs and needs binding preservation/recovery logic.
Risk: extra cross-Job runtime states and regression, without process crash isolation.
We have not established a proportionate safe approach.
Would you prefer direct host execution, a reversible test where feasible,
or to receive the Lisp and run/verify it manually?
~~~

**Do not treat "manual" as failure.** Human may simply say: "Give me the Lisp; I will LOAD and test." Coder supplies source and exact instructions, marks native outcome **PENDING HUMAN TEST / UNVERIFIED**, and does not build a hidden simulator or claim automated PASS. If a hard approved requirement truly mandates automation, a proposed change to that approved requirement uses the **existing** Human/Criteria authority rather than an unrecorded bypass.

### E10. AutoLISP / AutoCAD — full host-specific causal example

**Professional execution fact:** Lisp runs in AutoCAD, not in a generic language sandbox. An external mock, static parser or simulated CAD object model can help with limited issues, but it cannot prove actual AutoCAD geometry or command-side effects.

**False shortcut 1:** "Test in an AutoCAD sandbox." Unless such an actual isolated, verified host facility exists and fits the requirement, Coder cannot assume or invent it. A sandbox runner plus fake APIs becomes a new subsystem needing its own tests.

**False shortcut 2:** "Open another test DWG in this AutoCAD session." That is **not process isolation**: a fatal Lisp/AutoCAD crash can close all drawings in the same process. In CadGPT, the current Job/other Jobs may be bound to the original drawing; testing on the new drawing can require re-binding, restoring identity and synchronizing state among Jobs. What began as "test one Lisp" becomes a change to the larger binding architecture.

**Proportionate options the Human can accept:**
- Test directly on the currently authorized/bound host drawing when the operational risk is understood and acceptable; no automatic drawing switch.
- For operations that are genuinely reversible, capture appropriate pre-test state, use a correctly managed AutoCAD UNDO Group and error/ESC cleanup, inspect actual output, then undo when test restoration is intended.
- Deliver the Lisp for **Human manual LOAD/RUN/inspection** without building automated test infrastructure; report results from actual human test when received.

**Limits:** UNDO Groups can help restore supported DWG edits; they do **not** isolate crashes, guarantee restoration after the process terminates, roll back external-file effects, undo every side effect or substitute for recovery of unsaved user work. A direct-host option is a Human-accepted operational choice, not a blanket claim of zero risk. A test that changes a drawing must still honor relevant binding/Save rules, including avoiding false Done.

Reviewer need not know a novel CAD expert technique. Its duty is to recognize that the engineering solution is expanding beyond the small request and **ask Human rather than approve a fragile architecture**. The Human may know an inexpensive practical method unavailable to the model.

### E11. Lead/Worker, context and optional actual source skeleton — integration rules

**Lead/Worker profiles are task authority scopes, not model capability rankings or installation tiers.** Codex cloud may be Planner, Reviewer, Tester or Coder. Local QwenCode/Continue can be Workers for delegated tasks and may be reviewed locally where they genuinely see all relevant design; final Lead integration checks remain as configured.

- A Lead can prepare multiple isolated nonconflicting branches/worktrees and assign reviewed Task-level interfaces. Worktree separation controls Git working trees, **not arbitrary OS writes**; host-native permission/hook protection must be tested. No fake sandbox.
- Worker Coder sees its assigned Plan/Task and accepted decisions. If shared mechanism overlaps another Task/workstream, a Reviewer with the **combined relevant proposals** resolves the interface. Do not require every Worker to reconstruct the whole project.
- A Worker may continue **already prepared, reviewed and authorized implementation** while cloud access is unavailable. The absence of cloud access does not license changes to Project Criteria, approvals, protected hooks, integration policy or unreviewed cross-workstream architecture.
- Keep instruction/context loading sparse: small Universal Core; full ACTIVE role, scoped relevant skill metadata; full skill content on activation; NO metadata or full content for unrelated agents, skills, tools, knowledge or harness prompt instructions. Inspect host-injected schemas and retained conversation separately; cannot promise to remove inaccessible platform context.
- Native QwenCode hooks must be tested as QwenCode hooks. Copied Codex hook config, Markdown "deny" statements and worktrees are NOT equivalent to verified enforcement.
- A possible **post-review implementation** experiment can ask a 27B model to write actual source skeletons and smaller models to fill narrow modules. This is distinct from the **pre-code descriptive proposal**, which never creates product code. Only use this experiment when end-to-end metrics justify it, not by default.

### E12. Acceptance cases that directly falsify plan drift

| Case | Input condition | Required observation / reason to FAIL |
| --- | --- | --- |
| D-PRESERVE-1 | Human settles a detailed domain mechanism with exceptions | Secretary record preserves all critical steps, exceptions and rejection rationale; a mere topic label FAILS |
| D-PRESERVE-2 | Human revises a decision | Old text remains linked and readable, successor marked active; silent overwrite FAILS |
| D-PLAN-1 | Planner rewrites Goals/Milestones | Each still-relevant accepted decision is linked and readable; lost link or changed rule FAILS |
| D-CODER-1 | Goal fully documents operational logic and professional solution | Coder produces technical proposal without asking Human to repeat known facts |
| D-CODER-2 | Goal lacks materially consequential host/professional input | Coder asks a focused real-world question before selecting the implementation |
| D-PRECODE-1 | Task proposes 3 new modules | Proposal file describes proposed modules/functions/callers; no application source file exists/changes yet |
| D-PRECODE-2 | Brownfield Task has suitable existing helper | Coder cites/reuses real helper; new parallel service without justification FAILS |
| D-REVIEW-1 | Two Tasks propose overlapping gate/contract logic | Reviewer sees **both**, weighs consolidation and documents decision before implementation |
| D-REVIEW-2 | Reviewer identifies needless subsystem but Coder code not yet written | Reviewer returns precise CHANGES_REQUIRED; Coder revises text, not source |
| D-REVIEW-3 | Reviewer PASS | Reviewed per-file/interface component list can be read from accepted proposal with no new registry |
| D-RISK-1 | Small Lisp test proposes drawing rebinding and cross-Job state manager | Reviewer flags SMALL FUNCTION → BIG SOLUTION → LARGER SYSTEM IMPACT despite technical feasibility |
| D-RISK-2 | Reviewer cannot establish a proportionate solution | HUMAN_ESCALATION BEFORE code, not automatic PASS or architecture invention |
| D-RISK-3 | Human elects to test Lisp personally | Coder delivers Lisp/instructions; no automated test subsystem; native PASS remains UNVERIFIED until observed |
| D-HOST-1 | A mock parser says Lisp "passes" but actual CAD has not run | Do not claim native AutoCAD PASS |
| D-HOST-2 | A test drawing opens inside same AutoCAD process | Do not claim crash isolation or disregard binding impact |
| D-BROWN-1 | A Job update is proposed through a new draft-per-edit lifecycle | Reviewer rejects unjustified duplication if verified V5 final-source tools suffice |
| D-LEAD-1 | Worker only sees its own Task's proposal | Worker review cannot claim cross-workstream design PASS without combined relevant proposals |
| D-LEAD-2 | Worker has approved Task/worktree and cloud usage is exhausted | Worker can continue allowed coding/test without inventing new authority |
| D-CONTEXT-1 | Only Coder task is active | Do not preload Advisor/Planner/irrelevant skill metadata by policy; report host injection limits separately |
| D-MODEL-1 | Optional 27B model produces executable skeleton | Skeleton creation is *after* Pre-Code review and is tested as implementation, not mistaken for the proposal |
| D-GOV-1 | Discussion Job or pre-code review is invoked | No new Criteria re-approval, compulsory Advisor consultation, user technical design gate, global registry or job lifecycle is created |

All these are **design acceptance tests for this upgrade**, not claims that the present Bootstrap runtime implements them. Measured enforcement requires real tool/host evidence, not an instruction file alone.




## 6F. Conversation decision coverage — content preserved, not just headings

This is a *plan-local trace table* of distinct design decisions settled in the discussion. IDs here are coverage handles for **this draft**, not a claim that Secretary has already written permanent DEC files. Later Secretary may link/migrate them to actual decision records with unbroken provenance. On future revisions, reviewers compare **the right-hand operational rule** with the proposal/runtime, not merely the left-hand name.

| Plan-local ID | Actual decision that must survive | Normative specification / falsification |
| --- | --- | --- |
| CD-01 | Discussion Job is optional | E2: explicit request opens; generic discussion asks once; no automatic classification/gates |
| CD-02 | Secretary faithfully records a settled expert solution | E2: exact solution, rationale, exceptions, examples, exclusions, provenance and status; no shortened topic-only record |
| CD-03 | Decisions survive correction and handoffs | E2/E3: immutable readable history + supersession and active link; no loss on Plan revision |
| CD-04 | Planner references rather than re-invents accepted domain solutions | E3: Goal/Task/acceptance depends on full DEC link; coverage/conflict/feasibility reviewed |
| CD-05 | Planner retains ability to research and challenge *before* acceptance | E3: critical feasibility and alternatives remain possible; no blind agreement or silent rewrite |
| CD-06 | Coder is software engineer, NOT domain expert | E4: no invented professional rule, operational logic or host assumptions |
| CD-07 | New solution-clarification skill is Goal/Job-Pack scoped | E4: asks only consequential missing operational foundation or professional solution, not function-level trivia |
| CD-08 | Fully documented Goal means NO repeat questions | E4: Coder proceeds to code-design response if Plan/decisions already sufficient |
| CD-09 | Coder response is source-technical | E5: future file paths, actual functions/gates/contracts/callers/interface fields, dependencies, test mechanism; not a business story |
| CD-10 | Coder proposal is tied DIRECTLY to Detailed Implementation Plan/Task List | E5: each Task ID, related requirement/decision, verified source and proposed changes traceable; not independent Technical Plan |
| CD-11 | Pre-Code creates ONE descriptive proposal, NOT application files | E1/E5: no empty source/stubs or modified existing files before Reviewer PASS |
| CD-12 | Coder is not required to optimize the whole system | E5/E8: Coder proposes per Task; Reviewer compares across all relevant Task proposals |
| CD-13 | Reviewer sees the "empty shell" across Tasks | E8: cross-Task file/module/function/caller dependency assessment and missing links before code |
| CD-14 | Consolidated technical list is an OUTPUT of Reviewer PASS | E8: only corrected reviewed proposed components are listed; no Coder-authored registry before review |
| CD-15 | Greenfield and Brownfield share a protocol, not identical evidence | E6: Greenfield names proposed files; Brownfield reads real source/callers, preserves current working code |
| CD-16 | Reuse beats generic new framework where applicable | E7/E8: source-supported REUSE/MODIFY before CREATE; unnecessary drafts, services and duplicate gates challenged |
| CD-17 | Technical feasibility alone is not sufficient | E9: value/cost/risk proportionality checked even when solution could be coded |
| CD-18 | **Small Function → Big Solution → Larger System Impact** must be explicit | E9: reviewer traces system cascade, higher bug/regression risk and affected stable subsystems |
| CD-19 | Reviewer may not know a simpler domain-specific answer | E9: do not invent one; ask Human if no adequate simple safe approach |
| CD-20 | Human can choose partial/manual work instead of automation | E9: direct test, manual LOAD/verification, reduce scope/defer/drop; no fake PASS |
| CD-21 | AutoLISP executes in a real AutoCAD host | E10: mock/sandbox cannot be claimed as native geometry or command verification |
| CD-22 | Opening another DWG in same CAD session is not isolation | E10: same process crash blast radius; binding switch can affect Jobs and spawn new infrastructure |
| CD-23 | AutoCAD Undo Group is a conditional reversible edit mechanism | E10: helps supported DWG changes, no process crash guarantee or external effects rollback |
| CD-24 | CadGPT Create Job must not be redesigned with draft-per-update | E7: existing final Job source + real run + publish as distinct discovery action; preserve accepted V5 model |
| CD-25 | Lead and Worker are execution profiles, not tier/model rank | E11 + Sections 1–3: scoped authority; Codex also Coder; Worker Coder/Tester/Reviewer; reviewed handoffs |
| CD-26 | Context should load only what is relevant | E11 + Section 5: no global metadata of inactive roles; host-injected limits acknowledged |
| CD-27 | Cloud/local parallel workflows need real scoped enforcement | E11 + Section 4: verified native hooks, worktrees, no pretend sandbox/permission from text alone |
| CD-28 | 27B-created real skeleton/small-model fill is optional and post-design | E11 + Section 6/M6: benchmarks and real tests; never confuse executable skeleton with descriptive proposal |
| CD-29 | Optimize total completion cost and quality | Section 6D/M1/M7: add pre-code/review cost, implementation, native testing, rework; no universal savings claim |
| CD-30 | No Criteria change or invented gates | Section 0/6A–6E/8: keep already approved product Criteria, Advisor trigger, branch authority and existing Human decisions |
| CD-31 | Reviewed changed Phase/Plan retires ALL unfinished work inside its scope | G1/R-01/R-02/R-03/R-20: completed results checked; no per-unfinished-Task KEEP/REPLACE debate |
| CD-32 | RETIRED covers Plan revision, Phase, Milestone, Job, Task and exclusive branch | G2/R-03/R-06/R-10/R-11: logical status and provenance at the owning artifact; shared/protected refs remain safe |
| CD-33 | Obsolete READY/IN_PROGRESS work does not block current Job closure | G3/R-04/R-05/R-13: fence, safely settle, remove obsolete checkpoint/queue obligations, no fake PASS |
| CD-34 | New work uses fresh Milestone/Job/Task identities and reviewed proposals | G1/G3/R-01/R-09/R-16: no old task IDs revived, no old Proposal PASS inherited |
| CD-35 | Running work cannot be assumed remotely stopped or rolled back | G3/R-04/R-05/R-19: settle Run/cursor/host effects with actual evidence before terminal retirement |
| CD-36 | Reuse GSA authoritative retirement; no duplicate lifecycle engine or automatic Git deletion | G0/G2/G4/R-10/R-11/R-14/R-15/R-18: idempotency, client/schema tests, branch protection |
| CD-37 | Changed Phase causes whole unfinished scope reset, not Task-by-Task triage | G1/R-01/R-02/R-20: completed work reviewed for reuse; rest retired regardless of speculative individual salvage |
| CD-38 | Branch RETIRED is logical and must not erase unique source | G2/R-10/R-11: exclusive work branch retired, physical Git ref preserved until separate authorized checks |
| CD-39 | Tester SIMULATE means real user entrypoint → actual invoked flows → visible outcome | H1/S-01/S-02/S-12: no unit/mock/prose-only PASS |
| CD-40 | Tester scenarios ascend single Task → normal sequence → interleaved/random → adversarial | H2/S-01/S-03/S-06/S-09: risk-scaled reproducible scenarios, no unsafe destructive testing |
| CD-41 | One user action may spawn accidental parallel flows | H3/S-02/S-04/S-05/S-11: trace flow IDs, causal spawn, queue/lease/wait graph, terminal state |
| CD-42 | Three genuine Coder fix + independent Tester retest cycles maximum | H4/S-13: same defect, original user trigger replay, no fourth routine patch or counter reset via Job split |
| CD-43 | Failed third cycle invokes advanced root cause skill rather than blind repair | H5/S-13/S-14: deeper multi-flow causal investigation and report before more code |
| CD-44 | A correct unit/CI result is not user-path acceptance | H1/H3/S-12/S-15/S-16: real exposed app routing and host evidence, UNVERIFIED when unavailable |
| CD-45 | Native skill reuse, no new persistent Tester/Bug Fixer agent | H0/H5/H6: existing bug-fix and systematic-debugging skill upgraded; new focused skill only if needed |

**Coverage rule:** A later abbreviated plan summary can link to CD-01…CD-45 and their full sections, but cannot replace these rules. Deleting or changing a CD line requires evidence of a subsequent actual Human change to that decision, not a stylistic compression.


## 6G. Revised Human decision — RETIRE entire unfinished changed scope, rebuild fresh work topology

**Decision revision — 2026-10-24:** The former per-Task KEEP/REVALIDATE/REPLACE analysis within a replaced Phase is **SUPERSEDED**. Human chose a simpler rule: when an accepted implementation direction changes, **all UNFINISHED work within the changed Plan boundary is RETIRED**, while completed work is examined for reusable results. Create new Milestone/Job/Task identities for the replacement work. The purpose is to eliminate old READY/RUNNING duplicates, stale obligations and zombie Jobs without an expensive Task-by-Task salvage process.

### G0. Source-grounded status and boundaries

- Standalone Bootstrap currently has TASKS.md Active/Next/Done/STALE/Blocked and a single active-task.json using ACTIVE/NOT_CONFIGURED; no verified standalone Plan/Phase/Milestone/Job/Task retirement execution.
- GSA already recognizes Job/Task RETIRED, with reviewed Plan-change intent, dispatch fence, exact-SHA transitions and Run/cursor settlement; however its current generic per-Job Plan reconciliation does NOT establish complete **scope-wide Phase/Milestone/Plan revision retirement**. Inspect/extend the owning GSA operations only when needed rather than cloning its runtime.
- GSA has a separate source-branch retirement contract. The 2026-10-23 deploy note documents a runtime rollout, **not an E2E PASS on a real Job**; old registered plugin schemas may reject RETIRED. Verify actual connected behavior, not just source enum declarations.

### G1. Select changed boundary once, not each unfinished Task

1. On an authorized, reviewed Plan revision, determine **which Phase boundaries are replaced**. If several Phases changed, use their union. If the entire Plan is reworked, the whole old Plan revision is the affected boundary. An explicitly defined smaller independently replaceable unit may be used only when it already exists in the Plan topology; do not invent a new hierarchy for this purpose.
2. **Examine COMPLETED items only for output reuse**: preserve their historical identity, PASS and evidence; check whether their result still meets the newly agreed solution. If valid, explicitly reference that result in the new scope. If incompatible, preserve history but create new work; no retroactive RETIRED status for completed work.
3. **Every other unfinished item in the changed boundary automatically RETIRES**, including PLANNED/DRAFT, READY, IN_PROGRESS, BLOCKED/WAITING Job/Task work and unfinished Milestones. Do NOT apply a per-unfinished-Task KEEP-vs-REPLACE analysis to save the old plan.
4. Rebuild the changed portion as **fresh Phase revision/identity, new Milestone IDs, new Job IDs and new Task IDs**, updated dependencies/acceptance and a new applicable Code Structure Proposal/Reviewer review. Do not just rename old READY Task IDs or inherit a stale Pre-Code PASS.
5. Outside changed boundaries, all independent Phases/Jobs/Tasks remain intact. Only actual crossing dependencies need targeted review for valid upstream deliverables/replacements. No blanket retirement of unrelated work.
6. A **draft or discussion** of changes does not retire anything. The action is applied at the current existing authorized Plan-review checkpoint, with no new Human/Advisor gate.

**Example — one Phase changed:** Phase P2 currently has two COMPLETED Tasks, three READY Tasks, two IN_PROGRESS Tasks and one incomplete Milestone. Human changes the solution used by P2. Verify the two completed outputs, mark **all five unfinished Tasks and that incomplete Milestone RETIRED**, terminate/retire obsolete P2-owned Jobs after safe Run settlement, retire old Phase P2 revision and create replacement Phase/Milestone/Job/Task IDs. P1 and P3 remain unchanged.

**Example — multiple Phases or whole Plan:** Human replaces the approach across P2, P3 and P5: do a completed-work reuse review for each, RETIRE **all** remaining unfinished structures inside P2/P3/P5 and the exclusive branches that belong only to that old work, and create new topology. For an entire Plan rewrite, logically retire its old revision and unfinished topology, then create new Plan revision with fresh Phase/Milestone/Job/Task identities; keep the old plan and historical PASS readable.

### G2. Retirement applies to Plan, Phase, Milestone, Job, Task and source branch

| Artifact | Meaning and record |
| --- | --- |
| **Plan revision** | Logically RETIRED when superseded as a whole; preserve the old approved Plan content, decision refs, reason and link to current revision. Do not delete the canonical Plan file or all valid unchanged Phases because one Phase changed. |
| **Phase** | The replaced Phase revision is logically retired and its unfinished children retire. If Phase is a section of a Plan, annotate it in the existing Plan history/trace; do not create a Phase database just for status. |
| **Milestone** | Every unfinished Milestone in changed Phase is retired; it cannot keep its old checkpoint/evidence requirements active in the new Plan. New scope gets fresh Milestone ID. Completed Milestones remain historical. |
| **Job** | Every unfinished Job in changed Phase retires once active Runs settle. Fresh Job IDs represent new implementation work. Broad retirement needs NO one-to-one successor for every old Job, even if new work is conceptually similar. |
| **Task** | Every unfinished Task under changed scope retires, including READY or IN_PROGRESS; no new dispatch or unfinished closure obligation. |
| **Run** | No invented Run.RETIRED state: settle actual running work, possibly CANCELLED with Plan-change reason, before terminal parent transition. |
| **Git repo branch** | Exclusive work branch owned only by retired scope is logically RETIRED and ineligible for future code, merge/deploy, with exact ref/head SHA and lineage. Physical ref deletion is separate, never implicit. New work uses a fresh authorized branch from a verified approved base; carry forward only deliberately accepted source. **Do NOT retire/delete main, default, Release/active integration or a shared branch with unaffected work.** On a shared branch retire obsolete scope claims and isolate new work, or raise the specific branch-ownership decision. Preserve unmatched commits and open PR facts. |

**Term distinctions:** RETIRED means obsolete old unfinished work, not deletion, rollback or PASS. SUPERSEDED remains historically valid for explicit one-to-one replacements outside this scope-wide policy. CANCELLED means actual Run/operation interruption, not Plan retirement; STALE is unknown applicability, not retirement. COMPLETED history is preserved and only its output reuse is assessed.

### G3. Exact safe execution order

~~~text
Human changes solution → Planner revises Plan → existing Reviewer/Human authority
→ identify changed Phase(s) / whole Plan boundary ONCE
→ fence new dispatch and source-step continuation for old affected scope
→ inspect COMPLETED outputs for valid reuse (not all unfinished Tasks)
→ for unfinished READY/DRAFT: record terminal RETIRED, read back
→ for unfinished IN_PROGRESS:
   inspect real Runs, tools/host writes, cursor, Git branch/HEAD/tree
   settle at safe boundary; if UNKNOWN/PENDING keep fenced, DO NOT fake RETIRED
   write RETIRED when safe, with Plan-change reason/provenance/readback
→ retire replaced Phase/Plan revisions and exclusive job-owned branches logically
→ create NEW Phase/Milestone/Job/Task identities + fresh authorized work branch
→ validate cross-boundary dependencies / current closure obligations
→ new relevant Code Structure Proposal + whole-Task Reviewer
→ dispatch only current authorized work
~~~

- A fence prevents **new** dispatch, not an automatic cross-chat hard stop or rollback of a CAD/Git tool already executing. Do not repeat an uncertain non-idempotent action or discard committed source. Preserve evidence, diffs, unique commits and observable effects.
- Do not mark an IN_PROGRESS Job terminal until its active Run/source/cursor has been reconciled. UNKNOWN/PENDING remains clearly NEEDS_RECONCILIATION, not magically retired.
- Idempotent retry: one reviewed Plan-change identity maps to one retirement action set and one new-work topology. Rerunning may not mint duplicate Job/Task/branch identities, repeat source writes, or turn unrelated work terminal.
- A retired Job/Task is not a PASS but **is no longer pending** for old/current closure. Current Job acceptance uses only current reviewed obligations and explicitly re-accepted completed outputs; obsolete READY work must not block closure.

### G4. Ownership and implementation limits

When Bootstrap runs via GSA, **GSA owns durable Job/Task/Run transitions** and already has some of the tools. Adapt Plan-scope selection and lifecycle integration there if needed; Bootstrap Planner/Reviewer skills route and verify, not create a shadow control plane. When Bootstrap runs alone, use existing Plan/Milestone/Task artifacts and actual dispatch authority; add a minimum retirement guard only when needed and verifiable.

Branch retirement is a **logical authority restriction**; do not auto-delete Git refs or retire protected/shared integration branches merely because they contain old code. If changed work shares a branch with valid work, preserve the valid work and retire only obsolete work claims. A new Phase does not imply a new remote repository or separate Git history.

### G5. Scope-wide retirement acceptance (previous per-Task R-01–R-14 meanings SUPERSEDED)

| Case | Starting condition | Required observation |
| --- | --- | --- |
| R-01 | One changed Phase, two COMPLETED and five unfinished Tasks | Completed results evaluated for reuse; all five unfinished RETIRED, fresh replacement IDs |
| R-02 | Three of five Phases changed | Unfinished work in all three retired; other two untouched |
| R-03 | Entire Plan changed | Old Plan revision/topology logically retired, fresh Plan/Phase/Milestone/Job/Task identities; historical output preserved |
| R-04 | IN_PROGRESS Job in retired Phase | Fence new work, settle actual Run/cursor/source effect before terminal |
| R-05 | Pending/UNKNOWN host or Git write | Remain fenced/NEEDS_RECONCILIATION, no false RETIRED/duplicate write |
| R-06 | Old READY Job/Task or unfinished Milestone | All non-dispatchable, no obsolete checkpoint blocks new closure |
| R-07 | Completed result still applicable | Historical PASS intact; explicit result reuse by current new scope |
| R-08 | Completed result no longer applicable | Historical PASS intact, new work required, not retroactive RETIRED |
| R-09 | Retired work has conceptually similar new requirement | New unique Job/Task/Milestone IDs with Plan lineage, not resuming old |
| R-10 | Exclusively owned old branch contains unmerged unique commits | Logical retired status and retained remote ref/history, no auto-delete/merge |
| R-11 | Shared/default/release/integration branch | Remains active/protected; retire old write claims, new work branches safely |
| R-12 | Another Phase depends on old completed work | Check only crossing dependency, do not retire whole unaffected Phase |
| R-13 | Old READY/IN_PROGRESS jobs remain in queue during revision | Dispatch rejects old scope, no zombie closure blocker after safe terminal |
| R-14 | Restart after interrupted retirement | Same intent, same IDs, no duplicate work or source mutations |
| R-15 | Connector schema lacks RETIRE though runtime source has it | Show UNVERIFIED/client mismatch, never bypass authority |
| R-16 | Old Code Structure Proposal was reviewed PASS | PASS revoked for replaced scope; new proposal/review required |
| R-17 | Human only discusses a possible Plan change | No retirement until existing reviewed authorization |
| R-18 | Standalone mode lacks enforced Task RETIRED state | Report precise guidance-only vs tool-enforced limitation |
| R-19 | Run cancelled as part of Plan retirement | Run CANCELLED with cause; Job/Task RETIRED only after settlement |
| R-20 | Partial Phase change with many unfinished Tasks | One enclosing-scope sweep; no per-unfinished-Task salvage/classification debate |

**Non-goals:** no global cleanup daemon, Task-salvage arbitration system, GSA shadow lifecycle, automatic branch ref deletion, evidence erasure or new Human approval gate.

---

## 6H. Tester simulation from REAL USER TRIGGERS and 3-cycle debug escalation

**Human decision, 2026-10-24:** Tester must SIMULATE **people using the application**, not merely call the nearest implementation function and claim its logic is correct. Simulated users start with an actual or faithful app entrypoint, perform realistic interactions, vary timing/order, and ultimately attempt disorderly/adversarial use. Tester must trace **all flows activated by each user action**, including accidental concurrent workflows, waits, state and exclusive capabilities. For an unresolved bug, allow at most **three Coder repair → independent Tester retest cycles**, then STOP routine patching and invoke **a more advanced root-cause debugging skill**.

### H0. Verified present capabilities and what is missing

Current Bootstrap project-template/.agents/roles/tester.md, skills/bug-fix-loop/SKILL.md and skills/systematic-debugging/SKILL.md already require minimal reproduction, root-cause reasoning, regression tests and stopping blind repair after three unsuccessful repairs. Some hosts may provide native superpowers:systematic-debugging. Existing GSA lesson docs/process/lessons/BUG-FIX-ROOT-CAUSE-SIMULATION-2026-10-05.md documents end-to-end caller/state/runtime investigation and post-CI behavioral simulation but was a candidate lesson.

**Gaps:** no complete requirement to **start as a user triggers the feature**, exercise realistic randomized and interleaved user-action sequences, observe all actual spawned subflows, and detect hidden race/deadlock/duplicate work; no distinct higher-depth diagnostic workflow reliably invoked after the failed **third** full Coder/Tester cycle. Do not mistake a previously written generic skill title for verified execution.

### H1. What SIMULATE must mean, in executable terms

**Not sufficient:** an imagined story, function unit test, successful mock or CI alone, fabricated UI clicks, or textual call graph declared "SIMULATION PASS."

**Start at the application-facing boundary, whenever an authorized host is available:**
- user opens app, presses an actual button, sends a prompt/command, selects a CAD/Revit element, uses a tool through its public connector, changes app state or performs another user-level action;
- Tester records exact initial app state, environment, input, user intent, expected final UI/host result and the exact source/runtime revision;
- activation must traverse actual deployed/presented UI → public entrypoint → router/dispatcher → Job/Task/tool/Lisp/command → callbacks/event handlers → shared capabilities/state/persistence → actual host when needed → result returned to the user;
- capture **each child flow spawned by that one input** (flow IDs, causal parent, expected vs observed number, owner, dependencies, waits, leases/locks, writes, completion status, errors);
- report both **correct outward result** and **internal operational safety**, not simply whether one function returned success.

Use an actual host for the critical acceptance whenever possible. For inaccessible external hosts, a bounded executable simulation may call the **real production dispatcher and important logic** with controlled dependencies and deterministic event scheduling; identify it as SIMULATED only, and **REAL HOST UNVERIFIED** for untested native effects. A mock AutoCAD cannot prove actual AutoCAD command/geometry/save correctness, nor process-crash isolation. The Human may choose manual host testing; Tester must label pending evidence, not pretend to have run it.

**Required scenario/test evidence shape:**
~~~text
Scenario ID; scenario level; deterministic seed/order where relevant
User entrypoint: <actual button/prompt/public connector command>
Initial state: <document binding, active Job/Run, queued operations, session>
Input sequence: <each user interaction, with ordering and overlap>
Expected user-visible result; expected number/ownership of background flows
Observed graph:
  User event U1 → UI/API entrypoint E1 → router R1
  R1 → child flow F1 (why launched, which Job/Task)
  R1 → child flow F2 (why launched, expected or accidental?)
  F1 / F2 → exact queue/capability/state owner → host command/persistence
  callbacks / retries / completions → final user-visible output
For every flow: inputs, calls, state reads/writes, waits, lease ownership,
  return/error/terminal status and any late event.
Assertions:
  correct request routing; allowed vs unintended flow count;
  correct serialization/exclusivity, no deadlock, no leaked lease;
  no duplicate side effect; correct binding and persisted state;
  no stale Run/Job, no false DONE; expected UI/host output.
Evidence: observable trace/log/ref/screenshot, real vs simulated boundary,
  expected vs actual, failure classification and reproduction steps.
~~~

Do not impose a universal event-bus logger or new monitoring service just to support a tiny test: use existing traces, host tools, debugger instrumentation and bounded test harness when sufficient. Introduce instrumentation only if it addresses a proved observable gap without substantially changing runtime behavior.

### H2. User behavior simulation ladder — from one happy path to troublemaking

Tester selects **risk-proportionate** representative scenarios (not necessarily hundreds for every trivial function), in increasing behavioral complexity:

**S1 — Single legitimate Task / happy path:** one ordinary user action starts the expected one Task/Job path and returns an observable correct result. Validate activation itself and ensure one action has not accidentally spawned extra child jobs.

**S2 — Realistic sequential user workflow:** a person performs two or more normal actions in natural order: create, edit, run, save, switch tab/view where allowed, reopen, repeat. Test dependent operations, persistence, user-visible notifications and completion.

**S3 — Realistic interleaving, concurrent and random behavior:** while action A runs or is awaiting an event/callback, user triggers B, retries, clicks repeatedly, sends another chat prompt, switches allowed UI state, or another Job performs an independent action. Include both compatible concurrent work and exclusive resource conflicts; vary order/delays with reproducible fixed seeds or explicit barriers. Do not declare that ALL parallelism is wrong: only simultaneous actions that violate the actual host/capability contract.

**S4 — Adversarial/disorderly user behavior:** send invalid/stale inputs, issue commands out of order, spam/duplicate a request, cancel during a pending operation, close/reconnect/restart during a Task, force child-flow failure, edit a Plan while old Tasks are READY/IN_PROGRESS, choose conflicting drawing/tab, and attempt combinations a careful normal user avoids. Observe graceful refusal/recovery, lifecycle correctness and leak-free termination.

**When the real host is stateful/destructive:** use the approved real execution environment, user-approved safety precautions, reversible checks where feasible, or safe staged tests. Do not execute destructive stress tests on a live user's production drawing just because a scenario is conceivable. Missing real-host proof stays UNVERIFIED; a Human may prefer to run Lisp manually.

### H3. Trace multiple flows for ONE user action — CadGPT regression anchor

CadGPT has a single primary bound drawing in a CAD session, and CAD commands/Lisp using one exclusive CAD capability must not run concurrently on that host; other independent SYSTEM/file processing may proceed concurrently where permitted.

**Example bug class:** User requests one action to Create/Run a Job. A handler, callback, retry or duplicate routing accidentally starts TWO subflows for the same input. Flow F1 acquires CAD capability while F2 waits for a CAD command or event, or two flows hold mutually dependent states; one never settles. Each local function might pass its unit test. The user sees a stuck Job or inaccurate DONE.

**Tester must establish causal evidence:**
1. Identify the **one** user event and its expected outcome; do not start by calling an internal queue helper.
2. Determine which public handler/router was actually activated; compare configured vs deployed tool/connector surfaces.
3. Record every spawned child, Job, Run, request ID, callback/retry and reason; expected vs observed graph. Ask **why** the second flow exists.
4. Read each flow's CAD lease/queue ownership, wait-for edges, shared drawing anchor/binding, persistent state and cleanup conditions.
5. Check for cycle or permanent wait, double execution, early DONE, orphaned token or state touched by the wrong flow.
6. Reproduce with controlled interleaving/seed; change one factor to distinguish duplicate dispatch from serializer error, callback race, missing release, process/binding error or stale client schema.
7. Confirm after the repair by replaying **the same real user event** plus an overlapping interaction; do not replace this with only a passing test of the patched helper.

Do **not** solve this automatically by inventing a second global scheduler, test runner, CAD mutex framework or source manager. Inspect existing serialization/capability leasing first; Reviewer's Small Function → Big Solution → Larger System Impact escalation still applies.

**Important:** A "simulation" that invokes mocked Lisp functions without traversing real command registration, CAD adapter and ownership does NOT verify this bug class. Simulation fidelity must be stated explicitly: which real layers were executed, which were stubbed and what claims remain unverified.

### H4. Exactly three full Coder-fix/independent-Tester-retest opportunities per defect

The counter belongs to the **same defect/root user-visible symptom and reproduction scenario**, not to Job ID, chat, Coder hypothesis or newly named duplicate bug. One counted cycle is **Coder changes an authorized implementation** followed by **independent Tester actually rerunning the original user trigger, the failing behavioral scenario and relevant regression**.

~~~text
Tester discovers failure from actual app-user behavior → Defect OPEN
→ Cycle 1: Coder diagnoses/repairs → independent Tester retest
     PASS? close with real evidence. FAIL? retain same defect, add evidence.
→ Cycle 2: Coder revises diagnosis/repairs → independent Tester retest
     PASS? close. FAIL? retain same defect, add evidence.
→ Cycle 3: Coder revises diagnosis/repairs → independent Tester retest
     PASS? close. FAIL? STOP ordinary patch/retest.
→ invoke advanced-root-cause diagnostic skill or proven native equivalent (H5)
→ investigate and explain cause before any further implementation
→ if architecture/decision must change: Coder new proposal → Reviewer, Human only if needed
→ resume only on a genuinely revised evidence-based approach and current authorization
~~~

- A Coder self-check or CI green alone is not independent Tester PASS. Retest may fail because test fixture, tool connection or host is unavailable; classify accurately. UNVERIFIED is not a false Product FAIL or PASS and must not silently reset retries.
- If a **serious structural/race/shared-state problem** is already apparent earlier, trigger advanced investigation before reaching three attempts; three is a **maximum**, never an instruction to perform three speculative patches.
- If the same defect is renamed or assigned to a new Job, the three-attempt history stays linked; splitting records does not evade the stop rule. Unrelated genuinely new bugs have their own identities.
- Tester never writes product source. Coder owns authorized repair; post-repair independent Tester repeats the original user action. Reviewer judges changed cross-module architecture where applicable.
- Do not create a mandatory Human approval after ordinary three-cycle debugging. Ask Human only for missing host access, material scope/domain/risk decision, or unavailable necessary external action.

### H5. Advanced root-cause skill (escalation, not a fourth patch)

**Entry:** three failed full fix/retest cycles on the same defect OR earlier evidence of an architectural/cross-flow failure that cannot be responsibly fixed by a local patch.

1. Stop patching. Capture exact failing revision, tested source/runtime, scenario seed/action sequence, log/event graph and the **three attempted fixes/results**.
2. Load **a genuinely deeper available root-cause skill/tool**. Start with existing installed native systematic-debugging capability and project-local equivalents; if none includes full multi-flow causal analysis, define a focused advanced-root-cause-analysis skill or stronger mode of the current debugging skill. Do not add a persistent Bug Fixer agent/service. Record whether skill loading actually occurred; if not available, mark that limitation.
3. Reconstruct the **whole** entrypoint-to-user-result call graph and causal event timeline, including UI/connector exposure, dispatchers, caller-of-caller, sibling implementations, async callbacks, resource acquisition/release, wait-for graph, Job/Task/Run states, branch/document binding, persistence, process/reload boundaries, real external host and UI completion.
4. List **all plausible root-cause sites**, rank against observations and systematically eliminate wrong hypotheses using bounded discriminating experiments (one variable, deterministic interleavings, trace/replay, compare working vs failing path).
5. Identify the **first diverging causal event**, not merely the nearest exception. Confirm if the symptom stems from wrong tool selection, duplicate route, deadlock, race, obsolete code path, stale deployed/plugin schema, missing host, mock fixture or true product logic.
6. Deliver an **Advanced Defect Report**: original user action, exact reproduction, expected/actual, flow map + wait graph, seed/events, three attempts, experiments, root-cause evidence/confidence, minimal proportionate remediation, risk, acceptance replay and residual UNVERIFIED gaps.
7. Do not automatically issue a fourth fix. When evidence demands changes to shared contracts, major architecture or accepted solution, update Code Structure Proposal and return through existing Reviewer/Human routes before new code. When an evidence-based narrow fix is identified within accepted scope, authorize the next controlled repair under existing rules and retest from the real user entrypoint.

**Why:** This interrupts the failure pattern user-visible bug → patch nearest function → CI green → still broken in the actual application → repeated patching elsewhere. The target is a complete causal explanation and a user-behavior replay, not an elaborate new test infrastructure.

### H6. Observable simulation/debug acceptance scenarios

| Case | User trigger / condition | What Tester must demonstrate |
| --- | --- | --- |
| S-01 | One normal user command, one Task | Genuine user entrypoint → real router/Job path → correct result; no unintended second Run |
| S-02 | One click produces two child flows | Capture both spawned flow IDs, causal parent, expected-vs-actual multiplicity and waiting state |
| S-03 | Normal create → run → save → reopen | Correct state/host persistence and outward user outcome |
| S-04 | Action B arrives while A owns exclusive CAD capability | Legitimate CAD commands serialize; independent permitted SYSTEM work may run without deadlock |
| S-05 | Two chats use same bound DWG | No illegal CAD command overlap, wrong binding, stale Job ownership or false DONE |
| S-06 | User repeatedly clicks/submits requests | No unintended duplicate mutation, leaked lease, ghost Job or silent overwrite |
| S-07 | Cancel/reconnect during pending callback | Known terminal/pending state, no unsafe automatic replay and no orphan wait |
| S-08 | User changes tab/drawing mid-Job | Approved binding semantics honored; no automatic rebind unless actually authorized |
| S-09 | Reproducible randomized valid/invalid action sequence | Fixed seed/order/trace reproduces found defect or reports uncertainty |
| S-10 | User edits Plan with READY/RUNNING old Jobs | Scope-wide retire fence prevents obsolete dispatch, race and zombie Job closure |
| S-11 | One of two child flows fails | User-facing failure/partial result accurate, other flow terminates or remains explicitly pending |
| S-12 | Only test-fixture/mock simulation available | Result marked SIMULATED and real host UNVERIFIED, no fabricated acceptance PASS |
| S-13 | Coder fixes + independent Tester retests fail three times | Same defect/attempt history, STOP a fourth routine patch, advanced skill invoked or unavailable clearly reported |
| S-14 | Deep diagnosis indicates a shared contract/architectural flaw | Coder revised technical proposal + Reviewer before source changes, no speculative infrastructure |
| S-15 | CI/unit green but real user flow hangs | Tester FAIL with causal trace, no CI-only closure |
| S-16 | App/plugin restart changes actual exposed entrypoint | Test registered vs externally callable surface and actual lifecycle, not code presence alone |
| S-17 | Destructive adversarial test unsafe on production DWG | Do not execute without suitable authorization; report UNVERIFIED/manual alternative |

**Implementation fit:** Extend the existing Tester instructions, test-and-verify, bug-fix-loop and systematic-debugging skill routing; optionally a focused user-behavior-simulation Tester skill and advanced-root-cause-analysis mode ONLY if actual native/local capabilities are insufficient. No new Tester role, Job state, general simulated application framework, fake sandbox or permanent test manager. Tester writes test scenarios/evidence in existing test locations; exact host adapters implement only supported real interaction.

---

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

Inspect real Bootstrap installer/roles/skills/harness, approved-criteria protections, native host adapters and hook events, Lite/Standard/Full tiers, Branch Authority, Worktree behavior, session/handoff, Planner/Reviewer coordination, present Coder sequence, existing decision storage, **Plan/Phase/Milestone/Job/Task/branch retirement coverage**, GSA actual runtime/connector schema capabilities and **Tester user-entrypoint simulation plus existing 3-cycle/systematic-debugging skill coverage**. Characterize greenfield and brownfield needs and missing support for QwenCode. Establish reproducible Codex/QwenCode baseline: context injected/loaded, latency, tool calls, token use, total time, correctness, test/rework and material scope drift.

**PASS:** Real-source gap map and baseline; evidence separates verified operation from instruction-only guidance, identifies decision loss and pre-code gaps. Measurement instrumentation, if needed, receives an appropriately reviewed minimal design before code.

### M2 — Single solution design and Reviewer check

Finalize optional Discussion Job activation, Secretary decision schema/index/supersession, stable reference links, Planner coverage/conflict/feasibility behavior, **changed-boundary Phase/whole-Plan RETIRE for every unfinished Plan/Milestone/Job/Task and exclusive branch, completed-result reuse, new IDs, safe Run settlement and current closure (6G)**, Coder domain boundary and solution-clarification skill, Code Structure Proposal file format and per-Task fields, combined Reviewer protocol, complexity escalation and manual alternative. At the same time finalize **H1–H6 user-triggered simulation ladder, flow-trace evidence and exact 3-cycle fix/retest → advanced-root-cause skill routing**, Lead/Worker authority, Task Criteria/Goals, delegation schema, profile/role/context dependency matrix, native hook/worktree policy, Universal Core, existing tiers compatibility and non-goals.

**PASS:** One reviewed design; **CD-01–CD-45 checked against E1–E12, G0–G5 and H0–H6 with actual acceptance examples**, no rewriting of domain decisions, no proposed universal manager/registry/sandbox, no additional Human approval or Technical Advisor gate, clear host enforcement limitations.

### M3 — Decision preservation and Pre-Code workflow implementation

Implement **only necessary changes** to optional Discussion Job/Secretary record-keeping and Planner decision references. Integrate reviewed **changed Phase/Plan boundary → retire ALL unfinished Milestones/Jobs/Tasks/old branch ownership → create fresh work IDs** through the owning lifecycle (GSA if connected), with READY/IN_PROGRESS fencing, safe Run settlement, completed-evidence salvage, branch protection, dependency/closure checks and connector capability verification. Do not duplicate existing GSA control-plane code in Bootstrap. Add/modify Coder Instruction and the scoped solution-clarification skill; align implement-task and Reviewer instructions/adapters across supported hosts. Enable **descriptive** per-Task Code Structure Proposal and **whole-relevant-proposal** Reviewer consolidation, CHANGES_REQUIRED repair and HUMAN_ESCALATION. Reuse document/task stores and existing reviewer dispatch as far as feasible; do not create a second planning engine or source registry. **Extend Tester role + test-and-verify/bug-fix-loop/systematic-debugging skills to perform H1–H6 actual user-action scenario generation, multi-flow tracing and advanced root-cause skill escalation after failed third retest; new focused skill only when verified existing native/local capability is insufficient.**

**PASS:** (a) Accepted expert decision survives Plan rewrite/handoff with provenance and exceptions (E2–E3, CD-02–CD-04); (a2) Retirement acceptance R-01–R-20 verified on applicable real authority paths, unsupported paths clearly flagged; simulation/debug acceptance S-01–S-17 verified at appropriate executable/host evidence level; (b) clear Task needs no repeated Human interview; (c) no source files modified during pre-code; (d) Reviewer detects needless duplicate gate/contract and requests simplification; (e) disproportionate feasible small function escalates to Human, manual-test choice respected; (f) only accepted reviewed proposal authorizes implementation under existing source-write rules.

### M4 — Profile-aware setup, native hooks and minimal context

Implement Lead/Worker profile-aware setup orthogonal to installation tiers, host-specific native rules (especially QwenCode), shared branch/path authority and isolated worktree provisioning. Preserve Codex Lead and Coder capability. Configure full role-scoped instructions + in-scope metadata, targeted activation and compact handoffs; do not promise control over platform-injected schemas or chat history. Verify existing multi-host installation, permission event semantics, bypass limitations, direct shell/MCP edit surfaces and conflicts.

**PASS:** Concurrent Codex/QwenCode profiles without corrupting shared config; verified scope protections and explicit gaps; Worker sees only relevant skills/instructions; Code Structure Proposal and decision links available to correct Reviewer/Coder.

### M5 — End-to-end delegated Coder/Tester/Reviewer operation

Lead prepares task contract/branch/worktree; Worker Coders receive accepted task and reviewed design, implement within allowed source scope; Worker Tester/Reviewer verify, then Lead cross-workstream review/integration checks. Exercise concurrent disjoint Tasks, Reviewer cross-Task consolidation before coding, discrepancy escalation, **actual user-action simulation S1–S4 with single-action, sequential, interleaved/seeded and adversarial flows**, **independent Tester/Coder/Tester cycle cap at 3 then advanced root-cause diagnosis**, FAIL→Coder fix→Tester retest, blocked/stop, **Plan/Phase scoped retirement and closure of all obsolete READY/IN_PROGRESS work including unique old source branch**, compact handoff and continuation of authorized local tasks while cloud quota unavailable. Preserve independent Lead verification and existing approval rules.

**PASS:** One full delegated greenfield and one brownfield representative Goal with real diffs, review evidence, regression tests and protected integration; accepted domain decisions and shared contracts survive role/session changes. Replay at least one real user-triggered two-child-flow concurrency defect and 3-failed-cycle advanced diagnosis with evidence; no fake native-host PASS.

### M6 — Optional multi-model code implementation benchmark

Only **after Pre-Code Reviewer PASS**, prototype capable ~27B model constructing an **actual source skeleton** for a suitable multi-module Goal, smaller local model filling narrow approved modules and running tests, then integration/Reviewer. Compare to one capable model implementing directly. Test syntax/build, interface compatibility, native host suitability, model-switch costs, regression and rework. **Do not confuse actual code skeleton with pre-code descriptive document.**

**PASS:** Representative evidence of lower total completion time with acceptable quality, otherwise leave disabled/optional; no extra gate on basic Coder execution.

### M7 — Full regression, efficacy and release decision

Regression cover greenfield and brownfield bootstrap, Criteria/Advisor trigger and human authority, Plan/Milestones, **scope-wide Plan/Phase/Milestone/Job/Task/branch retirement including completed-output reuse, fresh replacement IDs, safe Run/source reconciliation, dependency/closure, branch history, and actual GSA schema compatibility (R-01–R-20); user-entrypoint behavioral simulation and 3-cycle deep debugging escalation (S-01–S-17)**, Decision Ledger including supersession, refusal of unsanctioned theory change, Reviewer preservation of professional solutions, Coder solution clarification, source-free pre-code proposals, cross-Task deduplication, disproportionate-risk escalation/manual option, genuine AutoCAD Lisp host limitations as an example, Worker role/skill boundaries, branch/worktree/path hooks, parallel projects, cloud exhaustion, resume/handoff, Tester→Coder retest, installation tiers and independent checks.

Compare **end-to-end Goal cost** with baseline (cloud tokens and request sizes, local latency and total time, rework iterations, bugs/regressions, missed user decisions and complexity introduced). Never claim a universal percentage gain without data. Do not push a release/deployment until the ordinary reviewed authorization and real host evidence are complete.

**PASS:** CD-01–CD-45, R-01–R-20 and S-01–S-17 covered by actual test/evidence without semantics-only drift; no governance/decision drift; no unreviewed code-scope escalation; normal short Tasks remain friction-light; measurable benefits or explicitly documented neutral/negative results; deployment only by separate authorized action.

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
17. An approved Plan revision **retires ALL unfinished work within replaced Phase/Plan boundaries**, covering Plan revision, Phase, Milestone, Job, Task and exclusive work branch; COMPLETED output is reviewed for reuse, all new implementation gets fresh Milestone/Job/Task IDs. Safe Run/source settlement, historical preservation and current closure are mandatory. No Task-by-Task salvage of unfinished changed-scope work.
18. RETIRED does not require a one-to-one replacement Job; create a fresh reviewed topology for the changed boundary without inheriting stale PASS, rerunning uncertain writes or duplicating existing GSA lifecycle authority. Logical branch retirement never implies destructive ref deletion or retire of protected/shared branches.
19. Tester begins scenario verification with app-user entrypoints and traces every activated subflow from trigger through router, scheduling, state, host and user-visible outcome. Include progressive happy path, real workflow, deterministic interleaving and adversarial scenarios proportionate to risk.
20. Maximum **three Coder code-fix plus independent Tester full retest cycles per defect**; after unresolved third FAIL stop routine patches, invoke actual advanced multi-flow root-cause skill and return for architecture/Plan review only when necessary. A simulation/mock/CI PASS never certifies untested real-host behavior.

## 10. Immediate next step and stop condition

Review **this single draft** against the current source, Decision references and operational constraints, then perform M1 audit. Do not begin implementation work merely because this document was saved. Existing Criteria/Plan/Milestones and already-verified Bootstrap readiness remain authoritative; use the normal Reviewer and Human authorization path for actual changes.

**Recorded decisions consolidated in this draft (see full E1–E12, decision coverage CD-01–CD-45, scoped retirement G0–G5 and user simulation/debug H0–H6; NEVER substitute this paragraph for them):** One unified plan; optional Discussion Job + Secretary with precise accepted-decision records and supersession; reference-based Planner with decision fidelity; **scope-wide Plan/Phase/Milestone/Job/Task/exclusive-branch retirement on revised approved solution and new work IDs**; **Tester activation from real user actions with graduated interleaving/adversarial scenarios, flow causality and 3-cycle repair limit then advanced root-cause skill**; Coder as Software Engineer (not Domain Expert) plus focused solution-clarification only for missing consequential logic; per-Task descriptive Pre-Code Code Structure Proposal without source writes; Reviewer whole-proposal consolidation and PASS/rework/escalation; explicit **Small Function → Big Solution → Larger System Impact** review; Human option of manual work/verification; greenfield/brownfield source-fit; Lead/Worker profiles and authority; verified native controls per host; scoped Task Criteria/Goals; Lead-prepared worktrees; Worker Coder/Tester/Reviewer; minimal role-scoped context; optional post-review actual 27B-skeleton/small-model implementation; cloud/local parallel continuity. These are design decisions recorded in a **DRAFT plan**, not an implementation completion claim.
