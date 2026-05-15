# Module 04 — Exercises

## 1. Chart-to-data
Find any bar chart screenshot. Ask Claude to extract the categories and approximate values as JSON. Validate the JSON.

## 2. Resize matters
Take a 4MB high-res photo. Send it once at full resolution, once resized to 1024px on the long side. Compare:
- Input tokens reported.
- Latency.
- Whether the answer changes.

## 3. PDF Q&A with citations
Pick any PDF (a paper, a manual). Upload to Files API. Ask 5 specific factual questions. For each answer, list the citations returned.

## 4. Compare two images
Find two product screenshots (real or mocked). Wrap each in `<design_a>` / `<design_b>` text blocks. Ask Claude to list 3 differences. Confirm references in the response.

## 5. Multimodal tool-use combo
Combine Module 03 + Module 04: define a `lookup_inventory(sku: str)` tool. Show the model a product photo with a SKU label. It should OCR the SKU and call your tool with it.

## 6. Cost calculator
Write a function `image_token_estimate(width, height) -> int` using the approximation in §3. Use it in a pre-flight check that warns if a request would exceed a token budget.
