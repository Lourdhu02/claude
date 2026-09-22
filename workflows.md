# Workflows

Repeatable Claude workflows for common engineering tasks. Each workflow is a step-by-step sequence you can follow with the Claude API, Claude Code, or a chat session. Adapt them to your stack.

---

## Workflow 1: Code Review

Use Claude to review a pull request, a diff, or a file you just wrote. Works with the API (paste the diff in a message) or with Claude Code (`/code-review` style prompts).

### Steps

1. **Set the context**
   - Tell Claude what the code does, what layer it belongs to, and any relevant constraints (performance, security, backwards compatibility).
   - Share the diff or the file. If the file is large, share the changed sections plus surrounding context.

2. **Give Claude a review rubric**
   Use this as the system prompt or instruction:

   ```text
   Review the code below for:
   - Correctness: does it do what it claims? Any logic errors or edge cases missed?
   - Security: any injection, auth, or data-exposure risks?
   - Performance: any obvious N+1 queries, unnecessary work, or unbounded loops?
   - Readability: is the intent clear? Any confusing names or missing comments on non-obvious logic?
   - Testing: are the important cases covered? Any missing edge cases?
   - Style: does it match the existing codebase conventions?

   For each issue, give: severity (critical / important / nit), the location, what's wrong, and a concrete suggestion. Do not nitpick style if the codebase is inconsistent — focus on what matters.
   ```

3. **Claude reviews**
   - Claude returns a structured list of findings. Read through.

4. **Claude suggests fixes (optional)**
   - Ask Claude to write the fix for any issue you want to address. Review the generated code before applying it — treat it like a suggestion from a junior reviewer, not a final answer.

5. **You decide**
   - Apply the fixes you agree with. Dismiss the rest with a reason (e.g., "intentional", "out of scope for this PR").

6. **Iterate**
   - If you apply fixes, re-run the review on the updated diff. One round of review + fix is usually enough; more than two rounds and you are over-engineering the review.

### Tips

- **Diff size**: if the diff is more than a few hundred lines, ask Claude to focus on the most changed files or the highest-risk areas (auth, payment, data mutation).
- **Tie to tickets**: if the code implements a specific requirement, paste that requirement too. Claude can check that the implementation matches the spec.
- **Don't skip your own review**: Claude is a second pair of eyes, not a replacement for your judgment.

---

## Workflow 2: Documentation Generation

Use Claude to turn code, a README skeleton, or a rough outline into polished documentation.

### Steps

1. **Collect the source material**
   - The code or API you are documenting.
   - Any existing notes, docstrings, or a rough outline.
   - The audience: who is this doc for? (new users, internal devs, API consumers, etc.)

2. **Give Claude the doc brief**

   ```text
   Write documentation for the following [code / API / feature].

   Audience: [who reads this]
   Goal: [what should the reader be able to do after reading]
   Format: [README / API reference / tutorial / migration guide]
   Tone: [concise / friendly / technical / tutorial-style]

   Include:
   - A short "what is this" opening.
   - A quick-start section: the smallest thing the reader can do to see it work.
   - The main concepts, in order of need.
   - Code examples for the common cases.
   - A "what could go wrong" or troubleshooting section if there are common mistakes.

   Use the code and docstrings as the source of truth. Do not invent APIs or parameters — if something is unclear, leave a [TODO: verify] note rather than guessing.
   ```

3. **Claude drafts**
   - Read the draft. Check that every code example is correct (run it if you can).

4. **Fact-check**
   - Cross-check any API signatures, parameter names, and return types against the actual code. Claude can hallucinate details, especially for things it cannot see.

5. **Refine**
   - Ask Claude to revise specific sections: "make the quick-start shorter", "add an example for X", "rewrite the intro for a less technical audience".

6. **Publish**
   - Add to your repo, wiki, or docs site. Keep the source material (code, docstrings) as the long-term truth — docs drift otherwise.

### Tips

