---
name: bug-fix-loop
description: Use when Tester detects failure or regression and Coder must repair it inside approved scope.
---

# Tester ↔ Coder defect loop

1. Tester owns independently reproduced evidence, AC/GOAL, classification and the defect record; Coder owns authorized product-code repairs; Reviewer validates scope and closure evidence.
2. Investigate with `systematic-debugging` first: full error, minimal reproduction, environment, recent changes, data/control boundaries, comparison with working behavior, single falsifiable hypothesis and minimal experiment. Separate bad tool choice, fixture, permissions, host availability and product code.
3. TESTER FAIL → DEFECT OPEN → ROOT CAUSE INVESTIGATION → CODER REGRESSION RED → MINIMAL FIX → CODER GREEN → INDEPENDENT TESTER RE-TEST → REVIEW. Any failure returns the *same* defect to investigation with new evidence. Do not create duplicate jobs or unrelated gate requests.
4. Prefer demonstrated red-green regression evidence. Where a live-host regression cannot be automated, preserve reproducible manual steps and mark automated portion UNVERIFIED, rather than forge success.
5. Tester runs original reproduction, changed-path checks, dependent regression, full applicable suite and real-host acceptance when required. Build-only, mocks, logs or Coder claims alone never imply PASS.
6. Limit each SAME defect to **at most three complete Coder repair → independent Tester replay cycles**. Each retest must reproduce the original user entrypoint/scenario (when user behavior is the defect), focused fix and affected regression with actual environment evidence; do not reset attempts by changing Job, Task, chat or defect label. If the third full retest FAILS, or earlier evidence establishes architectural/shared-state failure, **STOP ordinary patching** and invoke the advanced cross-flow root-cause investigation mode of `systematic-debugging` (causal timeline, parent/child flows, resource wait-for, competing hypotheses and distinguishing experiments) BEFORE any more fixes. Only actual required redesign returns through Reviewer/Plan review; no fourth blind fix, independent new Bug Fixer Agent, automatic Advisor or Criteria gate.
7. Closure requires AC coverage, fresh command output/exit status, fixed original symptom, regressions, remaining limitations, and required Reviewer acceptance. Unsupported host evidence stays UNVERIFIED.

Defect record minimum: ID, approved GOAL/AC, severity, scope, environment/version/ref, precise input/reproduction, expected/actual, logs, root-cause evidence/hypothesis, numbered attempts, changed files/ref, command/output, retest result, owner, status and next action.

## Non-negotiable limits
Respect branch authority, authorized file ownership, protected Criteria, human approvals and runtime hooks. A confirmed ordinary bug within approved scope never requires fresh bootstrap, Plan/Criteria approval or Technical Advisor.
