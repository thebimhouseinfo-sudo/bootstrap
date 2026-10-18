#!/usr/bin/env python3
"""Codex project config + hook preflight; no claim of native hook trust/enforcement."""
import argparse
import json
import math
import pathlib
import shutil
import subprocess
import sys

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

ROOT = pathlib.Path(__file__).resolve().parents[2]
REQUIRED_EVENTS = {"SessionStart", "PreToolUse", "Stop"}
REQUIRED_FILES = (
    ".codex/config.toml", ".codex/hooks.json", "harness/codex/hook.py",
    "harness/common/snapshot.py", "harness/common/task.py",
    "harness/common/verify.py", "harness/hook-policy.json",
    "harness/active-task.json",
)

def validate_hooks(path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or not isinstance(obj.get("hooks"), dict):
        raise ValueError("hooks.json requires a hooks object")
    if set(obj["hooks"]) != REQUIRED_EVENTS:
        raise ValueError("hook events must be SessionStart, PreToolUse and Stop")
    for event, groups in obj["hooks"].items():
        if not isinstance(groups, list) or not groups:
            raise ValueError("missing hook group for " + event)
        for group in groups:
            if (not isinstance(group, dict) or not isinstance(group.get("hooks"), list)
                    or not group["hooks"]):
                raise ValueError("invalid hook group")
            for item in group["hooks"]:
                if (not isinstance(item, dict) or item.get("type") != "command"
                        or not isinstance(item.get("command"), str)
                        or "harness/codex/hook.py" not in item["command"]):
                    raise ValueError("hook command cannot resolve Codex Python adapter")
                timeout = item.get("timeout", 600)
                if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
                        or not math.isfinite(timeout) or timeout <= 0):
                    raise ValueError("hook timeout must be a finite positive number")

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--effective-approval-policy",
                    choices=["untrusted","on-failure","on-request","never"],
                    help="reported effective permission mode (not automatically verified)")
    ap.add_argument("--project-trusted", choices=["yes","no","unknown"], default="unknown")
    args = ap.parse_args(argv)
    binary = shutil.which("codex")
    if binary:
        try:
            result = subprocess.run([binary,"--version"], capture_output=True, text=True,
                                    timeout=8, check=False)
            print("CODEX_VERSION:", result.stdout.strip() or result.stderr.strip() or "UNVERIFIED")
        except (OSError, subprocess.TimeoutExpired):
            print("CODEX_VERSION: UNVERIFIED")
    else:
        print("CODEX_VERSION: UNAVAILABLE")
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).is_file()]
    if missing:
        print("NOT_CONFIGURED: missing project adapter files:", ", ".join(missing))
        return 2
    if tomllib:
        try:
            with (ROOT / ".codex/config.toml").open("rb") as f:
                tomllib.load(f)
            print("PROJECT_TOML: PARSED (not proof loaded)")
        except (OSError, ValueError) as exc:
            print("PROJECT_TOML: INVALID", str(exc))
            return 2
    else:
        print("PROJECT_TOML: UNVERIFIED (install tomli for Python 3.9 syntax checking)")
    try:
        validate_hooks(ROOT / ".codex/hooks.json")
        print("PROJECT_HOOKS: PARSED (not proof loaded)")
    except (OSError, ValueError, TypeError) as exc:
        print("PROJECT_HOOKS: INVALID", str(exc))
        return 2
    print("PROJECT_TRUST:", args.project_trusted)
    print("EFFECTIVE_APPROVAL:", args.effective_approval_policy or "UNVERIFIED (parent/CLI/managed config can override)")
    if args.effective_approval_policy == "never":
        print("WARNING: no interactive approvals in never mode")
    if args.project_trusted != "yes":
        print("WARNING: project-local hooks require user trust; inspect /hooks and restart if necessary")
    print("HOOK_TRUST: UNVERIFIED until native Codex /hooks shows these exact trusted definitions")
    print("NATIVE_AGENTS: file presence is not proof of runtime discovery")
    return 0

if __name__ == "__main__":
    sys.exit(main())
