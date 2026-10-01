# Presentation

**A System One model inside Claude Code: early experience with Jev**, an internal talk at EPAM Istanbul, 1 October 2026 (20 minutes: about 9 minutes of slides, a 6-minute live demo, then questions).

[EPAM-Istanbul-UgurEmrahSurat.pdf](EPAM-Istanbul-UgurEmrahSurat.pdf), 9 slides.

| # | Slide | Where to find it in this repo |
|---|---|---|
| 1 | A System One model inside Claude Code | |
| 2 | From BERT to System One | |
| 3 | What people are already building with Jev | Links to the four public posts are on the slide |
| 4 | Where System One fits: two industrial patterns | |
| 5 | A real manufacturing use case: failure modes in maintenance logs | [`playground/`](../playground/) has a runnable, invented version of this case |
| 6 | How we would test it: a System 1 pilot | The five questions are in [`playground/questions.json`](../playground/questions.json) |
| 7 | Hands-on tests: Jev vs Haiku 4.5 vs local models | Not published here yet |
| 8 | Over to the terminal | The live demo: the Playground, then [`experiments/01-qualitative-linter/`](../experiments/01-qualitative-linter/) |
| 9 | Thank you | |

Notes:
- **Slide 5** shows an illustrative notification. The field names, values and codes on it are generic, not client data.
- **Slide 7** reports our own measurements on our own data; read it as a worked example, not a leaderboard. The command guard and prompt router behind it are not in this repo yet.
- **Slide 8** still shows the command guard as part of the demo plan. In the talk, the guard was covered by slide 7, and the live demo showed the Playground and the linter.
