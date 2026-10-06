# SSSS Papers

## Research question
LMS/VLMを共通評価器として使い、評価結果をDBへ蓄積し、MLによる改善へ接続できるか。

## VeMo
**Zero-Shot Text-to-Motion Evaluation using Video Language Models / ICML 2026**

Text-to-motionと生成動画の意味的一致をVideo Language Modelで評価する研究。Animation Intent → Render → VLM評価の主要参考。

## EvalCrafter
**Benchmarking and Evaluating Large Video Generation Models / CVPR 2024**

Visual Quality、Motion、Text-Video Alignment、Temporal Consistencyなど複数軸で動画生成を評価する。評価Ontology設計の主要参考。

## VideoScore
**Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation / EMNLP 2024**

細粒度な人間評価を自動評価へ変換する研究。評価器を生成改善へのFeedback sourceとして扱う設計に対応。

## VisualPrompter
**ICLR 2026**

視覚的評価から不足概念を発見し、プロンプト改善へ接続する方向の研究。VLM出力をfailure / repair instructionとして保存する設計に対応。

## 3D Human Animation Quality Assessment
**Quality Assessment of 3D Human Animation: Subjective and Objective Evaluation / IEEE TVCG 2026**

3Dアニメーションの主観・客観評価と品質予測を扱う。VLM、Python測定、人間検証を分離する設計の参考。

## 3D 生成の先駆研究
- **DreamFusion: Text-to-3D using 2D Diffusion / ICCV 2023**
  Text-to-3D の金字塔。Score Distillation Sampling でテキストから 3D 造型を最適化。
  テーマ 2 の「テキスト → bpy」生成の先例。
- **Point-E: A System for Generating 3D Point Clouds from Textual Descriptions / CVPR 2023**
  Text-to-3D の高速生成パイプライン。生成→評価ループの高速化の先例。
- **Magic3D: High-Resolution Text-to-3D Content Creation / CVPR 2024**
  Text-to-3D の高解像度化。多段階生成→upscale の設計。

## VLM 評価の基礎
- **CLIP: Learning Transferable Visual Models From Natural Language Supervision / ICML 2021**
  画像とテキストを共通空間に埋め込むゼロショット評価の基盤。CPU でも動作する軽量版が広く利用可能。
- **What matters when building vision-language models? / arXiv 2024 (Idefics2)**
  VLM 設計の決定要因を実験的に明らかに。評価器選び（サイズ・データ）の指針。

## 嗜好予測・人間フィードバック
- **Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation / NeurIPS 2023**
  Text-to-image 生成のための大規模嗜好データセット。PickScore は軽量な嗜好予測モデル。
- **ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation / NeurIPS 2023**
  人間の嗜好を学習したテキスト画像評価モデル。
- **Human Preference Score v2 / arXiv 2023**
  Text-to-image 生成の人間嗜好ベンチマークとスコアリングモデル。
- **Training language models to follow instructions with human feedback (InstructGPT / RLHF) / NeurIPS 2022**
  人間の偏好データから報酬モデルを学習し、PPO で最適化。インテント → 報酬 → 改善の理論基盤。
- **Direct Preference Optimization (DPO) / NeurIPS 2024**
  報酬モデルなしでペアワイズ嗜好データから直接最適化。データ効率が良い。

## アクティブラーニング・コスト管理
- **Active Learning for Large Language Model-based Chatbots / EMNLP 2023**
  人間アノテーションコストを抑えつつ効率的に学習データを選ぶ手法。
- **The False Dawn: Reevaluating Performance Gains of Small Language Models / arXiv 2024**
  SLM の性能とコストのトレードオフを検証。CPU 制約下でのタスク分担指針。

## エージェント連携プロトコル
- **Model Context Protocol (MCP) / Anthropic 2024**
  LLM と外部ツール・データソースを標準接続するオープンプロトコル。
- **Agent2Agent Protocol (A2A) / Google 2025**
  エージェント間の相互運用プロトコル。

## 軽量モデル
- **Phi-3 Technical Report / arXiv 2024**
  Microsoft の小規模・高品質言語モデル。CPU でも実用的。
- **Llama 3.2 / Meta 2024**
  エッジデバイス向け軽量マルチモーダルモデル。1B/3B は CPU で動作可能。

## 信頼性・出典管理
- **A Watermark for Large Language Models / ICML 2023**
  LLM 出力の追跡可能な透かし。生成物・評価の信頼性管理の参考。

## Synthesis
1. 動画・画像評価は多軸化し、軽量モデル（CLIP, PickScore, ImageReward, HPSv2）で近似可能。
2. VLM を semantic/perceptual evaluator として利用するが、CPU 制約では CLIP-small 等の軽量版を使う。
3. 人間の嗜好はペアワイズ比較で効率的に収集し、Bradley-Terry や DPO で学習する。
4. MCP でツール層を標準化し、A2A でエージェント連携を標準化する。
5. 評価結果を生成改善の Feedback source として扱い、構造化データとして蓄積する。
6. 人間フィードバックは有限・高価なので、アクティブラーニングで高情報量サンプルを選ぶ。
7. SLM（Phi-3, Llama 3.2 等）を使い、CPU 16GB 内で回転ループを回し続ける。
8. 蓄積履歴から ML で ranking、prediction、repair strategy を改善する。

## Loop
Generation → Auto Evaluation → Human Feedback → DB → Intent Estimation → Criteria Update → Repair → Generation の継続的な評価・学習ループ。
