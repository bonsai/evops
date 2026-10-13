# MCP Servers (evops) — Core Infrastructure

**MCP レベルのインフラのみ。** ドメイン固有のスキル（bpy-gen, videogen, artcraft 等）は `../skills/` に移動済み。

## 構成

```
mcp/
├── base_server.py           # FastMCP + FastAPI 共通ラッパー
├── db/                      # SQLite 履歴管理 (port 8001)
├── evaluator/               # 画像評価 (port 8002)
├── gateway/                 # MCP ゲートウェイ統合
├── mcp-db/                  # DB 操作 MCP
├── papers/                  # 論文データストア
├── tests/                   # MCP テストユーティリティ
└── README.md                # このファイル
```

## サービス一覧

| サーバー | ポート | 役割 | 活用先 |
|---------|--------|------|--------|
| `db/server.py` | 8001 | SQLite 生成履歴・評価データ | 全ステージ |
| `evaluator/server.py` | 8002 | CLIP/基本指標/色彩/動画/AA/エフェクト評価 | Eval ステージ |
| `gateway/server.py` | — | MCP サーバー統合ゲートウェイ | 統合制御 |

## スキル（移動済み）

以下のドメインスキルは `evops/skills/` に配置されています。MCP サーバー実装も含まれます：

| スキル | 旧パス | 新パス |
|--------|--------|--------|
| bpy-gen | `mcp/bpy-gen/` | `skills/bpy-gen/` |
| sf-paper-comic | `mcp/sf-paper-comic/` | `skills/sf-paper-comic/` |
| videogen | `mcp/videogen/` | `skills/videogen/` |
| artcraft | `mcp/artcraft/` | `skills/artcraft/` |
| egg-shadow | `mcp/egg-shadow/` | `skills/egg-shadow/` |
| lang-brothers | — | `skills/lang-brothers/` |
| chaperone | — | `skills/chaperone/` + 独立リポジトリ |
| telop | — | `skills/telop/` |
| voicevox | — | `skills/voicevox/` |
| effect-eval | — | `skills/effect-eval/` |
| fontgen | — | `skills/fontgen/`（外部リポジトリ連携） |

## Chaperone ワークフロー統合

[chaperone](https://github.com/bonsai/chaperone) リポジトリに workflow manager を push 済み：

```bash
cd /home/bons/chaperone
node cli/chaperone-cli.js run ~/evops/workflow.yaml
```
