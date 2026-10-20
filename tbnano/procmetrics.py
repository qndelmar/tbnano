"""Process metrics (spec v2, section 3).

Computed per episode from its trajectory; aggregated next to pass@1.
Episodes ending in harness_error are excluded (the failure is ours, not
the model's). All definitions in one place so the numbers can be audited
against the pilot's hand-computed values.
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

# Refusal phrases — the ONLY list; keep all variants here (spec 3).
REFUSAL_PATTERNS = [
    "don't have access", "do not have access", "cannot", "can't",
    "unable to", "not able to", "i'm sorry", "i am sorry",
    "no access", "as an ai", "impossible",
]
REFUSAL_RE = re.compile("|".join(re.escape(p) for p in REFUSAL_PATTERNS), re.I)

# `run` commands that count as "looking before acting" for grounding.
INSPECT_CMD_RE = re.compile(r"^\s*(ls|find|cat|head|tail|wc|file|stat|du|tree)\b")

# Filename-looking tokens in the instruction (e.g. data.csv, docs/a.txt,
# Makefile). Deliberately generous — misses are less bad than noise.
FILE_TOKEN_RE = re.compile(r"\b[\w.-]*[\w-]+\.(?:txt|csv|tsv|json|jsonl|ndjson|"
                           r"log|py|sh|bash|c|h|cpp|rs|go|js|ts|sql|db|sqlite|"
                           r"md|markdown|yaml|yml|ini|conf|cfg|toml|xml|html|"
                           r"mk|out|dat|bin|key|lock)\b|\bMakefile\b")


def instruction_files(instruction: str) -> list[str]:
    """File names the instruction mentions (basename candidates kept
    verbatim — matching is a substring test on call args)."""
    out = []
    for m in FILE_TOKEN_RE.finditer(instruction):
        t = m.group(0)
        if t.lower() in ("e.g.", "i.e."):
            continue
        out.append(t)
    return out


def _call_of(entry: dict[str, Any]) -> Optional[tuple[str, str]]:
    """(name, canonical-args-json) for a *valid* call entry, else None.
    Entries flagged 'invalid' (bad args) count as attempts, not calls."""
    if entry.get("kind") != "call" or "invalid" in entry:
        return None
    try:
        c = json.loads(entry["call"])
        return c.get("name", ""), json.dumps(c.get("arguments", {}), sort_keys=True)
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def _result_error(entry: dict[str, Any]) -> bool:
    """True when the tool result reports failure: error key, nonzero exit
    code, or ok:false."""
    out = entry.get("result")
    if not out:
        return False
    try:
        r = json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return False
    if r.get("error"):
        return True
    if r.get("exit_code", 0) not in (0, None):
        return True
    if r.get("ok") is False:
        return True
    return False


def episode_metrics(
    trajectory: list[dict[str, Any]],
    instruction: str = "",
    end_reason: str = "",
) -> dict[str, Any]:
    """Per-episode process metrics; aggregated by metrics._group_stats."""
    calls: list[tuple[str, str]] = []      # (name, args_json) of valid calls
    err_after: list[tuple[str, str]] = []  # errored calls (same tuples)
    err_recovered = 0
    invalid = 0
    refused = False

    entries = [e for e in trajectory if e.get("kind") in
               ("call", "text", "final_text", "invalid")]
    for i, e in enumerate(entries):
        if e.get("kind") == "invalid":
            invalid += 1
            continue
        if e.get("kind") in ("text", "final_text"):
            if REFUSAL_RE.search(e.get("reply") or ""):
                refused = True
            continue
        tup = _call_of(e)
        if tup is None:
            invalid += 1  # call parsed but args malformed
            continue
        calls.append(tup)
        if _result_error(e):
            # recovery = the NEXT agent action is a different valid call
            for j in range(i + 1, len(entries)):
                nxt = _call_of(entries[j])
                if nxt is not None:
                    if nxt != tup:
                        err_recovered += 1
                    break
                if entries[j].get("kind") in ("text", "final_text", "invalid"):
                    break  # text or garbage next: not recovery
            err_after.append(tup)

    # loop: 3 identical consecutive valid calls
    looped = any(
        calls[k] == calls[k + 1] == calls[k + 2] for k in range(len(calls) - 2)
    )

    # grounded_first_call (spec v2 3): the first valid call either names a
    # file mentioned in the instruction or is an inspect command. Defined
    # for every episode; False when there was no valid call at all.
    files = instruction_files(instruction)
    grounded = False
    if calls:
        name, args = calls[0]
        try:
            argtext = json.dumps(json.loads(args))
            cmd = str(json.loads(args).get("cmd", ""))
        except json.JSONDecodeError:
            argtext, cmd = args, ""
        grounded = bool(
            any(f in argtext for f in files)
            or (name == "run" and INSPECT_CMD_RE.search(cmd))
        )

    return {
        "valid_calls": len(calls),
        "call_attempts": len(calls) + invalid,
        "grounded_first": grounded,
        "looped": looped,
        "err_calls": len(err_after),
        "err_recovered": err_recovered,
        "proper_end": end_reason == "finish",
        "refused": refused,
    }
