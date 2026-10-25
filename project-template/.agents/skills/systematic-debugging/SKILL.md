---
name: systematic-debugging
description: Investigate bugs, failed tests, build issues and unexpected behavior before attempting a fix.
---

# Systematic debugging — portable project guidance

Adapted process from the installed ChatGPT `superpowers:systematic-debugging` skill. Prefer that native skill when the host supports it; this local guidance enables the same essential workflow on other coding hosts.

## Four phases
1. **Root cause investigation**: read complete error and trace; reproduce minimal failure; inspect recent diffs, dependencies, host/config; trace data across component boundaries and backwards to the first corrupt value. Keep observations separate from hypotheses.
2. **Pattern comparison**: identify nearest working case/reference; compare differences and assumptions, including host version/API and fixture.
3. **Falsifiable hypothesis**: state a single specific cause and predicted observation. Run the smallest experiment varying one factor, document evidence. If disproven, return to investigation, not shotgun patching.
4. **Repair/verify**: demonstrate a failing regression test where feasible, make the smallest root-cause fix, verify test passes and original symptom disappears, execute dependent regression/full suite and real-host acceptance as required.

No root-cause evidence → no speculative fix. Three unsuccessful repairs → architectural review, not a fourth blind fix. Intermittent or unavailable-host cases remain UNVERIFIED with diagnostic evidence. Do not use arbitrary timeouts or instrumentation that changes contract behavior without project approval. Never claim PASS without fresh output from the verification run.


## Advanced cross-flow root cause — on third failed fix/retest or earlier strong architectural evidence

This is an **escalation MODE of the existing systematic-debugging skill**, not a new agent, approval gate or repetitive patch cycle. Before any additional code write:

1. Reproduce the SAME original user-facing action/scenario and collect every observed descendant event through public entrypoint, dispatcher, callbacks, tool/file/CAD boundary, asynchronous acknowledgments, queue/lease, save and result terminal state. Include the causal parent ID even where IDs exist only as trace labels; never invent a persistent GUID registry.
2. Produce a time-ordered **causal graph and wait-for graph**: which flow spawned each child, why it exists, who holds each exclusive resource, who waits for whom, which result was late/duplicated/unknown, and what completed or remains in-flight. A single user request launching two paths may strand one despite all local unit tests passing.
3. Identify the earliest *observable* divergence from Human/Criteria expected behavior; distinguish source-code bug, wrong tool selection, stale Test oracle, external contract, permission, environment and genuinely undecided requirement. Unknown is NOT equivalent to impossible.
4. List at least two plausible competing root-cause hypotheses when evidence supports them, plus specific observations predicted by each. Choose minimal **discriminating experiments** and record observed results; do not hide inconclusive evidence.
5. Check host partial-effect and recoverability: completed or unknown CAD/file writes, save/undo/ESC behavior, lease ownership and real operating contract. Mock host cannot certify real host. Do not assert job rollback, safe cancellation, timeout or automatic restart without a real native mechanism.
6. Deliver an **Advanced Defect Report** under existing Tester evidence: original trigger, full timeline, graph, observed facts, hypothesis confidence, experiments, previous three attempts, unverified boundaries and concrete minimal fix options. If redesign materially changes reviewed interfaces, send to existing Reviewer/Planner; otherwise Coder may take one reviewed evidence-based repair only after this deeper diagnosis.
7. A diagnosis report is NOT test PASS, and this mechanism does not itself authorize additional blind attempts, new lifecycle or new per-defect persistent service.

Related local skills: `debug-protocol`, `test-and-verify`, `bug-fix-loop`.
