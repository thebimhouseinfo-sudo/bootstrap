#!/usr/bin/env python3
"""Copy-safe, tier- and runtime-aware installer. Python >=3.9, stdlib only."""
import argparse
import hashlib
import json
import pathlib
import os
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent
SOURCE = REPO / "project-template"
MANIFEST = SOURCE / "harness/specs/TIER_MANIFEST.json"
TIERS = ("Lite", "Standard", "Full")
RUNTIMES = ("antigravity", "codex", "claude", "continue")
SKIP = {"README.md", "SETUP.md"}
# Restrict copied artifacts to packaged template sources, never test/build/editor output.
# This explicit filter is applied BEFORE tier/runtime filtering and is independent
# of whether tests ran in this checkout.
RELEASE_ROOTS = {".agents", ".antigravity", ".claude", ".codex", ".continue", "docs", "harness", "lessons"}
RELEASE_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "SETUP.md", "TASKS.md", ".gitignore"}
RELEASE_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".json", ".py", ".gitkeep"}
CACHE_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".nox", ".venv", "venv", "node_modules", "dist", "build",
    ".cache", ".idea", ".vscode",
}
CACHE_NAMES = {".DS_Store", "Thumbs.db", ".coverage"}
CACHE_SUFFIXES = {".pyc", ".pyo", ".pyd", ".swp", ".swo", ".tmp", ".bak"}

# Applied to installed projects only. Do not put these rules in the canonical
# template's own .gitignore: the template is distributable source in this repo.
LOCAL_SETUP_PATHS = (
    ".agents/", ".antigravity/", ".codex/", ".claude/", ".continue/", "harness/", "lessons/",
    "AGENTS.md", "AGENTS.bootstrap.md", "CLAUDE.md", "TASKS.md",
    "docs/PROJECT_PROFILE.md", "docs/TRACE.md",
    "docs/reports/_TEMPLATE.md", "docs/reports/_REVIEW_TEMPLATE.md",
)
IGNORE_START = b"# BEGIN bootstrap local agent setup"
IGNORE_END = b"# END bootstrap local agent setup"


def ignored_setup_bytes(original):
    """Keep product rules verbatim; put one managed local-only block last."""
    lines = original.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == IGNORE_START]
    ends = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == IGNORE_END]
    if starts or ends:
        if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
            raise ValueError("ambiguous .gitignore managed block; preserve and reconcile manually")
        original = b"".join(lines[:starts[0]] + lines[ends[0]+1:])
    newline = b"\r\n" if b"\r\n" in original else b"\n"
    if original and not original.endswith(b"\n"):
        original += newline
    block = [IGNORE_START, b"# Local agent configuration/state; product source and docs remain trackable."]
    block.extend(("/" + path).encode("ascii") for path in LOCAL_SETUP_PATHS)
    return original + newline.join(block + [IGNORE_END, b""])


def ignore_contents(root, source):
    target = root / ".gitignore"
    confine(root, target)
    if target.exists() and not target.is_file():
        raise ValueError(".gitignore must be a regular file")
    return ignored_setup_bytes(target.read_bytes() if target.exists() else source.read_bytes())


def write_ignore(root, source):
    target = root / ".gitignore"
    confine(root, target)
    before = target.read_bytes() if target.exists() else None
    rendered = ignore_contents(root, source)
    if before == rendered:
        return
    if before is None:
        with target.open("xb") as output:
            output.write(rendered)
        return
    # Replace only this explicitly managed file, after checking concurrent edits.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(root), prefix=".gitignore.bootstrap-",
                                         suffix=".tmp", delete=False) as output:
            temporary = pathlib.Path(output.name)
            output.write(rendered)
        os.chmod(temporary, target.stat().st_mode & 0o777)
        confine(root, target)
        if target.read_bytes() != before:
            raise ValueError(".gitignore changed during install; retry preview")
        temporary.replace(target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def git_worktree(root):
    if not shutil.which("git"):
        print("GIT_INDEX: UNVERIFIED (git unavailable)")
        return False
    probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
                           capture_output=True, timeout=10)
    if probe.returncode == 0 and probe.stdout.strip() == b"true":
        return True
    markers = [(parent / ".git") for parent in (root, *root.parents)]
    if (probe.returncode == 0 or any(p.exists() or p.is_symlink() for p in markers)
            or os.environ.get("GIT_DIR") or os.environ.get("GIT_WORK_TREE")):
        raise ValueError("cannot inspect Git repository; check access, ownership and metadata integrity")
    return False


def tracked_local_setup(root):
    """Inspect the real index; ignore rules cannot hide already tracked files."""
    if not git_worktree(root):
        return []
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--",
                             *[path.rstrip("/") for path in LOCAL_SETUP_PATHS]],
                            capture_output=True, timeout=15)
    if result.returncode:
        raise ValueError("cannot inspect Git index for tracked local setup")
    return sorted(set(os.fsdecode(path) for path in result.stdout.split(b"\0") if path))


