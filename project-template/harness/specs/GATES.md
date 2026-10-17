# Milestone and gate engine implementation guide

Planner defines milestone GOAL set and triggers. Bootstrap builds gate machinery appropriate to runtime, without defining project milestones or product acceptance criteria.

Gate statuses: PASS, FAIL, BLOCKED, UNVERIFIED, NOT_CONFIGURED, NOT_APPLICABLE. Missing gate mechanism/approval never counts PASS. Source or theory changes invalidate dependent gates only. Record actual evidence, who/what granted authorization, and rollback. Follow G0–G14 semantics as applicable from bootstrap prompt v9; don't install Full mechanisms in Lite by default.
