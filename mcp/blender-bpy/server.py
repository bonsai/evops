"""Blender + SVG MCP server.

Provides:
- Parameterized SVG generation
- Blender headless rendering via subprocess
- Scene setup helpers

Run:
    python mcp/blender-bpy/server.py

This server does NOT run inside Blender's Python; it shells out to
`blender --background --python render_script.py` for rendering.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import svgwrite
from fastmcp import FastMCP

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
    """Generate an SVG file from a list of shape parameters.

    shapes example:
        [
          {"type": "circle", "cx": 256, "cy": 256, "r": 100, "fill": "#ff5555"},
          {"type": "rect", "x": 100, "y": 100, "width": 200, "height": 200, "fill": "#55ff55"}
        ]
    """
    shapes = shapes or []
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#ffffff"))

    for s in shapes:
        t = s.pop("type", "circle")
        if t == "circle":
            dwg.add(dwg.circle(**s))
        elif t == "rect":
            dwg.add(dwg.rect(**s))
        elif t == "ellipse":
            dwg.add(dwg.ellipse(**s))
        elif t == "polygon":
            dwg.add(dwg.polygon(**s))
        else:
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
    """Generate a simple Doraemon-like character SVG (educational example).

    This is a geometric placeholder for character-structure evaluation.
    For production, replace with an original character to avoid copyright issues.

    action: "standing" | "reading" | "flying"
    """
    dwg = svgwrite.Drawing(output_path, size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#f0f8ff"))

    cx, cy = width // 2, height // 2
    body_r = 90
    head_r = 70
    blue = "#1e90ff"
    red = "#ff0000"
    yellow = "#ffd700"
    white = "#ffffff"
    black = "#000000"

    # Body
    dwg.add(dwg.circle(center=(cx, cy + 20), r=body_r, fill=blue, stroke=black, stroke_width=2))
    # Belly / pocket
    dwg.add(dwg.circle(center=(cx, cy + 25), r=55, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx, cy + 45), rx=30, ry=18, fill=white, stroke=black, stroke_width=1.5))
    # Collar
    dwg.add(dwg.ellipse(center=(cx, cy - 35), rx=55, ry=12, fill=red, stroke=black, stroke_width=1.5))
    # Bell
    dwg.add(dwg.circle(center=(cx, cy - 25), r=12, fill=yellow, stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx - 10, cy - 22), end=(cx + 10, cy - 22), stroke=black, stroke_width=1))
    dwg.add(dwg.circle(center=(cx, cy - 22), r=2, fill=black))

    # Head
    dwg.add(dwg.circle(center=(cx, cy - 90), r=head_r, fill=blue, stroke=black, stroke_width=2))
    # Face
    dwg.add(dwg.circle(center=(cx, cy - 80), r=55, fill=white, stroke=black, stroke_width=1.5))
    # Eyes
    dwg.add(dwg.ellipse(center=(cx - 18, cy - 110), rx=14, ry=18, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx + 18, cy - 110), rx=14, ry=18, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.circle(center=(cx - 14, cy - 105), r=3, fill=black))
    dwg.add(dwg.circle(center=(cx + 14, cy - 105), r=3, fill=black))
    # Nose
    dwg.add(dwg.circle(center=(cx, cy - 95), r=10, fill=red, stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx, cy - 85), end=(cx, cy - 60), stroke=black, stroke_width=1.5))
    # Whiskers
    for dx in (-35, -35, -35):
        pass
    dwg.add(dwg.line(start=(cx - 50, cy - 95), end=(cx - 20, cy - 90), stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx - 50, cy - 80), end=(cx - 20, cy - 80), stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx - 50, cy - 65), end=(cx - 20, cy - 70), stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx + 50, cy - 95), end=(cx + 20, cy - 90), stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx + 50, cy - 80), end=(cx + 20, cy - 80), stroke=black, stroke_width=1.5))
    dwg.add(dwg.line(start=(cx + 50, cy - 65), end=(cx + 20, cy - 70), stroke=black, stroke_width=1.5))

    # Mouth
    dwg.add(dwg.path(d=f"M {cx - 30},{cy - 70} Q {cx},{cy - 40} {cx + 30},{cy - 70}", fill="none", stroke=black, stroke_width=2))

    # Arms
    dwg.add(dwg.ellipse(center=(cx - 90, cy + 10), rx=15, ry=35, fill=blue, stroke=black, stroke_width=1.5, transform=f"rotate(30, {cx - 90}, {cy + 10})"))
    dwg.add(dwg.ellipse(center=(cx + 90, cy + 10), rx=15, ry=35, fill=blue, stroke=black, stroke_width=1.5, transform=f"rotate(-30, {cx + 90}, {cy + 10})"))
    # Hands
    dwg.add(dwg.circle(center=(cx - 115, cy - 15), r=15, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.circle(center=(cx + 115, cy - 15), r=15, fill=white, stroke=black, stroke_width=1.5))

    # Action-specific props
    if action == "reading":
        # Book in front
        dwg.add(dwg.rect(insert=(cx - 40, cy + 60), size=(80, 50), fill="#8b4513", stroke=black, stroke_width=1.5))
        dwg.add(dwg.rect(insert=(cx - 35, cy + 65), size=(70, 40), fill="#fff8dc", stroke=black, stroke_width=1))
    elif action == "flying":
        # Takecopter above head
        dwg.add(dwg.ellipse(center=(cx, cy - 175), rx=70, ry=8, fill="#deb887", stroke=black, stroke_width=1.5))
        dwg.add(dwg.rect(insert=(cx - 3, cy - 170), size=(6, 25), fill="#deb887", stroke=black, stroke_width=1))

    # Feet
    dwg.add(dwg.ellipse(center=(cx - 40, cy + 105), rx=30, ry=15, fill=white, stroke=black, stroke_width=1.5))
    dwg.add(dwg.ellipse(center=(cx + 40, cy + 105), rx=30, ry=15, fill=white, stroke=black, stroke_width=1.5))

    dwg.save()
    return {
        "status": "ok",
        "output_path": output_path,
        "width": width,
        "height": height,
        "action": action,
        "note": "Educational placeholder; use original characters in production.",
    }


@mcp.tool()
def render_svg_with_blender(
    svg_path: str,
    output_path: str,
    blender_executable: str = DEFAULT_BLENDER,
    resolution: int = 512,
    samples: int = 32,
) -> dict[str, Any]:
    """Render an SVG as a PNG using Blender headless mode.

    Requires Blender installed and available on PATH or via BLENDER_EXECUTABLE.
    """
    render_script = HERE / "render_in_blender.py"
    if not render_script.exists():
        return {
            "status": "error",
            "message": f"{render_script} not found. Please create the Blender render script.",
        }

    cmd = [
        blender_executable,
        "--background",
        "--python",
        str(render_script),
        "--",
        svg_path,
        output_path,
        str(resolution),
        str(samples),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        success = result.returncode == 0 and Path(output_path).exists()
        return {
            "status": "ok" if success else "error",
            "output_path": output_path,
            "returncode": result.returncode,
            "stdout_tail": "\n".join(result.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(result.stderr.splitlines()[-20:]),
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Blender not found: {blender_executable}",
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Blender render timed out"}


@mcp.tool()
def list_capabilities() -> dict[str, Any]:
    """List capabilities and check Blender availability."""
    blender_ok = False
    version = None
    try:
        result = subprocess.run(
            [DEFAULT_BLENDER, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        blender_ok = result.returncode == 0
        if blender_ok:
            version = result.stdout.splitlines()[0]
    except Exception:
        pass

    return {
        "svg_generation": True,
        "blender_available": blender_ok,
        "blender_version": version,
        "blender_executable": DEFAULT_BLENDER,
    }


if __name__ == "__main__":
    # stdio is the standard MCP transport; clients connect via MCP client SDK.
    mcp.run(transport="stdio")
