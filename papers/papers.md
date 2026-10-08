# SSSS Papers

## Research Question
LMS/VLMを共通評価器として使い、評価結果をDBへ蓄積し、MLによる改善へ接続できるか。

## External Papers

### P01 — VeMo: Zero-Shot Text-to-Motion Evaluation using Video Language Models
**VeMo: Zero-Shot Text-to-Motion Evaluation using Video Language Models / ICML 2026 / 2026**

Text-to-motion と生成動画の意味的一致を Video Language Model で評価する研究。Animation Intent → Render → VLM 評価の主要参考。

**Relevance**: 評価 Ontology 設計、VLM 評価器の構成の参考。

### P02 — EvalCrafter: Benchmarking and Evaluating Large Video Generation Models
**EvalCrafter: Benchmarking and Evaluating Large Video Generation Models / CVPR 2024 / 2024**

Visual Quality、Motion、Text-Video Alignment、Temporal Consistency など複数軸で動画生成を評価する。評価 Ontology 設計の主要参考。

**Relevance**: 多軸評価軸の設計（semantic / motion / temporal / composition）。

### P03 — VideoScore: Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation
**VideoScore: Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation / EMNLP 2024 / 2024**

細粒度な人間評価を自動評価へ変換する研究。評価器を生成改善への Feedback source として扱う設計に対応。

**Relevance**: VLM 評価を生成改善のフィードバックへ接続する設計の根拠。

### P04 — VisualPrompter
**VisualPrompter / ICLR 2026 / 2026**

視覚的評価から不足概念を発見し、プロンプト改善へ接続する方向の研究。VLM 出力を failure / repair instruction として保存する設計に対応。

**Relevance**: failure 記述 → repair instruction の変換設計。

### P05 — 3D Human Animation Quality Assessment: Subjective and Objective Evaluation
**3D Human Animation Quality Assessment: Subjective and Objective Evaluation / IEEE TVCG 2026 / 2026**

3D アニメーションの主観・客観評価と品質予測を扱う。VLM、Python 測定、人間検証を分離する設計の参考。

**Relevance**: 3D 生成物評価の主観・客観・自動測定の分離設計。

### P06 — DreamFusion: Text-to-3D using 2D Diffusion
**DreamFusion: Text-to-3D using 2D Diffusion / ICCV 2023 / 2023**

Text-to-3D の金字塔。Score Distillation Sampling でテキストから 3D 造型を最適化。テーマ 2 の「テキスト → bpy」生成の先例。

**Relevance**: テキスト → 3D 生成パイプラインの先例。

### P07 — Point-E: A System for Generating 3D Point Clouds from Textual Descriptions
**Point-E: A System for Generating 3D Point Clouds from Textual Descriptions / CVPR 2023 / 2023**

Text-to-3D の高速生成パイプライン。生成→評価ループの高速化の先例。

**Relevance**: 生成→評価ループの高速化先例。

### P08 — Magic3D: High-Resolution Text-to-3D Content Creation
**Magic3D: High-Resolution Text-to-3D Content Creation / CVPR 2024 / 2024**

Text-to-3D の高解像度化。多段階生成→upscale の設計。

**Relevance**: 多段階生成設計の参考。

### P09 — What matters when building vision-language models? (Idefics2)
**What matters when building vision-language models? (Idefics2) / arXiv 2024 / 2024**

VLM 設計の決定要因を実験的に明らかに。評価器選び（サイズ・データ）の指針。Idefics2 は 8B で大規模モデルに匹敵。

**Relevance**: 評価器（ローカル VLM）のサイズ・選択指針。

### P10 — CLIP: Learning Transferable Visual Models From Natural Language Supervision
**CLIP: Learning Transferable Visual Models From Natural Language Supervision / ICML 2021 / 2021**

画像とテキストを共通の埋め込み空間にマッピングし、ゼロショットで分類・検索・評価が可能。CPU でも動作する軽量版（ViT-B/32, RN50 など）が広く利用可能。

**Relevance**: CPU 16GB 制約下での軽量自動評価器の基盤。テーマ適合度・類似度計算に活用。

