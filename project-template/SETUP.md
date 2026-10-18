# Setup contract — Codex-first, reuse by default

1. Copy the **contents** of project-template into target project root, never overwrite existing user files without review.
2. Codex is the default: root AGENTS.md and generic .agents/skills are already populated. Reuse .agents/roles instructions; native named-subagent binding requires version verification.
3. For existing code, inventory repo/OS/host/runtime/model/test commands; populate PROFILE and tailor only project-specific instructions. For blank projects, Planner starts Discovery with brainstorm/research and records OPEN decisions in CRITERIA.
4. Do not rewrite generic role/skill workflows per project. Add optional specialist skill/knowledge packs separately for Coder/Tester when user approves.
5. Read harness/specs and implement the runtime-specific hooks/approval/gate/snapshot/trace/loop mechanisms for the selected tier; scripts are NOT universally portable. Codex adapters may be supplied but must not be represented as verified without tests.
6. Test generic agent workflows and both allowed/blocked guard scenarios in a disposable copy. Distinguish READY (portable content), CONFIGURE (target facts/native mapping), IMPLEMENT (runtime scripts), and ENFORCED (actual tested guard).
7. For Claude Code/Copilot/Cline translate only runtime interfaces, not product theory or reusable role logic.
