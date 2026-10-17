# Trace and stale propagation contract (Standard+)

This is a spec, not a runnable generator. Generate `docs/TRACE.md` from live data; never edit generated trace by hand.

Links: approved theory ID → GOAL → milestone → exactly one goal per task → file/test → evidence → status.

Check:
- IDs and version references resolve; OPEN/PENDING_APPROVAL do not authorize dependent tasks.
- Approved IDs have goal coverage; scoped goal IDs have task/test links.
- Changes to theory IDs mark affected goal, milestone, task and test STALE; unrelated entries remain current.
- No DONE while in-scope evidence or gate is STALE.
- Unknown or absent approved GOALMAP → NOT_CONFIGURED.
- Link checks do not prove product behavior; tester and reviewer must verify semantics.
