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

## Synthesis
1. 動画評価は多軸化する。
2. VLMをsemantic/perceptual evaluatorとして利用する。
3. 評価を生成改善のFeedbackへ接続する。
4. 評価履歴を構造化データとして蓄積する。
5. 蓄積履歴からMLでranking、prediction、repair strategyを改善する。

研究対象は Generation → LMS/VLM → DB → ML → Repair → Generation の継続的な評価・学習ループである。
