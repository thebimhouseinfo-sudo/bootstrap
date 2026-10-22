---
applyTo: "docs/CRITERIA.md"
description: "Bootstrap Criteria changes require the read-only Planner draft or delta, a Human write request, independent Technical Advisor advice, then a new Human decision"
---

# Before any edit to product Criteria

Do not modify `docs/CRITERIA.md` using ordinary edit, patch, file write, terminal redirection or MCP tools.

**Greenfield / unapproved placeholder:** Planner drafts the complete product Criteria in chat. Only after Human agrees it may be written should Technical Advisor be invoked, to advise before the write. After the advice, Human decides again.

**Brownfield / already approved Criteria:** Planner first agrees on a precise proposed addition/removal/update with Human and shows a before→after delta in chat. Only when Human requests an update is Advisor consulted on that exact delta. Human decides after advice.

The sole intended Copilot write path is the one-time `criteria-apply.cjs` command after native hooks observe an actual `technical-advisor` completion and a subsequent confirming Human prompt. Never fabricate these events. This file is guidance; inspect real hook dispatch and document write routes that remain unprotected.
