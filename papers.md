# Research Papers — Animation Automation / VLM Evaluation

## Research theme

**VLMを用いた異種アニメーション生成バックエンドの共通評価・改善ループ**

10日間の実装では、生成モデルそのものを作るのではなく、

~~~text
Animation Intent
  ↓
Generator
  ↓
Render
  ↓
VLM / Programmatic Evaluation
  ↓
Score + Failure Reason
  ↓
Repair Prompt / Skill
  ↓
Regenerate
~~~

という評価・改善ループを研究対象とする。

対象バックエンド:

- Blender / bpy
- SVG / CSS Animation
- Stable Diffusion 1.5（比較用ベースライン）

---

## 1. VeMo — Zero-Shot Text-to-Motion Evaluation using Video Language Models

**ICML 2026**

- Paper: https://proceedings.mlr.press/v306/ji26l.html
- Code / project: https://github.com/jihoonerd/VeMo

### 概要

テキストで指定された3Dモーションと、実際に生成・レンダリングされたモーション動画の意味的一致をVideo Language Modelで評価する研究。

### 今回との関係

最も直接的に参考になる論文。

~~~text
Animation Intent
      ↓
Blender / Motion
      ↓
Render Video
      ↓
VLM
      ↓
Text-Motion Alignment
~~~

という構成が、今回の Blender/bpy → Render → VLM評価 に対応する。

### 取り入れる考え方

- テキストで表現したAnimation Intentを評価基準にする
- レンダリングされた動画をVLMへ入力する
- 動きの意味的一致を評価する
- 人間評価との相関を評価する

### 今回の仮説

> VLMによる意味的評価は、BlenderだけでなくSVG/CSSやSD系の生成結果にも共通化できる。

---

## 2. EvalCrafter — Benchmarking and Evaluating Large Video Generation Models

**CVPR 2024**

- Paper: https://openaccess.thecvf.com/content/CVPR2024/html/Liu_EvalCrafter_Benchmarking_and_Evaluating_Large_Video_Generation_Models_CVPR_2024_paper.html
- Project: https://evalcrafter.github.io/

### 概要

動画生成モデルを多面的に評価するためのベンチマーク。

Visual Quality、Content、Motion、Text-Video Alignment、Temporal Consistencyなど、動画品質を複数の評価軸に分解する。

### 今回との関係

今回の「評価軸の言語化・DB化」の中心的な参考資料。

単一の quality スコアではなく、評価をOntologyとして分解する。

### 今回の評価軸案

- semantic
- motion
- temporal
- character
- composition
- visual_quality
- artifact

評価軸そのものをJSONLとして管理し、実験結果と分離する。

---

## 3. VideoScore — Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation

**EMNLP 2024**

- Paper: https://aclanthology.org/2024.emnlp-main.127/

### 概要

動画生成結果に対する人間の多面的な評価を利用して、自動動画評価器を構築する研究。

動画生成を単純な一つのスコアではなく、細粒度の品質評価として扱う。

### 今回との関係

今回の

~~~text
Render
 ↓
Evaluation
 ↓
Failure
 ↓
Improvement
~~~

を成立させる根拠になる。

特に「評価器を生成モデル改善のためのFeedbackとして利用する」という方向が重要。

### 取り入れる考え方

- 人間が見る評価軸を構造化する
- VLM/MLLMを自動評価器として使う
- 評価結果を生成側へFeedbackする
- iterationごとのスコアを保存する

---

## 4. VisualPrompter

**ICLR 2026**

- Paper: https://proceedings.iclr.cc/paper_files/paper/2026/hash/33c8427b6fbd5622a04b51b0af7d705c-Abstract-Conference.html

### 概要

生成画像を自動評価し、視覚的なフィードバックから不足している概念を発見し、プロンプトを修正する方向の研究。

### 今回との関係

今回の

~~~text
Generate
 ↓
VLM Evaluation
 ↓
Failure Reason
 ↓
Repair Prompt
 ↓
Generate Again
~~~

に対応する。

### 今回の実装

VLMの出力を単なる評価値として捨てず、

~~~json
{
  "primary_failure": "foot_sliding",
  "repair_instruction": "Keep the planted foot stationary during ground contact."
}
~~~

のような構造化Feedbackとして保存する。

そのFeedbackから次のPrompt / Skill invocationを生成する。

---

## 5. Quality Assessment of 3D Human Animation: Subjective and Objective Evaluation

**IEEE Transactions on Visualization and Computer Graphics, 2026**

- PubMed: https://pubmed.ncbi.nlm.nih.gov/41223104/

### 概要

3Dヒューマンアニメーションの品質について、主観評価と客観評価を比較し、品質予測を扱う研究。

### 今回との関係

「VLMだけを正解としない」という設計の参考になる。

今回も、

~~~text
VLM = semantic / perceptual evaluation
Python = measurable evaluation
Human = validation
~~~

という3層に分ける。

---

# 共通する研究上の知見

## 1. 動画評価は単一スコアではなく多軸化する

今回のDBでは、

~~~text
semantic
motion
temporal
character
composition
visual_quality
artifact
~~~

を独立した評価軸として保存する。

---

## 2. VLMは「生成器」より「評価器」として利用する

今回の10日間では、VLMをアニメーションそのものの生成に使うことより、

> **Animation Director / QA Agent**

として使う。

~~~text
Intent
 ↓
Generator
 ↓
Render
 ↓
VLM Director
 ↓
Failure Analysis
 ↓
