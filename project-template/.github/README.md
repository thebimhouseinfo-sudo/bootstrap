# Copilot-native Bootstrap agent/hook setup

This directory is **not** a renamed `.generic` folder. VS Code Copilot discovers agents in `.github/agents/*.agent.md`, and the Copilot harness discovers repository hooks in `.github/hooks/*.json`. The installed hook uses the **Copilot camelCase** `preToolUse` schema and expects `toolName` and `toolArgs`. Select the **Copilot** session target, not a Codex or Claude harness selected inside VS Code.

## Criteria contract (both initial and existing)

1. **Initial:** Planner brainstorms and shows the full Criteria draft **in chat only**. No Advisor during drafting. When Human says to write/finalize the draft, the pre-write checkpoint calls **Technical Advisor** for advice on the exact draft. Human then decides after reading that advice; Planner only then requests a Criteria tool edit.
2. **Existing:** Planner discusses the new feature/removal and shows the exact agreed delta in chat without changing Criteria. On Human request to apply, the pre-write checkpoint calls Technical Advisor to advise on current Criteria plus delta. Human decides again after advice; Planner then requests an edit.
3. The `preToolUse` hook returns `deny` for directly named Criteria writes without a current local receipt. It tells the agent to call Advisor. After Human's **post-advice** decision, Planner can create `harness/criteria-write-authorization.json` referencing the current Criteria SHA256, a meaningful proposal ID, and a short expiry (15 minutes maximum). The hook returns `ask`, **never automatic allow**. Human checks the actual tool edit in the Copilot permission UI before approving.

Receipt example (only after the above consultation and Human decision):
```json
{
  "schema_version": 1,
  "target": "docs/CRITERIA.md",
  "baseline_sha256": "CURRENT_SHA256_OR_ABSENT",
  "advisor_consulted": true,
  "human_decided_after_advice": true,
  "decision": "apply",
  "scope": "initial",
  "proposal_id": "criteria-draft-v1",
  "expires_utc": "YYYY-MM-DDTHH:MM:SSZ"
}
```

The receipt is **agent-writable**, so it does not authenticate the Advisor or Human and may be forged by an untrusted agent. The native `ask` step is the final interactive approval; if the host cannot display it, do not treat the edit as authorized. Hook interception is **limited** to tool arguments explicitly naming Criteria and only while Copilot hooks execute. Indirect shell scripts, remote tools, disabled hooks, malicious modifications to hook/config or timeout fail-open behavior can bypass it. Do not call this universal file protection or an authenticated gate.

## Installation validation

Run `python tests/test_copilot_native.py` in Bootstrap (CI script simulation). In the **target project**, check Copilot session target, agent discovery, hook registration and a harmless read. Test a direct Criteria write denied before consultation on a disposable clone. Then check a valid receipt yields **ask**, not allow, and that Human sees the native approval request. Do not mutate real approved Criteria as a negative test.

Source: https://code.visualstudio.com/docs/agent-customization/hooks and https://code.visualstudio.com/docs/agent-customization/custom-agents
