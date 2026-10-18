# Verification runner contract (implement per OS/runtime)

This file is a **specification**, not an executable verifier.

Sequence (stop on actual failure, exit nonzero): dependencies → lint/typecheck → build → tests → changed-file scope → changed-file secret scan → trace (Standard+) → outcome.

- Print failing step, source location when known, reproduction and remediation.
- Missing command or unavailable host → UNVERIFIED/NOT_CONFIGURED, never PASS.
- Only include checks supported by the confirmed project stack.
- Snapshot before edits and demonstrate restore in a disposable test.
- Runtime hook integration and Stop retry cap (max 3) require implementation and positive/negative tests.
- Check no hard-coded network execution or unsafe destructive commands.
- Separate build success from real-host integration success.
