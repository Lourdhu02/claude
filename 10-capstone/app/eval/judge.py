"""LLM-as-judge grader for the capstone eval."""

import os
import json
from anthropic import Anthropic

_client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

JUDGE_SYSTEM = """You are a strict grader. Reply ONLY as JSON:
{"correct": bool, "cited": bool, "confident_appropriate": bool, "notes": "<= 20 words"}.

Score the candidate report against the rubric. Be unforgiving."""


def judge(question: str, rubric: str, must_contain: list[str], report: dict) -> dict:
    must_ok = all(any(s in (report.get("answer", "") + " " + " ".join(report.get("bullets", [])))
                       for s in [m]) for m in must_contain)
    body = json.dumps(report, indent=2)
    msg = (
        f"<question>{question}</question>\n"
        f"<rubric>{rubric}</rubric>\n"
        f"<must_contain>{must_contain}</must_contain>\n"
        f"<candidate>{body}</candidate>\n"
        f"<must_contain_check>{must_ok}</must_contain_check>"
    )
    r = _client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": msg}],
    )
    text = r.content[0].text.strip()
    if not text.startswith("{"):
        text = "{" + text.split("{", 1)[1]
    verdict = json.loads(text)
    verdict["must_contain_ok"] = must_ok
    return verdict
