"""
Minimal MCP server demo for Module 07.

Run standalone:
    pip install mcp
    python server.py

Wire into Claude Code by adding to ~/.claude.json:
    {
      "mcpServers": {
        "course-demo": {
          "command": "python",
          "args": ["D:/Lourdu-Personal/claude/07-mcp/server.py"]
        }
      }
    }
"""

from mcp.server.fastmcp import FastMCP

app = FastMCP("course-demo")


# --- Tools (with side effects, the model can call) -----------------------------

@app.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


@app.tool()
def word_count(text: str) -> int:
    """Count whitespace-separated words in a string."""
    return len(text.split())


# In-memory KV store for the resource demo
_NOTES: dict[str, str] = {
    "rag":     "RAG = retrieval-augmented generation. Retrieve, then generate grounded in retrieved docs.",
    "caching": "Prompt caching gives ~10x discount on read for stable prefixes. Up to 4 breakpoints.",
}


@app.tool()
def save_note(topic: str, body: str) -> str:
    """Persist a note under a topic key (overwrites)."""
    _NOTES[topic.lower()] = body
    return f"saved: {topic}"


# --- Resources (read-only, addressable by URI) ---------------------------------

@app.resource("notes://{topic}")
def read_note(topic: str) -> str:
    """Read the note stored under `topic`."""
    return _NOTES.get(topic.lower(), f"(no note for {topic!r})")


# --- Prompts (templates user can invoke as slash commands) ---------------------

@app.prompt()
def code_review(language: str) -> str:
    """Generate a code review prompt for `language`."""
    return (
        f"You are a senior {language} reviewer. Review the following code for:\n"
        f"1. Correctness bugs.\n"
        f"2. Style and idiomaticity.\n"
        f"3. Performance gotchas.\n\n"
        f"Reply with markdown bullets grouped by category."
    )


if __name__ == "__main__":
    # Defaults to stdio. For HTTP transport: app.run(transport='streamable-http').
    app.run()
