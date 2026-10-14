# EvOps Development Retrospective

**期間**: 2026-10-11 〜 2026-10-13（3日間）  
**対象**: 論文→アニメ自動生成パイプライン（evops）  
**担当**: bons

---

## 1. 成果一覧（What was built）

### 1.1 MCP サーバー群（8台）

| サーバー | Port | 役割 | 状態 |
|----------|------|------|------|
| gateway | 8000 | ルーティング・認証 | ✅ Stub |
| db | 8001 | SQLite統合・履歴管理 | ✅ 動作中 |
| evaluator | 8002 | 画像/動画/論文アニメ評価 | ✅ 拡張済 |
| sf-paper-comic | 8004 | 4コマSVG生成 | ✅ 動作中 |
| bpy-gen | 8005 | Blender 3D生成 + DSL | ✅ 動作中 |
| videogen | 8006 | 動画編集・フェード・mux | ✅ 動作中 |
| artcraft | 8007 | エフェクト（egg-shadow等）| ✅ 動作中 |
| paper-digest | 8008 | 論文咀嚼・ドメイン変換 | ✅ 統合済 |
| storyboard | 8009 | カット割り・タイムライン | ✅ 新規 |

### 1.2 スキル・支援ツール群

| コンポーネント | 説明 |
|---------------|------|
| chaperone | Workflow YAML定義・10ステップ自動実行 |
| lang-brothers | 4コマSF落語企画エージェント |
| telop | ASS字幕生成・CLIツール |
| voicevox | TTS（ななちゃん）― 準備中、現状gTTS使用 |
| effect-eval | エフェクト専用評価（ASCII/動画） |
| evops-mcp | 統合マネージャー（list/start/call/status） |

### 1.3 実際の生成物（S01-resnet）

```
outputs/papers/S01/
├── episode.json           # 4コマ構成定義
├── final.mp4              # 完成動画（20秒, 298KB, h264+aac）
├── panels/
│   ├── S01_panel_01.svg   # 設定：深く学習すれば…
│   ├── S01_panel_02.svg   # 衝突：情報が届かない
│   ├── S01_panel_03.svg   # 解決：ショートカット道
│   ├── S01_panel_04.svg   # 結論：どんどん深く学べる
│   └── S01_panel_*.png    # cairosvg変換（640×480）
└── assets/
    ├── raw.mp4            # スライドショー（フェード付き）
    ├── subs.ass           # 字幕ファイル
    ├── narration.mp3      # gTTS音声
    └── voice_0*.mp3       # 個別音声ファイル
```

### 1.4 データベース設計

```sql
-- sotsusei.db 主要テーブル
bpy_renders        -- 3Dレンダリング履歴（job_id, file_path, params, timestamp）
evaluations        -- 評価結果（video_path, score, report_json）
workflows          -- chaperone実行履歴
knowledge_atoms    -- Universal Digestion output（元: atomic_knowledge）
```

---

## 2. 設計判断の振り返り（Design Decisions）

### 2.1 ADR（Architecture Decision Records）

#### ADR-001: Single Shared Database
- **決定**: `bpy-gen`, `evaluator`, `chaperone` 等全てを `sotsusei.db` で一元管理
- **代替案**: 各スキルが独立したSQLiteを持つ
- **理由**: 横断クエリが容易、バックアップが単一ファイルで済む
- **現状**: 正常動作中。各スキルは `mcp_core.db.connection` 経由で接続

#### ADR-002: CLI/JSON Loose Coupling
- **決定**: `evops` は `kamishibai`, `telop`, `fonts` を直接importせず、JSON spec + シェル経由で呼び出す
- **代替案**: Pythonのimportで統合
- **理由**: 各リポジトリが独立して進化可能、言語の縛りなし、テスト容易
- **現状**: `bridge_kamishibai.sh`, `telop/bin/telop-cli.js` 等で動作確認済

#### ADR-003: MCP as Thin Adapter
- **決定**: 各スキルはCLIファースト、HTTP/MCPは後付けのoptional wrapper
- **理由**: MCPが新興規格で不安定（fastmcp 4.x vs mcp 1.xの崩壊体験）、CLIは永続的
- **現状**: 全スキルが `python3 server.py --http` と `python3 server.py --stdio` の両モードをサポート

#### ADR-004: mcp → mcp_core Rename
- **決定**: ローカル `evops/mcp/` を `evops/mcp_core/` に改名
- **理由**: PyPIパッケージ `mcp` との名前空間衝突（`cannot import name 'FastMCP'` エラー発生）
- **影響**: 全サーバーのimport文を一括置換（200行超の変更）
- **教訓**: ローカルパッケージ名はPyPIと重複しないプレフィックス必須

