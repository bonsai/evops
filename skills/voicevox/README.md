# Voicevox TTS Skill — Hibiki（空野ヒビキ / speaker 8）

音声生成スキル。Video pipeline のナレーション出力に特化。

## 役割

- `episode.json` の `text` / `subtitle_track` から音声を生成
- Hibiki（空野ヒビキ）ボイスをデフォルトとする（男性・落ち着いた口調）
- MP3 / WAV 出力（ffmpeg 互換）

## 接続（疎結合）

```
[episode.json / subtitle_track] --(text)--> [voicevox-cli] --> narration.mp3
                                      ↑
                              [char_tkt_*.json] (文字票承認済み)
```

## 依存

- Voicevox サーバー (`http://localhost:50021` 既定)
- 仕様: `curl -X POST -H 'Content-Type: application/json' -d '{"text":"...","speaker":8}'`
- Hibiki の speaker ID は通常 `8`

## CLI 使用例

```bash
node skills/voicevox/bin/voicevox-cli.js \
  --text "論文の評価はできるが、知識にどう繋がる？" \
  --speaker 8 \
  --output narration.mp3
```

または、4 コマ全体を順に読み上げるバッチモード：

```bash
python scripts/voicevox_batch.py \
  --episode episode.json \
  --speaker 8 \
  --output narration.mp3
```

## データ契約（JSON 入出力）

```json
{
  "input": {
    "text": "...",
    "speaker": 8,
    "speed": 1.0,
    "pitch": 0.0,
    "intonation": 1.0
  },
  "output": {
    "file_path": "/tmp/narration.mp3",
    "duration_sec": 12.5,
    "status": "ok"
  }
}
```

## MCP 統合（オプション）

`mcp/voicevox/server.py` を作成すれば、以下のツールを提供可能：
- `generate_voice` — テキストから MP3 生成
- `generate_batch` — episode.json から一括生成

ただし、今は CLI スキルとして完結。MCP 統合は必要に応じて `base_server.py` を利用して追加。