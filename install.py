#!/usr/bin/env python3
"""Copy-safe, tier- and runtime-aware installer. Python >=3.9, stdlib only."""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent
SOURCE = REPO / "project-template"
MANIFEST = SOURCE / "harness/specs/TIER_MANIFEST.json"
TIERS = ("Lite", "Standard", "Full")
RUNTIMES = ("codex", "claude", "continue")
SKIP = {"README.md", "SETUP.md"}
# Restrict copied artifacts to packaged template sources, never test/build/editor output.
# This explicit filter is applied BEFORE tier/runtime filtering and is independent
# of whether tests ran in this checkout.
RELEASE_ROOTS = {".agents", ".claude", ".codex", ".continue", "docs", "harness", "lessons"}
RELEASE_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "SETUP.md", "TASKS.md", ".gitignore"}
RELEASE_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".json", ".py"}
CACHE_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".nox", ".venv", "venv", "node_modules", "dist", "build",
    ".cache", ".idea", ".vscode",
}
CACHE_NAMES = {".DS_Store", "Thumbs.db", ".coverage"}
CACHE_SUFFIXES = {".pyc", ".pyo", ".pyd", ".swp", ".swo", ".tmp", ".bak"}

def is_release_source(relative):
    parts = relative.parts
    if not parts or any(part in CACHE_DIRS for part in parts):
        return False
    if any(part.startswith(".coverage.") for part in parts):
        return False
    if relative.name in CACHE_NAMES or relative.suffix.lower() in CACHE_SUFFIXES:
        return False
    if relative.name.endswith(("~", ".orig", ".rej")):
        return False
    if len(parts) == 1:
        return relative.name in RELEASE_FILES
    return parts[0] in RELEASE_ROOTS and relative.suffix.lower() in RELEASE_SUFFIXES

