# Bootstrap revision work plan (temporary)

Purpose: implement the user-agreed first-install and handoff workflow, preserving established behavior until actual runtime tests are complete.

## Scope
1. Keep only root README.md; move English guide to docs/user-guide.en.md and the AI instructions to docs/FOR_AI.md. Root README provides three links (Vietnamese, English, For AI). Include distinct new/existing-project prompts and next-session Planner kickoff.
2. Separate product requirements in docs/CRITERIA.md from implementation GOALMAP in a new docs/IMPLEMENTATION_PLAN.md. Each plan item starts with an outcome GOAL, traces to CRITERIA, carries implementation, acceptance, tests; Planner creates milestones after approval. Align role/skill/spec references. Do not silently rewrite approved criteria.
3. Add optional staged first-install path and setup lifecycle. Keep old install behavior compatible. Staged preflight protects against first-session hook self-block, and setup final activation is explicit after actual test evidence. Add audit, smoke, fresh-session instructions and recovery guidance. Never claim attested approval or native enforcement from local scripts.
4. Add project-specific stack/dialect skills and testing configuration instructions, technical-direction checkpoint, new/existing project criteria intake, and final handoff to Planner.
5. Add automated Python regressions for staged setup, readiness, docs links and plan trace. Run six-platform GitHub CI, reconcile failures.
6. Remove this temporary work-plan directory completely at end; do not leave process artifacts.

## Safety and change constraints
- No product source or user project edits; operate in bootstrap repo only.
- No automatic harmful Git operations; keep prior local/tracked semantics.
- Existing hook behavior without explicit staged mode remains unchanged.
- Hook/native acceptance must be verified separately using a fresh actual host session. Tab performing setup remains open until pass and handoff.
- No fake signatures, autonomous trusted approvals or universal hook enforcement.
- On failure, report exact limitations; do not silently loosen guard checks.

## Verification
- Existing six OS/Python matrix passes.
- Staged hooks allow legitimate setup work even with missing branch config; READY hooks retain branch check.
- No stale CRITERIA/GOALMAP references in canonical guidance.
- Only one root README; all three doc links work; English AI-only guide.
- Newly generated docs and scripts installed at correct tier, smoke testing safely in isolated paths.
- Temp planning folder deleted before completion.
