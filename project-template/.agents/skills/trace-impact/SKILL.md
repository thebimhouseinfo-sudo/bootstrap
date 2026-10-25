---
name: trace-impact
description: For reviewed Plan changes, retire all unfinished work inside replaced Plan/Phase scope without creating another runtime.
---

# trace-impact — changed scope RETIRED, unaffected scope unchanged

## Trigger and ownership
Use only when a reviewed and authorized new Plan replaces a Phase or entire Plan; a discussion, proposed delta, draft file save or future option does **not** retire running work. Planner identifies the changed boundary. Bootstrap is standalone. When a target has a separately integrated runtime, only its verified owner can manage Job/Run transitions and in-flight effects; otherwise leave those effects UNVERIFIED. This skill is a guided procedure, not an automatic cancel daemon or authenticated gate.

## Procedure
1. Read the old and accepted revised Plans, decision references and goal/milestone/task dependencies. Mark exactly the changed Phase(s) or whole Plan; avoid pulling unaffected scope into cleanup.
2. Inspect **COMPLETED** historical items for evidence and whether their outputs still meet the revised need. Keep the old completion/history unchanged; re-use only compatible results by explicit link. Do not reclassify a completed item as automatically failed or retire it.
3. For the replaced boundary, treat **ALL unfinished** Milestones, Jobs, Tasks, READY, IN_PROGRESS, BLOCKED, DRAFT and obsolete pre-code proposals as RETIRED work. Do **not** spend time triaging every unfinished Task into KEEP/REPLACE/REVALIDATE; no one-to-one replacement requirement.
4. Before actual terminal write on an IN_PROGRESS/unknown Run, stop scheduling new old-scope work and use the owning runtime's authorized cancellation/fence and settlement facilities. Inspect external CAD/Git/file effects first. If safe settlement cannot be verified, report BLOCKED/UNVERIFIED and maintain the fence. Do not claim that a Markdown change remotely canceled execution; do not retry uncertain mutations or promise job-wide rollback.
5. Create new reviewed Plan revision/Phase, Milestones, Jobs and Tasks with **fresh identities**, correct dependencies and proposals. Link compatible completed outputs. Replaying the same revision must be idempotent, not duplicate new topology.
6. Logically retire the exclusive source branch for obsolete work; preserve actual Git refs/unmerged commits and protect main/shared/release. Before real merge/push use existing branch authority. Avoid inventing automatic deletion.
7. After confirmed authoritative RETIRED state, exclude obsolete obligations from current closure and queue. Verify no zombie READY/IN_PROGRESS work, cross-Phase effects or duplicate successors. If the actual environment lacks the needed operation, report the verified limitation rather than inventing a replacement runtime.
8. Record before/after scope, completed output reuse evidence, items intended/confirmed retired, unknown in-flight effects, fresh work links, branch handling, source tool evidence and acceptance limits. Do not trigger Criteria Advisor for an ordinary Plan change.

## Output
Actual evidence, classified COMPLETED/RETIRED/UNVERIFIED changes and next existing-authority action. Standalone Task checks can reject an explicitly RETIRED selected Task, but do not establish full Plan-to-Run propagation. This skill does not create new human approvals, change Criteria, or run Git cleanup.
