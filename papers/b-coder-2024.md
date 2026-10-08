# B-CODER: Value-Based Deep Reinforcement Learning for Program Synthesis

Source: https://arxiv.org/abs/2310.03173
Year: 2024, ICLR
Relevance: High

## Intent relevance
hw-sotsusei treats generation code as part of the genome. B-CODER is relevant because historical programs and executable verification can become learning signals.

## Research question
Can value-based reinforcement learning improve program synthesis when programs and historical samples provide verifiable feedback?

## Method
B-CODER uses value-based RL, pretrained language-model initialization, a conservative Bellman operator, and learned value functions for post-processing generated programs.

## Main finding
The paper reports competitive program-synthesis performance with relatively little reward engineering.

## Import into hw-sotsusei
- Treat bpy code as an inspectable artifact.
- Add executable/render success as a hard signal.
- Preserve historical code candidates.
- Learn which mutations are promising.
- Separate semantic visual score from executable validity.

## Cannot assume
A valid Blender script is not necessarily visually correct.

## Design implication
Use multi-level reward: validity -> geometry constraints -> visual evaluation -> intent alignment.

## Limitation
It does not solve image/VLM evaluation or 3D artistic similarity.
