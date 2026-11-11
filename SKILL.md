---
name: evops
description: EvOps — 生成→評価→プロンプト進化 のループを回すパイプライン。CLI evops-mcp と MCP 群（db:8001, evaluator:8002）で、paper-number スキーマの成果物を生成・評価・改善する。「evops」「eval loop」「評価ループ」「進化ループ」「evolve loop」「生成→評価」「paper-number」「sotsusei.db」などで発動。
---

# evops — 生成 → 評価 → 進化ループ

**3 層分離**: Planning(`docs/`) → Generation(`skills/`) → Evaluation(`mcp_core/`)。評価結果でプロンプト/パラメータを進化させる。

- 実体: `/home/bons/evops`（CLI: `evops` / `evops-mcp` → `skills/cli_mcp/cli.py`）
- 単一 DB: `/home/bons/evops/mcp_core/db/sotsusei.db`（生成履歴・評価履歴）
- ループ本体: `skills/evolve/loop.py`（生成 → 評価 → プロンプト進化）、`skills/evolve/{generator,evaluator,prompter,gallery}.py`
- Gate: Wide Gate（開発・緩）→ Narrow Gate（品質・厳）
- 出力（paper-number スキーマ）:
  ```
  outputs/papers/<PAPER_ID>/
  ├── episode.json
  ├── panels/<ID>_panel_01.svg
  ├── assets/<ID>_voice_01.mp3
  └── reports/eval_report.json
  ```

## CLI

```bash
evops mcp list / start / start-all / status / stop
evops mcp call <server> <tool> '<json>'
evops evolve --concept donpen --iterations 5
evops pipeline render --paper-id S01
```

## MCP サーバー（`mcp/`）

| server | port | 役割 |
|---|---|---|
| db | 8001 | SQLite 生成/評価履歴 |
| evaluator | 8002 | CLIP / 基本指標 / 色彩 / 動画 / AA / エフェクト評価 |
| gateway | — | MCP サーバー統合ゲートウェイ |

## 制約 / 既知事項

- WSL Python で `bpy` import 不可 → `.blend_spec.json` スタブで代用
- Voicevox(:50021) 不通時は gTTS フォールバック
- CLI/JSON 疎結合: evops は `kamishibai`/`telop`/`fonts` を import せず、JSON 仕様を書いて CLI を呼ぶ
- 進化ダッシュボード: http://localhost:8010/（10s 自動更新）

## 関連

- 評価系: `comfy-eval-loop`, `lm-hex-eval` / 生成系: `kamishibai`
- Kaggle Tier-2 GPU 評価: `kagura`（kaggle-discovery）
