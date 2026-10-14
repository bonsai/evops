# Full Pipeline — Digest → Storyboard → Gen → Eval → Evolve

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Input     │──►│   Digest    │──►│  Storyboard │──►│  Generate   │──►│  Evaluate   │
│  (Paper)    │   │  (分解)     │   │  (カット設計)│   │  (SVG/Video)│   │  (3-Tier)   │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └──────┬──────┘
                                                                                  │
                                                           ┌──────────────────────┘
                                                           │  feedback
                                                           ▼
                                                    ┌─────────────┐
                                                    │   Evolve    │
                                                    │  (Prompt↑)  │
                                                    └─────────────┘
```

## Phase 1: Input → Digest (Universal Digestion)

**Skill**: `skills/paper-digest/`
**Port**: 8008
**Input**: PDF / ArXiv URL / Text
**Output**: `episode.json` (AtomicKnowledge + IntuitiveMetaphor + NarrativeSkeleton)

```bash
./evops-mcp call paper-digest digest_paper \
  '{"url": "https://arxiv.org/abs/1512.03385", "paper_id": "S02"}'
```

**Adapter Pattern**: Digest 出力はドメイン非依存。2次アダプタで変換:
- `comedy_adapter` → お笑い漫才
- `comic_adapter`   → 4コマSF漫画
- `note_adapter`    → Qiita/note 風解説
- `youtube_adapter` → YouTube 台本

## Phase 2: Digest → Storyboard

**Skill**: `skills/storyboard/`
**Port**: 8009
**Input**: `episode.json`
**Output**: `evops-timeline-v1` JSON (per-cut asset list)

```bash
./evops-mcp call storyboard plan_cuts_tool \
  '{"episode_json_path": "outputs/papers/S02/episode.json", "style": "sf_comic"}'
```

## Phase 3: Storyboard → Generate

### 3a. SVG Panels (`sf-paper-comic`)
**Skill**: `skills/sf-paper-comic/svg-gen.py`
**Flag**: `--paper-id S02`
**Output**: `S02_panel_01.svg` … `S02_panel_04.svg`

### 3b. PNG Rasterization (`cairosvg`)
```bash
for svg in outputs/papers/S02/panels/*.svg; do
  cairosvg "$svg" -o "${svg%.svg}.png"
done
```

### 3c. Video Composition (`videogen`)
**Skill**: `skills/videogen/`
**Port**: 8006
**Input**: 4 PNGs + narration.mp3
**Output**: `raw.mp4` → `final.mp4` (字幕焼き込み)

### 3d. 3D Character (`bpy-gen` — optional)
**Skill**: `skills/bpy-gen/`
**Port**: 8005
**Variants**: `don_quixote_bpy.py`, `donpen_bpy.py`, `doraemon_bpy.py`

## Phase 4: Evaluate (3-Tier)

```
Tier-1 Local CPU ──► evaluator MCP (port 8002)
  ├─ review_paper_anime()
  ├─ suggest_improvements()
  └─ eval_loop()

Tier-2 Kaggle GPU ──► kaggle/eval_clip_gpu.ipynb
  ├─ CLIP semantic score
  ├─ VideoScore frame analysis
  └─ FID / IS (generative metrics)

Tier-3 JEV Human ──► manual_review_queue
  ├─ Aesthetic ranking
  ├─ Narrative coherence
  └─ Creative judgment
```

**Gate Modes**:
| Mode | Threshold | Use Case |
|------|-----------|----------|
| wide  | pass=50, A=80 | 開発中、パイプライン連続実行 |
| narrow| pass=75, A=95 | 品質フィルタ、リリース判定 |

## Phase 5: Evolve

**Script**: `scripts/evolve_loop.py`
**Input**: eval_report + current prompt
**Output**: enriched prompt → regenerate

```
評価結果 (missing attrs) ──► evolve_prompt() ──► 新プロンプト
                                    │
                                    ▼
                          generate_character_bpy()
                                    │
                                    ▼
                               次世代評価
```

**収束条件**: `score >= target_score`（Narrow Gate: 75, Wide Gate: 50）

## Paper-ID 命名規則

すべてのアーティファクトに `paper_id` プレフィックス:
```
outputs/papers/{PAPER_ID}/
├── episode.json
├── panels/
│   ├── {PAPER_ID}_panel_01.svg
│   └── {PAPER_ID}_panel_01.png
├── assets/
│   ├── {PAPER_ID}_voice_01.mp3
│   └── {PAPER_ID}_narration.mp3
└── reports/
    ├── raw.mp4
    ├── final.mp4
    ├── subs.ass
    └── eval_report.json
```

## 自動化統合 — Chaperone

**Skill**: `skills/chaperone/`
**Workflow**: `workflow.yaml`

```yaml
steps:
  - name: digest
    skill: paper-digest
  - name: storyboard
    skill: storyboard
  - name: generate_panels
    skill: sf-paper-comic
  - name: generate_video
    skill: videogen
  - name: evaluate
    skill: evaluator
  - name: loop_if_needed
    skill: evolve_loop
    condition: eval.score < 75
```
