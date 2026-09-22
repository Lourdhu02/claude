# Contributing

Thanks for your interest in this course. This document covers how to report issues, suggest improvements, and — if you want to — submit changes.

---

## Reporting an issue

Open an issue at <https://github.com/Lourdhu02/claude/issues>.

Good issue reports include:
- **What you were doing** — which module, which lab, which step
- **What you expected** — what should have happened
- **What actually happened** — the error message, the wrong output, the confusing section
- **Your setup** — OS, Python version, whether you're using Jupyter or a terminal, the model you pinned (if any)

If you found a typo or a wording issue, that's fine too — open an issue or a PR, whichever you prefer.

---

## Suggesting a new module or topic

Open an issue with the `suggestion` label. Describe:
- What topic or skill is missing
- Who it's for (beginner, intermediate, advanced)
- A rough idea of what the module would cover

You don't have to write the content. A clear problem statement is enough.

Current module gaps that are open for contribution:
- A short "prompt evaluation" exercise — how do you know your prompt is good?
- A "RAG from scratch" walkthrough that builds on Module 09
- A TypeScript version of one or two labs (the concepts transfer; the code doesn't)

---

## Running the labs

1. Clone the repo and follow the setup in the [README](../README.md).
2. Start Jupyter: `jupyter lab`
3. Open the module's `lab.ipynb` and run the cells.
4. If a lab fails, check:
   - Your `ANTHROPIC_API_KEY` is set and valid (`.env` or environment)
   - You have billing credit on your Anthropic account
   - The model name in `.env` matches a model that exists (check the [model docs](https://docs.claude.com/en/docs/about-claude/models))
   - Your `anthropic` package version is recent enough (`pip install -U anthropic`)

---

## Submitting a pull request

Small PRs are welcome: typo fixes, clearer wording, corrected code examples, new exercises.

Before submitting:
1. Fork the repo and create a branch from `main`.
2. Make your change. If it's a code change, run the relevant lab cell to confirm it still works.
3. Open a PR against `main` with a short description of what changed and why.

For larger changes (a new module, a substantial rewrite of an existing module), open an issue first to discuss the approach before spending time on the implementation.

### Style notes

- **Python 3.10+**. Don't use features newer than 3.10 without noting it.
- **Follow the existing module structure**: `README.md` (lesson) + `lab.ipynb` (hands-on) + `exercises.md` (problems).
- **Prefer concrete over abstract**: a worked example beats a paragraph of explanation.
- **Link to docs**: when you quote a limit, price, or capability, link to the current Anthropic docs. Things change.
- **Mermaid for diagrams**, tables for comparisons. Consistency with the rest of the repo.

---

## Code of Conduct

Be respectful and constructive. This is a learning resource — treat issue discussions and PR comments as you would a good code review: specific, kind, and focused on the work. See [SECURITY.md](./SECURITY.md) for reporting security issues privately.
