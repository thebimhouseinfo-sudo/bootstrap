# Qwen Code — adapter guidance (host-untested)

Qwen Code documentation describes custom project subagents in `.qwen/agents/` with Markdown + YAML frontmatter, and `/agents` for managing them. Source: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

Choose `--runtime generic --target-app qwen-code`. After Human selects roles/permissions, use `.generic/agents/<role>.md` as the prompt body in the documented Qwen native format. Set host-supported model selection and **least necessary actual tools/approvalMode** only after checking version and user intent; do not invent a sandbox or bypass permissions. The installed `AGENTS.md` can be reused where Qwen supports it (see https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/).

**This generic package does not automatically create `.qwen/agents/`.** That step requires adapter verification and project approval. Smoke-test discovery via `/agents`, one allowed task, one disallowed edit, and actual model/tool availability.
