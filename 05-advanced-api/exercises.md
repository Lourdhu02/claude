# Module 05 — Exercises

## 1. Cache write vs read
Send the same large (~3K token) system prompt twice with a cache_control breakpoint. Print `cache_creation_input_tokens` and `cache_read_input_tokens` for both calls. Verify the 2nd call shows reads, not writes.

## 2. Cache invalidation
Change one character in the cached prefix and resend. Show that the cache is invalidated (write count returns).

## 3. Three breakpoints
Build a request with three cache breakpoints: system prompt, tool defs, and a large document. Confirm all three layers cache.

## 4. Batch micro-experiment
Submit a batch of 20 single-question requests. Poll until done. Measure: total wall-clock, total cost, vs sequential (don't actually run sequential — estimate).

## 5. Thinking vs not
On a problem like "How many trailing zeros does 100! have?" — run with and without extended thinking. Compare correctness, latency, total tokens, and *cost*.

## 6. Routing with Haiku
Build a tiny router: Haiku decides whether a question is "math", "code", or "chat", then you dispatch to Sonnet with a different system prompt per category. Measure latency / cost vs always-Sonnet.

## 7. Pydantic + forced tool
Define a Pydantic model `MeetingNotes` with attendees, decisions, action_items. Use `model_json_schema()` to populate a forced tool. Round-trip an example transcript and parse the result into the Pydantic type.
