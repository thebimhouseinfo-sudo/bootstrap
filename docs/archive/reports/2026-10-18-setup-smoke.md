# Installed setup smoke and native Codex inspection

Date: 2026-10-18, Asia/Bangkok. Platform: Windows, Python 3.14.5.
Baseline published before fixes: `d8e77b4`.

## Reproduced and fixed

`tests/test_setup_smoke.py` installs into disposable projects outside this checkout
and executes the shipped scripts and configured hook commands as subprocesses.
The initial eight tests produced nine failing assertions/subtests:

- Claude hook commands failed from a nested cwd because of relative script paths.
- Legacy MultiEdit's top-level file_path was omitted from pre-edit snapshots.
- Claude preflight crashed on an array-valued hook policy.
- Codex Add File traversal was not recognized by the path validator.
- Codex Move to traversal was not recognized by the path validator.
- Valid moves omitted an existing destination from the snapshot.
- Codex preflight accepted empty handler lists and boolean timeouts.
- The trace helper accepted REQ-123 when only REQ-1234 / REQ-123-extra existed.

A subsequent failing test reproduced missing native PreToolUse context JSON and
missing protected-path guidance for absolute Claude tool paths. Both were fixed.
Added a positive/negative Claude Stop check with a bounded retry.

Final setup suite: 10 tests pass. The existing suites and the new suite are
checked before the fix commit is published. CI now includes the new suite.

## Actual native Codex probe

Executed the installed `codex app-server --strict-config`, without a model turn,
against a disposable Standard/Codex installation. Protocol requests were
`initialize`, `hooks/list` and `config/read` with project layers included.
No trust bypass, project trust change, model substitution or user config edit.

- Client: `codex-cli 0.163.0-alpha.10.2`.
- initialize: successful.
- hooks/list: the project's list was empty; no hook parsing errors reported.
- config/read: project `.codex` layer had a disabledReason stating that the
  project must be added as trusted before project config/hooks/policies load.
- Effective project agent configuration was absent.

This is an observed project-trust prerequisite, not proof of working lifecycle
hooks. No SessionStart/PreToolUse/Stop native-dispatch or role-run acceptance is
claimed. Claude CLI was unavailable on PATH; Claude coverage is subprocess
adapter testing, not native Claude acceptance.

The first probe inside the shell sandbox timed out during initialization. The
same bounded probe succeeded outside that sandbox with approved execution.
Similarly, fixture tests required an explicitly writable external TEMP directory;
the sandbox-provided default TEMP had denied writes. Neither failure was hidden
as a passing code test.

## Next real-project test

After Human identifies the target project, inspect its existing files and Git
state, run installer preview, reconcile conflicts and apply the scoped setup.
Choose the active/frozen branches explicitly. Configure only the project's actual
check commands and approved task. Review project trust and exact hooks through
native Codex controls; then test allowed/denied edits, snapshot bytes, Stop
success/failure/bounded continuation and actual agent discovery on that client.

Keep compatible existing project data and instructions. Do not alter global
trust, automatically overwrite conflicts, fabricate approved requirements, or
mark Standard READY to get through setup. Authenticated approval, full gates,
full trace/staleness and autonomous review orchestration remain unimplemented;
their proposed architecture is in the separate design document.

## Runtime references

- [OpenAI hook trust and native output](https://learn.chatgpt.com/docs/hooks)
- [Claude hook stdin, PreToolUse context and Stop](https://code.claude.com/docs/en/hooks)
