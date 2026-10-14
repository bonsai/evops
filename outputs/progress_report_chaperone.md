# 進捗報告 — chaperone 管理下のパイプライン（介添え報告）

## 管理体制
- **オーケストレーター**: `chaperone.yaml` (`/home/bons/chaperone/`)
- **キャスト**: はっちゃん、熊さん、ご隠居さん、ななちゃん
- **外部接続**: Voicevox (`:50021`)、kamishibai (`/home/bons/kamishibai`)
- **MCP ゲートウェイ**: sf-paper-comic (`:8004`)、videogen (`:8006`)、evaluator (`:8002`)、bpy-gen (`:8005`)

---

## パイプライン別進捗（色分けダッシュボード連携）

### 1. P01 — VeMo (Zero-Shot Text-to-Motion)
| ステップ | 状態 | 備考 |
|---|---|---|
| 論文サーベイ | ✅ 完了 | `papers/P01-vemo-2026/README.md` |
| 4コマ企画 (`episode.json`) | ✅ 完了 | `paper_videos/P01/episode.json` |
| SVG 描画 | ⏸ 待機 | `S02/panels/paper_1.svg` が `pending` |
| アニメーション（raw.mp4） | ⏸ 待機 | `kanban` で `in-progress` |
| ナレーション（Voicevox / ななちゃん or Hibiki） | ⏸ 待機 | `voicevox_batch.py` 準備済み |
| テロップ焼き込み | ⏸ 待機 | `telop` スキル準備済み |
| 動画編集（videogen） | ⏸ 待機 | `videogen/server.py` 準備済み |
| 評価（evaluator） | ⏸ 待機 | `mcp/evaluator/server.py` 準備済み |
| **動画出力** | `pending` / `in-progress` | `kanban_dashboard_color.html` で可視化 |

### 2. P02 — EvalCrafter (Benchmarking Video Gen)
| ステップ | 状態 | 備考 |
|---|---|---|
| 論文サーベイ | ✅ 完了 | `papers/P02-evalcrafter-2024/` |
| 4コマ企画 | ✅ 完了 | `paper_videos/P02/episode.json` |
| SVG 描画～動画出力 | ⏸ 待機（パイプライン共通化で P01 完了後に自動実行可能） | `kanban` で `in-progress` |

### 3. P03 — VideoScore (Fine-grained Human Feedback)
| ステップ | 状態 | 備考 |
|---|---|---|
| 論文サーベイ | ✅ 完了 | `papers/P03-videoscore-2024/` |
| 4コマ企画 | ✅ 完了 | `paper_videos/P03/episode.json` |
| SVG 描画～動画出力 | ⏸ 待機（P01 完了後に自動実行可能） | `kanban` で `in-progress` |

---

## 全体進捗（Kanban 連携）

### 完成（`done`: 16 件）
- **bpy 生成物**（B01-B06）: `B01-doraemon`, `B02-bear`, `B03-don_quixote`, `B04-donpen`, `B05-pagoda`, `B06-salmon_bear`
- **動画/音声**（B07）: `psychedelic_pose_20261008_170058.mp4`, `final.mp4`, `narration.mp3`
- **SVG パネル**（S01, S03）: `S01-resnet/panels/`, `S03/svg/knowledge_loop.svg`, `S03/panels/*.svg`
- **論文原稿**（S02, P01-P03）: `S02/subs.md`, `P01/P02/P03/episode.json`
- **ダッシュボード**（3 種）: `kanban_dashboard.md`, `kanban_dashboard_blocks.html`, `kanban_dashboard_color.html`

### 進行中（`in-progress`: 3 件）
- **PV01** (`P01/video.mp4`)
- **PV02** (`P02/video.mp4`)
- **PV03** (`P03/video.mp4`)

### 待機（`pending`: 4 件）
- **S02** (`S02/panels/paper_1.svg`) — SVG 描画待ち
- **PV01-PV03 の古いエントリ**（重複登録分）

---

## 介添え（チーム・キャラクター別の貢献）

### はっちゃん（評価・分析役）
- `P01`（VeMo）の評価設計を主導
- `S03` の 4 コマ原稿（`panel_01.md` 〜 `panel_10.md`）を作成
- `kanban_dashboard.md` の構造設計を担当

### ご隠居さん（教え役）
- `S03` の知識ループ（`knowledge_loop.svg`）の構造を指導
- `chaperone.yaml` のポリシー（`on_failure: pause`, `max_retries: 1`）を設定
- `kanban_dashboard_color.html` の色分けバーを設計

### ななちゃん（ナレーション役 / デフォルト TTS）
- `voicevox-cli.js` で `speaker 2`（デフォルト: ななちゃん）を維持
- `kanban` の音声アセット (`B07-02`, `S01-02`) を生成

### 熊さん（競演役 / 少数競演作）
- `B04-donpen` の進化レポート（`donpen_evolution_report.json`）を担当
- `B07` の動画素材（`psychedelic_pose_...mp4`）の管理

---

## 次のステップ（自動実行可能なコマンド）

```bash
# TUI から動画生成（P01）
python /home/bons/evops/skills/videogen/tui.py
# → Compose Video → P01/video.mp4

# MCP サーバー経由でパイプライン開始
python /home/bons/evops/mcp/video_pipeline/server.py --pipeline P01
python /home/bons/evops/mcp/video_pipeline/server.py --pipeline P02
python /home/bons/evops/mcp/video_pipeline/server.py --pipeline P03

# ダッシュボード確認
cat /home/bons/evops/outputs/kanban_dashboard.md
open /home/bons/evops/outputs/kanban_dashboard_color.html  # msedge 等
```

---

## 結論

**全パイプライン（P01 / P02 / P03）は `chaperone.yaml` の管理下で進行中。**
- **3 本の論文動画** は `in-progress`（Voicevox サーバー起動後に完了予定）
- **S03（4コマ漫画）** は `done`（SVG + 原稿 10 話完了）
- **bpy（B01-B06）** は `done`
- **MCP サーバー**（`mcp/video_pipeline/server.py`）は準備済み
- **カラーダッシュボード**（`kanban_dashboard_color.html`）で進捗を視覚化済み
