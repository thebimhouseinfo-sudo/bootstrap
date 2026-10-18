# Harness — instructions to implement, not prebuilt implementation

Copy these contracts as the project tree. After approval, Bootstrap implements the real mechanisms per VERIFIED agent runtime, OS, shell, product host, version and available tool capabilities. Prefer existing trusted native facilities; avoid overengineering.

| Area | Instruction contract | Expected implementation |
|---|---|---|
| verify | specs/VERIFY.md | actual executable script/command |
| snapshot/restore | specs/SNAPSHOT.md | safe backup and restore |
| hooks | specs/HOOKS.md | native hooks when supported, else manual/task-runner fallback |
| loop | specs/REVIEW_LOOP.md | verified review/repair trigger and state |
| gates | specs/GATES.md | approved milestone gate checks |
| approvals/journal | specs/APPROVAL.md | real human-only channels and append-only ledgers |
| trace | specs/TRACE.md | generator/checker |
| fix | specs/FIXER.md | Full only, real doctor and selftest |
| acceptance/selftests | specs/TESTS.md | tier-scoped positive/negative simulated tests |
| approved guard specification | specs/HARNESS_SPEC_TEMPLATE.md | approved rules copied and adapted into HARNESS_SPEC.md |

A description is NOT an implementation. Bootstrap records ENFORCED/GUIDED_ONLY/NOT_CONFIGURED, actual tests and rollback. Do not fabricate empty executable files or claim tests pass. Install only mechanisms required by the approved tier.
