# Design & Intent Retrospective

**文書種別**: 設計振り返り / Design Retrospective  
**対象期間**: 2026-10-11 〜 2026-10-13  
**記録日**: 2026-10-13  

---

## Executive Summary（設計の核心）

本システム（evops）は**「専門論文を誰にでも伝わる物語へ変換する」**という企画意図を支えるために、以下の3本柱で設計された。

1. **疎結合（Loose Coupling）**: 各コンポーネントはJSON spec + CLI呼び出しのみで連携。直接importしない
2. **段階的品質制御（Graduated Gates）**: Wide Gate（ゆるい）で量産 → Narrow Gate（厳格）で絞り込む
3. **形態非依存の中間表現（Universal Digestion）**: 論文→「咀嚼済み構造」→任意出力（漫画/動画/漫才/記事）

これらは全て「**知識の民主化**」という一つの企画意図から導出されている。

---

## 1. 企画意図 → 設計原則の導出関係

```
┌──────────────────────────────────────────────────────────────┐
│                    企画意図（Why）                            │
│    「論文の知見を、専門外の人にも伝わる形に変換したい」        │
└──────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    ▼                         ▼                         ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ 多様な出力形態 │       │ 品質の自律向上 │       │ 日本語教育文化 │
│ を生む仕組み  │       │ によるスケール │       │ への親和性   │
└─────────────┘       └─────────────┘       └─────────────┘
    │                         │                         │
    ▼                         ▼                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    設計原則（How）                            │
│  • Universal Digestion（中間表現）                            │
│  • Domain Adapter（後付け変換）                               │
│  • Eval Loop（評価→改善→再評価）                             │
│  • Wide Gate（量産優先の初期基準）                            │
│  • ASS字幕 / IPAexフォント / Voicevox（ななちゃん）           │
└──────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    ▼                         ▼                         ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ 9台のMCP    │       │ paper_id    │       │ chaperone   │
│ サーバー群  │       │ 命名規則    │       │ workflow    │
│（疎結合）   │       │（追跡性）   │       │（自動化）   │
└─────────────┘       └─────────────┘       └─────────────┘
```

### 導出の論理

| 企画意図 | 設計原則 | 理由 |
|----------|----------|------|
| 論文1本から漫画も動画も作りたい | **Universal Digestion + Adapter** | 直接変換ではなく中間表現を挟むことで、出力形態を後から追加できる |
| 専門外にも届く | **Metaphor層** | 高校生レベルの比喩に翻訳する専用レイヤーを設ける |
| 大量の論文を処理したい | **Wide Gate + Eval Loop** | 人力レビューを挟まず、システムが自律的に品質を収束させる |
| 日本語の教育コンテンツとして使いたい | **ASS字幕 + IPAex + Voicevox** | 日本語圏の教育文化（テロップ、漫画的表現）に寄り添う技術選定 |
| チームで開発・拡張したい | **Loose Coupling + MCP Thin Adapter** | 各コンポーネントが独立して進化可能 |

---

## 2. システム設計の3本柱

### 2.1 疎結合アーキテクチャ（Loose Coupling）

#### 設計意図
> **「各コンポーネントは独立して動作し、相互にimportしない」**

これは「チーム開発」「外部贡献」「長期メンテナンス」という未来を見据えた設計。MCPが新興規格で不安定（fastmcp 4.x の互換性崩壊が実際に発生）だったため、CLIファーストを貫く判断が下された。

#### インターフェース設計

```
┌──────────────────────────────────────────────────────┐
│  Paper Digest MCP (8008)                             │
│  Input:  text/title                                  │
│  Output: DigestedPaper JSON                          │
│  Interface: HTTP POST /call OR stdio                 │
└──────────────────────────────────────────────────────┘
                         │
                         ▼ DigestedPaper JSON
┌──────────────────────────────────────────────────────┐
│  Storyboard MCP (8009)                               │
│  Input:  episode.json                                │
│  Output: CutPlan + Timeline JSON                     │
│  Interface: HTTP POST /call OR stdio                 │
└──────────────────────────────────────────────────────┘
                         │
                         ▼ CutPlan JSON
┌──────────────────────────────────────────────────────┐
│  SF-Paper-Comic (8004) / bpy-gen (8005)             │
│  Input:  panel spec                                  │
│  Output: S01_panel_01.svg                            │
│  Interface: CLI: python3 svg-gen.py --episode ...    │
└──────────────────────────────────────────────────────┘
                         │
                         ▼ PNG sequence
┌──────────────────────────────────────────────────────┐
│  Videogen MCP (8006)                                 │
│  Input:  image list + audio + subtitle               │
│  Output: final.mp4                                   │
│  Interface: HTTP POST /call OR ffmpeg CLI            │
└──────────────────────────────────────────────────────┘
```

