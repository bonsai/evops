# データをとる行為：課題感と設計

## 背景：なぜ「データをとる行為」にフォーカスするか

これまでの議論は、**どう自動化するか**や**どう評価するか**に注力しがちだった。  
しかし、論文リサーチから分かるように、生成・評価・改善のループを回すための根幹は、
**何を、どう、なぜ測定し、蓄積するか**という「データをとる行為」にある。

> データを取らなければ、評価も学習も改善も始まらない。  
> データの質と構造が、最終的な自動化の天井を決める。

## 課題感

### 1. 「良い」とは何かが定義されていない

- 人間の美的判断は文脈依存で、言語化されていない部分が大きい。
- したがって、**「良さ」をデータとして捕捉する設計**が必要。

### 2. 生成物は無限に作れるが、評価データは有限

- 画像・文章・3D は安価に量産できる。
- 一方、人間の評価は時間と労力がかかる。
- **少ない評価データから多くを学ぶ設計**が鍵。

### 3. 評価基準と生成戦略が分断されている

- 多くの場合、生成と評価が別々に最適化される。
- 評価データは生成改善に使われず、生成パラメータは評価結果を無視しがち。
- **データが双方向に流れる構造**が必要。

### 4. 履歴が失われる

- 試行錯誤の過程（プロンプト、生成物、スコア、コメント）が散逸する。
- 失敗がナレッジにならない。
- **構造化された履歴蓄積**が必要。

## 論文リサーチから得られた知見

[papers/](../papers/papers.md) の調査結果を基に、以下が可能だと分かった。

| 論文 | データをとる行為への示唆 |
|------|------------------------|
| **VeMo** | Animation Intent → Render → VLM 評価。意図と生成物の対応をデータ化できる。 |
| **EvalCrafter** | Visual Quality / Motion / Text-Video Alignment / Temporal Consistency など**多軸評価**の Ontology を設計できる。 |
| **VideoScore** | 細粒度な人間フィードバックを自動評価に変換。**人間データをスケール可能な指標**に変換できる。 |
| **VisualPrompter** | VLM 出力を failure / repair instruction として保存。**失敗の言語化データ**が次の生成に使える。 |
| **3D Human Animation QA** | 主観評価・客観測定・自動評価を**分離して蓄積**する設計が可能。 |
| **DreamFusion / Point-E / Magic3D** | テキスト → 3D の生成パイプライン。生成パラメータと結果をセットで記録できる。 |
| **Idefics2** | VLM の設計要因。評価器選びの根拠データを残せる。 |

###  synthesis

1. 評価は**多軸**で行う。
2. VLM / LMS を**共通評価器**として使う。
3. 評価結果を**生成改善の feedback source** にする。
4. 履歴を**構造化データ**として蓄積する。
5. 蓄積データから **ML で ranking / prediction / repair** を改善する。

## 「データをとる行為」の設計

### 何を取るか（What）

| データ種別 | 内容 | 用途 |
|-----------|------|------|
| **意図データ** | 人間が作りたいものの言語化、参照画像、テーマ | 生成の北極星、インテント推定の入力 |
| **プロンプト・パラメータデータ** | プロンプト、SVG パラメータ、Blender 設定 | 再現性、生成空間の探索 |
| **生成物データ** | 画像、文章、3D レンダリング、メタデータ | 評価対象、特徴量抽出の入力 |
| **自動評価データ** | VLM/LMS スコア、画像指標、文章指標 | 大規模探索、候補絞り込み |
| **人間評価データ** | 総合スコア、軸別スコア、コメント、A/B 選択 | 正解ラベル、インテント学習 |
| **改善指示データ** | failure 記述、repair instruction、次のパラメータ案 | 次の生成に反映 |
| **メタデータ** | 日時、モデル、ツール、バージョン、実験ID | 再現性、実験管理 |

### どう取るか（How）

#### 1. 実験単位でデータを設計する

```text
Experiment
├── intent           # 人間の意図
├── parameters       # 生成パラメータ
├── generated_items  # 生成物
├── auto_evaluations # 自動評価
├── human_evaluations # 人間評価
└── feedback         # 改善指示
```

#### 2. 評価軸を多軸化する（EvalCrafter 方式）

- 総合スコアだけでなく、軸別スコアを取る。
- 例（画像）: 構図、色彩、一貫性、テーマ適合度、独創性、技術品質
- 例（文章）: テーマ適合、読みやすさ、語彙多様性、感情トーン、構造

#### 3. 相対評価で密度を上げる

- 絶対スコアではなく「A と B どちらが良いか」を繰り返す。
- ペアワイズ比較データから、人間の順位好みを推定する。
- 同じ時間でより多くの情報を得られる。

#### 4. 失敗を積極的に記録する

- 低得点作品こそ情報量が多い。
- なぜ低得点かを言語化し、repair instruction として保存する（VisualPrompter 方式）。

