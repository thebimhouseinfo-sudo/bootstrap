# M5 — Pre-Code Proposal: Reviewer whole-related-design evaluation

**Status:** Descriptive PRE-CODE. Source: Unified v7.0 Plan E8/E9, M5-T1..T6. Guided self-check only; real independent Reviewer invocation not available from current GitHub-only tool.

## Observable outcome
Reviewer reviews ALL interacting Coder Task-level design sections together, the complete accepted Human decision sources and verified brownfield code/callers. It catches duplicate gates, paths, state and unauthorized small-function→large-infrastructure expansion *before* source changes. Design verdict is PASS / CHANGES_REQUIRED / HUMAN_ESCALATION with concrete evidence; not code/test/native-host PASS. A corrected consolidated component list is derived from the SAME reviewed proposal, not a new registry.

## Source-level proposal
- MODIFY project-template/.agents/roles/reviewer.md: review scope/inputs, flow, cross-Task component reconciliation, proportionality, user-file lifecycle and exact 3 outcomes; technical Reviewer cannot invent domain rules or require a universal enterprise framework.
- MODIFY project-template/.agents/skills/goal-review/SKILL.md: add branch for descriptive PRE-CODE review, avoid review of one isolated Task when interfaces interact, require evidence and Human escalation only for missing consequential choices.
- MODIFY project-template/docs/reports/_REVIEW_TEMPLATE.md: add PRE-CODE input and outcomes without removing CODE/TEST PASS/FAIL/UNVERIFIED.
- MODIFY seven host Reviewer copies (.generic, .codex, .claude, .continue agent, .antigravity, .github, .continue role rule) preserving native wrappers and canonical text.
- MODIFY tests/test_installer.py: existing installer regression that reviewed role and review template ship unchanged.
- KEEP install.py, Criteria, Reviewer/Critic role separation, code source authority, GSA lifecycle, and all product file/Job identity unchanged.

## Acceptance
1. Two interacting Task proposals propose ReadGate and WriteGate for same authority: Reviewer catches duplication and requests simplification, not blind merge.
2. One Task proposes new interface with no caller: CHANGES_REQUIRED before source.
3. One small AutoLISP Test Task proposes a new DWG/binding manager: challenge Small Function → Big Solution → Larger System Impact; Human may choose manual LOAD/test and mark native host UNVERIFIED until observed.
4. User-created operational Job source cannot be forced into SHA/GUID registry by technical convenience.
5. Unavailable related Task proposal cannot be claimed cross-Task PASS; REAL code/host acceptance separate.
6. Existing Critic remains public-artifact-only; no new Reviewer agent or sign-off database.

## Preliminary guided review
Existing Reviewer and goal-review already check overengineering. Extend them, do not add a second review engine. Native independent Reviewer PASS remains UNVERIFIED. This is temporary dogfood evidence to remove from release HEAD only after actual verification.
