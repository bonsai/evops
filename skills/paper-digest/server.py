from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")
sys.path.insert(0, "/home/bons/paper-survey-agent/src")
import argparse
import json
from pathlib import Path
from typing import Any

from survey_agent.digester.manager import EvOpsSurveyManager

manager = EvOpsSurveyManager()

def digest_paper(text: str, title: str = "Untitled Paper", domain: str = "comic") -> dict:
    res = manager.process_paper(text, title, domain)
    if "error" in res:
        return {"status": "error", "message": res["error"]}
    return {
        "status": "ok",
        "domain": res["domain"],
        "output": res["result"],
        "seed_json": res["digested_seed"]
    }

def list_domains() -> dict:
    return {
        "domains": list(manager.adapters.keys()),
        "description": "comic: 4コマ漫画, manzai: 漫才, note: 解説記事, youtube: 動画構成案"
    }

def run_stdio():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("paper-digest")

    @mcp.tool()
    def _digest_paper(text: str, title: str = "Untitled Paper", domain: str = "comic") -> dict:
        return digest_paper(text, title, domain)

    @mcp.tool()
    def _list_domains() -> dict:
        return list_domains()

    mcp.run(transport="stdio")

def run_http(port: int = 8008):
    from fastapi import FastAPI, Body
    import uvicorn

    app = FastAPI(title="paper-digest", version="1.0.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "paper-digest", "tools": ["digest_paper", "list_domains"]}

    def _call_tool(body: dict):
        tool_name = body.get("name")
        args = body.get("arguments", {})
        if tool_name == "digest_paper":
            return digest_paper(**args)
        elif tool_name == "list_domains":
            return list_domains()
        else:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}

    @app.post("/call")
    def call_tool(body: dict = Body(...)):
        return _call_tool(body)

    # Alias for compatibility with evops-mcp which uses /mcp/call for other servers
    @app.post("/mcp/call")
    def mcp_call_tool(body: dict = Body(...)):
        return _call_tool(body)

    @app.get("/ready")
    def ready():
        return {
            "status": "ok",
            "service": "paper-digest",
            "capabilities": {
                "tools": ["digest_paper", "list_domains"],
                "domains": list(manager.adapters.keys())
            }
        }

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8008)
    parser.add_argument("--stdio", action="store_true")
    args = parser.parse_args()
    if args.http:
        run_http(port=args.port)
    else:
        run_stdio()
