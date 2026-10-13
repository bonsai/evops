# videogen MCP Server & TUI

`videogen` is a loose‑coupled video editing service that consumes outputs from
other MCP servers (bpy-gen, sf-paper-comic, kamishibai, telop) and produces final MP4 files via `ffmpeg`.

## Features (MCP Tools)

| Tool | Purpose |
|------|---------|
| `compose_video` | Combine an input video with optional audio and subtitle tracks |
| `merge_panels`  | Concatenate multiple panel videos (e.g., from kamishibai) into a single sequence |

Both tools are exposed via the MCP HTTP endpoint at `http://localhost:8006/mcp/tools/<tool_name>`.

## TUI (Terminal User Interface)

A simple curses‑based TUI is provided at `tui.py`. It allows interactive invocation of the two tools and health checking.

### Running the TUI

```bash
# Ensure the videogen server is running (see below)
python mcp/videogen/tui.py
```

### TUI Menu

1. **Compose Video** – Prompt for input video, audio, subtitle, output, resolution, FPS.
2. **Merge Panels** – Prompt for directory containing `panel_*.mp4` files and output path.
3. **Check Server Health** – Ping the `/health` endpoint.
4. **Exit** – Return to shell.

## Server Usage (HTTP)

Start the server in HTTP mode:

```bash
python mcp/videogen/server.py --http --port 8006
```

The server mounts MCP tools under `/mcp/tools/` and provides `/health` and `/ready` probes.

### Example Calls

```bash
# Compose video with audio and subtitles
curl -X POST http://localhost:8006/mcp/tools/compose_video \
  -H "Content-Type: application/json" \
  -d '{
    "input_video": "/tmp/merged.mp4",
    "audio_path": "/tmp/narration.mp3",
    "subtitle_path": "/tmp/subs.ass",
    "output_path": "/tmp/final.mp4",
    "resolution": 1280,
    "fps": 30
  }'

# Merge four panel videos
curl -X POST http://localhost:8006/mcp/tools/merge_panels \
  -H "Content-Type: application/json" \
  -d '{
    "panel_dir": "/tmp/panels",
    "output_path": "/tmp/merged.mp4"
  }'
```

## Dependencies

- `ffmpeg` (must be in `$PATH`)
- Python 3.8+ (standard library only: `curses`, `json`, `urllib`)

## Loose‑Coupled Design

`videogen` does **not** import any other MCP service code. It interacts solely via:

- Input video files (produced by `kamishibai` or previous steps)
- Optional audio/subtitle files (produced by `telop` or external tools)
- Output video files (consumed by downstream steps or stored as artifact)

This allows each stage (3D generation, SVG creation, panel rendering, telop addition) to be replaced or scaled independently.

## Integration Example (Full Pipeline)

```bash
# 1. Generate episode JSON (sf-paper-comic)
python mcp/sf-paper-comic/cli.sh demo-paper-001 > episode.json

# 2. Create SVGs (svg-gen.py) – omitted for brevity
#    (produces panel_1.svg … panel_4.svg)

# 3. Render panels to MP4 (kamishibai CLI)
node /home/bons/kamishibai/cli/render.js episode.json /tmp/panel_

# 4. Merge panels
python mcp/videogen/tui.py   # → choose “Merge Panels”

# 5. Add telop (telop skill)
node mcp/evops/skills/telop/bin/telop-cli.js \
  --input /tmp/merged.mp4 \
  --spec telop_spec.json \
  --output /tmp/teloped.mp4

# 6. Compose final video with audio
python mcp/videogen/tui.py   # → choose “Compose Video”
```

Now you have a fully decoupled video generation workflow where each step can be run, monitored, and replaced independently.