---
name: worker-execution
description: Execute Lead-delegated work against a CR-PASS Technical Proposal as the sole Worker Criteria; skip project bootstrap and duplicate pre-code review.
---

# worker-execution — delegated implementation, not project bootstrap

## Entry conditions
Activate only when an existing Lead delegates a **specific Technical Proposal that has already passed independent Critic Pre-Code review**. The approved proposal is the **only Worker Criteria** in the recommended workflow. Do not start a standalone Worker, infer approval from a filename or self-issue a CR PASS. If the approved proposal or delegation is missing, return a precise handoff gap to Lead. Do **not** recreate Project Criteria, Plan, GOALMAP, Milestones or run Technical Advisor/bootstrap.

The Worker uses the **same installed Bootstrap roles and skills** as Lead. Worker mode is an assignment entry point, not a tier, model-size classification, installer profile or new permissions subsystem.

## Execution flow
1. Read the entire approved Technical Proposal, including scope, functions/files/callers, interfaces, dependencies, exclusions, tests and acceptance. This is the sole normative Criteria for the Worker assignment.
2. Receive repository location, existing revision/branch, source access and input references as **execution logistics only**; these do not amend Worker Criteria. Read the **minimum relevant** implementation/source/knowledge; expand when dependencies actually require it, not a blanket preloading of project-wide history.
3. Confirm actual write/branch authority using existing harness rules; a worktree isolates Git changes but is **not a sandbox**. If source authority is missing, stop with an exact error instead of inventing an override.
4. **Skip ordinary implement-task Stage A**: Lead has already completed technical proposal and independent Critic Review. Begin Stage B for the approved scope. Do not generate another proposal or CR gate for unchanged work.
5. Implement, run the task's actual syntax/build/tests and appropriate independent verification; repair confirmed defects under existing limits. Report only real evidence. A native host action is UNVERIFIED until observed in the host.
6. Hand back to Lead: modified paths/changes, relevant revision, executed checks with PASS/FAIL, remaining uncertainties, deviations and any acceptance gaps. Do not change global project Criteria, Plan or Lead-owned governance.

## Escalation
If technical implementation details need ordinary engineering judgment, resolve them locally within the proposal. If the proposal's substantive design or assigned scope needs to change, **do not silently redesign**: explain the specific conflict and return it to Lead for an appropriate revised proposal and independent Critic CR. No Worker self-approval, secondary Worker Criteria or duplicated bootstrap.

## Host limit
This skill is instruction-guided unless the selected real host proves native role invocation and write interception. It does not launch a subagent, allocate worktrees or enforce filesystem permissions on its own.
