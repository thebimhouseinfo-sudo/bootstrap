# `.antigravity/` — Google Antigravity IDE role definitions

This directory mirrors the same role structure as `.codex/` and `.claude/`, adapted for the **Google Antigravity IDE** runtime.

## Structure

```text
.antigravity/
  agents/         ← per-role agent definitions with Antigravity-native model names
    advisor.md
    coder.md
    critic.md
    explorer.md
    harness-fixer.md
    planner.md
    reviewer.md
    tester.md
```

## How it relates to `.agents/`

| Path | Purpose |
|---|---|
| `.antigravity/agents/*.md` | **Role registration** — model assignment, effort, runtime tag. One file per role. |
| `.agents/roles/*.md` | **Role contracts** — actual instructions for each role (shared across runtimes). |
| `.agents/skills/*.md` | **Skills** — natively auto-loaded by Antigravity from this directory. |
| `.agents/hooks.json` | **Lifecycle hooks** — Antigravity Stop/PreToolUse hooks (e.g. auto-verify). |

The `contract:` field in each `.antigravity/agents/*.md` points back to `.agents/roles/{role}.md`, which holds the actual instructions. This separation follows the bootstrap pattern: runtime-specific config (model name, effort) lives here; generic logic lives in `.agents/roles/`.

## Model mapping (verified 2026-10-18)

Available models in this IDE:

| Role | Model | Fallback |
|---|---|---|
| planner | Claude Opus 4.6 (Thinking) | Gemini 3.8 Flash High |
| advisor | Claude Opus 4.6 (Thinking) | Gemini 3.8 Flash High |
| reviewer | Claude Sonnet 4.6 (Thinking) | Gemini 3.8 Flash High |
| coder | Claude Sonnet 4.6 (Thinking) | Gemini 3.8 Flash High |
| tester | Gemini 3.8 Flash High | Claude Sonnet 4.6 (Thinking) |
| critic | GPT-OSS 120B (Medium) | Gemini 3.8 Flash High |
| explorer | Gemini 3.8 Flash High | Claude Sonnet 4.6 (Thinking) |

> **Rule:** If the assigned model is unavailable, report `UNAVAILABLE` — never substitute silently.
> Full rationale: `.agents/MODEL_SELECTION.md`