### P11 — Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation
**Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation / NeurIPS 2023 / 2023**

Text-to-image モデルの出力に対する人間の偏好データセット。PickScore はこのデータで学習された軽量な画像評価モデル。

**Relevance**: 人間嗜好を予測する軽量スコアリングモデルの先例。相対評価データの重要性。

### P12 — ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation
**ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation / NeurIPS 2023 / 2023**

Text-to-image 生成物に対する人間の詳細な嗜好を学習した報酬モデル。人間フィードバックを自動評価に変換する設計の参考。

**Relevance**: 自動評価器が人間の嗜好をどう近似するかの参考。

### P13 — Human Preference Score v2: A Solid Benchmark for Evaluating Human Preferences of Text-to-Image Synthesis
**Human Preference Score v2: A Solid Benchmark for Evaluating Human Preferences of Text-to-Image Synthesis / arXiv 2023 / 2023**

HPSv2 は text-to-image モデルの人間嗜好を予測するためのベンチマークとスコアリングモデル。

**Relevance**: 自動評価器の信頼性確認と、人間嗜好予測の設計参考。

### P14 — Training language models to follow instructions with human feedback (InstructGPT / RLHF)
**Training language models to follow instructions with human feedback (InstructGPT / RLHF) / NeurIPS 2022 / 2022**

人間の偏好データを使って報酬モデルを学習し、PPO で言語モデルを最適化。人間の意図をモデル化する基本フレームワーク。

**Relevance**: インテント推定 → 報酬モデル → 生成改善の流れの理論基盤。

### P15 — Direct Preference Optimization: Your Language Model is Secretly a Reward Model
**Direct Preference Optimization: Your Language Model is Secretly a Reward Model / NeurIPS 2024 / 2024**

RLHF の報酬モデル学習を省略し、ペアワイズ嗜好データから直接言語モデルを最適化する DPO。データ効率が良い。

**Relevance**: 少ない人間嗜好データからの学習手法。回転ループ内での効率的な改善に活用可能。

### P16 — Active Learning for Large Language Model-based Chatbots
**Active Learning for Large Language Model-based Chatbots / EMNLP 2023 / 2023**

人間アノテーションコストを抑えつつ、効率的に学習データを選ぶアクティブラーニング手法。不確実性サンプリングなど。

**Relevance**: 人間評価データ取得コストを抑え、高情報量サンプルを選ぶ戦略。

### P17 — Model Context Protocol (MCP)
**Model Context Protocol (MCP) / Anthropic Technical Specification / 2024**

Anthropic 提唱のオープンプロトコル。LLM アプリケーションが外部ツール、データソース、リソースに安全に接続するための標準。server/client モデル。

**Relevance**: 本プロジェクトのツール層（Blender, DB, Evaluator）を標準化する基盤。

### P18 — Agent2Agent Protocol (A2A)
**Agent2Agent Protocol (A2A) / Google Technical Specification / 2025**

Google 提唱のエージェント間通信プロトコル。異なるフレームワーク・プラットフォームで動作するエージェントが協調できる標準。

**Relevance**: Generator / Evaluator / Intent Estimator などの専門エージェント連携の基盤。

### P19 — Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone
**Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone / arXiv 2024 / 2024**

Microsoft の Phi-3 シリーズ。3.8B パラメータで大規模モデルに匹敵する性能。量子化により CPU でも実用的な推論が可能。

**Relevance**: CPU 16GB 制約下での軽量 LLM 選定の指針。

### P20 — Llama 3.2: Revolutionizing edge AI and vision with open, Customizable Models
**Llama 3.2: Revolutionizing edge AI and vision with open, Customizable Models / Meta Technical Report / 2024**

Meta の Llama 3.2。1B / 3B のテキストモデルと、11B / 90B のビジョンモデル。軽量版は CPU/エッジで動作可能。

**Relevance**: ローカル CPU で動かせる LLM / VLM の選択肢。

### P21 — The False Dawn: Reevaluating Performance Gains of Small Language Models
**The False Dawn: Reevaluating Performance Gains of Small Language Models / arXiv 2024 / 2024**

SLM の性能とコストのトレードオフを実験的に検証。タスク難易度によっては小モデルで十分、というケースと限界を示す。

