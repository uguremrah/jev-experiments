# Playground

Ready-to-paste JSON for the Playground in the TypeSafe console (console.typesafe.ai → Playground). All data is invented.

## The case: failure modes in maintenance notifications

A maintenance notification is a short record a technician writes when equipment fails. Classifying it by failure mode is one choice among many codes, which makes it a System One job. The failure-mode options follow the public ISO 14224 style (external leakage, vibration, noise and so on).

| File | What it is |
|---|---|
| `state_leak.json` | A pump seal leak, with the previous notification on the same pump |
| `state_bearing.json` | Bearing noise, vibration and a hot housing: a genuinely ambiguous case |
| `questions.json` | Five questions in one request: failure mode (choice, 15 options), failure family (choice), same failure as last time (yes/no), root cause in 6M terms (choice), production impact (score, 0 to 3) |

## In the console

1. Switch the State pane to its JSON view (the `</>` button). Paste a state file into it.
2. Paste `questions.json` into the Questions pane. The warning counter should show 0.
3. Press **Run request** (or ⌘↵), then expand each answer to see the full distribution.
4. **Try this:** in `state_leak.json`, change `validation_text` to `"Confirmed by the shift lead. No standby pump available, the line is stopped."` and run again. Only the production impact should move, from about 2.1 to 3.0.

## From the command line

```bash
python3 playground/run.py playground/state_leak.json
python3 playground/run.py playground/state_bearing.json
```

## Results (2026-10-01, `jev-1.13.0`, through the API)

| Case | Failure mode | Same failure | Root cause | Impact | Time |
|---|---|---|---|---|---|
| Seal leak | external leakage (process) 1.00 | 0.90 | machine 0.98 | 2.10 | 0.30 to 0.32 s |
| Seal leak, "line is stopped" edit | unchanged | unchanged | unchanged | 3.00 | 0.33 s |
| Bearing | noise 0.57, vibration 0.29, overheating 0.14 | 0.06 | machine 1.00 | 1.01 | 0.29 to 0.44 s |

Each request uses about 1,500 input tokens. The bearing split is the interesting one: the model isn't sure, and the distribution says so.

The console runs `jev-latest`, so its numbers can differ slightly: the largest difference we saw was 0.07.
