# M3 — Code Structure Proposal: changed-scope RETIRED without a second runtime engine

**Status:** PRE-CODE, GUIDED_ONLY design review; owner of actual GSA Job/Run remains GSA. **Source:** Functional v7.0 M3 and G0–G5.

## Verified current facts
- Planner's 'trace-impact' skill currently says to mark only affected entries STALE. That contradicts Human's rule: on approved changed Plan/Phase, examine completed results for reuse and **retire every unfinished item inside changed boundary**. No per-unfinished Task salvage negotiation.
- The template 'TASKS.md' still lists STALE; Milestones template has no retirement instruction.
- 'harness/common/task.py' only validates one configured 'ACTIVE' task and checks links; status other than ACTIVE returns NOT_CONFIGURED. It has **no** Plan/Phase dependency graph, GSA Job/Run authority, branch manager or automatic cancellation mechanism.
- Project's 'harness/specs/TRACE.md' says full graph and automatic propagation are not implemented. Don't conceal this.
- Current GSA external source/client schema and connected Job/Run capability for scope sweep haven't been verified as part of this Bootstrap branch; don't invent an endpoint or claim full runtime success.

## Per-Task changes

| Task | Proposed file/action | Behavior and callers |
| --- | --- | --- |
| M3-T1/T2/T3 | MODIFY project-template/.agents/skills/trace-impact/SKILL.md | On reviewed+authorized Plan change, choose Phase/whole Plan boundary; review COMPLETED outputs for reuse, retire ALL unfinished in that boundary; untouched scopes remain; no per-Task KEEP/REPLACE classification; record superseded Plan/Phase and fresh Milestone/Job/Task dependencies. |
| M3-T1..T7 | MODIFY project-template/.agents/roles/planner.md and seven existing host mirror files | Add bounded Plan-change procedure, honest distinction between guided document changes and real GSA authority. No new Criteria/Advisor gate. |
| M3-T3 | MODIFY project-template/TASKS.md | Template for Active/Next/Done/RETIRED/Blocked; do not put retired work in active queue, preserve history/evidence. |
| M3-T3/T5 | MODIFY project-template/docs/MILESTONES.md | Record scope retirement and fresh milestones with new identities. Do not retire unrelated scopes or completed evidence. |
| M3-T4/T6 | MODIFY project-template/harness/common/task.py | For explicitly RETIRED active-task metadata, fail closed with clear obsolete-task diagnostic. Existing ACTIVE/NOT_CONFIGURED safety remains; NOT a full automated GSA Run cancel engine. |
| M3-T4 | MODIFY tests/test_harness_runtime.py | In disposable installed project, make formerly valid task explicitly RETIRED and verify plan/delivery checks fail; restore ACTIVE and verify checks pass. |
| M3-T6 | REUSE_AS_IS project-template/harness/specs/TRACE.md | Keep honest claim that full graph/automatic STALE/retire isn't implemented; update wording only if tests show documentation mismatch. |
| GSA actual Run/Job | EXTERNAL OWNER — NO UNVERIFIED SOURCE MUTATION | Must inspect real GSA client's supported statuses, quiescence/fence and transition operations under separate authority before claiming scope-wide running Job retirement. |

## Exact scope algorithm (Planner-guided, not a new service)
1. Only after a reviewed approved Plan/Phase change, identify changed boundary. Mere discussion or draft edit doesn't retire anything.
2. Preserve completed historical evidence and evaluate **only COMPLETED** work for reuse; it cannot turn into new current PASS automatically.
3. Fence old unpublished dispatch; for READY/BLOCKED/IN_PROGRESS/DRAFT in changed boundary, choose RETIRED as intended terminal disposition; in-flight writes require observed settlement first. If unsafe or unknown, leave fenced and report reconciliation needed rather than fabricating RETIRED.
4. Retire obsolete Phase/Plan revision and exclusive old work branch logically; don't delete Git refs or touch protected/shared branches.
5. Create fresh Milestone/Job/Task IDs/dependencies for new scope; don't mint unnecessary one-to-one replacements. Replaying same Plan revision must not allocate duplicates.
6. Remove obsolete tasks from current closure calculations only through the actual owning runtime; no fake status based on editing Markdown.
7. Report source/host evidence, unsupported real GSA capabilities UNVERIFIED or BLOCKED.

## Reviewer challenge
A new universal Plan/Job/Run state engine inside Bootstrap would duplicate GSA ownership and is rejected. Only existing Planner skill/template and narrow active-task checker are changed here. The complete multi-Job in-flight behavior is an **external dependency**, not silently accepted. Native independent Reviewer PASS remains UNVERIFIED in this host.

## Regression examples
- Changed one Phase: 2 completed results, 2 ready, 1 running. Completed outputs historically preserved, all unfinished retired only after safe settling of running Run, and unrelated phase untouched.
- Changed whole Plan: all unfinished old work obsolete; new work fresh IDs; repeat request idempotent.
- Task selection status RETIRED: local task checker exits 2 and never reports TRACE_LINKS_VALID.
- Git shared/main branches unchanged; unknown Run state never labeled retired.
- No change to approved Criteria or ordinary Advisor trigger.
