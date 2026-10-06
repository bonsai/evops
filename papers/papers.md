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
- **DreamFusion: Text-to-3D using 3D Diffusion / CVPR 2023**
  Text-to-3D の金字塔。Score Distillation Sampling でテキストから 3D 造型を最適化。
  テーマ 2 の「テキスト → bpy」生成の先例。
- **Point-E: A System for Generating 3D Point Clouds from Textual Descriptions / ICCV 2023**
  Text-to-3D の高速生成パイプライン。生成→評価ループの高速化の先例。
- **Magic3D: High-Resolution Text-to-3D Content Creation / CVPR 2024**
  Text-to-3D の高解像度化。多段階生成→upscale の設計。

## VLM 評価の基礎
- **What matters when building vision-language models? / arXiv 2024 (Idefics2)**
  VLM 設計の決定要因を実験的に明らかに。評価器選び（サイズ・データ）の指針。
- **Zero-Shot Text-to-Motion Evaluation using Video Language Models / ICML 2026 (VeMo)**
- **Benchmarking and Evaluating Large Video Generation Models / CVPR 2024 (EvalCrafter)**
- **Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation / EMNLP 2024 (VideoScore)**
- **VisualPrompter / ICLR 2026**
- **Quality Assessment of 3D Human Animation: Subjective and Objective Evaluation / IEEE TVCG 2026**

## Synthesis
1. 動画評価は多軸化する。
2. VLM を semantic/perceptual evaluator として利用する。
3. 評価を生成改善の Feedback へ接続する。
4. 評価履歴を構造化データとして蓄積する。
5. 蓄積履歴から ML で ranking、prediction、repair strategy を改善する。

研究対象は Generation → LMS/VLM → DB → ML → Repair → Generation の継続的な評価・学習ループである。
