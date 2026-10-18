# Claude Code native agents

The main chat model and reasoning are selected by the user; project .claude/settings.json deliberately does not override them.

Subagents are preconfigured in .claude/agents/*.md: Planner, Reviewer, Critic and Harness Fixer use Opus; Coder and Tester use Sonnet; Explorer uses Haiku. Full generic role instructions are already present; no need to rewrite.

For a user's different plan, model availability or quota/quality preference, follow MODEL_SELECTION.md. Ask the user before changing only affected role frontmatter; no silent fallback. Verify actual native agent discovery. Hook, approval, gate and orchestration mechanisms remain separate and must be tested.
