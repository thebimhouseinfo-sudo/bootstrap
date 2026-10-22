---
name: Bootstrap Criteria pre-write checkpoint
alwaysApply: true
description: Prevent premature Criteria edits and keep independent Advisor consultation at the decision-stage boundary.
---

Bootstrap requires **Planner → Human request to write → Technical Advisor advice → NEW Human decision → apply exact Criteria**.

**First-time (no approved Criteria):** Planner drafts the entire Criteria IN CHAT. During brainstorm and draft iterations, do NOT invoke Advisor and do NOT write `docs/CRITERIA.md`. When Human asks to save/finalize the displayed draft, STOP before writing, stage the exact resulting file in `harness/criteria-proposal.md`, consult Technical Advisor using the available separate advisor configuration, explain the advice, then await a NEW Human confirmation.

**Existing Criteria:** agree on a before/after feature delta IN CHAT. Only after Human explicitly asks to update Criteria do the pre-write consultation with the current Criteria and settled delta. Again obtain a NEW Human decision after advice. Never treat the earlier instruction to save as post-advice authorization.

**Continue CLI:** `.continue/settings.json` invokes `.continue/hooks/criteria-gate.cjs` for recognized native CLI events. The tool hook blocks identifiable direct writes even during staged bootstrap. If a genuine independent `SubagentStop` for `technical-advisor` and later `UserPromptSubmit` cannot be observed, the one-shot apply must stay blocked; **do not forge events or receipts**. Agents do not invent a host hook capability.

**Continue IDE extension:** a Continue CLI settings hook is NOT an IDE tool hook. Continue IDE has not been verified to dispatch the CLI hook events; turn off direct write tools or require manual review where necessary, and label Criteria enforcement `GUIDED_ONLY`. For all environments the native hook isn't an OS-level immutable file lock; independent Human identity and alternate shell/MCP paths remain unresolved.
