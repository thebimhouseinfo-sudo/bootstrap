# Decision, journal and approval contract (runtime-specific implementation required)

This file is a **specification**, not an operational approval system.

- Journal user messages via trusted hook/tool with redaction; append-only, hash chained and excluded from Git.
- Decision entries must quote an exact substring of a journal message. Product theory changes appear only in CRITERIA.
- Request: ID, type, summary, before/after, scope/content hash, source, implications, risks, state PENDING.
- Exactly three user choices: AGREE / DISAGREE / OTHER (note mandatory). No expiration.
- AGREE authorizes only matching unchanged request/scope; DISAGREE closes without action; OTHER supersedes and creates revised request without authorization.
- A chat 'ok' is NOT approval. Agents may request but may not answer for a user.
- A verified UI or human-only command channel is required; if agent can impersonate user, mark GUIDED_ONLY.
- Pending approval defaults to BLOCKED. Altered request hashes invalidate authorization.
- Protected files: journal, decisions, approvals, request history and theory-update pathway.
- Implement rejection tests: fabricated quote, agent answering own request, changed request after approval, repeated rejected request, missing OTHER note.
- Do not claim cryptographic or permission guarantees without actual enforcement tests.

## Request types

| Type | Replaces |
|---|---|
| THEORY_CHANGE | change to `docs/CRITERIA.md` after Advisor's outcome/complexity/impact analysis and user's informed decision |
| THEORY_GAP | choosing an option where theory is silent; batch several gaps into one request |
| COVERAGE_MAP | approval of GOALMAP (goal to theory-ID coverage) |
| MILESTONE_SET / MILESTONE_ACCEPT | approving milestones and triggers / accepting a finished milestone |
| PUSH, BRANCH_ACTION | one-time push for exact remote, ref and commit set / merge, cleanup, new branch |
| HARNESS_PATCH | the bootstrap plan itself, protected-config changes, tier upgrades |
| BREAK_GLASS | one-time unlock for exactly one BLOCK; never changes config |
| DEP_ADD, MODEL_CHOICE | adding a dependency, choosing a model |

## Theory decisions and Advisor

Before first approval of CRITERIA or a THEORY_CHANGE, request Technical Advisor's concise, mandatory three-way comparison **Tạm dùng / Ổn / Nâng cao** for every evaluated requirement. Each option must specify the actual subsystem/components, safe scope, limits, engineering/maintenance complexity, costs/risks and downstream theory IDs/goals/tasks/tests affected. Separate the user's analogy from the actual capability wanted. Recommend the minimum sufficient scope, not the most sophisticated option. Human remains free to select any option, override advice or revise the request; selection of a design level is distinct from the final AGREE / DISAGREE / OTHER theory-change approval. Advisor cannot edit APPROVED theory or sign requests. This is a decision-stage trigger, not an always-running review loop; until a real protected approval mechanism exists, the advisory handoff is GUIDED_ONLY.

## Answer channel (choose at intake, in order of preference)

1. Real buttons in the target tool's UI.
2. A command only the human types, e.g. `harness answer REQ-0012 agree|disagree|other --note "..."`.
3. A generated `inbox.html` whose buttons copy the command.

If no channel exists the state is `AWAITING_USER`. Never substitute chat "ok".

## Runtimes without hooks (e.g. a chat UI driving tools over MCP)

The machine cannot capture the user's messages, so the journal and the "quote must be a substring of the journal" check are `GUIDED_ONLY`: an agent that relays the user's words could fabricate both sides. Record this in `ENFORCEMENT.md`. Mitigation: the user pastes the decision text into the request, or answers through a real UI channel.
