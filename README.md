# ssss

VLMを用いた異種アニメーション生成バックエンドの共通評価・改善ループ。

## Core

Intent → Generate → Render → VLM/LMS Evaluate → DB Accumulate → ML Learn → Repair → Regenerate

研究の肝は、VLM/LMSを評価者として使い、生成結果・評価・失敗・修正・再生成履歴をDBに蓄積し、その履歴をMLで学習して次の生成を改善する閉ループにある。

## Backends

- Blender/bpy: main
- SVG/CSS: fast 2D baseline
- SD1.5: generative baseline
- Blender MCP: tool operation layer

## Layers

- `presen/`: presentation
- `papers/`: literature
- `plan/`: research plan
- `lms/`: LLM/VLM evaluation and reasoning
- `db/`: experiment/evaluation knowledge
- `ml/`: scoring, prediction, ranking, prompt optimization
- `sdk/`: common loop implementation
- `skills/`: reusable evaluation/repair knowledge
- `mcp/`: external tool control
- `crx/`: browser UI and observation
