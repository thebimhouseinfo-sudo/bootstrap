# Claude Code — change subagent model only when necessary

**Defaults already configured in `.claude/agents/*.md`:** Planner/Reviewer/Critic/Harness Fixer: `opus`; Coder/Tester: `sonnet`; Explorer: `haiku`. **Chat model/effort stays user-selected**; `.claude/settings.json` does not override it.

If user plan lacks a model or user asks to optimize quota/quality: verify available provider aliases and agent-specific effort fields for their Claude Code version, ask the user, then edit only `model:` frontmatter in affected `.claude/agents/<role>.md`. Set effort only if supported and explicitly needed. Never silently fallback or rewrite generic instructions. Confirm actual native agent discovery and safe invocation. Runtime approvals/hooks remain separately unverified.
