from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")
import argparse
import json
from pathlib import Path
from typing import Any

# ── Storyboard Engine ──────────────────────────────────────────

def load_episode(episode_path: str) -> dict:
    with open(episode_path, "r", encoding="utf-8") as f:
        return json.load(f)

def plan_cuts(episode: dict, paper_id: str = "UNKNOWN", default_duration: float = 5.0) -> list[dict]:
    """episode.json → cut sheet (カット割り)"""
    cuts = []
    panels = episode.get("panels", [])
    for i, panel in enumerate(panels):
        cuts.append({
            "cut_id": f"{paper_id}_cut_{i+1:02d}",
            "panel_index": i,
            "text": panel.get("text", ""),
            "speaker": panel.get("speaker", ""),
            "role": panel.get("role", ""),
            "duration_sec": default_duration,
            "required_assets": {
                "svg": f"{paper_id}_panel_{i+1:02d}.svg",
                "png": f"{paper_id}_panel_{i+1:02d}.png",
                "voice": f"{paper_id}_voice_{i+1:02d}.mp3"
            }
        })
    return cuts

def export_timeline(cuts: list[dict], fps: int = 30) -> dict:
    """カット割り → 簡易タイムライン (OTIO-like JSON)"""
    timeline = {
        "format": "evops-timeline-v1",
        "fps": fps,
        "tracks": [
            {
                "name": "video",
                "kind": "Video",
                "clips": []
            },
            {
                "name": "audio",
                "kind": "Audio",
                "clips": []
            },
            {
                "name": "subtitle",
                "kind": "Subtitle",
                "clips": []
            }
        ]
    }
    current_time = 0.0
    for cut in cuts:
        duration = cut["duration_sec"]
        timeline["tracks"][0]["clips"].append({
            "cut_id": cut["cut_id"],
            "start_time": current_time,
            "duration": duration,
            "source": cut["required_assets"]["png"],
            "type": "image"
        })
        timeline["tracks"][1]["clips"].append({
            "cut_id": cut["cut_id"],
            "start_time": current_time,
            "duration": duration,
            "source": cut["required_assets"]["voice"],
            "type": "audio"
        })
        timeline["tracks"][2]["clips"].append({
            "cut_id": cut["cut_id"],
            "start_time": current_time,
            "duration": duration,
            "text": cut["text"],
            "type": "subtitle"
        })
        current_time += duration
    timeline["total_duration"] = current_time
    return timeline

def generate_ffmpeg_command(timeline: dict, output_dir: str, output_file: str) -> str:
    """タイムラインから ffmpeg コマンドを生成"""
    # Simplified: assumes all panels are same size and concat can be used
    # Real implementation would be more complex
    return f"# ffmpeg command generated from {len(timeline['tracks'][0]['clips'])} cuts\n# Use videogen skill for actual muxing"

# ── MCP / HTTP Server ──────────────────────────────────────────

def run_stdio():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("storyboard")

    @mcp.tool()
    def load_episode_tool(episode_path: str) -> dict:
        return load_episode(episode_path)

    @mcp.tool()
    def plan_cuts_tool(episode_path: str, paper_id: str = "UNKNOWN", default_duration: float = 5.0) -> dict:
        ep = load_episode(episode_path)
        cuts = plan_cuts(ep, paper_id, default_duration)
        return {"cuts": cuts, "total_panels": len(cuts)}

    @mcp.tool()
    def export_timeline_tool(episode_path: str, paper_id: str = "UNKNOWN", default_duration: float = 5.0, fps: int = 30) -> dict:
        ep = load_episode(episode_path)
        cuts = plan_cuts(ep, paper_id, default_duration)
        timeline = export_timeline(cuts, fps)
        return {"timeline": timeline, "total_duration": timeline["total_duration"]}

    @mcp.tool()
    def generate_ffmpeg_cmd_tool(episode_path: str, output_dir: str, output_file: str) -> dict:
        ep = load_episode(episode_path)
        cuts = plan_cuts(ep)
        timeline = export_timeline(cuts)
        cmd = generate_ffmpeg_command(timeline, output_dir, output_file)
        return {"command": cmd, "timeline": timeline}

    mcp.run(transport="stdio")

def run_http(port: int = 8009):
    from fastapi import FastAPI, Body
    import uvicorn

    app = FastAPI(title="storyboard", version="1.0.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "storyboard"}

    @app.post("/call")
    def call_tool(body: dict = Body(...)):
        name = body.get("name")
        args = body.get("arguments", {})
        if name == "load_episode_tool":
            return load_episode(**args)
        elif name == "plan_cuts_tool":
            ep = load_episode(args["episode_path"])
            cuts = plan_cuts(ep, args.get("paper_id", "UNKNOWN"), args.get("default_duration", 5.0))
            return {"cuts": cuts, "total_panels": len(cuts)}
        elif name == "export_timeline_tool":
            ep = load_episode(args["episode_path"])
            cuts = plan_cuts(ep, args.get("paper_id", "UNKNOWN"), args.get("default_duration", 5.0))
            timeline = export_timeline(cuts, args.get("fps", 30))
            return {"timeline": timeline, "total_duration": timeline["total_duration"]}
        else:
            return {"status": "error", "message": f"Unknown tool: {name}"}

    @app.post("/mcp/call")
    def mcp_call_tool(body: dict = Body(...)):
        return call_tool(body)

    @app.get("/ready")
    def ready():
        return {"status": "ok", "tools": ["load_episode_tool", "plan_cuts_tool", "export_timeline_tool"]}

    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8009)
    parser.add_argument("--stdio", action="store_true")
    args = parser.parse_args()
    if args.http:
        run_http(port=args.port)
    else:
        run_stdio()
