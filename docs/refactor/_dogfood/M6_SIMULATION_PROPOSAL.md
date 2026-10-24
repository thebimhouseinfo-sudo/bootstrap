# M6 — PRE-CODE Proposal: Tester-owned simulation skill and advanced diagnosis

**Status:** GUIDED_ONLY design assessment, no independent Reviewer sign-off. Authority: Unified v7 functional M6, H0–H6. Preserve the user-supplied Claude `simulate.skill` bundle as original reference source, not assistant-authored substitute.

## Goal and existing source

Tester can selectively activate `simulate` within an existing assigned Test Task. Original `simulate/SKILL.md` and its five references (app-brief-template, input-catalog, external-mocks, example-autocad-addin, harness-playwright) are the methodology. Designer (before reading code) derives user journeys and oracle from accepted Criteria/README/App Brief/observable UI; freezes expected outcomes; Tracer then drives public entrypoint and traces actual triggered subflows. T0–T6 remain the authored taxonomy; do not create competing S1–S4 gates.

Already existing Tester role and `test-and-verify`, `bug-fix-loop`, `systematic-debugging` provide independent test and retry concepts; missing parts are the on-demand `simulate` activation, causal fan-out and more explicit three-failed-retest escalation to an **advanced** cross-flow root-cause mode.

## Proposed source responsibility by Task

| Task | Path and action | Caller / expected behavior |
| --- | --- | --- |
| M6-T1/T2 | REUSE_AS_IS the exact original `.agents/skills/simulate/SKILL.md` and five references (import source verbatim) | Tester invokes as needed. Do not create new Simulation Job, Contract, manager or mandatory `FROZEN.md` file beyond existing evidence. |
| M6-T1–T4 | MODIFY `.agents/roles/tester.md` | Explicit activation of `simulate` in ordinary Test Task, T0–T6, Designer→Tracer discipline, mock-vs-native evidence, causal child-flow capture. |
| M6-T3 | CREATE small `.agents/skills/simulate/references/bootstrap-causal-fanout.md` | Optional guidance for parent/child flow IDs, origin, queue/lease/wait graph, callbacks, terminal/stranded states and same-input double-dispatch; not an app runtime or permanent trace manager. |
| M6-T5/T6 | MODIFY `.agents/skills/bug-fix-loop/SKILL.md`, `.agents/skills/systematic-debugging/SKILL.md` and `.agents/skills/test-and-verify/SKILL.md` | Same defect, up to three Coder fix + independently replayed user-entrypoint Tester retests. After failed third STOP normal patching, invoke existing advanced causal root-cause mode/skill, hypotheses and discriminating experiments; return to Reviewer if architecture affected. |
| M6-T1 | MODIFY 7 native/project Tester role mirrors via full canonical text, preserve TOML/YAML/Markdown wrappers | Existing installer copies same roles; no installer architecture change. |
| M6-T7 | MODIFY `tests/test_installer.py` | Verify real original skill+reference package intact (source checksums/UTF-8 lengths/known headings), correct packaging across current Codex/Claude/Continue layout, retry and causal guidance shipped. Static test does not prove Tester actually executed scenarios. |
| All others | REUSE_AS_IS `install.py`, tiers, GSA, CAD, project data and Criteria | No new runtime engine, tester agent, CLI or simulation gate. |

## Acceptance and reviewer challenge

- An app-user action may inadvertently create two child flows; trace **every** child, not only single Input→Handler chain. Identify why each flow was spawned, who owns CAD capability or other shared state, who waits, and why entire user request remains stuck.
- Report T0–T6 behavioral simulation at actual user entrypoints with exact observed input/output; mocks test app reaction to simulated outcomes, **not real AutoCAD geometry or host recovery**.
- Preserve user-facing acceptance criteria and original expected result even when code differs. An unrun native host remains UNVERIFIED.
- On third failed independent retest, no fourth ordinary blind patch and no defect-ID reset, use advanced systematic-debugging skills already present if adequate; otherwise smallest added focused skill only after need proven.
- If installing the whole scenario toolchain for one small feature would create a disproportionate subsystem, Tester can use suitable existing native/manual host test or mark host execution pending; Reviewer must challenge the new infrastructure rather than fabricate safety.
- Reviewer evaluation in this conversation is GUIDED_ONLY, not independent/native sign-off.