#### ADR: MCP as Thin Adapter
- **決定**: CLIファースト。HTTP/MCPはoptionalなwrapper
- **根拠**: CLIは10年後も動く。MCPはまだ規格が揺らいでいる
- **実装**: 全スキルが `--http` と `--stdio` の両モードをサポート

### 2.2 段階的品質制御（Graduated Quality Gates）

#### 設計意図
> **「完成状況はゆるくていい。まず回して、後から厳しくする」**

これはユーザーの核心思想であり、設計に深く浸透している。

#### Gate スキーマ

| 項目 | Wide Gate（初期・デフォルト） | Narrow Gate（品質絞り込み時） |
|------|---------------------------|---------------------------|
| 合格点 | 50/100 | 75/100 |
| A判定 | 80点以上 | 95点以上 |
| B判定 | 65点以上 | 85点以上 |
| 字幕網羅率 | 50%以上 | 90%以上 |
| 輝度範囲 | 0.15 〜 0.95 | 0.35 〜 0.75 |
| 用途 | 量産・テスト・PoC | 公開・商用・教育配信 |

#### Eval Loop 設計

```
┌─────────────────────────────────────────────────────────────┐
│                        Eval Loop                             │
│                                                              │
│   生成物 ──→ review_paper_anime() ──→ Score + Grade        │
│      ↑                                    │                  │
│      │                                    ▼                  │
│      └──── suggest_improvements() ←──── Fail または Target   │
│                   │                                         │
│                   ▼                                         │
│            ┌──────────────┐                                │
│            │ Action決定   │                                │
│            │ • regenerate │ ──→ 外部スクリプト呼び出し      │
│            │ • adjust     │                                │
│            │ • skip       │ ──→ 次のイテレーション          │
│            └──────────────┘                                │
│                   │                                         │
│                   └───────────────────────────────────────→ │
│                                                              │
│   Parameters: max_iterations=3, target_score=75             │
│   Gate Mode: wide（開発期）/ narrow（品質期）                │
└─────────────────────────────────────────────────────────────┘
```

#### 教訓
- Wide Gate によって「棒人間SVG + gTTS音声」という低品質でも**システム全体の流れを検証**できた
- もし最初から Narrow Gate だったら、3日間で動くものは作れなかった
- **品質は時間とともに上がる設計**（graduated improvement）

### 2.3 形態非依存の中間表現（Universal Digestion）

#### 設計意図
> **「論文の内容は一度『消化』してから、任意の形態に変換できるようにしたい」**

これは「単一ソース・マルチユース（SSOT）」の原則。

#### データモデル

```python
# 中間表現（形態に依存しない）
DigestedPaper:
  title: str
  summary: str
  atoms: List[AtomicKnowledge]      # 主張・根拠・制約
  metaphors: List[IntuitiveMetaphor] # 高校生レベルの比喩
  skeleton: NarrativeSkeleton       # 起承転結

# 出力形態（Domain Adapter で後付け変換）
ComicAdapter:      DigestedPaper → episode.json (4-panel)
YouTubeAdapter:    DigestedPaper → script.json (hook-3s)
ManzaiAdapter:     DigestedPaper → manzai.json (boke-tsukkomi)
NoteAdapter:       DigestedPaper → article.md
```

#### 設計の利点

| シナリオ | 従来設計（直接変換） | 本設計（中間表現） |
|---------|------------------|----------------|
| 新しい出力形態追加 | 論文→X のパイプラインを一から構築 | Adapter 1つ書くだけ |
| 論文解析の改善 | 全パイプラインを修正 | Digestion 層のみ修正 |
| A/B テスト | 別パイプラインを並列構築 | Adapter のみ差し替え |

---

## 3. データフロー設計の詳細

### 3.1 Paper → Video の完全フロー

