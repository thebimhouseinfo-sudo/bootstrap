# Self-tests — implemented and not-yet-implemented mechanisms

**Executable tests in this Bootstrap repo:** `python tests/test_installer.py`, `python tests/test_harness_runtime.py`, and `python project-template/harness/common/test_verify.py`. CI runs Windows/macOS/Linux on Python 3.9/3.12.

Tested in disposable Python fixtures: installer tier/runtime, idempotence/cache protection, one-task theory/test/evidence validation, snapshot + hash-guarded preview/restore, refusal of unsafe paths, native Codex hook JSON mapping and execution from a nested cwd, pre-edit apply_patch snapshot and unsupported Bash path, Stop PASS/FAIL and **one** continuation with stop_hook_active preventing an endless loop.

**Future required tests before claiming ENFORCED or Codex-ready complete:** real client version and hook trust, permission/host bypass, user-only approval channel with impersonation rejection, complete G0–G14 signatures, full STALE propagation, automatic role orchestration, bounded repair with target hashes, Git policy and fixer negative tests. A fixture cannot certify these features. No fabricated pass or generic enterprise requirements for personal-only projects.
