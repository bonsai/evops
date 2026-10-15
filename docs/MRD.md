# MRD — Reproducible CLIP Evaluation

- Status: Draft
- Scope: `bonsai/evops` CLIP evaluation capability
- Related issue: [#45](https://github.com/bonsai/evops/issues/45)
- Related PR: [#46](https://github.com/bonsai/evops/pull/46)

## 1. Problem

Image-generation workflows need a repeatable way to compare a generated image with its intended prompt or reference text. A bare score is difficult to trust when the model, preprocessing, runtime, prompt set, and score semantics are not recorded. Treating one CLIP score as overall image quality also risks overclaiming what the metric measures.

## 2. Users and needs

- Image-generation researchers need comparable, traceable experiments.
- Pipeline maintainers need a CPU-testable interface and a GPU path for batch evaluation.
- Creative practitioners need prompt-alignment signals that complement, rather than replace, human review and other evaluation axes.
- Automated agents need machine-readable ontology and result records.

## 3. Market / workflow requirements

1. Provide a repeatable image-text semantic similarity signal.
2. Preserve per-prompt results rather than silently collapsing a prompt set to its maximum.
3. Record model identity/revision, preprocessing, input reference, device, and execution status.
4. Support local development and GPU batch evaluation without maintaining separate evaluation semantics.
5. Emit machine-readable results suitable for JSONL history, reports, and later analysis.
6. Make the limitations explicit: CLIP similarity is not a probability and is not a complete measure of aesthetics, factual correctness, safety, anatomy, or temporal consistency.

## 4. Success criteria

- A result can be interpreted and traced to the model/configuration and inputs that produced it.
- Compatible runs can be compared without losing per-prompt detail.
- Contract tests can run without downloading or executing a real model.
- A real-model benchmark can be run in the GPU environment and its environment details recorded.
- Documentation does not imply unexecuted tests or benchmarks have passed.

## 5. Non-goals

- Replacing human creative review.
- Claiming one metric certifies overall image quality.
- Building a new general evaluation platform outside the existing evops architecture.
- Duplicating evaluation logic across CLI, notebook, and MCP adapters.

## 6. Assumptions and risks

- Model availability, licenses, and revisions must be verified before pinning a production model.
- Scores from different models or preprocessing pipelines may not be directly comparable.
- Model downloads and GPU access can fail; failures must be represented explicitly, not mapped to a score of zero.