```
[Input]
  arXiv Paper / PDF / User Text
      │
      ▼
┌─────────────────────────────────────┐
│  paper-digest (8008)                │
│  • Decompose → AtomicKnowledge      │
│  • Metaphorize → IntuitiveMetaphor  │
│  • Structure → NarrativeSkeleton    │
└─────────────────────────────────────┘
      │
      ▼ DigestedPaper JSON
┌─────────────────────────────────────┐
│  Domain Adapter (paper-digest内)    │
│  • ComicAdapter.apply()             │
│  • Output: episode.json             │
└─────────────────────────────────────┘
      │
      ▼ episode.json
┌─────────────────────────────────────┐
│  storyboard (8009)                  │
│  • plan_cuts() → CutPlan            │
│  • export_timeline() → Timeline     │
│  • 各カットに required_assets 紐付け │
└─────────────────────────────────────┘
      │
      ├──────────┬──────────┬──────────┐
      ▼          ▼          ▼          ▼
  SVG生成     PNG変換     音声生成    字幕生成
  sf-paper-  cairosvg     voicevox   telop
  comic      (CPU)        (or gTTS)  (ASS)
  (8004)                              
      │          │          │          │
      └──────────┴──────────┴──────────┘
                      │
                      ▼ assets/
              ┌───────────────┐
              │  videogen     │
              │  (8006)       │
              │  • slideshow  │
              │  • fade       │
              │  • mux        │
              └───────────────┘
                      │
                      ▼ final.mp4
              ┌───────────────┐
              │  evaluator    │
              │  (8002)       │
              │  • review     │
              │  • suggest    │
              │  • eval_loop  │
              └───────────────┘
                      │
                      ▼ eval_report.json
              ┌───────────────┐
              │  sotsusei.db  │
              │  (SQLite)     │
              └───────────────┘
```

### 3.2 命名・識別設計（paper_id）

#### 設計意図
> **「どの論文から、どの設定で、どんな動画が作られたか100%追跡できる」**

#### 命名規則

```
outputs/papers/{paper_id}/
├── {paper_id}_episode.json                    # 構成定義
├── {paper_id}_final.mp4                       # 完成動画
├── panels/
│   ├── {paper_id}_panel_{NN}.svg              # SVGソース
│   └── {paper_id}_panel_{NN}.png              # PNGレンダリング
├── assets/
│   ├── {paper_id}_voice_{NN}.mp3              # 個別音声
│   ├── {paper_id}_narration.mp3               # 連結音声
│   ├── {paper_id}_narration_padded.mp3        # 無音 padded
│   └── {paper_id}_subs.ass                    # 字幕
└── reports/
    └── {paper_id}_eval_report.json            # 評価結果
```

#### なぜすべてのファイルにprefixを付けるか

- **混在防止**: 一時ディレクトリや共有ボリュームで複数論文のファイルが混ざるリスクを排除
- **grep可能**: `find outputs/ -name "S01_*"` で完全に分離した成果物が抽出できる
- **移動安全**: ディレクトリ構造が崩れてもファイル名で所属論文が分かる
- **DB連携**: `file_path LIKE 'S01_%'` でSQL検索可能

---

## 4. 制約からの設計判断

### 4.1 環境制約

| 制約 | 設計への影響 |
|------|------------|
| WSL + 16GB CPU | GPU系（Stable Diffusion等）はKaggleへ委譲。ローカルはSVG + ffmpeg + gTTS |
| Windowsアクセス | `\\wsl.localhost\Ubuntu\home\bons\...` パスを考慮したファイル配置 |
| Blender 5.0 | bpy-gen DSLでバージョン互換を抽象化 |
| ffmpeg | 全動画処理の統一エンジン。codec=h264, audio=aac |

### 4.2 技術的生態系の制約

| 制約 | 設計への影響 |
|------|------------|
| fastmcp 4.x ≠ mcp 1.x | fastmcpパッケージを完全削除。`mcp.server.fastmcp` のみ使用 |
| PyPI `mcp` パッケージ | ローカル `mcp/` を `mcp_core/` に改名 |
| Voicevox localhost:50021 | gTTSをフォールバックとして実装。声質は下がるがシステムは回る |
| cairosvg の未熟な認知 | ImageMagick の前に cairosvg を試したところ高品質・軽量で採用 |

### 4.3 「ゆるくていい」という制約

| ユーザーの意思 | 設計への現れ |
|-------------|-----------|
| 完成度より回すことを優先 | Wide Gate デフォルト |
| 3Dは後でいい | 最初は棒人間SVGでOK |
| 音声は後でいい | gTTSで暫定、Voicevoxは準備のみ |
| とりあえず動画が出ればOK | S01-resnet（棒人間＋gTTS）で「完成」と宣言 |

