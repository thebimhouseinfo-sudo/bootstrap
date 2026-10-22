# Copilot has a packaged native runtime

**For a fresh Copilot harness project select `--runtime copilot`**, which installs `.github/agents/`, `.github/hooks/` and `.github/COPILOT_SETUP.md` from Bootstrap. This generic porting guide remains for legacy generic installs; upgrading from an existing generic Copilot installation requires reviewed migration of managed files/state, not silent rebinding.

## Legacy generic installations only

The remaining work for an existing generic Copilot project is a reviewed migration to the packaged native adapter. Inspect existing native files and managed state, preserve user changes, and reconcile them with `.github/COPILOT_SETUP.md`. Do not run the first-install generic command again: the installer rejects new `generic --target-app copilot` installs.

Verify the actual Copilot Session Target, Node.js, native role discovery and hook allow/deny events on a disposable project. Native scripts are procedural, tool-scoped checks; they do not authenticate Human identity or cover every indirect shell/MCP write. Never fabricate Advisor or Human events to complete a migration.

Official references:
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://code.visualstudio.com/docs/agents/run/agent-harnesses
- https://docs.github.com/en/copilot/reference/hooks-reference