- **Docstrings first**: if your code has good docstrings, ask Claude to expand them into full docs rather than writing from scratch. It's more accurate.
- **Examples matter more than prose**: readers remember working code. Prioritize examples over descriptions.
- **Keep a source of truth**: for API docs, generate from the code (docstrings, type hints) rather than maintaining a separate file by hand. Claude can help write the generator.

---

## Workflow 3: Testing

Use Claude to help write, review, and expand tests — unit tests, integration tests, or fixtures.

### Steps

1. **Show Claude the code under test**
   - Share the function or class, its signature, and what it is supposed to do.
   - If there are existing tests, share those too so Claude matches the style.

2. **Give Claude the testing brief**

   ```text
   Write tests for the following code.

   Framework: [pytest / unittest / Jest / whatever]
   What to cover:
   - The happy path(s): the common case(s) that should work.
   - Edge cases: empty input, boundary values, None / null, large input.
   - Error cases: what happens when things go wrong? Are errors raised correctly?
   - Any invariants or post-conditions the code should preserve.

   Style:
   - Follow the existing test style in the codebase.
   - One assertion per test where practical; test names that describe the behavior.
   - Use fixtures / setup helpers if they already exist.
   - Do not test implementation details — test behavior from the caller's perspective.

   If the code depends on external resources (DB, API, filesystem), show me how to mock or fixture those.
   ```

3. **Claude drafts tests**
   - Read the tests. Run them. Fix any failures.

4. **Check coverage of intent**
   - Ask Claude: "what cases did I miss?" or "what's the riskiest thing that could be wrong in this code, and do we have a test for it?"

5. **Add to suite**
   - Merge the tests. Run the full suite to make sure nothing broke.

### Tips

- **Test the contract, not the body**: tests should break when behavior changes, not when internal refactoring happens.
- **Claude can write brittle tests**: if the code changes, Claude's tests may still assert on old behavior. Review before merging.
- **Round-trip**: after writing tests, ask Claude to run them (if you have a CLI setup) or to review whether they actually cover the riskiest case.
- **Property-based testing**: for pure functions, ask Claude to suggest property-based tests (e.g., "for any sorted list, reversing twice gives the original") in addition to example-based tests.

---

## Workflow 4: Debugging a Failing Test or Error

Use Claude to help diagnose a test failure, exception, or unexpected behavior.

### Steps

1. **Share the symptom**
   - The error message or the failing test output.
   - The relevant code (the failing test, the code under test, and any setup).
   - What you expected to happen.

2. **Ask Claude to diagnose**

   ```text
   This test / code is failing with the error below. The expected behavior is [X].

   [paste error + relevant code]

   Help me understand:
   - What is the most likely cause?
   - What would I check first?
   - What are 2–3 other possible causes, and how would I distinguish them?

   Do not just give me a fix — walk me through the reasoning so I can verify it.
   ```

3. **Claude proposes causes**
   - Read the reasoning. Check the likely cause yourself before applying a fix — it's easy to accept a plausible-sounding answer that's wrong.

4. **Test the hypothesis**
   - Apply the smallest change that tests the hypothesis. Run the test. If it passes, you likely found it. If not, go back to step 2 with the new information.

5. **Fix and add a regression test**
   - Once fixed, ask Claude to write a regression test that would have caught this failure. Add it.

### Tips

- **Paste the real error**: truncated or paraphrased errors lead to wrong diagnoses. Paste the full traceback.
- **Smallest reproducer**: if you can reduce the failure to a small, self-contained example, Claude will help faster and more accurately.
- **Don't stop at the first answer**: if the suggested fix doesn't work, share the new result and ask Claude to revise. Debugging is usually 2–3 rounds.

---

## General workflow principles

- **Give Claude context, not just code**: what is this for, who uses it, what matters most. The more context, the better the output.
- **One task per turn**: don't ask Claude to review, fix, and write docs in one message. Review first, then fix, then docs. Each step benefits from the output of the previous one.
- **Review before you apply**: Claude's suggestions are drafts. You are the author. Apply what's right, dismiss what's not, and understand the "why" before merging.
- **Iterate in small steps**: a 20-line diff is easier to review with Claude than a 500-line refactor. Break large tasks into reviewable pieces.
