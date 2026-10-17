# Optional project knowledge packs

This folder defines how project-specific reference material is attached, not a universal source of technical facts. Keep the shared generic template repository free from CAD/Revit/web-specific assumptions.

A knowledge pack can hold verified dialect rules, API/host version compatibility, language conventions, official documentation locations, known integration constraints and reproducible examples. The user or bootstrap customizes it in the target project. Do not present unverified snippets as authoritative.

Coder and Tester independently load the applicable knowledge on each session/task (or when the project profile/version changes), alongside their SKILL.md selection. Load only relevant scoped material to avoid context dilution; track source, version and verification status. Tester uses knowledge to select correct assertions and host-specific reproduction steps, not to copy the coder's conclusions.

Missing/unloadable *optional* knowledge falls back to generic reasoning + source inspection + incremental test/debug. Notify when useful; never silently claim the relevant knowledge was consulted. An explicit supported-host requirement or user-approved constraint is still binding and cannot be bypassed due to missing optional context.
