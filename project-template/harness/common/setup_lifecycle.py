#!/usr/bin/env python3
"""Staged Bootstrap setup coordinator. Local human coordination, NOT an authenticated gate."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE = ROOT / "harness/setup-state.json"
REQUIRED = ("AGENTS.md", "docs/CRITERIA.md", "docs/ARCHITECTURE.md",
            "docs/PROJECT_PROFILE.md", "harness/common/checks.json")


def read_state():
    if not STATE.exists():
        return None  # legacy installs are deliberately not reinterpreted
    try:
        value = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"schema_version": 1, "phase": "BOOTSTRAPPING", "invalid": True}
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return {"schema_version": 1, "phase": "BOOTSTRAPPING", "invalid": True}
    return value


def stage_active():
    state = read_state()
    return state is not None and state.get("phase") != "READY"


def run(args, cwd=ROOT, data=None):
    return subprocess.run(args, cwd=str(cwd), input=data, text=True, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=45, check=False)


def configured_checks():
    try:
        obj = json.loads((ROOT / "harness/common/checks.json").read_text(encoding="utf-8"))
        checks = obj.get("checks") if isinstance(obj, dict) else None
        return isinstance(checks, list) and bool(checks) and all(
            isinstance(c, dict) and isinstance(c.get("argv"), list) and
            bool(c["argv"]) and all(isinstance(a, str) and a for a in c["argv"])
            for c in checks)
    except (OSError, ValueError):
        return False


def audit():
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    for item in missing:
        print("BLOCK: missing required setup file:", item)
    problems = list(missing)
    if "docs/CRITERIA.md" not in missing:
        criteria = (ROOT / "docs/CRITERIA.md").read_text(encoding="utf-8")
        if not any(x.strip().upper() == "STATUS: APPROVED" for x in criteria.splitlines()):
            print("NOT_CONFIGURED: CRITERIA is not explicitly APPROVED")
            problems.append("CRITERIA approval")
    for doc in ("docs/ARCHITECTURE.md", "docs/PROJECT_PROFILE.md"):
        if doc not in missing:
            value = (ROOT / doc).read_text(encoding="utf-8")
            if "PLACEHOLDER" in value or "UNVERIFIED" in value:
                print("NOT_CONFIGURED: review project-specific technical facts:", doc)
                problems.append(doc)
    if not configured_checks():
        print("NOT_CONFIGURED: checks.json requires real verified argv checks")
        problems.append("checks.json")
    git = run(["git", "rev-parse", "--is-inside-work-tree"])
    if git.returncode == 0 and git.stdout.strip() == "true":
        auth = run([sys.executable, str(ROOT / "harness/common/branch_authority.py"), "status"])
        if auth.returncode:
            print("BLOCK: Git branch authority:", (auth.stdout + auth.stderr)[-350:])
            problems.append("branch authority")
    elif (ROOT / ".git").exists():
        print("BLOCK: Git metadata present but unusable")
        problems.append("Git metadata")
    if problems:
        print("AUDIT: BLOCKED; resolve only observed mandatory gaps before lock")
        return 2
    print("AUDIT: SCRIPT_READY (native host and approvals need separate evidence)")
    return 0


def smoke():
    """Run native adapter handlers on a disposable Git fixture; never edit product files."""
    state = read_state()
    if state is None:
        print("SMOKE: LEGACY mode; use installed native preflight and host tests")
        return 2
    runtime = state.get("runtime")
    if runtime not in ("codex", "claude"):
        print("SMOKE: native positive/negative fixtures not provided for", runtime,
              "- host-specific live tests required; no fake PASS")
        return 2
    hook_rel = "harness/" + runtime + "/hook.py"
    hook = ROOT / hook_rel
    if not hook.is_file():
        print("SMOKE: missing adapter:", hook_rel)
        return 2
    with tempfile.TemporaryDirectory(prefix="bootstrap-smoke-") as d:
        dest = pathlib.Path(d) / "project"
        dest.mkdir()
        for relative in ("docs/ARCHITECTURE.md", "docs/CRITERIA.md",
                         "harness/hook-policy.json", "harness/active-task.json",
                         "harness/common/branch_authority.py", "harness/common/snapshot.py",
                         "harness/common/task.py", "harness/common/verify.py",
                         "harness/common/checks.json", hook_rel):
            src = ROOT / relative
            if not src.is_file():
                print("SMOKE: missing", relative)
                return 2
            dst = dest / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        if run(["git", "init"], cwd=dest).returncode:
            print("SMOKE: git unavailable for isolated branch tests")
            return 2
        for args in (["git", "config", "user.name", "Bootstrap Fixture"],
                     ["git", "config", "user.email", "bootstrap@example.invalid"],
                     ["git", "add", "."], ["git", "commit", "-m", "smoke fixture"]):
            result = run(args, cwd=dest)
            if result.returncode:
                print("SMOKE: fixture error:", result.stderr[-350:])
                return 2
        branch = run(["git", "branch", "--show-current"], cwd=dest).stdout.strip()
        config = run([sys.executable, str(dest / "harness/common/branch_authority.py"),
                      "configure", "--active", branch, "--apply"], cwd=dest)
        if config.returncode:
            print("SMOKE: cannot configure isolated branch:", config.stdout[-350:])
            return 2
        if runtime == "codex":
            def hook_call(patch):
                payload = {"hook_event_name": "PreToolUse", "tool_name": "apply_patch",
                           "tool_input": {"command": patch}}
                p = run([sys.executable, str(dest / hook_rel)], cwd=dest, data=json.dumps(payload))
                try:
                    return p.returncode, json.loads(p.stdout)
                except ValueError:
                    return p.returncode, {}
            allowed = hook_call("*** Begin Patch\n*** Update File: docs/ARCHITECTURE.md\n@@\n-absent\n+present\n*** End Patch")
            blocked = hook_call("*** Begin Patch\n*** Add File: ../escape.md\n+bad\n*** End Patch")
            good = allowed[0] == 0 and allowed[1].get("hookSpecificOutput", {}).get("permissionDecision") != "deny"
            bad = blocked[1].get("hookSpecificOutput", {}).get("permissionDecision") == "deny"
        else:
            def hook_call(path):
                payload = {"hook_event_name": "PreToolUse", "tool_name": "Edit",
                           "tool_input": {"file_path": path}}
                return run([sys.executable, str(dest / hook_rel)], cwd=dest, data=json.dumps(payload))
            good = hook_call("docs/ARCHITECTURE.md").returncode == 0
            bad = hook_call("../escape.md").returncode == 2
        print("SMOKE_ALLOW:", "PASS" if good else "FAIL")
        print("SMOKE_DENY:", "PASS" if bad else "FAIL")
        if not (good and bad):
            return 1
    print("SMOKE: SCRIPT_TESTED on isolated clone, NOT real host dispatch")
    return 0


def activate(evidence):
    state = read_state()
    if state is None or state.get("invalid"):
        print("BLOCK: no valid staged setup state")
        return 2
    if state.get("phase") == "READY":
        print("READY: already activated; do not rewrite lock evidence")
        return 0
    if audit() or smoke():
        print("BLOCK: setup audit/smoke incomplete")
        return 2
    path = pathlib.Path(evidence).resolve()
    if not path.is_file() or not path.is_relative_to(ROOT) or path == STATE:
        print("BLOCK: evidence must be an existing file inside project")
        return 2
    try:
        item = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("BLOCK: invalid evidence JSON")
        return 2
    if (not isinstance(item, dict) or item.get("runtime") != state.get("runtime") or
            not isinstance(item.get("host_version"), str) or not item["host_version"].strip() or
            any(item.get(name) is not True for name in
                ("fresh_session", "hook_dispatched", "allow_observed", "deny_observed"))):
        print("BLOCK: observed fresh-host hook evidence missing or mismatched")
        return 2
    if not isinstance(item.get("notes"), str) or not item["notes"].strip():
        print("BLOCK: provide concrete observation notes")
        return 2
    updated = dict(state, phase="READY", evidence_path=str(path.relative_to(ROOT)),
                   evidence_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    temp = STATE.with_name("setup-state.json.new")
    if temp.exists() or temp.is_symlink():
        print("BLOCK: unfinished state transaction")
        return 2
    try:
        temp.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
        temp.replace(STATE)
    finally:
        if temp.exists():
            temp.unlink()
    print("READY: configuration activation recorded; requires POST-LOCK LIVE retest")
    print("MANUAL_COORDINATION ONLY: file evidence does not authenticate human approval")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    choices = p.add_subparsers(dest="action", required=True)
    choices.add_parser("status")
    choices.add_parser("audit")
    choices.add_parser("smoke")
    act = choices.add_parser("activate")
    act.add_argument("--evidence", required=True, help="Manual real-host observation JSON inside the project")
    act.add_argument("--human-approved", action="store_true", help="Affirm an explicit user instruction, not an authenticated signature")
    a = p.parse_args(argv)
    if a.action == "status":
        print(json.dumps(read_state() or {"phase": "LEGACY_NO_STAGED_STATE"}, indent=2))
        return 0
    if a.action == "audit":
        return audit()
    if a.action == "smoke":
        return smoke()
    if not a.human_approved:
        print("BLOCK: require explicit human-approved final lock instruction")
        return 2
    return activate(a.evidence)


if __name__ == "__main__":
    sys.exit(main())
