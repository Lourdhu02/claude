"""Subagent definitions for the capstone.

The orchestrator delegates focused subtasks here. Subagents:
- Run on smaller/cheaper models when possible.
- Have a narrower tool set.
- Return short text summaries back to the parent (small context footprint).
"""

import os
from anthropic import Anthropic
from tools import TOOLS, TOOL_FNS

_client = Anthropic()
FAST = os.getenv("ANTHROPIC_FAST_MODEL", "claude-haiku-4-5-20251001")


def _run_tools(content):
    out = []
    for b in content:
        if b.type != "tool_use":
            continue
        try:
            r = TOOL_FNS[b.name](**b.input)
            out.append({"type": "tool_result", "tool_use_id": b.id, "content": str(r)})
        except Exception as e:
            out.append({"type": "tool_result", "tool_use_id": b.id,
                        "content": f"ERROR: {e}", "is_error": True})
    return out


def search_agent(query: str, max_steps: int = 3) -> str:
    """Cheap research subagent. Web-search only. Returns a one-paragraph summary."""
    messages = [{"role": "user", "content": query}]
    system = (
        "You are a research subagent. Use web_search to gather facts. "
        "Reply in <=40 words, ending with a citation in parentheses (source). "
        "Do NOT call the calculator."
    )
    search_only = [t for t in TOOLS if t["name"] == "web_search"]

    for _ in range(max_steps):
        r = _client.messages.create(
            model=FAST,
            max_tokens=512,
            system=system,
            tools=search_only,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": r.content})
        if r.stop_reason == "end_turn":
            return "".join(b.text for b in r.content if b.type == "text")
        if r.stop_reason == "tool_use":
            messages.append({"role": "user", "content": _run_tools(r.content)})
            continue
        break
    return "(subagent did not complete)"
