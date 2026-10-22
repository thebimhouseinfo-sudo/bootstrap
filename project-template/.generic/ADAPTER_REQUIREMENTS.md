# Generic host adapter requirements — build for the actual coding client

**Mandatory for the setup agent, not for the Human to code.** Bootstrap deliberately does **not** ship a guessed adapter for every IDE/CLI. `--runtime generic --target-app CLIENT` copies portable contracts; **the installation workflow must then research, implement, register, and test the actual CLIENT-native integration**, within verified host capabilities. Copying files is phase 1, **not** completion. Applicable to OpenCode, Claude/Command Code variants, Qwen Code, Copilot, and any actual DeepSeek-based client; identify the *client and its harness*, not merely the model name.

## Inputs and evidence (before writing native files)

1. Identify exact host/client, harness mode, version, OS, execution model (local/cloud), and supported workspace hooks/subagents/skills/tool permissions. Capture official documentation or actual inspected schema/tool output and its version. Do not transplant `.codex/hooks.json` into other clients.
2. Read the selected tier's `harness/specs/TIER_MANIFEST.json`, `harness/specs/HOOKS.md`, `harness/specs/GATES.md`, `harness/specs/APPROVAL.md`, `harness/specs/ENFORCEMENT.md`, `harness/specs/READINESS.md`, and the canonical roles and skills. These specify *intended outcomes*, not proof that every future gate already exists.
3. Map each demanded capability to a **documented host-native event or API**. Classify: SUPPORTED / UNVERIFIED / UNSUPPORTED, with specific evidence. If critical interception cannot be proven, do not claim that requirement is enforceable.
4. Obtain Human approval for necessary host permissions and any potentially intrusive registration or shell script. No silent changes to organization settings or weakening of host security.

## Implement: native files, not more generic prose

- **Role and skill discovery:** place/configure Planner, Technical Advisor, Coder, Tester and other tier agents and shared `.agents/skills` using the documented host mechanism. Verify a real agent session can invoke them. A language model selected inside another host does not change which host's hooks are active.
- **Session/start or equivalent:** load succinct project instructions, configured task/status, and available capability limits if host supports an entry event.
- **Before write/tool use:** when the host provides interception, implement a native pre-tool script or adapter that uses real event input/output schema, runs applicable existing `harness/common/` checks, and denies supported unsafe operations *before mutation*. Map actual write tools (file edit, patch, terminal, MCP) individually; do not pretend an intercepted tool implies universal write coverage. Handle path normalization, workspace escape, bypass routes and error behavior conservatively.
- **Protected Criteria:** Planner must present an exact proposed draft/delta, obtain Technical Advisor advice on that proposal, and only edit after Human's **subsequent** decision. A prompt or agent-writable receipt is not trusted proof of Human authorization. If the host cannot supply an independently verifiable approval path, leave this part `GUIDED_ONLY`; do not silently invent signed gates. A host script may deny protected writes absent authorization if all relevant paths are intercepted, but then Human needs a real, reviewed unlock process.
- **After work / Stop or equivalent:** if supported, run configured `harness/common/verify.py` and task trace checks with a bounded retry; do not claim review agents or milestone signing are automatic without actual orchestration. For platforms without a Stop event, implement the closest **actually supported** command/CI/pre-commit path and label it GUIDED_ONLY where agent can bypass it.
- Reuse common Python helpers when appropriate; if Python or a hook facility is absent, implement an equivalent supported script/tool **with evidence**, not a made-up API. Do not modify portable role theory or weaken safety rules merely to achieve a green indicator.

## Verify against this acceptance matrix in a disposable project

| Capability | Positive check | Negative check |
|---|---|---|
| Native role discovery | invoke Planner and Advisor in real host | absent/misnamed role is reported, not simulated |
| Hook registration | observe actual event invocation | absent/disabled/untrusted hook is not called PASS |
| Tool preflight | safe edit proceeds | unsafe edit is blocked **before file change** on each claimed write route |
| Protected Criteria | exact Advisor/Human sequence respected | model-initiated protected edit without authorization denied **where claimed enforced** |
| Branch / scope | approved target accepted | frozen branch, traversal and unsupported route handled conservatively |
| Verification / Stop | successful configured command observed | failed command reported; no unbounded retry or fabricated approval |
| Recovery | legitimate Human can resume/edit via documented path | agent cannot silently self-authorize an exception where claimed guarded |

Test native registration, tool input/output, actual allow/deny outcomes, workspace file integrity, and the configured release phase. Record host name/version, native adapter file paths, hook events, observed test logs and exclusions. CI that only exercises Python scripts proves `SCRIPT_TESTED`, not `RUNTIME_VERIFIED` or `ENFORCED`.

## Completion and limitations

**Mandatory installation effort:** after staged install the agent must attempt the supported native port and host testing instead of declaring that `generic` is permanently guidance-only. Do not ask the Human to implement it manually.

- **Supported and tested:** record the actual native files and evidence. Use `setup_lifecycle.py host-test`; activation may reflect tested native hooks *only* if complete, specific observations are recorded. Human-controlled activate/finalize confirmation remains separate; this local record is not cryptographic authorization.
- **Partly supported:** install and test the feasible subset, list each unsupported capability and its effect. Mark uncovered boundaries `GUIDED_ONLY / UNVERIFIED` and do not claim the full required harness is ready. Escalate any must-have gap before regular coding.
- **Unsupported:** provide exact technical evidence, stop claiming native completion, and propose a manual alternative; do not spend cycles fabricating adapters.

The generic adapter is generated **per target project/host during setup**. It should not become a new universal platform-specific template in Bootstrap unless intentionally promoted and independently maintained.
