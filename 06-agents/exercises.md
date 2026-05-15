# Module 06 — Exercises

## 1. Step budget
Add a hard step budget to your agent loop. Verify it breaks cleanly and returns a partial answer when exceeded.

## 2. Plan tag enforcement
Build an agent that MUST emit `<plan>` before the first tool call. Detect missing plans and reject (force a re-run with a system reminder).

## 3. Web-search subagent
Hand-roll a subagent that takes a query and returns the top 3 hits (mocked). The parent agent uses it to research a topic, then writes a summary. Show parent context stays small (token counts).

## 4. Cost tracker
Track cumulative `usage` across all calls in a loop. Stop the agent if estimated cost exceeds $0.10. Print a per-step cost breakdown at the end.

## 5. Reflexion loop
Build a code-writing agent that:
1. Drafts code.
2. Runs tests (mocked: pretend a `run_tests(code)` tool returns pass/fail).
3. If failure, critiques and retries up to 3 times.

## 6. Compare hand-rolled vs SDK
Reimplement one of the above exercises using the Claude Agent SDK. Compare lines of code, readability, and whether the SDK pattern would scale to multi-agent.

## 7. Goal injection
Run a 15-step agent and watch its outputs. Does it drift from the original goal? Try re-injecting the goal into the system prompt at step 5 and 10. Compare drift.
