# PRD — Research Generation Loop

## Product
VLM評価型アニメーション生成研究基盤。

## Problem
生成AIは画像・動画を生成できても、「どこが良く、どこが悪く、次に何を直すか」を継続的に蓄積して改善する仕組みが弱い。

## Requirements
### P0
- 共通Episode / Candidate / Evaluation / Fitness schema
- CLIで実行可能な治具
- MCP Adapter
- VLM/LMS評価
- JSONL/DBへの履歴保存
- MP4生成

### P1
- Pygame / SVG-CSS / Blender / Godot renderer
- 論文SF動画ループ
- 評価→修正→再レンダリング

### P2
- ドラえもん生成Genome
- 世代管理
- Selection / Mutation / Crossover / Repair / Kill
- 成長アニメーション
- 統計・Fitness可視化

## Non-goals
- HTMLアプリを必須デプロイしない
- MCPに処理本体を実装しない
- 特定のLLM/VLMに固定しない
- 生成結果だけを研究成果としない

## Architecture
Paper / Intent → Data → Skill → Tool / Jig → MCP Adapter → AW / WF → MP4 Artifact → Evaluation → Data

## Acceptance
同一入力からローカルとCIで同じ契約の成果物を生成でき、評価履歴を再利用できること。