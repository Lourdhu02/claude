# Roadmap

What's planned for this course, what's being worked on, and what's next. Updated monthly.

---

## Vision

A self-paced course that takes a Python engineer from "I've heard of Claude" to "I can build and ship a production-grade Claude-powered application" — with real labs, real exercises, and content that stays current with the API.

---

## Now (this month)

- [x] Prompt library (`prompts.md`) — reusable system prompts for common use cases
- [x] Workflow library (`workflows.md`) — code review, docs, testing, debugging
- [ ] README refresh — badges, 5-minute quick start, clearer hook
- [ ] Contributor guide (`CONTRIBUTING.md`) — how to report issues, suggest modules, run labs

## Next month

- [ ] Add a "what you'll build" section to the README — describe the capstone and a couple of intermediate project ideas
- [ ] Add a troubleshooting / FAQ section to the README (common errors, API key issues, model selection questions)
- [ ] Add visual samples — screenshots of a lab notebook running, sample terminal output in Module 00
- [ ] Module 08 deep-dive: add a custom skill example and a hooks configuration example to the Claude Code module

## This quarter

- [ ] Add a "VS Code / JetBrains setup" note to the setup section — how to use the course with an IDE, not just Jupyter
- [ ] Add a "running without a key" note — explain the free tier, what you can trial, and what requires billing
- [ ] Add a lightweight test for the capstone app (Module 10) so the project ships with a working test suite
- [ ] Expand Module 09 with a concrete evals example (a small rubric + a scored run)

## Longer-term ideas

- [ ] A short "Claude for non-Python engineers" note — how to apply the concepts in TypeScript, Go, or via the REST API directly
- [ ] A "cost calculator" notebook — estimate monthly cost for a hypothetical app given expected request volume
- [ ] A glossary of common mistakes — "things I see engineers get wrong with Claude" (e.g., sending the whole history every turn without truncation, not handling tool_use stop reasons, assuming the model can see files you uploaded to your computer)
- [ ] Video companion snippets — short screen-captures of a lab notebook running (optional, community-driven)

---

## How to suggest something

Open an issue with the label `suggestion` and describe:
- What's missing or unclear
- Who it's for
- A rough idea of what it would look like

You don't need to write the content — an issue that says "Module 03 doesn't explain parallel tool calls clearly" is enough to get started. See [CONTRIBUTING.md](./CONTRIBUTING.md).
