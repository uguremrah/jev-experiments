"""Minimal Jev client, standard library only.

The key is read from the TYPESAFE_API_KEY environment variable. It is never printed or logged.
"""
import json
import os
import time
import urllib.request

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"  # pinned: results in this repo were measured on this version
PRICE_PER_MTOK = 0.042  # USD per million input tokens, list price at the time of measurement; output is free


def api_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        raise SystemExit("Set TYPESAFE_API_KEY first (see .env.example).")
    return key


def ask(state, questions, model=MODEL, timeout=20):
    """POST one request. Returns (payload, seconds)."""
    body = json.dumps({"model": model, "state": state, "questions": questions}).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST",
                                 headers={"Authorization": "Bearer " + api_key(),
                                          "Content-Type": "application/json"})
    t0 = time.perf_counter()
    payload = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    return payload, time.perf_counter() - t0
