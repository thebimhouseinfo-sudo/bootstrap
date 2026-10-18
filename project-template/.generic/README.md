# Generic coding-agent adapter source (PORT REQUIRED)

This folder is a **copy-and-adapt starter**, not a native registered extension for any IDE. It saves setup quota by shipping the **same full agent role contracts** found in `.agents/roles/` as standalone `.generic/agents/<role>.md` files. The installer filters roles according to Lite / Standard / Full.

Use this only when your actual coding host does not have a ready runtime package. **Codex and Antigravity generic templates are already copy-ready; Claude Code is preconfigured but host-untested; Continue is nearly ready with model/provider selection.** Do not regenerate their contracts merely for compatibility.

For a new host:
1. Read `PORTING.md` and the relevant `platforms/*.md` guide.
2. Reuse only installed role files (`.generic/agents/`) and shared procedures (`.agents/skills/`, `harness/common/`). Do not hallucinate native syntax.
3. Inspect the host's official role/skill/hook discovery, configuration schema, permissions, model/provider, and authorization. Convert native adapter files **only**, preserve role mandates and Human gates.
4. Verify positive AND negative smoke cases inside the actual host; mark `UNVERIFIED` or `GUIDED_ONLY` where unsupported.
5. Configure project-specific facts separately: CRITERIA, actual code/SDK, commands/tests, active Git branch, approved task and secrets only via host-approved secret storage.

Do not copy `.generic/agents/*.md` into a guessed native directory automatically. They are portable source text until a host-specific installation is explicitly validated. Human approval is required for runtime permission changes.

Use `python install.py --ask-first` to print ONE set of setup questions for the AI to ask in chat; then `python install.py --target PATH --tier Standard --runtime generic --target-app cline` to preview. Apply only after approval.
