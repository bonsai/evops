# 論文から得られた設計原則（8本柱）

## 01
動画・画像評価は多軸化し、軽量モデル（CLIP, PickScore, ImageReward, HPSv2）で近似可能。

## 02
VLM は semantic/perceptual evaluator として利用するが、CPU 制約では CLIP-small 等の軽量版を使う。

## 03
人間の嗜好はペアワイズ比較で効率的に収集し、Bradley-Terry や DPO で学習する。

## 04
MCP でツール層を標準化し、A2A でエージェント連携を標準化することでモジュール性と差し替え性を確保する。

## 05
評価結果を生成改善の Feedback source として扱い、構造化データとして蓄積する。

## 06
人間フィードバックは有限・高価なので、アクティブラーニングで高情報量サンプルを選び、コストを抑える。

## 07
SLM（Phi-3, Llama 3.2 等）を使い、CPU 16GB 内で回転ループを回し続ける。

## 08
蓄積履歴から ML で ranking、prediction、repair strategy を改善する。