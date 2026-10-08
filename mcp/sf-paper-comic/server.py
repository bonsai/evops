"""SF paper comic MCP server.

Paper -> four-panel SF storyboard -> SVG animation metadata.
The server is deliberately small: it prepares structured episode data;
rendering remains deterministic and can be handled by SVG/HTML tooling.
"""

from mcp.server.fastmcp import FastMCP

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
) -> dict:
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
def make_timeline(duration: int = 60) -> dict:
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


if __name__ == "__main__":
    mcp.run()
