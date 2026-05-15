# Module 09 — Exercises

## 1. Cost dashboard
Instrument your client to log per-call: model, input_tokens, cache_read, cache_write, output_tokens, latency. Run 50 calls. Plot a per-call cost histogram. Spot outliers.

## 2. Eval harness
Build a JSONL eval set of 10 (input, expected) pairs for a task you care about. Write a grader. Run it. Save scores to a CSV. This is the *baseline*.

## 3. Prompt v2
Change one thing about the system prompt. Re-run the eval. Did average score move up or down? By how much? Is the change within noise?

## 4. LLM-as-judge bias check
Compare your LLM-as-judge scores to your manual scores on 10 examples. Compute agreement (Cohen's kappa). If kappa < 0.6, fix the judge prompt.

## 5. Minimal RAG
Build a RAG pipeline over the README.md files in this repo. Use any embedding API. Implement: chunk → embed → store → retrieve top-3 → answer with citations.

## 6. Hybrid retrieval
Add BM25 retrieval alongside dense. Combine scores (rank fusion). Show 2 queries where hybrid finds something dense misses.

## 7. Prompt injection
Write a system prompt that holds a "secret" string. Build a chat. As the "user", try to extract the secret. Document 3 successful attacks. Then add defenses (separation, tags, output filter) and re-test.

## 8. Fallback chain
Implement a graceful-degradation chain: Opus → Sonnet → Haiku. Simulate Opus failures (raise APIStatusError). Confirm fallback fires.

## 9. Trace export
Export 20 production-like LLM calls to OpenTelemetry spans (use any OTEL collector). Visualize in Jaeger / Honeycomb / Phoenix.