LITE_SKILL_EXCLUSIONS = {
    "critical-review", "goal-review", "trace-impact", "plan-task",
    "research-evidence", "brainstorm-theory",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def role_names(tier):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    current = tier
    roles = set()
    visited = set()
    while current:
        if current in visited or current not in manifest["tiers"]:
            raise ValueError("invalid tier manifest inheritance")
        visited.add(current)
        entry = manifest["tiers"][current]
        roles.update(entry["agents"])
        current = entry.get("inherits")
    return roles

def eligible(rel, tier, runtime, roles):
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
        leaf = rel.name
        if tier == "Lite" and leaf in {"GATES.md", "TRACE.md", "REVIEW_LOOP.md", "GIT_ADMIN.md",
                                       "FIXER.md", "HARNESS_SPEC_TEMPLATE.md", "HARNESS_SPEC.md"}:
            return False
        if tier != "Full" and leaf in {"GIT_ADMIN.md", "FIXER.md", "HARNESS_SPEC_TEMPLATE.md"}:
            return False
    if tier == "Lite" and name in {"docs/MILESTONES.md", "docs/TRACE.md", "docs/BACKLOG.md"}:
        return False
    if name.startswith(".agents/roles/") and rel.stem not in roles:
        return False
    if name.startswith((".codex/agents/", ".claude/agents/", ".continue/rules/roles/")) and rel.stem not in roles:
        return False
    if name.startswith(".continue/agents/") and rel.parts[2] not in roles:
        return False
    if tier == "Lite" and name.startswith(".agents/skills/") and rel.parts[2] in LITE_SKILL_EXCLUSIONS:
        return False
    return True

def entries(tier, runtime):
    roles = role_names(tier)
    files = []
    for src in SOURCE.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(SOURCE)
        if is_release_source(rel) and eligible(rel, tier, runtime, roles):
            files.append((src, rel))
            if runtime == "claude" and rel.parts[:2] == (".agents", "skills"):
                files.append((src, pathlib.Path(".claude", "skills", *rel.parts[2:])))
    return sorted(files, key=lambda item: item[1].as_posix())

def confine(root, target):
    """Reject existing symlink/junction ancestors *before* any mkdir or write."""
    relative = target.relative_to(root)
    curr = root
    if curr.is_symlink() or curr.resolve() != root:
        raise ValueError("target root changed")
    for part in relative.parts:
        curr = curr / part
        if curr.is_symlink():
            raise ValueError("symlink in destination: " + str(curr))
        if curr.exists() and not curr.resolve().is_relative_to(root):
            raise ValueError("destination escapes project: " + str(curr))

def classify(root, src, target):
    try:
        confine(root, target)
    except ValueError:
        return "CONFLICT"
    if target.exists():
        if not target.is_file():
            return "CONFLICT"
        return "SAME" if digest(src) == digest(target) else "CONFLICT"
    return "ADD"

def plan(dest, tier, runtime):
    return [(classify(dest, src, dest / rel), src, dest / rel) for src, rel in entries(tier, runtime)]

def safe_copy(root, source, target):
    confine(root, target)
    rel = target.relative_to(root)
    parent = root
    for part in rel.parts[:-1]:
        parent = parent / part
        confine(root, parent)
        if not parent.exists():
            parent.mkdir()  # one level only; no mkdir outside validated parents
        confine(root, parent)
        if not parent.is_dir():
            raise ValueError("destination parent is not a directory")
    confine(root, target)
    with target.open("xb") as output, source.open("rb") as input_file:
        shutil.copyfileobj(input_file, output)

def main():
    ap = argparse.ArgumentParser(description="Safe template install, dry-run by default.")
    ap.add_argument("--target", required=True)
    ap.add_argument("--tier", choices=TIERS, default="Standard")
    ap.add_argument("--runtime", choices=RUNTIMES, default="codex")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dest = pathlib.Path(args.target).expanduser().resolve()
    if not dest.is_dir() or dest == REPO or REPO in dest.parents or dest in REPO.parents:
        ap.error("target must be an existing project outside the bootstrap checkout")
    try:
        ops = plan(dest, args.tier, args.runtime)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("NOT_CONFIGURED: invalid manifest/source:", exc)
        return 2
    for state, source, target in ops:
        print(state, target.relative_to(dest).as_posix())
    conflicts = [target for state, _, target in ops if state == "CONFLICT"]
    merge = (dest / "AGENTS.md") in conflicts and (dest / "AGENTS.md").is_file()
    summary = {k: sum(x[0] == k for x in ops) for k in ("ADD", "SAME", "CONFLICT")}
    print("SUMMARY:", json.dumps(dict(tier=args.tier, runtime=args.runtime, **summary), sort_keys=True))
    if merge:
        print("MERGE_REQUIRED: existing AGENTS.md retained; review AGENTS.bootstrap.md")
    if not args.apply:
        return 2 if conflicts else 0
    # Preflight every destination before any write, including AGENTS merge candidate.
    try:
        for _, _, target in ops:
            confine(dest, target)
        if merge:
            confine(dest, dest / "AGENTS.bootstrap.md")
    except ValueError as exc:
        print("BLOCK: unsafe destination:", exc)
        return 2
    try:
        if merge:
            candidate = dest / "AGENTS.bootstrap.md"
            if not candidate.exists():
                safe_copy(dest, SOURCE / "AGENTS.md", candidate)
                print("EXPORTED: AGENTS.bootstrap.md")
            elif digest(candidate) != digest(SOURCE / "AGENTS.md"):
                print("CONFLICT: existing AGENTS.bootstrap.md retained")
        for state, source, target in ops:
            if state == "ADD":
                safe_copy(dest, source, target)
    except (OSError, ValueError) as exc:
        print("ERROR: incomplete non-destructive install; inspect newly added files:", exc)
        return 1
    print("APPLIED: new files only" if not conflicts else "APPLIED_WITH_CONFLICTS: merge/reconcile required")
    return 2 if conflicts else 0

if __name__ == "__main__":
    sys.exit(main())
