"""Capstone orchestrator: a planning, tool-using, subagent-spawning research assistant.

Run via cli.py. This module is import-safe (no side effects)."""

import os
import time
import json
import logging
from dataclasses import dataclass, field
from anthropic import Anthropic, APIStatusError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from tools import TOOLS, TOOL_FNS
from subagents import search_agent
from schemas import REPORT_TOOL, Report
from guardrails import validate_input, redact_output

log = logging.getLogger("assistant")

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SYSTEM = [
    {
        "type": "text",
        "text": (
            "You are a meticulous research assistant. Your goal is to answer the user's "
            "question accurately and concisely, citing sources.\n\n"
            "Process:\n"
            "1. Briefly emit a <plan>2-3 step plan</plan>.\n"
            "2. Use tools to gather facts. Prefer `research` (subagent) for factual lookups "
            "   and `calculator` for math. Do NOT make up facts.\n"
            "3. When you have enough information, call `deliver_report` exactly once with "
            "   the final structured report. Do not respond with free text after that.\n\n"
            "Rules: never invent citations; if uncertain, set confidence=low and say so."
        ),
        "cache_control": {"type": "ephemeral", "ttl": "1h"},
    }
]

# Expose subagent as a tool to the orchestrator.
ORCH_TOOLS = [
    {
        "name": "research",
        "description": (
            "Delegate a factual lookup to a fast research subagent. Returns a short summary "
            "with a citation. Prefer this over directly searching for factual questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"question": {"type": "string"}},
            "required": ["question"],
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"},
    },
    *TOOLS,
    REPORT_TOOL,  # forced final output schema
]


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read: int = 0
    cache_write: int = 0

    def add(self, u):
        self.input_tokens  += u.input_tokens or 0
        self.output_tokens += u.output_tokens or 0
        self.cache_read    += getattr(u, "cache_read_input_tokens", 0) or 0
        self.cache_write   += getattr(u, "cache_creation_input_tokens", 0) or 0


@retry(
    retry=retry_if_exception_type((APIStatusError,)),
    wait=wait_exponential(min=1, max=20),
    stop=stop_after_attempt(4),
    reraise=True,
)
def _create(client, **kw):
    return client.messages.create(**kw)


def _dispatch_tool(block):
    if block.name == "research":
        return search_agent(block.input["question"])
    fn = TOOL_FNS.get(block.name)
    if fn is None:
        raise ValueError(f"unknown tool: {block.name}")
    return fn(**block.input)


def run(question: str, *, max_steps: int = 10, max_cost_usd: float = 0.50) -> dict:
    """Return a dict: {report: Report dict, usage: Usage, steps: int, ok: bool, reason: str}."""
    question = validate_input(question)
    client = Anthropic()
    usage = Usage()

    messages = [{"role": "user", "content": question}]

    for step in range(max_steps):
        r = _create(
            client,
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM,
            tools=ORCH_TOOLS,
            messages=messages,
        )
        usage.add(r.usage)
        messages.append({"role": "assistant", "content": r.content})

        # Look for the report-tool call to terminate.
        report_call = next(
            (b for b in r.content if b.type == "tool_use" and b.name == "deliver_report"),
            None,
        )
        if report_call is not None:
            report = Report(**report_call.input).model_dump()
            report["answer"] = redact_output(report["answer"])
            return {"ok": True, "report": report, "usage": usage, "steps": step + 1, "reason": "delivered"}

        if r.stop_reason == "tool_use":
            tool_results = []
            for b in r.content:
                if b.type != "tool_use":
                    continue
                try:
                    out = _dispatch_tool(b)
                    tool_results.append({"type": "tool_result", "tool_use_id": b.id, "content": str(out)})
                except Exception as e:
                    log.warning("tool %s failed: %s", b.name, e)
                    tool_results.append({"type": "tool_result", "tool_use_id": b.id,
                                          "content": f"ERROR: {e}", "is_error": True})
            messages.append({"role": "user", "content": tool_results})
            continue

        if r.stop_reason == "end_turn":
            # Model gave up without calling deliver_report. Salvage what we have.
            text = "".join(b.text for b in r.content if b.type == "text")
            return {"ok": False, "report": {"answer": text}, "usage": usage,
                    "steps": step + 1, "reason": "ended_without_report"}

        return {"ok": False, "report": None, "usage": usage,
                "steps": step + 1, "reason": f"stop:{r.stop_reason}"}

    return {"ok": False, "report": None, "usage": usage,
            "steps": max_steps, "reason": "step_budget"}
