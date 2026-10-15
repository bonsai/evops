# PRD — CLIP Evaluation Adapter

- Status: Draft / contract-first
- Related MRD: [MRD.md](MRD.md)
- Related design: [DRD.md](DRD.md)
- Related issue: [#45](https://github.com/bonsai/evops/issues/45)
- Contract PR: [#46](https://github.com/bonsai/evops/pull/46)

## 1. Product outcome

Add a reusable CLIP-compatible image-text similarity evaluator to evops. The ontology and result schema are the source of truth for concept IDs and result semantics; notebook, CLI, and MCP entry points should call the same core evaluator.

## 2. Functional requirements

- **FR-01 Ontology:** define stable concept IDs for CLIP evaluation, image-text similarity, prompt alignment, embeddings, cosine similarity, and provenance.
- **FR-02 Input:** accept an image reference/path and one text prompt per evaluation request.
- **FR-03 Scoring:** compute normalized image/text embeddings and cosine similarity using a documented model/preprocessing path.
- **FR-04 Per-prompt preservation:** preserve each prompt-score result. Any aggregation must be explicit and separately named.
- **FR-05 Provenance:** record model ID, revision when available, library/version, preprocessing configuration, runtime device, input reference, and duration when available.
- **FR-06 Result contract:** emit a result object conforming to `schemas/clip-evaluation-result.schema.json`.
- **FR-07 History:** support one JSON object per line for append-only JSONL evaluation history.
- **FR-08 Failure handling:** represent failed runs with a failed status and error details; do not substitute score 0 for an exception.
- **FR-09 Entry points:** reuse one core implementation from CLI, Kaggle notebook, and MCP adapters.
- **FR-10 Testability:** provide schema/unit/fixture tests that do not require GPU or model download; keep real-model integration tests separate.

## 3. Non-functional requirements

- Reproducibility: configuration and provenance are retained.
- Loose coupling: CLI/MCP/notebook are adapters, not independent scoring implementations.
- Portability: contract-level tests run on CPU-only developer environments.
- Observability: failed and skipped evaluations are explicit.
- Honest reporting: only executed tests and benchmarks may be reported as passed.

## 4. Acceptance criteria

1. Ontology and result schema are machine-readable and validated in tests.
2. Core evaluator returns a normalized structured result.
3. Per-prompt scores and model/configuration metadata are retained.
4. Error paths produce a failed record rather than a fabricated numeric score.
5. CLI/notebook/MCP use the same scoring implementation.
6. JSONL output is valid and suitable for downstream reports.
7. A documented GPU run demonstrates real-model evaluation before claiming model-level validation.

## 5. Out of scope

- Training or fine-tuning a CLIP model.
- Treating CLIP as the sole quality, safety, or correctness gate.
- Implementing a new MCP-specific scoring algorithm.
- Claiming current implementation is complete: PR #46 establishes ontology/schema/docs only.
