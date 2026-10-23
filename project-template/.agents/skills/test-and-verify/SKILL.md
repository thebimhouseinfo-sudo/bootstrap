---
name: test-and-verify
description: Independently verify approved acceptance criteria and repairs with fresh observable evidence.
---

# Test and verify

Map every approved GOAL/AC to positive, negative, edge, recovery, repeated and regression cases where applicable. Define expected/actual and capture executable commands, full output, exit status, versions and host observations. For each confirmed bug use `bug-fix-loop`: failing regression before fix where feasible; after repair, rerun original reproduction, focused tests, impacted integration cases, full relevant suite and required real-host check. Distinguish STATIC, UNIT, MOCK, INTEGRATION and REAL-HOST evidence. Never declare PASS on build alone, Coder claim, stale logs, a fixture instead of host, or weakened assertions. Unrun tests remain UNVERIFIED; failures include exact defect handoff and next action.
