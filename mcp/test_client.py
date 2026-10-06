"""Simple stdio MCP client for testing the sotsusei MCP servers.

Usage:
    python mcp/test_client.py mcp/db/server.py
    python mcp/test_client.py mcp/evaluator/server.py
    python mcp/test_client.py mcp/blender-bpy/server.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(server_script: str):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(server_script).resolve())],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description[:60]}...")

            # Call capabilities / list if available
            if any(t.name == "list_capabilities" for t in tools.tools):
                result = await session.call_tool(
                    "list_capabilities", arguments={}
                )
                print("\nCapabilities:")
                for c in result.content:
                    if hasattr(c, "text"):
                        print(c.text)

            # DB smoke test
            if server_script.endswith("db/server.py"):
                result = await session.call_tool(
                    "save_record",
                    arguments={
                        "table": "experiments",
                        "record": {
                            "name": "smoke_test",
                            "task_context": "image",
                            "intent_text": "cute character",
                        },
                    },
                )
                print("\nDB save result:")
                for c in result.content:
                    print(c.text)

            # Evaluator smoke test (no image required for capabilities)
            if server_script.endswith("evaluator/server.py"):
                print("\nEvaluator smoke: capabilities listed above")

            # Blender smoke test
            if server_script.endswith("blender-bpy/server.py"):
                print("\nBlender smoke: capabilities listed above")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path/to/server.py>")
        sys.exit(1)
    asyncio.run(run(sys.argv[1]))
