# P24 — UniAPO

- Year: 2025
- Category: Multimodal / Prompt Optimization
- Source: https://arxiv.org/abs/2508.17890

## Intent relevance
プロンプト・コード・評価知識を履歴として蓄積し、次の生成方法へ戻す閉ループ設計に対応する。

## Research question
マルチモーダル生成で、評価フィードバックと履歴を使ってプロンプトを自動改善できるか。

## Method
feedback modeling と prompt refinement を分け、short-term / long-term memory を使う。

## Import
- 評価とmutationを分離
- 成功履歴を再利用
- 短期履歴と圧縮知識を分ける
- prompt mutation を method-selection の一演算子にする

## Design implication
History → Feedback Model → Prompt/Genome Mutation → Candidate → Evaluate → History

## Limitation
Blender geometry optimization や自然選択全体を代替するものではない。
