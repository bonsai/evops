# EvOps 開発記録 / DevLog

**プロジェクト**: evops — 論文→アニメ自動生成パイプライン  
**記録開始**: 2026-10-13  
**記録者**: bons

---

## 2026-10-13 (本日)

### 実施した作業

#### 1. paper-survey-agent 統合（paper-digest MCP）
- `paper-survey-agent` を `evops/skills/paper-digest/` へ統合
- `UniversalDigester` クラスを実装
  - **Atomic Knowledge**: 論文を「主張・根拠・制約」に分解
  - **Intuitive Metaphor**: 専門用語を高校生でも分かる比喩に翻訳
  - **Narrative Skeleton**: 起承転結の物語骨組みに構造化
- **ドメイン変換アダプター**を実装
  - `ManzaiAdapter` — 漫才脚本（ボケ・ツッコミ構成）
  - `ComicAdapter` — 4コマ構成案（1コマ〜4コマ）
  - `NoteAdapter` — 解説記事構成
  - `YouTubeAdapter` — 動画構成案（0-3sフック）
- MCP サーバー化（HTTP + stdio デュアルモード、port 8008）
- `evops-mcp` レジストリに登録

**設計判断**: 論文→「咀嚼済みシード」→任意ドメイン変換の3段階パイプライン。  
**理由**: 形式に依存しない中間表現を持つことで、YouTube/漫画/漫才など任意出力への拡張が容易になる。

#### 2. mcp → mcp_core rename
- `evops/mcp/` を `evops/mcp_core/` に改名
- 理由: `mcp` パッケージ名が `pip install mcp` と競合し、FastMCP v1/v3 のimportエラーが発生していたため
- 全サーバーのimport pathを一括置換

#### 3. evops-mcp 統合マネージャー作成
- `scripts/evops-mcp.py` を作成
- 機能: `list`, `status`, `start`, `call`（MCPサーバー管理のワンストップ）
- 8台のMCPサーバーを自動検出・登録

#### 4. storyboard スキル作成
- `skills/storyboard/server.py`（port 8009）
- `episode.json` → **カット割り** → **タイムライン（evops-timeline-v1）** 変換
- 各カットに対して `required_assets`（SVG/PNG/voice）を紐付け

#### 5. evaluator 拡張（論文アニメ評価）
- `review_paper_anime(video_path, episode_json, gate_mode)` 追加
  - 視覚品質・内容網羅性・構造的一貫性・字幕音声同期をチェック
  - 100点満点の総合スコア + A/B/C/D グレード
- `suggest_improvements(eval_results, gate_mode)` 追加
  - 評価結果から優先度付きの改善アクションを生成
- `eval_loop(video, episode, max_iterations, target_score, gate_mode)` 追加
  - 評価→提案→再評価のループ制御

#### 6. ゲートモード（Wide / Narrow Gate）実装
- **Wide Gate**（広いゲート）: 緩やかな基準。多くの作品を通す。合格点50、A=80
- **Narrow Gate**（狭いゲート）: 厳格な基準。高品質のみ通す。合格点75、A=95
- 各評価軸（輝度、字幕網羅率、解像度）の閾値をゲートモードで切り替え

**設計判断**: 「完成状況はゆるくていい」という要求から、Wide Gate をデフォルトに。  
理由: 開発初期は量産・テストを優先し、品質は後から絞り込む方針。

#### 7. S01-resnet 論文アニメ完成
- **入力**: ResNet論文（skip connections / vanishing gradient）
- **出力**: 20秒の4コマ連続再生動画（MP4）
- **構成**:
  1. Setup — 「深く学習すれば賢くなるはず」
  2. Conflict — 「深すぎると情報が届かない！伝言ゲーム状態」
  3. Resolution — 「ショートカット道を作れば解決！」
  4. Punchline — 「これでどんどん深く学べる！」
- **生成フロー**:
  - `paper-digest` → `episode.json`
  - `sf-paper-comic` → 4枚のSVG（棒人間＋吹き出し）
  - cairosvg → PNG（640×480）
  - ffmpeg → スライドショー動画（5秒/コマ、フェード）
  - gTTS → 各コマの日本語音声
  - ASS → 字幕ファイル
  - ffmpeg mux → `final.mp4`（字幕焼込み＋音声合成）

**成果物パス**: `outputs/papers/S01/final.mp4`（298KB、20秒）

#### 8. 生成物管理の命名規則統一
- `paper_id` をファイル名に付与（例: `S01_panel_01.svg`, `S01_voice_01.mp3`）
- `svg-gen.py`, `storyboard` のアセット参照を同期更新
- 管理ディレクトリ: `outputs/papers/{paper_id}/`

#### 9. agentic-anime-studio 資産調査
- `mcp-storyboard` — 台本→シーン構造化・OTIO出力（stub実装）
- `mcp-2d-pipeline` — 2Dアニメ特化・ControlNet/LoRA管理（stub実装）
- `mcp-ojev` — 統計的品質検証（Logits評価）
- `rust-processor` — 高速サムネイル/WebP変換
- **判断**: `mcp-storyboard`の概念をevopsの`storyboard`スキルに統合。OTIO出力は将来拡張。

