# Codex native adapter

Native named agents are prepackaged in `.codex/agents/*.toml` using the documented required fields `name`, `description` and `developer_instructions`; read-only roles specify `sandbox_mode`. No agent model is pinned: the effective model comes from the verified parent/runtime configuration. Model/approval/sandbox constraints imposed by the parent cannot be escalated by role files.

Project-local `.codex/config.toml` is intentionally privilege-neutral. The user's trusted-project state and effective parent CLI flags/overrides can suppress project configuration or interaction. Run `python harness/codex/preflight.py` to see non-sensitive evidence and warnings; parent effective approval must be supplied only from direct runtime observation.

Installer: from this bootstrap checkout, `python install.py --target <existing-project-path>` previews additions/conflicts; after review/approval, `python install.py --target <path> --apply` copies only missing files, preserving existing source/config. Repeat is idempotent for unchanged files. Conflicts are not overwritten.

Native hook definitions are not installed by default because version-specific lifecycle mapping, trust review and failure semantics require verified runtime testing; do not claim hook enforcement. Project hooks may require explicit human trust. See `harness/specs/READINESS.md` and `harness/specs/APPROVAL_MAINTENANCE.md`.

Official references: https://learn.chatgpt.com/docs/agent-configuration/subagents and https://learn.chatgpt.com/docs/hooks
