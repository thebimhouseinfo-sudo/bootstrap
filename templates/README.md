# Generic harness starter templates

Copy only the templates needed for the approved bootstrap tier. These are **scaffolds, not a working harness**. Follow `harness-bootstrap-prompt-v9.md` for intake, proposal, user approval, runtime-specific implementation and simulation tests.

## Selection

| Tier | Copy |
|---|---|
| Lite | `core/*`, `operations/EVIDENCE_REPORT.md`, `operations/LESSON.md`, `contracts/VERIFY.md`, `contracts/APPROVAL.md`, `contracts/ENFORCEMENT.md` |
| Standard | Lite + `planning/*`, `operations/REVIEW.md`, `contracts/TRACE.md`, `contracts/ROLES.md` |
| Full | Standard + `contracts/FIXER.md`, `contracts/GIT_ADMIN.md` |

The `core/CRITERIA.md` file is **the only source of truth for product theory**. GOALMAP lives in CRITERIA, not in a separate authoritative file. Milestones, tasks, tests and trace are derived.

## Use

1. Complete intake and inventory existing files, commands and constraints. If new project has no approved logic, stop (case C). 
2. Present a harness-only proposal and obtain the required user approval before installing anything.
3. Copy only appropriate templates into the project, mapping directories to the paths in the prompt. Delete irrelevant sections; fill placeholders with verified evidence or `UNVERIFIED`.
4. Implement executable scripts, hooks, role configs and UI **for the verified target runtime**; the contract templates below are not executable.
5. Simulate allowed and blocked scenarios on a disposable copy. Record `ENFORCED`, `GUIDED_ONLY`, `UNVERIFIED` honestly. Do not treat template presence as a passing test.

Never copy real secrets, project-specific assumptions, model IDs, platform commands, or example product behavior into the target project by default.
