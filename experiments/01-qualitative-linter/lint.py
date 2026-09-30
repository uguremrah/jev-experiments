"""Qualitative linter: Jev judges what every logging or print call writes to the log.

Usage (from the repo root):
    python3 experiments/01-qualitative-linter/lint.py experiments/01-qualitative-linter/shop
    python3 experiments/01-qualitative-linter/lint.py experiments/01-qualitative-linter/shop --replay

Code finds the calls and decides the action; Jev only answers one Choice per call.
All demo code is invented. The key comes from TYPESAFE_API_KEY.
Exit code 1 when any line is an ERROR.
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from shared.jev import API_URL, MODEL, PRICE_PER_MTOK, api_key  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
ACT_AT = 0.80

# One pattern per call style. Each demo call sits on one line.
CALL = {
    ".py": re.compile(r"^\s*(log\.(debug|info|warning|error)|logger\.\w+|print)\("),
    ".java": re.compile(r"^\s*(log\.(debug|info|warn|error)|System\.out\.print(ln)?)\("),
}

# The naive keyword linter shown next to Jev for contrast.
NAIVE = [
    ("secret", re.compile(r"password|passwd|secret|token|api_?key", re.I)),
    ("financial", re.compile(r"card|iban|cvv", re.I)),
    ("personal", re.compile(r"email|phone|ssn", re.I)),
]

INSTRUCTIONS = (
    "You review logging for data leaks. What kind of value does the logging statement on "
    "line {line} of `files.{name}` write to the log output? The statement is: {code}\n"
    "Use the surrounding code in `files.{name}` to know what each variable holds. "
    "Judge the value that actually reaches the log, not the variable names."
)
CRITERIA = {
    "nothing_sensitive": "No sensitive value reaches the log: counts, status flags, booleans, "
                         "durations, amounts and prices, technical ids, and any value that is "
                         "masked, hashed or truncated (for example a card shown as ****1234).",
    "personal_data": "Data that identifies or contacts a person: email address, phone number, "
                     "postal or shipping address, full name, date of birth.",
    "secret": "A credential that grants access: password, API key, access or refresh token, "
              "session secret, the value of an Authorization header, private key.",
    "financial": "Full payment or bank data: a full card number, CVV, IBAN or bank account number.",
}
ACTION = {"secret": "ERROR", "financial": "ERROR", "personal_data": "WARN", "nothing_sensitive": "OK"}
SHORT = {"nothing_sensitive": "nothing", "personal_data": "personal", "secret": "secret",
         "financial": "financial"}


def find_calls(root):
    """Return (files, calls): numbered sources per file and every log call found by code."""
    files, calls = {}, []
    for dirpath, _, names in os.walk(root):
        for name in sorted(names):
            ext = os.path.splitext(name)[1]
            if ext not in CALL:
                continue
            lines = open(os.path.join(dirpath, name)).read().splitlines()
            files[name] = "\n".join("%3d| %s" % (i, l) for i, l in enumerate(lines, 1))
            for i, l in enumerate(lines, 1):
                if CALL[ext].search(l):
                    calls.append({"key": "%s:%d" % (name, i), "name": name, "line": i,
                                  "code": l.strip()})
    return files, calls


def naive(code):
    for label, pat in NAIVE:
        if pat.search(code):
            return label
    return "-"


def build_body(files, calls):
    questions = {c["key"]: {"type": "choice",
                            "instructions": INSTRUCTIONS.format(line=c["line"], name=c["name"],
                                                                code=c["code"]),
                            "criteria": CRITERIA} for c in calls}
    return {"model": MODEL, "state": {"files": files}, "questions": questions}


def ask(body):
    req = urllib.request.Request(API_URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + api_key(),
                                          "Content-Type": "application/json"})
    t0 = time.perf_counter()
    payload = json.loads(urllib.request.urlopen(req, timeout=20).read())
    return payload, time.perf_counter() - t0


def decide(probs):
    top = max(probs, key=probs.get)
    p = round(probs[top], 2)  # decide on the value shown on screen
    return top, p, (ACTION[top] if p >= ACT_AT else "REVIEW")


def main(argv):
    root = argv[1]
    replay = "--replay" in argv
    files, calls = find_calls(root)
    body = build_body(files, calls)
    digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    cache_file = os.path.join(CACHE, digest + ".json")

    if replay:
        cached = json.load(open(cache_file))
        payload, seconds = cached["payload"], cached["seconds"]
    else:
        payload, seconds = ask(body)
        os.makedirs(CACHE, exist_ok=True)
        json.dump({"payload": payload, "seconds": seconds}, open(cache_file, "w"))

    width = min(max(len(c["code"]) for c in calls), 52)
    print("%4s  %-*s  %-9s  %-15s %s" % ("line", width, "code", "regex", "jev (p)", "action"))
    counts = {"ERROR": 0, "WARN": 0, "REVIEW": 0, "OK": 0}
    current = None
    for c in calls:
        if c["name"] != current:
            current = c["name"]
            print("-- %s %s" % (current, "-" * (width + 32 - len(current))))
        top, p, action = decide(payload["answers"][c["key"]]["probabilities"])
        counts[action] += 1
        code = c["code"] if len(c["code"]) <= width else c["code"][:width - 3] + "..."
        print("%4d  %-*s  %-9s  %-10s %.2f %s" % (c["line"], width, code, naive(c["code"]),
                                                 SHORT[top], p, action))
    tokens = (payload.get("usage") or {}).get("input_tokens", 0)
    print()
    print("ERROR %d   WARN %d   REVIEW %d   OK %d" % tuple(counts[k] for k in
                                                        ("ERROR", "WARN", "REVIEW", "OK")))
    print("%d log lines judged in %.2f s%s, %d input tokens, about $%.5f at list price"
          % (len(calls), seconds, " (replayed)" if replay else "", tokens,
             tokens * PRICE_PER_MTOK / 1e6))
    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
