# Milestone and gate contract (Standard+)

A specification, not a gate engine. Milestones, triggers and gate selection are written by the Planner and approved by the user; bootstrap only builds the engine. No approved GOALMAP or milestone means `NOT_CONFIGURED`, never an invented M1. A gate is never PASS because this file exists.

## Gate catalog

| Gate | Who | Target | Meaning |
|---|---|---|---|
| G0 | user (request) | GOALMAP + milestones | approved goal-to-ID table and milestones (COVERAGE_MAP / MILESTONE_SET) |
| G1 | reviewer | plan | goal is faithful to the IDs it covers (nothing missing, added or reworded); tasks point to the right goal |
| G2 | critic | plan | plan is clear and consistent to an outsider |
| G3 | coder | code | self-review done |
| G4 | script | code | verify PASS |
| G5 | tester | code | acceptance conditions pass when actually run |
| G6 | reviewer | tests | tests cover the conditions and were not weakened |
| G7 | reviewer | code | diff matches goal and acceptance conditions |
| G8 | critic + reviewer | code | no blocking finding remains |
| G9 | critic + reviewer | tests | tests are not weak (mutation-style check on a copy) |
| G10 | reviewer | milestone | no drift from goals; everything traces back to IDs |
| G11 | user (request) | milestone | acceptance (MILESTONE_ACCEPT) |
| G12 | git-admin (Full) | repo | this task's change is integrated at the target; NOT_APPLICABLE without Git |
| G13 | trace | plan + code + tests | links valid, no OPEN/STALE in scope, every in-scope ID has task and test |
| G14 | tester + reviewer (Full) | running product | goal flows, invariants and errors verified on the real product; unresolved THEORY_GAP blocks PASS |

## Profiles (per task, take the highest after escalation)

- light: G3, G4 (+G5 if there is a real-run criterion)
- standard: G3, G4, G5, G7
- heavy: G3-G9 (plan through G1+G2)
- G13 applies to every task in every profile. G12 applies when the change must be integrated. G14 at milestone end and before release.
- Sample escalation thresholds (tune per project): diff >=150 lines / 5 files -> standard; >=400 lines / 12 files -> heavy; touching `harness/sensitive-paths`, dependencies, or a goal with an invariant -> heavy; edited or deleted tests -> G6 and G9 mandatory; verify failing 3 times or 2 review rounds -> raise one level, still failing -> stop and open a request.

## State and expiry

- Each signed gate stores `verdict, evidence, target_hash, at`.
- Hash covers: task code and test files, the goal and its acceptance conditions, and the content and version of the covered theory IDs.
- Changed target means the gate (and dependent gates) expire; a changed theory ID expires only gates of affected goals/tasks.
- Only the gate tool writes state. G0 and G11 are signed only from a valid AGREE in the approvals ledger; otherwise `AWAITING_USER`.

## Commands (implement for the runtime)

- `status`: milestone, task, effective profile, required gates with state, open requests, and the **MANDATORY NEXT STEP**.
- `sign <gate> <PASS|FAIL> <evidence>`
- `check`: exit 0 only if every required gate is PASS and unexpired; otherwise print the next step. Past the loop limit: "STOP: user needed".
- `advance`: only when `check` passes; marks the task done; a milestone closes only with G11.

## Automatic triggering

- Trigger fields: event, scope, profile/gate, responsible role, PASS condition, max rounds (default 2 per pair), action when it cannot run.
- Events must be ones the runtime can really observe (e.g. `plan_ready`, `task_code_ready`, `task_verified`, `feature_complete`, `milestone_complete`, `risk_escalated`). Do not fire on every file save; do not repeat a trigger already PASS for the same hash.
- Hooks (if supported): session start / prompt submit inject `gate status`; Stop runs `gate check` and blocks at most 3 times per task, then stops and reports; pre-tool guard blocks hand edits of state, task done-status, hook config, CRITERIA, journal, decisions and approvals, and blocks agents from signing G0/G11 or answering requests.
- Hooks only block and name the next step; the main agent (or an external orchestrator) calls the sub-agents.
- Without hooks use a `next_step` tool, a rule to call it first and before declaring done, and `gate check` in pre-commit/CI. Mark what is `GUIDED_ONLY`.
- Call it "automatic" only with real orchestration; prove it with a fake milestone on a disposable copy.

## Honest limits

A signed gate by an agent is not proof of who signed unless permissions are enforced. Gates are only as good as the acceptance conditions; vague conditions make PASS meaningless.
