# One project, several coding harnesses

Bootstrap shares Criteria, plans, tasks, skills and Python helpers while installing each selected host's native adapter separately. A model selected inside a host does not change the harness. One primary host owns staged activation; each secondary host still needs its own real-host verification.

## Install together

From the Bootstrap checkout, preview a project outside that checkout:

```sh
python3 install.py --target /path/to/project --tier Standard \
  --runtime codex --runtime continue --runtime copilot --staged
```

After review, repeat with `--apply`. Copilot is optional. The first runtime is primary; retain it first when extending or upgrading the installation. The installer deduplicates shared files and preserves existing user-modified files as conflicts. Inspect conflicts before continuing.

For an existing, unlocked setup, repeat the original primary plus the additional runtimes to preview an extension. To update unchanged manifest-owned files, use the explicit `--upgrade` path after review. Activated setups require separately reviewed maintenance for protected hooks/scripts; do not use `--staged` to reopen them or delete lock evidence. Existing locks created before multi-adapter hashing need reviewed re-verification, rather than silently accepting a changed hash set.

The lifecycle hashes the install manifest and all installed native hook adapters, including Continue Stop. This detects configuration drift; it does not prove that secondary hosts load the hooks. Keep the exact host version, surface, allow/deny observations and limitations in the handoff report for **each** installed host. A primary READY is not a native PASS for all selected hosts.

## Lead → Worker: the recommended delegated execution path

**Lead is the primary project Bootstrap flow** and may implement its own work without delegating. A Worker exists only for an assignment from an existing Lead. Both use the same Bootstrap; the difference is **entry workflow and Criteria scope**, not model, installation tier, role set or a separate installer.

1. Lead completes project Bootstrap, develops the concrete Technical Proposal and obtains independent **Critic PRE_CODE_TECHNICAL PASS**.
2. In the recommended flow, **the approved Technical Proposal is the Worker's sole Criteria**. The Lead may give a repository path, branch/revision, write permissions and source references as operational access information, never as another Criteria or an expanded assignment.
3. Worker explicitly enters `.agents/skills/worker-execution/SKILL.md`, skips project Bootstrap and duplicate Pre-Code, reads only relevant source/context, implements the approved proposal, tests and sends evidence to Lead.
4. Material design/scope gaps return to Lead for revised proposal and Critic CR; ordinary bug repair and testing remain Worker responsibilities. Lead integrates changes and manages project-wide decisions.
5. Multiple hosts do not share chat history automatically; native agent dispatch or write guards are unverified until observed on the actual host. A Git worktree is Git isolation, not a security sandbox.

**Model choice:** Do not presume ~27B local models can lead whole projects. If an actual local model is capable of Lead responsibility, use normal Lead and let it do the implementation too. Worker is never an independent bootstrap alternative.

## Codex Planner → Continue with a local model → review

1. Codex Planner settles approved `docs/CRITERIA.md`, technical direction, `docs/IMPLEMENTATION_PLAN.md` with GOALMAP, and milestones. Human approval precedes task creation/coding. Each task needs concrete behavior, files or interfaces to change, dependencies, non-goals, actual checks and completion evidence.
2. Write the approved task to `TASKS.md` and configure the one `harness/active-task.json` with its goal ID, Criteria IDs and test/evidence links. The next host reads these files; it cannot assume access to another host's chat history. Preserve explicit branch authority.
3. Configure the actual provider and model in the **selected** Continue config. For CLI, select `.continue/agents/coder/config.yaml` explicitly with the supported `cn --config` option; for IDE, select/configure the intended assistant through its UI. `models: []` is a placeholder, and filling `.continue/config.yaml` does not fill every role config. Use the exact installed local model tag, actual endpoint and verified tool support; never invent credentials or silently switch to a cloud model. See the official Continue config reference and test the installed version.
4. Continue Coder reads the approved documents and active task, implements only that task, executes real checks and records results. It returns missing requirements or Criteria/plan changes to Planner rather than authorizing them itself. Continue role YAML files do not automatically launch isolated subagents.
5. Codex/Tester/Reviewer checks the resulting diff and evidence, runs the relevant checks and updates task status. Until native Stop behavior is observed, run `python harness/common/task.py` and `python harness/common/verify.py` directly for an active task. Empty checks or missing evidence are NOT_CONFIGURED, not PASS.

Suggested Continue handoff:

> Act as Coder using the configured local model. Read AGENTS.md, PROJECT_PROFILE, approved CRITERIA, IMPLEMENTATION_PLAN and the active task. Implement only that task, preserve unrelated changes, run configured checks and record actual evidence. Return scope gaps to Planner. Do not alter Criteria, invent approval or claim an unexecuted test passed.

## State and concurrency

Use one writer at a time in the same checkout: the current shared `active-task.json` represents one task. Multiple installed harnesses do not imply simultaneous independent coding sessions. Concurrent coders require separate worktrees/tasks and an explicit integration policy.

Copilot and Continue use `criteria-guard.copilot.json` and `criteria-guard.continue.json` under `harness/`; both remain ignored even in tracked mode. Receipts are scoped to runtime and the observed session. The proposal and Criteria are shared, so keep one Criteria transaction active at a time. A changed proposal or Criteria hash invalidates outstanding confirmation. Old unscoped receipts are ignored after upgrade and require a fresh confirmation flow.

Continue CLI hooks do not establish interception in the IDE extension. Continue can also load `.claude/settings.json`; when installing Claude alongside it, verify which hooks execute and avoid cross-host duplicate behavior. Local files are procedural state, not authenticated Human identity or an OS security boundary.

References: https://docs.continue.dev/reference ; https://docs.continue.dev/cli/configuration ; host-specific `.continue/HOOKS_SETUP.md` and `.github/COPILOT_SETUP.md`.
