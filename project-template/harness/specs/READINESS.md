# Readiness contract

READY_CONTENT means documented generic skills/role instructions exist; it does not imply runtime activation.
SCRIPT_TESTED means tests of script logic succeeded on named Python/OS versions.
RUNTIME_VERIFIED means named Codex CLI version/trust/approval mode actually loaded skills/roles/hooks and passed negative/positive acceptance.
ENFORCED requires validated permissions/hooks, no override bypass and human-only channel tested.
UNVERIFIED for any combination not exercised (including Desktop when only CLI was tested).

Preflight must distinguish project config from parent session, managed/CLI overrides and trust. In approval_policy=never sessions, interactive approval features may be unavailable. Do not change global policy or work around untrusted hooks. Report restart/review steps and evidence.
