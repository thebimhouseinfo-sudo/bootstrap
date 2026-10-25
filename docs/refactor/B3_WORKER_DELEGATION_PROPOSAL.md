# B3 — Lead → Worker delegation and scoped context

**Status:** Source-grounded pre-code design; scoped functional change only, no new runtime/installer/Criteria format.
**Input decisions:** Lead is the normal project Bootstrap flow. A Worker can exist only under an existing Lead. In recommended operation, the **CR-PASS Technical Proposal is the sole Worker Criteria**. Worker does not bootstrap a project and does not repeat Pre-Code CR on unchanged approved work. Same harness/roles/skills; model choice does not confer Lead authority.

## Existing source and issue

- `.agents/skills/implement-task/SKILL.md` Stage A and `.agents/roles/coder.md` require Pre-Code Proposal/CR for an ordinary Coder; without explicit scoped Worker exception this repeats a phase already completed by Lead.
- `harness/MULTI_HARNESS.md` currently illustrates Codex Planner → Continue local Coder through global `CRITERIA.md`/`TASKS.md`; valid for cohost coding, but not the normative Worker Criteria contract.
- `harness/specs/REVIEW_LOOP.md` correctly assigns Pre-Code approval to independent Critic; current hook does not automatically dispatch it.
- `install.py` already packages all canonical `.agents/skills` for Standard and supported runtime mirrors without a profile switch.

## Options / Critic technical challenge

1. Separate `--worker` installer, `WORKER_CRITERIA.md`, runtime token/registry: **REJECT**; duplicates existing harness and Criteria.
2. Worker automatically replays task bootstrap + Stage A Pre-Code: **REJECT**; violates approved assignment.
3. Skip all Worker review/tests/branch restrictions: **REJECT**; conflates entry workflow with execution responsibility.
4. **Select:** one canonical `worker-execution` skill used when Lead supplies already CR-PASS proposal; minimal conditional exception in ordinary Coder skill; describe Lead-to-Worker handoff in existing multi-harness guide. No new enforcement claim.

## Source map, callers and acceptance

| File | Action | Caller / behavior |
| --- | --- | --- |
| `project-template/.agents/skills/worker-execution/SKILL.md` | CREATE | Worker explicitly activates this existing-skill-pattern instruction when a Lead-owned approved Technical Proposal is handed over. Its only Criteria is the proposal; repository/branch access info is operational data, not another Criteria. |
| `project-template/.agents/skills/implement-task/SKILL.md` | MODIFY | Early branch for actual delegated Worker: skip Stage A and begin Stage B for unchanged accepted CR-PASS proposal, without relaxing write checks, verification and escalation. Ordinary Lead/Coder path remains unchanged. |
| `project-template/.agents/roles/coder.md` | MODIFY | Clarify conditional Worker execution path; default project path still creates pre-code design. |
| `project-template/harness/MULTI_HARNESS.md` | MODIFY | Explain optional Worker handoff separately from existing cohost in one project; no cross-chat assumption or installer integration. |
| `tests/test_installer.py` | MODIFY | Static packaged contract asserts skill and conditional Coder coverage without asserting native runtime behavior. |
| `install.py`, tier manifest, state/branch authority, host adapters | REUSE_AS_IS | No extra profile, new CLI, state machine, native API guesses or worktree sandbox claims. |

## Handoff contract

Lead → Worker: **one CR-PASS Technical Proposal**, with proposal's interfaces, exact accepted scope, acceptance and dependencies. Lead may separately provide current repository, revision, branch/access, required inputs; these are logistics **not Criteria**. Worker: verify that Lead and approved proposal actually exist, read minimum relevant source/knowledge, respect source authority, implement, test and return changed paths/diffs, reproducible results and deviations. If CR proof or scope is materially missing, return a precise handoff issue to Lead; **do not perform project bootstrap or invent approval**. Material design deviation returns Lead/independent Critic, not self-approved expanded work. Worker need not be separate model or computer.

## Verification and limits

- Static tests establish packaging and text contract, not native subagent dispatch/permissions.
- Dogfood will assess real task delivery quality/context versus direct capable model later; model benchmark B4 and host-native B5 remain separate.
- No mandatory project bootstrap, Technical Advisor, new Criteria/Plan/milestone or second proposal CR for Worker.
