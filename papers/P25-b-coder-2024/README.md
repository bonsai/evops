# P25 — B-CODER

- Year: 2024 / ICLR
- Category: Program Synthesis / Selection
- Source: https://arxiv.org/abs/2310.03173

## Intent relevance
bpyコードをgenomeの一部として扱い、実行可能性と見た目を別々の信号として学習する設計に直結する。

## Research question
実行可能なプログラムと過去の生成履歴から価値を学習し、program synthesis の探索を改善できるか。

## Method
value-based reinforcement learning と value function を使い、生成プログラムを検証可能な候補として扱う。

## Import
- bpy code を inspectable artifact にする
- execute/render success を hard signal にする
- historical candidates を保存
- 有望なmutationを学習
- validity と visual score を分離

## Design implication
Intent → Code Generator → Candidate Code → Execute/Render → Verifiable Reward → Value Model → Selection

## Limitation
実行可能なBlender script = 見た目が正しい、ではない。
