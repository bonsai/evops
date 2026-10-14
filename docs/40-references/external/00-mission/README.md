# mission / 卒制試作プロジェクト

`hw-sotsusei` のミッション置き場。  
主に **有限会社カイカイキキ「ビジュアルクリエイター / AI画像生成エンジニア」** の求人を見据えた試作・学習計画をまとめる。

## 業務理解項目（5本立て）

本プロジェクトの核心となる5つの業務理解柱です。

### 0. 基本方針
> **回転ループをなるべく回す**ことを課題にする。  
> 自動化が課題だが、設計と評価は人間がやる。  
> テストも人間がやる。  
> しかし、教えれば機械もできる。  
> その試作をする。

- **人間がやる**: コンセプト設計、美的判断、評価基準の策定、テスト設計
- **機械に任せる（教えたあと）**: 反復生成、統計処理、可視化、ベクトル化・ナレッジ蓄積
- **最重要**: 限られたコストで、**なるべく多くの回転ループ**を回し、成果と満足度を最大化する

### 1. 主なチャレンジ
1. [回転ループを回し続ける設計](./cost-management.md)  
   token はフリーではない。bpy 書かせるのもお金がかかる。  
   **コストあたりの成果・満足度**を最大化する設計。

2. [画像生成パイプライン](./image-generation-blender-bpy.md)  
   Comfy モデルは管理が厳しい / Web API は key 管理が面倒 → **Blender + bpy + SVG** で試す。

3. [MCP/A2A + CPU 16GB 再設計](./mcp-a2a-redesign.md)  
   大規模 VLM は使えない。**MCP server + A2A Agent + 軽量モデル**で CPU 16GB 内で回す。

4. [インテント推定型評価エージェント](./intent-evaluation-agent.md)  
   自然言語のプロンプト調整ではなく、**人間が高得点をつけるインテント（意図）を推定**し、  
   評価基準を試行錯誤するエージェントを **LangChain / LangGraph / LangSmith** で設計する。

5. [データをとる行為](./data-collection-focus.md)  
   論文リサーチから、**何を・どう・なぜ測定するか**を設計する。

### 2. 画像生成パイプライン
Comfy モデルは管理が厳しい / Web API は key 管理が面倒 → **Blender + bpy + SVG** で試す。

### 3. MCP/A2A + CPU 16GB 再設計
大規模 VLM は使えない。**MCP server + A2A Agent + 軽量モデル**で CPU 16GB 内で回す。

### 4. インテント推定型評価エージェント
自然言語のプロンプト調整ではなく、**人間が高得点をつけるインテント（意図）を推定**し、評価基準を試行錯誤するエージェントを **LangChain / LangGraph / LangSmith** で設計する。

### 5. 直近のタスク
- [ ] 回転ループ 1 回あたりのコスト見積もり
- [x] MCP server 最小セット（blender-bpy, evaluator, db）の実装
- [ ] インテント推定型評価エージェントの最小設計
- [ ] 評価指標の選定（画像 / 小説 それぞれ）
- [ ] Blender bpy で SVG → 3D/レンダリングの最小パイプライン作成
- [ ] 生成履歴を保存する SQLite or ベクトル DB のスキーマ設計
- [ ] 評価ループの最小プロトタイプ（1 プロンプト → 生成 → 評価 → 再生成）
- [ ] Plotly での評価スコア時系列プロット

## ディレクトリ

```text
mission/
├── README.md                          # このファイル
├── automation-design-evaluation.md    # 自動化と人間領域の分離
├── cost-management.md                 # 回転ループのコスト管理
├── data-collection-focus.md           # データをとる行為の設計
├── image-generation-blender-bpy.md    # Blender/bpy/SVG 画像生成
├── mcp-a2a-redesign.md                # MCP/A2A + CPU 16GB 再設計
├── evaluation-loop.md                 # 評価ループと DB/ナレッジ化
├── intent-evaluation-agent.md         # インテント推定型評価エージェント
├── intent-evaluation-agent.html       # 上記の Mermaid 可視化
├── novel-evaluation.md                # 小説・文章の評価
├── ml-kaggle.md                       # 機械学習/Kaggle 計画
├── visualization.md                   # Plotly/PyVista 可視化
├── doraemon-vlm-correction.md         # ドラえもん VLM 修正ループ
├── doraemon-vlm-correction.html       # 上記の Mermaid 可視化
└── roadmap.md                         # 段階的アクションプラン
```
