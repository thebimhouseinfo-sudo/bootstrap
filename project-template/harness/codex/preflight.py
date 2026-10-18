#!/usr/bin/env python3
"""Non-destructive Codex preflight; never assumes effective session approval/trust."""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys
try:
    import tomllib
except ImportError:
    tomllib=None

ROOT=pathlib.Path(__file__).resolve().parents[2]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--effective-approval-policy",choices=["untrusted","on-failure","on-request","never"],help="explicitly reported by active parent session")
    ap.add_argument("--project-trusted",choices=["yes","no","unknown"],default="unknown")
    args=ap.parse_args()
    codex=shutil.which("codex")
    if codex:
        try:
            result=subprocess.run([codex,"--version"],capture_output=True,text=True,timeout=8,check=False)
            print("CODEX_VERSION:",result.stdout.strip() or result.stderr.strip() or "UNVERIFIED")
        except (OSError,subprocess.TimeoutExpired):
            print("CODEX_VERSION: UNVERIFIED")
    else:
        print("CODEX_VERSION: UNAVAILABLE")
    conf=ROOT/".codex/config.toml"
    if tomllib:
        try:
            with conf.open("rb") as f:tomllib.load(f)
            print("PROJECT_TOML: PARSED (not proof loaded)")
        except (OSError,ValueError) as exc:
            print("PROJECT_TOML: INVALID",type(exc).__name__)
            return 2
    else:
        print("PROJECT_TOML: UNVERIFIED (tomllib requires Python 3.11+)")
    print("PROJECT_TRUST:",args.project_trusted)
    print("EFFECTIVE_APPROVAL:",args.effective_approval_policy or "UNVERIFIED: parent CLI flags, managed config and runtime overrides can win")
    if args.effective_approval_policy=="never":
        print("WARNING: interactive approval workflow unavailable in 'never' sessions; do not claim human approval channel")
    if args.project_trusted!="yes":
        print("WARNING: project-local Codex hooks/config may not load until reviewed/trusted and session restarted")
    print("HOOK_TRUST: UNVERIFIED: requires runtime inspection; do not silently enable or bypass trust")
    print("NATIVE_AGENTS: config files present is NOT a discovery test")
    return 0
if __name__=="__main__":sys.exit(main())
