# Codex READY: repository setup and complete Standard harness

Status: PROPOSED — scope requested by Human; this written design awaits review.
Date: 2026-10-18 (Asia/Bangkok).
Repository baseline: `853fd82` plus existing uncommitted Claude adapter changes.

## 1. Requested outcome

Human requested both outcomes after the local readiness audit:

1. Bootstrap itself is configured for practical Codex development, with one
   repeatable check command and real runtime evidence.
2. The reusable template implements its existing Standard contract: approvals,
   gates, trace/staleness, milestones and bounded review orchestration.

Implement mechanisms described by the existing contracts. Do not declare missing
features optional merely to obtain a green readiness result. Preserve existing
local work, the installer safety contract, role responsibilities and chosen models.

## 2. Observed baseline

- Template configuration exists under `project-template/`; the repository root
  has no AGENTS.md, .codex directory or installed harness.
- Local Python 3.14.5 checks: 29 passed, two symlink cases skipped. This is not
  confirmation of the CI Python 3.9/3.12 matrix or native runtime acceptance.
- Installed Codex CLI reports `0.163.0-alpha.10.2`.
- Python hook bridge covers SessionStart, recognized direct apply_patch and Stop.
- Snapshot, verify, branch-authority and limited one-task link validation exist.
- Full gates, authenticated approvals, complete trace and autonomous reviews are
  explicitly unimplemented. Native hook trust and agent loading are unverified.
- Current root branch is main; no branch-authority choice has been supplied for
  activating a root harness. Do not infer a new active/frozen branch policy.
- Existing dirty files include install.py, template AGENTS/CLAUDE/SETUP,
  Claude configuration, capabilities.json and a new harness/claude directory.

## 3. Readiness has separate claims

Use the following independent results in machine-readable and human reports:

| Result | Required evidence |
| --- | --- |
| TEMPLATE_TESTED | Required files, parsers, installer and relevant regression tests pass for the exact source hash |
| PROJECT_CONFIGURED | Real project profile/check commands, required configuration and explicit Git authority are valid |
| CODEX_RUNTIME_VERIFIED | Exact project hook definitions trusted; real lifecycle events and required role discovery observed on a named client/version |
| STANDARD_READY | All Standard mechanisms implemented and validated, configured human-only approval issuer, passing real task/milestone flow and positive/negative host tests |

The readiness command prints each result, missing evidence and the next required
action. It must not turn an unconfigured project into READY because a template
capability file says SCRIPT_TESTED. A project using manual coordination remains
usable, but cannot claim authenticated G0/G11 or STANDARD_READY.

Evidence binds project identity, runtime/version, source/configuration hashes,
session/run IDs, actual observations and timestamps. Relevant changes invalidate
the affected result. Raw runtime artifacts are observations, not unforgeable
signatures unless a trusted host actually attests them.

## 4. Root setup without installing product placeholders

Add root AGENTS.md, a documented check entry point, Python test configuration and
project-local Codex configuration appropriate for maintaining this repository.
Reference canonical template primitives rather than copying the whole template
into the bootstrap checkout or bypassing install.py's self-install prohibition.
The setup does not create fictional approved CRITERIA, goals or milestones.

Root checks run existing suites plus new Standard/readiness regressions, schema
validation and installed-fixture smoke tests. Each child command has a timeout,
an explicit working directory and a saved result. On Windows, set a writable
fixture TEMP explicitly. Never silently install dependencies or skip required
tests. Missing optional test support is reported distinctly from a passing test.

Place runtime-generated artifacts under an ignored state directory. Root setup
cannot certify its own trust or alter user/global Codex settings. Preparing root
configuration and activating hooks are separate operations: Git authority and
native trust must be settled before activating a guard that would deny all edits.

## 5. Shared Standard engine

Keep a Python 3.9+ common engine, callable by Codex and existing adapters. Avoid
a daemon, VM or second product requirements source. Modules have explicit duties:

