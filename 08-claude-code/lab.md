# Module 08 — Lab: Daily-drive Claude Code

These are hands-on exercises in your real Claude Code install — there's no notebook. Tick them off in your own copy of this file.

## Setup

- [ ] `claude --version` returns a current build.
- [ ] `cd D:\Lourdu-Personal\claude && claude` opens this repo.
- [ ] `/help` shows you the slash-command index.

## 1. The prompt habit

Pick any module's `exercises.md`. Ask Claude Code:

```
> Open 03-tool-use/exercises.md, do exercise 1 in scratch/03_calc.py, run it, and explain what happened.
```

Observe:
- Did it read the file you pointed it at, or wander?
- Did it run the script?
- Did the explanation match the actual run?

## 2. Tighten permissions

Edit `.claude/settings.local.json` (create if missing). Add an allowlist for safe commands you use repeatedly:

```json
{
  "permissions": {
    "allow": ["Bash(pytest:*)", "Bash(python:*)", "Bash(pip install:*)"]
  }
}
```

Run a session and confirm fewer permission prompts.

> Tip: the `fewer-permission-prompts` skill scans your history and suggests an allowlist for you.

## 3. Write a slash command

Create `.claude/commands/quiz.md`:

```markdown
---
description: Quiz me on a module by number.
---

Read `0$1-*/README.md` and ask me 5 questions, one at a time. Mark right/wrong and explain.
```

Invoke `/quiz 3`. It should quiz you on Module 03.

## 4. Author a custom agent

Create `~/.claude/agents/notebook-cleaner.md`:

```markdown
---
name: notebook-cleaner
description: Clean Jupyter notebooks - clear outputs, prune empty cells, fix metadata.
tools: Read, Edit, Bash, Glob
---

You are a notebook hygienist. Given a target .ipynb file or directory, you:
1. Clear all cell outputs.
2. Remove empty cells.
3. Ensure metadata has a Python 3 kernelspec.
4. Re-save in place. Report which files changed.
```

Run `/agents` to confirm it registers, then:

```
> Use the notebook-cleaner agent on 01-prompting/.
```

## 5. Hook practice

Add a `Stop` hook that pings you when Claude finishes:

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "powershell -Command \"[console]::beep(1200,200)\"" } ] }
    ]
  }
}
```

(Use `osascript -e 'beep'` on macOS or `paplay` on Linux.)

Run any session — confirm the beep fires.

## 6. Wire your Module 07 MCP server

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "course-demo": {
      "command": "python",
      "args": ["D:/Lourdu-Personal/claude/07-mcp/server.py"]
    }
  }
}
```

Restart Claude Code. Then:

```
> Use the course-demo `add` tool to compute 17+25.
> Read the resource notes://caching and summarize it.
> Run the slash command /course-demo:code_review with language=Python.
```

## 7. Background work with `/loop`

```
> /loop 10m  Run pytest and report failures since the last run.
```

Open in a separate terminal: `claude --print` for one-off prompts that print results.

## 8. Scheduled agent

```
> /schedule  Each weekday at 9am, summarize git activity since yesterday into a file scratch/standup.md.
```

Inspect with `/schedule list`.

---

## Stretch

- Author your own *skill* under `.claude/skills/my-skill/SKILL.md` and invoke it.
- Pin different models per call-site by setting `model` in settings vs `--model` flag at run time.
- Hook up `security-review` to your CI as a PR comment bot.