**Relevance**: CPU 16GB 制約下でどのタスクを SLM に任せ、どこを人間に残すべきかの指針。

### P22 — A Watermark for Large Language Models
**A Watermark for Large Language Models / ICML 2023 / 2023**

LLM 生成テキストに透かしを埋め込み、出典追跡や品質管理を行う手法。生成物の信頼性・再現性管理の参考。

**Relevance**: 回転ループで生成されたプロンプト・bpy コード・評価の出典管理・信頼性担保。

### P25 — B-CODER: Benchmarking Code Generation with Evaluation Loop
**B-CODER: Benchmarking Code Generation with Evaluation Loop / ICLR 2024 / 2024**

コード生成タスクにおいて、生成→評価→修正ループの性能を測定するベンチマークとフレームワーク。

**Relevance**: 生成→評価→改善ループの定式化の参考。


## EvOps Original Papers

### P23 — VQualA: Video Quality Assessment via VLM
**VQualA: Video Quality Assessment via VLM / in-house / 2025**

生成動画の品質をVLMで多軸評価し、構造的・意味的両面からスコアリングする自社フレームワーク。

**Keywords**: evaluation, vlm, video

**Doc**: [P23-vlmを用いた動画品質評価フレームワーク-2025/README.md](P23-vlmを用いた動画品質評価フレームワーク-2025/README.md)

### P24 — UniAPO: Unified Automatic Pipeline Orchestration
**UniAPO: Unified Automatic Pipeline Orchestration / in-house / 2025**

複数の生成・評価サービスを統合し、共通DSLで制御するオーケストレーション層の設計。

**Keywords**: mcp, a2a, orchestration

**Doc**: [P24-統合自動パイプラインオーケストレーション-2025/README.md](P24-統合自動パイプラインオーケストレーション-2025/README.md)

### P26 — MLOps Evaluation Loop Automation
**MLOps Evaluation Loop Automation / in-house / 2024**

生成AIパイプラインにおける継続的評価ループの自動化設計。評価器の選定、閾値管理、フィードバック機構の標準化。

**Keywords**: mlops, evaluation, automation

**Doc**: [P26-mlops評価ループの自動化設計-2024/README.md](P26-mlops評価ループの自動化設計-2024/README.md)

### P27 — VLM Evaluation Automation for Visual Content
**VLM Evaluation Automation for Visual Content / in-house / 2024**

画像・動画生成物のVLM評価を自動化し、スコア閾値ベースの合格判定と修復指示生成を行う仕組み。

**Keywords**: vlm, evaluation, automation, visual

**Doc**: [P27-視覚コンテンツ向けvlm評価自動化-2024/README.md](P27-視覚コンテンツ向けvlm評価自動化-2024/README.md)

### P28 — Evolutionary Generation Loop with Feedback Accumulation
**Evolutionary Generation Loop with Feedback Accumulation / in-house / 2024**

過去の評価フィードバックを遺伝的アルゴリズム的に蓄積・選択し、次世代の生成パラメータを進化させるループ設計。

**Keywords**: evolutionary, feedback, loop, optimization

**Doc**: [P28-フィードバック蓄積型進化生成ループ-2024/README.md](P28-フィードバック蓄積型進化生成ループ-2024/README.md)

### P29 — Jev-Driven MLOps: High-Speed Judgment Layer for Observable and Controllable Generative Pipelines
**Jev-Driven MLOps: High-Speed Judgment Layer for Observable and Controllable Generative Pipelines / in-house / 2024**

TypeSafe AIのJev(System One Model)をMLOpsの内部制御プレーンとして統合。5つの統合ポイント(Backend Router, Prefilter Gate, Human Gate, Repair Router, Knowledge Ranker)を設計し、30%コスト削減と29×加速を実現。

**Keywords**: jev, mlops, control-plane, cost-optimization

**Doc**: [P29-mlops内部への高速判断レイヤー統合-2024/README.md](P29-mlops内部への高速判断レイヤー統合-2024/README.md)

