# Operations Manual — Evolve Loop & Dashboard

## Evolve Loop 運用手順

### 基本実行

```bash
# ドン・キホーテ進化（3世代、目標75点）
python3 scripts/evolve_loop.py --concept don_quixote --iterations 3 --target 75

# どんぺん進化（5世代、目標70点）
python3 scripts/evolve_loop.py --concept donpen --iterations 5 --target 70
```

### 出力構造

```
outputs/evolution/
└── {concept}_{MMDD_HHMMSS}/
    ├── gen_{concept}_00.png      # 世代0のレンダリング
    ├── gen_{concept}_01.png      # 世代1のレンダリング
    ├── ...
    ├── {concept}_evolution_report.json
    └── {concept}_evolution_gallery.html
```

### 閾値調整 — Gate Mode

`scripts/evolve_loop.py` 内の `evaluate_character()` で変更:

```python
# Wide Gate（開発中 / ゆるい完了）
converged = total >= 50
grade = "A" if total >= 80 else "B" if total >= 65 else "C" if total >= 50 else "D"

# Narrow Gate（品質フィルタ / 厳選）
converged = total >= 75   # target_score と同値
grade = "A" if total >= 95 else "B" if total >= 80 else "C" if total >= 60 else "D"
```

**推奨運用**:
- 日次開発: Wide Gate（50点合格）
- 週次リリース判定: Narrow Gate（75点合格、A=95）
- 最終審査: JEV Tier-3 Human Gate

## Evolution Dashboard

### 起動

```bash
./evops-mcp start evolution-dashboard
# または直接
python3 skills/evolution-dashboard/server.py --http --port 8010
```

### アクセス

| URL | 用途 |
|-----|------|
| `http://localhost:8010/` | 🧬 HTMLダッシュボード（世代別カード） |
| `http://localhost:8010/api/report/latest` | 最新レポート JSON |
| `http://localhost:8010/api/compare/{concept}` | 最初 vs 最後の比較 |
| `http://localhost:8010/docs` | Swagger UI（OpenAPI対話実行） |

### 自動リロード

ダッシュボードは **10秒ごとに自動リロード**。
進化ループ実行中にブラウザで開いておくと、リアルタイムで世代が追加されていく。

### JSON API 例

```bash
# 全レポート一覧
curl -s http://localhost:8010/api/reports | jq

# 特定コンセプトの全世代
curl -s http://localhost:8010/api/generations/don_quixote | jq

# 特定世代の詳細
curl -s http://localhost:8010/api/generations/don_quixote/2 | jq

# 最初 vs 最後の比較
curl -s http://localhost:8010/api/compare/don_quixote | jq
```

## MCP サーバ統合運用

### 全サーバ起動

```bash
./evops-mcp start-all
```

### 状態確認

```bash
./evops-mcp status
```

### 特定サーバ呼び出し

```bash
# Evolution Dashboard MCP (stdio)
./evops-mcp call evolution-dashboard list_generations_tool \
  '{"concept": "donpen"}'

# Evaluator MCP
./evops-mcp call evaluator review_paper_anime \
  '{"video_path": "outputs/papers/S01/final.mp4", "gate_mode": "wide"}'

# Storyboard MCP
./evops-mcp call storyboard plan_cuts_tool \
  '{"episode_json_path": "outputs/papers/S02/episode.json"}'
```

## DB 永続化

すべての評価結果は `mcp_core/db/sotsusei.db` に保存。

```bash
sqlite3 mcp_core/db/sotsusei.db <<EOF
SELECT concept, generation_id, score, grade, timestamp FROM eval_results
ORDER BY timestamp DESC LIMIT 10;
EOF
```

**今後追加予定**:
- `eval_kaggle` テーブル — Kaggle Tier-2 結果
- `eval_human` テーブル — JEV Tier-3 人間評価

## トラブルシューティング

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bpy` not found | Blender not in PATH | `apt install blender` or check `which blender` |
| Voicevox unreachable | localhost:50021 down | Use gTTS fallback; `export TTS_FALLBACK=gtts` |
| Kaggle API error | Token missing | Set `KAGGLE_USERNAME` / `KAGGLE_KEY` env vars |
| Evolution not converging | Target too high | Lower `--target` or use wide gate |
