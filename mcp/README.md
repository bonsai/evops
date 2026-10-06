# MCP Servers

このディレクトリは、`hw-sotsusei` プロジェクトのツール層を MCP（Model Context Protocol）で標準化したもの。
CPU 16GB 制約下で回転ループを回すため、各ツールは軽量に設計している。

## サーバー一覧

| サーバー | ポート | 機能 |
|---------|--------|------|
| `db/server.py` | 8001 | SQLite への生成履歴・評価データの読み書き |
| `evaluator/server.py` | 8002 | 軽量画像評価（CLIP, 基本指標, 色彩統計） |
| `blender-bpy/server.py` | 8003 | SVG 生成 + Blender ヘッドレスレンダリング |

## 起動

各サーバーは独立して起動できる。

```bash
# Terminal 1
python mcp/db/server.py

# Terminal 2
python mcp/evaluator/server.py

# Terminal 3
python mcp/blender-bpy/server.py
```

## 呼び出し例

### Blender-bpy：ドラえもん SVG 生成

```bash
python mcp/test_client.py mcp/blender-bpy/server.py
```

または MCP client から `generate_doraemon_svg` を呼び出す。

```json
{
  "name": "generate_doraemon_svg",
  "arguments": {
    "output_path": "/tmp/doraemon_reading.svg",
    "action": "reading"
  }
}
```

`action` は `"standing" | "reading" | "flying"`。
これは教育用プレースホルダーであり、実運用ではオリジナルキャラクターに置き換える。

### DB

```bash
curl -X POST http://localhost:8001/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "save_record",
    "arguments": {
      "table": "experiments",
      "record": {
        "name": "test",
        "task_context": "image",
        "intent_text": "cute pop character"
      }
    }
  }'
```

### Evaluator

```bash
curl -X POST http://localhost:8002/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "evaluate_image",
    "arguments": {
      "image_path": "/path/to/image.png",
      "prompt": "a cute pop character",
      "axes": ["basic", "color", "clip_text"]
    }
  }'
```

### Blender-bpy

```bash
# SVG 生成
curl -X POST http://localhost:8003/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "generate_svg",
    "arguments": {
      "output_path": "/tmp/test.svg",
      "shapes": [
        {"type": "circle", "cx": 256, "cy": 256, "r": 100, "fill": "#ff5555"}
      ]
    }
  }'

# Blender レンダリング（Blender が PATH に通っている必要あり）
curl -X POST http://localhost:8003/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "render_svg_with_blender",
    "arguments": {
      "svg_path": "/tmp/test.svg",
      "output_path": "/tmp/test.png",
      "resolution": 512,
      "samples": 32
    }
  }'
```

## 制約

- CPU 16GB を想定。Evaluator の CLIP は `openai/clip-vit-base-patch32` を使用し、必要時に遅延ロードする。
- Blender レンダリングは CPU レンダリング（`CYCLES` + `CPU`）。
- 大規模 VLM や Diffusion モデルは利用しない。

## 今後の拡張

- `mcp/svg-generator` の分離（現在は blender-bpy 内に含む）
- ベクトル DB（pgvector）対応
- 人間評価用 UI からの MCP 呼び出し統合
