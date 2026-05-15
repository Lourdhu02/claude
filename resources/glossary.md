# Glossary

A running reference of terms that show up across the course. Add to it as you go.

| Term | Definition |
|---|---|
| **Agent** | An LLM in a loop that can take actions via tools, observe results, and decide what to do next until it reaches a goal. |
| **Agent SDK** | Anthropic's SDK for building agents — gives you the loop, memory, subagents, and tool-execution scaffolding. |
| **Batch API** | An async API that runs many requests at a discount (50% off), returning results within 24 hours. |
| **Cache breakpoint** | A `cache_control` marker placed on a content block; everything *up to and including* the breakpoint becomes a cacheable prefix. |
| **Cache hit / miss** | A hit reuses a previously stored prefix (cheaper, faster); a miss writes a new cache entry (more expensive than a normal read). |
| **Chain-of-thought (CoT)** | Asking the model to reason step-by-step before answering. With Claude 4.x use *extended thinking* instead of asking for "let's think step by step." |
| **Context window** | The maximum total tokens (input + output) a model can handle in a single request. |
| **Extended thinking** | A Claude feature where the model produces internal reasoning tokens before its final answer. Toggled via the `thinking` request parameter. |
| **Files API** | An Anthropic API for uploading files once and referencing them by ID across requests. |
| **Hook (Claude Code)** | A shell command Claude Code runs in response to events (PreToolUse, PostToolUse, Stop, etc.) — configured in `settings.json`. |
| **MCP** | Model Context Protocol — an open protocol for connecting LLMs to external tools, resources, and prompts via a standard interface. |
| **Messages API** | The primary Claude API endpoint (`/v1/messages`); accepts a list of messages and returns an assistant turn. |
| **Prompt caching** | Reusing prefixes (system + early messages + tool defs) across requests for ~90% input-token cost savings. TTLs: 5 min (default) or 1 hour. |
| **Skill (Claude Code)** | A reusable prompt + tool bundle invoked via `/skill-name` or auto-triggered by the harness. |
| **Stop reason** | Why generation ended: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`. |
| **Streaming** | Receiving response tokens as Server-Sent Events instead of one final blob. |
| **Subagent** | A child agent spawned by a parent to handle an isolated task with its own context. |
| **System prompt** | Top-level instructions to the model, passed via the `system` parameter (separate from `messages`). |
| **Tool** | A function the model can call. Defined by a JSON Schema; the *application* runs the actual code. |
| **Tool use loop** | Repeatedly: model emits `tool_use` → app runs tool → app sends `tool_result` → model continues, until `stop_reason` is `end_turn`. |
| **`tool_choice`** | Request parameter controlling whether the model must use a tool, may choose one, or use a specific one (`auto`, `any`, `tool`, `none`). |
| **Vision** | Passing images as input via the `image` content block; supported on all Claude 4.x models. |
