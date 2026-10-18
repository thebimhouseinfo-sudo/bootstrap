# Enforcement inventory

| Boundary / rule | Mechanism | State | Proof (allowed and rejected cases) |
|---|---|---|---|
| Protected theory writes | <hook/tool> | UNVERIFIED | <evidence> |
| Human-only approvals | <UI/sandbox> | UNVERIFIED | <evidence> |
| Journal/ledger integrity | <append-only/hash/ACL> | UNVERIFIED | <evidence> |
| Role write isolation / critic context | <sandbox> | UNVERIFIED | <evidence> |
| Unsafe commands / secrets | <pretool guard> | UNVERIFIED | <evidence> |
| Raw push / Git policy | <guard/git-admin> | UNVERIFIED | <evidence> |
| Stop/verify gating | <runtime hook> | UNVERIFIED | <evidence> |

States: ENFORCED = demonstrated by mechanism and tests; GUIDED_ONLY = instructions without reliable technical guard; UNVERIFIED = untested; NOT_APPLICABLE = justified absent feature.

For any BLOCK: include rule ID, actual reason, location of definition and authorized recovery path. Record false positive tests too.
