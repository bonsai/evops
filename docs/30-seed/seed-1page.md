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

## 論文から得られた設計原則（8本柱）

### 01: 動画・画像評価は多軸化し、軽量モデル（CLIP, PickScore, ImageReward, HPSv2）で近似可能
→ 複数評価軸を並列運用、単一モデルの欠点を補完

### 02: VLM は semantic/perceptual evaluator として利用するが、CPU 制約では CLIP-small 等の軽量版を使う
→ 大規模VLM不可のCPU制約下で、CLIPS-small で近似評価

### 03: 人間の嗜好はペアワイズ比較で効率的に収集し、Bradley-Terry や DPO で学習する
→ 人間フィードバック収集を情報量最大化のペア比較で実現

### 04: MCP でツール 層を標準化し、A2A でエージェント連携を標準化
→ ツール層をMCP stdio、エージェント連携をA2A JSON-RPCで標準化、差し替え性確保

### 05: 評価結果を生成改善の Feedback source として扱い、構造化データとして蓄積する
→ SQLite/JSONL に prompt, score, tags, repair_inst を蓄積

### 06: 人間フィードバックは有限・高価なので、アクティブラーニングで高情報量サンプルを選ぶ
→ 閾値付近のスコアケースを優先的に人間に提示

### 07: SLM（Phi-3, Llama 3.2 等）を使い、CPU 16GB 内で回転ループを回し続ける
→ 大規模モデル不可のCPU 16GB 環境でPhi-3/Llama 3.2をループ回転

### 08: 蓄積履歴から ML で ranking、prediction、repair strategy を改善する
→ bqmlite（決定論的）で修復戦略を学習・改善

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