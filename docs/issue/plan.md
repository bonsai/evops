# SSSS Research Plan

## Core loop

Intent → Generate → Render → LMS/VLM Evaluate → DB Store → ML Learn → Repair → Regenerate

## Research focus

LMS/VLM を評価者として使い、生成結果・評価・失敗・修正履歴を DB に蓄積し、
その履歴から ML で次の生成・修正戦略を改善する。

## Themes

| テーマ | 生成対象 | ベース | 特徴 |
|---|---|---|---|
| テーマ 1 | 2D 描画 | SVG/CSS | 高速バメイントライン |
| **テーマ 2** | **3D 造型** | **Blender/bpy** | **VLM→bqmlite→自動修復ループ（テーマ本体）** |

テーマ 2 の起点プロンプト：ドラえもん（bpy プリミティブで造型）。

## Backends
- Blender/bpy — main（テーマ 2）
- SVG/CSS — fast baseline（テーマ 1）
- SD1.5 — generative baseline
- Blender MCP — operation layer
- bqmlite MCP — learning layer

## エージェント連携（A2A）

- MCP サーバ群（bpy/Blender, bqmlite, LM Studio）で各レイヤーを接続
- LangChain 3 兄弟：LangChain（ツール/プロンプト）、LangGraph（評価→学習→修復の循環状態機械）、LangSmith（各ターントレーシング）
- bpy コード差分は GitHub（git）で管理・バージョン化；diff reviewer が修正内容をレビュー

## 可視化・分析

- データ分析：matplotlib, pandas, numpy, plotly
- 3D メッシュ可視化：https://pyvista.org/
- ループ履歴・スコア推移・改造効果のダッシュボード

## 10-day plan
1. Papers / evaluation ontology（VeMo, EvalCrafter, VideoScore, VisualPrompter, 3D Human Animation QA, DreamFusion, Idefics2）
2. DB / JSONL schema
3. LMS/VLM evaluator
4. SVG/CSS baseline（テーマ 1）
5. Blender/bpy baseline（ドラえもん、テーマ 2）
6. Blender MCP / bqmlite MCP / LM Studio MCP
7. SD1.5 baseline
8. Repair loop（LangGraph 実装）
9. ML / cross-backend comparison / 分析ダッシュボード（matplotlib/pandas/plotly/PyVista）
10. Analysis / presentation

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
