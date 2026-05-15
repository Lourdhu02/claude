# 02 — Messages API deep dive

By the end you can:

1. Map every Messages API parameter to a use case.
2. Stream responses and handle SSE events.
3. Run reliable multi-turn conversations.
4. Handle errors and rate limits without losing your mind.

Time budget: ~60 minutes reading, ~45 minutes lab.

---

## 1. The full request shape

```python
client.messages.create(
    model="claude-sonnet-4-6",     # required
    max_tokens=1024,               # required
    messages=[...],                # required
    system="...",                  # optional, str OR list[content_block]
    temperature=1.0,               # 0.0-1.0
    top_p=None,                    # nucleus sampling, mutually exclusive w/ temperature in practice
    top_k=None,                    # rarely useful
    stop_sequences=["</answer>"],  # up to 4
    metadata={"user_id": "..."},   # opaque to the model; for your logs
    stream=False,                  # see §4
    tools=[...],                   # Module 03
    tool_choice={"type": "auto"},  # Module 03
    thinking={"type": "enabled"},  # Module 05
)
```

Key things to internalize:

| Param | Use |
|---|---|
| `model` | Pin a specific version; never default in production. |
| `max_tokens` | Ceiling on **output** tokens only. Always set this lower than you think you need; it's a safety lid, not a target. |
| `temperature` | 0.0 = deterministic-ish (still some variance); 0.7+ = creative. For extraction/classification use 0; for writing use 0.7–1.0. |
| `stop_sequences` | Up to 4 strings. Generation halts when any is produced. Useful with prefill. |
| `metadata.user_id` | Helps Anthropic with abuse signals; doesn't influence output. |

> `temperature` and `top_p` both exist, but in practice you only tune `temperature`. Setting both confuses the sampling distribution and is rarely useful.

---

## 2. The full response shape

```json
{
  "id": "msg_01ABCxyz...",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-6",
  "content": [
    {"type": "text", "text": "..."}
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 124,
    "output_tokens": 87,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

| `stop_reason` | Meaning |
|---|---|
| `end_turn` | Model finished naturally — most common. |
| `max_tokens` | You hit your `max_tokens` cap. Probably truncated. |
| `stop_sequence` | A `stop_sequences` entry matched. |
| `tool_use` | Model wants to call a tool; loop continues (Module 03). |
| `pause_turn` | Long-running operation paused (Module 06 agents). |

Always check `stop_reason`. Treating every response as `end_turn` masks truncation bugs that only show up in prod.

---

## 3. Building multi-turn correctly

Pattern: a `Conversation` class that owns the message list and appends model responses.

```python
class Conversation:
    def __init__(self, system: str, model: str):
        self.system = system
        self.model = model
        self.messages: list[dict] = []

    def ask(self, user_text: str, **kw) -> str:
        self.messages.append({"role": "user", "content": user_text})
        r = client.messages.create(
            model=self.model,
            system=self.system,
            max_tokens=1024,
            messages=self.messages,
            **kw,
        )
        # Append the assistant turn so the next user msg has full history.
        self.messages.append({"role": "assistant", "content": r.content})
        return "".join(b.text for b in r.content if b.type == "text")
```

Notes:
- Append the **raw content blocks** (`r.content`), not a stringified version. That preserves tool calls, thinking, etc. for future turns.
- Trim the history before it exceeds the context window. Common strategies: keep last N turns, summarize older turns, or use a rolling window with pinned system prompt.

---

## 4. Streaming

For chat UIs and long outputs, stream the response so users see tokens as they arrive.

```python
with client.messages.stream(
    model=MODEL,
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a 5-sentence story."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    final = stream.get_final_message()  # full Message object after stream completes
```

For finer control, iterate raw events:

```python
with client.messages.stream(model=MODEL, max_tokens=512, messages=[...]) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            ...
        elif event.type == "message_stop":
            ...
```

| Event | When |
|---|---|
| `message_start` | Stream began; carries initial usage. |
| `content_block_start` | New content block (text, tool_use, thinking) starting. |
| `content_block_delta` | Incremental chunk. |
| `content_block_stop` | Block finished. |
| `message_delta` | Mid-stream usage/stop_reason updates. |
| `message_stop` | Stream done; final message available. |

Streaming doesn't change pricing — same input/output tokens, just delivered incrementally.

---

## 5. Counting tokens before you spend money

```python
r = client.messages.count_tokens(
    model=MODEL,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": doc_text}],
    tools=tools,   # if you have them
)
print(r.input_tokens)
```

Use this to:
- Pre-flight a long prompt against your model's context window.
- Estimate cost before a batch run.
- Decide which chunks to include in a RAG pipeline.

---

## 6. Errors and retries

The SDK auto-retries `429`, `500`, `502`, `503`, `529` with exponential backoff and `Retry-After` honored. You normally don't need your own retry layer.

When you do need custom retry (e.g. across a queue worker restart), use `tenacity`:

```python
from anthropic import APIError, APIStatusError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    retry=retry_if_exception_type((APIStatusError,)),
    wait=wait_exponential(min=1, max=30),
    stop=stop_after_attempt(5),
)
def safe_call(**kw):
    return client.messages.create(**kw)
```

| Error | Action |
|---|---|
| `APIConnectionError` | Network. Retry with backoff. |
| `RateLimitError` (429) | SDK handles; if you see it, you exhausted retries. Reduce concurrency. |
| `APIStatusError` 5xx | Server-side. Retry with backoff. |
| `BadRequestError` 400 | Your fault. Don't retry — fix the request. |
| `AuthenticationError` 401 | Bad key. Don't retry. |

---

## 7. Cancellation and timeouts

```python
client = Anthropic(timeout=30.0, max_retries=3)
# Or per-call:
client.messages.create(..., timeout=10.0)
```

For long-running streamed responses, wrap the `with` block in your own task and cancel it. The SDK respects `httpx` cancellation.

---

## 8. Choosing parameters: a cheat sheet

| Task | model | temperature | max_tokens | stop_sequences |
|---|---|---|---|---|
| Extraction / classification | Haiku 4.5 or Sonnet 4.6 | 0 | tight (50–200) | optional |
| Code generation | Sonnet 4.6 | 0.2–0.5 | generous (1–4K) | none |
| Long-form writing | Sonnet 4.6 / Opus 4.7 | 0.7–1.0 | budget | none |
| Reasoning / math | Sonnet 4.6 + thinking | 1.0 (default w/ thinking) | thinking + 1K answer | none |
| Routing / triage in a hot loop | Haiku 4.5 | 0 | 16 | none |

---

## 9. What to do with the lab

[`lab.ipynb`](./lab.ipynb) walks through streaming, a multi-turn class, error/retry handling, and token counting on a long document.

---

## References

- API reference (messages): <https://docs.claude.com/en/api/messages>
- Streaming: <https://docs.claude.com/en/api/messages-streaming>
- Errors: <https://docs.claude.com/en/api/errors>
- Token counting: <https://docs.claude.com/en/api/messages-count-tokens>
