# DRD — CLIP Evaluator Design

- Status: Draft / implementation design
- Related MRD: [MRD.md](MRD.md)
- Related PRD: [PRD.md](PRD.md)
- Ontology: [../ontology/clip-evaluation.json](../ontology/clip-evaluation.json)
- Result schema: [../schemas/clip-evaluation-result.schema.json](../schemas/clip-evaluation-result.schema.json)
- Related issue: [#45](https://github.com/bonsai/evops/issues/45)

## 1. Architecture

```
Input image + prompt
        |
        v
Shared CLIP evaluator core
  - load pinned/configured model
  - preprocess image and tokenize text
  - compute embeddings
  - normalize embeddings
  - cosine similarity
        |
        v
Normalized evaluation record
        |
        +--> JSONL history
        +--> CLI adapter
        +--> Kaggle GPU notebook adapter
        +--> MCP adapter
```

Adapters must not reimplement preprocessing or scoring.

## 2. Canonical artifacts

- `ontology/clip-evaluation.json`: semantic concept IDs and constraints.
- `schemas/clip-evaluation-result.schema.json`: output contract.
- `docs/clip-evaluation.md`: operational semantics and implementation sequence.
- Existing entry points to refactor/reuse: `docker/eval_clip_gpu.py`, `notebooks/eval_clip_gpu.ipynb`, and `mcp/kaggle/eval_clip_gpu.ipynb.py`.

## 3. Data flow

1. Resolve image input and text prompt.
2. Validate input and capture a stable input reference.
3. Load the configured CLIP-compatible model and record its identity/revision and library version.
4. Apply model-specific image preprocessing and text tokenization.
5. Compute image and text embeddings, normalize them, and calculate cosine similarity.
6. Return a result record with `concept=evaluation.image_text_similarity`, explicit score interpretation, provenance, and status.
7. Append the record as one JSON object to JSONL history.
8. On exceptions, return/record a failed result with an error; never hide the failure as score zero.

## 4. Result contract

A successful record includes `evaluation_id`, `concept`, `status`, `input`, `model`, `method`, `score`, `score_interpretation`, and `runtime`. The schema is authoritative. Store one prompt-score pair per record; a multi-prompt evaluation may emit multiple records linked by a shared run or candidate ID.

## 5. Testing strategy

- Schema tests: valid success/failure records and invalid records.
- Unit tests: embedding normalization and cosine similarity on small known vectors.
- Fixture tests: missing image, empty prompt, malformed image, unavailable model.
- Contract tests: JSONL records validate against the result schema.
- Integration tests: actual model execution, isolated from CPU-only tests.
- GPU verification: run in Kaggle, record runtime/device/model revision, and preserve results as artifacts.

## 6. Security and reliability

- Do not store credentials or tokens in evaluation records.
- Bound input sizes and handle corrupt files.
- Keep model downloads and network access out of contract-only tests.
- Preserve input and model provenance sufficient to explain score changes.

## 7. Implementation sequence

1. Validate the ontology and schema.
2. Extract a shared core evaluator from the existing script.
3. Add tests and structured error handling.
4. Connect JSONL persistence.
5. Route CLI/notebook/MCP adapters to the shared core.
6. Run a real-model GPU integration test and document measured results.

## 8. Current implementation status

PR #46 adds the ontology, JSON Schema, and this design direction. The reusable evaluator, test suite, JSONL persistence, adapter integration, and GPU verification remain pending until implemented and executed.
