# HANDOFF — Bootstrap Functional Refactor — Technical Proposal RL checkpoint
**Saved:** 2026-10-25 (Asia/Ho_Chi_Minh)
**Repository:** https://github.com/thebimhouseinfo-sudo/bootstrap
**Working branch:** `refactor/functional-dogfood-v7`
**Draft PR:** https://github.com/thebimhouseinfo-sudo/bootstrap/pull/21
**Source baseline:** `main@ea5f70f8bc051a036496158a4e33a2bfe6f99725`
**Last verified functional head before this docs-only checkpoint:** `2c119a1bd7ec8898a9a581486d3654850c68b92c`
**CHECKPOINT PURPOSE:** Preserve the **current Project / Phase / Task authority** across chats. This is temporary dogfood evidence, NOT new Criteria, a new approved Plan, a new Job, a new execution gate, or proof of Reviewer PASS.

## 1. Human instructions — highest-priority scope boundary
1. **Project is BOOTSTRAP, NOT GSA, CadGPT or KE Math.** It is deliberate that Bootstrap has NOT been configured as a GSA-managed project. The Human wants to **dogfood Bootstrap's own harness template within this repository** to assess, test and improve Bootstrap.
2. **Function first.** Do NOT redesign `install.py`, installation tiers, local-to-Worker setup, new local hooks, multi-model/profile architecture or Worktree provisioning in the current iteration. The deferred B1–B5 scope stays in the one Plan; not canceled, just later after functional stabilization.
3. **Phase of work:** Continue **Technical Proposal / Detailed Plan review and repair (RL)**. The current canonical file is explicitly DRAFT, not independent Reviewer PASS or Human authorization for implementation. Review the proposed files, functions, callers, dependencies, test design and unnecessary abstractions. Coder changes occur only after this approval boundary, not because a tool happens to permit writes.
4. **Use actual harness state and source, not model memory, to select project/phase/Task.** Verify available role/skill, task/branch state and authoritative Decision/Plan before actions. The template copy under `project-template/` is NOT automatically a configured active-root project or proof of native harness execution.
5. **Finding log:** use temporary `docs/refactor/_dogfood/LESSONS_LEARNED.md`. Record observed symptom, reproducer/evidence, observed vs expected, confidence in root cause, minimal repair and real Tester retest. On ship **delete the entire `docs/refactor/_dogfood/` directory from release HEAD**, but keep verified source fixes, regression tests and necessary accepted product docs. Do not claim Git history erasure.
6. **Criteria remains unchanged.** No spontaneous Advisor activation, no new review gates/services/registries. No merge/deploy without independent review and authorized release decision.

## 2. Canonical files and read order (DO NOT confuse the two)
1. **Canonical DRAFT Upgrade/Detailed Technical Plan:**
   `docs/refactor/CONTEXT_OPTIMIZATION_REFACTOR_PLAN_DRAFT.md` on main; v7.0 Functional-First Detail Plan. In particular read §0, §6A–§6I, §7 (deferred), §8.1–§8.12, §9 and its acceptance/Decision coverage. The document's top status remains **DRAFT — awaiting Planner/Reviewer review and Human approval**.
2. **Actual Bootstrap harness template:**
   `project-template/AGENTS.md`, `project-template/.agents/roles/{planner,coder,reviewer,tester}.md`, relevant `project-template/.agents/skills/*/SKILL.md`, `project-template/harness/specs/{REVIEW_LOOP,READINESS,TRACE}.md`, `project-template/harness/common/{task,branch_authority}.py`, `project-template/harness/active-task.json`, `project-template/TASKS.md`, `project-template/docs/{IMPLEMENTATION_PLAN,MILESTONES}.md`. **Confirm real configured root/host state before claiming enforcement**.
3. **Existing task-level proposals / WIP review evidence:**
   `docs/refactor/_dogfood/M1_ROLE_PARITY_PROPOSAL.md` through `M6_SIMULATION_PROPOSAL.md` and `LESSONS_LEARNED.md` on this branch. These are **temporary and GUIDED_ONLY** proposals, not independently approved Technical Design.
4. **Implementation diff under review:** Draft PR #21 vs main. Review source paths and callers in the actual diff, rather than treating script CI as approval. Note that proposals and code were created before adequate RL approval; that process violation must be recorded and reconciled, not silently legitimized.

## 3. Verified repository status at save time
- Branch before this checkpoint: `2c119a1bd7ec8898a9a581486d3654850c68b92c`; `main` unchanged at `ea5f70f8bc051a036496158a4e33a2bfe6f99725`.
- PR #21 **OPEN / DRAFT / NOT MERGED**.
- Two GitHub Actions suites for `2c119a1bd7ec8898a9a581486d3654850c68b92c` both **SUCCESS**, 6/6 OS/Python matrix jobs each:
  - PR: https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40157929479
  - push: https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40157926610
