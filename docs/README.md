# EvOps Documentation

Numbered document scheme (latest): `00-` → `50-` priority/phase order.

## Root Design Documents

| # | File | Purpose |
|---|------|---------|
| 00 | `00-intent.md` | Research intent & problem statement |
| 10 | `10-kpi.md` | Key performance indicators |
| 20 | `20-mrd.md` | Market requirements document |
| 21 | `21-prd.md` | Product requirements document |
| 30 | `30-mvp.md` | Minimum viable product definition |
| 40 | `40-poc.md` | Proof of concept plan |

## Task Tracking (`issue/`)

| # | File | Topic |
|---|------|-------|
| 00 | `00-automation-design-evaluation.md` | Auto-evaluation design |
| 01 | `01-evaluation-loop.md` | Evaluation loop architecture |
| 02 | `02-intent-evaluation-agent.md` | Intent-based evaluation agent |
| 03 | `03-doraemon-vlm-correction.md` | VLM character correction |
| 04 | `04-cost-management.md` | Cost & resource management |
| 05 | `05-visualization.md` | Visualization & dashboards |
| 06 | `06-mcp-a2a-redesign.md` | MCP/A2A protocol redesign |
| 07 | `07-image-generation-blender-bpy.md` | Blender-bpy image generation |
| 08 | `08-data-collection-focus.md` | Data collection strategy |
| 09 | `09-novel-evaluation.md` | Novel evaluation metrics |
| 10 | `10-ml-kaggle.md` | ML/Kaggle experiments |
| 11 | `11-roadmap.md` | Development roadmap |
| 12 | `12-plan.md` / `12-plan.json` | Execution plan |

## Presentation Artifacts

- `index.html` — Integrated presentation
- `hw-sotsusei-kanban.md` — kanban board view
- `0.html` — MCP feedback-loop diagram (if present)

## Research Loop

```
Generation → VLM/LMS Evaluation → DB Accumulation → ML Learning → Repair → Regeneration
```
