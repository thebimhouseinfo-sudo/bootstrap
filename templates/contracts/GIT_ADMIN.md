# Git administration contract (Full, optional)

Not an executable script. Install only when Git is in use and the user approved the mechanism.

- Inspect repo, remote, working tree, branch and merge state before action.
- Default: do not push. Direct push forbidden by real guard if claimed ENFORCED.
- Authorized push binds exact request, remote, ref and commit set, one use only, with required gate PASS.
- Protect uncommitted work, unknown branches and unrelated commits. No unconditional reset --hard, force push, unreviewed branch deletion or history rewrite.
- If no Git: NOT_APPLICABLE. If integration unknown or unverified: BLOCKED/UNVERIFIED.
- Test with local disposable remotes, both legitimate and prohibited operations.
