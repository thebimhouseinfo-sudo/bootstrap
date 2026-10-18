#!/usr/bin/env python3
"""Copy-only, conflict-safe bootstrap installer. Python >=3.9. No external dependencies."""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

SOURCE = pathlib.Path(__file__).resolve().parent / "project-template"
SKIP = {"SETUP.md", "CODEX_READY.md"}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def files():
    return sorted(p for p in SOURCE.rglob("*") if p.is_file() and p.relative_to(SOURCE).as_posix() not in SKIP)
def plan(dest):
    actions=[]
    for src in files():
        relative=src.relative_to(SOURCE)
        target=dest/relative
        if not target.exists():
            actions.append(("ADD",src,target))
        elif target.is_symlink() or not target.is_file():
            actions.append(("CONFLICT",src,target))
        elif sha(src)==sha(target):
            actions.append(("SAME",src,target))
        else:
            actions.append(("CONFLICT",src,target))
    return actions
def main():
    ap=argparse.ArgumentParser(description="Safe Codex template install: dry-run by default.")
    ap.add_argument("--target",required=True,help="existing target project root")
    ap.add_argument("--apply",action="store_true",help="copy only missing files, never overwrite")
    args=ap.parse_args()
    dest=pathlib.Path(args.target).expanduser().resolve()
    if not dest.is_dir() or not SOURCE.is_dir() or dest == SOURCE or SOURCE in dest.parents:
        ap.error("target must be an existing project directory outside template source")
    actions=plan(dest)
    for status,src,target in actions:
        print(status,src.relative_to(SOURCE).as_posix())
    summary={key:sum(status==key for status,_,_ in actions) for key in ("ADD","SAME","CONFLICT")}
    print("SUMMARY:",json.dumps(summary,sort_keys=True))
    if not args.apply:
        return 0 if not summary["CONFLICT"] else 2
    # All conflicts are preserved; no overwrite or mutation of preexisting files.
    copied=[]
    try:
        for status,src,target in actions:
            if status!="ADD":
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists() or target.is_symlink():
                print("CONFLICT during install:",target)
                return 2
            # Exclusive creation avoids overwrites even under a concurrent writer.
            with open(target,"xb") as out,open(src,"rb") as inp:
                shutil.copyfileobj(inp,out)
            copied.append(target)
        print("APPLIED:",len(copied),"new files; existing files untouched")
    except (OSError,ValueError) as exc:
        print("ERROR:",exc,"; inspect target manually. No destructive rollback performed.")
        return 1
    return 0 if not summary["CONFLICT"] else 2
if __name__=="__main__":
    sys.exit(main())
