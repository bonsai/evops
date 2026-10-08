# KPI — Research Success Metrics

## Primary KPI

### 1. Fitness Improvement
世代0から最終世代までFitnessが上昇すること。

目標: 有意な上昇傾向を確認する。

### 2. Similarity
Referenceとの視覚的類似度。

目標: 0.90以上を研究上の到達目標として検証する。0.90自体を真理とはせず、評価器の妥当性と人間評価との相関を確認する。

### 3. Intent Alignment
自然言語Intentと生成結果の一致度。世代進行に伴い上昇すること。

### 4. Evaluation Reliability
VLM/LMS評価と人間評価の一致度。定期的に人間評価で校正する。

### 5. Reproducibility
同一Input + 同一設定から同等のArtifactを再生成できる割合。目標: 100%を原則とする。

## Secondary KPI
- Generation数
- Candidate数
- Elite率
- Mutation率
- Repair率
- Kill率
- Runtime
- Code size
- VLM評価コスト
- MP4生成成功率
- 失敗Candidateの再利用率

## Paper Loop KPI
- 論文核心の伝達率
- 事実性
- 文字可読性
- SF落語としての理解度
- VLM評価→修正後の改善率

## Research Decision
KPIは「良い動画を作れたか」だけではなく、評価 → 学習/選択 → 再生成によって改善したかを測るために使う。