### 現在のシステム構成

```
evops/
├── mcp_core/              ← コアインフラ（旧mcp/）
│   ├── evaluator/         # 評価 (port 8002)
│   ├── gateway/           # ゲートウェイ (port 8000)
│   ├── db/                # DB (port 8001)
│   └── base_server.py     # 共通MCPサーバーテンプレート
│
├── skills/                ← ドメインMCP
│   ├── paper-digest/      # 論文咀嚼 (port 8008)
│   ├── sf-paper-comic/    # SVG生成 (port 8004)
│   ├── storyboard/        # カット割り (port 8009)
│   ├── bpy-gen/           # 3D生成 (port 8005)
│   ├── videogen/          # 動画編集 (port 8006)
│   ├── artcraft/          # エフェクト (port 8007)
│   ├── voicevox/          # TTS（ななちゃん）
│   ├── telop/             # 字幕
│   └── effect-eval/       # エフェクト評価
│
├── scripts/evops-mcp.py   # MCP統合マネージャー
├── outputs/papers/S01/    # 生成物（論文番号管理）
└── docs/devlog.md         # ← 本ファイル
```

### 次のアクション / TODO

1. **S02 以降の論文パイプライン自動化**
   - `chaperone` workflow で `paper_id` 指定→全自動生成
   - 現在は手動で各スキルを呼び出している

2. **voicevox エンジン接続**
   - 現在は gTTS を使用（品質・表現力の制限あり）
   - Voicevox（ななちゃん）へ切り替えて感情表現を追加

3. **eval_loop の自動再生成連携**
   - 現在は「評価と提案のみ」。実際の再生成は手動
   - `suggest_improvements` の `action` フィールドを自動実行に接続

4. **agentic-anime-studio 統合**
   - `mcp-ojev` の統計的評価を evaluator に組み込む
   - `rust-processor` の高速変換パイプラインを検討

5. **DB層への評価結果蓄積**
   - `eval_report.json` → `mcp_core/db/sotsusei.db` へ保存
   - 次回生成時のフィードバックループ実現

---

## 2026-10-12（昨日）

### 実施した作業

#### evops リポジトリ再構成
- domain-specific MCP を `skills/` へ移設
- `chaperone/` workflow manager を追加
- `telop/`, `voicevox/`, `effect-eval/` スキルを新設
- `lang-brothers/`（4コマ企画エージェント）を追加
- 大規模リファクタリング（267ファイル変更）

#### bpy-gen DSL統合
- `bpy_gen_dsl(dsl_json)` ツール追加
- Blender Python を自動生成（DSL → AST → IR）
- 既存の固定キャラクタースクリプトも DSL 経由で統一

#### P03 VideoScore クローズドループ検証
- `episode.json` → SVG → PNG → raw.mp4 → final.mp4 → `eval_report.json`
- 手動実行で全工程を通し確認

---

## 2026-10-11（一昨日）

### 実施した作業

#### 初期構築
- `evops/mcp/` ディレクトリ構造確立
- `bpy-gen`（Blender連携）、`videogen`（動画編集）MCPサーバー作成
- `evaluator` MCP（CLIP評価、基本画像メトリクス）実装
- `sf-paper-comic` で4コマSVG生成（棒人間＋吹き出し）
- `artcraft` MCP（egg-shadow, zanzou, mediapipe エフェクト）
- `chaperone` workflow YAML 作成（10ステップ）

### 決定事項（ADR）

| # | 決定 | 理由 |
|---|------|------|
| 1 | **Single shared DB** | `bpy-gen` の系譜テーブルも `/home/bons/evops/mcp_core/db/sotsusei.db` で一元管理 |
| 2 | **CLI/JSON loose coupling** | evops は kamishibai/telop/fonts を直接importせず、JSON spec + CLI呼び出し |
| 3 | **Text ticket layer** | 字体/テキスト決定を pending/approved/rejected のチケットで管理 |
| 4 | **MCP as thin adapter** | 各サービスはCLIファースト。HTTP/MCPは後付けのoptional wrapper |
| 5 | **3-Layer Separation** | Planning (`docs/`) → Generation (`skills/`) → Evaluation (`mcp_core/`) |
| 6 | **Evaluation Hierarchy** | Local CPU（基本）→ Kaggle GPU（CLIP/ML）→ JEV（人間フィードバック） |
| 7 | **paper_id naming** | `S01`, `P03` などのIDを生成物ファイル名に埋め込み、混在を防止 |
| 8 | **Gate Mode** | 開発初期は Wide Gate（緩やか）をデフォルトとして量産優先 |

---

## 各種接続情報

| サービス | URL/Path | 状態 |
|----------|----------|------|
| evops-mcp | `~/evops/evops-mcp` | CLI OK |
| paper-digest | `http://localhost:8008` | HTTP OK, stdio OK |
| storyboard | `http://localhost:8009` | HTTP OK |
| evaluator | `http://localhost:8002` | HTTP OK (要起動) |
| S01 final.mp4 | `outputs/papers/S01/final.mp4` | 完成 |

---

*最終更新: 2026-10-13 / Next: S02自動化 or eval_loop自動再生成*
