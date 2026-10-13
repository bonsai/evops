"""HTTP MCP client for testing sotsusei MCP servers.

Usage:
    # Server side (terminal 1)
    python mcp/db/server.py --http --port 8001

    # Client side (terminal 2)
    python mcp/test_client.py http://localhost:8001
"""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

import httpx


async def call_tool(base_url: str, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Call an MCP tool via HTTP POST to /mcp/tools/{tool_name}"""
    # fastmcp http_app() mounts tools at /tools/{name} under the mounted path
    url = f"{base_url.rstrip('/')}/mcp/tools/{name}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=arguments, timeout=30.0)
        resp.raise_for_status()
        return resp.json()


async def list_tools(base_url: str) -> list[str]:
    """List available MCP tools via HTTP GET."""
    url = f"{base_url.rstrip('/')}/mcp/tools"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        return [t.get("name") for t in data.get("tools", [])]


async def run(base_url: str):
    print(f"Connecting to {base_url}")

    tools = await list_tools(base_url)
    print(f"Tools ({len(tools)}): {', '.join(tools)}")

    # Health check via FastAPI (outside MCP)
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{base_url.rstrip('/')}/health")
        print(f"Health: {resp.json()}")

    # Service-specific smoke tests
    if any("save_record" in t for t in tools):
        result = await call_tool(base_url, "save_record", {
            "table": "experiments",
            "record": {"name": "smoke_test", "task_context": "image", "intent_text": "cute character"},
        })
        print(f"DB save: {json.dumps(result, indent=2)[:400]}")

    if any("evaluate_image" in t for t in tools):
        print("Evaluator: evaluate_image available (requires image_path)")

    if any("generate_svg" in t for t in tools):
        print("Blender: generate_svg available")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <http://host:port>")
        print("Example: python mcp/test_client.py http://localhost:8001")
        sys.exit(1)
    asyncio.run(run(sys.argv[1]))
