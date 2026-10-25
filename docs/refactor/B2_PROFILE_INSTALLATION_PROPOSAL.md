# B2 — Profile-aware installation: source-backed Technical Proposal

**Status:** PRE-CODE DESIGN / CR FINDINGS RESOLVED IN DOCUMENT; host-native enforcement UNVERIFIED.
**Authority:** Accepted Bootstrap plan §8.10; B1 installer/host-fit source survey. Bootstrap is standalone, not GSA. Scope B2 only.

## Goal and invariant

Lead and Worker use the **same Bootstrap harness and role/skill capabilities**, but Worker is an **execution-only subordinate session that can exist only after a Lead**. The difference is the **Criteria/scope supplied to each instance**, not agent kind, installer profile or capability ranking. Lead holds the whole-project approved Criteria; Worker holds the specific accepted assignment whose operative Criteria is the **approved Technical Proposal** for that delegated work. Preserve traceability to overall project Criteria, but do not force the Worker to re-bootstrap the project or redesign/reapprove its assignment. Existing installs and updates must remain safe. Critic `PRE_CODE_TECHNICAL` is the last proposal review, never another Reviewer approval.

## Concrete existing call path

`install.py:main` parses `--tier`, repeatable `--runtime`, `--target-app`, `--staged`, `--upgrade`, and manages setup-state lock. `role_names(tier)` reads `TIER_MANIFEST.json`; `entries(tier,runtime)` and `multi_entries` determine copying; `plan_multi` and `classify` preserve target edits; a manifest records ownership. Existing selected primary runtime is immutable during staged setup. `.generic` is a staging adapter, not proof of native host support.

## Options examined in critical design review

- **Reject:** Replace Lite/Standard/Full with Lead/Worker tiers. It changes tier semantics and breaks compatibility.
- **Reject:** Create a Worker installer, orchestrator, queue, identity registry, runtime daemon, or global hook abstraction. No demonstrated missing function requiring these.
- **Reject:** Automatically downgrade/strip Planner/Advisor/Critic from installed Worker role files. Install packaging and *per-task delegated authority* are different concepts; role absence can break independent review.
- **Reject:** Claim that a copied generic file or local Git worktree enforces host permissions.
- **Prefer:** Reuse the **identical Bootstrap installation/harness**. Supply different scope inputs: whole-project Criteria to Lead; accepted Task assignment and **CR-PASS Technical Proposal as Worker operative Criteria**. No additional installer CLI profile is needed **unless a real host-specific workflow demonstrates an otherwise unmet installation requirement**.

## Reviewed minimal B2 design — REUSE first

| Proposed action | File/function/caller | Acceptance |
| --- | --- | --- |
| REUSE_AS_IS | `install.py` `main`, `role_names`, `eligible`, `entries`, `multi_entries`, `plan_multi`, `classify` | All existing tier/runtime/staged/upgrade pathways remain unchanged |
| REUSE_AS_IS | `project-template/harness/specs/TIER_MANIFEST.json` | No new tier, role removal or renamed tier |
| REUSE_AS_IS | Existing `.agents/roles`, Pre-Code Critic skill and `harness/specs/REVIEW_LOOP.md` | Both instances keep the same capabilities; Worker operates under approved Technical Proposal and assigned task scope, not installer labels |
| REUSE_AS_IS | `.generic/ADAPTER_REQUIREMENTS.md`, `HOST_NATIVE_LAYOUT.md` | Selected real host/version must verify native discovery and interception before claims of enforcement |
| DEFER TO B3 | Pass approved Technical Proposal as Worker operative Criteria; task-scoped handoff/context selection and delegated write boundary | Evaluate actual user task and host mechanics; distinguish guided procedure from enforced guard |
| NO CREATE | A universal `--profile lead/worker` flag, `PROFILE_MANIFEST`, dedicated Worker installer, cross-platform dispatcher | No verified consumer requiring any of them |
| TEST WHEN ACTUAL HOST SELECTED | Installed role discovery, allowed vs denied write, non-destructive `--upgrade`, staged lock, user-modified local settings | Host-specific observation, never inferred from static package tests |

## Human correction — identical Lead/Worker, different Criteria

