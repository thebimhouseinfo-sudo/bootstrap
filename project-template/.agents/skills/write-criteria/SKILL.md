---
name: write-criteria
description: Planner uses this to draft or amend the single human-readable product theory in docs/CRITERIA.md.
---

# write-criteria — human-readable product theory

## Purpose
`docs/CRITERIA.md` is the **single source of truth about the product humans want**, not a code specification, implementation plan, architecture diagram or agent execution log. A Human should understand what is being made, who uses it, why, the expected behaviors and accepted limits without needing software-engineering knowledge.

## Required writing approach
1. Write in clear, natural language centered on the user's real problem: what the product is, who it serves, what it is for, user journeys, observable behavior, important constraints, exclusions and success criteria.
2. Express requirements as outcomes and examples understandable to a non-developer. Stable identifiers can be used for traceability but never dominate readability.
3. Document desired behavior separately from current observed behavior. Label unresolved product decisions OPEN and unverified feasibility UNVERIFIED. Never assert a promise just because it was suggested.
4. Include necessary product-level boundaries (e.g. 'works offline', 'never edits files without approval') when Human has chosen them; omit algorithms, libraries, classes, API endpoints, file tree, task breakdown, test commands, milestones, rollout plan, and architecture alternatives unless a specific technical constraint is itself a Human-approved product requirement.
5. Use `challenge-feasibility` before proposing an unverified technical dependency as a committed capability. Treat research evidence as support for the discussion, not as a reason to turn CRITERIA into a technical research paper.
6. For an existing product, reconstruct observed CURRENT behavior from evidence but only the Human sets DESIRED behavior. Follow existing Advisor and Human approval gates before any protected CRITERIA update; do not create a competing theory file.

## Helpful outline (adapt to product; don't fill with boilerplate)
- What we are building and why
- Who will use it and in what circumstances
- What users must be able to do and how it should behave
- What is explicitly outside scope
- Constraints, tradeoffs, assumptions and unresolved decisions
- Plain-language examples of successful use

## Quality check
Could a non-technical stakeholder read this alone and explain what the product should do? Can technical implementers later derive a Plan without smuggling new product decisions into it? If either answer is no, revise.
