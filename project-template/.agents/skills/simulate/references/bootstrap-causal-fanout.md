# Bootstrap addendum — user-triggered causal fan-out and fidelity

**Owner:** The existing Tester role. **Method:** This is a focused reference supplement to the unchanged user-provided `simulate` skill. No new Simulation Contract, Job, Manager, agent or lifecycle is created.

## Boundaries that refine the original methodology
- Use the original `SKILL.md` and its five source references verbatim. Preserve **Designer blind to code → freeze scenario design → Tracer reads source/executes**. Its T0–T6 tiers and expected-outcome source discipline are authoritative.
- "Freeze" means the observed approved expected `design` cannot be edited to fit current code. Existing Tester test-case/evidence storage suffices when it preserves the original version; **a separate `simulate/FROZEN.md` registry is not mandatory**, nor is a fixed quota of 30–60 scenarios for a small Task.
- The mock AutoCAD reference includes *illustrative* Undo/sysvar/timeout expectations. Treat them as tests **only when supported by approved User/host contract**. Do not assert automatic job-level rollback, instant CAD crash recovery, app-controlled COM timeout, or always one-step undo by default.
- Actual execution fidelity is explicit: DESIGN_ONLY / STATIC_TRACE / MOCK_EXECUTED / INSTRUMENTED / REAL_HOST_EXECUTED. Never infer a real AutoCAD PASS from Python fake host; missing host availability remains UNVERIFIED. Do not run destructive simulated chaos against actual customer DWGs by default.

## Single User Action → every spawned child flow
Tracer records every observable branch caused by ONE public user event; mere tests of two unrelated clients are insufficient to detect accidental duplicate internal dispatch.

| Observation | Minimum description |
| --- | --- |
| Root input | Which user command/UI click/public API was actually activated; expected user result and Criteria source |
| Spawn | Each child flow origin, causal parent, action that triggered it; **why two flows exist** rather than assuming concurrency is legitimate |
| Authority | Flow owner, which Project/Job/Task/drawing it can touch, writable path or host capability needed |
| Resource ownership | Existing CAD command capability, mutex/lease/queue, shared UI save/commit stream; exclusive CAD actions must serialize through the **existing** owner |
| Wait-for | Which flow awaits a lock, callback, host result or parent/other flow; draw a compact wait-for graph |
| External events | Real/mock response, reordered or duplicated acknowledgment, disconnect, ESC/cancel, drawing tab switch |
| Effects | CAD objects/variables and file writes **actually observed**, unknown pending effects, artifact persistence/save evidence |
| Terminal states | Every spawned child reached DONE/FAIL/CANCELED or remains WAITING/UNKNOWN; parent user request must not claim DONE while a required child is stranded |

**Example:**
~~~text
User: "Run Create EQM Block"  [one user input]
  → public router dispatches request Q
      ├── Flow A owns the exclusive CAD command lease and writes drawing
      └── Flow B unexpectedly starts another CAD command and waits on A
  → Flow A returns; Flow B never resumes; parent waits forever

Tester does NOT merely mark a timeout. It identifies the unintended spawn,
the resource owner and missed handoff/settlement, and checks that the next
ordinary User command is still possible.
~~~
Never propose a second CAD dispatcher solely because its absence is measurable. Reviewer determines whether the smallest correction is fixing the duplicate launch, callback/ownership or an existing queue contract.

## Session/project continuity as a user-behavior simulation

When testing an AI-led application or harness, include a **risk-scoped context-boundary scenario** if the User workflow depends on the active project: after a long active-project conversation/handoff, supply a short ambiguous message through the normal chat entrypoint. The oracle comes from the User's current active project/Task and explicit project-switch rules, not from the source code. Expected: preserve the current Project/branch/Task when naturally applicable, or ask one concise clarification if genuinely uncertain; **never silently import an unrelated project's content and call it the active Task**. Trace which accepted session scope/context references were actually read and whether a source-of-truth retrieval was missed. Model/ChatGPT behavior outside the installed Bootstrap agent cannot be claimed fixed by this skill's text; native execution remains UNVERIFIED until exercised.

## Tester execution and closure
Start with a simple genuine user T0 entrypoint, then risk-proportionate realistic sequence, overlapping action, and disorderly user behavior from the original scenario generator. Control seeds and interleaving order where possible; archive expected versus actual and trace under the **existing Test Task**. When a defect is found, hand one evidence set to existing `bug-fix-loop`; run **at most 3** independent full Coder-fix/Tester-retest cycles for the same defect. After unresolved third FAIL, use existing advanced `systematic-debugging`, causal timeline/wait-for and hypothesis experiments before further architecture-changing repair. No fake Reviewer receipt.

**No generic host mock requirement:** For native add-ins that are harder to stub than to test, use a safe real test drawing and authorized host action, or leave test/manual verification PENDING with proper fidelity. Preserve native Error/ESC behavior and data recoverability as the actual host/User contract specifies.
