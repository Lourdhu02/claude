# CHANGELOG

All notable changes to this course are documented here. Format is loosely based on [Keep a Changelog](https://keepachangelog.com/).

---

## [2026-09-22]

### Added
- `prompts.md` — reusable system prompt library (code assistant, data analysis, creative writing, document Q&A, brainstorming, generic)
- `workflows.md` — step-by-step workflows for code review, documentation generation, testing, and debugging
- `CONTRIBUTING.md` — how to report issues, suggest modules, run labs, submit PRs
- `SECURITY.md` — private vulnerability reporting policy
- `ROADMAP.md` — current priorities, next-month and quarterly plans, longer-term ideas
- `08-claude-code/examples/skills/triage/SKILL.md` — copy-pasteable triage skill example
- `08-claude-code/examples/settings.json` — copy-pasteable hooks configuration (bash logger + post-edit linter)
- `.github/workflows/monthly-release.yml` — GitHub Actions workflow: cuts a monthly release on the 1st from the CHANGELOG's Unreleased section
- `scripts/release.sh` — manual release CLI (`--dry-run`, `--version`, no args)

### Changed
- README: ASCII banner (title + tagline), Shields badges (Python, MIT, SDK, Jupyter), features strip, **What you'll build** milestone table, **Troubleshooting & FAQ** (7 Q&As), **Claude Projects** table linking to prompts.md and workflows.md
- Module 08 README: new sections 13 (custom skill worked example) and 14 (starter hooks configuration), with inline examples and "what makes this good" notes

### Fixed
- README footer: replaced dangling "Claude Projects: Prompts, Workflows, Integration" stubs with a real assets table

---

## [Unreleased]

---

## [2026-09-01]

### Added
- Module 08: Claude Code CLI — lab, exercises, README
- Module 09: Production — evals, cost/latency, RAG, guardrails, observability
- Module 10: Capstone — end-to-end agentic assistant project

### Updated
- README: added model cheat sheet, repository layout, conventions, learning path diagram
- `resources/glossary.md` — expanded with agent, MCP, prompt caching, extended thinking, tool use loop, and more
- `.env.example` — added `ANTHROPIC_MODEL` and `ANTHROPIC_FAST_MODEL` pins

---

## [2026-08-01]

### Added
- Module 07: MCP — lab, exercises, README, `server.py`
- Module 06: Agents & Agent SDK — lab, exercises, README
- Module 05: Advanced API — prompt caching, batch, extended thinking, model selection

### Updated
- README: expanded module table, added model cheat sheet
- `requirements.txt` — added pandas, scikit-learn for Module 09 evals

---

## [2026-07-01]

### Added
- Module 04: Multimodal & files — vision, PDFs, Files API, citations
- Module 03: Tool use — tool definitions, tool loop, parallel & structured outputs

### Updated
- Glossary: added tool use, tool_use block, tool_choice, stop reasons

---

## [2025-06-01]

### Added
- Module 02: Messages API — streaming, multi-turn, token counting, errors, retries
- Module 01: Prompting — system prompts, XML tags, few-shot, chain-of-thought
- Module 00: Foundations — first request, model family, Messages API overview

### Updated
- Initial project structure: 10 module directories, `resources/`, `requirements.txt`, `.env.example`
- LICENSE: MIT
- README: project overview, setup instructions, learning path

---

## About this changelog

- Each month on the first Saturday, a new entry is added for anything that changed since the last release.
- Minor typo fixes and wording tweaks are grouped under the month's "Updated" section.
- Breaking changes (e.g., a module that no longer works with a new SDK version) are called out explicitly under "Breaking".
