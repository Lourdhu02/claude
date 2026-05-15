# Module 03 — Exercises

## 1. Calculator tool
Build a `calculator` tool that takes `{expression: str}` and evaluates it safely (use `ast.literal_eval` or a small parser — NOT `eval`). Wire it into the loop from §3 of the README. Test with "what is 17 * 23 + sqrt(144)?"

## 2. Forced structured output
Take a paragraph of free text describing a person ("Maya, 34, lives in Pune, works as a data scientist…") and use a forced tool to extract `{name, age, city, role}`. Validate with Pydantic.

## 3. Multiple tools, model picks
Provide three tools: `get_weather`, `search_news`, `calculator`. Ask one question that triggers each. Confirm the model picks correctly.

## 4. Parallel calls
Ask "What's the weather in Tokyo, London, and Lagos?" and verify Claude emits 3 `tool_use` blocks in one turn. Run them concurrently with `asyncio.gather`.

## 5. Forbid the loop's last tool call
Build a tool loop that allows tool calls *except on the final answer turn*. Set `tool_choice={"type": "none"}` once you've gathered enough info. Test with a 3-step task.

## 6. Tool error recovery
Make `get_weather` randomly return `is_error: true` 30% of the time with message "service unavailable". Does the model retry? Does it try a different tool? Tune the system prompt to influence behavior.

## 7. Token cost
Print `usage.input_tokens` for each turn of a 3-tool-call loop. How many tokens does carrying tool definitions across turns cost? (Hint: caching them is Module 05.)
