# Bootstrap self-dogfood — temporary Lessons Learned

**Scope:** Refactor Functional Core M1–M7, using the current Bootstrap roles/skills/harness in this same project.
**Branch:** `refactor/functional-dogfood-v7`. **Source baseline:** `main@ea5f70f8bc051a036496158a4e33a2bfe6f99725`.
**Working document only:** NOT a new Criteria, Job Pack, gate, role, source-of-truth or permanent shipped lesson catalog.
**Shipment rule (Human):** Fix each confirmed issue in the existing product mechanism, preserve a regression test/source fix, and **remove `docs/refactor/_dogfood/` from the shipped tree once the functional release is accepted**. Git commit history may still show earlier files; ordinary deletion does not erase that history. Do not remove prior to real verification or automatically delete active evidence.

## LL-001 — Canonical role instructions drift from host-specific copies

- **Status:** FIXED / SCRIPT_TESTED on current branch; independently run native host role loading and Reviewer receipt are UNVERIFIED.
- **Date / Milestone:** 2026-10-24, M1 baseline.
- **Evidence:** [GitHub Actions run 40107221591](https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40107221591), Linux Python 3.9 Job 120911309191, `python tests/test_installer.py`. Six matrix jobs on Ubuntu, macOS, Windows, Python 3.9 and 3.12 fail at the installer role parity test and skip following tests.
- **Actual failing tests:** `test_portable_agent_contracts_remain_identical_to_canonical` and `test_role_adapter_instructions_match_generic_contract`.
- **Reproduction trace:** The first test compares `.generic/agents/<role>.md` byte-for-byte against `.agents/roles/<role>.md` and fails at `coder`. `.generic/agents/coder.md` lacks `## Defect repair contract` present in the canonical Coder role. The second test requires the full canonical role text inside host-adapter instructions and fails at `planner`; the canonical Planner role has the new `## Milestone placement of verification and bug-fix loop` section missing from at least the Codex planner adapter.
- **Root cause (source supported):** Duplicated role instruction files were updated inconsistently. This is **distribution/context drift**, not evidence of incorrect Coder/Planner requirements.
- **Repair boundary:** Reconcile actual host adapters with canonical role source **without** adding a new central loader, changing installer tiers or weakening the equality/containment tests. Preserve valid host-specific wrapper/config syntax. Do not replace unrelated adapter-specific instructions.
- **Observed fix:** Existing canonical Planner and Coder role instructions were synchronized to **14 existing host mirror files** (Generic, Codex, Claude, Continue configs + rules, Copilot, Antigravity) in commits `ea935b41e08eae2786ab169be236fdcb5713a8e9` and `e82de5308f330ba0c86681608b1e1e36e0439529`. No installer/Criteria/role canonical changes. Full GitHub Actions [run 40108684465](https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40108684465) on code commit `e82de5308` passed **6/6 matrix jobs** (Ubuntu, macOS, Windows × Python 3.9 and 3.12), including `test_installer.py` and all downstream suites. This is SCRIPT_TESTED, not proof that native IDE/CLI agents loaded role text.
- **Expected continuing evidence:** Native selected-host instruction loading and independent Reviewer sign-off when available. If later test fails, reopen the same defect instead of duplicating Jobs.
- **Earlier detection:** Existing equality and containment tests already detect drift; CI gate failed. Pre-release review must not call the product stable when those tests fail; consider a minimal canonical-sync check in existing edit workflow if actual repeated failures justify it.
- **Severity:** Functional packaging blocker (M1 baseline).
- **Repeat count:** At least current six-job matrix; this is ONE defect across environments, not six unrelated bugs.
- **Disposition:** Existing parity tests are retained as the safeguard; no new synchronization daemon required. **Remove this temporary lesson from release HEAD when ship requirements are met**, not before. The tested code fixes and tests remain shipped.

## LL-002 — Harness execution mode is not automatic in this self-hosted GitHub session

- **Status:** CONFIRMED CAPABILITY LIMIT / GUIDED_ONLY; no product defect inferred yet.
- **Evidence:** `project-template/harness/specs/REVIEW_LOOP.md` explicitly says no autonomous Planner/Reviewer/Critic orchestration engine. `project-template/harness/specs/BRANCH_AUTHORITY.md` stores authority in the local Git common directory and explicitly says hosted MCP/GitHub writes are not intercepted. Current chat's GitHub connector can inspect and edit remote branches but does not expose an authenticated Bootstrap native role/hook execution event.
- **Implication:** We can use the actual Planner/Coder/Tester/Reviewer instruction contracts and obtain real GitHub Actions Tester evidence; **do not claim local `branch_authority.py check-write`, human approval authentication or automated Reviewer PASS occurred**. GitHub branch isolation and permissions are the effective remote boundary during this exercise. Future local host test needs a genuinely installed harness/checkout.
- **Next step:** Apply relevant existing role/skill instructions manually and report it as GUIDED_ONLY. Keep code changes in `refactor/functional-dogfood-v7` and do not merge until actual evidence/review permits it.
- **Disposition:** If a later host provides native verified execution, update product evidence; no new approval daemon for this exercise.

