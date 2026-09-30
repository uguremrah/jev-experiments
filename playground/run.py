"""Send a Playground case through the API: the same state and questions you paste into the console.

Usage (from the repo root):
    python3 playground/run.py playground/state_leak.json
    python3 playground/run.py playground/state_bearing.json
All data here is invented. The key comes from TYPESAFE_API_KEY.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from shared.jev import ask  # noqa: E402

state = json.load(open(sys.argv[1]))
questions = json.load(open(os.path.join(HERE, "questions.json")))
payload, seconds = ask(state, questions)
print("%.2f s  usage %s" % (seconds, payload.get("usage")))
for key, ans in payload["answers"].items():
    t = ans.get("type")
    if t == "noul":
        print("%-18s yes %.2f" % (key, ans["noul"]))
    else:
        probs = sorted(ans["probabilities"].items(), key=lambda kv: -kv[1])[:3]
        head = ("score %.2f  " % ans["score"]) if t == "score" else ""
        print("%-18s %sconf %.2f  top: %s" % (key, head, ans.get("confidence", float("nan")),
                                              ", ".join("%s %.2f" % kv for kv in probs)))