#### 5. 自動評価と人間評価をペアで取る

- 同じ生成物に対し、自動評価と人間評価を両方記録。
- 両者の相関を常に計算し、自動評価の信頼性を監視する。

### なぜ取るか（Why）

| 目的 | 必要なデータ | 活用先 |
|------|------------|--------|
| 再現性 | パラメータ + 生成物 | 同じ結果を再生成 |
| インテント推定 | 人間評価 + コメント | 人間の価値関数を学習 |
| 自動評価の学習 | 自動指標 + 人間スコア | 人間予測モデル |
| 生成改善 | failure + repair | 次のプロンプト / パラメータ |
| 傾向分析 | 時系列スコア | 改善軌跡の可視化 |
| ナレッジ蓄積 | 全履歴 | 類似タスクへの転用 |

## データ収集のプロトコル

### Phase 1: 探索的データ収集

```text
1. 多様なパラメータで生成
2. 人間がざっくり採点 + コメント
3. 自動評価も実行
4. すべてを DB に保存
```

- 目的：広くサンプルを取り、どの属性が重要かを把握する。

### Phase 2: インテント推定

```text
1. 探索データから人間の好みパターンを分析
2. インテントベクトルを推定
3. 重要そうな評価軸を仮説として設定
```

### Phase 3: 集中的データ収集

```text
1. 推定されたインテント周辺で生成
2. 軸別スコア + 相対評価で高密度に採点
3. 自動評価と人間評価の差分を分析
4. 差分が大きいものは特に記録（失敗学習）
```

### Phase 4: 自動化の学習

```text
1. 人間評価を正解ラベルとして ML モデル学習
2. 自動評価の重みを最適化
3. 人間介入が少ない高速探索ループを構築
```

## DB スキーマ案（データをとるための構造）

```sql
-- 実験単位
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    task_context TEXT,       -- 画像 / 小説 / 3D など
    intent_text TEXT,        -- 人間の意図言語化
    created_at TIMESTAMP
);

-- 生成パラメータ
CREATE TABLE parameters (
    id INTEGER PRIMARY KEY,
    experiment_id INTEGER,
    param_json TEXT,         -- 全パラメータを JSON で
    prompt_text TEXT,
    tool_version TEXT
);

-- 生成物
CREATE TABLE generated_items (
    id INTEGER PRIMARY KEY,
    parameter_id INTEGER,
    file_path TEXT,
    item_type TEXT,          -- image / text / 3d
    created_at TIMESTAMP
);

-- 自動評価
CREATE TABLE auto_evaluations (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    evaluator_name TEXT,     -- clip / vlm / custom
    axis_name TEXT,
    score REAL,
    raw_output TEXT,
    evaluated_at TIMESTAMP
);

-- 人間評価
CREATE TABLE human_evaluations (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    overall_score INTEGER,   -- 1-5
    axis_scores TEXT,        -- JSON
    comment TEXT,
    evaluator_id TEXT,       -- 自分 or 第三者
    evaluated_at TIMESTAMP
);

-- 相対評価
CREATE TABLE pairwise_comparisons (
    id INTEGER PRIMARY KEY,
    item_a_id INTEGER,
    item_b_id INTEGER,
    winner_id INTEGER,       -- a / b / tie
    reason TEXT,
    evaluated_at TIMESTAMP
);

-- 改善フィードバック
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    failure_description TEXT,
    repair_instruction TEXT,
    next_parameters TEXT     -- JSON
);
```

## ツール連携

```text
[生成] → [自動評価] → [人間評価 UI] → [DB 保存]
   ↑                                          ↓
   └──────── [改善指示] ← [傾向分析・可視化] ←┘
```

- **生成**: Blender bpy, SVG generator
- **自動評価**: CLIP, DINOv2, VLM, 文章指標
- **人間評価 UI**: Streamlit / Gradio / TUI
- **蓄積**: SQLite / PostgreSQL + pgvector
- **可視化**: Plotly, PyVista
- **学習**: scikit-learn, LightGBM, PyTorch

## 次のアクション

- [ ] 最小データ収集プロトコルを定義
- [ ] 上記 DB スキーマの実装
- [ ] 人間評価用 UI の作成
- [ ] 画像 10 枚 + 小説 3 篇で試行的データ収集
- [ ] 自動評価と人間評価の相関を計算
- [ ] 失敗パターンを 3 件言語化

## 関連ファイル

- [intent-evaluation-agent.md](./intent-evaluation-agent.md): インテント推定エージェント
- [evaluation-loop.md](./evaluation-loop.md): 評価ループ全体
- [visualization.md](./visualization.md): 収集データの可視化
- [ml-kaggle.md](./ml-kaggle.md): 収集データの ML 活用
- [../papers/papers.md](../papers/papers.md): 論文リサーチ
