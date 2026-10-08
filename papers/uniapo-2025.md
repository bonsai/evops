# UniAPO: Unified Multimodal Automated Prompt Optimization

Source: https://arxiv.org/abs/2508.17890
Year: 2025
Relevance: Very high

## Intent relevance
The project compresses and expands prompt/code knowledge while converging toward an Intent.

## Research question
How can automatic prompt optimization extend to multimodal tasks with stable feedback and useful history?

## Method
UniAPO uses an EM-inspired optimization process separating feedback modeling from prompt refinement, plus short-term and long-term memory.

## Main finding
The framework reports gains across text, image, and video benchmarks and emphasizes explicit feedback modeling and historical memory.

## Import into hw-sotsusei
- Separate evaluation from prompt/code mutation.
- Store historical feedback as first-class data.
- Keep successful prompts/methods as reusable candidates.
- Use short-term history and long-term compressed knowledge.
- Treat prompt optimization as one operator in the larger method-selection loop.

## Cannot assume
Prompt optimization is not equivalent to Blender geometry optimization. The genome must include code, geometry, ratios, materials, and camera.

## Design implication
History -> Feedback Model -> Prompt/Genome Mutation -> Candidate.

## Limitation
It does not provide the complete natural-selection loop.