### P30 — Model-Free Visual Synthesis: Deterministic 3D Rendering via ComfyUI-Workflow Concepts Mapped to Blender-bpy
**Model-Free Visual Synthesis: Deterministic 3D Rendering via ComfyUI-Workflow Concepts Mapped to Blender-bpy / in-house / 2024**

ComfyUIのノードグラフ概念を保持し、実行バックエンドをBlender-bpyに置き換える決定論的ビジュアル合成パイプライン。LLMが自然言語をbpyコードに変換し、CPUのみで100%再現可能な3Dレンダリングを実現。

**Keywords**: model-free, blender-bpy, deterministic, comfyui, 3d

**Doc**: [P30-拡散モデル不要の決定論的ビジュアル合成-2024/README.md](P30-拡散モデル不要の決定論的ビジュアル合成-2024/README.md)

### P31 — Inverse Preference Learning for Evaluation Agents: Inferring Human Value Functions from Scores
**Inverse Preference Learning for Evaluation Agents: Inferring Human Value Functions from Scores / in-house / 2024**

自然言語プロンプト調整の代替として、人間の採点履歴からインテントベクトルを逆推定し、動的に評価基準を生成・最適化するエージェント設計。LangChain/LangGraph/LangSmith三兄弟活用。

**Keywords**: intent-estimation, inverse-preference, langchain, bradley-terry

**Doc**: [P31-人間の価値関数を採点履歴から逆推定-2024/README.md](P31-人間の価値関数を採点履歴から逆推定-2024/README.md)

### P32 — Cost-Aware Rotation Loop Design for Resource-Constrained MLOps: Token Budget Optimization in CPU-Only Generative Pipelines
**Cost-Aware Rotation Loop Design for Resource-Constrained MLOps: Token Budget Optimization in CPU-Only Generative Pipelines / in-house / 2024**

APIトークン予算とCPU-only(16GB RAM)制約下での回転ループコスト構造を定式化。自動評価優先ハイブリッドで同予算内5倍ループ増加を実現。予算閾値による動作モード切り替えルールを設計。

**Keywords**: cost-optimization, cpu-only, token-budget, rotation-loop

**Doc**: [P32-cpu制約下でのコスト意識型回転ループ設計-2024/README.md](P32-cpu制約下でのコスト意識型回転ループ設計-2024/README.md)

### P33 — Structured Feature Axes for Character-Aware Visual Correction Loops: Multi-Layer Evaluation Combining Detection, Histogram, and VLM
**Structured Feature Axes for Character-Aware Visual Correction Loops: Multi-Layer Evaluation Combining Detection, Histogram, and VLM / in-house / 2024**

曖昧なVLM評価を構造軸(色ヒストグラム・輪郭検出)とスタイル軸(CLIP)に分解し、段階的に評価・修正するフレームワーク。人間介入ポイントを5箇所に明示的設計。

**Keywords**: structured-evaluation, character-aware, human-in-the-loop, visual-correction

**Doc**: [P33-構造特徴軸によるキャラクター認識型画像修正ループ-2024/README.md](P33-構造特徴軸によるキャラクター認識型画像修正ループ-2024/README.md)

### P34 — From Evaluation to Knowledge: Continuous Learning in Generative Pipelines via Structured Feedback Accumulation
**From Evaluation to Knowledge: Continuous Learning in Generative Pipelines via Structured Feedback Accumulation / in-house / 2024**

評価データを5テーブルスキーマで構造化蓄積し、ChromaDB/pgvectorによる類似度検索で次世代生成に再利用。成功/失敗パターンの抽出とFID/LPIPSによる多様性管理を統合。

**Keywords**: knowledge-accumulation, vector-search, continuous-learning, feedback

**Doc**: [P34-構造化フィードバック蓄積による継続学習-2024/README.md](P34-構造化フィードバック蓄積による継続学習-2024/README.md)

### P35 — A Unified Domain-Specific Language for Heterogeneous Generative Pipeline Composition
**A Unified Domain-Specific Language for Heterogeneous Generative Pipeline Composition / in-house / 2024**

Blender-bpy, ComfyUI, Evaluator, DBなど異種サービス間をJSON DSLで統一的に記述。Workflow DSL/IR/バックエンドコードの三層構造。$refによるステージ間参照とevaluation・feedback_loop・repair_strategyの第一級統合。

