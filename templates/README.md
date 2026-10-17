# Generic harness bootstrap library

This directory supplies copy-and-adapt scaffolds plus **portable subagent and skill definitions**. It is not an installed runtime harness. Follow the main bootstrap prompt for intake, user approval, adaptation and simulation tests.

## Select a tier
- Lite: core docs, evidence, lesson, verify/approval/enforcement contracts, generic coder + reviewer agents, relevant default skills.
- Standard: Lite + planning docs, planner/tester/critic agent contracts, goal-review and trace-related skill/contracts.
- Full: Standard + harness-fixer, Git administration and advanced diagnosis contracts.

## Portable roles
`subagents/planner.md`, `reviewer.md`, `critic.md` are broadly project-independent. Keep their semantics stable. `coder.md` works generically without project extras; user may add specialized skills in project-scoped configuration. Never change the shared base because of a particular product.

## Bootstrap steps
1. Inventory existing repo, runtime/version, available model IDs, official extension formats, existing trusted skills and approvals. Case C (no approved product logic): stop.
2. Prepare harness-only proposal and obtain user approval; avoid overwriting existing config.
3. Copy relevant docs, subagent contracts, SKILL.md folders and data-only assignment samples. Adapt native subagent/skill directories and permission/sandbox to **verified runtime**, not assumptions.
4. Leave generic coder fully functional when `coder-skills.example.yaml` customization is empty. Add user-approved project-specific skills separately when provided. Verify stack/host and commands before enabling checks.
5. Implement authorization, state, verification and hooks for selected tier; templates alone are NOT executable protections.
6. Test both allowed and rejected role/guard scenarios in a disposable workspace, record ENFORCED vs GUIDED_ONLY vs UNVERIFIED.

`docs/CRITERIA.md` remains the single source of product theory with GOALMAP inside. All plans/tasks/trace derived. No raw pushes or product code during bootstrap.
