---
name: implement-task
description: Coder reads complete accepted decisions, describes Task-level Code Structure BEFORE source, implements only after reviewed design and current source authority.
---

# implement-task — pre-code then authorized implementation

## Delegated Worker exception (approved work only)
An existing Lead may delegate a Technical Proposal already passed by independent Critic. For that **specific Worker assignment**, follow `.agents/skills/worker-execution/SKILL.md` and **go directly to Stage B** without project bootstrap, another Criteria, or repeating Stage A/CR. Confirm approval and actual source authority; if absent, report to Lead rather than self-approving. A material design/scope change returns to Lead for fresh scoped Critic CR. Ordinary project Coder/Lead tasks continue with Stage A below.

## Stage A — descriptive PRE-CODE (NOT executable files)
1. Validate the assigned approved Goal/Task, Criteria, branch authority, full relevant current accepted Human decisions, existing source/callers and actual host/SDK. Do not invent missing domain logic or assume a Coder-made technology decision is a User-approved workflow.
2. When the professional/host operating solution is **materially missing**, use solution-clarification once at Goal/Task-pack level. Normal coding choices are not Human questions. Use the focused operational-file-lifecycle knowledge only when the Task handles User file products or app-owned supporting files.
3. Inspect the existing brownfield implementation before proposing a rewrite; prefer REUSE/MODIFY to CREATE when evidence justifies it.
4. Produce ONE descriptive Markdown Code Structure Proposal in `docs/TECHNICAL_PROPOSAL.md`. The first one covers the **whole Plan** (all milestones and Tasks), written bottom-up from Tasks; later ones cover only materially changed scope. Include per-Task IDs, verified/current vs proposed future files, CREATE/MODIFY/REUSE_AS_IS/REMOVE, classes/functions/gates, interface fields, inputs/outputs/callers, inter-Task dependencies, evidence, verified host constraints, tests and exclusions. No actual source/code stub/test file creation in Stage A.
5. Send the complete proposal to independent Critic in PRE_CODE_TECHNICAL mode for a top-down review. When Critic returns PASS, set the line `Critic CR: PASS` in `docs/TECHNICAL_PROPOSAL.md`; that file is the final proposal Coder implements milestone by milestone. Critic returns PASS, CHANGES_REQUIRED or HUMAN_ESCALATION with evidence. CHANGES_REQUIRED means edit the proposal, not application source. A smaller solution that avoids large downstream state/gates is preferred if it still meets accepted criteria.
6. A Critic CR design PASS allows normal implementation **only through the existing authorization and branch/write controls**; it never equals test/native-host PASS. If native Critic execution is unavailable, label the coordination GUIDED_ONLY; do not invent a native Critic receipt or add another technical review gate.

## Stage B — implementation and proof (after reviewed design)
7. Recheck current authorized source branch, snapshot when required and implement the smallest change respecting the reviewed caller/contracts; no new unrelated infrastructure or User file identity/version policy.
8. Run real syntax/build/tests, independent Tester and actual host checks when available; mock/static checks cannot prove AutoCAD, Revit or other native host effects. Use systematic debugging and existing bug-fix-loop for confirmed failures.
9. When new major files, shared interface, operational logic or host effects differ materially from reviewed proposal, return to Critic technical CR. Do not demand Human approval for ordinary coding details.
10. Report modified paths, commands, observed PASS/FAIL, Critic CR/independent Tester evidence or honest UNVERIFIED limitations, and next authorized action. No fabricated source writes or approvals.

## Boundaries
This is existing Coder skill/coordination, NOT a new Task lifecycle engine, extra source registry, automatic Advisor, authenticated gate or separate technical Plan. User-approved CRITERIA and actual source permissions remain authoritative.
