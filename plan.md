# Research Plan

## Theme

**VLMを用いた異種アニメーション生成バックエンドの共通評価・改善ループ**

## Goal

Blender/bpy、SVG/CSS、SD1.5を同一の評価軸で比較し、VLMを中心とした

Intent → Generate → Render → Evaluate → Failure Analysis → Repair → Regenerate

の有効性を10日間で検証する。

## Research hypotheses

- **H1** — VLMベースの意味・知覚評価は異なる生成バックエンドで共通利用できる。
- **H2** — 評価軸を構造化してDB化すると、実験比較と改善知識の再利用性が高まる。
- **H3** — VLMの失敗記述を修正指示へ変換すると、次回生成の品質改善に利用できる。
- **H4** — Blender/bpyやSVG/CSSの決定的バックエンドは、SD1.5より短く制御しやすい改善ループを構成できる。

## Backend roles

| Backend | Role | Purpose |
|---|---|---|
| Blender/bpy | main | 決定的・編集可能な3Dアニメーション |
| SVG/CSS | baseline | 高速な2Dアニメーション |
| SD1.5 | baseline | 生成AI系との比較 |

SD1.5は「遅い」という感覚を結論にせず、生成時間・品質・時間的一貫性を実測する。

## Common evaluation axes

1. Semantic Alignment
2. Motion Quality
3. Temporal Consistency
4. Character Consistency
5. Composition
6. Visual Quality
7. Artifact

Artifactだけは低いほど良い指標とする。

## Role separation

- **VLM**: 意味・知覚・失敗理由・修正指示
- **Python**: 評価、画像/動画解析、DB、研究ライブラリ、プロトタイピング
- **MCP**: Blenderなど外部ツールの操作
- **Skill**: 評価知識・制作知識・修正知識の再利用
- **Rust**: 実測された処理ボトルネックがある場合のみ

## 10-day schedule

| Day | Theme | Deliverable |
|---|---|---|
| 1 | 文献・評価軸 | papers.md / evaluation axes |
| 2 | 評価DB | JSONL schema |
| 3 | VLM evaluator | JSON評価prompt |
| 4 | SVG/CSS | 高速2D baseline |
| 5 | Blender/bpy | 3D baseline |
| 6 | Blender MCP | MCP生成・再生成 |
| 7 | SD1.5 | 比較データ |
| 8 | Repair loop | failure → repair → regenerate |
| 9 | Cross-backend | 同一Intent比較 |
| 10 | Analysis | HTML dashboard / report |

## Primary experiment

**Intent:** simple cartoon robot walks left to right for 3 seconds in a simple studio, medium static shot, cartoon style.

このIntentを3バックエンドで実行し、同じ評価器・評価軸で比較する。

## Success criteria

- 3バックエンドで同一Intentを実行
- 共通評価JSONを取得
- 失敗理由から修正指示を生成
- 少なくとも1回の再生成による改善差を測定
- HTMLで結果を比較

## Repository structure

ssss/
├── papers.md
├── plan.md
├── plan.json
├── plan.html
├── ontology/
├── experiments/
├── prompts/
├── skills/
├── mcp/
└── dashboard/

plan.json を正本とし、plan.md と plan.html は研究計画を読むための派生表現とする。
papers.md は文献リサーチとして独立させる。
evaluation-axes.jsonl、experiments.jsonl、evaluations.jsonl、iterations.jsonl は実験データとして別管理する。
