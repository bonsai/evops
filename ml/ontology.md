# ML Ontology

## 目的

`ml/` は、生成結果を学習するだけの場所ではない。

**Intent と Reference に近い生成を、より少ない無駄で実現するために、評価履歴から「次に何を試すか」「どの手法を残すか」「どの手法を殺すか」を学習・探索する層**である。

## Core ontology

```
Intent
  ↓
Reference
  ↓
Generation Method
  ↓
Candidate
  ↓
Artifact
  ↓
Evaluation
  ↓
Fitness
  ↓
Learning
  ↓
Selection
  ├─ Elite
  ├─ Mutation
  ├─ Crossover
  ├─ Repair
  └─ Kill
  ↓
Next Generation
```

## Concepts

| Type | Meaning |
|---|---|
| Intent | 何を作るべきかという目的・要求 |
| Reference | お手本となる画像・動画・形状・評価基準 |
| Method | 生成に使う方法・戦略 |
| MethodFamily | primitive、subdivision、procedural等の手法系統 |
| Genome | Methodを探索可能な遺伝子表現にしたもの |
| Candidate | あるMethod/Genomeから生成された候補 |
| Artifact | Blender/bpy等で実際に生成された成果物 |
| Evaluation | VLM/LMS/数値指標/人間による評価 |
| Criterion | 評価軸 |
| Score | 評価値 |
| Fitness | 複数評価を統合した生存適応度 |
| Failure | 生成・評価上の失敗 |
| Repair | 既存候補を改善する操作 |
| Mutation | Genomeの一部を変化させる操作 |
| Crossover | 複数Genomeを組み合わせる操作 |
| Selection | 次世代へ残す候補を選ぶ操作 |
| Elimination | 効果の低いMethodを淘汰する操作 |
| Elite | 現世代で特に優れた候補 |
| Generation | 同一探索世代の候補集合 |
| Population | 同時に探索する候補集合 |
| Diversity | 探索候補の多様性 |
| Stagnation | Fitnessが一定期間改善しない状態 |
| Restart | Method選択・探索空間からやり直す操作 |
| Complexity | コード量、構造、計算量等の複雑さ |
| Uncertainty | Score/Evaluationの不確実性 |
| History | Generation/Evaluation/Failure/Repairの蓄積 |
| Model | Historyから予測・ランキング等を学習するモデル |

## Evaluation ontology

評価は単一スコアに潰す前に、多軸で保存する。

```
Evaluation
├── intent_alignment
├── reference_similarity
├── geometry
├── proportion
├── material
├── camera
├── lighting
├── visual_quality
├── failure
├── complexity
└── runtime
```

VLM/LMSによる意味・視覚評価と、Blenderから取得できる数値的評価を分離して保持する。

## Fitness ontology

基本形：

```
fitness =
  similarity
  + intent_alignment
  - λ complexity
  - μ runtime
  - ν code_size
```

Fitnessは「似ているだけ」ではなく、

> **Intent/Referenceに近く、簡潔で、安く、再現可能なMethod**

を優先する。

多目的最適化ではPareto frontierを保持する。

## Method ontology

Methodはコードそのものではなく、生成戦略として扱う。

例：

```json
{
  "primitive": "sphere_cylinder",
  "proportion": "reference_ratio",
  "head": "subdivision",
  "eye": "boolean",
  "body": "primitive_union",
  "material": "simple",
  "camera": "reference_match",
  "lighting": "three_point"
}
```

これをGenomeとしてMutation/Crossover可能にする。

## Learning ontology

Historyから学ぶ対象：

- score prediction
- ranking
- failure prediction
- method selection
- repair strategy selection
- hyperparameter optimization
- uncertainty estimation
- active learning
- preference learning

### Statistical / ML toolbox

```
Statistics
├── descriptive statistics
├── regression
├── bootstrap
├── cross-validation
├── uncertainty
└── hypothesis testing

ML
├── linear/logistic regression
├── regularization
├── tree ensembles
├── boosting
├── ranking
├── classification
└── prediction

Optimization
├── random search
├── Bayesian optimization
├── evolutionary search
├── GA
├── NSGA-II
└── MAP-Elites
```

## Evolution ontology

### Selection

良い候補を残す。

### Mutation

既存Methodの一部を変える。

### Crossover

複数の良いMethodの構成要素を組み合わせる。

### Kill

Fitnessが低い、失敗率が高い、または複雑すぎるMethodを淘汰する。

### Diversity

最良候補だけを複製せず、異なるMethodFamilyを一定数残す。

### Restart

Stagnationを検出したら現在の局所探索を捨て、

```
Population
 ↓
Kill
 ↓
Method Search
 ↓
New Population
```

とする。

## State machine

```
SEARCH
  ↓
GENERATE
  ↓
RENDER
  ↓
EVALUATE
  ↓
LEARN
  ↓
SELECT
  ├── IMPROVE → MUTATE/CROSSOVER → GENERATE
  ├── REPAIR  → GENERATE
  ├── KILL    → SEARCH
  └── STAGNATE → RESTART → SEARCH
```

## Design principles

1. **Evaluation history is data.**
2. **Method is a first-class object.**
3. **Bad methods are knowledge too.**
4. **Repair is not the only action.**
5. **Selection precedes optimization.**
6. **Similarity alone is insufficient.**
7. **Complexity is a cost.**
8. **Diversity prevents premature convergence.**
9. **Stagnation permits a zero-based restart.**
10. **The system learns which methods should exist next.**

## Research hypothesis

> VLM/LMS評価と蓄積された履歴をFitnessとして利用すれば、bpyによる3D生成手法をGA/AutoML的に選択・淘汰・交叉・突然変異し、IntentとReferenceに近い一方で不要な複雑性の少ない生成Methodを自律的に探索できる。

## Relation to other layers

- `lms/`: 評価・推論
- `db/`: 評価履歴・実験知識
- `ml/`: 履歴からの学習・予測・選択・淘汰
- `sdk/`: 共通ループ
- `skills/`: 再利用可能な生成・評価・修復知識
- `mcp/`: Blender/bpy/VLM等の外部操作
- `crx/`: 人間による観察・介入
- `plan/`: 何を検証するか
- `papers/`: 既存研究

## Canonical distinction

**lms = judge**

**db = memory**

**ml = learn + select**

**ga = evolve**

**sdk = loop**

**mcp = act**

**skills = knowledge**

**plan = hypothesis**

**papers = evidence**
