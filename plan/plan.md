# SSSS Research Plan

## Core loop

Intent → Generate → Render → LMS/VLM Evaluate → DB Store → ML Learn → Repair → Regenerate

## Research focus

LMS/VLMを評価者として使い、生成結果・評価・失敗・修正履歴をDBに蓄積し、その履歴からMLで次の生成・修正戦略を改善する。

## Backends
- Blender/bpy — main
- SVG/CSS — fast baseline
- SD1.5 — generative baseline
- Blender MCP — operation layer

## 10-day plan
1. Papers / evaluation ontology
2. DB / JSONL schema
3. LMS/VLM evaluator
4. SVG/CSS baseline
5. Blender/bpy baseline
6. Blender MCP
7. SD1.5 baseline
8. Repair loop
9. ML / cross-backend comparison
10. Analysis / dashboard

## Repository separation
- plan = what to verify
- papers = prior research
- lms = evaluation/reasoning
- db = accumulated experiment knowledge
- ml = learning from accumulated data
- sdk = common loop
- skills = reusable knowledge
- mcp = external operations
- crx = human observation/control
- presen = communication
