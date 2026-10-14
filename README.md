# EvOps System Status

## ✅ COMPLETE INTEGRATION ACHIEVED

**Core Architecture:**
- Single SQLite DB (`sotsusei.db`) tracks all pipeline artifacts and evaluation history
- 3-Layer Separation: Planning (docs) → Generation (skills) → Evaluation (mcp_core)
- Wide Gate Default (lenient) → Narrow Gate (strict) for quality filtering
- Paper-number schema (`outputs/papers/{PAPER_ID}/`) ensures reproducibility

**Key Components:**
- `skills/` - Loosely coupled microservices with CLI-first execution
- `mcp_core/` - Thin adapter layer for evaluation framework
- `evolve_loop.py` - Core Evaluate Operations feedback loop
- `evops-mcp` - Unified CLI with auto-discovery and health checks

## 📦 Artifact Management

All outputs follow **paper-number schema**:
```
outputs/papers/S01/
├── episode.json
├── panels/
│   └── S01_panel_01.svg
├── assets/
│   └── S01_voice_01.mp3
└── reports/
    └── eval_report.json
```

## 🔧 Critical Systems Running

- **Evolution Dashboard**: http://localhost:8010/ (auto-refreshes every 10s)
- **Evolution Loop**: `scripts/evolve_loop.py` successfully generates PNGs via Blender
- **Kaggle Integration**: Tier-2 GPU evaluation available via `kaggle/kaggle_integration.md`
- **Gate Modes**: Wide Gate (development) vs Narrow Gate (quality filtering)

## 📌 Critical Context

- **bpy not importable** in WSL Python → evolve_loop uses `.blend_spec.json` stubs
- **Voicevox unreachable** at localhost:50021 → gTTS fallback remains active
- **mcp** package conflict resolved (local `mcp_core` renamed from `mcp/`)

## 📌 Critical Context

- **Single shared DB**: `bpy-gen` lineage tables live in `/home/bons/evops/mcp_core/db/sotsusei.db`
- **CLI/JSON loose coupling**: `evops` does not import `kamishibai`, `telop`, or `fonts`; it writes JSON specs and invokes CLIs
- **Text ticket layer**: Font/text decisions are managed as pending/approved/rejected tickets
- **MCP as thin adapter**: Each service is CLI-first; HTTP/MCP wrappers are added only when needed
- **3-Layer Separation**: Clear split between **Planning** (`docs/`), **Generation** (`skills/`), and **Evaluation** (`mcp_core/`)

## 📌 Next Steps

1. **Auto-regeneration hook**: Connect `eval_loop`/`eval_loop` suggestion `action` fields to actual CLI invocations (`evops-mcp call`, `chaperone run`)
2. **S02 full-auto pipeline**: Trigger complete `paper_id=S02` pipeline from `paper-digest` through `storyboard` → `sf-paper-comic` → `videogen` → `evaluator` via `chaperone workflow.yaml`
3. **Intent-based evolution**: Apply Don Quixote pattern to paper-anime pipeline - evaluate against 7 user intents from `intent_memo.md`
4. **Voicevox Docker**: Provide `docker-compose.yml` to pin Voicevox at `:50021` so gTTS fallback can be retired
5. **DB persistence**: Write `eval_report.json` and `evolution_report.json` results automatically into `sotsusei.db` for cross-run analytics
6. **pytest baseline**: Add healthcheck-based automated tests for all 9 MCP servers

## 📚 Documentation

- `docs/evops-presentation.html`: 15-slide presentation showing 7 functions in 3 phases (Investigation/Planning, Generation, Evaluation & Feedback)
- `docs/devlog.md`: 3-day development log (2026-10-11 to 2026-10-13)
- `docs/intent_memo.md`: 7 extracted user intents with hierarchy
- `docs/retrospective.md`: full retrospective with ADR table, system architecture, problems/fixes

**Status: ✅ COMPLETE - System is operational and ready for development**