def exposed_local_setup(root):
    """Use Git's actual rule precedence, including nested .gitignore exceptions."""
    if not git_worktree(root):
        return []
    probes = {path + "__bootstrap_local_probe__" if path.endswith("/") else path: path
              for path in LOCAL_SETUP_PATHS}
    result = subprocess.run(["git", "-C", str(root), "check-ignore", "--no-index", "-z", "--stdin"],
                            input=b"\0".join(os.fsencode(p) for p in probes) + b"\0",
                            capture_output=True, timeout=15)
    if result.returncode not in (0, 1):
        raise ValueError("cannot verify effective Git ignore rules")
    ignored = {os.fsdecode(p) for p in result.stdout.split(b"\0") if p}
    return sorted(probes[path] for path in probes.keys() - ignored)

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
    if name in {".agents/hooks.json", ".agents/MODEL_SELECTION.md"} and runtime != "antigravity":
        return False
    if name.startswith(".antigravity/agents/") and rel.stem not in roles:
        return False
    if name.startswith(".antigravity/") and runtime != "antigravity":
        return False
    if name.startswith(".codex/") and runtime != "codex":
        return False
    if (name.startswith(".claude/") or name == "CLAUDE.md") and runtime != "claude":
        return False
    if name.startswith(".continue/") and runtime != "continue":
        return False
    if name.startswith("harness/codex/") and runtime != "codex":
        return False
    if name.startswith("harness/claude/") and runtime != "claude":
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
        if src.is_symlink() or not src.is_file() or any(parent.is_symlink() for parent in src.parents if parent != SOURCE.parent):
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
    ops = []
    for src, rel in entries(tier, runtime):
        target = dest / rel
        if rel.as_posix() == ".gitignore":
            # Existing product rules are mergeable; unsafe or malformed files raise.
            rendered = ignore_contents(dest, src)
            state = ("SAME" if target.read_bytes() == rendered else "UPDATE") if target.exists() else "ADD"
        else:
            state = classify(dest, src, target)
        ops.append((state, src, target))
    return ops

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

def pre_ask_summary(dest, tier, runtime):
    """Return structured pre-ask configuration summary."""
    try:
        is_git = git_worktree(dest) if dest.is_dir() else False
        git_desc = "Git worktree verified" if is_git else "No Git worktree (local-only directory)"
    except Exception:
        git_desc = "Git repository inspection unverified or corrupt"
    try:
        roles = role_names(tier)
        roles_str = f"{tier} ({', '.join(sorted(roles))})"
    except Exception:
        roles_str = tier
    model_policy = "Antigravity native (all fallbacks -> Gemini 3.8 Flash High)" if runtime == "antigravity" else f"{runtime} role presets"
    return {
        "target": dest.as_posix(),
        "tier": roles_str,
        "runtime": f"{runtime} ({'Google Antigravity IDE' if runtime == 'antigravity' else runtime})",
        "git_status": git_desc,
        "model_policy": model_policy,
        "local_protection": "Managed .gitignore block for .agents, .antigravity, harness",
        "report_language": "Vietnamese documentation, English commands/IDs",
        "approval_channel": "UI buttons / terminal commands (no silent execution)",
    }


def print_pre_ask_block(dest, tier, runtime):
    """Display the pre-ask configuration block (Step 0 / Buoc 0) before plan and install."""
    info = pre_ask_summary(dest, tier, runtime)
    print("=" * 72)
    print("PRE-ASK CONFIGURATION / KHOI CAU HINH TRUOC (Buoc 0)")
    print("=" * 72)
    print(f"  [1] Target Directory : {info['target']}")
    print(f"  [2] Tier             : {info['tier']}")
    print(f"  [3] Runtime          : {info['runtime']}")
    print(f"  [4] Git Status       : {info['git_status']}")
    print(f"  [5] Model Policy     : {info['model_policy']}")
    print(f"  [6] Local Protection : {info['local_protection']}")
    print(f"  [7] Report Language  : {info['report_language']}")
    print(f"  [8] Approval Channel : {info['approval_channel']}")
    print("=" * 72)


