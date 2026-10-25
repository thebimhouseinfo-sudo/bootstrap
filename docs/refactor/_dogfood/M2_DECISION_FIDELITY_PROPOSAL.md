# M2 — Pre-Code Proposal: optional Discussion Job, Secretary records, Planner decision fidelity

**Status:** PRE-CODE working proposal / GUIDED_ONLY review. **Authority:** Unified v7.0 Detailed Plan, E1–E3 and M2-T1..T5. **Branch:** refactor/functional-dogfood-v7.

## Observable result

Human explicitly requests a Discussion Job → open a working documentation context directly (not an execution Job). A vague request to discuss → offer once only. Normal discussion does not need any job. Only when a recording context is active and Human accepts a specific decision, the Secretary recording method writes the FULL chosen solution, evidence, input/output, examples, exceptions, rejected alternatives, risks, and outstanding questions, then verifies readback. Later corrections supersede but never overwrite/delete original accepted text. Planner links full accepted records into Goal/Task/acceptance and preserves them over handoffs. Criteria and Advisor unchanged.

## Concrete source and caller map

| Task | File and action | Functions / behavior | Consumer |
| --- | --- | --- | --- |
| M2-T1..T3 | CREATE project-template/.agents/skills/record-decisions/SKILL.md | On-demand Secretary method: optional open, accepted Decision capture, index current/superseded, full record/readback, failed-write reporting. No parser/daemon or new Job state. | Existing leading agent and Planner on active Discussion Job |
| M2-T4 | MODIFY project-template/.agents/roles/planner.md | Read full current decision refs and status before Plan; Goal/Task coverage/conflict/feasibility; preserve Human-chosen procedure and protected Criteria boundary. | Host Planner adapters |
| M2-T4 | MODIFY project-template/.agents/skills/plan-task/SKILL.md | Link accepted Decision source, cover every applicable step, reject conflict/superseded sources without losing history. No forced Discussion Job. | Planner task derivation |
| M2-T4 | MODIFY project-template/docs/IMPLEMENTATION_PLAN.md | Add accepted Decision refs and coverage/conflicts to existing Goal/Plan fields; no second Plan. | Human/Coder/Reviewer |
| M2-T1 | MODIFY project-template/AGENTS.md | Route explicit Discussion Job requests to scoped recording skill; do not trigger automatically. | Existing installed hosts |
| M2-T4 | MODIFY 7 existing Planner role host adapters | Distribute full canonical text while retaining TOML/YAML/Markdown host wrappers. Generic exact, Codex, Claude, Continue config + rules, Antigravity, Copilot. | Host native agents |
| M2-T5 | MODIFY tests/test_installer.py | Existing-installer regression for skill presence, role mirroring and Goal/Plan fields. | GitHub Actions six OS/Python jobs |
| Non-goals | REUSE_AS_IS | install.py, tiers, branch authority, Task runner, Criteria, App source, separate Secretary agent, generic identity/registry, database, new approval gate. | Existing owners |

## Data and workflow contract

User explicitly opens Discussion Job → agent reads recording skill → creates an authorized project-local readable directory only if user project/host write authority permits → remembers this active discussion in its existing context → a Human-accepted decision produces a complete DEC reference and an index link → file write/readback verified → Planner reads the **full currently accepted record** and links Goal/Tasks → Coder later reads the same source. The illustrative DEC reference is a navigational label, not a mandatory SHA/GUID or business ID. Ordinary chat without recording stays unchanged.

Record fields: title; ACCEPTED/UNRESOLVED/SUPERSEDED; available Human source evidence (no invented URLs); ordered exact intended behavior; reason; environment/domain rules; concrete user examples; exceptions, limits and risks; rejected alternatives and why; open questions; linked Goal/Tasks; supersession links. No Assistant speculation can be marked accepted. Write error = NOT_VERIFIED, never saved.

## Reviewer and overengineering check

Do NOT add Secretary daemon, universal decision ledger, content-hash registry, automatic Discussion Job classifier, new approval engine, active Plan state, Advisor call, or forced permanent file/version identity. A short Plan abstract is NOT a replacement for the accepted decision source. Reviewer should keep existing roles and source ownership. Guided architectural self-check supports narrow design, but **independent Reviewer PASS is UNVERIFIED**.

## Acceptance scenarios

1. Explicit open directly; generic invitation offers once; normal question does not open.
2. Detailed eight-step Human decision survives recording/readback, subsequent Plan rewrite and Coder handoff in full.
3. Rejected/unresolved assistant ideas never become ACCEPTED.
4. Revised decision preserves readable old record and current/superseded references.
5. Write failure does not claim persistence.
6. Criteria remains unchanged; no unsolicited Advisor gate.
7. All installed hosts package focused skill and preserve role content.
8. SCRIPT_TESTED static/installer parity is not claimed to prove native conversational behavior.

This descriptive Pre-Code proposal is kept TEMPORARY in _dogfood and deleted from release HEAD after actual review and completion.