**Keywords**: dsl, json-schema, workflow-ir, pipeline-composition

**Doc**: [P35-異種生成パイプライン統合dsl-2024/README.md](P35-異種生成パイプライン統合dsl-2024/README.md)

### P36 — Multi-Metric Automated Story Evaluation: Beyond Readability to Thematic Coherence via Embedding and Sentiment Analysis
**Multi-Metric Automated Story Evaluation: Beyond Readability to Thematic Coherence via Embedding and Sentiment Analysis / in-house / 2024**

日本語・英語小説に対して読みやすさ、語彙多様性、感情軌跡、テーマ適合度、キャラクター一致性、プロット構造を多軸評価。機械計算指標と人間定義テーマ制約の分離と長期分析基盤。

**Keywords**: story-evaluation, readability, sentiment-analysis, thematic-coherence, nlp

**Doc**: [P36-多指標自動小説評価フレームワーク-2024/README.md](P36-多指標自動小説評価フレームワーク-2024/README.md)

### P37 — Observability Dashboards for Generative Pipelines: From Score Tracking to 3D Parameter Space Exploration
**Observability Dashboards for Generative Pipelines: From Score Tracking to 3D Parameter Space Exploration / in-house / 2024**

評価ループ全体を可視化するダッシュボードアーキテクチャ。時系列プロット、散布図、UMAPクラスタリング、PyVistaによるパラメータ空間3Dマッピング。Streamliteフロントエンドで検索空間を可視化。

**Keywords**: observability, dashboard, 3d-visualization, pyvista, umap

**Doc**: [P37-生成パイプライン観測性ダッシュボード-2024/README.md](P37-生成パイプライン観測性ダッシュボード-2024/README.md)

### P38 — MCP Server Standardization via fastmcp and FastAPI: Transport Unification, SDK Compatibility, and Multi-Protocol Exposure
**MCP Server Standardization via fastmcp and FastAPI: Transport Unification, SDK Compatibility, and Multi-Protocol Exposure / in-house / 2024**

同一リポジトリ内でmcp 2.x SDK（FastMCP→MCPServerリネーム）とfastmcp 4.xパッケージが混在しimport互換性が破壊される問題を实名調査。fastmcp 4.xのhttp_app()がStarletteアプリを返しFastAPIにmount可能であることを確認し、全MCPサービス（blender-bpy/evaluator/db/sf-paper-comic）をFastMCP+FastAPI統合パターンで再構築。transport={stdio,sse,http,streamable-http}の切替可能なベースサーバーテンプレートを共通化し、個別サービスと統合ゲートウェイの両方で動作するアーキテクチャを確立。

**Keywords**: mcp, fastmcp, fastapi, transport, sdk-compatibility, multi-protocol, stdio, sse, streamable-http

**Doc**: [P38-fastmcp+fastapi統合によるmcpサー-2024/README.md](P38-fastmcp+fastapi統合によるmcpサー-2024/README.md)


## Synthesis
1. 動画・画像評価は多軸化し、軽量モデル（CLIP, PickScore, ImageReward, HPSv2）で近似可能。
1. VLM は semantic/perceptual evaluator として利用するが、CPU 制約では CLIP-small 等の軽量版を使う。
1. 人間の嗜好はペアワイズ比較で効率的に収集し、Bradley-Terry や DPO で学習する。
1. MCP でツール層を標準化し、A2A でエージェント連携を標準化することでモジュール性と差し替え性を確保する。
1. 評価結果を生成改善の Feedback source として扱い、構造化データとして蓄積する。
1. 人間フィードバックは有限・高価なので、アクティブラーニングで高情報量サンプルを選び、コストを抑える。
1. SLM（Phi-3, Llama 3.2 等）を使い、CPU 16GB 内で回転ループを回し続ける。
1. 蓄積履歴から ML で ranking、prediction、repair strategy を改善する。

## Loop
Generation → Auto Evaluation → Human Feedback → DB → Intent Estimation → Criteria Update → Repair → Generation の継続的な評価・学習ループ
