# <Project>

Follow the approved harness contract. Project-specific commands/profile below must be verified.

## Commands
- Verify: <verified command or UNVERIFIED>
- Build/test/run: <verified commands or UNVERIFIED>

## Sources and precedence
- Product theory: `docs/CRITERIA.md` only; GOALMAP is inside it.
- Derived: `docs/MILESTONES.md`, `TASKS.md`, tests and generated trace.
- Runtime constraints: `docs/PROJECT_PROFILE.md`.
- Ambiguous theory: report `THEORY_GAP`; do not invent behavior.

## Workflow
- Work on one scoped task linked to one approved goal.
- Snapshot before edits; verify and attach actual evidence afterward.
- Do not alter product theory, approval ledgers, generated state or protected harness settings by ordinary file edit.
- User approvals must use a verified approval channel. Chat agreement is not an approval token.
- No direct push or destructive Git action without the prescribed authorization.
- Critic is context-isolated; reviewer assesses only findings relevant to the current goal.
- A guard implemented only in these instructions is `GUIDED_ONLY`, not `ENFORCED`.

## Done
- Goal acceptance evidence exists; tests run on relevant target; limitations stated.
- No blocking findings or unresolved gates for the claimed scope.
