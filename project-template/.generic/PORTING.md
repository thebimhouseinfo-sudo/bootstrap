# Porting the generic source to another coding agent

## Minimal adaptation contract

- **Inputs:** selected Lite/Standard/Full tier, exact target client/extension and version, provider/model, OS/shell, available tool/permission model, Git active branch, existing project facts, human's approval path.
- **Scope:** do not rewrite `.generic/agents/<role>.md` or `.agents/skills/` simply to fit a syntax change. Copy approved role text into the **real supported host registration mechanism**; link to project `AGENTS.md` where supported. Host syntax is not shared across apps.
- **Model/provider:** user selects actual available model, no invented fallback, account ID, endpoint or credential; never write API keys into tracked templates.
- **Host actions:** determine actual agent discovery and skill loading; inspect hooks, permission request UX and tools. A file with a native-looking filename is not proof the host loaded it.
- **Safety:** no claimed enforced read-only/approvals/sandbox without a host negative test. Reuse optional Python helpers only where integration is verified.
- **Verification:** run `harness/common/inventory.py --tier TIER --runtime generic` for packaged source inventory; this does NOT verify converted native adapters. Run host tests for role discovery, allowed work, blocked protected actions, model validity and build/test checks, record evidence and caveats. Do not claim full autonomous gate engine.

## Host routing examples

- **Cline:** `platforms/cline.md` — Cline-specific rules/instructions; verify native discovery before porting roles.
- **Qwen Code:** `platforms/qwen-code.md` — project-level `.qwen/agents/` role registration (verified documentation), with explicit permissions.
- **DeepSeek:** `platforms/deepseek.md` — DeepSeek may be a **model/provider used inside another coding client**, not a unique native coding runtime. Ask which client is running; port to that client, then configure its supported provider/model.

For other apps, use the same workflow with documented native paths; **never install all platform adapters together**. Portable role source and per-project configuration are different layers.
