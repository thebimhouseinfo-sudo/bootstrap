# Goal-scoped review — <target / T-ID / GL-ID>

- Target: PRE-CODE / PLAN / CODE / TEST
- Approved goal and version: <GL-ID @vN>
- Inputs: <goal, ALL related Task Code Structure Proposal sections, full accepted Decision refs, verified existing callers/host facts, diff/evidence where CODE or TEST>
- PRE-CODE independent Critic mode: PRE_CODE_TECHNICAL (final CR, no extra Reviewer/Human layout signoff)
- PRE-CODE Critic verdict: PASS / CHANGES_REQUIRED / HUMAN_ESCALATION / UNVERIFIED
- Review execution evidence: <independent Critic invocation or GUIDED_ONLY; do not fabricate native dispatch>
- CODE/TEST outcome: PASS / FAIL / UNVERIFIED
- Cross-Task duplicate gates/interfaces/state and missing callers: <specific overlapping paths, or NONE with evidence>
- Proportionality (Small Function → Big Solution → Larger System Impact): <source-supported cost/risks and simpler native/manual alternative where relevant>
- Derived approved components (only after PRE-CODE PASS): <section/view of SAME corrected proposal, never a separate registry>
- Host/native-test limits: <SCRIPT_TESTED / GUIDED_ONLY / REAL_HOST verified with evidence>

| Finding | Blocking? | Goal / condition | Reproducible evidence | Required action |
|---|---|---|---|---|
| <F-ID> | YES / NO / UNKNOWN | <ID or OUT_OF_SCOPE> | <observed> | <smallest fix / backlog> |

For PRE-CODE_TECHNICAL, independent Critic receives scoped approved Criteria/Goal/Plan, full accepted Decisions, all interacting proposals and inspected source/callers. For PUBLIC_ARTIFACT, Critic only observes delivered product and public README; private project scope is prohibited. Reviewer classifies post-code PLAN/CODE/TEST findings, but is not a second PRE-CODE approval gate. Out-of-scope suggestions go to BACKLOG, not into the current coder task.