---

## 5. 設計パターンの抽出

### 5.1 「Thin Adapter」パターン
**状況**: 新しい規格（MCP）を使いたいが、安定性に不安がある  
**設計**: 各スキルはCLIファースト。MCP/HTTPは外側の薄いラッパー  
**利点**: 規格が変わっても核のロジックは無傷

### 5.2 「Gate Switch」パターン
**状況**: 開発初期と品質期で評価基準が異なる  
**設計**: 同じ評価関数に `gate_mode` パラメータを与える  
**利点**: コードの分岐なしに品質ポリシーを切り替え可能

### 5.3 「Future-Proof Naming」パターン
**状況**: ファイルが増えてくると管理が困難  
**設計**: paper_id をすべての成果物ファイル名にprefix  
**利点**: ディレクトリ構造に依存しない追跡可能性

### 5.4 「Digestion Sandwich」パターン
**状況**: 入力から直接出力を作ると拡張性が失われる  
**設計**: Input → Digest（中間）→ Transform → Output  
**利点**: 入力解析と出力生成が独立して進化

### 5.5 「Fallback Cascade」パターン
**状況**: 外部サービス（Voicevox）が落ちると全体が止まる  
**設計**: Primary（Voicevox）→ Secondary（gTTS）→ Tertiary（無音）  
**利点**: 外部依存の障害でシステムが停止しない

---

## 6. 将来への設計的影響

### 6.1 明示的に設計された拡張点

| 拡張点 | 現在の実装 | 将来の方向 |
|--------|-----------|----------|
| Domain Adapter | Comic, YouTube, Manzai, Note | Podcast, TikTok, Instagram Carousel |
| Evaluator | Image/Video/ASCII metrics | LLM-as-judge, Human-in-loop (JEV) |
| Storyboard | evops-timeline-v1 | OTIO export（agentic-anime-studio連携） |
| Generation | SVG stick figure | bpy-gen 3D scene, ControlNet anime |
| Voice | gTTS fallback | Voicevox multi-speaker, emotion control |
| Distribution | local file | YouTube API, Twitter API |

### 6.2 設計上の懸念事項

| 懸念 | 現状 | 対応策 |
|------|------|--------|
| MCP SDK の変化 | fastmcp 4.x で互換性崩壊 | mcp<2 を固定。CLIファーストを維持 |
| DB スキーマ進化 | sotsusei.db は単一ファイル | マイグレーションスクリプトを今後追加 |
| 大量生成時のI/O | paper_id でファイル数が増大 | 月次/週次アーカイブを検討 |
| 品質の「ゆるさ」が恒常化 | Wide Gate デフォルトのまま | Narrow Gate 移行をMilestoneに設定 |

---

## 7. 総括：設計が語るもの

### 7.1 設計思想の3行まとめ

> **「論文は一度咀嚼して中間表現に変換し、CLIで疎結合なスキル群に処理させ、Wide Gateで量産しながらEval Loopで品質を自律的に高めていく」**

### 7.2 企画意図との整合マトリクス

| Intent | 設計要素 | 整合度 |
|--------|---------|--------|
| 知識の民主化 | Universal Digestion + Metaphor | ✅ 直接導出 |
| 自律的品質向上 | Eval Loop + Gate Switch | ✅ 直接導出 |
| 疎結合拡張 | Thin Adapter + CLI First | ✅ 直接導出 |
| 形態非依存 | Digestion Sandwich | ✅ 直接導出 |
| 再現性追跡 | paper_id + Single DB | ✅ 直接導出 |
| 段階的自動化 | Wide Gate + Fallback Cascade | ✅ 直接導出 |
| 日本語配慮 | ASS + IPAex + Voicevox | ✅ 直接導出 |

### 7.3 設計が示す未来

この設計は**「論文自動収集→自動生成→自動評価→自動配信」**という完全無人パイプラインへの第一歩である。

- 現時点では人間が `episode.json` を確認し、各スキルを順次起動している
- 次の段階では `chaperone workflow.yaml` が全てを自動化する
- 最終的には arXiv API → paper-digest → auto-eval → auto-upload というフローが実現する

設計の柔軟性（疎結合+中間表現）があれば、その道のりは確実に歩める。

---

*本ドキュメントは設計意図と実装の接続を記録し、将来の設計判断の文脈を保全するためのもの。*
