# B1 — Installer / Host Fit Technical Proposal (Pre-Code)

**Repository:** Bootstrap standalone harness
**Branch:** `design/b1-installer-host-fit`
**Status:** SOURCE-INSPECTED DESIGN CANDIDATE — Critic independent native dispatch not verified; do not mislabel this as native CR PASS.
**Scope:** B1 only: existing installer/host inventory, smallest sufficient Lead/Worker profile proposal, verification criteria. **No installer/source modification in B1.** B2–B5 remain separate later milestones.

## A. Verified present source facts

| Source | Observed current contract | Implication |
| --- | --- | --- |
| `install.py` lines 22–25; 364–377 | `TIERS=Lite/Standard/Full`, `RUNTIMES=antigravity/codex/claude/continue/copilot/generic`; `role_names(tier)` follows tier inheritance in JSON | Tier is an *installation feature set*, not Lead/Worker authority; do not rename or conflate them. |
| `project-template/harness/specs/TIER_MANIFEST.json` | Lite: coder/reviewer/advisor; Standard adds planner/tester/critic/explorer; Full adds harness-fixer | A Lead/Worker profile must not silently remove required tier roles or alter Lite capability promises. |
| `install.py` `eligible()`, `entries()`, `multi_entries()` | Existing runtime-specific filters, shared file de-duplication and conflicting-payload rejection; selected runtimes may be repeated | Reuse packaging. No second copied-file registry, secondary installer or speculative abstraction. |
| `install.py` `plan_multi()`, `classify()`, upgrade/manifest logic | File conflict detection; prior-manifest-owned and unmodified upgrade; existing custom content retained | Any future B2 profile distribution must preserve upgrade and non-destructive behavior. |
| `install.py` `main()` | Primary runtime owns staged setup; `--staged`, `--upgrade`, `--config-git`, explicit `--apply`; generic `--target-app` | Do not redesign primary owner, change activated lock, or automatically choose host. |
| `.generic/ADAPTER_REQUIREMENTS.md`, `HOST_NATIVE_LAYOUT.md` | Generic files are staging, not active host configuration. Exact client/version, supported API, native installation paths, event interception and safe negative tests are required. | A copied file / renamed folder cannot certify native hooks or Critic dispatch. |
| `project-template/harness/specs/REVIEW_LOOP.md` | No autonomous Planner/Reviewer/Critic orchestration; guided coordination is not host-enforced | B1 cannot promise unattended Lead↔Worker transfers from the current repo. |

**Evidence boundary:** The above is a source inspection of repository HEAD, not an execution trace of a local Qwen Code, Continue IDE, or Codex host. Exact live version, APIs and events are **UNVERIFIED** until host selection/inspection. Codex is the manifest's reference runtime, not a verified universal hook platform.

## B. Functional theory preserved

1. **Lead/Worker is an execution authority/profile boundary**, never a model-size rank or a Lite/Standard/Full tier replacement. A capable cloud agent may be a Worker; a local agent is not automatically a Worker.
2. Lead retains approved Goal/Task scope, input/output interfaces, dependencies, branch/source authority and coordination; Worker receives only delegated Task context and authorized paths. Worker Coder, Tester and Reviewer are task functions, not new mandatory models.
3. **Independent Pre-Code CR is Critic in `PRE_CODE_TECHNICAL` mode** with scoped private context. `PUBLIC_ARTIFACT` is a separate public-only assessment. No extra Reviewer/Human file-layout approval.
4. Bootstrap does **not** require GSA. External runtime integrations and user file-product lifecycle remain project-specific.
5. Actual worktree provides Git isolation, **not security sandboxing**; write tool interception is host-specific and must be verified before any claim of enforcement.
6. No new Job, manager, registry, sidecar, auto-generated identity or cross-platform hook daemon solely for B1.

## C. Candidate minimal design for subsequent B2/B3 (no code yet)

**B1-T01 REUSE_AS_IS:** `install.py`: `role_names(tier)`, `eligible`, `entries`, `multi_entries`, `plan_multi`, existing manifest and update/lock controls. Do not touch during B1.

