# Review and repair orchestration — existing-host limits

Codex native role TOMLs and the Python Stop hook are installed, but **there is no autonomous Planner/Reviewer/Critic orchestration engine**. The Stop hook runs trace-link and configured-script checks; it does not call Critic or issue approval receipts.

## Pre-Code Technical Proposal
Coder nominates all related file/function/caller/interface/dependency/test changes → **independent Critic** runs `.agents/skills/critical-review/SKILL.md` in **PRE_CODE_TECHNICAL** mode with relevant scoped Criteria, Plan, accepted decisions and source → PASS / CHANGES_REQUIRED / HUMAN_ESCALATION. CHANGES_REQUIRED loops **proposal text**, not source. Critic PASS is the **final technical design review**; no additional Reviewer or Human technical-layout signature. Escalate only unresolved consequential domain/theory or disproportionate complexity choices. Existing branch/source authority still applies to implementation. An instruction-only/manual review is GUIDED_ONLY, not proof of native execution.

## Post-code review and testing
Tester independently verifies approved user behavior and source/host evidence. Reviewer may classify PLAN/CODE/TEST results. Critic in **PUBLIC_ARTIFACT** mode reads only delivered artifacts/public instructions, never private Criteria or Plan, and sends observations to Reviewer. This is a separate scope, not a second Pre-Code gate.

Future host-native orchestration may use verified native subagents; do not introduce a daemon/VM or claim native guarantees before observation.
