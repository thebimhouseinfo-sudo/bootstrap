#!/usr/bin/env python3
"""Non-overwriting, tier/runtime-aware installer. Python >=3.9, stdlib only."""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys

SOURCE = pathlib.Path(__file__).resolve().parent / "project-template"
SKIP = {"README.md", "SETUP.md"}
TIERS = ("Lite", "Standard", "Full")
RUNTIMES = ("codex", "claude", "continue")
AGENT_BASE = {"coder", "reviewer"}
AGENT_STANDARD = {"planner", "tester", "critic"}
AGENT_FULL = {"harness-fixer"}
INDEPENDENT = {"explorer"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def names_for(tier):
    result = set(AGENT_BASE)
    if tier in ("Standard", "Full"):
        result |= AGENT_STANDARD
    if tier == "Full":
        result |= AGENT_FULL
    return result

def eligible(rel, tier, runtime):
    name = rel.as_posix()
    if name in SKIP:
        return False
    if name.startswith(".codex/") and runtime != "codex":
        return False
    if (name.startswith(".claude/") or name == "CLAUDE.md") and runtime != "claude":
        return False
    if name.startswith(".continue/") and runtime != "continue":
        return False
    if name.startswith("harness/codex/") and runtime != "codex":
        return False
    if name.startswith("harness/specs/") or name == "harness/HARNESS_SPEC.md":
        # Specifications are inert; install tier-relevant ones, do not install Full-only fixer.
        leaf = rel.name
        if tier == "Lite" and leaf in {"GATES.md", "TRACE.md", "REVIEW_LOOP.md", "GIT_ADMIN.md", "FIXER.md", "HARNESS_SPEC_TEMPLATE.md", "HARNESS_SPEC.md"}:
            return False
        if tier != "Full" and leaf in {"GIT_ADMIN.md", "FIXER.md", "HARNESS_SPEC_TEMPLATE.md"}:
            return False
    if name in {"docs/MILESTONES.md", "docs/TRACE.md", "docs/BACKLOG.md"} and tier == "Lite":
        return False
    if name.startswith(".agents/roles/"):
        stem = rel.stem
        if stem != "README" and stem not in names_for(tier):
            return False
    if name.startswith(".codex/agents/") or name.startswith(".claude/agents/") or name.startswith(".continue/rules/roles/"):
        stem = rel.stem
        if stem not in names_for(tier):
            return False
    if name.startswith(".agents/skills/") and tier == "Lite":
        if rel.parent.name in {"critical-review", "goal-review", "trace-impact", "plan-task", "research-evidence", "brainstorm-theory"}:
            return False
    return True

def entries(tier, runtime):
    return sorted((p for p in SOURCE.rglob("*") if p.is_file() and eligible(p.relative_to(SOURCE), tier, runtime)), key=str)

def plan(dest, tier, runtime):
    operations = []
    for source in entries(tier, runtime):
        rel = source.relative_to(SOURCE)
        destination = dest / rel
        if destination.is_symlink() or (destination.exists() and not destination.is_file()):
            status = "CONFLICT"
        elif destination.is_file():
            status = "SAME" if digest(source) == digest(destination) else "CONFLICT"
        else:
            status = "ADD"
        operations.append((status, source, destination))
    return operations

def safe_copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or any(part.is_symlink() for part in (target.parent, *target.parents) if part != target.anchor):
        raise FileExistsError("symlink in destination path")
    with target.open("xb") as out, source.open("rb") as src:
        shutil.copyfileobj(src, out)

def main():
    parser = argparse.ArgumentParser(description="Safe project-template installation (dry run by default)")
    parser.add_argument("--target", required=True, help="existing target project root")
    parser.add_argument("--tier", choices=TIERS, default="Standard")
    parser.add_argument("--runtime", choices=RUNTIMES, default="codex")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    destination = pathlib.Path(args.target).expanduser().resolve()
    if not destination.is_dir() or not SOURCE.is_dir() or destination == SOURCE or SOURCE in destination.parents:
        parser.error("target must be an existing directory outside source templates")
    operations = plan(destination, args.tier, args.runtime)
    conflicts = []
    for status, source, target in operations:
        print(status, source.relative_to(SOURCE).as_posix())
        if status == "CONFLICT":
            conflicts.append(target.relative_to(destination).as_posix())
    # Existing AGENTS.md is never overwritten. Export a manual merge candidate.
    original = destination / "AGENTS.md"
    candidate = destination / "AGENTS.bootstrap.md"
    needs_merge = original.is_file() and "AGENTS.md" in conflicts
    if needs_merge:
        print("MERGE_REQUIRED: inspect AGENTS.bootstrap.md and merge into existing AGENTS.md manually")
        if args.apply:
            try:
                safe_copy(SOURCE / "AGENTS.md", candidate)
                print("EXPORTED: AGENTS.bootstrap.md")
            except FileExistsError:
                print("MERGE_CANDIDATE_EXISTS: AGENTS.bootstrap.md preserved")
            except OSError as exc:
                print("ERROR: cannot export merge candidate:", exc)
                return 1
    summary = {s: sum(x[0] == s for x in operations) for s in ("ADD", "SAME", "CONFLICT")}
    print("SUMMARY:", json.dumps({"tier":args.tier, "runtime":args.runtime, **summary}, sort_keys=True))
    if not args.apply:
        return 2 if conflicts else 0
    # No silent success when conflicted instructions might not have been activated.
    try:
        for status, source, target in operations:
            if status == "ADD":
                safe_copy(source, target)
        print("APPLIED: new files only; existing contents preserved")
    except (OSError, FileExistsError) as exc:
        print("ERROR: partial non-destructive install, inspect target:", exc)
        return 1
    return 2 if conflicts else 0

if __name__ == "__main__":
    sys.exit(main())
