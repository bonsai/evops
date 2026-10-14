# Papers

P01–P25の研究文献を、**論文 → 解説 → 概念グラフ → アニメーション**として整理する。

## Canonical structure

```
papers/
├─ P01-.../                 # 1論文 = 1フォルダ
│  ├─ README.md             # 論文解説・研究への取り込み
│  ├─ concept.mmd           # Mermaid / 概念グラフ
│  └─ explain.svg           # SVG + CSS アニメーション
├─ ...
├─ P25-.../
├─ _shared/                 # 共通CSS
├─ animation/               # 論文アニメーション・ビューア
├─ index.html               # 調査Index
├─ papers.html              # 論文目次 / ビジュアル一覧
├─ ontology.html            # 研究Ontology
├─ papers.jsonl             # 論文データ（正規データ）
├─ papers.json              # JSONビュー
├─ papers.md                # 調査全体の統合メモ
├─ intent.md                # 調査Intent
└─ gen_papers.py            # 生成・更新スクリプト
```

## Rule

- **P番号を永続ID**にする
- **1論文 = 1フォルダ**
- 論文の説明本文は `README.md`
- 構造・関係は `concept.mmd`
- ブラウザで動く説明図は `explain.svg`
- 古い `Pxx-title.md/mmd/html` の直置きは作らない
- データと表示を分離する
- P01–P25を同じ形式へ揃える

## Flow

```
PDF / URL
   ↓
Paper README
   ↓
Concept MMD
   ↓
SVG
   ↓
CSS Animation
   ↓
Research Design
```

現在、P23–P25をこの形式の実装済みパイロットとする。