def prompt_choice(prompt_text, choices, default):
    choice_str = "/".join(f"[{c}]" if c == default else c for c in choices)
    while True:
        try:
            val = input(f"{prompt_text} ({choice_str}): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(1)
        if not val:
            if default is not None:
                return default
            print("Please select a runtime explicitly.")
            continue
        for c in choices:
            if val.lower() == c.lower():
                return c
        print(f"Invalid choice '{val}'. Choose from: {', '.join(choices)}")


def prompt_target(default=None):
    prompt_str = f"Target project directory [{default}]: " if default else "Target project directory: "
    while True:
        try:
            val = input(prompt_str).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(1)
        if not val and default:
            val = default
        if val:
            dest = pathlib.Path(val).expanduser().resolve()
            if not dest.is_dir():
                print(f"Directory does not exist: {dest}")
                continue
            if dest == REPO or REPO in dest.parents or dest in REPO.parents:
                print("Target must be an existing project outside the bootstrap checkout.")
                continue
            return dest


def prompt_confirm(prompt_text, default=False):
    suffix = "[Y/n]" if default else "[y/N]"
    try:
        val = input(f"{prompt_text} {suffix}: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)
    if not val:
        return default
    return val in ("y", "yes")


def main():
    ap = argparse.ArgumentParser(description="Safe template install, dry-run by default.")
    ap.add_argument("--target", help="Target project directory")
    ap.add_argument("--tier", choices=TIERS, default="Standard", help="Template tier (Lite, Standard, Full)")
    ap.add_argument("--runtime", choices=RUNTIMES, default=None, help="Agent runtime (antigravity, codex, claude, continue)")
    ap.add_argument("--ask-first", action="store_true", help="Run interactive pre-ask configuration block before installing")
    ap.add_argument("--apply", action="store_true", help="Apply template installation (write files)")
    ap.add_argument("-y", "--yes", action="store_true", help="Skip interactive confirmation on apply")
    args = ap.parse_args()

    is_interactive = sys.stdin.isatty()
    ask_first_mode = args.ask_first or (is_interactive and not args.target and not args.apply)

    if not args.target:
        if ask_first_mode or is_interactive:
            dest = prompt_target()
        else:
            ap.error("the following arguments are required: --target")
    else:
        dest = pathlib.Path(args.target).expanduser().resolve()

    if args.ask_first and not is_interactive:
        ap.error("--ask-first requires an interactive terminal; pass --runtime explicitly for automation")

    if not dest.is_dir() or dest == REPO or REPO in dest.parents or dest in REPO.parents:
        ap.error("target must be an existing project outside the bootstrap checkout")

    tier = args.tier
    runtime = args.runtime

    if ask_first_mode and is_interactive:
        print("\n--- CAU HINH CAI DAT (PRE-ASK CONFIGURATION) ---")
        tier = prompt_choice("Chon Tang (Tier)", TIERS, default=args.tier)
        runtime = prompt_choice("Chon Runtime", RUNTIMES, default=args.runtime)

    if runtime is None:
        ap.error("select --runtime explicitly (antigravity/codex/claude/continue) or use --ask-first")

    # Print the pre-ask configuration block upfront before any inspection or changes
    print_pre_ask_block(dest, tier, runtime)

    try:
        ops = plan(dest, tier, runtime)
        tracked = tracked_local_setup(dest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print("NOT_CONFIGURED: invalid source, ignore policy or Git index:", exc)
        return 2
    for state, source, target in ops:
        print(state, target.relative_to(dest).as_posix())
    conflicts = [target for state, _, target in ops if state == "CONFLICT"]
    merge = (dest / "AGENTS.md") in conflicts and (dest / "AGENTS.md").is_file()
    summary = {k: sum(x[0] == k for x in ops) for k in ("ADD", "SAME", "UPDATE", "CONFLICT")}
    print("SUMMARY:", json.dumps(dict(tier=tier, runtime=runtime, **summary), sort_keys=True))
    if merge:
        print("MERGE_REQUIRED: existing AGENTS.md retained; review AGENTS.bootstrap.md")
    for name in tracked:
        print("TRACKED_LOCAL_SETUP:", name)
    if tracked:
        print("PRIVACY_REVIEW_REQUIRED: .gitignore does not untrack existing index entries; no files/index entries removed")

    if not args.apply and not ask_first_mode:
        return 2 if conflicts or tracked else 0

    if ask_first_mode:
        if conflicts or tracked:
            print("\nCANH BAO: Phat hien xung dot hoac file da duoc Git theo doi.")
        if not prompt_confirm(f"Tien hanh cai dat (apply) vao thu muc '{dest}'?", default=False):
            print("ABORTED: Qua trinh cai dat bi huy boi nguoi dung.")
            return 2 if conflicts or tracked else 0
    elif args.apply and is_interactive and not args.yes:
        if not prompt_confirm(f"Xac nhan cai dat template vao '{dest}'?", default=True):
            print("ABORTED: Cai dat bi huy.")
            return 2 if conflicts or tracked else 0

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
        ignore_op = next(op for op in ops if op[2].name == ".gitignore")
        if ignore_op[0] == "CONFLICT":
            raise ValueError("cannot safely install local-only .gitignore policy")
        write_ignore(dest, ignore_op[1])
        exposed = exposed_local_setup(dest)
        if exposed:
            for name in exposed:
                print("LOCAL_SETUP_NOT_IGNORED:", name)
            print("BLOCK: reconcile nested Git ignore exceptions before installing local setup")
            return 2
        if merge:
            candidate = dest / "AGENTS.bootstrap.md"
            if not candidate.exists():
                safe_copy(dest, SOURCE / "AGENTS.md", candidate)
                print("EXPORTED: AGENTS.bootstrap.md")
            elif digest(candidate) != digest(SOURCE / "AGENTS.md"):
                print("CONFLICT: existing AGENTS.bootstrap.md retained")
        for state, source, target in ops:
            if state == "ADD" and target.name != ".gitignore":
                safe_copy(dest, source, target)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print("ERROR: incomplete non-destructive install; inspect newly added files:", exc)
        return 1
    print("APPLIED: new files and local-only ignore policy" if not conflicts else "APPLIED_WITH_CONFLICTS: merge/reconcile required")
    return 2 if conflicts or tracked else 0

if __name__ == "__main__":
    sys.exit(main())