## LL-003 — Unverified canonical Criteria bootstrap for the Bootstrap repository itself

- **Status:** SOURCE-FIT LIMIT; NOT an automatic new Criteria approval request.
- **Evidence:** Current root repository has `docs/refactor/CONTEXT_OPTIMIZATION_REFACTOR_PLAN_DRAFT.md` but no verified installed root `docs/CRITERIA.md` / root `harness/active-task.json`; corresponding files under `project-template/` are **template placeholders** and cannot be presented as active approved Bootstrap project state.
- **Consequence:** Calling `project-template/harness/common/task.py` without installing/configuring to a real project would validate placeholder scope or return NOT_CONFIGURED, **not prove dogfood delivery readiness**.
- **Remedy:** Use existing accepted conversation decisions and the single detailed Plan as scope references for a **scoped functional M1 audit**, and require a real installed-host/approved-target setup before claiming formal automated harness readiness. Do not silently manufacture approved Criteria or turn this into a new Technical Advisor gate.
- **Disposition:** Preserve a simple regression/installation fixture when justified; remove temporary audit note at ship.

## Working practice

For each new finding, add symptom, exact entrypoint/test/host/revision, observed versus expected, root cause PROVEN or UNVERIFIED, smallest repair, independent Tester retest, and the existing check to prevent recurrence. Do **not** create a separate issue for every retry or give the finding a permanent User Job lifecycle.

**Functional phase is NOT shipped while material open findings remain unresolved.** At ship: keep useful source fixes/tests/docs, explicitly delete the `_dogfood` working directory from release HEAD, and verify deletion. Do not promise historical commit erasure.

## Verification snapshot — M1 role parity dogfood

- **PRE-FIX** `main@ea5f70f` → GitHub Actions `40107221591`: 6/6 matrix jobs FAIL at installer tests (2 canonical role parity failures); later tests skipped.
- **POST-FIX** `refactor/functional-dogfood-v7@e82de5308` → GitHub Actions `40108684465`: **6/6 matrix jobs SUCCESS**, downstream regression suites executed.
- **Role behavior evidence:** Coder role and Planner role canonical text now present in existing host mirror files; native agent discovery/hooks not re-tested here.
- **Reviewer acceptance:** Manual design assessment only (GUIDED_ONLY). Formal independent Reviewer PASS and merge remain outstanding.
- **Next scoped milestone:** Continue M1 evidence audit and subsequent M2 decision preservation. No Local Worker/installer refactor during functional M1–M7.

## LL-004 — Tester assertion drifted from the actual Coder skill contract

- **Status:** CONFIRMED TEST DEFECT; one minimal correction applied, CI retest pending.
- **Date / Scope:** 2026-10-24, M4 Coder knowledge packaging regression.
- **Evidence:** GitHub Actions [run 40114253849](https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40114253849), Ubuntu 3.12 job 120932164525, test_coder_precode_and_user_file_lifecycle_knowledge_are_packaged line 157. Same failure appears in six OS/Python jobs. New test asserted the exact non-existent fragment "materially missing".
- **Actual skill wording and root cause:** solution-clarification/SKILL.md correctly limits invocation to information that "materially changes the correct operational/domain solution"; this rule was present. Tester used a guessed shorthand phrase as a brittle string oracle rather than checking the source's meaningful requirement. No product symptom demonstrated.
- **Fix:** Update the test to assert the actual complete normative phrase, **not remove the check, weaken a runtime guard or change the user-approved skill**. Keep the same defect and first repair attempt.
- **Regression:** Re-run tests/test_installer.py and full six-OS/Python CI after this commit; native host skill activation remains UNVERIFIED regardless of script result.
- **Lesson:** Build static packaging assertions from the real contract and preserve semantic intent, not invented shorthand. For behavioral acceptance rely on real input-output simulation rather than text equality alone.
- **Ship:** Remove this temporary record after source/tests are verified and useful checks retained; do not conceal CI history.
