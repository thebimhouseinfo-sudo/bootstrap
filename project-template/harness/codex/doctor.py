#!/usr/bin/env python3
"""Platform-independent baseline template validation; not a security guard."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
NEEDED = [
    "AGENTS.md", "docs/CRITERIA.md", "docs/PROJECT_PROFILE.md",
    "TASKS.md", ".agents/roles/planner.md", ".agents/roles/reviewer.md",
    ".agents/roles/critic.md", ".agents/roles/coder.md",
    ".agents/roles/tester.md", ".agents/skills/plan-task/SKILL.md",
    "harness/codex/verify.py", "harness/codex/checks.json",
]
def main():
    missing = [p for p in NEEDED if not (ROOT / p).is_file()]
    for p in missing: print("MISSING:", p)
    skills = list((ROOT / ".agents/skills").glob("*/SKILL.md"))
    invalid = [p for p in skills if not p.read_text(encoding="utf-8").startswith("---\n")]
    for p in invalid: print("INVALID_SKILL_FRONTMATTER:", p)
    if missing or invalid:
        return 1
    print("PASS: template file inventory only; runtime hooks, approvals and gates NOT_VERIFIED")
    return 0
if __name__ == "__main__": sys.exit(main())
