# Generic harness bootstrap library

Reusable scaffolds, role contracts and generic SKILL.md definitions. These are not a preinstalled runtime harness; follow the main prompt for approvals, runtime-specific implementation and testing.

## Tiers
- Lite: core docs, evidence/lesson/verify/approval contracts, generic coder + reviewer and relevant common skills.
- Standard: Lite + planning docs, planner/tester/critic, review/trace contracts.
- Full: Standard + harness-fixer and Git administration.

## Reusability contract
- Planner, Reviewer, Critic: portable project-independent role behavior.
- Coder **and Tester**: generic defaults work with empty custom configuration. Optional project-scoped skill and knowledge packs are loaded/reloaded independently per role on session/task/project-context change to improve first-pass accuracy, not to make basic operation possible.
- Use `config/worker-context.example.yaml`, `skills/context-reload/`, and `knowledge/PACK.template.md` as the starting points. The former coder-skills example is compatibility-only.
- Technical profile requirements are not optional: missing optional knowledge is no excuse to knowingly ignore target dialect or API compatibility.
- No shared generic template should embed project-specific Visual LISP, Revit, web or other reference rules.

## Installation
1. Inventory existing project, approved theory, runtime/version, skills, models and tools; stop for case C without approved product logic.
2. Propose only harness setup and obtain approval before material changes.
3. Copy selected documents, subagent/skill contracts and data manifests; adapt to official native runtime configuration and verify actual invocation, permissions and context reload.
4. Project user may add coder/tester skill and knowledge paths without modifying generic base roles. No customization is required for initial use.
5. Implement scripts/guards/hooks per verified runtime; simulation-test working generic fallback, enriched mode and blocked cases. Do not claim ENFORCED when merely described.
6. Keep `docs/CRITERIA.md` as sole product-theory source, with GOALMAP inside.

No product development or raw push during bootstrap.
