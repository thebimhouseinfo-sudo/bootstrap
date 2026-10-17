# Role contracts (configure with target runtime's verified syntax)

| Role | Mandate | Write scope | Input | Output |
|---|---|---|---|---|
| Planner | Derive goalmap, milestones and tasks | planning files; theory only via approved update | user-sourced approved theory | plan + approval requests |
| Coder | One scoped task | source files only | task, goal, profile | code + verify output |
| Tester | Validate actual acceptance | tests, evidence | goal/AC, runtime | tests and measured evidence |
| Reviewer | Contextual goal-scoped audit | findings/backlog/lessons | goal, task, diff, evidence | blocking finding or PASS |
| Critic | Independent outside view | none | product and public README ONLY | raw observations |
| Explorer (optional) | Narrow repository research | none | concrete question | concise findings |
| Harness fixer (Full) | Repair harness without weakening policy | harness per authorized tier | block diagnosis/spec | verified patch |

Model, reasoning, sandbox, skill and fallback assignments must be configured and VERIFIED for the actual agent runtime. No silent model substitution. Role != model != project profile != skill. A textual role table is GUIDED_ONLY unless permissions are actually enforced.