**B1-T02 REUSE_AS_IS:** `project-template/harness/specs/TIER_MANIFEST.json` and approved docs. Preserve tier semantics. No profile keys in tier JSON unless B2 shows a real consumer and profile-vs-tier interface contract.

**B1-T03 FUTURE MODIFY only if source-backed B2 need:** Existing host-native setup guides/config for selected runtime; ideally express Lead/Worker instructions as scoped **role responsibilities in existing skills**, not another selection engine. Never auto-install untested native hooks.

**B1-T04 FUTURE B3 design boundary:** Lead gives one Task packet containing approved Goal/Criteria and relevant accepted Decisions, proposal/CR outcome, specific source read context, branch/path scope, expected output and acceptance. Worker returns modified files, commands, results, uncertainties and handoff. Do not implement a new packet schema/manager in B1; first dogfood an ordinary readable packet.

**B1-T05 HOST VALIDATION:** Select exact host/version only when actually available. Check primary host ownership, role/skill discovery, support for native agent invocation, before-write permission interception, native hook events, safe and blocked operation, recovery and coexistence with existing settings. When missing, mark GUIDED_ONLY/UNVERIFIED instead of pretending.

**B1-T06 MODEL MEASUREMENT:** B4-only optional ~27B skeleton experiment against direct capable coding, evaluated by *finished accepted result, rework, time and cost*; no automatic hybrid/default change now.

## D. Source change inventory

| Action | Path | Why |
| --- | --- | --- |
| CREATE (B1 documentation) | `docs/refactor/B1_INSTALLER_HOST_FIT_PROPOSAL.md` | Durable inspected proposal and review findings |
| REUSE_AS_IS | `install.py`, `project-template/harness/specs/TIER_MANIFEST.json` | Existing package/tier/upgrade mechanism sufficient for B1 study |
| REUSE_AS_IS | `project-template/.generic/ADAPTER_REQUIREMENTS.md`, `HOST_NATIVE_LAYOUT.md` | Host-specific verified migration already specified |
| REUSE_AS_IS | `project-template/harness/specs/REVIEW_LOOP.md` | Guided/native boundary already explicit |
| DEFER | All installer/model/worktree/host hooks/source files | B2–B5 after separate scoped CR and actual host facts |
| NO CREATE | Separate Lead/Worker runtime, approval database, universal hook driver | Disproportionate without demonstrated missing capability |

## E. Independent Critic Review checklist — source-grounded design critique

- **C1 Tier/profile collision:** PASS at design level: orthogonal profile instruction does not alter Lite/Standard/Full or package role eligibility.
- **C2 Incorrect native-host assumptions:** PASS at design level: no claim of real Qwen/Continue hook invocation; host facts pending actual invocation.
- **C3 Duplicate orchestration:** PASS at design level: no queue/state/installer service proposed.
- **C4 Existing upgrade/lock preservation:** PASS at design level: all existing source retained for B1; future B2 must test actual cases.
- **C5 Authority and sandbox confusion:** PASS at design level: scoped Git paths are not enforcement; actual write interception remains unverified.
- **C6 CR identity:** PASS at design level: independent technical Critic is final proposal review; Reviewer post-code remains distinct.
- **C7 Testability:** PASS at design level: package/script verification separated from host-native evidence and real-project effectiveness.

**Review limitation:** The above is a documented critical design assessment; no independent host Critic invocation/receipt has been observed here. It must not be represented as a separately executed native Critic or B2 authority. No actionable source change is nominated for **B1 itself**. Future B2/B3 technical proposals require their own file/caller evaluation when a concrete host/version and implementation scope are selected.

## F. B1 exit and next milestone

B1 **source inspection and proportionate proposal are complete**. External host-native facts are explicitly pending and belong to B2/B5 verification, not a reason to invent an installer implementation or more approval gates.

Proceed to B2 Pre-Code design only with an actual selected host and accepted activation scope. Keep `B1–B5` deferred source implementation until the relevant milestone is explicitly begun; no unrequested model/default installer refactor.
