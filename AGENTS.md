# Instructions for coding agents

You are working in a repository of small, reproducible experiments with Jev, TypeSafe's System One model. Read this file before running or adding anything.

## Ground rules

1. **API key:** read it from the `TYPESAFE_API_KEY` environment variable. Never print it, log it, pass it on a command line, or write it to a file.
2. **Data:** use only invented or public data. Never send private, client or personal data to the API, and never commit it.
3. **Model version:** pin it (for example `jev-1.13.0`) in every script and record it next to every result.
4. **Hooks and automation:** anything that plugs into an agent starts **log-only**. It may not block or change behaviour until it has been measured against a baseline.
5. **Results:** report what you measured, with the command you ran. If a number differs from the one in the README, report both; do not overwrite the README silently.

## Replicating an experiment

1. Read `experiments/<name>/README.md` fully.
2. Run exactly the command it gives, with the pinned model version.
3. Compare with the recorded numbers. Small drift (around 0.01 in probabilities) is normal between runs.
4. Write your numbers into a new file `experiments/<name>/results-<date>.md`.

## Adding an experiment

1. Copy `experiments/_template/` to `experiments/NN-short-name/`.
2. Fill in every section of its README before running anything at scale.
3. Keep the experiment self-contained: its data, scripts and results live in its folder. Shared helpers go in `shared/`.

## TypeSafe request format (reference)

`POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer $TYPESAFE_API_KEY` and a JSON body:

```json
{
  "model": "jev-1.13.0",
  "state": {"text": "..."},
  "questions": {
    "is_x":   {"type": "noul",   "instructions": "...", "criteria": {"true": "...", "false": "..."}},
    "which":  {"type": "choice", "instructions": "...", "criteria": {"option_a": "...", "option_b": "..."}},
    "how_bad":{"type": "score",  "instructions": "...", "criteria": ["level 0 ...", "level 1 ...", "level 2 ..."]}
  }
}
```

Current documentation: https://docs.typesafe.ai
