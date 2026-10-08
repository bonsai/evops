"""SF paper comic MCP server with FastAPI integration.

Paper -> four-panel SF storyboard -> SVG animation metadata.
"""
from __future__ import annotations

import argparse
from typing import Any

from fastmcp import FastMCP
from mcp.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("sf-paper-comic")


@mcp.tool()
def make_episode(
    paper_id: str,
    title: str,
    hook: str,
    panel1: str,
    panel2: str,
    panel3: str,
    panel4: str,
) -> dict[str, Any]:
    """Create a four-panel SF paper episode specification."""
    return {
        "id": paper_id,
        "title": title,
        "format": "SF-4koma",
        "duration": "45-90s",
        "panels": [
            {"no": 1, "role": "problem", "text": panel1},
            {"no": 2, "role": "anomaly", "text": panel2},
            {"no": 3, "role": "invention", "text": panel3},
            {"no": 4, "role": "research-connection", "text": panel4},
        ],
        "visual": {"theme": "SF research lab", "accent": "#7c3aed"},
        "animation": {"sequence": [1, 2, 3, 4], "transition": "cut"},
    }


@mcp.tool()
def make_timeline(duration: int = 60) -> dict[str, Any]:
    """Return a default four-panel timing plan in seconds."""
    duration = max(45, min(duration, 90))
    intro = 4
    outro = 6
    panel_time = (duration - intro - outro) / 4
    return {
        "duration": duration,
        "intro": [0, intro],
        "panels": [
            [intro + panel_time * i, intro + panel_time * (i + 1)]
            for i in range(4)
        ],
        "outro": [duration - outro, duration],
    }


app = create_mcp_app(mcp, transport="http")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8004)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
