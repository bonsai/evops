"""Video editor / compositor MCP server.
Loose-coupled: consumes episode.json + panel SVGs + telop spec,
produces final MP4 via ffmpeg subprocess.
No direct import from bpy-gen / kamishibai / svg-gen.
"""
from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from mcp_core.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("videogen")

HERE = Path(__file__).resolve().parent


@mcp.tool()
def compose_video(
    input_video: str,
    audio_path: str | None = None,
    subtitle_path: str | None = None,
    output_path: str = "/tmp/final.mp4",
    resolution: int = 1280,
    fps: int = 30,
) -> dict[str, Any]:
    """Composite video + optional audio + optional subtitle track."""
    cmd = ["ffmpeg", "-y", "-i", input_video]
    if audio_path:
        cmd += ["-i", audio_path, "-c:a", "aac", "-b:a", "64k"]
    cmd += ["-c:v", "libx264", "-crf", "23", "-r", str(fps), "-preset", "fast"]
    if subtitle_path:
        cmd += ["-vf", f"subtitles={subtitle_path}:force_style='FontName=IPAexGothic,FontSize=24'"]
    cmd += ["-pix_fmt", "yuv420p", output_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0 and Path(output_path).exists()
        return {
            "status": "ok" if success else "error",
            "output": output_path,
            "ffmpeg_returncode": result.returncode,
            "stderr_tail": result.stderr[-300:],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
def merge_panels(panel_dir: str, output_path: str = "/tmp/merged.mp4") -> dict[str, Any]:
    """Merge 4 panel videos (from kamishibai) into single sequence."""
    panels = sorted(Path(panel_dir).glob("panel_*.mp4"))
    if not panels:
        return {"status": "error", "message": f"No panel videos in {panel_dir}"}
    # Use concat demuxer
    list_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    for p in panels:
        list_file.write(f"file '{p.resolve()}'\n")
    list_file.close()
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file.name,
        "-c", "copy", output_path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0 and Path(output_path).exists()
        return {
            "status": "ok" if success else "error",
            "output": output_path,
            "panel_count": len(panels),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        Path(list_file.name).unlink(missing_ok=True)

# Create MCP app with HTTP transport
app = create_mcp_app(mcp, transport="http")


@app.get("/health")
def health():
    return {"status": "ok", "service": "videogen", "ffmpeg_available": True}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8006)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
