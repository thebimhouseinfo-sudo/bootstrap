# Hook implementation guide — runtime-specific

1. Discover whether the selected agent runtime/version supports SessionStart, user prompt capture, pre-edit/pre-command and Stop (or equivalent); consult official documentation.
2. Implement only supported lifecycle events. Examples: journal capture/redaction, snapshot before modifications, quick checks after edits, final verify with max 3 guarded retry cycles.
3. Unsupported events → provide explicit manual/task-runner/MCP fallback; mark GUIDED_ONLY where constraints cannot be enforced.
4. Log rule ID, reason, scope and how to unblock. Test one allowed and one denied scenario in a disposable workspace.
5. Hook instructions are not executable hooks. Do not invent native filenames or JSON schema before verifying runtime.
