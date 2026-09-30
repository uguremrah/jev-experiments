"""Repeat live runs against labels.json: agreement per line and drift of the top probability.

Usage (from the repo root):
    python3 experiments/01-qualitative-linter/check.py experiments/01-qualitative-linter/shop 5
Labels exist only for the unfixed shop/ files; for fixed/ it checks that no line is an ERROR.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint  # noqa: E402

root, runs = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 5
labels = json.load(open(os.path.join(lint.HERE, "labels.json")))
files, calls = lint.find_calls(root)
body = lint.build_body(files, calls)
seen = {c["key"]: [] for c in calls}
times = []
for _ in range(runs):
    payload, seconds = lint.ask(body)
    times.append(seconds)
    for c in calls:
        seen[c["key"]].append(lint.decide(payload["answers"][c["key"]]["probabilities"]))
agree = 0
for key, results in seen.items():
    tops = {r[0] for r in results}
    ps = [r[1] for r in results]
    expected = labels.get(key)
    ok = expected is not None and tops == {expected} and all(r[1] >= lint.ACT_AT for r in results)
    agree += ok
    print("%-24s expected %-18s got %-30s p %.2f-%.2f  %s" % (
        key, expected, ",".join(sorted(tops)), min(ps), max(ps), "ok" if ok else "CHECK"))
print("\n%d/%d lines agree over %d runs; seconds min %.2f max %.2f" % (
    agree, len(seen), runs, min(times), max(times)))
print("actions: %s" % sorted({r[2] for rs in seen.values() for r in rs}))
