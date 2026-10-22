# Host-native layout migration — mandatory for generic setup

The `.generic/` folder is a **temporary source/staging name** supplied by Bootstrap, **not an automatically loaded settings directory**. During setup, identify the actual coding host and **rename/move or translate its role, skill and hook files into the native paths that the host really discovers**. The outcome must be equivalent to renaming the generic *configuration* to the host-native name; a directory rename alone never converts file schemas.

## Required host selection and destination

Read the exact host's documentation and version first. Examples to verify against the running installation:

| Active coding host | Native project-local destination | Notes |
|---|---|---|
| OpenCode | `.opencode/agents/`, `.opencode/skills/`; project `opencode.json` | Register hooks/plugins via its **actual** extension API; do not invent `.opencode/hooks.json` |
| Qwen Code | `.qwen/agents/` | Find the documented settings/hooks/skills paths and file formats for that Qwen version |
| VS Code Copilot harness | **Packaged** `.github/agents/`, `.github/hooks/*.json`, `.github/copilot-instructions.md` | Installed automatically for `--target-app copilot`; verify native discovery and observed hook deny/ask |
| Claude Code harness | `.claude/agents/`, `.claude/skills/`, `.claude/settings.json` | Only when the selected runtime is Claude Code, not a Claude *model* inside Copilot |
| Unlisted IDE/CLI (including a client using DeepSeek) | **Discover and verify its native project settings location** | Do not infer a folder from the model or invent a `.<app>` convention |

## Migration contract for the installing agent

1. Keep `harness/`, `docs/`, `.agents/skills/` and the user's existing project files separate. Bootstrap's initial `.generic/` contains **reference files as well as draft agent definitions**; do not blindly rename the entire folder into `.opencode/`, `.qwen/`, or `.github/`, since those clients expect different schemas and layouts.
2. For *host-consumed* content, **move/rename the relevant `.generic/agents/*` to the verified native agents directory**, converting the frontmatter, name and permissions as necessary. Similarly place skills, hooks, startup config and settings in the documented native locations. This native destination becomes the **authoritative active configuration**. Do not keep a second independently edited active copy with divergent rules.
3. If a native destination already exists, inspect its contents and use a non-destructive merge; **never overwrite or delete** project-owned settings. If a move would damage managed Bootstrap inventory/upgrade paths, **copy/convert the host-facing files** and leave `.generic/` as managed source until an explicit, reviewed cleanup/migration. The effective runtime configuration **must** be native even when the portable staging files remain.
4. Verify host precedence, project-root discovery, agent list, skill discovery and hook loading with **actual host tools/commands/UI**, not folder-name assumptions. Record whether project files override personal/global settings, or whether enterprise policies can disable them; do not claim universal priority.
5. Verify a harmless edit is allowed and an unapproved protected edit is denied **on each supported write channel**. Check terminal/MCP bypass separately. Advisor/Human proof remains GUIDED_ONLY unless independently verifiable.
6. Log host/version, chosen native path, generated file list, actual registration method, positive/negative evidence, and limitations in setup evidence. `native_adapter_paths` must list **real native active files, not `.generic/*` reference files**.
7. Only after native discovery and evidence may setup proceed toward activation. If the host has no equivalent capability, provide evidence and a limited fallback instead of claiming a successful rename or automatic hook.

**Rule:** `.generic` is the **input**; verified host-native folders and project settings are the **active output**. Renaming without schema conversion and loading evidence does not make the host prioritize the configuration.

Reference docs (verify current version during setup):
- OpenCode: https://opencode.ai/docs/config/ and https://opencode.ai/docs/agents/
- Qwen Code: https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/sub-agents.md
- VS Code Copilot: https://code.visualstudio.com/docs/agent-customization/custom-agents and https://code.visualstudio.com/docs/agent-customization/hooks
- Claude Code: https://code.claude.com/docs/en/sub-agents and https://code.claude.com/docs/en/skills
