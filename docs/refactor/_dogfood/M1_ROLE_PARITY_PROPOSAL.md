# M1 — Code Structure Proposal and review: role mirror drift

Status: PROPOSED / PRE-CODE — no product role files changed at proposal creation
Decision authority: Bootstrap Unified Functional-First Detailed Plan v7.0 (M1 source-fit baseline, full Decision fidelity, no Worker installer redesign).
Defect: LL-001 in temporary Lessons Learned, existing `tests/test_installer.py` failures at main@ea5f70f.
This is a narrow repair to existing role packaging rather than adding a new role/file manager.

## Requirement and current verified source

At least these invariants already exist in `tests/test_installer.py`:
1. `test_portable_agent_contracts_remain_identical_to_canonical`: for Full-tier roles, `.generic/agents/<role>.md` must be byte-identical to `.agents/roles/<role>.md`.
2. `test_role_adapter_instructions_match_generic_contract`: canonical Planner/Advisor/Reviewer/Critic text must be included in matching Codex TOML developer_instructions, Claude Markdown agent body and Continue YAML rules.

**Actual CI failures**: main run 40107221591, job 120911309191, Python 3.9 Linux, shows `coder` generic copy missing `## Defect repair contract`, and `planner` role absent from Codex adapter's embedded full canonical text. This may also affect other role copies; inspect and reconcile all tested copies before writing.

## Task M1-CI-01 — repair existing role parity

### Source files planned
- REUSE_AS_IS `project-template/.agents/roles/coder.md` and `project-template/.agents/roles/planner.md` — canonical normative role behavior (no change to their requirements).
- MODIFY `project-template/.generic/agents/coder.md` — synchronize EXACT contents with canonical Coder; no extra contract invented.
- MODIFY `project-template/.generic/agents/planner.md` IF comparison confirms mismatch — synchronize exact contents with canonical Planner.
- MODIFY `project-template/.codex/agents/planner.toml` — preserve valid TOML metadata and append/insert missing canonical Planner section into existing `developer_instructions`, retaining any host-specific wrapper.
- MODIFY `project-template/.claude/agents/planner.md` and `project-template/.continue/agents/planner/config.yaml` ONLY IF canonical containment comparison proves they are missing text; preserve native format.
- For any other role/adapter from the existing tested set, MODIFY only on confirmed mismatch, no speculative mass rewrite.
- KEEP `install.py`, `TIER_MANIFEST.json`, `harness/common/branch_authority.py`, `harness/common/task.py` and approved Criteria unchanged.
- KEEP `tests/test_installer.py` existing assertions unchanged; no weakening to get CI green.

### Algorithm / caller relations

Canonical role file → existing installer packages canonical portable `.agents/roles/*` and host copies under `.generic/.codex/.claude/.continue` → runtime host loads its corresponding config → native role text must convey the same complete product rules. Test `test_installer.py` detects mismatches. This repair synchronizes existing distribution only; **no new loader, mirroring daemon, registry, installation tier or version policy**.

### Verification

- Test before fix: existing CI shows two concrete failing tests, six OS/Python matrix jobs. Do not claim local reproduction: present chat has only remote GitHub access and no bootstrapped checkout.
- Existing `python tests/test_installer.py`: previously failing tests should become PASS on refactor branch in GitHub Actions.
- Verify all six matrix jobs proceed past `test_installer.py`, and later regressions are actually executed.
- Track any newly revealed failures as separate evidence/lesson, not the same defect.
- Independent Reviewer/Tester host execution: unavailable here unless actual external Reviewer is run; this initial static/manual design review is **GUIDED_ONLY**, not authenticated approval.

## Reviewer pre-code check (guided manual review, NOT independent/native PASS)

- Plan/Criteria fidelity: restoring canonical text is required by pre-existing tests; does not add a new process to user-facing operation.
- Disproportionate complexity: introducing a global role synchronizer or installer refactor to fix one missing section is oversized; explicitly exclude it.
- Interface/format: keep TOML/YAML valid and native keys, full section copied exactly.
- Blast radius: only mismatched role mirror files changed, no source capability registry/permissions/config modification.
- Verdict: APPROPRIATE NARROW REPAIR FOR EXISTING TEST CONTRACT, but **independent Reviewer execution UNVERIFIED**. Human authority to perform this refactor arises from requested functional dogfooding; do not describe this note as a reviewer receipt or a formally autonomous gate.

## Next actions

1. Compare all role mirrors used by existing tests with canonical; choose exact subset.
2. Make scoped changes on `refactor/functional-dogfood-v7`, never main.
3. Let push-triggered GitHub Actions run fresh CI; record actual matrix findings.
4. On PASS, keep repaired role mirrors and unchanged parity tests; remove THIS temporary proposal and Lessons Learned from shipped tree.

## Post-implementation Tester evidence (append-only M1 result)

- **Actual source commit:** Planner mirrors `ea935b41e08eae2786ab169be236fdcb5713a8e9`; Coder mirrors `e82de5308f330ba0c86681608b1e1e36e0439529`.
- **Scope:** 14 existing host adapter role mirrors changed; canonical role files, installer, Criteria and Tier Manifest unchanged.
- **Automated Tester result:** [Actions run 40108684465](https://github.com/thebimhouseinfo-sudo/bootstrap/actions/runs/40108684465): **6/6 OS/Python jobs SUCCESS**, formerly failing role-parity tests now PASS and remaining suites completed.
- **Honest limitation:** SCRIPT_TESTED only. No native host loading/authenticated Reviewer or local Git common-dir branch-authority `check-write` was executed for this remote GitHub-connector change.
- **Disposition:** Keep the code and existing test coverage; delete this PRE-CODE working proposal from shipped tree after normal independent review/acceptance.
