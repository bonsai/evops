# CLIP evaluation: ontology and contract

Related issue: [#45](https://github.com/bonsai/evops/issues/45)

## Canonical definitions

- Ontology: `ontology/clip-evaluation.json`
- Result contract: `schemas/clip-evaluation-result.schema.json`
- Existing GPU evaluation entry point: `docker/eval_clip_gpu.py`
- Existing notebook: `notebooks/eval_clip_gpu.ipynb`

## Semantics

The first supported measure is image-text cosine similarity. The result is a relative similarity signal for a specific model and preprocessing pipeline, **not a probability** and not a complete measure of image quality. Record the model identifier/revision, preprocessing, runtime device, input reference, and score interpretation alongside each result.

Do not silently use the maximum score across unrelated prompts as the quality score. If ranking multiple prompts, retain each prompt-score pair and record the explicit aggregation rule.

## JSONL record

Store one result object per line using the result schema. Failed evaluations should be represented with `status: "failed"` and an `error`; they must not be converted to a numeric score of zero, because zero is a legitimate similarity value.

## Implementation sequence

1. Validate ontology and result schema.
2. Refactor the existing evaluator into a reusable core function that returns structured records.
3. Keep CLI, notebook, and MCP as thin entry points to the same implementation.
4. Add CPU contract tests and fixture tests; run real-model tests in the Kaggle GPU environment.
5. Compare known positive/negative image-text pairs and preserve per-prompt scores.
6. Add evaluation history integration only after the record contract is stable.

## Acceptance notes

A passing schema test proves contract compliance, not model quality. Real-model benchmarks and GPU execution must be recorded only after they have actually run.
