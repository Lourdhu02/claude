# Module 00 — Exercises

Work through these in `lab.ipynb` or a scratch script. Solutions at the bottom — try first.

## 1. Hello, Claude
Send a request to `claude-sonnet-4-6` asking it to return the string `"pong"` and nothing else. Print only the text content.

## 2. Inspect the full response
Call `response.model_dump_json(indent=2)` on a response and read every field. Identify:
- `stop_reason`
- `usage.input_tokens` vs `usage.output_tokens`
- `id` and `type`

## 3. Multi-turn
Build a 3-turn conversation:
1. user: "Pick a number between 1 and 10."
2. assistant: (model's first answer)
3. user: "Now double it."

Send the conversation in *one* call by including the assistant's first reply in `messages`.

## 4. Model swap
Re-run exercise 1 with `claude-haiku-4-5-20251001`. Compare:
- Latency (use `time.perf_counter()`).
- Output tokens.
- The actual text.

## 5. System prompt
Set `system="You only respond in haiku."` Send any user question. Confirm the output is three short lines.

## 6. Break it
Send a request with `max_tokens=8`. Inspect `stop_reason`. Why does it stop there? When would you intentionally cap tokens this hard?

## 7. Token counting (preview)
Without sending a request, estimate the input tokens of `"the quick brown fox jumps over the lazy dog"` using `client.messages.count_tokens(...)`. Compare your estimate to what an actual request reports.

---

## Solutions

<details>
<summary>1. Hello, Claude</summary>

```python
from anthropic import Anthropic
client = Anthropic()

r = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16,
    messages=[{"role": "user", "content": "Reply with exactly the word: pong"}],
)
print(r.content[0].text)
```
</details>

<details>
<summary>3. Multi-turn</summary>

```python
messages = [
    {"role": "user", "content": "Pick a number between 1 and 10."},
    {"role": "assistant", "content": "7"},
    {"role": "user", "content": "Now double it."},
]
r = client.messages.create(model="claude-sonnet-4-6", max_tokens=32, messages=messages)
print(r.content[0].text)
```
</details>

<details>
<summary>6. Break it</summary>

`stop_reason` will be `"max_tokens"` — the model wanted to keep going but you cut it off. You'd cap this hard when you only want a single token classification (e.g. "yes"/"no" routing in a hot loop) and need predictable latency/cost.
</details>

<details>
<summary>7. Token counting</summary>

```python
r = client.messages.count_tokens(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "the quick brown fox jumps over the lazy dog"}],
)
print(r.input_tokens)
```
</details>
