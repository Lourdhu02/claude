"""Tool definitions and implementations for the capstone.

TODO: replace mocked web_search with a real provider (e.g. Tavily, Brave, SerpAPI)
when you're ready to plug into the live internet. Until then, the mock keeps
the orchestrator deterministic for evals.
"""

import ast
import math


# ---------- mocked knowledge base for web_search --------------------------------

_INDEX = {
    "population of tokyo":   "Tokyo metropolitan population: ~13.96 million (2024).",
    "population of paris":   "Paris commune population: ~2.10 million (2024).",
    "population of lagos":   "Lagos metropolitan population: ~15.4 million (2024).",
    "speed of light":        "c = 299,792,458 m/s in vacuum.",
    "earth radius":          "Mean Earth radius ≈ 6,371 km.",
    "boiling point water":   "Water boils at 100°C / 212°F at 1 atm.",
}


def web_search(query: str) -> str:
    q = query.strip().lower()
    for k, v in _INDEX.items():
        if k in q:
            return v
    return "no results — try a different phrasing"


# ---------- safe calculator -----------------------------------------------------

_FUNCS = {"sqrt": math.sqrt, "log": math.log, "log10": math.log10}


def calculator(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")

    def walk(n):
        if isinstance(n, ast.Expression): return walk(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp):
            l, r = walk(n.left), walk(n.right)
            return {ast.Add: l + r, ast.Sub: l - r, ast.Mult: l * r,
                    ast.Div: l / r, ast.Pow: l ** r, ast.Mod: l % r}[type(n.op)]
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -walk(n.operand)
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id in _FUNCS):
            return _FUNCS[n.func.id](*(walk(a) for a in n.args))
        raise ValueError(f"unsupported node: {ast.dump(n)}")

    return str(walk(tree))


# ---------- tool schemas (registered with Anthropic API) ------------------------

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search a curated index of factual snippets. Returns one short snippet. "
            "Use for factual lookups (populations, constants, definitions). "
            "Do not chain >3 searches per question."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Concise search query."},
            },
            "required": ["query"],
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"},
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate an arithmetic expression. Supports + - * / ** % and sqrt(), log(), log10()."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '17 * (3.5 + 2)'"},
            },
            "required": ["expression"],
        },
        "cache_control": {"type": "ephemeral", "ttl": "1h"},
    },
]

# Map names back to Python callables
TOOL_FNS = {
    "web_search": web_search,
    "calculator": calculator,
}
