# bpy-gen MCP Service

Blender Python 生成ツールの MCP サーバー。`blender-bpy/` とは独立したマイクロサービスとして回転。

## ツール

| ツール名 | 説明 |
|---------|------|
| `render_doraemon` | ドラえもんを 3D 生成して PNG にレンダリング |
| `render_pagoda` | 五重塔を 3D 生成して PNG にレンダリング |
| `render_bear` | ローポリ木彫りクマを 3D 生成して PNG にレンダリング |

## 起動

```bash
# stdio モード（MCP クライアント用）
python mcp/bpy-gen/server.py

# HTTP モード
python mcp/bpy-gen/server.py --http --port 8005
```

## 呼び出し例（HTTP）

```bash
curl -X POST http://localhost:8005/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "render_doraemon",
    "arguments": { "output_path": "/tmp/doraemon.png" }
  }'
```

Blender は `BLENDER_EXECUTABLE` 環境変数で指定可能（デフォルト: `blender`）。
出力は WSL 側ではなく、指定されたパス（Windows 側パスでも可）。