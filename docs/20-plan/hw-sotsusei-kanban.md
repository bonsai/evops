# hw‑sotsusei Kanban – Structured by Road‑map Phases (Stage 0‑2)

The three phases follow the roadmap described in [Issue #30](https://github.com/bonsai/hw-sotsusei/issues/30) and [Issue #29](https://github.com/bonsai/hw-sotsusei/issues/29):

| Stage | Theme | Goal / Dependency |
|------|-------|-------------------|
| **Stage 0 – MCP 基盤整備** | Infrastructure, orchestration, evaluation foundations | Must be completed before any video‑generation or Doraemon‑loop work can rely on stable MCP / evaluation pipelines. |
| **Stage 1 – 論文・動画生成** | Paper‑driven video/animation production, quality improvement | Depends on Stage 0 MCP & evaluation; produces the “論文SF落語動画” (paper‑SF‑rakugo video) artefact. |
| **Stage 2 – ドラえもん成長進化ループ** | Doraemon‑centric generative loops, character evolution, mobile‑first workflows | Depends on Stage 1 video artefacts; aims at an autonomous, self‑sufficient loop (Goal from #31). |

Below are the current 33 issues grouped under these stages (assignment is based on keywords in the title; feel free to move issues between columns as the roadmap evolves).

---  

## 📦 Stage 0 – MCP 基盤整備

| # | Title |
|---|-------|
| **33** | Jules向け：Progress MCPで研究6段階をGitHub実績から自動評価・最終ページへ可視化 |
| **26** | Poly Haven素材を取得して4シーンアニメーションを生成するMCPワークフローを実装 |
| **22** | WF + Web UI + API中心の開発ループとGCP/Cloudflare/MCP相互運用を構築する |
| **21** | JSONデザインシステムを合理化しWeb UI生成の共通仕様にする |
| **14** | Blender / Photoshop / 映像編集の役割分担とMCP操作を検証する |
| **6** | プロンプト・コード・評価知識のオントロジー＋DB化 |
| **9** | 評価閾値と90%到達基準を定義する |
| **8** | 評価可視化：意味グラフ＋数値折れ線グラフ＋チャート |
| **7** | 圧縮・展開ループ：生成知識を収束させる |
| **4** | 評価ループ：生成画像とコードからGood/Badを抽出し修正・固定する |
| **3** | 自然淘汰型の生成手法探索を実装する：VLM評価 × ML/GA × 手法選択 |
| **2** | 文献収集・自動要約パイプラインの構築 |
| **1** | 文献調査リサーチエージェントの作成 |

---  

## 📦 Stage 1 – 論文・動画生成

| # | Title |
|---|-------|
| **30** | 研究ロードマップを3段階化：0 MCP完全化 → 1 論文SF落語動画 → 2 ドラえもん成長進化ループ |
| **29** | 研究課題を2系統に分離：01 論文動画化ループ / 02 ドラえもん生成進化ループ |
| **28** | VLM＋ラング三兄弟でSF動画の文字化けと脚本品質を評価・改善する閉ループを実装 |
| **27** | 論文SFアニメの生成基盤をPygame / Blender / Godot併用へ拡張し、動画Artifactのみデプロイする |
| **25** | 論文から得られた設計原則：8本柱の要約 |
| **19** | 生成物への「やわらかなダメだし」評価とパラメータ固定のループを設計する |
| **17** | ArtCraftをAgent/MCPによる編集・修正層として評価する |
| **15** | 簡易アニメーション生成：評価ループの成果を動画化する |
| **16** | SD生成はサムネイル用途に限定する |
| **12** | 2D SVG POC：家を描き、MD/JSON/DXF/G-code/JSXへ変換可能なベクター表現を作る |
| **10** | 世代別統計：評価ループの収束・停滞・淘汰を分析する |

---  

## 📦 Stage 2 – ドラえもん成長進化ループ

| # | Title |
|---|-------|
| **31** | ゴールとイシューから逆算して研究基盤を疎結合・自給自足へ再設計 |
| **32** | スマホだけで進められる研究作業を切り出す |
| **24** | MMDからCSSアニメーションを作るプレゼン資料構成図の動的視覚化 |
| **23** | やわらかなダメだし：生成物の不満足を放置しない付き合い方を設計する |
| **11** | ドラえもん顔の進化をPNG連番から簡易アニメーション化する |
| **5** | ドラえもんらしさの多尺度定義：自然言語・コード・ピクセル・mm・角度・比率 |

---  

#### How to use this Kanban
1. **Create a board** (e.g., GitHub Projects, Trello, or a physical board) with three columns titled **Stage 0**, **Stage 1**, **Stage 2**.  
2. **Add cards** for each issue number/title listed under the appropriate column.  
3. **Move cards** forward as dependencies are satisfied: all Stage 0 cards must be closed (or marked “in progress”) before starting Stage 1, and similarly Stage 1 before Stage 2.  

---  

*Generated from the GitHub issue list of `bonsai/hw-sotsusei` (33 open issues).*