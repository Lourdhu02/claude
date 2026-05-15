# Capstone app — Research Assistant

A streaming CLI research assistant. See parent module's [`README.md`](../README.md) for the full design.

## Setup

```bash
cd ../..                # repo root
pip install -r requirements.txt
cp .env.example .env    # add your key
```

## Run

```bash
cd 10-capstone/app
python cli.py "How many people live in Tokyo, and what is that divided by 100?"
```

## Evaluate

```bash
python eval/run.py
```

Prints overall accuracy + per-row results, writes `eval/scores.csv`.

## Files

| File | What |
|---|---|
| `assistant.py` | Orchestrator agent loop |
| `tools.py` | Tool schemas + (mocked) implementations |
| `subagents.py` | Search subagent (Haiku) |
| `schemas.py` | Pydantic report schema |
| `guardrails.py` | Input/output filters |
| `cli.py` | Streaming CLI entrypoint |
| `eval/set.jsonl` | Eval dataset |
| `eval/judge.py` | LLM-as-judge grader |
| `eval/run.py` | Run + score |

Stretch ideas in the parent README.
