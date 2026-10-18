# Codex-first setup and portability

**Default runtime: Codex CLI / Codex IDE in trusted project.** The generic AGENTS.md and .agents/skills are ready to use without rewrites. Role instructions in .agents/roles are ready as portable behavioral contracts; Codex must delegate/read them, and native subagent names require a verified adapter. Custom project skills/knowledge are optional and must not be fabricated.

**Need to fill:** project product theory, host/profile, model IDs when required, verified build/test commands, existing-system integration. Planner owns product-specific content; Bootstrap owns runtime-specific environment.

**Need to implement/test:** actual hooks or equivalent lifecycle wiring, protect/approval authorization, snapshot/restore, gate engine, trace generator and automated loop. The specs are complete contracts but are NOT executing guards. Never claim complete automatic harness until verified.

**Other runtimes:** Claude Code, Copilot, Cline, etc must adapt AGENTS/agent entrypoint, skills location/metadata, native hooks, subagent permissions and scripts, then run positive/negative tests. The universal theory, role and skill content should stay intact.

**Codex smoke test:** in a disposable trusted project run Codex; confirm root AGENTS guidance and skill discovery; ask it to use brainstorm-theory, then a mock one-goal coder/tester task. Check results, no protected edits or pushes, and mark any missing native feature UNVERIFIED.
