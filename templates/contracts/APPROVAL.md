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
