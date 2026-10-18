# Codex-ready adapter

Codex recognizes project-root AGENTS.md and discovers project skills in .agents/skills/*/SKILL.md. The portable role descriptions live in .agents/roles for Codex to read and delegate as instructed; **these markdown role files are not native named subagent registrations**. If named subagents are required, verify the installed Codex version and generate its supported configuration before claiming they are active.

The project .codex/config.toml is intentionally conservative: no invented model IDs, OS-specific commands, privilege expansions, or unverified hook event schemas. All platform-neutral skills and role instructions can be used immediately by Codex through its normal agent workflow. Runtime hooks, human-only approval enforcement, gate daemon, snapshot runner and audit ledgers require real implementation/testing; never describe them as ready merely because contracts exist.

For Claude Code, Copilot, Cline and other engines, adapt agent registration, skill discovery, config, hooks, approval semantics and tests according to their official version-specific docs. Never copy Codex-specific native files unchanged into another runtime.

Check: launch Codex in a trusted test copy, confirm AGENTS.md and skills discovery, run generic planner/coder/tester examples, and record any unavailable native subagent/hook feature as UNVERIFIED. No unauthorized write or real remote action during smoke tests.
