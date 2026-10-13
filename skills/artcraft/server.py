#!/usr/bin/env python3
"""Artcraft MCP server — Effect composition & editing for evops pipeline.

Provides tools to apply, compose, and edit visual effects (egg-shadow, zanzou,
rainbow afterimage, bpy, mediapipe) in a loosely-coupled manner.

Run:
    python mcp/artcraft/server.py        # stdio mode
    python mcp/artcraft/server.py --http # HTTP mode on port 8007
"""
from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from mcp.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("artcraft")
EFFECTS = {
    "egg-shadow": {
        "blender_script": "/home/bons/evops/skills/egg-shadow/blender/egg_shadow.py",
        "houdini_script": "/home/bons/evops/skills/egg-shadow/houdini/egg_shadow.py",
    },
    "zanzou": {
        "windows": "/mnt/c/Users/0501JP/zanzou/windows/main_tasks.py",
        "linux": "/mnt/c/Users/0501JP/zanzou/linux/main.py",
    },
    "bpy-render": {
        "engine": "blender",
    },
    "mediapipe-pose": {
        "engine": "mediapipe",
    },
}


def _run(cmd: list[str], timeout: int = 60) -> dict[str, Any]:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


@mcp.tool()
def list_effects() -> dict[str, Any]:
    """List available effects and their configurations."""
    return {"effects": EFFECTS}


@mcp.tool()
def apply_effect(
    effect: str,
    input_path: str,
    output_path: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply a named effect to an input file.

    Args:
        effect: one of egg-shadow, zanzou, bpy-render, mediapipe-pose
        input_path: source image/video path
        output_path: destination path
        params: effect-specific parameters
    """
    params = params or {}
    if effect == "egg-shadow":
        script = EFFECTS["egg-shadow"]["blender_script"]
        if not Path(script).exists():
            return {"status": "error", "message": f"script not found: {script}"}
        cmd = ["blender", "--background", "--python", script, "--", input_path, output_path]
        for k, v in params.items():
            cmd.extend([f"--{k}", str(v)])
        return _run(cmd, timeout=120)

    elif effect == "zanzou":
        script = EFFECTS["zanzou"]["linux"]
        if not Path(script).exists():
            return {"status": "error", "message": f"script not found: {script}"}
        cmd = ["python3", script, "--input", input_path, "--output", output_path, "--mode", params.get("mode", "rainbow")]
        return _run(cmd, timeout=120)

    elif effect == "bpy-render":
        return {"status": "error", "message": "bpy-render not yet implemented"}

    elif effect == "mediapipe-pose":
        return {"status": "error", "message": "mediapipe-pose not yet implemented"}

    return {"status": "error", "message": f"unknown effect: {effect}"}


@mcp.tool()
def compose_edit(
    base_video: str,
    effect_layers: list[dict[str, Any]],
    output_path: str,
    resolution: int = 1280,
    fps: int = 30,
) -> dict[str, Any]:
    """Compose a video edit by stacking effect layers on a base video.

    Args:
        base_video: source video path
        effect_layers: list of {"effect": str, "params": dict, "start": float, "end": float}
        output_path: final output path
        resolution: output width
        fps: output fps
    """
    # Build ffmpeg filter_complex or sequential processing
    # Simplified: concat with overlay
    layers_desc = json.dumps(effect_layers, ensure_ascii=False)
    return {
        "status": "ok",
        "output": output_path,
        "layers": len(effect_layers),
        "note": "Composition pipeline placeholder — implement ffmpeg filter_complex or blender VSE sequence",
        "base_video": base_video,
        "resolution": resolution,
        "fps": fps,
    }


app = create_mcp_app(mcp, transport="http")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8007)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
