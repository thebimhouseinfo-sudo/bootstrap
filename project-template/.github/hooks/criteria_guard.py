#!/usr/bin/env python3
"""Copilot preToolUse hook: block unreviewed, directly named Criteria writes.

Native UI approval (ask) is required even for a matching local receipt.
This script cannot authenticate model-authored claims or intercept indirect writes.
"""
import datetime
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CRITERIA = ROOT / "docs" / "CRITERIA.md"
RECEIPT = ROOT / "harness" / "criteria-write-authorization.json"
TARGET = re.compile(r"(?:^|[/\\])(?:docs[/\\])?criteria\.md\b", re.I)
READ_NAMES = {"read", "view", "grep", "glob", "search", "web_search", "web_fetch"}


def text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from text_values(v)
    elif isinstance(value, list):
        for v in value:
            yield from text_values(v)


def touches_criteria(event):
    name = str(event.get("toolName", event.get("tool_name", ""))).lower()
    if name in READ_NAMES:
        return False
    args = event.get("toolArgs", event.get("tool_input", {}))
    # Native payload can hold arguments as JSON text or structured values.
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except (ValueError, TypeError):
            pass
    return any(TARGET.search(v.replace("\\", "/")) for v in text_values(args))


def baseline():
    if not CRITERIA.is_file():
        return "ABSENT"
    return hashlib.sha256(CRITERIA.read_bytes()).hexdigest()


def permitted_receipt():
    try:
        if RECEIPT.is_symlink():
            return None
        obj = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if (not isinstance(obj, dict)
                or obj.get("schema_version") != 1
                or obj.get("target") != "docs/CRITERIA.md"
                or obj.get("baseline_sha256") != baseline()
                or obj.get("advisor_consulted") is not True
                or obj.get("human_decided_after_advice") is not True
                or obj.get("decision") != "apply"
                or obj.get("scope") not in ("initial", "amendment")
                or not isinstance(obj.get("proposal_id"), str)
                or not obj["proposal_id"].strip()):
            return None
        expiry = datetime.datetime.fromisoformat(obj["expires_utc"].replace("Z", "+00:00"))
        if expiry.tzinfo is None or expiry <= datetime.datetime.now(datetime.timezone.utc):
            return None
        # Keep the authorization intentionally short lived.
        if expiry > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15):
            return None
        return obj
    except (OSError, ValueError, KeyError, TypeError):
        return None


def decision(event):
    if not touches_criteria(event):
        return {}
    receipt = permitted_receipt()
    if receipt is None:
        return {
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "CRITERIA_PREWRITE_BLOCKED: Do NOT write docs/CRITERIA.md. "
                "If initial Criteria: Planner must first display the entire draft IN CHAT; "
                "only after Human requests writing it, invoke Technical Advisor on that draft. "
                "If existing Criteria: settle an exact delta with Human IN CHAT; when Human "
                "requests updating, invoke Technical Advisor on current Criteria + delta. "
                "Advisor gives advice only; Human must decide again AFTER reading advice. "
                "Only then may Planner prepare a scoped local authorization receipt and retry. "
                "If Technical Advisor cannot be invoked, do not edit Criteria."
            ),
        }
    return {
        "permissionDecision": "ask",
        "permissionDecisionReason": (
            "CRITERIA_POST_ADVICE_HUMAN_CONFIRMATION: Proposal "
            + receipt["proposal_id"]
            + " claims Advisor consultation and Human post-advice decision. "
            "Before approving this tool call, Human must verify the exact proposed changes "
            "match their decision. This native UI approval is separate from an "
            "agent-writable receipt and cannot prove Advisor actually ran."
        ),
    }


def main():
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("invalid hook payload")
        result = decision(event)
    except (OSError, ValueError, TypeError):
        # Hook errors fail closed for Copilot command preToolUse (apart from timeouts).
        # Still return explicit deny when possible.
        result = {"permissionDecision": "deny",
                  "permissionDecisionReason": "CRITERIA_HOOK_INPUT_INVALID: check hook configuration"}
    sys.stdout.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main()
