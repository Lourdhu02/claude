"""Input and output guardrails for the capstone."""

import re

MAX_INPUT_CHARS = 4000
SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9-_]+"),     # API keys
    re.compile(r"AKIA[0-9A-Z]{16}"),          # AWS access keys
]


def validate_input(text: str) -> str:
    """Raise ValueError if input is unacceptable. Return cleaned text otherwise."""
    if not text or not text.strip():
        raise ValueError("empty input")
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(f"input too long ({len(text)} > {MAX_INPUT_CHARS} chars)")
    return text.strip()


def redact_output(text: str) -> str:
    """Strip well-known secret patterns from outputs as a safety net."""
    out = text
    for pat in SECRET_PATTERNS:
        out = pat.sub("[REDACTED]", out)
    return out


def quarantine(label: str, untrusted: str) -> str:
    """Wrap untrusted third-party text so the model is reminded it's not instructions."""
    return f"<{label}>\n{untrusted}\n</{label}>"
