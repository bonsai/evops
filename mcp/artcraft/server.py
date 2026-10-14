#!/usr/bin/env python3
"""
ArtCraft MCP — Crafting Apps (PhotoCraft / VectorCraft / FilmCraft / etc.)
Open-source Adobe alternatives (Rust-based) via MCP interface.
Integrates with Kaggle GPU evaluation and our pipeline.
"""
import sys, os, json, subprocess
sys.path.insert(0, "/home/bons/evops")
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("artcraft")
SKILL_DIR = Path("/home/bons/evops/skills/artcraft")
APPS_FILE = SKILL_DIR / "apps.json"

@mcp.tool()
def list_apps() -> dict:
    """List available ArtCraft open-source creative apps."""
    try:
        with open(APPS_FILE) as f:
            data = json.load(f)
    except:
        data = {"apps": [{"name":"PhotoCraft","adobe":"Photoshop","status":"Early alpha"}]}
    return {"status": "ok", "count": len(data.get("apps", [])), "apps": [a["name"] for a in data.get("apps", [])]}

@mcp.tool()
def get_app_info(app_name: str) -> dict:
    """Get details for a specific Crafting App."""
    try:
        with open(APPS_FILE) as f:
            data = json.load(f)
        for a in data.get("apps", []):
            if a["name"] == app_name:
                return {"status": "ok", "app": a}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    return {"status": "error", "message": f"App {app_name} not found"}

@mcp.tool()
def generate_image_artcraft(prompt: str, output_path: str = "/tmp/artcraft_output.png") -> dict:
    """Generate image using ArtCraft PhotoCraft pipeline (placeholder: uses current pipeline components)."""
    # Actual PhotoCraft usage would call its Rust binary or CLI
    # Here we document the integration point
    return {"status": "pending", "message": f"PhotoCraft image generation queued for '{prompt}'", "output_path": output_path, "pipeline": "photo-craft-rust-cli"}

@mcp.tool()
def compose_filmcraft(input_dir: str, output_path: str = "/tmp/filmcraft_final.mp4") -> dict:
    """Compose video using FilmCraft pipeline (placeholder for open-source video editing)."""
    # FilmCraft replaces Premiere / After Effects
    return {"status": "pending", "message": f"FilmCraft video composition queued from {input_dir}", "output_path": output_path, "pipeline": "film-craft-rust-cli"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8008)
    args = parser.parse_args()
    from mcp_core.base_server import create_mcp_app, run_mcp_server
    app = create_mcp_app(mcp, transport="http")
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
