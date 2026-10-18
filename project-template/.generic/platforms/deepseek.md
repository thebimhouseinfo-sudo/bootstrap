# DeepSeek-based coding workflow — choose the actual client first

**DeepSeek generally identifies a model/API provider**, not one universally standardized IDE coding-agent runtime. Official provider docs: https://api-docs.deepseek.com/guides/coding_agents/

Choose `--runtime generic --target-app deepseek` only if the Human still needs to decide/port the actual coding client. Ask which client uses DeepSeek (e.g. Qwen Code, Cline, OpenCode, Continue, a custom tool). **Do not register a fictional `.deepseek/agents` directory.** If a supported client already has a prepared adapter, choose THAT `--runtime` (e.g. Continue), and configure its provider/model only.

Reuse `.generic/agents/` when adapting an unconfigured client. Keep provider tokens/secrets in supported credential storage; verify exact model, API/tool compatibility, native rules, approval prompts and permitted file operations in the host. Record UNVERIFIED claims.