Repair
~~~

---

## 3. 評価結果をDBに蓄積する

生成結果だけではなく、

- Intent
- Backend
- Prompt
- Render
- Evaluation
- Failure
- Repair
- Next Prompt
- Score

を1つの実験履歴として保存する。

これによって「プロンプトの学習」を、モデルのFine-tuningではなく、まず**制作知識の蓄積・検索・再利用**として実装できる。

---

# 今回の評価DB案

### evaluation_axes.jsonl

~~~json
{"axis_id":"semantic","name":"Semantic Alignment","evaluator":"vlm"}
{"axis_id":"motion","name":"Motion Quality","evaluator":"vlm+python"}
{"axis_id":"temporal","name":"Temporal Consistency","evaluator":"vlm+python"}
{"axis_id":"character","name":"Character Consistency","evaluator":"vlm"}
{"axis_id":"composition","name":"Composition","evaluator":"vlm"}
{"axis_id":"visual_quality","name":"Visual Quality","evaluator":"vlm"}
{"axis_id":"artifact","name":"Artifact","evaluator":"vlm+python"}
~~~

### evaluations.jsonl

~~~json
{
  "evaluation_id":"eval001",
  "experiment_id":"exp001",
  "scores":{
    "semantic":0.91,
    "motion":0.72,
    "temporal":0.95,
    "character":0.98,
    "composition":0.87,
    "visual_quality":0.81,
    "artifact":0.12
  },
  "primary_failure":"foot_sliding",
  "repair_instruction":"Keep the planted foot stationary during ground contact.",
  "confidence":0.84,
  "decision":"iterate"
}
~~~

---

# 3 Backend Experiment

## A. Blender / bpy

### Purpose

制御可能な3Dアニメーション生成。

### Pipeline

~~~text
Animation Intent
 ↓
LLM / Skill
 ↓
bpy
 ↓
Blender
 ↓
Render
 ↓
VLM
 ↓
Repair
 ↓
bpy
~~~

### Candidate actions

- walk
- wave
- jump
- turn
- camera movement

10日間ではまず **simple robot / simple character** を対象にする。

---

## B. SVG / CSS

### Purpose

高速な2Dアニメーション評価環境。

### Pipeline

~~~text
Animation Intent
 ↓
SVG Generator
 ↓
CSS Animation
 ↓
Browser
 ↓
Capture
 ↓
VLM
~~~

生成・評価が速いため、共通Evaluatorの開発・デバッグに利用する。

---

## C. Stable Diffusion 1.5

### Purpose

画像生成系バックエンドの比較用ベースライン。

SDを主役にせず、

- generation latency
- visual quality
- semantic alignment
- consistency

を測定する。

特に、Blender / SVGと比較して反復速度が遅いかどうかをデータ化する。

---

# Research Hypotheses

### H1 — Common Evaluation

VLM-based semantic and perceptual evaluation can be shared across different animation generation backends.

### H2 — Structured Evaluation Ontology

Explicitly modeling evaluation axes as structured data improves comparison, analysis, and reuse.

### H3 — Feedback Loop

VLM-generated failure descriptions can be transformed into repair instructions and used to improve subsequent generations.

### H4 — Backend Efficiency

Deterministic generators such as Blender/bpy and SVG/CSS can provide shorter and more controllable evaluation-improvement loops than SD 1.5.

---

# 10-Day Research Plan

| Day | Task | Output |
|---|---|---|
| 1 | Literature / ontology | evaluation axes |
| 2 | JSONL schema | experiment DB |
| 3 | VLM evaluator | structured JSON evaluation |
| 4 | SVG/CSS baseline | fast backend |
| 5 | Blender/bpy baseline | 3D backend |
| 6 | Blender MCP | tool integration |
| 7 | SD1.5 baseline | comparison |
| 8 | Repair Prompt | feedback loop |
| 9 | Cross-backend experiment | benchmark data |
| 10 | Dashboard / report | research result |

---

# Architecture

~~~text
                 Animation Intent
                        |
                +-------v-------+
                |     Skill     |
                | knowledge / QA|
                +-------+-------+
                        |
             +----------+----------+
             |          |          |
          Blender    SVG/CSS      SD1.5
           /bpy
             |          |          |
             +----------+----------+
                        |
                     Render
                        |
              +---------v---------+
              | VLM + Python Eval|
              +---------+---------+
                        |
                Evaluation DB
                        |
                 Failure Reason
                        |
                 Repair Prompt
                        |
                    Iterate
~~~

### Role separation

- **Skill** = 制作知識・評価知識・判断方法
- **MCP** = Blender / Browser等の外部ツール操作
- **Python** = 評価、画像・動画処理、DB、科学計算、プロトタイピング
- **Rust** = Pythonでボトルネックになった高速処理だけ担当
- **VLM** = semantic / perceptual director and evaluator

---

# Conclusion

今回の10日間では、SD 1.5そのものを高度化することを目的にしない。

**研究の中心を「共通Animation Evaluation Loop」に置く。**

~~~text
Intent
 → Generate
 → Render
 → Evaluate
 → Explain Failure
 → Repair
 → Generate
~~~

Blender/bpy、SVG/CSS、SD1.5を同じIntentで比較し、同じ評価OntologyとVLM evaluatorを適用することで、

> **異なる生成バックエンドに対して共通の評価・改善ループを構築できるか**

を10日間で検証する。

これは将来的に、キャラクター、建築物、アバターなど異なるアニメーション対象にも拡張できる。
