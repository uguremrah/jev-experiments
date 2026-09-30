# 01 - Qualitative linter: what does each log line leak?

## Question
For every logging or print call in a codebase, what kind of value does it write to the log: nothing sensitive, personal data, a secret, or financial data?

A keyword linter can't answer this, because the answer depends on what a variable *holds*, not on what it is called. It's a System One job: one small judgment per line, over many lines, cheap enough to run on every commit.

## Setup
- Model: `jev-1.13.0`
- Baseline: a naive keyword regex (`password|secret|token|api_key`, `card|iban|cvv`, `email|phone|ssn`), shown side by side
- Question type: one **choice** per log call, with 4 options

Code does everything except the judgment:
- It finds the calls (one regex per call style).
- It sends one batched request: the state is both files, numbered, and there is one question per call.
- It applies the policy:
  - secret or financial at p >= 0.80 → ERROR;
  - personal data at p >= 0.80 → WARN;
  - a top answer below 0.80 → REVIEW;
  - anything else → OK.
- It exits 1 if there is any ERROR.

## Data
Invented code in `shop/`: `checkout.py` and `PaymentService.java`, with 11 log calls. No real values appear in the files.

The traps for the keyword regex are planted on purpose:
- **False alarms:** `token_count`, `api_key_rotated`, and a card that is already masked.
- **Misses:** an email hidden in `contact`, the Authorization header in `creds`, and a shipping address.

Expected answers are in `labels.json`. `fixed/` holds the same code with the 3 ERROR lines wrapped in the existing mask helpers.

## How to run
From the repo root, with `TYPESAFE_API_KEY` set:

```bash
python3 experiments/01-qualitative-linter/lint.py experiments/01-qualitative-linter/shop     # expect exit 1
python3 experiments/01-qualitative-linter/lint.py experiments/01-qualitative-linter/fixed    # expect exit 0
python3 experiments/01-qualitative-linter/check.py experiments/01-qualitative-linter/shop 5  # repeat runs against labels.json
```

`--replay` prints the cached answer for the same file contents without calling the API. The cache is written on each live run and is not committed.

**With an agent:** run the linter with `!` inside Claude Code, so the output lands in the agent's context. Then ask: *"Fix only the ERROR lines from the linter output above, using the mask helpers already in the code."* Then run it again.

## Results
Measured on 2026-10-01 with `jev-1.13.0`.

| Metric | Jev | Keyword regex |
|---|---|---|
| Lines matching `labels.json` (11 lines, 10 runs) | 11 / 11 every run | 5 / 11 |
| Top probability per line | 0.94 or higher; varied by at most 0.02 between runs | n/a |
| Time per request (all 11 lines) | 0.34 to 0.45 s | n/a |
| Input tokens / cost per request | about 4,200 / about $0.00018 at list price | n/a |

After the fix (`fixed/`): ERROR 0, WARN 3, exit 0. Two masked secrets sit close to the threshold, so a REVIEW line is expected:

| Line | Masked value | `nothing_sensitive` probability |
|---|---|---|
| `checkout.py:20` | Authorization value | 0.77 to 0.84 (REVIEW in 3 of 7 runs) |
| `PaymentService.java:14` | gateway key | 0.81 to 0.88 |

For comparison, a masked card number scores 0.99. The model is less sure that the last four characters of a token are harmless, and the policy sends that doubt to a human instead of passing it.

## Caveats
- **11 lines of code we wrote ourselves, including the traps.** This shows the approach works, not how accurate it is. Measure it on your own code before relying on it.
- **Single-line calls only.** The extraction regex only finds calls that fit on one line; multi-line calls need a real parser.
- **The policy is ours.** Masked means safe, and the 0.80 threshold is our choice. Change `CRITERIA` and `ACT_AT` in `lint.py` to fit your rules.
