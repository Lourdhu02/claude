# 04 — Multimodal & files

By the end you can:

1. Pass images and PDFs as input.
2. Upload files once with the Files API and reuse them.
3. Get citations back tying assistant claims to source spans.
4. Pick between base64, URL, and Files-API references.

Time budget: ~45 minutes reading, ~45 minutes lab.

---

## 1. Content blocks recap

In Module 00 we said `messages[i].content` could be a string or a list of typed blocks. For multimodal it's always a list.

```python
messages=[{
  "role": "user",
  "content": [
      {"type": "text", "text": "What's in this image?"},
      {"type": "image", "source": {
          "type": "base64", "media_type": "image/png",
          "data": b64_encoded_png,
      }},
  ],
}]
```

| Input block type | Notes |
|---|---|
| `text` | Plain text. |
| `image` | PNG, JPEG, GIF, WebP. base64 or URL source. |
| `document` | PDFs (and text in some configurations). |
| `tool_result` | From a previous tool call (Module 03). |

---

## 2. Three ways to reference a file

```mermaid
graph LR
    A[Local file] --> B[base64 inline]
    A --> C[Files API upload]
    D[Public file] --> E[URL reference]

    B -.->|"simple, no setup<br/>~33% size overhead"| X[Use for: one-off, <5MB"]
    E -.->|"shared public docs"| Y[Use for: public PDFs, RAG sources]
    C -.->|"reuse across requests<br/>caches well"| Z[Use for: production, big files, repeated queries]
```

### base64 inline

```python
import base64, pathlib
img_b64 = base64.standard_b64encode(pathlib.Path("chart.png").read_bytes()).decode()
content = [
    {"type": "text", "text": "Describe this chart."},
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
]
```

### URL

```python
content = [
    {"type": "text", "text": "Summarize this PDF."},
    {"type": "document", "source": {"type": "url", "url": "https://example.com/whitepaper.pdf"}},
]
```

### Files API

Upload once, reference by ID forever (within your account).

```python
uploaded = client.beta.files.upload(file=open("invoice.pdf", "rb"))
# Then:
content = [
    {"type": "text", "text": "Extract the total."},
    {"type": "document", "source": {"type": "file", "file_id": uploaded.id}},
]
```

The Files API is the right choice for any file you'll re-use — it pairs with prompt caching for massive savings on repeated queries against the same doc.

---

## 3. Image limits to know

| Constraint | Value (approximate; check current docs) |
|---|---|
| Max image size | 5MB (base64) / 8000×8000 px (approx) |
| Max images per request | up to ~100 (model-dependent) |
| Cost calculation | tokens ≈ `(width × height) / 750` |

Resize before sending. The model rarely needs 4K resolution for text or chart reading; 1024px on the long side is usually enough and 10× cheaper.

---

## 4. PDFs

Two ways:

1. **Pass the PDF as a `document` block.** Claude reads the text and rendered pages — best for layout-sensitive docs (invoices, charts).
2. **Pre-extract text** (with `pypdf`) and pass it as a plain text block. Cheaper for text-only docs but loses layout / images.

Prefer option 1 by default. Optimize to option 2 only when the doc is text-heavy and you're cost-sensitive at scale.

---

## 5. Citations

Citations let the model point at exact sentences in your source documents. This is a built-in feature on `document` blocks when you set `citations`:

```python
content = [
    {"type": "document",
     "source": {"type": "file", "file_id": uploaded.id},
     "title": "Q3 financial report",
     "citations": {"enabled": True}},
    {"type": "text", "text": "What was revenue growth?"},
]

r = client.messages.create(model=MODEL, max_tokens=1024, messages=[{"role":"user","content":content}])

for block in r.content:
    if block.type == "text":
        print(block.text)
        for cite in (block.citations or []):
            print(f"  ↳ cited: {cite.cited_text!r} (doc #{cite.document_index}, page {cite.start_page_number})")
```

Citations are crucial for:
- Auditable assistants in regulated domains.
- RAG pipelines where users distrust ungrounded summaries.
- Eval pipelines: a fact without a citation is suspect.

---

## 6. Multi-image patterns

For comparison tasks ("which design is more accessible?"), pass images in order with `text` separators:

```python
content = [
    {"type": "text", "text": "Compare design A and B. List 3 differences."},
    {"type": "text", "text": "<design_a>"},
    {"type": "image", "source": {...A...}},
    {"type": "text", "text": "</design_a>\n<design_b>"},
    {"type": "image", "source": {...B...}},
    {"type": "text", "text": "</design_b>"},
]
```

The XML tags give you something to reference in the model's response.

---

## 7. Cost & latency

| Choice | Trade-off |
|---|---|
| Base64 vs URL vs file_id | All cost the same in **model tokens**, but base64 adds upload latency on every call. file_id is fastest after the first call. |
| Image resolution | Roughly linear: half the pixels, half the tokens. |
| Many small images vs one stitched | Many small is *more* expensive (per-image fixed overhead). Stitch when you can. |
| PDF as document vs extracted text | PDF block = layout fidelity + image content but more tokens; text = cheaper. |

Pair multimodal inputs with prompt caching (Module 05) when you'll query the same doc multiple times — the document tokens become cache hits.

---

## 8. Lab

[`lab.ipynb`](./lab.ipynb) walks through:
- Passing a local chart PNG and asking Claude to extract numeric data.
- Uploading a PDF via the Files API and asking citation-backed questions.
- Comparing two images side-by-side.

You'll need any PNG and any PDF on disk; the lab uses `pillow` to generate a placeholder PNG and a tiny `pypdf`-built PDF if you don't have one.

---

## References

- Vision: <https://docs.claude.com/en/docs/build-with-claude/vision>
- PDF support: <https://docs.claude.com/en/docs/build-with-claude/pdf-support>
- Files API: <https://docs.claude.com/en/docs/build-with-claude/files>
- Citations: <https://docs.claude.com/en/docs/build-with-claude/citations>
