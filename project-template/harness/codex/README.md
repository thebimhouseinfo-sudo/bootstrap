# Codex baseline scripts — immediately usable

These Python 3.9+ scripts have no third-party dependencies and work on Windows/macOS/Linux when Python exists.

- `python harness/codex/doctor.py`: validates template file inventory and skill header markers (NOT a proof of hooks or security).
- `python harness/codex/verify.py`: runs only explicit, verified project commands in `checks.json` without a shell. Empty commands yield NOT_CONFIGURED (exit 2), never a fake PASS.
- Before editing `checks.json`, Bootstrap inspects the actual project and asks for approval where required. Commands run in project root and have a timeout; do not add destructive commands.

**Not installed:** Codex hooks, native named subagents, approval ledger, snapshot lifecycle, gate engine and review-loop automation. Codex support differs by version. Read the relevant specs and implement those integrations only after checking official support; do not claim COMPLETE just because these baseline scripts exist.

**Other platforms:** the scripts use plain Python and may still work, but Codex config/agent/skill invocation needs translation and validation for Claude Code, Copilot, Cline, etc.
