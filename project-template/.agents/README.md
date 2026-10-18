# Subagents and skills — portable content

- roles/ contains immediately reusable generic behavioral instructions: planner, reviewer, critic/CR, coder, tester, optional explorer/fixer.
- skills/ contains reusable generic SKILL.md content.
- config/ holds project-local placeholders: real model IDs, optional coder/tester knowledge and skills.
- knowledge/ holds optional project host/dialect/API references.

**Portable content is READY TO ADAPT, not runtime-registered.** Bootstrap must map agent and skill files to the native paths/schema for the identified runtime, configure actual permissions/models, and test activation. Planner/Reviewer/Critic contracts should stay stable across projects. Coder and Tester function generically with empty custom packs, but reload relevant verified project skill+knowledge when present.
