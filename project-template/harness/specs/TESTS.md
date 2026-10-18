# Bootstrap self-test checklist (run on a disposable copy with fake data)

Each test needs one violating case that is correctly blocked and one legitimate case that is not blocked by mistake. A test that cannot be run is `UNVERIFIED`, never "passed". Run only the tiers you built.

## Lite
1. Snapshot restores the files.
2. Stop hook blocks on verify FAIL, releases on PASS, stops and reports after 3 blocks.
3. Journal stores the exact message; a fake secret is redacted; the agent cannot write to the journal.
4. Chat "ok" does not unlock an approval-gated action; the three-button request shows in the inbox; an agent-run `harness answer` is blocked (or recorded `GUIDED_ONLY`).
5. Editing CRITERIA outside `theory-update` is blocked.

## Standard (add)
6. Unapproved milestone gives `NOT_CONFIGURED` and no fake review; an approved trigger picks the next role without the user asking.
7. A blocking finding goes back to the coder, then verify/test/gate, then review again; out-of-scope goes to BACKLOG; over the round limit stops and reports.
8. A source edit expires only dependent gates; an agent cannot sign a user gate.
9. Changing a theory ID marks exactly its goals/milestones/tasks/tests STALE; unrelated items stay current.
10. A quote absent from the journal makes `decision add` fail; a conflicting entry without `supersedes` fails.
11. Request rules: DISAGREE cancels and the identical request is not resent; OTHER without a note is rejected, with a note it supersedes; an old pending request still blocks; changing content after approval voids the approval.
12. Missing model gives `BLOCKED/NEEDS_USER_CHOICE`, never a silent fallback; two sample projects of different stacks do not leak profiles.

## Full (add)
13. G13: task without goal blocked; in-scope ID without task/test reported; OPEN blocks dependants; silent theory gives `THEORY_GAP` instead of invention.
14. G14: operating scenarios run on a fake product; unresolved `THEORY_GAP` prevents PASS.
15. Git: unintegrated commit keeps G12 not PASS for the right scope; integrated commit recognized; unknown branch never auto-merged or deleted; no Git gives `NOT_APPLICABLE`; raw push blocked; `git-admin push` works only with an AGREE'd PUSH request and G12 PASS.
16. Fixer: every BLOCK prints code/rule/location/unlock; doctor catches seeded faults (wrong hook path, wrong schema version, two rules demanding opposites); T0 fix comes with a regression test and CHANGELOG; T1 is never auto-applied; weakening detector blocks loosening; "approved push still blocked" is diagnosed correctly; at most 2 attempts; failed protective test or selftest rolls back.
