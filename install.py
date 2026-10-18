#!/usr/bin/env python3
"""Copy-safe, tier- and runtime-aware installer. Python >=3.9, stdlib only."""
import argparse
import hashlib
import json
import pathlib
import re
import os
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent
SOURCE = REPO / "project-template"
MANIFEST = SOURCE / "harness/specs/TIER_MANIFEST.json"
TIERS = ("Lite", "Standard", "Full")
RUNTIMES = ("antigravity", "codex", "claude", "continue", "generic")
SKIP = {"README.md", "SETUP.md"}
# Restrict copied artifacts to packaged template sources, never test/build/editor output.
# This explicit filter is applied BEFORE tier/runtime filtering and is independent
# of whether tests ran in this checkout.
RELEASE_ROOTS = {".agents", ".antigravity", ".claude", ".codex", ".continue", ".generic", "docs", "harness", "lessons"}
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
    ".agents/", ".antigravity/", ".codex/", ".claude/", ".continue/", ".generic/", "harness/", "lessons/",
    "AGENTS.md", "AGENTS.bootstrap.md", "CLAUDE.md", "TASKS.md",
    "docs/PROJECT_PROFILE.md", "docs/TRACE.md",
    "docs/reports/_TEMPLATE.md", "docs/reports/_REVIEW_TEMPLATE.md",
)
STATE_PATHS = (
    "harness/chat-journal.jsonl", "harness/decisions.jsonl",
    "harness/approvals.jsonl", "harness/state.json",
    "harness/last-block.json", "harness/inbox.html",
    "harness/snapshots/", "harness/requests/",
    "docs/TRACE.md", ".claude/settings.local.json",
    "harness/setup-state.json", "harness/setup-live-evidence.json",
    "harness/setup-postlock-evidence.json", "harness/setup-intake.json", "harness/recovery-backups/",
)

IGNORE_START = b"# BEGIN bootstrap local agent setup"
IGNORE_END = b"# END bootstrap local agent setup"


def ignored_paths(mode):
    if mode not in ("local", "tracked"):
        raise ValueError("invalid Git config mode")
    return STATE_PATHS if mode == "tracked" else LOCAL_SETUP_PATHS


def existing_mode(root):
    path = root / ".gitignore"
    if not path.is_file():
        return None
    data = path.read_bytes()
    if IGNORE_START not in data:
        return None
    match = re.search(rb"^# mode: (local|tracked)\r?$", data, re.M)
    return match.group(1).decode("ascii") if match else "local"


def ignored_setup_bytes(original, mode):
    """Keep product rules verbatim; put one managed block last."""
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
    block = [IGNORE_START, b"# mode: " + mode.encode("ascii"),
             b"# Local agent configuration/state; product source and docs remain trackable."]
    block.extend(("/" + path).encode("ascii") for path in ignored_paths(mode))
    return original + newline.join(block + [IGNORE_END, b""])


def ignore_contents(root, source, mode):
    target = root / ".gitignore"
    confine(root, target)
    if target.exists() and not target.is_file():
        raise ValueError(".gitignore must be a regular file")
    return ignored_setup_bytes(target.read_bytes() if target.exists() else source.read_bytes(), mode)


def write_ignore(root, source, mode):
    target = root / ".gitignore"
    confine(root, target)
    before = target.read_bytes() if target.exists() else None
    rendered = ignore_contents(root, source, mode)
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


def tracked_local_setup(root, mode):
    """Inspect the real index; ignore rules cannot hide already tracked files."""
    if not git_worktree(root):
        return []
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--",
                             *[path.rstrip("/") for path in ignored_paths(mode)]],
                            capture_output=True, timeout=15)
    if result.returncode:
        raise ValueError("cannot inspect Git index for tracked local setup")
    return sorted(set(os.fsdecode(path) for path in result.stdout.split(b"\0") if path))