| Module | Responsibility |
| --- | --- |
| state/storage | Strict schemas, safe paths, atomic writes, single-writer lock and bounded journal |
| trace | ID → goal → milestone → task → source/test/evidence graph and affected-node staleness |
| approval | Immutable requests, external attestation verification, replay rejection and decision history |
| gates | Required gates/profiles, target digest, verdict provenance, expiry and completion checks |
| workflow | Trigger selection, next action, bounded rounds, review findings and milestone progression |
| readiness | Source-bound script results, project configuration and real-host evidence |

Commands return 0 for satisfied checks, 1 for executed failures, and 2 for
unconfigured/invalid prerequisites; JSON output also carries the precise state.
No missing prerequisite is converted into a PASS or successful empty run.

Reject absolute/traversal/secret paths, symlinks and junctions escaping the project,
malformed or oversized inputs and corrupt state. Do not execute strings through
a shell. Version state explicitly; refuse unsupported versions without resetting
or deleting user data. Hold one writer lock across a complete transition and
recover interrupted writes without treating partial history as valid.

An editable local hash chain detects accidental corruption, not a malicious
agent rewriting the entire chain. Do not market it as tamper-proof. Security
decisions require verification against the external trust root described below.

## 6. Approvals and the actual trust boundary

The default remains MANUAL_COORDINATION for ordinary scoped work. Authenticated
mode requires a host/user-only issuer whose signing authority is unavailable to
the coding agent. A private key in another folder reachable by the same agent,
a local HTML button, or an agent-callable approve command does not qualify.

Implement a pluggable verification boundary with a pinned public issuer identity.
The first supported transport imports detached, externally signed response
receipts. Use an established verifier, with availability preflight and bounded
subprocess execution; do not invent cryptography. A concrete verifier/dependency
is selected in the implementation plan after checking the supported platforms.
No credential is generated, installed or copied into this repository automatically.

A request includes a random ID, project identity, type, exact scope and proposed
content digest, current target digest, requesting run, nonce and schema version.
The attested response binds those fields plus AGREE / DISAGREE / OTHER, issuer,
timestamp and an OTHER note when applicable. Preserve request and response bytes.

Reject invalid/untrusted signatures, wrong project/request/scope/target, changed
requests, duplicates/replay, malformed choices and OTHER without a note. OTHER
does not approve the original; create a revised request. Gate checks reverify the
receipt rather than trusting an editable cached `approved: true` field.

Trust-root enrollment/replacement is a human/host operation. If the agent can
replace the verifier or trusted public identity, the authenticated boundary is
not ENFORCED. Test that boundary on the actual host; otherwise report UNVERIFIED.
Without a configured issuer, human gates stay AWAITING_USER/NOT_CONFIGURED.

## 7. Gates, trace and milestone transitions

Implement the existing G0–G11 and G13 Standard catalog and its light/standard/heavy
profiles; Full-only G12/G14 remain outside this requested Standard completion.
Apply existing escalation and review rules. Do not remove gates to lower scope.

Compute target digests over the approved theory IDs and acceptance conditions,
goal/task definitions, selected code/test files, check configuration and relevant
policy/model/adapter versions. Hash evidence contents, not just evidence paths.
Missing/deleted artifacts invalidate their gates. A PASS applies only to the exact
target and supported evidence type. FAIL never advances a task or milestone.

G0/G11 require verified human receipts. G4 is generated by actual configured check
execution. Agent review/test gates require observed role-run results bound to the
same target; a role name or agent-supplied PASS is insufficient identity proof.
Clearly label script validation, review verdicts and host attestations separately.

Trace requires unique IDs, explicit approved membership, valid edges, no cycles
and real bounded project artifacts. Replace substring matching as proof of ID
membership. Keep CRITERIA as the requirements source; a machine-readable index
maps stable IDs/sections and hashes back to it rather than duplicating theory.
Generate TRACE.md from graph state. Changes propagate STALE only through affected
dependencies, while shared configuration changes invalidate all affected gates.

`status` identifies task/milestone, profile, gates and mandatory next step.
`check` succeeds only for all required current gates. `advance` is atomic and
rechecks the target under lock. At most one task is active; a milestone closes
only with current G11. No goal/milestone is invented when state is absent.

