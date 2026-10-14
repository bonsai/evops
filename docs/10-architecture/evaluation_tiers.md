# Evaluation Tiers — 3層評価基盤

EvOps は **生成→評価→進化** の閉ループを高速に回すため、計算資源に応じた3層の評価基盤を持つ。

```
┌─────────────────────────────────────────────┐
│  TIER-1  Local CPU (WSL 16GB)               │
│  ├─ Basic structural checks                 │
│  ├─ Brightness / coverage metrics           │
│  ├─ Attribute keyword matching              │
│  └─ Fast feedback loop (< 1s)               │
├─────────────────────────────────────────────┤
│  TIER-2  Kaggle GPU (T4 / A100 x 2)         │
│  ├─ CLIP semantic similarity scoring        │
│  ├─ VideoScore frame-analysis               │
│  ├─ FID / IS (generative metrics)           │
│  └─ Batch processing with Secrets API       │
├─────────────────────────────────────────────┤
│  TIER-3  JEV Human-in-the-Loop              │
│  ├─ Aesthetic quality ranking               │
│  ├─ Narrative coherence check               │
│  └─ Domain-expert creative judgment         │
└─────────────────────────────────────────────┘
```

---

## Tier-1: Local CPU — Fast Gate

**環境**: WSL Ubuntu, 16GB RAM, CPU only

**役割**: 迅速な合格/不合格判定。パイプラインの各ステップで即座に実行。

**指標**:
| Metric | Tool | Threshold (Wide) | Threshold (Narrow) |
|--------|------|------------------|--------------------|
| Brightness | OpenCV | 0.15–0.95 | 0.35–0.75 |
| Subtitle Coverage | PIL | ≥ 50% | ≥ 90% |
| Attribute Match | Keyword | partial | exact |
| Grade | Custom | pass=50 | pass=75, A=95 |

**コスト**: $0（ローカル実行）
**レイテンシ**: < 1秒/アイテム

---

## Tier-2: Kaggle GPU — Precision Gate

**環境**: Kaggle Notebooks, T4 GPU × 1 or A100 × 2

**役割**: 高品質な自動スコアリング。CPUでは不可能なCLIPベースの意味的類似度、動画品質指標（VideoScore）を計算。

### 統合戦略

#### 1. Notebook 構成
```
kaggle/
├── eval_clip_gpu.ipynb          # CLIP-based image scoring
├── eval_videoscore.ipynb        # Video frame analysis
└── requirements_notebook.txt    # pinned deps
```

#### 2. データフロー
```
Local WSL                      Kaggle GPU
   │                              │
   ├──► Upload dataset via API  ──┤
   │   (evops_kaggle_input.zip)   │
   │                              ├──► Run eval_clip_gpu.ipynb
   │                              │     - Load CLIP model
   │                              │     - Score each frame
   │                              │     - Export scores.csv
   │                              │
   │◄── Download scores.csv ◄────┘
   │
   ├──► Merge into sotsusei.db
   │
   └──► Update dashboard (auto-reload)
```

#### 3. Kaggle Secrets API 連携
```python
from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
huggingface_token = secrets.get_secret("HF_TOKEN")
```
**必須 Secrets**:
- `HF_TOKEN` — HuggingFace model download (CLIP, VideoScore)
- `GITHUB_TOKEN` — Artifact push back to repo
- `OPENROUTER_KEY` — Optional: LLM-based eval fallback

#### 4. タスク別 GPU 割当
| Task | GPU Time | Priority |
|------|----------|----------|
| CLIP image scoring | ~2 min / 100 images | Daily batch |
| VideoScore frame eval | ~5 min / 30 sec video | Per-video |
| FID calculation | ~10 min / 1000 images | Weekly |
| Model fine-tuning | ~1 hour | Rare |

#### 5. コスト管理
- Kaggle: **無料**（T4: 30h/week, A100: 20h/week）
- 超過時は Local CPU fallback（Wide Gate 継続）
- 詳細: [`kaggle_cost_tracker.md`](kaggle_cost_tracker.md)

---

## Tier-3: JEV (Japanese Evaluation Vocabulary) — Human Gate

**環境**: Human evaluators, domain experts

**役割**: 創造性・美的品質・ストーリー一貫性の最終判定。自動評価では捕捉できないニュアンスを評価。

**統合**: `mcp_core/evaluator/server.py` の `review_paper_anime(..., gate_mode="narrow")` で最終判定。人間のスコアは SQLite `human_eval` テーブルに永続化。

---

## Tier 切り替えフローチャート

```
生成物ができた
    │
    ▼
┌──────────────────┐
│ Tier-1 Local CPU │ ──失格──► regenerate
│ (Wide Gate)      │
└────────┬─────────┘
         │ 合格
         ▼
┌──────────────────┐
│ Tier-2 Kaggle GPU│ ──失格──► suggest_improvements
│ (CLIP/VideoScore)│
└────────┬─────────┘
         │ 合格
         ▼
┌──────────────────┐
│ Tier-3 JEV Human │ ──失格──► manual review queue
│ (Narrow Gate)    │
└────────┬─────────┘
         │ 合格
         ▼
      DEPLOY
```