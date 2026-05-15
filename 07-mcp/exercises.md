# Module 07 — Exercises

## 1. Add a new tool
Extend `server.py` with a `read_file(path: str) -> str` tool. Make it safe: refuse paths outside a sandbox directory. Validate with adversarial inputs like `../etc/passwd`.

## 2. Add a resource list
Add a resource `notes://` (no parameter) that lists all known note topics as JSON. Useful for discovery.

## 3. New prompt
Write a `debug_python(traceback: str)` prompt that produces a structured debugging plan.

## 4. Local client
Write a small Python script using the `mcp` client library that connects to your server over stdio and:
- Lists all tools, resources, prompts.
- Calls `add(2, 3)`.
- Reads `notes://rag`.

## 5. Auth a remote server
Spin up the server in HTTP mode (`transport='streamable-http'`). Add a fake bearer-token check on requests. Demonstrate a 401 when missing.

## 6. Cross-client test
Wire the same server into Claude Code via `~/.claude.json`. Confirm tools show up via `/mcp` and that calling `add` from a Claude Code session works identically.

## 7. Security audit
List three injection or exfiltration risks specific to your server. For each, write a one-line mitigation.
