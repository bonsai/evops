# MRD — Master Research Definition

## 目的
VLM/LMSを評価者として使い、アニメーション生成を「生成して終わり」から「評価・蓄積・修正・再生成して目標へ近づく」研究へ変える。

## 最終ゴール
自分で研究を回せる、自給自足型の生成・評価基盤を作る。

研究の本丸はドラえもん生成進化ループ。その前段としてMCP完全化と論文動画化を完成させ、共通基盤を実証する。

## 3つの課題
### 0. MCP完全化
AIから研究・生成・評価・データ操作を可能にする。ただしMCPは薄いAdapterとする。

### 1. 論文動画化
論文 → SF落語 → 4コマ → SVG/CSS → MP4 → VLM評価 → 修正。

### 2. ドラえもん進化ループ
Intent + Reference → Method → Generate → Render → VLM → Fitness → Selection → Mutation/Crossover/Repair → 次世代。

## 成果物
- 研究データ: JSONL / DB
- 再利用可能なSkill
- CLI治具
- MCP Adapter
- 実験履歴
- 最終成果物: MP4

## 原則
Skill / 治具 / Data / MCPを疎結合にする。MCPがなくてもCLIで研究を継続できる。