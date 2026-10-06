# mission / 卒制試作プロジェクト

`hw-sotsusei` のミッション置き場。  
主に **有限会社カイカイキキ「ビジュアルクリエイター / AI画像生成エンジニア」** の求人を見据えた試作・学習計画をまとめる。

## 基本方針

> 自動化が課題だが、設計と評価は人間がやる。  
> テストも人間がやる。  
> しかし、教えれば機械もできる。  
> その試作をする。

- **人間がやる**: コンセプト設計、美的判断、評価基準の策定、テスト設計
- **機械に任せる（教えたあと）**: 反復生成、統計処理、可視化、ベクトル化・ナレッジ蓄積

## 主なチャレンジ

1. [画像生成パイプライン](./image-generation-blender-bpy.md)  
   Comfy モデルは管理が厳しい / Web API は key 管理が面倒 → **Blender + bpy + SVG** で試す。

2. [インテント推定型評価エージェント](./intent-evaluation-agent.md)  
   自然言語のプロンプト調整ではなく、**人間が高得点をつけるインテント（意図）を推定**し、  
   評価基準を試行錯誤するエージェントを **LangChain / LangGraph / LangSmith** で設計する。

3. [評価ループと統計データ](./evaluation-loop.md)  
   プロンプト・生成物・評価データをコンテキストに再生成を繰り返す。  
   先生案をベースに、自分は **DB / ナレッジベース** で永続化したい。

3. [小説の評価](./novel-evaluation.md)  
   画像だけでなく、物語・文章の評価基準も検討。

4. [機械学習・Kaggle](./ml-kaggle.md)  
   評価指標の学習や傾向抽出のために ML/Kaggle でスキルを磨く。

5. [統計データの可視化](./visualization.md)  
   Plotly / PyVista を使った生成履歴・評価値の可視化。

## ディレクトリ

```text
mission/
├── README.md                          # このファイル
├── automation-design-evaluation.md    # 自動化と人間領域の分離
├── image-generation-blender-bpy.md    # Blender/bpy/SVG 画像生成
├── evaluation-loop.md                 # 評価ループと DB/ナレッジ化
├── intent-evaluation-agent.md         # インテント推定型評価エージェント
├── novel-evaluation.md                # 小説・文章の評価
├── ml-kaggle.md                       # 機械学習/Kaggle 計画
├── visualization.md                   # Plotly/PyVista 可視化
└── roadmap.md                         # 段階的アクションプラン
```

## 直近のタスク

- [ ] インテント推定型評価エージェントの最小設計
- [ ] 評価指標の選定（画像 / 小説 それぞれ）
- [ ] Blender bpy で SVG → 3D/レンダリングの最小パイプライン作成
- [ ] 生成履歴を保存する SQLite or ベクトル DB のスキーマ設計
- [ ] 評価ループの最小プロトタイプ（1 プロンプト → 生成 → 評価 → 再生成）
- [ ] Plotly での評価スコア時系列プロット
