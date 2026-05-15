# Module 02 — Exercises

## 1. Build the Conversation class
Implement the `Conversation` class from §3, but add:
- `.reset()` to clear history.
- `.token_budget` — stop accepting new turns when total context tokens > 80% of the window. (Use `count_tokens`.)

## 2. Streaming TTFB
Measure **time to first byte** (the first `content_block_delta` event) for a 500-word generation. Compare against the same prompt non-streamed. Why is streaming worth it for UX?

## 3. Stop sequence trick
Use `stop_sequences=["</answer>"]` with a prompt that tells the model to wrap its answer in `<answer>...</answer>`. Capture only the inside.

## 4. Determinism check
At `temperature=0`, run the same prompt 5 times. Are the outputs identical? Why or why not?

## 5. Retry-aware wrapper
Wrap `client.messages.create` so it:
- Retries on 5xx and 429 with exponential backoff (max 5 tries).
- Logs each retry with the attempt number and error type.
- Does NOT retry on 400/401.

## 6. Token budget guard
Given a long document, write a function `fit_to_context(doc: str, max_input_tokens: int) -> str` that uses `count_tokens` and truncates the doc to fit. Truncate from the *middle*, not the end — beginning and end matter most for summarization.

## 7. Run-length test
Set `max_tokens=4096` and ask for "a 2000-word essay." Compare actual output length, `stop_reason`, and `usage.output_tokens`. Does the model know how to hit length targets?
