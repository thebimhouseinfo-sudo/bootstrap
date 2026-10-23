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

Related local skills: `debug-protocol`, `test-and-verify`, `bug-fix-loop`.
