# Research Intent — updated

## Core intent
Build a closed-loop system that does not merely repair generated artifacts, but learns which generation methods should survive and converge toward a clearly defined Intent.

## Evidence-driven refinement
The research loop now explicitly combines:
- multimodal evaluation
- pairwise preference and confidence
- prompt/code history
- executable verification
- evolutionary method selection
- quality-diversity
- parameter freezing with soft critique

## Paper selection priority
1. Evaluation reliability: VQualA and related multimodal quality comparison
2. Prompt optimization with memory: UniAPO
3. Code-as-genome and verifiable reward: B-CODER
4. Quality-diversity / MAP-Elites for preserving alternative good methods
5. Uncertainty and human calibration
6. Domain-specific Doraemon geometry and Blender evaluation

## Updated loop
Intent + Reference
→ Method Selection
→ Generate
→ Render / Execute
→ VLM/LMS Evaluate
→ Preference + Score + Confidence + JEV
→ DB
→ ML / Evolution
→ Soft Critique
→ Fix
→ Freeze reliable parameters
→ Next Generation

The evaluator is not the final goal. The goal is a reproducible search process whose evidence tells us which methods, parameters, and repairs should survive.
