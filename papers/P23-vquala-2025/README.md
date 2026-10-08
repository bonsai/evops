# P23 — VQualA 2025

- Year: 2025
- Category: VLM / Evaluation / Pairwise
- Source: https://arxiv.org/abs/2509.09190

## Intent relevance
「近い」を「どちらが良いか」「どの基準で」「どの程度確信できるか」に分解する評価器設計へ直結する。

## Research question
大規模マルチモーダルモデルは画像の視覚品質差を比較判断できるか。

## Method
single / pair / multi-image を対象に、2AFC や multiple-choice などの比較プロトコルを使う。

## Import
- A/B pairwise preference
- score + confidence + reason
- coarse-to-fine criteria
- human set で校正

## Design implication
Reference + Intent → Candidate A/B → VLM → Preference + Score + Confidence → Calibration → Selection

## Limitation
Doraemon固有の評価信頼性やBlenderコード評価を直接解決するものではない。
