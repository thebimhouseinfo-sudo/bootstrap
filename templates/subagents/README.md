# Portable subagent library

**Reusable across projects**: planner, reviewer, critic (CR) contracts should remain unchanged unless a deliberate versioned generic library update is approved. Coder and tester have effective generic defaults. Explorer and harness-fixer are optional/Full.

Bootstrap adapter responsibilities:
1. Verify target agent runtime/version from official docs. Map each role to native agent definition format, scopes and tool permissions; do not copy these files into a native config directory and claim it works.
2. Assign model/reasoning only from verified available IDs, with explicit user choice for unavailable selections.
3. Install default generic skills and optional project-specific coder skills (via user-controlled manifest) without changing role invariants.
4. Execute harmless simulated role tests: critic context isolation, coder works with no specialized skill, planner cannot code, reviewer does not broaden goal, and unauthorized approval stays blocked.
5. Mark non-enforceable restrictions GUIDED_ONLY.

Skill selection: always allow generic fallback, never silently bypass required tests or host constraints.