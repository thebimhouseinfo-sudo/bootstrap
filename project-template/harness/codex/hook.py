#!/usr/bin/env python3
"""Codex-native hook entry point; stdin/stdout follow documented Codex hook JSON."""
import contextlib
import importlib.util
import io
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
COMMON = ROOT / "harness/common"
POLICY = ROOT / "harness/hook-policy.json"
TASK = ROOT / "harness/active-task.json"

def load_module(filename):
    spec = importlib.util.spec_from_file_location("bootstrap_" + filename, COMMON / (filename + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def output(data):
    print(json.dumps(data, ensure_ascii=True))

def context(message, event):
    return {"hookSpecificOutput":{"hookEventName":event,"additionalContext":message}}

def policy():
    try:
        val = json.loads(POLICY.read_text(encoding="utf-8"))
        if isinstance(val, dict):
            return val
    except (OSError, ValueError):
        pass
    return {"snapshot_apply_patch": False, "stop_verify": False}

def patch_paths(payload):
    if not isinstance(payload, dict):
        return []
    tool = payload.get("tool_input")
    if not isinstance(tool, dict):
        return []
    command = tool.get("command", tool.get("patch", ""))
    if not isinstance(command, str):
        return []
    # Exact apply_patch file headers only. Do not pretend to cover shell/MCP edits.
    paths = []
    for line in command.splitlines():
        match = re.match(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$", line)
        if match:
            paths.append(match.group(1).strip())
    return list(dict.fromkeys(paths))

def pretool(payload):
    if payload.get("tool_name") != "apply_patch":
        return {}
    # Git branch authority is intentionally local to the Git common directory.
    # For Git projects do not allow an observed patch without an explicitly
    # chosen active branch. Other tools are NOT covered by this hook.
    try:
        probe = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--is-inside-work-tree"],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               text=True, timeout=5, check=False)
        if probe.returncode == 0 and probe.stdout.strip() == "true":
            branch_check = subprocess.run([sys.executable, str(COMMON / "branch_authority.py"),
                                           "check-write"], cwd=str(ROOT),
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          text=True, timeout=8, check=False)
            if branch_check.returncode != 0:
                return {"hookSpecificOutput": {
                    "hookEventName": "PreToolUse", "permissionDecision": "deny",
                    "permissionDecisionReason": "Branch authority: " + branch_check.stdout[-350:]}}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": "Cannot check Git branch authority: " + str(exc)[:180]}}
    paths = patch_paths(payload)
    notes = []
    if any(name.startswith(("docs/CRITERIA.md", "harness/active-task.json",
                            ".codex/hooks.json")) for name in paths):
        notes.append("PROTECTED-SCOPE GUIDANCE: no theory/approval/hook-state changes without actual human authorization; this hook cannot authenticate the human.")
    if paths and policy().get("snapshot_apply_patch", False):
        try:
            mod = load_module("snapshot")
            existing = []
            for name in paths:
                rel = pathlib.Path(name)
                if rel.is_absolute() or ".." in rel.parts or not rel.parts:
                    raise ValueError("patch path escapes project: " + name)
                dest = ROOT / rel
                if dest.is_symlink() or not dest.parent.resolve().is_relative_to(ROOT):
                    raise ValueError("patch path points to symlink/outside project: " + name)
                if dest.is_file():
                    # Apply the same exclusion rules as explicit snapshots.
                    mod.source_file(name)
                    existing.append(name)
            if existing:
                snap = mod.capture(existing)
                notes.append("Pre-edit snapshot " + snap + " captured for " + str(len(existing)) + " files.")
        except (OSError, ValueError) as exc:
            # Blocking the supported apply_patch tool on a failed explicit snapshot
            # is useful, but does NOT prevent Bash, MCP or hosted paths.
            return {"hookSpecificOutput":{"hookEventName":"PreToolUse",
                        "permissionDecision":"deny",
                        "permissionDecisionReason":"Pre-edit snapshot failed: " + str(exc)}}
    if notes:
        return context(" ".join(notes), "PreToolUse")
    return {}

def stop(payload):
    config = policy()
    if not config.get("stop_verify", False):
        return {}
    try:
        task = json.loads(TASK.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    if not isinstance(task, dict) or task.get("status") != "ACTIVE":
        return {}
    # Codex indicates this same turn has already been continued by Stop.
    # Never spend more model quota in an unbounded hook continuation loop.
    if payload.get("stop_hook_active") is True:
        return {"systemMessage":"Bootstrap: one bounded retry already requested; unresolved tests must be reported to human."}
    trace = load_module("task")
    with contextlib.redirect_stdout(io.StringIO()):
        trace_result = trace.main(["--stage", "delivery"])
    if trace_result != 0:
        return {"decision":"block",
                "reason":"Bootstrap active task has missing/invalid theory→test→evidence links. Correct only the current approved goal; do not mark a gate PASS."}
    result = subprocess.run([sys.executable, str(COMMON / "verify.py")],
                            cwd=str(ROOT), stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace",
                            timeout=120, check=False)
    if result.returncode == 0:
        return {"systemMessage":"Bootstrap: configured script checks passed; user approval and independent reviews are separate."}
    return {"decision":"block",
            "reason":"Bootstrap active task verification failed or is not configured (" +
                     str(result.returncode) + "). Resolve the test evidence, rerun the exact checks, then report unverified real-host tests. " +
                     result.stdout[-500:]}

def handle(payload):
    if not isinstance(payload, dict):
        return {}
    event = payload.get("hook_event_name")
    if event == "SessionStart":
        return context("Bootstrap Codex-first: use approved CRITERIA only; Advisor at decision gates. "
                       "Hook adapter installed, but human-only approvals/gate signatures remain NOT_CONFIGURED. "
                       "For Git projects use harness/common/branch_authority.py status before edits/merges/push; never infer main. "
                       "Check harness/common/status.py for tested capability state.", event)
    if event == "PreToolUse":
        return pretool(payload)
    if event == "Stop":
        return stop(payload)
    return {}

def main():
    try:
        payload = json.loads(sys.stdin.read(1_048_576))
        output(handle(payload))
        return 0
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired) as exc:
        # Report hook failure, never misrepresent it as successful enforcement.
        output({"systemMessage":"Bootstrap hook UNVERIFIED: " + str(exc)[:250]})
        return 0

if __name__ == "__main__":
    sys.exit(main())
