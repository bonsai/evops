# Papers structure

## Principle

**1論文 = 1フォルダ**。P番号を安定IDとして使う。

各論文は同じ3層にする。

- `README.md` — 何を研究したか / hw-sotsuseiへ何を取り込むか
- `concept.mmd` — 論文の方法・関係を構造化
- `explain.svg` — 概念グラフをCSSでアニメーション表示

## Shared

- `_shared/paper-animation.css` — 共通アニメーション
- `animation/index.html` — アニメーション一覧
- `index.html` — 文献Index
- `papers.html` — 研究文献のビジュアル目次
- `ontology.html` — 研究Ontology
- `papers.jsonl` — 正規データ
- `papers.json` — JSONビュー
- `papers.md` — 全体統合メモ
- `intent.md` — 調査Intent
- `gen_papers.py` — 生成補助

## Naming

`Pxx-short-title-year/`

例:

- `P23-vquala-2025/`
- `P24-uniapo-2025/`
- `P25-b-coder-2024/`

旧形式の `vquala-2025.md` などは廃止し、論文フォルダをCanonicalとする。

## Expansion

P23–P25で型を検証済み。次にP01–P22を同じ構造へ移行する。
