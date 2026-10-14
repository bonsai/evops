# System Overview — EvOps Complete Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                                    │
│  Paper PDF / ArXiv URL / Raw Text / Concept Prompt                     │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      00-CONCEPT / PLANNING                              │
│  paper-digest (8008) → episode.json                                     │
│  storyboard   (8009) → evops-timeline-v1                                │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      20-PIPELINE / GENERATION                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │ svg-gen  │  │ videogen │  │ voicevox │  │ bpy-gen  │                │
│  │ (comic)  │  │ (movie)  │  │ (audio)  │  │ (3D char)│                │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                │
│       │             │             │             │                        │
│       ▼             ▼             ▼             ▼                        │
│   S02_panel_01.svg  raw.mp4   narration.mp3  gen_donpen_00.png          │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   10-ARCHITECTURE / EVALUATION                          │
│                                                                         │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐      │
│   │  TIER-1 Local   │   │  TIER-2 Kaggle  │   │  TIER-3 JEV     │      │
│   │  CPU (WSL)      │──►│  GPU (T4/A100)  │──►│  Human Gate     │      │
│   │                 │   │                 │   │                 │      │
│   │ • Brightness    │   │ • CLIP score    │   │ • Aesthetic     │      │
│   │ • Keyword match │   │ • VideoScore    │   │ • Coherence     │      │
│   │ • Attribute chk │   │ • FID / IS      │   │ • Creative      │      │
│   │ • <1s / $0      │   │ • Batch / free  │   │ • Manual queue  │      │
│   └─────────────────┘   └─────────────────┘   └─────────────────┘      │
│                                                                         │
│   evaluator MCP (8002)     kaggle/*.ipynb      review_paper_anime()    │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                    feedback loop   │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   30-OPERATIONS / EVOLUTION                             │
│                                                                         │
│   eval_report ──► evolve_prompt() ──► enriched prompt                  │
│        │                                               │                │
│        └───────────────────────────────────────────────┘                │
│                              │                                          │
│                              ▼                                          │
│                    generate_character_bpy()                             │
│                              │                                          │
│                              ▼                                          │
│                    next generation evaluation                           │
│                              │                                          │
│                    converged? ──► YES ──► DEPLOY                        │
│                                                                         │
│   Dashboard: http://localhost:8010/  (auto-reload 10s)                  │
│   DB: mcp_core/db/sotsusei.db                                          │
└────────────────────────────────────────────────────────────────────────┘
```

## MCP Server Registry

| Server | Port | Role | Transport |
|--------|------|------|-----------|
| `bpy-gen` | 8005 | 3D character rendering | HTTP + stdio |
| `videogen` | 8006 | Video composition | HTTP |
| `artcraft` | 8007 | Effect composition | HTTP |
| `paper-digest` | 8008 | Paper universal digestion | HTTP + stdio |
| `storyboard` | 8009 | Cut planning & timeline export | HTTP + stdio |
| `evolution-dashboard` | 8010 | Evolution visualization | HTTP + stdio |
| `evaluator` | 8002 | Multi-axis evaluation | HTTP |

## Kaggle Integration Points

1. **Data Push** (`kaggle/kaggle_push.py`)
   - Local renders → Kaggle Dataset input
   
2. **GPU Evaluation** (`kaggle/eval_clip_gpu.ipynb`)
   - CLIP semantic scoring per frame
   - VideoScore temporal consistency
   
3. **Result Pull** (`kaggle/kaggle_pull.py`)
   - Scores CSV → `sotsusei.db` `eval_kaggle` table
   
4. **Auto-Fallback**
   - Kaggle quota exceeded → Tier-1 Wide Gate continues
   - No pipeline stall

## Gate Mode Summary

| Mode | Tier-1 Pass | Tier-2 Target | Tier-3 Use |
|------|-------------|---------------|------------|
| **Wide** | ≥ 50 | ≥ 60 (optional) | Rare |
| **Narrow** | ≥ 75 | ≥ 80 | Required for release |

**Development default: Wide Gate**
> 「完成状況はゆるくていい」— まず回す。
