#!/usr/bin/env python3
"""Real terminal menu for CLI Bootstrap setup. Not an approval or authentication tool."""
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE = ROOT / "harness/setup-state.json"
OUTPUT = ROOT / "harness/setup-intake.json"


def choice(label, options, input_fn=input, output_fn=print):
    """Show numbered options and return the value the user explicitly selected."""
    output_fn("")
    output_fn("CONFIGURATION QUESTION — not a permission request")
    output_fn(label)
    for i, (_, caption) in enumerate(options, 1):
        output_fn("  %s) %s" % (i, caption))
    while True:
        answer = input_fn("Choose a number (or q to cancel): ").strip()
        if answer.lower() in ("q", "quit", "cancel"):
            raise ValueError("questionnaire cancelled without saving")
        if answer.isdecimal() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1][0]
        output_fn("Invalid option. Read the question and choose a displayed number.")


def branch_name(value):
    """Basic safe branch-name validation, not a replacement for git check-ref-format."""
    return bool(value and len(value) <= 128 and
                not re.search(r"[\s\\~^:?*\[\]]", value) and
                not value.startswith((".", "-", "/")) and
                not value.endswith((".", "/", ".lock")) and
                ".." not in value and "//" not in value and "@{" not in value)


def collect(runtime, input_fn=input, output_fn=print):
    output_fn("BOOTSTRAP SETUP — CLI QUESTIONNAIRE")
    output_fn("You have already dealt with command permissions. The following numbered")
    output_fn("selections configure the project; 1/2/3 do NOT grant tool permissions.")
    responses = []
    def record(question_id, value):
        responses.append({"id": question_id, "value": value, "source": "cli_menu"})
    record("tier", choice("Which harness tier?", [
        ("Lite", "Lite — reduced role set, no full Planner/Tester workflow"),
        ("Standard", "Standard — Planner and Tester (recommended)"),
        ("Full", "Full — extended review and maintenance roles"),
    ], input_fn, output_fn))
    record("git_mode", choice("Should Bootstrap configuration be committed to project Git?", [
        ("local", "No: keep harness configuration local (recommended for private projects)"),
        ("tracked", "Yes: track non-private harness configuration in Git"),
    ], input_fn, output_fn))
    branch = choice("Is the active development branch already selected by you?", [
        ("later", "No: choose with the agent after inspecting the project's Git"),
        ("now", "Yes: enter the explicitly approved branch name"),
    ], input_fn, output_fn)
    if branch == "now":
        while True:
            active = input_fn("Active development branch name (q to cancel): ").strip()
            if active.lower() in ("q", "quit", "cancel"):
                raise ValueError("questionnaire cancelled without saving")
            if branch_name(active):
                record("active_branch", active)
                break
            output_fn("Invalid Git branch name; enter a valid name, e.g. develop or upgrade/v5.")
    else:
        record("branch_authority", "DEFERRED")
    return {
        "schema_version": 1,
        "channel": "cli_menu",
        "runtime": runtime,
        "host_event_ref": None,
        "captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "responses": responses,
    }


def write_trace(root, data):
    """Exclusive create. No partial or silent overwrite of recorded choices."""
    path = root / "harness/setup-intake.json"
    if path.is_symlink() or path.exists() or path.parent.is_symlink():
        raise ValueError("existing or unsafe intake trace; review it before retrying")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return path


def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("INTERACTIVE_INTAKE_UNAVAILABLE: real interactive CLI terminal (TTY) required.")
        print("Use your CLI host's own numbered selector if available, otherwise run")
        print("this wizard in a real terminal. Do not pipe fabricated answers into stdin.")
        return 2
    if OUTPUT.exists() or OUTPUT.is_symlink():
        print("BLOCK: prior setup-intake.json exists; inspect/reconcile, do not overwrite.")
        return 2
    try:
        if not STATE.is_file() or STATE.is_symlink():
            raise ValueError("first install the preliminary staged harness")
        state = json.loads(STATE.read_text(encoding="utf-8"))
        if not isinstance(state, dict) or state.get("phase") != "BOOTSTRAPPING":
            raise ValueError("questionnaire is for staged BOOTSTRAPPING projects only")
        runtime = state.get("runtime")
        if runtime not in ("codex", "claude", "antigravity", "continue", "generic"):
            raise ValueError("setup state has unknown runtime")
        data = collect(runtime)
        output = write_trace(ROOT, data)
    except (EOFError, KeyboardInterrupt, OSError, ValueError) as err:
        print("BLOCK:", err)
        return 2
    print("SETUP_INTAKE: RECORDED (CLI menu, not an authorization signature)")
    print("Saved local/private trace:", output.relative_to(ROOT))
    print("Continue in the original setup agent session; keep it open until handoff.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
