# EvOps Documentation

Evaluate Operations — 自動生成→評価→進化 のリアルタイム閉ループ基盤

## 📂 Directory Structure

| Dir | Purpose |
|-----|---------|
| [`00-concept/`](00-concept/) | 前提・ミッション・戦略・ドメイン定義 |
| [`10-architecture/`](10-architecture/) | システムアーキテクチャ、Kaggle統合評価基盤、3-Tier評価戦略 |
| [`20-pipeline/`](20-pipeline/) | パイプライン設計（Digest → Storyboard → Gen → Eval → Evolve） |
| [`30-operations/`](30-operations/) | 運用マニュアル（evolve_loop, dashboard, 閾値管理） |
| [`40-references/`](40-references/) | 各種参考資料・契約・PRD開発ログ |

## 🧪 Evaluation Tiers（Kaggle Explicit）

```
Tier-1  Local CPU    → Basic metrics, fast feedback      (WSL 16GB)
Tier-2  Kaggle GPU   → CLIP/ML-based scoring, GPU infer  (T4/A100)
Tier-3  JEV Human    → Aesthetic & Creative judgment       (人間評価)
```

Kaggle は **Tier-2 評価基盤** として本システムに統合されています。
詳細: [`10-architecture/evaluation_tiers.md`](10-architecture/evaluation_tiers.md)

## 🚀 Quick Start

```bash
# 全パイプライン実行
./evops-mcp start-all
# Donpen 進化ループ（実物レンダリング込み）
python3 scripts/evolve_loop.py --concept donpen --iterations 3 --target 70
```