- CI proves only **SCRIPT_TESTED installer/role parity and existing regressions**. It does NOT prove actual native Reviewer acceptance, connected GSA Job/Run retirement, real AutoCAD host outcomes, or successful real-agent conversation behaviour. New docs-only checkpoint commit needs its own check on readback.
- No code in `install.py` or new Local Worker installer was intentionally changed in Draft PR. Verify actual diff again before any approval.

## 4. What is already in Draft PR #21 (WIP, NOT approved milestones)
- **M1**: repaired canonical role copy drift in host adapter files and confirmed installer CI parity. LL-001.
- **M2**: added optional Secretary `record-decisions`, decision-preserving Planner skill/role and Plan template changes. Real interactive decision-recording remains UNVERIFIED.
- **M3**: changed `trace-impact` procedure to whole changed-Phase/Plan unfinished RETIRED and taught `task.py` to reject `RETIRED` Task selection. This is NOT a verified safe actual GSA Run/Job settlement engine; do not build a competing runtime.
- **M4**: Coder Pre-Code proposal, focused clarification and on-demand knowledge distinguishing DEV source, User OPERATION artifact (including CadGPT User-generated CODE Jobs/Lisp and Word DOCX / AutoCAD DWG) and app/host-managed support/recovery BAK/DWL/DWL2.
- **M5**: Reviewer whole-related-Task proposal review, unnecessary-system challenge, practical manual alternatives.
- **M6**: original user-provided Claude `simulate.skill` main SKILL + five references imported **byte-identical** (previous exact UTF-8/checksum checks); separate `bootstrap-causal-fanout.md` addendum, Tester role integration, bounded 3-cycle repair escalation. No Simulation Job Pack.
- **M7**: independent comprehensive E2E real-agent/harness/host regression and functional stable acceptance are **NOT COMPLETE**. Technical Proposal RL is the immediate work; M7 cannot be declared PASS from CI alone.

## 5. Open findings and exact mistakes to avoid
- **LL-001**: role mirror drift, fixed/script-tested; actual host loading separate.
- **LL-002**: harness documented no autonomous Planner/Reviewer/Critic orchestration engine; GitHub remote connector writes do not execute local hook/branch authority; **GUIDED_ONLY**, not native gate PASS.
- **LL-003**: Bootstrap source repo was not verified as a configured installed Bootstrap target; template placeholders are not the live project state. Use supported isolated dogfood workspace if installation is necessary; **do not change installer just to dogfood**.
- **LL-004**: test assertion/oracle checked guessed wording rather than normative skill text, fixed on CI; prefer contract-derived behavioural criteria and Tester replay.
- **LL-005**: short ambiguous user message caused inappropriate switch to unrelated KE Math; real host/root cause UNVERIFIED. Tester scenario must preserve current Project/branch/Task.
- **LL-006** (new): assistant drifted from **Technical Proposal RL** into source edits, and then twice confused Bootstrap with other projects. Preserve WIP as Draft, stop extra implementation, resume source-grounded RL.

## 6. IMMEDIATE NEXT ACTION IN THE NEW CHAT
**READ-ONLY FIRST**:
1. Fetch this handoff, canonical v7.0 DRAFT Plan (from main), task-level M1–M6 proposals, current PR #21 diff, existing actual harness template and Lessons Learned. Verify branch/commit/current CI; no memory-based phase assumption.
2. Enter **Bootstrap Technical Proposal RL**: Planner/Reviewer examine actual file/function/caller/dependency/test design across M1–M7 and challenge duplicate mechanics, fake GSA assumptions, installer work outside scope, unapproved source version policies and overly broad gates. Produce concrete `CHANGES_REQUIRED` findings; update only the Technical Proposal / associated review text, re-review to PASS, and accurately record independent vs GUIDED_ONLY status. Do NOT self-certify independent Reviewer PASS.
3. Confirm with Human when the reviewed DRAFT Plan is ready for their decision under the already accepted review flow. **Do NOT reactivate code changes, merge or deploy based solely on previous CI.**
4. After correct review/authorization, proceed functional milestones against **Bootstrap's own harness template** and verified host execution, collecting findings. Installer / Local Worker B1–B5 LAST.
5. At actual ship release, ensure `docs/refactor/_dogfood/` is deleted from release HEAD after useful fixes/tests are integrated and existing release controls pass.

## 7. Explicit STOP conditions
- A tool response or memory mentioning **GSA** does NOT make it the active project. User explicitly chose Bootstrap's own harness, not GSA.
- A reference to CAD/Word/KE Math is an **example**, not project switch.
- A green CI or a historical WIP commit is NOT independent Reviewer approval or a handoff from RL to implementation.
- Current installer source and its architecture are OUT OF SCOPE now; do not propose/install Lead/Worker changes until functional stability and later authorization.
- A statement that the model 'remembers' project scope does not replace reading this saved handoff and active source.
