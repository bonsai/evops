---
name: bqmlite
description: ローカルの SQLite/CSV を BQMLite (bonsai/bqmlite-go) で学習・予測する。BigQuery も MLフレームワークも使わず、決定的(deterministic)に mean / linear_regression / logistic_regression を実行し、結果と SHA-256 fingerprint を返す。「bqmlite」「dbをbqmlite」「BQML風に」「ローカルで学習」「SQLiteを学習/予測」「predict して .db」「fingerprint 出して」「bqmlite-go」などで発動。DB→Dataset変換(scripts/sqlite_to_dataset.py) → エンジン実行 → 再現可能な結果、までを担う。BigQuery本物/クラウド課金/重いMLは対象外。
---

# bqmlite — ローカル BQML 風エンジン

[`bonsai/bqmlite-go`](https://github.com/bonsai/bqmlite-go)（Go・外部依存なし）で、**SQLite/CSV を BigQuery ML 風にローカル実行**する。クラウド不要・無課金・決定的。

- リポジトリ実体: `/home/bons/repos/bqmlite-go`（WSL。無ければ `gh repo clone bonsai/bqmlite-go`）
- Go ≥1.26。`go build ./...` でOK
- コア契約: `Dataset → Train → Model → Predict → PredictionResult`、`Plan`/`Run` 境界、SHA-256 fingerprint

## 対応エンジン

| engine | 説明 | 制約 |
|--------|------|------|
| `mean` | 目的変数の平均を返す決定ベースライン | target 必須・数値 |
| `linear_regression` | 最小二乗（正規方程式・決定的）。特徴量は target 以外の全数値列を**名前順**に自動採用 | target/features すべて数値 |
| `logistic_regression` | 決定的バッチ勾配降下（1000 epoch, lr=0.1） | target は **0/1 のみ**、features 数値 |

特徴量は明示指定ではなく「target 以外のキー全部」から自動推定される。**余計な列（文字列など）があると失敗する**ので、SELECT で数値列だけに絞る。

## Dataset 形式

JSON:
```json
{ "name": "example", "target": "y",
  "rows": [ {"x": 1, "y": 2}, {"x": 2, "y": 4} ] }
```
CSV も読める（ヘッダ行あり）が、**CSV ローダは `target` を設定しない**ため `mean`/回帰では "target is required" になる。→ **JSON + target を推奨**（下記スクリプトを使う）。

## DB を bqmlite する（基本フロー）

`scripts/sqlite_to_dataset.py` で SQLite → Dataset JSON に変換し、CLI で実行する。

```bash
cd /home/bons/repos/bqmlite-go

# 1) DB → dataset.json（read-only・target は数値列を選ぶ）
python3 <このスキル>/scripts/sqlite_to_dataset.py \
  <db_path> "<SELECT 数値列... , target列 FROM ...>" <target列> /tmp/ds.json --name m

# 例: opencode.db のセッションで tokens_output を予測
python3 <このスキル>/scripts/sqlite_to_dataset.py \
  ~/.local/share/opencode/opencode.db \
  "SELECT tokens_input, cost, summary_files, tokens_output FROM session WHERE tokens_output>0" \
  tokens_output /tmp/sessions.json --name sessions

# 2) 実行（結果は stdout、-output で保存）
go run ./cmd/bqmlite -input /tmp/sessions.json -engine linear_regression -output /tmp/out.json
go run ./cmd/bqmlite -input /tmp/sessions.json -engine mean
go run ./cmd/bqmlite -input /tmp/ds.csv -engine logistic_regression   # target 未設定に注意
```

`<このスキル>` = `C:\Users\0501JP\.config\opencode\skills\bqmlite`（WSL からは `/mnt/c/Users/0501JP/.config/opencode/skills/bqmlite`）。

## 出力（PredictionResult）

```json
{ "model_name": "linear_regression",
  "results": [ {"value": 33945.54}, {"value": 17496.58} ] }
```
- `logistic_regression` は `{"value":0|1,"probability":0.83}` を返す
- CLI は **学習も予測も同じ `dataset.rows`** を使う（別データでの予測は下記 Agent JSON / ライブラリ）

## Agent JSON 境界（OpenCode/Hermes 連携）

`bqmlite.ExecuteJSON(ctx, input, registry)` が受け取る形:
```json
{ "plan": { "dataset": { "name":"m","target":"y","rows":[{"x":1,"y":0}] },
            "engine": "logistic_regression",
            "rows": [ {"x":2} ] } }
```
返り値:
```json
{ "result": {...}, "fingerprint": "sha256:..." }
```
- `Plan.rows` を指定すると **その行だけ予測**（学習データと分離可能）。未指定なら dataset.rows
- ⚠️ 薄い CLI(`cmd/bqmlite`) はこの JSON 境界を公開していない。使うには Go の小ハーネス（`ExecuteJSON` を呼ぶ main）を書く

## SQL サブセット（限定的）

```sql
CREATE MODEL <name> OPTIONS(model_type='<...>') AS SELECT ... TARGET ... FROM <dataset>;
```
- パーサは `CREATE MODEL ... AS SELECT ... FROM ...` の最小形のみ。SELECT に `TARGET` を含む必要あり。未対応構文は**エラーで落ちる**（BigQuery 互換を装わない）
- `TranslateSQL` は model 名から engine を推定し、名前に `linear` を含むと `mean` になるクセあり

## Station ドメインアダプタ

`station.Suggest(candidates, weights, limit)` — 特徴量(0..1)の重み付き和でランキング。`DefaultWeights` = phonetic .30 / mora_rhythm .20 / rhyme_structure .20 / semantic .10 / context_association .10 / integrated_fit .10。駅名/ネーミング選定などに使う。

## モデル永続化・再現性

- `SaveModel`/`LoadModel` で `{"engine":"...","model":{...}}` を JSON 保存・復元
- `ResultFingerprint` / `PlanFingerprint` = 安定 JSON の SHA-256（`sha256:...`）。同一入力・同一 engine なら**同一結果**（回帰は特徴量を辞書順・学習パラメータ固定）

## 検証手順

```bash
cd /home/bons/repos/bqmlite-go
go build ./... && go vet ./...
go test ./...            # deterministic unit / regression / artifact tests
```
期待: ビルド成功・テスト緑。`mean` は target 平均、回帰は特徴量を名前順採用。

## 設計境界 / やらないこと

- BigQuery 本物・クラウド課金・SQL 全互換は対象外。SQL は最小サブセット
- ML フレームワーク非依存（mean/線形/ロジットのみ）。深層学習・埋め込みは無い
- 文字列カテゴリの one-hot 等は無い → **DB 側で数値化してから**渡す
- 秘匿データを外部送信しない（完全ローカル）
