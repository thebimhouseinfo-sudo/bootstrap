#!/usr/bin/env python3
"""Claude Code project config + hook preflight; no claim of native hook trust/enforcement."""
import argparse
import json
import math
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
REQUIRED_EVENTS = {"UserPromptSubmit", "PreToolUse", "Stop"}
REQUIRED_FILES = (
    ".claude/settings.json", "harness/claude/hook.py",
    "harness/common/snapshot.py", "harness/common/task.py",
    "harness/common/verify.py", "harness/hook-policy.json",
    "harness/active-task.json",
)


def validate_hooks(path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or not isinstance(obj.get("hooks"), dict):
        raise ValueError("settings.json requires a hooks object")
    present = set(obj["hooks"])
    missing = REQUIRED_EVENTS - present
    if missing:
        raise ValueError("missing hook events: " + ", ".join(sorted(missing)))
    for event, groups in obj["hooks"].items():
        if event not in REQUIRED_EVENTS:
            continue
        if not isinstance(groups, list) or not groups:
            raise ValueError("missing hook group for " + event)
        for group in groups:
            if (not isinstance(group, dict) or not isinstance(group.get("hooks"), list)
                    or not group["hooks"]):
                raise ValueError("invalid hook group for " + event)
            for item in group["hooks"]:
                if (not isinstance(item, dict) or item.get("type") != "command"
                        or not isinstance(item.get("command"), str)
                        or "harness/claude/hook.py" not in item["command"]):
                    raise ValueError("hook command must reference harness/claude/hook.py")
                timeout = item.get("timeout", 600)
                if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
                        or not math.isfinite(timeout) or timeout <= 0):
                    raise ValueError("hook timeout must be a finite positive number")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project-trusted", choices=["yes", "no", "unknown"], default="unknown")
    args = ap.parse_args(argv)
    binary = shutil.which("claude") or shutil.which("claude-code")
    if binary:
        try:
            result = subprocess.run([binary, "--version"], capture_output=True, text=True,
                                    timeout=8, check=False)
            print("CLAUDE_VERSION:", result.stdout.strip() or result.stderr.strip() or "UNVERIFIED")
        except (OSError, subprocess.TimeoutExpired):
            print("CLAUDE_VERSION: UNVERIFIED")
    else:
        print("CLAUDE_VERSION: UNAVAILABLE (claude or claude-code binary not on PATH)")
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    if missing:
        print("NOT_CONFIGURED: missing project adapter files:", ", ".join(missing))
        return 2
    try:
        validate_hooks(ROOT / ".claude/settings.json")
        print("PROJECT_HOOKS: PARSED (not proof loaded)")
    except (OSError, ValueError, TypeError) as exc:
        print("PROJECT_HOOKS: INVALID", str(exc))
        return 2
    try:
        policy = json.loads((ROOT / "harness/hook-policy.json").read_text(encoding="utf-8"))
        if not isinstance(policy, dict) or any(
                not isinstance(policy.get(key), bool)
                for key in ("snapshot_apply_patch", "stop_verify")):
            raise ValueError("policy must contain boolean snapshot_apply_patch and stop_verify")
        print("HOOK_POLICY: snapshot_apply_patch=" + str(policy.get("snapshot_apply_patch")),
              "stop_verify=" + str(policy.get("stop_verify")))
    except (OSError, ValueError) as exc:
        print("HOOK_POLICY: INVALID", str(exc))
        return 2
    print("PROJECT_TRUST:", args.project_trusted)
    print("HOOK_EVENT: read hook_event_name from native JSON stdin; optional wrapper env override")
    print("HOOK_TRUST: UNVERIFIED until Claude Code actually dispatches hooks with correct env/schema")
    print("NATIVE_AGENTS: .claude/agents/*.md presence is not proof of runtime subagent discovery")
    if args.project_trusted != "yes":
        print("WARNING: verify hook trust settings in Claude Code before relying on enforcement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
