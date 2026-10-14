# Kaggle Integration — Tier-2 GPU Evaluation

## 概要

Kaggle Notebooks を **Tier-2 評価基盤** として本システムに統合する。
Local CPU では計算不可能な CLIP-based セマンティック類似度スコアリングや、VideoScore フレーム解析を無料 GPU で実行する。

## ファイル構成

```
evops/
├── kaggle/
│   ├── eval_clip_gpu.ipynb       # CLIP 画像評価
│   ├── eval_videoscore.ipynb     # 動画フレーム評価
│   ├── kaggle_push.py            # Local → Kaggle データ送信
│   ├── kaggle_pull.py            # Kaggle → Local 結果取得
│   └── requirements_notebook.txt # 固定依存
├── docs/10-architecture/
│   ├── evaluation_tiers.md       # 本ファイル
│   └── kaggle_integration.md     # ← このファイル
└── scripts/
    └── evolve_loop.py            # Kaggle eval 呼び出し統合
```

## ワークフロー

### 1. Local 側 — 評価対象の準備

```bash
# 評価対象画像/動画を ZIP 化
python3 kaggle/kaggle_push.py \
  --input outputs/papers/S01/final.mp4 \
  --concept donpen \
  --paper-id S01
# → outputs/kaggle_input/evops_S01_donpen.zip
```

### 2. Kaggle Notebook 実行

```python
# eval_clip_gpu.ipynb (冒頭セル)
from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
HF_TOKEN = secrets.get_secret("HF_TOKEN")

# データセット読み込み
!unzip /kaggle/input/evops-eval/evops_S01_donpen.zip -d /tmp/evops

# CLIP モデル読み込み
import torch, clip
model, preprocess = clip.load("ViT-B/32", device="cuda")

# スコアリング
scores = []
for img_path in image_paths:
    image = preprocess(Image.open(img_path)).unsqueeze(0).to("cuda")
    text = clip.tokenize(["Donpen, cute penguin mascot"]).to("cuda")
    with torch.no_grad():
        logits_per_image, _ = model(image, text)
        scores.append(logits_per_image.item())

# 結果出力
import pandas as pd
pd.DataFrame({"frame": frame_ids, "clip_score": scores}).to_csv("scores.csv", index=False)
```

### 3. Local 側 — 結果取得・統合

```bash
python3 kaggle/kaggle_pull.py \
  --kernel evops-clip-eval \
  --output outputs/papers/S01/kaggle_scores.csv
```

`kaggle_pull.py` は Kaggle API で Notebook の最新実行結果をダウンロードし、`sotsusei.db` の `eval_kaggle` テーブルに INSERT する。

## 必要 Secrets

| Secret Name | Purpose | Created By |
|-------------|---------|------------|
| `HF_TOKEN` | HuggingFace model download | User |
| `KAGGLE_USERNAME` | Kaggle API auth | User |
| `KAGGLE_KEY` | Kaggle API auth | User |

設定方法:
```python
from kaggle_secrets import UserSecretsClient
UserSecretsClient().set_secret("HF_TOKEN", "hf_xxxxx")
```

## コスト・制約

| Resource | Limit | Strategy |
|----------|-------|----------|
| T4 GPU | 30h/week | Daily batch, priority queue |
| A100 × 2 | 20h/week | Heavy eval only (VideoScore fine-tuning) |
| Disk | 20GB | Auto-cleanup old outputs |
| Runtime | 12h/session | Chunk large jobs |

超過時は **Tier-1 Local CPU fallback**（Wide Gate 継続）で運用継続。

## 統合コード例

`evolve_loop.py` からの呼び出し:
```python
if run_kaggle_eval:
    scores = kaggle.run_eval_clip(
        image_paths=panel_pngs,
        concept=concept,
        prompt=prompt,
    )
    kaggle_score = sum(scores) / len(scores)
    total_score = local_score * 0.4 + kaggle_score * 0.6  # Kaggle heavier weight
```

## 今後の拡張

- [ ] Kaggle Secrets 自動設定スクリプト
- [ ] Kaggle Kernel バージョニング（eval_v1, eval_v2）
- [ ] 複数 Kernel のアンサンブル評価