## 8. Codex review orchestration

Use the native Codex main agent and role tools, with engine-generated actions and
bounded receipts. A Python state machine alone is not autonomous orchestration.
Select the concrete supported integration after validating the installed host's
capabilities. Do not add a model/provider fallback or recursively launch an
unbounded Codex process from Stop.

Triggers include plan_ready, task_code_ready, task_verified, feature_complete,
milestone_complete and risk_escalated. Deduplicate by event, target, role and round.
Schedule only required roles/gates for the current profile; cap repair at two
rounds per blocker and stop for human input on exhaustion or unavailable tools.
Resume from persisted actions after interruption without duplicating successful
work or bypassing failed gates.

Advisor retains decision-stage feasibility consultation and no Plan/Code verdict.
Reviewer assesses approved scope and grounded findings. Critic receives only the
public artifact, not private CRITERIA/plans/reviews. Prompt restrictions alone do
not enforce confidentiality: use host-supported context/tool restrictions or an
explicit public-artifact-only workspace for Critic, and verify negative reads.
Inherited sandbox limitations remain visible in the readiness result.

## 9. Hooks and real-host verification

Retain explicit snapshot and bounded Stop behavior. Harden supported patch
parsing for update/delete/move and invalid paths, with positive and negative
regressions. Declare shell/MCP/hosted paths outside that hook's write boundary.

Do not bypass native hook trust. New/changed hook definitions are reviewed through
Codex /hooks. Smoke tooling prepares an isolated disposable project, exact test
instructions and a challenge ID. Collect actual Codex execution artifacts for:

- SessionStart from project root and nested cwd;
- direct apply_patch allowed and denied under explicit branch policy;
- pre-edit snapshot matching original bytes and safe hash-checked restoration;
- Stop success, failure, missing checks and bounded continuation;
- required agent discovery with unchanged model/effort assignments;
- reviewer/critic result flow and the declared context boundary;
- externally authenticated approval acceptance and forgery/replay rejection;
- complete Standard task and human-accepted milestone, followed by a target edit
  proving PASS invalidation and affected-graph STALE propagation.

Fixtures cannot certify native trust. If host access or human-only configuration
is unavailable, complete code and script tests, preserve the prepared smoke case,
and report precisely which readiness result is still UNVERIFIED.

## 10. Compatibility, recovery and validation

Keep installer dry-run, idempotence, conflict preservation and runtime/tier filters.
New common files must install for their required tiers; Lite must not accidentally
require Standard workflow state. Claude local changes are preserved, and shared
behavior changes receive adapter regression checks. Update capability claims,
README in both languages, setup docs and tests together after evidence exists.

Record a manifest of pre-existing changed files before implementation. Worktree
isolation, if used, must retain access to the intentional local Claude changes;
do not reset, overwrite, move or automatically commit them. Do not push or change
remote protection. Keep root configuration activation reversible. Snapshot only
explicit non-secret files; restoration needs acknowledged current hashes.

Required checks include allowed and rejected state transitions, signatures,
replay/scope mismatch, hash expiry, graph integrity, duplicate triggers, round
limits, missing roles/host, interrupted writes, concurrent transitions, corrupted
state, unsafe paths and unchanged legacy installer behavior. Run local checks on
the actual interpreter; CI covers its declared OS/Python matrix separately.

## 11. Review decision

This design is ready for Human review. Approval permits writing the detailed
implementation plan; it does not attest future gates, authenticate any receipt,
trust a native hook or choose an active/frozen Git branch.

External prerequisites will be surfaced as concrete setup actions after code and
smoke fixtures are prepared: human-only issuer enrollment, host trust, branch
selection and any actual permission boundary the host must enforce. Missing host
support must remain a visible limitation, never a fabricated STANDARD_READY.

## Official runtime references checked

- Hooks and exact-definition trust: https://learn.chatgpt.com/docs/hooks
- Project custom agents and inherited controls:
  https://learn.chatgpt.com/docs/agent-configuration/subagents
- Local CLI help: `codex --help`, `codex exec --help`, `codex debug --help`.
