# B2 — Profile-aware installation: source-backed Technical Proposal

**Status:** PRE-CODE DESIGN / CR FINDINGS RESOLVED IN DOCUMENT; host-native enforcement UNVERIFIED.
**Authority:** Accepted Bootstrap plan §8.10; B1 installer/host-fit source survey. Bootstrap is standalone, not GSA. Scope B2 only.

## Goal and invariant

Make **Lead/Worker execution responsibility** selectable without conflating it with installer **Lite/Standard/Full** tiers, changing the primary host, or inventing an executor. Existing installs and updates must remain safe. Critic `PRE_CODE_TECHNICAL` is the last proposal review, never another Reviewer approval.

## Concrete existing call path

`install.py:main` parses `--tier`, repeatable `--runtime`, `--target-app`, `--staged`, `--upgrade`, and manages setup-state lock. `role_names(tier)` reads `TIER_MANIFEST.json`; `entries(tier,runtime)` and `multi_entries` determine copying; `plan_multi` and `classify` preserve target edits; a manifest records ownership. Existing selected primary runtime is immutable during staged setup. `.generic` is a staging adapter, not proof of native host support.

## Options examined in critical design review

- **Reject:** Replace Lite/Standard/Full with Lead/Worker tiers. It changes tier semantics and breaks compatibility.
- **Reject:** Create a Worker installer, orchestrator, queue, identity registry, runtime daemon, or global hook abstraction. No demonstrated missing function requiring these.
- **Reject:** Automatically downgrade/strip Planner/Advisor/Critic from installed Worker role files. Install packaging and *per-task delegated authority* are different concepts; role absence can break independent review.
- **Reject:** Claim that a copied generic file or local Git worktree enforces host permissions.
- **Prefer:** Reuse the installed role/skill set; express Lead/Worker **execution scope per delegated task**, via existing Task/Plan/role instructions. No additional installer CLI profile is needed **unless a real host-specific workflow demonstrates an otherwise unmet installation requirement**.

## Reviewed minimal B2 design — REUSE first

| Proposed action | File/function/caller | Acceptance |
| --- | --- | --- |
| REUSE_AS_IS | `install.py` `main`, `role_names`, `eligible`, `entries`, `multi_entries`, `plan_multi`, `classify` | All existing tier/runtime/staged/upgrade pathways remain unchanged |
| REUSE_AS_IS | `project-template/harness/specs/TIER_MANIFEST.json` | No new tier, role removal or renamed tier |
| REUSE_AS_IS | Existing `.agents/roles`, Pre-Code Critic skill and `harness/specs/REVIEW_LOOP.md` | Authority comes from reviewed Task context and host permissions, not installer labels |
| REUSE_AS_IS | `.generic/ADAPTER_REQUIREMENTS.md`, `HOST_NATIVE_LAYOUT.md` | Selected real host/version must verify native discovery and interception before claims of enforcement |
| DEFER TO B3 | Worktree, task-scoped handoff/context selection and delegated write boundary | Evaluate actual user task and host mechanics; distinguish guided procedure from enforced guard |
| NO CREATE | A universal `--profile lead/worker` flag, `PROFILE_MANIFEST`, dedicated Worker installer, cross-platform dispatcher | No verified consumer requiring any of them |
| TEST WHEN ACTUAL HOST SELECTED | Installed role discovery, allowed vs denied write, non-destructive `--upgrade`, staged lock, user-modified local settings | Host-specific observation, never inferred from static package tests |

## Explicit limitation and review outcome

The approved **objective** is role-aware execution. B1 source inspection does not prove that this requires *installation-time* profile selection. Since the existing tier installer already installs appropriate role definitions, an unconditional `--profile` switch is an unjustified implementation. Critic's source-grounded objections resolve by choosing **no B2 installer source changes** until there is evidence of a missing native setup capability. This is a scoped **design PASS for the minimal no-op installer choice**, not a claim of a real native Critic agent call or native host success.

For actual Lead-to-Worker delegation, continue to **B3** with a concrete task packet, role-scoped context, source ownership and one observed supported host. A concrete B3 contract can then identify whether any B2 installation delta is truly needed. B4 model comparisons and B5 host-wide regression remain separate.

**No Criteria changes; no B2 source files generated.**
