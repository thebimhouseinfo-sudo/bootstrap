# Copilot-native Bootstrap (VS Code Copilot harness)

**Node.js requirement:** Native hooks invoke `node`. Confirm it is on PATH for the actual Copilot hook execution environment; if absent, the setup agent must arrange a verified equivalent or report the unresolved limitation instead of claiming hooks loaded.

**Select Session Target: GitHub Copilot (not VS Code Local, Claude or Codex harness).** Choose **Planner** in the agent selector. A model named Claude/Codex inside Copilot does NOT switch the harness. This runtime uses `.github/agents/*.agent.md`, `.agents/skills` and `.github/hooks/criteria.json`.

## Startup sequence

1. Installer: `--runtime copilot --tier Standard --staged`, after normal consent, preview and `--apply`. No second generic port or generated hook is required. Requires Node.js available to Copilot's hook execution host.
2. Open a real Copilot agent session and confirm Planner/technical-advisor are discoverable. Inspect installed hook in VS Code Copilot customization view; verify `sessionStart` and `preToolUse` fire. Do **not** copy Local/Claude `PreToolUse` JSON into Copilot.
3. Planner discovers goals (greenfield) or CURRENT/DESIRED/GAP (brownfield), without editing `docs/CRITERIA.md`. **Do not invoke Advisor** until Human explicitly asks to write/finalize the displayed draft or agreed existing delta.
4. On Human request to write, stage exact **full future file** as `harness/criteria-proposal.md` (ignored local state). Invoke **technical-advisor as a real Copilot subagent** on this proposal and existing Criteria if present. Advisor advises; it never approves, rejects or writes.
5. Planner presents Advisor advice to Human, runs `node .github/hooks/criteria-apply.cjs status` to display the one-time confirmation, and asks Human for a NEW message containing exactly `CONFIRM CRITERIA <nonce>`. Do not generate the Human's message; the `userPromptSubmitted` hook sees that real event.
6. On confirmed decision, run `node .github/hooks/criteria-apply.cjs` to atomically write the EXACT unchanged staged proposal, consuming the receipt. Direct edit/write tools aimed at `docs/CRITERIA.md` are denied by `preToolUse` regardless of role. Staged content changes or concurrent Criteria modifications invalidate the confirmation.

The gate is not a signature service. It relies on hook dispatch, a real subagent event and a new chat prompt; local state remains editable by sufficiently privileged agents. Native hooks cannot universally intercept indirect shell/MCP edits, and timeouts can fail open. **Never claim cryptographic Human identity or universal protected file writes.** Smoke-test each tool route in a disposable project and report limitations. If Advisor cannot be invoked natively, stop with `ADVISOR_DELEGATION_UNAVAILABLE`, not a fake consultation.

If setup starts from a legacy `--runtime generic --target-app copilot` installation, do not overwrite or rebind its managed state automatically: request a reviewed adapter migration (or install Copilot runtime into a clean test project).

## Diagnostic checklist (on a disposable checkout)

- Initial Criteria missing: no Advisor during brainstorm; draft in chat; Human asks to finalize; Advisor must be observed before confirmation and write.
- Existing Criteria: settle precise delta in chat; Human requests update; Advisor sees existing and delta; Human confirms afterward; only exact staged content is written.
- Direct file write/edit/shell referencing Criteria: denied before write, no file damage.
- A stale, wrong or repeated confirmation: denied.
- A different draft or existing file SHA after advice: denied.
- Regular non-Criteria edits work.
- Missing Node/runtime hooks, mismatched Session Target, alternate MCP or indirect shell writes: **UNVERIFIED** rather than claimed protection.

Official contracts: https://code.visualstudio.com/docs/agent-customization/hooks and https://code.visualstudio.com/docs/agent-customization/custom-agents.
