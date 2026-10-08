"""Unified MCP Gateway: mounts all sotsusei MCP services under one FastAPI app.

Each service remains independently runnable. The gateway composes them
to provide a single HTTP entrypoint with namespaced tool routing.

Run:
    python mcp/gateway/server.py --port 8000

Endpoints:
    /health          — gateway health
    /mcp/{service}   — individual MCP service endpoint
    /mcp/tools       — aggregated tool listing (all services)
"""
from __future__ import annotations

import argparse
from typing import Any

from fastapi import FastAPI
from fastmcp import FastMCP

# Import individual MCP instances (lightweight; no heavy models loaded unless tools called)
from mcp.blender_bpy.server import mcp as blender_mcp
from mcp.db.server import mcp as db_mcp
from mcp.evaluator.server import mcp as eval_mcp
from mcp.sf_paper_comic.server import mcp as comic_mcp

# Build composite MCP
gateway_mcp = FastMCP("evops-gateway")

# Mount each sub-service under its own namespace
gateway_mcp.mount(blender_mcp, namespace="blender")
gateway_mcp.mount(db_mcp, namespace="db")
gateway_mcp.mount(eval_mcp, namespace="evaluator")
gateway_mcp.mount(comic_mcp, namespace="comic")

# FastAPI app with composite MCP
app = FastAPI(title="EvOps MCP Gateway", description="Unified gateway for sotsusei MCP services")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "gateway": "evops-gateway"}


@app.get("/ready")
def ready() -> dict[str, Any]:
    try:
        all_tools = gateway_mcp.list_tools()
        return {
            "status": "ok",
            "tools_count": len(all_tools),
            "namespaces": ["blender", "db", "evaluator", "comic"],
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Mount composite MCP HTTP app
mcp_starlette = gateway_mcp.http_app(path="/", transport="http")
app.mount("/mcp", mcp_starlette)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=args.port)
