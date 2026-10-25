---
name: record-decisions
description: Optional Secretary recording method used only in an explicitly active Discussion Job to preserve full Human-accepted decisions without changing Criteria.
---

# record-decisions — faithful Human decisions, not a new Job runtime

## Invocation and authority
- Explicit Human "open/create Discussion Job" → use this skill to open the existing project documentation context directly when permitted. **No extra question or invented approval**.
- A vague "we should discuss" → offer the optional Discussion Job **once**; refusal and ordinary questions continue as normal chat with no files created.
- A Discussion Job is **not** a new executable Job Pack, extra lifecycle/state, daemon, agent or Criteria approval gate. The Secretary is a recording **responsibility** of the existing lead/Planner while recording is active.
- If no writable, user-authorized project documentation context is available, explain the actual limitation and retain the complete proposed record in the current conversation as NOT_VERIFIED. Do not invent a GitHub path/commit or claim persistence.

## Procedure — at a genuine Human decision, not every message
1. Read the exact Human statement(s) and already accepted decisions in the active discussion, including corrections. **Only a Human-chosen outcome** can become ACCEPTED. Do not promote assistant proposals, speculative examples or unresolved decisions.
2. Record the **full chosen solution** in Human/domain language: outcome and WHY; ordered actions; input/output fields and exact example values; native host/environment; constraints and exceptions; risks; rejected alternatives and their rationale; open questions and affected Goals/Tasks. A topic-name summary is NOT a decision record.
3. Record provenance with a real available message/document link or accurate conversation source context. Do not invent URLs, message IDs, dates or Human signatures.
4. Use the project's established file naming/storage convention. If none exists and the Human wants files, a readable local example is docs/discussions/<discussion-topic>/INDEX.md plus a distinct decision document (e.g. DEC-001.md). Those labels are references, **not a universal SHA/GUID-based file registry or required product identity**.
5. Index current ACCEPTED, SUPERSEDED and UNRESOLVED records. For a material correction keep the prior decision readable and link its successor; do not overwrite accepted history or treat earlier rejected options as new active instructions. Human's latest accepted choice governs only the specifically replaced scope.
6. Write through existing authorized documentation tools and **read back** the written file(s) before claiming they are saved. Failed or uncertain writes are NOT_VERIFIED, with a complete recoverable proposed text; never fabricate persistence or auto-retry unsafe mutations.
7. Hand Planner links to the **complete active decision documents**, plus relevant supersession history. Planner may then plan. Recording alone never changes approved CRITERIA, Plan, Tasks, Git branch, code or publication state.

## Minimum decision record (illustrative, not a new database schema)
- Title and status: ACCEPTED / SUPERSEDED / UNRESOLVED (only Human-approved instructions are ACCEPTED)
- Discussion context, applicable feature/Goal and actual Human provenance
- **Decision in full:** exact ordered professional/operational mechanism, inputs and outputs
- Reason/benefit; verified host/domain constraints; examples with unchanged values
- Exceptions, accepted risks and exclusions; explicitly rejected solutions and why
- Unresolved facts, if any, never silently completed
- Supersedes / superseded by when appropriate; links to affected work
- Write/readback evidence or NOT_VERIFIED

## Negative checks and handoff
A normal chat must not spawn a Discussion Job or files. A refusal does not block Planner. No mandatory SHA, GUID, immutable user-file version, new Agent/Job/registry, re-bootstrap, Technical Advisor gate or permanent checklist. Do not identify the file's programming-language extension as authority to classify its lifecycle. The file is a user-directed documentation artifact; use native project/host management. Reviewer should detect missing full decisions, overwritten history and false saved state. Testers may run scenario examples, but skill text alone is GUIDED_ONLY until real-host execution is observed.
