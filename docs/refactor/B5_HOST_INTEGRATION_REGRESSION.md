# B5 — Host integration regression and release evidence

**Status:** SOURCE-AUDITED / SCRIPT-TESTED where CI reports success; **real target host acceptance is pending**. This document is a verification plan and evidence ledger, not an invented live host test or extra design approval gate.

## Contract

Bootstrap **Lead** is the main project entry. A **Worker** exists only after Lead delegates an independently Critic-CR-PASS Technical Proposal; **that proposal alone is Worker Criteria**. Worker skips project bootstrap and duplicate Pre-Code CR. Lead may code directly. Existing Lite/Standard/Full tiers and primary staged host remain unchanged.

## Current source observations

- `install.py` handles the selected primary runtime plus optional additional runtimes, staged state, manifest-owned upgrade, and conflict preservation; it does not create or call native agents autonomously.
- `harness/MULTI_HARNESS.md` states that host sessions do not share history and secondary hosts need their **own** registration/hook verification. Worktrees isolate Git revisions, **not** write permissions.
- `.continue/HOOKS_SETUP.md` distinguishes Continue `cn` CLI hook support from Continue IDE extension, whose write interception remains unverified.
- `.github/COPILOT_SETUP.md` describes VS Code Copilot session-target, native agent and node-hook requirements; naming a Claude/Codex model inside Copilot does not activate a different harness.
- `harness/specs/READINESS.md` separates generic ready-to-install instructions from actual native `RUNTIME_VERIFIED` and `ENFORCED` capability status.
- GitHub CI passing proves source packaging/static and script tests **only**.

## Regression matrix for each actually available host

| Check | Positive observation | Negative observation | Without live host |
| --- | --- | --- | --- |
| Install and upgrade | Existing target content preserved; manifest-owned unchanged files upgrade cleanly | user-modified/native config not silently overwritten; locked staged setup not reopened | SCRIPT_TESTED only |
| Role and skill discovery | Lead entry and canonical Worker skill actually available | absent/misconfigured skill is not reported available | UNVERIFIED |
| Project bootstrap | Lead performs Criteria/Plan/Pre-Code CR when appropriate | Worker does not run initial bootstrap on delegated approved assignment | GUIDED_ONLY until live test |
| Worker Criteria fidelity | Worker uses **only** CR-PASS Technical Proposal as Criteria | task packet/logistics do not become another Criteria; no invented approval | GUIDED_ONLY until live test |
| Host hook invocation | precise host/version, event and stdout/exit evidence | no claiming registration from merely existing config files | UNVERIFIED |
| Write authority | allowed edits succeed and protected edits are denied before mutation on claimed routes | terminal/MCP bypass separately checked; worktree alone not enforcement | UNVERIFIED |
| Integration/handoff | Lead receives diff, relevant tests, missing gaps and source ref | no implicit chat-state transfer or double modification in same checkout | UNVERIFIED |
| B4 optional local path | actual local model/quantization/hardware/tool support logged, accepted output measured | inability to finish not concealed by raw token speed | NOT_RUN |
| Cloud quota exhaustion/local continuation | a real continued delegated task reaches accepted completion | no assumption of magically synchronized conversations | NOT_RUN |

## Supported surfaces to verify (do not generalize across variants)

1. **Codex CLI/App/Cloud:** exact native host surface/version, role/skill discovery, real hook events and observed branch/write outcomes. Cloud may lack independent Human-terminal sessions.
2. **Claude Code:** test actual project native agents/skills/settings; shipped files are not proof of runtime invocation.
3. **Continue CLI `cn`:** host reads `.continue/settings.json`; assert actual CLI `PreToolUse`/Stop event and deny/allow. **Continue IDE extension** separately remains GUIDED_ONLY without proven equivalent interception.
4. **VS Code Copilot:** verify Copilot session target, `.github/agents`, `.github/hooks/criteria.json`, Node.js availability and actual interception.
5. **Antigravity:** record concrete host version and actual hook/role loading. Do not import Codex/Copilot assumptions.
6. **Generic/OpenCode/Qwen Code:** `.generic` alone is staging. Adapt and verify the *selected version's* native files and APIs before asserting loaded/active behavior.

## Evidence format (one entry per host and scenario)

Host / version / OS:
Project source revision and Bootstrap revision:
Selected runtime and installed native adapter paths:
Lead entry / Worker entry:
CR-PASS proposal reference (Worker's sole Criteria):
Task, test and attempted negative route:
Observed log / command / exit code / before-after effect:
Verdict: PASS / FAIL / UNVERIFIED / NOT_RUN
Limitations and follow-up:

Record a real failed scenario exactly and repair only the proven cause; normal bounded repair and independent Tester verification remain applicable. Do not add a second approval process.

## B5 completion boundary

**Already supportable from repository:** static contract regression, installer script CI, documented integration limitations and test plan. **Not supportable from this GitHub-only session:** assertion that local Qwen/Continue/Copilot IDE runtime, project-specific permissions, local 27B hardware, cross-host continuation or native hooks have actually passed.

When a real supported host and authorized workspace become available, execute the matrix and update this ledger. There is **no need to solicit a new Human technical-design approval**; only actual connection/host access or consequential permission decisions constitute a Human gate.
