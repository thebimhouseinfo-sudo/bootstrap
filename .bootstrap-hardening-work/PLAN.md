# Bootstrap hardening review (temporary implementation plan)

Source: user-supplied external code review. Keep legacy installs usable; no unverified security claims.

1. Fix source onboarding: explicit clone to a safe temporary folder; use raw text links for entry documents, tree links for folders; consolidate overlapping FOR_AI phases; Standard/Full normal setup.
2. First-install safety: prominent fail-safe warning when applying without --staged; never silently convert existing non-staged installs.
3. Fix .gitkeep packaging and test across tier/runtime.
4. Add versioned install manifest containing per-file source and installed hashes; explicit --upgrade only when prior installed hash matches, never overwrite a changed file; preserve collision reports.
5. On unexpected copy/apply errors, roll back newly created files and managed ignore/state only when unchanged, preserve concurrent edits, emit detailed outcome. Guard .gitignore source lookup.
6. Final lock: require interactive terminal with typed confirmation for activate/finalize; do not mistake TTY for authenticated identity; user-operated terminal separate from agent. Add explicit recover.py with dry-run and backup; avoid bypass.
7. Add regression cases, run CI 3 OS x 2 Python versions, fix breakage; remove this temporary plan directory.

No native host capability or real-human approval can be certified by CI.
