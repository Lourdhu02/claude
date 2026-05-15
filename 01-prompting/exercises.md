# Module 01 — Exercises

## 1. Rewrite a bad prompt
Take this prompt and rewrite it using the template from §4 of the README:

> "Hey can you like read this contract and tell me if there's anything weird in it I should know about? Thanks!"

Make it specific, structured, and constrained.

## 2. Few-shot sentiment
Classify movie reviews into `{positive, negative, neutral}`. Write two versions:
- **v1**: zero-shot prose instructions.
- **v2**: three-shot with `<example>` tags covering all three classes.

Run both on these five inputs and compare:
1. "Absolute masterpiece. Cried twice."
2. "It was fine. I watched it."
3. "Pacing was off and the third act unraveled."
4. "Mid."
5. "Worth seeing for the cinematography alone."

## 3. Prefill JSON
Ask the model for the population of three cities. Use prefilling to *guarantee* the response is parseable JSON with shape:

```json
{ "cities": [{"name": "...", "population": 0}, ...] }
```

Verify with `json.loads()`.

## 4. Tag the inputs
Take a prompt that has both a *document to summarize* and *user instructions* mashed into one user message. Refactor it so the doc is in `<document>` and the request is plain text. Compare output quality.

## 5. Negative space
Write a prompt that asks Claude to extract dates from a paragraph but **never** to invent dates if none are present. Test it on a paragraph that contains zero dates. Does it stay silent / say "none"?

## 6. Length control
Ask for an explanation in exactly 50 words. Try three approaches:
1. Plain ask: "Explain X in 50 words."
2. Plain ask + count check: "Then count the words and adjust until exact."
3. Prefill `<answer>` and instruct format.

Which is most reliable? Why?

## 7. Failure cataloging
Pick a real task you'd want to automate (summarize a meeting, draft a Jira ticket, etc.). Write the prompt. Run it on **5** real inputs. Manually classify failures into 3 buckets. *That's your eval set.* Save it to `eval.jsonl` for Module 09.

---

## Solutions

<details>
<summary>1. Rewritten prompt</summary>

```text
You are a contract reviewer for a software engineer (not a lawyer). Your job is to
flag clauses worth a second look — not to give legal advice.

<instructions>
1. Read the contract in <contract>.
2. List clauses that are unusual, unilateral, vague, or commonly negotiated.
3. For each, explain in one sentence WHY it matters.
</instructions>

<rules>
- Do not invent clauses that aren't in the contract.
- Do not give legal conclusions; flag and explain.
- If the contract is fine, say "No notable concerns."
</rules>

<output_format>
A markdown list, where each item is:
**Section X — short title.** One-sentence explanation.
</output_format>

<contract>
{paste here}
</contract>
```
</details>

<details>
<summary>6. Length control</summary>

Prefill is most reliable, but even prefill can't guarantee an *exact* word count — token boundaries don't align to words. For exact-length output, generate, count words client-side, and either truncate or re-prompt. This is a good reminder that LLMs can't count their own output.
</details>
