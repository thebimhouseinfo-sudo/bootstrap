# Bootstrap — reusable project-root harness template

This repository provides the canonical **project-template/** directory tree. Copy its CONTENTS to the target project's root, inspect existing files, then adapt—not recreate—the project scaffold.

## Where to start

1. Read [project-template/SETUP.md](project-template/SETUP.md) and [the full bootstrap prompt](harness-bootstrap-prompt-v9.md).
2. Inspect the project and its agent runtime/OS/host; choose Lite, Standard or Full with the user.
3. Before modifying the target project, propose adaptation, enforcement and model assignments for approval. Never overwrite existing protected configuration blindly.
4. Copy the actual project-root tree. Portable generic skills and agent role prompts are reusable; runtime-specific registration, scripts, hooks, loops, gates and approval channels MUST be adapted and tested.
5. Planner writes the project's AGENTS.md, CRITERIA, GOALMAP, milestones and tasks, following approved theory. Bootstrap does not invent product logic.
6. An empty project begins in Planner **Discovery Mode** with brainstorming + research, recording OPEN ideas in CRITERIA. Full harness and development planning follow sufficient approved theory.
7. Coder and Tester work with generic defaults; optionally reload user-configured project skills/knowledge. Do not treat missing optional packs as task failure.
8. Test guard/loop behavior on disposable fake projects; report ENFORCED versus GUIDED_ONLY and UNVERIFIED honestly. Never claim working hooks merely from their specs.

## Source and compatibility

- Canonical project tree: `project-template/`.
- Legacy categorized templates (`templates/` on main) are not the installation target.
- The user-provided `bootstrap-reorganized.zip` informed the improved gate, approval, self-test and harness-spec guides in `project-template/harness/specs/`; it remains an input archive, not a second source of project templates.
- `docs/CRITERIA.md` inside each target project is the single product-theory source. GOALMAP lives there.

Default: no push, no unsafe/destructive changes, no fabricated approval, no silent model substitution.
