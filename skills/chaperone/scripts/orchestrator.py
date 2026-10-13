# bpy-gen MCP Orchestrator

Central coordinator that orchestrates the entire research pipeline:

**Workflow:** Survey → Character Generation → Image Evaluation → Afterimage Visualization

## Services Under Control

| Service | Role | Port |
|---------|------|-------|
| `bpy-gen` | Procedural 3D character generation (Blender) | 8005 |
| `db` | Experiment history & lineage tracking | 8001 |
| `evaluator` | Image quality scoring (CLIP, color stats) | 8002 |
| `blender-bpy` | SVG generation + Blender headless rendering | 8003 |

## Orchestration Flow

```
[Survey] → [bpy-gen] → [evaluator] → [Afterimage (p5js/Java)]
```

Each step produces structured JSON that feeds the next stage.

## API Endpoints

- **Orchestrator**: `/call` (MCP protocol) — dispatches the full pipeline
- **Health**: `/health` — overall system status
- **Logging**: All steps log to `db/experiments` table

## Integration Points

- **Survey** (`noguti`): extracts intent from research goals
- **Gen** (`bpy-gen`): renders 3D characters
- **Eval** (`evaluator`): scores images with VLM/CLIP
- **Afterimage** (p5js/Java): visualizes results as animated sequences

## Running

```bash
# Start all services (in parallel)
python mcp/bpy-gen/server.py --http --port 8005 &
python mcp/db/server.py &
python mcp/evaluator/server.py &
python mcp/blender-bpy/server.py &

# Run orchestrator
python mcp/orchestrator.py
```

## Data Contracts

All services exchange JSON objects with consistent schema:

```json
{
  "step": "gen",
  "input": { ... },  // survey intent
  "output": { ... },  // generated asset ID
  "metadata": { ... }
}
```

See `mcp/README.md` for detailed per-service contracts.