- **Lead instance:** Bootstrap with project-wide approved Criteria; plans/co-ordinates the entire project and delegates reviewed work.
- **Worker instance:** The **same Bootstrap**, no separate agent type or installer; its operative Criteria is the **specific assigned work**, expressed by the **Technical Proposal already approved through independent Critic CR**. That proposal should define precise outputs, affected files/functions/callers, constraints, dependencies and acceptance. **Worker does NOT run project Bootstrap:** no project discovery, initial project Criteria drafting/approval, Technical Advisor consultation, project-wide planning/milestone creation, or fresh Pre-Code CR for an unchanged already-approved proposal.
- **Handoff:** Lead delivers the approved Technical Proposal and necessary bounded implementation context. Worker enters **EXECUTION** directly, not BOOTSTRAP. Worker performs only task-relevant source/permission checks, implementation, tests, defect repair and handoff evidence. Worker's role skills and Tester/Review contracts remain available as needed, but **project initialization and project-wide approval gates are not re-run**; there is no new Pre-Code gate, independent redesign or shadow Criteria document required by default.
- **Boundary:** A Worker must not promote task-specific instructions into project-wide Criteria or reinterpret the proposal beyond approved scope. Material design gaps or changed scope are escalated to Lead and appropriate Critic CR; normal implementation choices remain Worker engineering responsibility.
- **Result:** No Lead/Worker selector, different tier, distinct installer, separate registration, or special model identity is justified.

## Worker entry contract — no Bootstrap phase

**Preconditions supplied by Lead:** assigned and already CR-PASS Technical Proposal; source revision/branch and authorized write scope; necessary input references and acceptance tests. If a prerequisite is missing, Worker reports a specific handoff gap to Lead, **not** a new project bootstrap request.

**Worker flow:** consume assignment → inspect only relevant existing code and constraints → implement the approved solution → run scoped verification/bug-repair → deliver outputs and evidence to Lead. It must not repeat discovery, ask Human to reapprove Criteria, create new GOALMAP/milestones for the project, or issue another mandatory technical proposal review. A proposed material redesign returns to Lead for a new scoped proposal/CR outside this execution flow.

**Separation of responsibility:** Lead alone is responsible for project bootstrap and global Criteria/Plan governance. Identical harness tooling does not imply identical entry workflow. This is a task-entry contract, not a new agent kind, installer flavor, tier or runtime manager.

## Worker existence and model-capability boundary — Human decision

**Worker profile is subordinate, never standalone.** It exists only after an actual Lead has established the project Criteria/Plan and delegated a specific **CR-PASS Technical Proposal**. Without that Lead and accepted assignment, do not offer/start Worker-only project initialization: use the normal Lead Bootstrap setup instead. The Worker has no independent project bootstrap and cannot create its own overarching Criteria/Plan.

**Model size does not define a profile.** There is no proposal to make a ~27B local model an autonomous Lead for a complete project: its capability is not established for that responsibility. The ~27B reference in B4 is an optional *bounded implementation benchmark only*, not Lead eligibility. Do not infer that all larger models are adequate without evidence.

**If a user's local model is genuinely capable of leading their project**, install/run the normal **Lead profile** with that model; the Lead may itself perform implementation work (acting as its own Worker) rather than requiring a separately installed Worker. This does not create two models, two installers or duplicate agents by default.

**B2/B3 implications:** The installer need not expose a standalone Worker onboarding path. A delegated Worker execution session is meaningful only with the Lead-provided approved proposal, scoped source access and task acceptance. Any future profile-selection UX must enforce the Lead-first dependency rather than present Worker as an independent bootstrap alternative; do not code such UX without a demonstrated B2 consumer and source-backed review.

## Explicit limitation and review outcome

The approved **objective** is identical harness execution with distinct Criteria scope. **Lead Criteria = whole project's approved Criteria. Worker Criteria = concrete assignment's approved Technical Proposal (including acceptance, interfaces, files and dependencies).** These are scope inputs, not two file-format families or two permission engines. B1 source inspection does not prove that this requires *installation-time* profile selection. Since the existing tier installer already installs appropriate role definitions, an unconditional `--profile` switch is an unjustified implementation. Critic's source-grounded objections resolve by choosing **no B2 installer source changes** until there is evidence of a missing native setup capability. This is a scoped **design PASS for the minimal no-op installer choice**, not a claim of a real native Critic agent call or native host success.

For actual Lead-to-Worker delegation, continue to **B3** with the **already approved Technical Proposal as the primary Worker assignment**, plus only necessary source/context and source authority. Do not invent a second Worker Criteria approval or ask Worker to run a fresh project-wide Pre-Code proposal on an already passed assignment. Work outside the approved proposal returns to Lead for appropriate design handling. A concrete B3 contract can then identify whether any B2 installation delta is truly needed. B4 model comparisons and B5 host-wide regression remain separate.

**No Criteria changes; no B2 source files generated.**
