# hw-sotsusei

**自給自足できる、VLM評価型アニメーション生成研究基盤。**

研究のゴールから逆算し、**MCP完全化 → 論文動画化 → ドラえもん進化ループ**の順で実装する。

## Goal

生成AIに「作らせる」だけではなく、

**生成 → 評価 → 蓄積 → 修正 → 再生成**

を繰り返し、目標に近づいていく過程そのものを研究対象にする。

最終成果物は **MP4**。  
Webアプリのデプロイを研究基盤の必須条件にはしない。

## 0. MCP完全化

まず、AIから研究・制作・評価環境を操作できる状態を作る。

ただし **MCPは本体ではない**。

- Skill = 知識・判断・手順
- 治具 = 再現可能な変換・生成・検証・評価
- Data = JSONL / DBとして残る事実と履歴
- MCP = 治具を外から操作する薄いAdapter
- AW / WF = 判断・オーケストレーション・決定的実行

原則：

> **MCPがなくてもCLI/治具だけで研究を継続できる。**

## 1. 論文をSF落語にして動画化

論文をそのまま説明するのではなく、研究の核心を抽出して、

**Paper → SF落語 → 4コマ → SVG → CSS Animation → MP4**

へ変換する。

評価対象：

- 論文の事実性
- 研究核心の伝達
- 脚本の分かりやすさ
- SFとしての面白さ
- 日本語文字の可読性
- VLMによる動画理解

問題があれば、

**VLM評価 → ラング三兄弟による批評・修正 → 再レンダリング**

を行う。

## 2. ドラえもん進化ループ

研究の本丸。

**Intent + Reference → Method → Generate → Render → VLM → Fitness → Selection → Mutation / Crossover / Repair → Next Generation**

生成・評価・修正履歴をDBへ蓄積し、世代を重ねる。

特に「ドラえもんらしさ」を、

- 自然言語
- コード
- ピクセル
- mm
- 角度
- 比率
- 構造
- 色・材質
- カメラ

など複数の表現で定義し、VLM評価と数値評価を組み合わせる。

最終的には、**最初の生成物から目標形へ近似していく成長アニメーション**として可視化する。

## 共通ループ

```text
Intent / Paper
      ↓
    Data
      ↓
    Skill
      ↓
   治具 / CLI
      ↓
  MCP Adapter
      ↓
    AW / WF
      ↓
 Artifact / MP4
      ↓
 Evaluation
      ↓
    Data
      ↺
```

### 疎結合の原則

各層は交換可能にする。

- 特定のLLM/VLMに依存しない
- 特定のレンダラに依存しない
- 特定のMCP実装に依存しない
- DataをUIやモデルから分離する
- 治具をCLIで直接実行できる
- MCPはAdapterとして差し替えられる
- ローカル実行とGitHub Actions実行を同じ入力・出力契約にする

## Renderer

用途に応じて併用する。

- **Pygame** — 2D / 4コマ / 軽量アニメーション
- **SVG / CSS** — 論文説明・ベクター表現
- **Blender / bpy** — 3D / カメラ / 空間表現
- **Godot** — 2D/3Dシーン・インタラクション

どのRendererを使っても最終インターフェースは **MP4**。

## Repository

| Directory | Role |
|---|---|
| `presen/` | 発表資料 |
| `papers/` | 論文調査・SF論文動画 |
| `plan/` | 研究計画・Kanban |
| `skills/` | 再利用可能な知識・制作規則 |
| `mcp/` | 外部ツール操作Adapter |
| `db/` | 実験・評価・生成履歴 |
| `lms/` | LLM/VLMによる評価・推論 |
| `ml/` | Fitness・予測・ランキング・学習 |
| `sdk/` | 共通ループ・データ契約 |
| `scripts/` | 自給自足用CLI・治具 |
| `crx/` | ブラウザ観測・UI |

## Research Loop

### Paper Loop

```text
Paper
 ↓
Research Skill
 ↓
SF落語
 ↓
SVG / CSS
 ↓
MP4
 ↓
VLM Evaluation
 ↓
Repair
 ↓
MP4
```

### Doraemon Loop

```text
Reference
 ↓
Method / Genome
 ↓
Generation
 ↓
Render
 ↓
VLM + Numeric Evaluation
 ↓
Fitness
 ↓
Selection
 ├─ Elite
 ├─ Mutation
 ├─ Crossover
 ├─ Repair
 └─ Kill
 ↓
Next Generation
 ↓
Growth Animation
```

## 自給自足の定義

この研究は、外部サービスが止まっても核心部分を再実行できることを目標とする。

1. Dataをローカルに保存できる
2. 治具をCLIから実行できる
3. MCPなしでも処理できる
4. 評価履歴をJSONL/DBに残せる
5. ローカルとCIで同じ処理を再現できる
6. MP4 Artifactを回収できる

**「自分で研究を回せる」ことが完成条件。**

## Status

- [x] 研究5段階構成
- [x] 論文データベース
- [x] SF論文4コマSVG
- [x] SVG → MP4決定的Renderer
- [x] Pygame / Blender / Godot併用方針
- [ ] MCP完全化
- [ ] Skill / 治具 / Data / MCPの境界整理
- [ ] VLM評価・修正ループ
- [ ] 論文SF落語の品質ループ
- [ ] ドラえもんDB
- [ ] Fitness / Selection / Evolution
- [ ] 成長アニメーション
- [ ] 自給自足型の一気通貫実験

## Principle

> **研究対象は生成物だけではない。  
> 生成方法・評価・失敗・修正・履歴そのものをデータとして蓄積し、次の生成方法を改善する。**

