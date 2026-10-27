# B4 — Optional local model collaboration benchmark

**Stage:** experimental protocol, not evidence of model capability or an installation change.
**Dependency:** Lead exists and produces the same independent Critic CR-PASS Technical Proposal for all comparison paths; Worker uses that proposal as sole Criteria. No project bootstrap for Worker.

## Question, not assumption

Does adding a bounded local implementation Worker (~27B candidate) improve accepted end-to-end delivery over (A) a capable Lead coding directly? If it does not, do not adopt. **No hypothesis that 27B can act as a full-project Lead**; a model demonstrably capable of Lead may run Lead and self-implement instead of using Worker.

## Arms

- **A — Direct capable Lead:** Lead implements the exact approved proposal and completes tests.
- **B — Lead + local Worker (~27B):** Lead delegates the exact same proposal as Worker Criteria. Worker executes and tests; Lead integrates/verifies.
- **C — Optional local collaboration:** a ~27B model produces a constrained implementation skeleton *only after* approved Pre-Code CR, and smaller local model fills isolated modules; Lead performs integration and final verification. Compare only when actual configured versions/tool support are available. C is never mandatory.

Do not change proposal, acceptance tests, scope, or model-specific prompts to rescue a single arm. No hidden help to one arm. Fixes after first attempt count as rework.

## Real tasks and evidence

Choose representative real changes (small localized, multi-module interface, dependency/caller regression) whose project Criteria and approved proposal already exist. Use comparable clean worktrees and the same pinned source revision; worktrees isolate Git states, not filesystem permissions. Record model exact name/version/quantization, host version, hardware, context size, tool availability, prompt/context references, start/finish records, revisions, tests and any Human interventions. If hardware or native host is unavailable, mark **NOT_RUN**, not estimated PASS.

## Measurements per arm

| Metric | Definition |
| --- | --- |
| Accepted completion | The specified task passes all actual acceptance checks and is accepted by Lead; partial code is not complete |
| Human correction | Count substantive extra Human requests/decisions during implementation |
| Rework | Count defect/fix/retest cycles and rejected integrations |
| End-to-end time | Lead assignment/review through final accepted integration, including handoffs, tests, and corrections |
| Compute/cost | Actual compute usage, cloud expense and local energy/host occupancy when measurable; mark missing |
| Correctness | Failing tests, regressions, unsupported interface assumptions, unauthorized scope edits |
| Context efficiency | Measured source/instruction context passed to each agent, not inferred from file count alone |

Preserve raw outcomes, including failures or abandons. Prefer repeatable tasks and multiple trials rather than one anecdote. Compare paired outcomes and report variability; if local arm wins speed but loses correctness/rework, it is **not** a proven productivity improvement.

## Decision and non-goals

A model/strategy is recommended only upon verified improvement in **accepted** full delivery and acceptable correctness, integration effort and stability on actual tasks. Otherwise retain capable Lead direct path. Do not set a model default, mandate multi-model installation, invent automatic dispatch, add context service or claim native hook enforcement under B4. B5 host regressions remain separately required for host-specific claims.

## Critical design examination

- **Selection bias:** use same approved proposals/source/test scope across arms.
- **Task contamination:** distinct worktrees and fresh sessions as supported, no copying solved code from competing arm.
- **Hidden transfer costs:** count Lead integration, extra approvals and context packaging.
- **Unverified 27B ability:** explicitly measure instead of presuming full-project leadership or even successful bounded tasks.
- **Skill/runtime limits:** actual Worker execution is guidance unless native dispatch proven; measure what was actually run.
- **Failure criterion:** any unsupported backend, missing test or inability to reproduce leaves that arm UNVERIFIED/NOT_RUN, not negative capability proof.

**Result now: PROTOCOL ONLY — no real experiment has been run in this milestone.**
