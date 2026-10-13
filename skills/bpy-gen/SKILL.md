# bpy-gen

Blender Python を使った作画・3D生成スキル。サーベイとは別のインテント。

## 提供ツール

- `doraemon_bpy.py` — ドラえもん
- `pagoda_bpy.py` — 五重塔
- `bear_bpy.py` — ローポリ木彫りクマ
- `render.sh` — Windows Blender ヘッドレスレンダリング + MEGA 自動同期

## 使い方

```bash
./render.sh <model>
# model: doraemon | pagoda | bear
```

出力先:
- ローカル: `~/bpy-gen/outputs/`
- クラウド: `MEGA/bpy-gen/outputs/` (MEGAsync 自動同期)

## 構成

- ソース: `~/.skills/bpy-gen/tools/`
- カタログ: `catalog.json`
- レンダーログ: `~/bpy-gen/outputs/.ledger.jsonl`

## 今後

- LLM（Sakura）→ 自然言語指示 → bpy 自動生成
- Colab GPU で PyTorch + bpy 連携実験
