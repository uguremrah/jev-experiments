# jev-experiments

Hands-on experiments with **Jev**, the System One model from [TypeSafe](https://typesafe.ai), used from coding agents such as Claude Code.

A System One model does not write text. You give it a **state** (the facts) and **questions** with the answers spelled out in advance, and it returns a probability for each answer in a fraction of a second. That makes it a fit for the many small, repeated decisions inside an AI system, where a slow reasoning model is overkill:

| Question type | Returns | Example |
|---|---|---|
| **Noul** (yes/no) | probability of yes | "Could this shell command lose data?" |
| **Choice** | one probability per option, up to 255 options | "Which failure mode does this maintenance note describe?" |
| **Score** | a position on 2 to 11 described levels | "How severe is the impact on production, 0 to 3?" |

> **Status:** work in progress. The structure is in place; experiments, data and results are added one at a time.

## Repository layout

```
jev-experiments/
├── README.md            this file
├── AGENTS.md            instructions for coding agents replicating the experiments
├── CLAUDE.md            points Claude Code at AGENTS.md
├── docs/                write-ups and background (to be filled)
├── experiments/         one folder per experiment, each self-contained
│   └── _template/       copy this to start a new experiment
├── playground/          JSON you can paste into the TypeSafe console Playground
└── shared/              small helpers shared by experiments (API client and so on)
```

## Replicate with your agent

1. Get an API key from the TypeSafe console and export it: `export TYPESAFE_API_KEY=...` (see `.env.example`). Never commit it.
2. Open this repository in your coding agent (Claude Code, Codex or similar). It reads `AGENTS.md` for the ground rules.
3. Pick a folder under `experiments/` and ask the agent to follow its README: *"Replicate experiments/<name> and compare your numbers with the README."*

Each experiment README states the question, the data, the exact command to run, the numbers we measured, the model version, and the caveats.

## Principles

- **Shadow first, trust later.** Anything wired into an agent starts log-only, and gets measured against a baseline before it may block or act.
- **Measure on your own data.** Our numbers show what worked for us; they are not a leaderboard.
- **Pin the model version.** Thresholds are only valid for the version they were measured on.
- **Keep private data out.** Experiments here use invented or public data only.

## Links

- TypeSafe docs: https://docs.typesafe.ai
- TypeSafe agent skill: https://github.com/typesafe-ai/skills

## License

MIT, see [LICENSE](LICENSE).
