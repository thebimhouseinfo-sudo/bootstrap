# Bootstrap and maintenance without fake authorization

There are two explicit modes. MANUAL_COORDINATION is the default until a user-authenticated adapter has been proven. An AI may propose changes and apply only actions directly authorized by the human in the current scope via the host's normal controls; it MUST NOT forge ledger entries, claim AGREE signatures, auto-sign G0/G11, or claim identity authentication. Protected automated gates remain AWAITING_USER / NOT_CONFIGURED, not PASS.

AUTHENTICATED_ADAPTER mode requires a user-response source the agent cannot invoke or impersonate. Verify role isolation with an adversarial test. Terminal commands run by the same OS account as the agent and copy-to-clipboard inbox do not establish human identity.

If the approval channel is unavailable or broken, the user operates a maintenance process outside the broken channel. Prepare a read-only plan, before/after hashes, snapshot and restore instructions; obtain explicit human action via an independent mechanism and keep the automation disabled until repaired and tested. This does not upgrade manual coordination into cryptographic approval.

Do not allow a broken approval service to approve its own repair. Treat privilege/policy changes as T1 and obtain independent approval before production application.
