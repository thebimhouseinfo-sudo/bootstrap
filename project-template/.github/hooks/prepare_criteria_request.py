#!/usr/bin/env python3
"""Create a short-lived, non-authenticated post-advice Criteria permission request.

Run ONLY after Technical Advisor has advised on the exact draft/delta,
and the Human has expressly decided to apply it in a new post-advice turn.
The agent may run this; the native Copilot preToolUse still returns ASK.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "CRITERIA.md"
DEST = ROOT / "harness" / "criteria-write-authorization.json"

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scope", choices=["initial", "amendment"], required=True)
    p.add_argument("--proposal-id", required=True)
    args = p.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]{0,95}", args.proposal_id):
        p.error("proposal-id must be a short, safe identifier of the advised proposal")
    if DEST.is_symlink():
        p.error("authorization path must not be a symlink")
    baseline = hashlib.sha256(SOURCE.read_bytes()).hexdigest() if SOURCE.is_file() else "ABSENT"
    expiry = (datetime.datetime.now(datetime.timezone.utc)
              + datetime.timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": 1, "target": "docs/CRITERIA.md",
        "baseline_sha256": baseline, "scope": args.scope,
        "proposal_id": args.proposal_id,
        "advisor_consulted": True, "human_decided_after_advice": True,
        "decision": "apply", "expires_utc": expiry,
    }
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("LOCAL_REQUEST_CREATED: Copilot native hook must still ASK Human before Criteria write.")
    print("NOT_AUTHENTICATION: receipt reflects agent assertions, not independent evidence.")
    print("If there was no actual Advisor advice and subsequent Human decision, STOP and remove request.")

if __name__ == "__main__":
    main()
