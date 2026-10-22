# GitHub Copilot in VS Code — installing agent generates native adapter

`--runtime generic --target-app copilot --tier Standard` installs portable role text and Python support, **PLUS the packaged Copilot-native `.github/agents` and `.github/hooks`**. The same is true for generic CLI targeting Copilot. The installer now includes a Copilot-native adapter. It must be **verified in the actual Copilot harness**; `.github/README.md` explains the scoped hook and limitations. Do not regenerate the packaged adapter from scratch unless the Copilot API has changed.

## Distinguish client, harness and model

Select the actual **Session Target / harness**. Running a model named "Codex" or "Claude" inside a **Copilot** session does not make `.codex/hooks.json` or `.claude/settings.json` authoritative for that Copilot session. See the official VS Code *Agent harnesses* and *Configure agent hooks* documentation.

## Native Copilot validation checklist (executed by setup agent after permission)

1. Inspect the target VS Code / Copilot runtime and whether its native hook feature is available and permitted by the organization.
2. Port required project roles/instructions into documented Copilot-native mechanisms; keep `.agents/skills/` as reusable source. Test that Planner and Technical Advisor really appear as active roles. Merely listing generic `.md` files is insufficient.
3. For Copilot harness, repository hook definitions are discovered from `.github/hooks/*.json`, with documented `preToolUse` and `sessionStart` events. The Copilot schema is **NOT** the Codex/Claude schema. Implement and register a reviewed native hook, using the exact Copilot event payload and top-level `permissionDecision: "deny"` when denial is supported.
4. Test on a **disposable project**: (a) hook is visible/dispatched; (b) harmless edit allowed; (c) protected Criteria write denied **before the file changes** without the required independent authorization; (d) alternate write routes (terminal, agent edit tool, MCP) checked separately. Unsupported routes must be reported as gaps, not as enforced.
5. A hook can deny known tool calls but **cannot prove that Technical Advisor consulted Human** merely from prompt text. Bootstrap currently has no authenticated pre-write Criteria gate. Until a genuinely independent, host-verified authorization mechanism exists, treat Advisor/Human coordination as **GUIDED_ONLY** and require Human review of any Criteria change.
6. Record real host evidence. Do not set `ENFORCED` or `READY` based on package copy, `Standard` tier, script-only smoke, or a positive test alone.

**Current shipped state:** the installer packages `.github/agents`, `.github/hooks/bootstrap-criteria.json`, and `.github/copilot-instructions.md` for `target-app copilot`. Verify installed discovery in Copilot. `Hooks: 0` after native install is **not** success. The hook's pre-write block and native ask are limited to recognized tool calls, not universal write enforcement. Stop at `PORT_REQUIRED` **only if** research/testing shows the capability is unavailable or necessary permissions are denied; explain the evidence and limits instead of skipping the port.

Official references:
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://code.visualstudio.com/docs/agents/run/agent-harnesses
- https://docs.github.com/en/copilot/reference/hooks-reference
