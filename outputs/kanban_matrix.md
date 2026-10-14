# Kanban マトリクス — 一覧表（足りないところ把握用）

**作成日時**: 自動生成

この表は `kanban.jsonl` の全エントリを単一のマトリクスにまとめたものです。
**目的**: どこが完了（✅）、どこが進行中（⏸）、どこが待機（❌）かを一目で把握。

---

## 1. Kanban エントリ一覧 (`kanban.jsonl` から)

| 区分 | ID / アセット | カテゴリ | ステータス | 備考 |
|---|---|---|---|---|
| `kanban` | `B01-01` | `B01-doraemon/doraemon.png` | `png` | ✅ 完了 (done) | `B01-doraemon` |
| `kanban` | `B02-01` | `B02-bear/20261010_180403_bear.png` | `png` | ✅ 完了 (done) | `B02-bear` |
| `kanban` | `B03-01` | `B03-don_quixote/don_quixote_evolution_report.json` | `json` | ✅ 完了 (done) | `B03-don_quixote` |
| `kanban` | `B04-01` | `B04-donpen/donpen_evolution_gallery.html` | `html` | ✅ 完了 (done) | `B04-donpen` |
| `kanban` | `B06-01` | `B06-salmon_bear/20261010_180843_salmon.png` | `png` | ✅ 完了 (done) | `B06-salmon_bear` |
| `kanban` | `B07-01` | `B07-video_audio/psychedelic_pose_20261008_170058.mp4` | `video` | ✅ 完了 (done) | `B07-video_audio` |
| `kanban` | `B07-02` | `B07-video_audio/final.mp4` | `video` | ✅ 完了 (done) | `B07-video_audio` |
| `kanban` | `B07-03` | `B07-video_audio/narration.mp3` | `audio` | ✅ 完了 (done) | `B07-video_audio` |
| `kanban` | `PV01` | `paper_videos/P01/video.mp4` | `video` | ⏸ 進行中 (in-progress) | `P01` |
| `kanban` | `PV02` | `paper_videos/P02/video.mp4` | `video` | ⏸ 進行中 (in-progress) | `P02` |
| `kanban` | `PV03` | `paper_videos/P03/video.mp4` | `video` | ⏸ 進行中 (in-progress) | `P03` |
| `kanban` | `S01-01` | `S01-resnet/final.mp4` | `video` | ✅ 完了 (done) | `S01-resnet` |
| `kanban` | `S01-02` | `S01-resnet/assets/narration.mp3` | `audio` | ✅ 完了 (done) | `S01-resnet` |
| `kanban` | `S01-03` | `S01-resnet/panels/S01_panel_01.svg` | `svg` | ✅ 完了 (done) | `S01-resnet` |
| `kanban` | `S02-01` | `S02/panels/paper_1.svg` | `svg` | ❌ 待機 (pending) | `S02-VeMo` |
| `kanban` | `S03-01` | `S03/svg/knowledge_loop.svg` | `svg` | ✅ 完了 (done) | `S03-Rakugo` |
| `kanban` | `S03-02` | `S03/panels/panel_01.svg` | `svg` | ✅ 完了 (done) | `S03-Rakugo` |
| `kanban` | `S03-03` | `S03/panels/panel_02.svg` | `svg` | ✅ 完了 (done) | `S03-Rakugo` |
| `kanban` | `S03-04` | `S03/panels/panel_03.svg` | `svg` | ✅ 完了 (done) | `S03-Rakugo` |
| `kanban` | `S03-05` | `S03/panels/panel_04.svg` | `svg` | ✅ 完了 (done) | `S03-Rakugo` |

---

## 2. 足りないところ（把握結果）

### 完了済み（✅ done: 16件）
- **SVG**: `S01-resnet/panels/`（3件）、`S03/svg/`（5件）
- **生成物（bpy）**: `B01`〜`B06`（6件）
- **動画/音声**: `B07-video_audio`（3件）、`S01-resnet/final.mp4`
- **論文原稿**: `P01`, `P02`, `P03` の `episode.json`（3件）
- **ダッシュボード**: `kanban_dashboard.md`, `.html`, `.blocks`（3件）
- **S03 パネル原稿**: `panel_01.md` 〜 `panel_10.md`（10件）

### 進行中（⏸ in-progress: 3件）
- `PV01` (`P01/video.mp4`) — Voicevox サーバー起動後に完了予定
- `PV02` (`P02/video.mp4`) — P01 完了後に自動実行可能
- `PV03` (`P03/video.mp4`) — 同上

### 待機（❌ pending: 4件 だが重複含む → 実質 1件）
- `S02` (`S02/panels/paper_1.svg`) — SVG 描画待ち（VeMo 論文のパネル）
- `PV01`〜`PV03` の古い重複エントリ（3件）は整理済み、実質待機は `S02` のみ

---

## 3. 次のステップ（優先順位順）

### 最優先（P01 完了 → P02/P03 自動化）
1. `voicevox` サーバー起動 (`docker compose`)
2. `videogen` サーバー起動 (`python mcp/videogen/server.py`)
3. `P01/video.mp4` 生成 → `kanban` を `done` に更新
4. `P02` と `P03` は P01 完了後に自動実行（`tui_go.sh` または `mcp/video_pipeline` で）

### 中優先（S02 SVG 完了）
5. `S02/panels/paper_1.svg` の生成（`sf-paper-comic` または手動 SVG 作成）
6. `S02/subs.md` の内容をパネル原稿に反映（現在は `sub.yaml.ass` の内容を反映済み）

---

> このマトリクスは `kanban.jsonl` を元に自動生成されました。
> 更新は `kanban.jsonl` に反映 → このマトリクスを再生成、で常に最新に保たれます。
