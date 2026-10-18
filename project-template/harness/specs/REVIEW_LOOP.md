# Review and repair orchestration guide — runtime-specific

- Planner supplies approved milestone trigger and current goal/task. No milestone approved => NOT_CONFIGURED.
- When trigger fires: run verify/test; Reviewer checks goal/AC; Critic independently tests artifact using only public context; Reviewer classifies critic observations against goal and evidence.
- Blocking findings return to Coder for bounded repair, then rerun relevant tests and review. Out-of-scope observations go to BACKLOG. No blocking findings means PASS.
- Respect user approvals for milestone acceptance and protected actions. Never auto-approve or treat chat as authorization.
- Implement via native subagent orchestration, state/hooks or manual commands based on platform. Test trigger, missing trigger, unrelated finding, bound exhaustion and no-findings path.
