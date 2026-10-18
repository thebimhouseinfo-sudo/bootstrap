#!/usr/bin/env python3
"""Codex-first, cross-platform verification runner. Python >=3.9, no dependencies.
Only runs user-verified commands from harness/codex/checks.json.
Never treats an empty checklist as PASS.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONFIG = pathlib.Path(__file__).with_name("checks.json")

def main():
    if not CONFIG.exists():
        print("NOT_CONFIGURED: missing checks.json")
        return 2
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        checks = data.get("checks", [])
        if not isinstance(checks, list) or not checks:
            print("NOT_CONFIGURED: no verified commands")
            return 2
        for item in checks:
            name, argv = item["name"], item["argv"]
            if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
                raise ValueError("argv must be a nonempty string array")
            timeout = int(item.get("timeout_seconds", 120))
            if timeout <= 0 or timeout > 3600:
                raise ValueError("timeout_seconds out of range")
            print("RUN:", name, flush=True)
            try:
                p = subprocess.run(argv, cwd=ROOT, timeout=timeout, check=False, shell=False)
            except (OSError, subprocess.TimeoutExpired) as exc:
                print("FAIL:", name, str(exc))
                return 1
            if p.returncode:
                print("FAIL:", name, "exit", p.returncode)
                return 1
            print("PASS:", name)
        print("PASS: all configured checks; real-host verification is separate")
        return 0
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print("NOT_CONFIGURED: invalid checks:", exc)
        return 2

if __name__ == "__main__":
    sys.exit(main())
