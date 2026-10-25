---
name: test-and-verify
description: Independently verify approved acceptance criteria and repairs with fresh observable evidence.
---

# Test and verify

Map every approved GOAL/AC to positive, negative, edge, recovery, repeated and regression cases where applicable. Define expected/actual and capture executable commands, full output, exit status, versions and host observations. For each confirmed bug use `bug-fix-loop`: failing regression before fix where feasible; after repair, rerun original reproduction, focused tests, impacted integration cases, full relevant suite and required real-host check. Distinguish STATIC, UNIT, MOCK, INTEGRATION and REAL-HOST evidence. Never declare PASS on build alone, Coder claim, stale logs, a fixture instead of host, or weakened assertions. Unrun tests remain UNVERIFIED; failures include exact defect handoff and next action.

## On-demand user scenario verification
When approved GOAL/AC concerns real User behavior, nontrivial sequences, concurrency or external failures, Tester may invoke the existing `simulate` skill and its T0–T6 methodology, with causal flow guidance in `simulate/references/bootstrap-causal-fanout.md`. Start from the externally visible input, freeze expected User outcome before source-reading, and verify every spawned child flow/state/lease and downstream result. Reuse the ordinary Test Task report and existing evidence locations, not a separate Simulation Job Pack. For the SAME defect, repeat the original user entrypoint on each independent retest, stop normal repair attempts after three unsuccessful cycles, and invoke advanced systematic-debugging. Host mocks or source traces are only MOCK/STATIC evidence; leave unavailable native behavior UNVERIFIED.
