# 機械学習と Kaggle

## 目的

EVOPS の評価履歴を使って、人間の評価を補助する予測モデルを学習・検証する。Kaggle は実験・GPU学習の環境として利用し、EVOPS の SQLite / JSONL を実験履歴の正本として維持する。

## 責務の境界

- **EVOPS**: 生成物、人間評価、実験ID、評価履歴、予測との比較レポートを保持する。
- **Kaggle Dataset**: 学習に使うデータのスナップショットをバージョン管理する。
- **Kaggle Notebook**: 特徴量抽出、ベースライン、モデル学習、検証、予測成果物の生成を行う。
- **人間**: 評価データの品質、モデルの誤差、採用可否を判断する。

Kaggle をワークフロー管理や唯一のDBにしない。接続は CSV / JSONL の入出力から始め、Kaggle が使えない場合も既存の EVOPS が動く構成にする。

## 最初のユースケース

**人間評価スコアの予測**から始める。

- 入力: 画像または文章の特徴量、および人間評価済みサンプル
- 出力: 予測スコア、実測との差、評価指標
- 目的: 人間評価を置き換えるのではなく、候補の優先順位付けと評価の省力化を支援する

クラスタリング、異常検知、ベイズ最適化は、最小モデルの再現性を確認した後に追加する。

## データ契約

EVOPS からエクスポートする学習データは、最初は JSONL または CSV とする。JSONL の例:

```json
{"sample_id":"stable-id","asset_uri":"dataset-relative/path","human_score":0.0,"split":"train","schema_version":"1"}
```

- `sample_id`: データセット内で安定した識別子
- `asset_uri`: Dataset 内の相対パス。ローカルの絶対パスは使わない
- `human_score`: 人間が実際に付けた数値評価
- `split`: `train` / `validation` / `test`
- `schema_version`: データ契約の版

教師あり学習には人間評価があるサンプルだけを使う。データ分割は学習前に固定し、同じ元画像や重複サンプルが train と validation にまたがらないようにする。個人情報、APIキー、秘密情報は Kaggle にアップロードしない。

## 最小実験フロー

1. [ ] EVOPS の評価履歴から、利用条件を確認したデータをエクスポートする。
2. [ ] データ件数、欠損、重複、スコア分布を検査する。
3. [ ] Kaggle Dataset を作成し、データ版を記録する。
4. [ ] Kaggle Notebook で単純な平均予測などのベースラインを作る。
5. [ ] scikit-learn の回帰モデルを学習し、MAE / RMSE をベースラインと比較する。
6. [ ] データ版、Notebook版、依存ライブラリ、乱数シード、指標を記録する。
7. [ ] validation 予測を CSV / JSONL で出力し、EVOPS に取り込む。
8. [ ] 予測と人間評価の差をレポート化し、人間が採用可否を判断する。

## 成果物の最小セット

- `predictions.csv`: `sample_id`, `human_score`, `predicted_score`, `absolute_error`
- `metrics.json`: データ版、Notebook版、MAE、RMSE、サンプル数、乱数シード
- `README.md`: データの由来、実行手順、既知の制約

モデルファイル自体は最初から EVOPS に組み込まない。予測成果物を取り込む運用を確立してから、必要に応じてモデル配布を検討する。

## 合格条件

- [ ] ベースラインと ML モデルを同じ validation データで比較できる
- [ ] 実験を同じデータ版・設定で再現できる
- [ ] 人間評価との誤差と失敗例を確認できる
- [ ] Kaggle が停止しても EVOPS の既存機能が動作する
- [ ] 自動採用を行う前に、人間が予測結果を確認できる

## 将来の拡張

1. 成功パターン抽出: クラスタリング、PCA / UMAP による可視化
2. 異常検知: 崩壊画像や低品質出力の検出
3. パラメータ探索: Optuna 等を使った探索
4. 文章品質評価: テキスト特徴量と人間評価の予測

## 参考

- [Kaggle Notebooks](https://www.kaggle.com/docs/notebooks)
- [Kaggle Datasets](https://www.kaggle.com/docs/datasets)
- [Kaggle CLI](https://github.com/Kaggle/kaggle-cli)
