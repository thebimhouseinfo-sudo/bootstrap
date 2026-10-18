# Harness self-diagnosis / fixer contract (Full)

Not an executable doctor or selftest.

- HARNESS_SPEC describes approved intention of each blocking rule, positive/negative examples and unlock owner.
- Every BLOCK explains code, rule, location, cause, required evidence and approval channel.
- Doctor checks actual runtime version/schema, paths, hooks, model availability, ledger integrity and policy contradictions.
- Reproduce in disposable workspace. T0 mechanical repair may proceed only without changing permission/guard semantics, with regression test and rollback.
- T1 any guard/permission/model/gate/approval behavior change requires HARNESS_PATCH approval first.
- T2 no product theory change, no forged approvals, no unauthorized remote/destructive action.
- Weakening detector flags removed or broadened safeguards as T1 even when labeled T0.
- On test failure roll back; after 2 failed fix attempts stop and report.
- Document patch, tests, decision, and rollback in CHANGELOG.
- Template for the approved intent of each rule: `contracts/HARNESS_SPEC.md`. Keep `harness/CHANGELOG.md` and a separate snapshot of harness files.
- Classify every block first as CONFIG ERROR / CORRECT BLOCK / OUTSIDE HARNESS (remote auth, branch protection, network); only the first kind may be repaired. A correct block is explained, not bypassed. An urgent need uses a one-time BREAK_GLASS request, then the root cause is fixed separately.