#### ADR-005: 3-Layer Separation
- **決定**: Planning (`docs/`) → Generation (`skills/`) → Evaluation (`mcp_core/`) の明確な分離
- **理由**: 責務の分離、並行開発、テスト容易
- **現状**: `docs/seed_domains.md` で3ドメイン（Paper/Idol/Comedy）を定義済

#### ADR-006: Wide Gate Default
- **決定**: 評価基準は「広いゲート」をデフォルトに（合格点50、A=80）
- **理由**: ユーザーの「完成状況はゆるくていい」指示。量産・テストを優先
- **今後**: Narrow Gate（合格75、A=95）へ段階的移行予定

#### ADR-007: paper_id Naming Convention
- **決定**: 生成物に `{paper_id}_panel_01.svg` 等のプレフィックスを付与
- **理由**: 同一ディレクトリでのファイル混在を防止、追跡容易
- **実装**: `svg-gen.py`, `storyboard/server.py` 両方で同期

#### ADR-008: Universal Digestion Architecture
- **決定**: 論文→ドメイン固有出力の直接変換ではなく、中間表現を挟む
- **中間表現**: `AtomicKnowledge` + `IntuitiveMetaphor` + `NarrativeSkeleton`
- **理由**: 単一ソース・マルチユース（論文1本→漫画/動画/漫才/記事の複数出力）

---

## 3. システム全体像（Current Architecture）

