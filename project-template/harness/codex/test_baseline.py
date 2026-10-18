#!/usr/bin/env python3
"""Disposable smoke checks of baseline scripts without running user project commands."""
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
def check(args, expected):
    p = subprocess.run([sys.executable, str(HERE / args)], capture_output=True, text=True, timeout=20)
    if p.returncode != expected:
        raise RuntimeError(f"{args}: expected {expected}, got {p.returncode}\n{p.stdout}\n{p.stderr}")
    return p.stdout
def main():
    assert "PASS: template file inventory" in check("doctor.py", 0)
    config = HERE / "checks.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    if not data.get("checks"):
        assert "NOT_CONFIGURED" in check("verify.py", 2)
    else:
        print("SKIP: verify smoke test, real commands are configured and must not run automatically")
    print("PASS: baseline smoke (no actual product verification)")
if __name__ == "__main__": main()
