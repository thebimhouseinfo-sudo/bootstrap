# Continue native configuration and hook setup (CLI vs IDE)

**There are two different Continue runtimes.** The `cn` terminal CLI (TUI) and the Continue IDE extension do **not** share a verified native tool-hook runtime. For the CLI, upstream code merged Claude Code-compatible hooks in March 2026, reading `.continue/settings.json` from the project, and `PreToolUse`, `SessionStart`, `SubagentStop`, `UserPromptSubmit`, `Stop` event payloads. For the **IDE extension**, there is no verified native preToolUse interception of the editor's built-in write tools. Do not report hooks loaded merely because `.continue/settings.json` exists.

## Files installed

- `.continue/config.yaml` and `.continue/agents/<role>/config.yaml`: workspace and role-specific Continue YAML; configure an actual model/provider first, without fabricated credentials. The **selected** config determines the active role; these files aren't automatic isolated subagents.
- `.continue/rules/00-bootstrap.md` and `01-criteria-gate.md`: always-on **instruction** rules. Rules are used in Continue Chat/Agent/Edit but cannot deny tool execution themselves.
- `.continue/skills/<skill>/SKILL.md`: tier-filtered copies of the canonical `.agents/skills/` library, discovered by the CLI Skills tool. The agent must test real discovery via `/skills`; file copy alone is a script-level check.
- `.continue/settings.json`: CLI-native Claude-compatible hook registration. The CLI loads project scope settings; may also load `.claude/settings.json`. Avoid double registration when installing multiple harnesses together.
- `.continue/hooks/criteria-gate.cjs`: reads Continue CLI `hook_event_name`, `session_id`, `tool_name`, `tool_input`, `agent_type`, `last_assistant_message`; emits hookSpecificOutput and exits 2 to refuse unsafe direct writes.
- `.continue/hooks/stop-verify.cjs`: on an ACTIVE task with stop_verify enabled, validates task evidence and approved checks at Stop; a failure returns blocking feedback. The CLI upstream can set `stop_hook_active=true` on the initial Stop, so that flag does not skip validation. Host retry/continuation behavior still requires live verification; the script does not launch an agent retry.
- `.continue/hooks/criteria-apply.cjs`: one-time apply only after exact proposal was advised and a **later** Human prompt was observed for the same session and SHA. The receipt is `harness/criteria-guard.continue.json`, includes `runtime: continue`, and cannot consume a Copilot receipt. The shared proposal stays at `harness/criteria-proposal.md`. Both are local-only; keep one Criteria transaction active per project.

## Real-host verification the installer cannot do automatically

1. Inspect `cn --version`, whether the user is running **CLI TUI**, IDE extension, or headless `cn -p`. Ensure `node` resolves in the actual command-hook environment.
2. For CLI, launch `cn` in the **project root** with the real account/model configured, not `--auto` for first test. Inspect that `.continue/settings.json` and `.continue/rules/01-criteria-gate.md` load. Exercise a harmless edit (allowed), a direct edit of `docs/CRITERIA.md` (DENIED before mutation), and a benign Criteria read (allowed).
3. Planner shows initial whole Criteria draft or agreed existing delta **in chat**, and asks Human to request writing. **Only at that request** should Planner consult Advisor. Continue CLI `--agent` and alternate role config are not proof of a `SubagentStop` event; event dispatch for that mode must be tested rather than assumed. If no genuine event can be observed, the protected one-shot apply remains locked. Do not synthesize a subagent event. The Advisor YAML is a selectable role config, not a registered native subagent identity. A separate chat named advisor is not evidence of `agent_type=technical-advisor`; that exact genuine event must be supported and observed before this gate can unlock. For Codex Planner → Continue Coder, keep Criteria decisions in the verified Planner host and hand only approved coding tasks to Continue.
4. If an Advisor event and a subsequent Human chat prompt really are observed, display `node .continue/hooks/criteria-apply.cjs status` and follow its one-time confirmation flow. No new Human confirmation means no write.
5. For IDE extension, CLI hook scripts alone do not protect normal editor write tools. Restrict write-tool permissions via Continue's tool policy UI and use Human review, or implement a separately verified IDE interception route; honestly record `GUIDED_ONLY / NATIVE_HOOK_UNVERIFIED`.
6. CLI **headless `cn -p`** is not verified to dispatch hooks consistently across versions. Do not use it to claim authorization, and do not assume that a project CLI hook is invoked by the VS Code extension.

## Limitation

This is the **maximum defensible Continue-native hook configuration** evidenced by the CLI source, not proof the user's Continue release dispatches all events. The upstream command/prompt "agent" hook handler is unimplemented in the inspected CLI source: hooks **do not automatically summon Technical Advisor**. Requiring true independent Advisor and Human confirmations is fail-closed: without those observed events, Criteria cannot be updated through the helper. No agent-writable JSON file proves authenticated Human approval. Paths invoked indirectly by privileged tools can bypass the pre-tool parser; verify the claimed boundaries in the user's actual host.

Sources: https://github.com/continuedev/continue/blob/main/extensions/cli/AGENTS.md ; https://github.com/continuedev/continue/blob/main/extensions/cli/src/hooks/types.ts ; https://docs.continue.dev/customize/deep-dives/rules ; https://docs.continue.dev/cli/configuration

## Multi-harness upgrades and verification

Copilot stores its receipt separately at `harness/criteria-guard.copilot.json`. Old unscoped `harness/criteria-guard.json` receipts are intentionally ignored: obtain fresh advice and a fresh post-advice Human confirmation after upgrading. Do not rename an old receipt to unlock the helper.

For Criteria shell reads, use a simple literal `cat`, `head`, `tail`, `type` or `Get-Content` command, or a native read tool. `sed`, search tools with execution options and interactive pagers are not accepted as shell read exceptions. General shell/MCP isolation remains unverified.

Run both `python harness/common/task.py` and `python harness/common/verify.py` directly when handing off an active task until the installed Continue version's real Stop dispatch and blocking behavior are verified. A passing script fixture is not a live host result. Record the exact Continue version and tested CLI/IDE surface.

The lifecycle lock hashes all installed native adapters listed in the install manifest, including this Stop hook. It does not establish native readiness for secondary hosts. See `../harness/MULTI_HARNESS.md` for Codex planning and Continue local-model coding.
