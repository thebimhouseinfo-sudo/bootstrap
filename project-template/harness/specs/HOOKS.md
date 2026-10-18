# Codex-first native hooks and portability contract

**Installed for Codex:** `.codex/hooks.json` declares `SessionStart`, `PreToolUse` (exact `apply_patch`), and `Stop`; each calls `harness/codex/hook.py` using the installed Python interpreter (project-root lookup works from nested directories). Hook JSON input/output follows official Codex hook schemas: https://learn.chatgpt.com/docs/hooks

**Runtime trust:** project config and hook definitions must be trusted using Codex `/hooks`; administrative policies can disable hooks. Project-local scripts are not system-enforced controls, and parent sandbox/approval still applies. Never auto-bypass hook trust.

- **SessionStart:** injects bounded contract/status context.
- **PreToolUse:** in Git projects first checks the explicitly configured active development branch from the Git common directory; unknown/frozen/unregistered/detached checkout causes an observed direct apply_patch to be denied. Non-Git projects do not need this Git-only configuration. This hook cannot cover shell/MCP/hosted edits. Then it makes a hash-checked pre-edit snapshot of existing files identified in direct `apply_patch` headers when `hook-policy.json` enables it. Known protected paths receive warning; the hook does not authenticate human decisions. Supported direct `apply_patch` operations may be denied if a requested snapshot fails. Shell commands, hosted tools and many MCP changes can bypass this path: do not claim full file-write protection or a universal sandbox.
- **Stop:** only for a configured `ACTIVE` goal in `harness/active-task.json`. Validate scoped goal/theory/test/evidence links, then run configured `harness/common/checks.json` (no shell). A failed check requests **one** continuation; `stop_hook_active` suppresses further automatic retries. No check config or no approved active task → no fake PASS and no forced continuation. This neither signs G0/G11 nor calls subagents.
- Hook policy fields in `harness/hook-policy.json`: `snapshot_apply_patch`, `stop_verify`. Default enabled for supported paths; activation is conditional on a real active task and approved command list.

**Port to Claude/other CLI/IDE:** reuse Python `common/*.py`; adapt event names, JSON schema, command lookup/trust and supported blocking semantics. If no matching hook, provide a manual runner and label GUIDED_ONLY. Equivalence means measured outcomes, not copying Codex JSON verbatim.

**Evidence required:** allowed/blocked apply_patch, hash-snapshot, Stop PASS/FAIL/NOT_CONFIGURED, trust prompt and actual Codex native invocation on the user’s version; CI Python tests alone do not certify the host.
