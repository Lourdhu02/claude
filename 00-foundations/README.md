# 00 — Foundations

By the end of this module you can answer:

1. What is Claude, and what's in the family?
2. How does the Messages API work at a high level?
3. Which model do I pick for which job?
4. How do I send my first request?

Time budget: ~45 minutes reading, ~15 minutes lab.

---

## 1. What is Claude

Claude is a family of large language models built by Anthropic. You use Claude through:

- **The Messages API** — a single HTTPS endpoint at `https://api.anthropic.com/v1/messages`. You send a conversation; you get back a response.
- **The Anthropic SDKs** — official wrappers for Python, TypeScript, Go, Java, and more.
- **Claude.ai / claude.com** — the chat product end-users see.
- **Claude Code** — the official CLI / IDE assistant (covered in Module 08).

This course is about building *on top of* Claude — so the API is your primary surface.

---

## 2. The model family

Claude 4.x has three tiers. All are general-purpose; they trade off cost, latency, and intelligence.

```mermaid
graph TB
    subgraph "Claude 4.x family"
      O["Opus 4.7<br/>claude-opus-4-7"]
      S["Sonnet 4.6<br/>claude-sonnet-4-6"]
      H["Haiku 4.5<br/>claude-haiku-4-5-20251001"]
    end
    O -.->|"hardest reasoning<br/>complex agents"| U1[Use it when intelligence > cost]
    S -.->|"workhorse default<br/>most apps"| U2[Use it 80% of the time]
    H -.->|"fast, cheap<br/>classification, routing"| U3[Use it when latency matters]
```

| Capability | Opus 4.7 | Sonnet 4.6 | Haiku 4.5 |
|---|---|---|---|
| Reasoning depth | highest | high | good |
| Speed | slowest | medium | fastest |
| Price | highest | mid | lowest |
| Context window | 200K tokens | 200K tokens | 200K tokens |
| Vision | yes | yes | yes |
| Tool use | yes | yes | yes |
| Extended thinking | yes | yes | yes |

**Rule of thumb**: start every project on **Sonnet 4.6**. Move *down* to Haiku once you've identified hot loops that are simple enough; move *up* to Opus only for the small fraction of calls where intelligence matters more than cost.

> Pricing changes — always check <https://docs.claude.com/en/docs/about-claude/pricing>.

---

## 3. How the Messages API works

At its core, the Messages API takes a **list of messages** and returns **one new assistant message**.

```mermaid
sequenceDiagram
    participant App
    participant API as Messages API
    participant Model as Claude

    App->>API: POST /v1/messages<br/>{ model, system, messages, max_tokens }
    API->>Model: route to selected model
    Model-->>API: assistant content blocks
    API-->>App: response (id, content, usage, stop_reason)
```

A request has three core inputs:

| Field | What it is |
|---|---|
| `model` | Which Claude model to use, e.g. `claude-sonnet-4-6`. |
| `system` | Top-level instructions ("You are a helpful Python tutor."). Separate from `messages`. |
| `messages` | An alternating list of `{role: "user"|"assistant", content: ...}`. |
| `max_tokens` | Maximum tokens to generate in the *response*. **Required.** |

A response includes:

| Field | What it is |
|---|---|
| `id` | Unique response ID. |
| `content` | A list of content blocks (text, tool_use, thinking, etc.). |
| `usage` | `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`. |
| `stop_reason` | Why generation ended: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`. |
| `model` | The model that actually served the request. |

That's the whole shape. Everything else in the course — tools, vision, streaming, caching — is just additional fields layered on top of this skeleton.

---

## 4. Anatomy of a conversation

Messages alternate roles. The model itself is stateless: every request, you send the *entire* conversation history.

```python
messages = [
    {"role": "user",      "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris."},
    {"role": "user",      "content": "And of Japan?"},
]
```

You'll send these along with your `system` prompt and get a new assistant turn back. To continue, append the response to `messages` and send again.

---

## 5. Getting an API key

1. Go to <https://console.anthropic.com/>.
2. Sign in, then open **Settings → API keys**.
3. Click **Create Key** and copy the value (starts with `sk-ant-`). You won't see it again.
4. Paste it into your local `.env` file:

   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. Add billing credit at **Settings → Plans & Billing**. Without credit, requests will 429.

The SDK reads `ANTHROPIC_API_KEY` from the environment automatically.

---

## 6. Your first request

The shortest useful Claude script in Python:

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()  # reads ANTHROPIC_API_KEY from env

response = client.messages.create(
    model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
    max_tokens=256,
    system="You answer in one short sentence.",
    messages=[{"role": "user", "content": "What is prompt engineering?"}],
)

print(response.content[0].text)
print(f"\n[tokens: in={response.usage.input_tokens} out={response.usage.output_tokens}]")
```

Run it in the lab notebook.

---

## 7. What "content blocks" are

Every assistant response is a *list* of typed blocks, not a single string. In the beginner case it's one `text` block. As you add features, the list grows:

| Block type | When it appears |
|---|---|
| `text` | Always (unless the model only emitted tool calls). |
| `tool_use` | Model wants to call a tool you defined. |
| `thinking` | When extended thinking is enabled. |
| `image` | Only on the *input* side. |
| `document` | PDFs / files on the input side. |

So `response.content[0].text` works only when the first block is text. Production code should iterate `response.content` and switch on `block.type`.

---

## 8. Common errors you'll hit early

| HTTP | Meaning | Fix |
|---|---|---|
| 401 | bad / missing key | check `.env`, restart kernel |
| 429 | rate limited | back off + retry; check billing |
| 400 | bad request | usually missing `max_tokens` or wrong message shape |
| 529 | overloaded | retry with backoff |

The official SDK already implements retries for transient errors.

---

## 9. Where to look next

- Module 01 teaches you to write the `system` prompt and `messages` so the model does what you want.
- Module 02 takes the Messages API apart parameter by parameter.

Then open [`lab.ipynb`](./lab.ipynb) to run your first request, and [`exercises.md`](./exercises.md) to practice.

---

## References

- API reference: <https://docs.claude.com/en/api/messages>
- Pricing: <https://docs.claude.com/en/docs/about-claude/pricing>
- Models overview: <https://docs.claude.com/en/docs/about-claude/models>
