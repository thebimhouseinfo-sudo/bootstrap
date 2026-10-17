---
name: context-reload
description: Use at session start, task start, or verified project context change to select and reload relevant worker skills and technical knowledge.
---

# Context reload for Coder and Tester

1. Read project profile and optional worker-context manifest, if present.
2. Select relevant trusted SKILL.md files and verified knowledge sources for the current role, host/version and task; do not preload unrelated packs.
3. Refresh changed references by version/hash when available. Keep original role invariants, approval permissions and independence of Tester.
4. If optional skill/knowledge is absent or fails to load, proceed with generic code investigation, official-doc checks as available, test/debug iterations and clear uncertainty. Never claim unavailable material was loaded.
5. Obey explicit host/compatibility requirements in PROJECT_PROFILE even when optional knowledge packs are unavailable. Unknown API → investigate or test; do not knowingly substitute a different language's constructs.
6. Record what was loaded, provenance/version and any unavailable sources in evidence when relevant.

Example: a verified Visual LISP pack can prevent accidental Common Lisp constructs and shorten review/test cycles, but lack of that pack is not itself a blocker. The agent must still discover the host dialect and verify the actual implementation.
