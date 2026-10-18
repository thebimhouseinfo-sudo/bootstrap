#!/usr/bin/env python3
"""Claude Code native hook adapter. Stdin/stdout follow Claude Code hook JSON schema.

Exit 0 = allow/continue. Exit 2 = block (stderr message returned to Claude).
Reads CLAUDE_HOOK_EVENT env var OR JSON payload on stdin; both paths supported.
Reuses harness/common/*.py; does not replicate Codex semantics verbatim.
"""
import contextlib
import importlib.util
import io
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
COMMON = ROOT / "harness/common"
POLICY = ROOT / "harness/hook-policy.json"
TASK = ROOT / "harness/active-task.json"

# Protected paths that require explicit human authorization.
PROTECTED_PATHS = frozenset([
    "docs/CRITERIA.md",
    "harness/active-task.json",
    ".claude/settings.json",
    "harness/hook-policy.json",
])


def load_module(filename):
    spec = importlib.util.spec_from_file_location(
        "bootstrap_" + filename, COMMON / (filename + ".py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def policy():
    try:
        val = json.loads(POLICY.read_text(encoding="utf-8"))
        if isinstance(val, dict):
            return val
    except (OSError, ValueError):
        pass
    return {"snapshot_apply_patch": False, "stop_verify": False}


def git_check_write():
    """Return None (ok) or error string if branch write is blocked."""
    try:
        probe = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=5, check=False,
        )
        if probe.returncode != 0 or probe.stdout.strip() != "true":
            return None  # not a Git project; skip check
        result = subprocess.run(
            [sys.executable, str(COMMON / "branch_authority.py"), "check-write"],
            cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=8, check=False,
        )
        if result.returncode != 0:
            return "Branch authority BLOCKED: " + result.stdout[-350:]
        return None
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "Cannot check Git branch authority: " + str(exc)[:180]


def extract_file_paths(tool_name, tool_input):
    """Extract file paths from Claude Code tool_input for known write tools."""
    paths = []
    if not isinstance(tool_input, dict):
        return paths
    # Edit, Write, MultiEdit, Create
    if tool_name in ("Edit", "Write", "Create", "str_replace_editor"):
        p = tool_input.get("file_path") or tool_input.get("path")
        if isinstance(p, str) and p.strip():
            paths.append(p.strip())
    elif tool_name == "MultiEdit":
        # Legacy MultiEdit applies several replacements to one top-level file.
        p = tool_input.get("file_path")
        if isinstance(p, str) and p.strip():
            paths.append(p.strip())
        edits = tool_input.get("edits", [])
        for edit in edits if isinstance(edits, list) else []:
            p = edit.get("file_path") if isinstance(edit, dict) else None
            if isinstance(p, str) and p.strip():
                paths.append(p.strip())
    # Bash: scan for output-redirected files or explicit paths (best-effort only)
    # NOTE: Bash is not fully covered; do not claim universal file-write protection.
    return list(dict.fromkeys(paths))


def pretool(payload):
    """Handle PreToolUse: branch check, protected-path warning, optional snapshot."""
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # 1. Git branch authority check for all write tools.
    write_tools = {"Edit", "Write", "Create", "MultiEdit", "str_replace_editor", "Bash"}
    if tool_name in write_tools:
        err = git_check_write()
        if err:
            print(err, file=sys.stderr)
            return 2

    # 2. Collect file paths for write-capable tools.
    paths = extract_file_paths(tool_name, tool_input)

    # 3. Protected-path guidance (cannot authenticate human; guidance only).
    warnings = []
    for p in paths:
        relpath = pathlib.Path(p)
        if relpath.is_absolute():
            try:
                relpath = relpath.relative_to(ROOT)
            except ValueError:
                continue  # Snapshot validation below handles out-of-project paths.
        rel = relpath.as_posix()
        if any(rel == prot or rel.startswith(prot + "/") for prot in PROTECTED_PATHS):
            warnings.append(
                f"PROTECTED-SCOPE GUIDANCE: '{rel}' requires explicit human "
                "authorization. This hook cannot authenticate the human."
            )

    # 4. Optional pre-edit snapshot for known project files.
    config = policy()
    if paths and config.get("snapshot_apply_patch", False) and tool_name in (
        "Edit", "Write", "MultiEdit", "str_replace_editor"
    ):
        try:
            mod = load_module("snapshot")
            existing = []
            for name in paths:
                rel = pathlib.Path(name)
                if rel.is_absolute():
                    # Try to make relative to ROOT
                    try:
                        rel = rel.resolve().relative_to(ROOT)
                    except ValueError:
                        raise ValueError("path escapes project: " + name)
                if ".." in rel.parts or not rel.parts:
                    raise ValueError("path traversal rejected: " + name)
                dest = ROOT / rel
                if dest.is_symlink() or not dest.parent.resolve().is_relative_to(ROOT):
                    raise ValueError("symlink or outside-project path: " + name)
                if dest.is_file():
                    mod.source_file(str(rel))
                    existing.append(str(rel))
            if existing:
                snap = mod.capture(existing)
                warnings.append(
                    f"Pre-edit snapshot {snap} captured for {len(existing)} file(s)."
                )
        except (OSError, ValueError) as exc:
            print("Pre-edit snapshot failed: " + str(exc), file=sys.stderr)
            return 2

    if warnings:
        # PreToolUse context must use native JSON; plain stdout is not injected.
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "additionalContext": "\n".join(warnings)
        }}, ensure_ascii=True))
    return 0


