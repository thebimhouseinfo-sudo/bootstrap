# Setup intake — Host-native dialog and trace contract

## Two separate interactions

1. Before the installer tool-permission dialog, the agent sends **one short chat notice** explaining the difference between command permission and the setup questionnaire. The notice contains **no questions**.
2. The Human approves the actual command permission to obtain/preview the installer.
3. The agent uses a separate **host-native structured question dialog** to collect missing setup choices. A tool authorization click is NEVER an answer to a configuration question. Do not ask or accept setup answers in ordinary chat, shell `input()`, a terminal survey or `install.py --ask-first`.
4. After the native dialog returns, keep the host tool response in the session trace and persist only non-secret answers locally in `harness/setup-intake.json` once filesystem access is available.
5. If native input tools are missing, explicitly report `DIALOG_UNAVAILABLE` and stop before reporting setup audit or handoff success. Do not fabricate the dialog or automatically select the choices.

## Common fields (only if not already known)

- Tier: Lite / Standard / Full (recommend Standard when Planner/Tester are required)
- Harness Git configuration: local / tracked
- Human-selected active development branch and protected/frozen branches
- Missing product/technical context that cannot be determined from the workspace
- Runtime/provider details only when genuinely unresolved

The initial prompt already gives the project folder and identifies a new or existing project; do not re-ask either. Use native host tool output and the session trace as provenance for each question. Do not store credentials/secrets in the intake trace.

## Saved trace example — NOT real proof

```json
{
  "schema_version": 1,
  "channel": "native_dialog",
  "runtime": "codex",
  "host_event_ref": null,
  "responses": [
    {"id": "git_mode", "value": "local", "source": "native_dialog"}
  ]
}
```

When the host supplies a native dialog event ID, record it in `host_event_ref` for correlation. Otherwise use null, not a fabricated identifier. `setup_lifecycle.py audit` checks required fields and runtime consistency for staged installs, but does **not** independently authenticate the user, guarantee a dialog occurred or replace Human approvals.

`harness/setup-intake.json` is always local/private, including with `--config-git tracked`. Any CRITERIA / technical-direction / final-lock approvals remain separate Human Gates.