def exposed_local_setup(root, mode):
    """Use Git's actual rule precedence, including nested .gitignore exceptions."""
    if not git_worktree(root):
        return []
    probes = {path + "__bootstrap_local_probe__" if path.endswith("/") else path: path
              for path in ignored_paths(mode)}
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
    return parts[0] in RELEASE_ROOTS and (relative.name == ".gitkeep" or relative.suffix.lower() in RELEASE_SUFFIXES)

LITE_SKILL_EXCLUSIONS = {
    "critical-review", "goal-review", "trace-impact", "plan-task",
    "research-evidence", "brainstorm-theory",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


BOOTSTRAP_MANIFEST = "harness/.bootstrap-manifest.json"


def read_install_manifest(dest):
    target = dest / BOOTSTRAP_MANIFEST
    confine(dest, target)
    if not target.exists():
        return None
    if not target.is_file():
        raise ValueError("bootstrap manifest is not a regular file")
    try:
        manifest = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("invalid bootstrap manifest: " + str(exc)) from exc
    if (not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or
            not isinstance(manifest.get("files"), dict)):
        raise ValueError("unsupported bootstrap manifest; review it before upgrading")
    for name, record in manifest["files"].items():
        if (not isinstance(name, str) or not name or name.startswith("/") or
                any(x in (".", "..") for x in pathlib.PurePosixPath(name).parts) or
                not isinstance(record, dict) or
                not isinstance(record.get("installed_sha256"), str) or
                not re.fullmatch(r"[a-f0-9]{64}", record["installed_sha256"])):
            raise ValueError("invalid bootstrap manifest file record")
    return manifest


def write_install_manifest(dest, content, previous=None):
    target = dest / BOOTSTRAP_MANIFEST
    confine(dest, target)
    target.parent.mkdir(parents=True, exist_ok=True)
    new = (json.dumps(content, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if previous == new:
        return
    if previous is None:
        with target.open("xb") as output:
            output.write(new)
        return
    if target.read_bytes() != previous:
        raise ValueError("bootstrap manifest changed during install")
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(target.parent), prefix=".manifest-", delete=False) as output:
            temp = pathlib.Path(output.name)
            output.write(new)
        confine(dest, target)
        if target.read_bytes() != previous:
            raise ValueError("bootstrap manifest changed during install")
        temp.replace(target)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def replace_managed_file(dest, src, target, recorded_sha):
    """Explicit upgrade only; preserve modified local copies as CONFLICT."""
    confine(dest, target)
    if not target.is_file() or digest(target) != recorded_sha:
        raise ValueError("upgrade conflict: target differs from previous manifest")
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(target.parent), prefix=".bootstrap-upgrade-", delete=False) as out:
            temp = pathlib.Path(out.name)
            with src.open("rb") as source:
                shutil.copyfileobj(source, out)
        os.chmod(temp, target.stat().st_mode & 0o777)
        if digest(target) != recorded_sha:
            raise ValueError("upgrade conflict: target changed during install")
        temp.replace(target)
    finally:
        if temp is not None and temp.exists():
            temp.unlink()


def rollback_install(dest, added, replaced, ignore_before, ignore_after, state_created,
                     manifest_before, manifest_written):
    """Best effort, content-aware rollback; never overwrite concurrent modifications."""
    print("ROLLBACK: attempting restore of this transaction only")
    for target, previous, expected in reversed(replaced):
        try:
            confine(dest, target)
            if target.is_file() and digest(target) == expected:
                target.write_bytes(previous)
                print("ROLLBACK_RESTORED:", target.relative_to(dest))
            else:
                print("ROLLBACK_MANUAL:", target.relative_to(dest), "changed concurrently")
        except OSError as exc:
            print("ROLLBACK_MANUAL:", target.relative_to(dest), exc)
    for target, expected in reversed(added):
        try:
            confine(dest, target)
            if target.is_file() and digest(target) == expected:
                target.unlink()
                print("ROLLBACK_REMOVED:", target.relative_to(dest))
            else:
                print("ROLLBACK_MANUAL:", target.relative_to(dest), "content differs")
        except OSError as exc:
            print("ROLLBACK_MANUAL:", target.relative_to(dest), exc)
    state_path = dest / "harness/setup-state.json"
    if state_created is not None and state_path.is_file():
        try:
            if state_path.read_bytes() == state_created:
                state_path.unlink()
                print("ROLLBACK_REMOVED: harness/setup-state.json")
        except OSError as exc:
            print("ROLLBACK_MANUAL: setup-state.json", exc)
    if manifest_written:
        path = dest / BOOTSTRAP_MANIFEST
        try:
            if path.is_file() and path.read_bytes() == manifest_written:
                if manifest_before is None:
                    path.unlink()
                else:
                    path.write_bytes(manifest_before)
                print("ROLLBACK_RESTORED:", BOOTSTRAP_MANIFEST)
        except OSError as exc:
            print("ROLLBACK_MANUAL: manifest", exc)
    ignore = dest / ".gitignore"
    try:
        if ignore.is_file() and ignore.read_bytes() == ignore_after:
            if ignore_before is None:
                ignore.unlink()
            else:
                ignore.write_bytes(ignore_before)
            print("ROLLBACK_RESTORED: .gitignore")
        else:
            print("ROLLBACK_MANUAL: .gitignore changed concurrently")
    except OSError as exc:
        print("ROLLBACK_MANUAL: .gitignore", exc)


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
    if name.startswith(".generic/") and runtime != "generic":
        return False
    if name.startswith(".generic/agents/") and rel.stem not in roles:
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

def plan(dest, tier, runtime, mode, upgrade=False, previous=None):
    ops = []
    for src, rel in entries(tier, runtime):
        target = dest / rel
        if rel.as_posix() == ".gitignore":
            # Existing product rules are mergeable; unsafe or malformed files raise.
            rendered = ignore_contents(dest, src, mode)
            state = ("SAME" if target.read_bytes() == rendered else "UPDATE") if target.exists() else "ADD"
        else:
            state = classify(dest, src, target)
            if state == "CONFLICT" and upgrade and previous:
                recorded = previous["files"].get(rel.as_posix())
                if recorded and target.is_file() and digest(target) == recorded["installed_sha256"]:
                    state = "UPGRADE"
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
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(target.parent), prefix=".bootstrap-copy-",
                                         delete=False) as output, source.open("rb") as input_file:
            temporary = pathlib.Path(output.name)
            shutil.copyfileobj(input_file, output)
        os.chmod(temporary, source.stat().st_mode & 0o777)
        confine(root, target)
        # Link creation fails if a concurrent writer created the destination; never truncate it.
        os.link(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()

def print_setup_questions():
    """Developer-only question reference. Native host dialog must capture actual answers."""
    print("PRE-ASK / ONE-BATCH SETUP QUESTIONS (DEVELOPER REFERENCE, NOT USER UI)")
    print("1. Target project directory and existing/new code? [required]")
    print("2. Tier: Lite / Standard (default) / Full?")
    print("3. Coding host: Codex / Antigravity / Claude Code / Continue / Other (generic)?")
    print("   If Other: exact app/client + version? e.g. Cline, Qwen Code, DeepSeek-based client.")
    print("   DeepSeek model/provider alone is NOT an IDE; identify the actual client.")
    print("4. OS, shell, Git remote, HUMAN-selected active development and frozen branches?")
    print("5. Product type, actual host/SDK/dialect, existing approved CRITERIA and stack?")
    print("6. Verified build/test/host tools, accounts/devices? No invented commands.")
    print("7. Provider/model: retain working native presets, or choose available model?")
    print("   Continue: provider/model selection needed; native role configs already exist.")
    print("8. Reporting language and approval channel/preferences?")
    print("9. Keep harness configuration local (default), or track it in Git?")
    print("   Approvals remain local and are supported for one Human only.")
    print("IDE: use native dialog. CLI: use numbered terminal selection/menu.")
    print("If CLI host has no selector: use harness/common/setup_intake.py with a real TTY.")
    print("Keep responses in local harness/setup-intake.json for trace.")
    print("Permission prompts are distinct; then preview and request --apply approval.")
    print("No files have been inspected or changed.")


def print_pre_ask_block(dest, tier, runtime, target_app, mode):
    """Display confirmed CLI package selection, not invented project answers."""
    print("=" * 72)
    print("INSTALL PREVIEW CONFIGURATION (EXPLICIT CLI CHOICES)")
    print("  Target Directory :", dest)
    print("  Tier             :", tier)
    print("  Runtime          :", runtime)
    print("  Config in Git    :", mode)
    if mode == "tracked":
        print("  ALWAYS_LOCAL     :", ", ".join(STATE_PATHS))
        print("  WARNING          : approvals are local and do not support multiple Humans")
    if runtime == "generic":
        print("  Target app/client:", target_app)
        print("  Porting status   : portable roles + guide; native adapter NOT INSTALLED")
    if runtime == "continue":
        print("  Continue model   : must configure actual provider/models")
        print("  Shared core      : same .agents roles/skills and Python helpers as Antigravity")
        print("  Native differences: Continue configs/rules, not Antigravity agent/hooks files")
    print("  Product settings : NOT_CONFIGURED by template; verify per-project facts")
    print("  Apply            : explicit --apply after approval (no terminal survey)")
    print("=" * 72)


def main():
    ap = argparse.ArgumentParser(description="Safe tier/runtime package install (preview by default).")
    ap.add_argument("--target", help="Existing target project directory")
    ap.add_argument("--tier", choices=TIERS, default="Standard")
    ap.add_argument("--runtime", choices=RUNTIMES, help="Explicit coding client or portable generic")
    ap.add_argument("--target-app", help="With --runtime generic: actual target host name, e.g. cline/qwen-code/deepseek/other")
    ap.add_argument("--ask-first", action="store_true", help="Print developer-only setup question reference; NOT a native dialog")
    ap.add_argument("--apply", action="store_true", help="Apply scoped file installation after Human approval")
    ap.add_argument("--staged", action="store_true", help="First-time safe setup, defer blocking hooks until actual verification")
    ap.add_argument("--upgrade", action="store_true", help="Explicitly update only previously manifest-owned, unmodified files")
    ap.add_argument("--config-git", choices=("local", "tracked"), default="local",
                    help="Keep agent setup local (default) or track configuration in Git")
    ap.add_argument("--change-config-git", action="store_true",
                    help="Explicitly allow changing the existing managed Git configuration mode")
    ap.add_argument("-y", "--yes", action="store_true", help="Ignored compatibility flag; does NOT enable --apply")
    args = ap.parse_args()
    if args.yes:
        print("IGNORED_FLAG: -y/--yes does not enable --apply or skip approval")

    # Human answers come from the host-native dialog, NOT chat or permission prompts.
    # --ask-first prints a developer reference; it never opens a user-facing dialog.
    if args.ask_first:
        if args.apply:
            ap.error("--ask-first is questions-only and cannot be combined with --apply")
        print_setup_questions()
        return 0
    if not args.target:
        ap.error("--target is required; run --ask-first for all setup questions")
    if not args.runtime:
        ap.error("--runtime is required; run --ask-first to select a coding client")
    if args.runtime == "generic":
        if not args.target_app or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}", args.target_app):
            ap.error("--runtime generic requires --target-app <client-name> (letters, digits, ._-)")
    elif args.target_app:
        ap.error("--target-app is only valid with --runtime generic")

    dest = pathlib.Path(args.target).expanduser().resolve()
    if not dest.is_dir() or dest == REPO or REPO in dest.parents or dest in REPO.parents:
        ap.error("target must be an existing project outside the bootstrap checkout")
    tier = args.tier
    runtime = args.runtime
    mode = args.config_git
    try:
        prev = existing_mode(dest)
    except OSError as exc:
        print("NOT_CONFIGURED: cannot inspect existing .gitignore:", exc)
        return 2
    if prev and prev != mode and not args.change_config_git:
        print(f"MODE_CHANGE_REQUIRES_APPROVAL: {prev} -> {mode}")
        print("Preview with --change-config-git to inspect changes; --apply also requires this flag")
        return 2
    staged_state = dest / "harness/setup-state.json"
    try:
        confine(dest, staged_state)
    except ValueError as exc:
        print("BLOCK: unsafe setup state path:", exc)
        return 2
    if args.staged and not staged_state.exists() and any(
            (dest / p).exists() for p in ("harness/codex/hook.py",
                                         "harness/claude/hook.py", ".agents/hooks.json")):
        print("BLOCK: --staged may not silently unlock an existing legacy harness")
        return 2
    if args.staged and staged_state.exists():
        try:
            existing = json.loads(staged_state.read_text(encoding="utf-8"))
            if existing.get("phase") in ("READY", "READY_WITH_LIMITATIONS", "HANDOFF_COMPLETE") or existing.get("runtime") != runtime:
                print("BLOCK: staged state is already READY or belongs to another runtime")
                return 2
        except (OSError, ValueError, AttributeError):
            print("BLOCK: staged state malformed; repair using independent maintenance")
            return 2
    print_pre_ask_block(dest, tier, runtime, args.target_app, mode)
    if not args.staged and not staged_state.exists():
        print("WARNING_UNSTAGED_INSTALL: blocking hooks can run immediately with incomplete")
        print("branch setup and prevent repair in a fresh session. RECOMMENDED: --staged.")
        print("This mode is retained for existing CLI compatibility; do not use for first setup.")
    if args.staged:
        print("STAGED: hooks defer blocking while BOOTSTRAPPING; final lock requires live tests")

    try:
        old_manifest = read_install_manifest(dest)
        if args.upgrade and old_manifest is None:
            print("BLOCK: --upgrade needs a prior bootstrap file manifest; manual reconciliation required")
            return 2
        ops = plan(dest, tier, runtime, mode, upgrade=args.upgrade, previous=old_manifest)
        tracked = tracked_local_setup(dest, mode)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print("NOT_CONFIGURED: invalid source, ignore policy or Git index:", exc)
        return 2
    for state, source, target in ops:
        print(state, target.relative_to(dest).as_posix())
    conflicts = [target for state, _, target in ops if state == "CONFLICT"]
    merge = (dest / "AGENTS.md") in conflicts and (dest / "AGENTS.md").is_file()
    summary = {k: sum(x[0] == k for x in ops) for k in ("ADD", "SAME", "UPDATE", "UPGRADE", "CONFLICT")}
    print("SUMMARY:", json.dumps(dict(tier=tier, runtime=runtime, target_app=args.target_app,
                                      config_git=mode, **summary), sort_keys=True))
    if runtime == "generic":
        print("PORT_REQUIRED: copy .generic/agents roles into the verified native host format after separate approval")
    for name in tracked:
        print("TRACKED_LOCAL_STATE:" if mode == "tracked" else "TRACKED_LOCAL_SETUP:", name)
    if tracked:
        print("PRIVACY_REVIEW_REQUIRED: .gitignore does not untrack existing index entries; no files/index entries removed")

    if not args.apply:
        return 2 if conflicts or tracked else 0
    if args.upgrade and staged_state.is_file():
        current_phase = json.loads(staged_state.read_text(encoding="utf-8")).get("phase")
        if current_phase in ("READY", "READY_WITH_LIMITATIONS", "HANDOFF_COMPLETE") and any(
                state == "UPGRADE" and ("hook" in target.name.lower() or
                "harness/common/" in target.relative_to(dest).as_posix())
                for state, _, target in ops):
            print("BLOCK: protected active hooks/scripts require separately approved maintenance")
            return 2


    # Preflight every destination before any write, including AGENTS merge candidate.
    try:
        for _, _, target in ops:
            confine(dest, target)
        if merge:
            confine(dest, dest / "AGENTS.bootstrap.md")
    except ValueError as exc:
        print("BLOCK: unsafe destination:", exc)
        return 2
    ignore = dest / ".gitignore"
    ignore_before = ignore.read_bytes() if ignore.exists() else None
    ignore_after = ignore_before
    manifest_path = dest / BOOTSTRAP_MANIFEST
    manifest_before = manifest_path.read_bytes() if manifest_path.is_file() else None
    added, replaced = [], []
    state_created = None
    manifest_written = None
    try:
        ignore_op = next((op for op in ops if op[2].name == ".gitignore"), None)
        if ignore_op is None:
            raise ValueError("template is missing required .gitignore source")
        if ignore_op[0] == "CONFLICT":
            raise ValueError("cannot safely install .gitignore policy")
        ignore_after = ignore_contents(dest, ignore_op[1], mode)
        write_ignore(dest, ignore_op[1], mode)
        exposed = exposed_local_setup(dest, mode)
        if exposed:
            for name in exposed:
                print("LOCAL_STATE_NOT_IGNORED:" if mode == "tracked" else "LOCAL_SETUP_NOT_IGNORED:", name)
            raise ValueError("nested Git ignore exceptions must be reconciled before copying setup")
        if args.staged and not staged_state.exists():
            confine(dest, staged_state)
            staged_state.parent.mkdir(parents=True, exist_ok=True)
            confine(dest, staged_state)
            with staged_state.open("x", encoding="utf-8") as out:
                json.dump({"schema_version": 1, "phase": "BOOTSTRAPPING",
                           "runtime": runtime, "tier": tier}, out, indent=2)
                out.write("\n")
            state_created = staged_state.read_bytes()
            print("STAGED_STATE: BOOTSTRAPPING")
        if merge:
            candidate = dest / "AGENTS.bootstrap.md"
            if not candidate.exists():
                safe_copy(dest, SOURCE / "AGENTS.md", candidate)
                added.append((candidate, digest(SOURCE / "AGENTS.md")))
                print("EXPORTED: AGENTS.bootstrap.md")
            elif digest(candidate) != digest(SOURCE / "AGENTS.md"):
                print("CONFLICT: existing AGENTS.bootstrap.md retained")
        for state, source, target in ops:
            if state == "ADD" and target.name != ".gitignore":
                safe_copy(dest, source, target)
                added.append((target, digest(source)))
            elif state == "UPGRADE":
                old_bytes = target.read_bytes()
                replace_managed_file(dest, source, target,
                                     old_manifest["files"][target.relative_to(dest).as_posix()]["installed_sha256"])
                replaced.append((target, old_bytes, digest(source)))
        records = dict(old_manifest["files"]) if old_manifest else {}
        for state, source, target in ops:
            if state in ("ADD", "SAME", "UPGRADE") and target.name != ".gitignore":
                if target.is_file() and digest(target) == digest(source):
                    records[target.relative_to(dest).as_posix()] = {
                        "source_sha256": digest(source), "installed_sha256": digest(target)}
        template_fingerprint = hashlib.sha256("\\n".join(
            rel.as_posix() + ":" + digest(src) for src, rel in entries(tier, runtime)
        ).encode("utf-8")).hexdigest()
        new_manifest = {"schema_version": 1, "template_fingerprint_sha256": template_fingerprint,
                        "tier": tier, "runtime": runtime, "config_git": mode, "files": records}
        write_install_manifest(dest, new_manifest, manifest_before)
        manifest_written = manifest_path.read_bytes()
    except (OSError, ValueError, subprocess.TimeoutExpired, KeyError, StopIteration) as exc:
        print("ERROR: install transaction failed:", exc)
        rollback_install(dest, added, replaced, ignore_before, ignore_after,
                         state_created, manifest_before, manifest_written)
        return 2

    print("APPLIED: new files and managed Git ignore policy" if not conflicts else "APPLIED_WITH_CONFLICTS: merge/reconcile required")
    return 2 if conflicts or tracked else 0

if __name__ == "__main__":
    sys.exit(main())