def stop_hook(payload):
    """Handle Stop: validate active task trace/evidence and run configured checks."""
    config = policy()
    if not config.get("stop_verify", False):
        return 0

    try:
        task = json.loads(TASK.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return 0

    if not isinstance(task, dict) or task.get("status") != "ACTIVE":
        return 0

    # Prevent unbounded continuation loop.
    # Claude Code Stop payload includes `stop_hook_active` analogously to Codex.
    if payload.get("stop_hook_active") is True:
        print(
            "Bootstrap: one bounded retry already requested; "
            "unresolved tests must be reported to human.",
            file=sys.stderr,
        )
        return 0  # Allow stop; do not loop.

    # Validate trace links.
    trace = load_module("task")
    with contextlib.redirect_stdout(io.StringIO()):
        trace_result = trace.main(["--stage", "delivery"])
    if trace_result != 0:
        print(
            "Bootstrap active task has missing/invalid theory→test→evidence links. "
            "Correct only the current approved goal; do not mark a gate PASS.",
            file=sys.stderr,
        )
        return 2  # Block stop; request continuation.

    # Run configured script checks.
    result = subprocess.run(
        [sys.executable, str(COMMON / "verify.py")],
        cwd=str(ROOT), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
        timeout=120, check=False,
    )
    if result.returncode == 0:
        print(
            "Bootstrap: configured script checks passed; "
            "user approval and independent reviews are separate."
        )
        return 0

    print(
        "Bootstrap active task verification failed or is not configured "
        f"({result.returncode}). Resolve test evidence, rerun checks, "
        "then report unverified real-host tests.\n" + result.stdout[-500:],
        file=sys.stderr,
    )
    return 2  # Block stop; request continuation.


def session_start(payload):
    """Handle UserPromptSubmit (used as session/context injection)."""
    print(
        "Bootstrap Claude-adapter: follow approved CRITERIA only; "
        "Advisor at decision gates. "
        "Branch authority: run harness/common/branch_authority.py status before edits. "
        "Hook adapter installed; human-only approvals/gate signatures remain NOT_CONFIGURED. "
        "Check harness/common/status.py for tested capability state."
    )
    return 0


def handle(payload, event):
    """Dispatch to correct handler by event name."""
    if event == "UserPromptSubmit":
        return session_start(payload)
    if event == "PreToolUse":
        return pretool(payload)
    if event == "Stop":
        return stop_hook(payload)
    # Unknown event: allow transparently.
    return 0


def main():
    # Native event identity arrives in JSON stdin. Keep the environment override
    # for explicitly configured wrappers; do not require the host to set it.
    event = os.environ.get("CLAUDE_HOOK_EVENT", "")
    try:
        raw = sys.stdin.read(1_048_576)
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            payload = {}
        # Fallback: event may also be in payload.
        if not event:
            event = payload.get("hook_event_name", "")
        return handle(payload, event)
    except subprocess.TimeoutExpired as exc:
        print("Bootstrap hook TIMEOUT: " + str(exc)[:200], file=sys.stderr)
        return 0  # Allow on timeout; do not block unexpectedly.
    except (OSError, ValueError, TypeError) as exc:
        # Report but do not block: hook failure should not silently prevent work.
        print("Bootstrap hook UNVERIFIED: " + str(exc)[:250], file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
