"""Blender + SVG MCP server with FastAPI integration.

Provides:
- Parameterized SVG generation
- Blender headless rendering via subprocess
- Scene setup helpers

Run:
    python mcp/blender-bpy/server.py        # stdio mode
    python mcp/blender-bpy/server.py --http # HTTP mode on port 8003
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import svgwrite
from fastmcp import FastMCP

from mcp.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("sotsusei-blender-bpy")

HERE = Path(__file__).resolve().parent
DEFAULT_BLENDER = os.environ.get("BLENDER_EXECUTABLE", "blender")


@mcp.tool()
def generate_svg(
    output_path: str,
    width: int = 512,
    height: int = 512,
    shapes: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate an SVG file from a list of shape parameters."""
    shapes = shapes or []
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#ffffff"))
    shape_map = {
        "circle": dwg.circle,
        "rect": dwg.rect,
        "ellipse": dwg.ellipse,
        "polygon": dwg.polygon,
    }
    for s in shapes:
        t = s.pop("type", "circle")
        fn = shape_map.get(t, dwg.circle)
        try:
            dwg.add(fn(**s))
        except Exception:
            dwg.add(dwg.circle(cx=width / 2, cy=height / 2, r=10, fill="#cccccc"))
    dwg.save()
    return {"status": "ok", "output_path": output_path, "shape_count": len(shapes)}


@mcp.tool()
def generate_doraemon_svg(
    output_path: str,
    width: int = 512,
    height: int = 512,
    action: str = "standing",
) -> dict[str, Any]:
    """Generate a simple Doraemon-like character SVG (educational example)."""
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#f0f8ff"))
    cx, cy = width // 2, height // 2
    blue, red, yellow, white, black = "#1e90ff", "#ff0000", "#ffd700", "#ffffff", "#000000"

    # Body
    dwg.add(dwg.circle(center=(cx, cy + 20), r=90, fill=blue, stroke=black, stroke_width=2))
    dwg.add(dwg.circle(center=(cx, cy + 25), r=55, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx, cy + 45), rx=30, ry=18, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx, cy - 35), rx=55, ry=12, fill=red, stroke=black, stroke_width=1.5))
    dwg.add(dwg.circle(center=(cx, cy - 25), r=12, fill=yellow, stroke=black, stroke_width=1.5))

    # Head
    dwg.add(dwg.circle(center=(cx, cy - 90), r=70, fill=blue, stroke=black, stroke_width=2))
    dwg.add(dwg.circle(center=(cx, cy - 80), r=55, fill=white, stroke=black, stroke_width=1.5))

    # Eyes, nose, whiskers, mouth...
    for dx, dy in [(-18, -110), (18, -110)]:
        dwg.add(dwg.ellipse(center=(cx + dx, cy + dy), rx=14, ry=18, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.circle(center=(cx - 14, cy - 105), r=3, fill=black))
    dwg.add(dwg.circle(center=(cx + 14, cy - 105), r=3, fill=black))
    dwg.add(dwg.circle(center=(cx, cy - 95), r=10, fill=red, stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx, cy - 85), end=(cx, cy - 60), stroke=black, stroke_width=1.5))
    for dx in [-50, 50]:
        for dy in [-95, -80, -65]:
            end_x = cx + (20 if dx > 0 else -20)
            dwg.add(dwg.line(start=(cx + dx, cy + dy), end=(end_x, cy + dy + 5), stroke=black, stroke_width=1.5))
    dwg.add(dwg.path(d=f"M {cx - 30},{cy - 70} Q {cx},{cy - 40} {cx + 30},{cy - 70}", fill="none", stroke=black, stroke_width=2))

    # Arms & hands
    dwg.add(dwg.ellipse(center=(cx - 90, cy + 10), rx=15, ry=35, fill=blue, stroke=black, stroke_width=1.5, transform=f"rotate(30, {cx - 90}, {cy + 10})"))
    dwg.add(dwg.ellipse(center=(cx + 90, cy + 10), rx=15, ry=35, fill=blue, stroke=black, stroke_width=1.5, transform=f"rotate(-30, {cx + 90}, {cy + 10})"))
    dwg.add(dwg.circle(center=(cx - 115, cy - 15), r=15, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.circle(center=(cx + 115, cy - 15), r=15, fill=white, stroke=black, stroke_width=1.5))

    if action == "reading":
        dwg.add(dwg.rect(insert=(cx - 40, cy + 60), size=(80, 50), fill="#8b4513", stroke=black, stroke_width=1.5))
        dwg.add(dwg.rect(insert=(cx - 35, cy + 65), size=(70, 40), fill="#fff8dc", stroke=black, stroke_width=1))
    elif action == "flying":
        dwg.add(dwg.ellipse(center=(cx, cy - 175), rx=70, ry=8, fill="#deb887", stroke=black, stroke_width=1.5))

    # Feet
    dwg.add(dwg.ellipse(center=(cx - 40, cy + 105), rx=30, ry=15, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx + 40, cy + 105), rx=30, ry=15, fill=white, stroke=black, stroke_width=1.5))

    dwg.save()
    return {"status": "ok", "output_path": output_path, "width": width, "height": height, "action": action}


@mcp.tool()
def render_svg_with_blender(
    svg_path: str,
    output_path: str,
    blender_executable: str = DEFAULT_BLENDER,
    resolution: int = 512,
    samples: int = 32,
) -> dict[str, Any]:
    """Render an SVG as a PNG using Blender headless mode."""
    render_script = HERE / "render_in_blender.py"
    if not render_script.exists():
        return {"status": "error", "message": f"{render_script} not found"}

    cmd = [
        blender_executable, "--background", "--python", str(render_script),
        "--", svg_path, output_path, str(resolution), str(samples),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        success = result.returncode == 0 and Path(output_path).exists()
        return {
            "status": "ok" if success else "error",
            "output_path": output_path,
            "returncode": result.returncode,
            "stdout_tail": "\n".join(result.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(result.stderr.splitlines()[-20:]),
        }
    except FileNotFoundError:
        return {"status": "error", "message": f"Blender not found: {blender_executable}"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Blender render timed out"}


@mcp.tool()
def list_capabilities() -> dict[str, Any]:
    """List capabilities and check Blender availability."""
    blender_ok, version = False, None
    try:
        result = subprocess.run([DEFAULT_BLENDER, "--version"], capture_output=True, text=True, timeout=10)
        blender_ok = result.returncode == 0
        version = result.stdout.splitlines()[0] if blender_ok else None
    except Exception:
        pass
    return {
        "svg_generation": True,
        "blender_available": blender_ok,
        "blender_version": version,
        "blender_executable": DEFAULT_BLENDER,
    }


app = create_mcp_app(mcp, transport="http")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8003)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
