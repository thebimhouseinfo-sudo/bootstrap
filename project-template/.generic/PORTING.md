# Agent-executed native port: mandatory generic setup stage

**This is an action contract for the installing agent**, not instructions for the Human to hand-code their host adapter. The generic installer copies the requirements first; the same setup run must attempt to build, register, test and document the actual host-specific scripts before claiming completion. Begin with [ADAPTER_REQUIREMENTS.md](ADAPTER_REQUIREMENTS.md).

## Minimal adaptation contract

- **Inputs:** selected Lite/Standard/Full tier, exact target client/extension and version, provider/model, OS/shell, available tool/permission model, Git active branch, existing project facts, human's approval path.
- **Scope:** do not rewrite `.generic/agents/<role>.md` or `.agents/skills/` simply to fit a syntax change. Copy approved role text into the **real supported host registration mechanism**; link to project `AGENTS.md` where supported. Host syntax is not shared across apps.
- **Model/provider:** user selects actual available model, no invented fallback, account ID, endpoint or credential; never write API keys into tracked templates.
- **Host actions:** determine actual agent discovery and skill loading; inspect hooks, permission request UX and tools. **Implement and register** those native adapters under verified host-supported paths. A file with a native-looking filename is not proof the host loaded it.
- **Safety:** no claimed enforced read-only/approvals/sandbox without a host negative test. Reuse optional Python helpers only where integration is verified.
- **Verification:** run `harness/common/inventory.py --tier TIER --runtime generic` for packaged source inventory; this does NOT verify converted native adapters. Then run native host tests for role discovery, allowed work, blocked protected actions, model validity and build/test checks. Record generated adapter paths and real allow/deny evidence in setup-live-evidence; their hashes are checked at activation. Do not claim a full autonomous gate engine or authenticated Human decisions merely from hooks.

## Host routing examples

- **Copilot / VS Code:** `platforms/copilot.md` — select the Copilot harness, use documented `.github/hooks/*.json` for native hooks, check host policy, and negative-test against Criteria writes. `--target-app copilot` alone does not install those files. The current pre-write checkpoint is instruction-guided, **not hook-enforced**.
- **Cline:** `platforms/cline.md` — Cline-specific rules/instructions; verify native discovery before porting roles.
- **Qwen Code:** `platforms/qwen-code.md` — project-level `.qwen/agents/` role registration (verified documentation), with explicit permissions.
- **DeepSeek:** `platforms/deepseek.md` — DeepSeek may be a **model/provider used inside another coding client**, not a unique native coding runtime. Ask which client is running; port to that client, then configure its supported provider/model.

For other apps, use the same workflow with documented native paths; **never install all platform adapters together**. Portable role source and per-project configuration are different layers.
