# VQualA 2025 Challenge on Visual Quality Comparison for Large Multimodal Models

Source: https://arxiv.org/abs/2509.09190
Year: 2025
Relevance: Very high

## Intent relevance
hw-sotsusei needs an evaluator that can distinguish “near” from “good enough” and explain which candidate is better.

## Research question
How well can large multimodal models reason about visual-quality differences across images?

## Method
The challenge uses coarse-to-fine visual-quality comparison tasks covering single images, pairs, and groups, including 2AFC preference and multiple-choice protocols.

## Main finding
Instruction-tuned multimodal models show emerging ability for open-domain visual-quality comparison, while evaluation protocol and reasoning remain important.

## Import into hw-sotsusei
- Use pairwise comparison, not only an absolute score.
- Store candidate A/B, preference, reason, and confidence.
- Add coarse-to-fine criteria.
- Treat 90% similarity as a calibrated decision protocol, not a magical scalar.
- Calibrate VLM judgment against a small human set.

## Cannot assume
A benchmark result does not prove reliable Doraemon evaluation. Domain-specific calibration is required.

## Design implication
Evaluate(reference, candidate A, candidate B, criteria) should return preference, scores, confidence, and reasons.

## Limitation
It does not directly solve Blender code evaluation or parameter freezing.
