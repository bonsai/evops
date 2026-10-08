# hw-sotsusei — SSSS Research 1ページ概要

## コアアーキテクチャ

**MCP-to-MCP フィードバックループ**：  
`User Intent → Prompt Engineer → Code Generator (bpy/SVG) → Renderer → VLM Evaluator → DB → Repair Agent → Re-prompt`

- **MCP stdio による独立MCPサーバー間通信**（User Intent, Prompt Engineer, Code Generator, Renderer, VLM Evaluator, DB, Repair Agent）
- **閾値システム**：VLM評価スコア ≥ 0.85 で完了、未満なら修復ループへ
- **意図と出力の cosine similarity** で「齟齬」を定量化、欠落要素を自動抽出

## LMS/VLM → DB → ML → Repair → Regenerate

CPU 16GB 制約下、CLIP-small 等の軽量評価器を活用。  
人間の嗜好はペアワイズ比較で収集し、Bradley-Terry や DPO による効率化。  
Phi-3 / Llama 3.2 など SLM を MCP 経由で A2A 連携。

## 研究テーマ2：3D 自律改善ループ

**「pain（ストレス）をなくす」自動軽減型 3D 生成ループ**

| レイヤー | 技術 |
|---|---|
| 生成 | bpy コード生成・編集 (Blender/bpy) |
| レンダリング | CYCLS/Eevee |
| 評価 | LM Studio ローカル VLM |
| 蓄積 | SQLite/JSONL |
| 学習 | bqmlite（決定論的・SHA-256） |
| 可視化 | matplotlib/plotly/PyVista |
| 連携 | MCP経由A2A（bpy/Blender, bqmlite, LM Studio） |

## 主要な3兄弟エージェント

- **LangChain**：プロンプト管理、ツール呼び出し標準
- **LangGraph**：評価→学習→修復の状態機械実装
- **LangSmith**：ターン別トレーシング・モニタリング

## 目標

1. VLM評価器としてDB蓄積を実現
2. bqmlite による修復戦略の自動改善
3. MCP/A2A で人間介入を最小化
4. 可視化ダッシュボードでプロセス言語化