# Loose coupling: evops/mcp ↔ kamishibai

No direct module import. Only CLI contracts and JSON data exchange.

## Contract
- `evops` writes `episode.json` (from sf-paper-comic)
- `kamishibai` reads `episode.json` via its CLI (`cli/render.js`)
- Output: `mp4` (video artifact)

## Dependency direction
`evops/mcp` → `kamishibai` is one-way (data feed only).
`kamishibai` never calls back to `evops`.

## Execution
```bash
# 1. Generate episode JSON (evops MCP)
python mcp/sf-paper-comic/cli.sh demo-paper-001 > episode.json

# 2. Render to MP4 (kamishibai CLI, independent)
cd /home/bons/kamishibai
node cli/render.js episode.json output.mp4
```