```
┌─────────────────────────────────────────────────────────────────┐
│                         Input Layer                              │
│   Paper (arXiv) → PDF/Text → paper-digest MCP (port 8008)      │
│                        ↓                                         │
│            UniversalDigestion (論文→中間表現)                    │
│                        ↓                                         │
│         DomainAdapter (comic/youtube/manzai/note)                │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Planning Layer (docs/)                      │
│   episode.json (4コマ定義)                                       │
│   workflow.yaml (chaperone 10-step)                              │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Generation Layer (skills/)                   │
│   ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌────────────┐     │
│   │storyboard│→│sf-paper- │→│bpy-gen  │→│ videogen   │     │
│   │(cut plan)│  │comic     │  │(3D opt) │  │(mp4/mux)   │     │
│   └──────────┘  │(SVG/PNG) │  └─────────┘  └────────────┘     │
│                 └──────────┘          ↑                          │
│   ┌──────────┐  ┌──────────┐          │                          │
│   │ telop    │  │ voicevox │──────────┘                          │
│   │(ASS sub) │  │(TTS/narr)│                                     │
│   └──────────┘  └──────────┘                                     │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Evaluation Layer (mcp_core/)                  │
│   ┌──────────────────────────────────────────────┐              │
│   │ evaluator (port 8002)                        │              │
│   │ • review_paper_anime(video, episode, gate)  │              │
│   │ • suggest_improvements(eval_results)        │              │
│   │ • eval_loop(video, episode, max_iter, tgt)  │              │
│   │ • Wide Gate / Narrow Gate switch            │              │
│   └──────────────────────────────────────────────┘              │
│                                ↓                                │
│   ┌──────────────────────────────────────────────┐              │
│   │ sotsusei.db (SQLite, single shared)          │              │
│   └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 技術的負債と解決済み問題（Problems & Fixes）

| 問題 | 原因 | 解決策 | ステータス |
|------|------|--------|-----------|
| mcp/fastmcp import エラー | fastmcp 4.x が mcp 1.x と非互換 | `fastmcp` パッケージ削除、`mcp.server.fastmcp` 使用 | ✅ 解決 |
| mcp パッケージ名衝突 | ローカル `mcp/` と PyPI `mcp` | `mcp_core/` に改名 | ✅ 解決 |
| Voicevox 接続不能 | localhost:50021 応答なし | gTTS をフォールバックに使用 | ⏳ 暫定対応 |
| git submodule 障害 | skills/bpy-gen がサブモジュール化 | `.git` 削除、ファイル直接配置 | ✅ 解決 |
| SVG→PNG 変換 | 初期は手動 or ImageMagick | cairosvg の発見・導入 | ✅ 解決 |
| S01 ファイル名混在 | paper_id なしで後から追加困難 | 命名規則導入 + 全生成物一括rename | ✅ 解決 |

---

## 5. 3日間の開発フロー振り返り

### 10/11（Day 1）— 基盤構築
- **目標**: 「mcp」という名前空間で統合サーバー群を構築
- **結果**: gateway, db, evaluator, bpy-gen, videogen, sf-paper-comic, artcraft の7台を作成
- **問題発生**: fastmcp 4.x のアップデートで動かなくなる

### 10/12（Day 2）— 再構成とDSL
- **目標**: domain-specific コンポーネントを skills/ へ分離
- **結果**: chaperone, telop, voicevox, lang-brothers, effect-eval を追加。267ファイル変更の大型リファクタリング
- **問題発生**: mcp パッケージ名衝突 → import エラー

### 10/13（Day 3）— 統合と評価ループ
- **目標**: 論文→動画の完全自動化 + 評価ループ
- **結果**: 
  - paper-digest 統合（mcp_core rename含む）
  - storyboard 作成（カット割り）
  - evaluator 拡張（review + suggest + eval_loop + gate_mode）
  - S01-resnet の完成動画生成（final.mp4, 20秒）
  - devlog.md, intent_memo.md, retrospective.md のドキュメント化
- **残タスク**: eval_loop の自動再生成連携（手動ステップが残る）

---

## 6. 評価：何がうまくいったか（What went well）

1. **疎結合設計の実証**: `paper-digest` → `storyboard` → `videogen` を個別に起動・テストでき、連携はJSON spec経由で問題なし
2. **命名規則の効果**: `S01_panel_01.svg` 形式により、複数論文の生成物が混在する未来でも安全
3. **cairosvg の発見**: SVG→PNG の品質とサイズが良好（17-21KB）
4. **ゲートモード**: Wide/Narrow で同じコードベースで品質基準を切り替えられる
5. **ドキュメント文化**: 設計判断（ADR）とIntentメモを即座に残せた

## 7. 評価：改善すべき点（What could be better）

1. **MCP SDK の不安定さ**: fastmcp 4.x との互換性問題で半日を消費。今後はLTSバージョンを固定化すべき
2. **Voicevox 接続**: 準備は整っているがエンジン未起動。Docker Compose で固定化すべき
3. **手動ステップ残存**: 
   - SVG 生成後の手動 cairosvg 変換
   - 音声生成後の手動 ffmpeg concat
   - eval_loop の「評価→提案→手動修正→再評価」
4. **テスト不足**: 現状は手動で `./evops-mcp call` で確認のみ。自動テストがない
5. **エラーハンドリング**: `video_metrics` 失敗時のフォールバックが不完全

---

## 8. 次のステップ（Next Actions）

### 短期（1-2日）
- [ ] **eval_loop 自動化**: `suggest_improvements` の `action` フィールドを実際のCLI呼び出しに接続
- [ ] **S02 自動パイプライン**: `chaperone workflow.yaml` で paper_id=S02 を指定して全自動実行
- [ ] **Voicevox 固定**: Docker Compose で `:50021` を立ち上げ、`gTTS` フォールバックを維持

### 中期（1週間）
- [ ] **agentic-anime-studio 統合**: `mcp-ojev` の統計的評価を evaluator に組み込み
- [ ] **自働 DB 蓄積**: `eval_report.json` → `sotsusei.db` への自動書き込み
- [ ] **テスト基盤**: `pytest` で各MCPサーバーの healthcheck を自動化

### 長期（1ヶ月）
- [ ] **Web UI ダッシュボード**: 現在の `docs/index.html` を動的化
- [ ] **arXiv 自動収集**: `paper-digest` に arXiv API 連携
- [ ] **YouTube アップローダー**: `skills/youtube-upload/` スキル作成
- [ ] **Narrow Gate 移行**: 品質基準を Wide → Narrow へスイッチ

---

## 9. ユーザーの Intent との整合性確認

| Intent | 現状の整合度 | 備考 |
|--------|-----------|------|
| 知識の民主化（論文→物語）| ✅ 高 | S01-resnet で実証済 |
| 自律的品質向上 | ⚠️ 中 | eval_loop は手動修正が必要 |
| 疎結合・拡張可能 | ✅ 高 | 9台のMCPが独立稼働 |
| 形態非依存の中間表現 | ✅ 高 | UniversalDigestion + 4アダプター |
| 再現性・追跡可能性 | ✅ 高 | paper_id + 単一DB |
| 段階的自動化（ゆるく）| ✅ 高 | Wide Gate デフォルト、gTTS暫定 |
| 日本語コンテンツへの配慮 | ⚠️ 中 | ASS字幕OK、Voicevox未接続 |

---

## 10. 総括（Summary）

3日間で「論文テキスト→教育アニメ動画」という一見不可能に見えたパイプラインを、**実際に動くシステム**として構築した。

最大の成果は**MCPサーバー群による疎結合アーキテクチャの実証**である。各コンポーネントが独立して動作し、JSON spec のみで連携する設計は、ユーザーが意図する「拡張性」と「メンテナンス性」を満たしている。

一方で、**完全自動化にはまだ距離がある**。現在は「半自動」で、CUI操作からの eval_loop の最終ステップ（自動再生成）が未実装。これは次期スプリントの最優先事項となる。

**現時点では S01-resnet の完成動画（20秒）が、本システムの動作実証として十分な成果物**である。

---

*本ドキュメントは2026-10-13時点のスナップショットであり、次回更新時には「S02自動化」「eval_loop完全自動化」を報告することを目標とする。*
