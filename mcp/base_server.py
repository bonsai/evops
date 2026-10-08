"""Base template for FastMCP + FastAPI unified MCP servers.

Provides a common pattern for all sotsusei MCP services:
1. FastMCP tools for MCP-protocol clients
2. FastAPI-mounted HTTP endpoint for REST clients
3. Health/readiness probes
4. Unified logging and error handling

Usage (per service):
    from base_server import create_mcp_app
    from fastmcp import FastMCP

    mcp = FastMCP("my-service")

    @mcp.tool()
    def my_tool(...) -> dict: ...

    app = create_mcp_app(mcp, port=8001)
    # Then: uvicorn my_module:app --port 8001
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI
from fastmcp import FastMCP

logger = logging.getLogger("evops.mcp")


def create_mcp_app(
    mcp: FastMCP,
    *,
    transport: str = "http",
    path: str = "/",
    cors_origins: list[str] | None = None,
) -> FastAPI:
    """Create a FastAPI app that mounts the given FastMCP instance.

    Args:
        mcp: Configured FastMCP instance with tools already registered.
        transport: One of "http", "streamable-http", "sse".
        path: Mount path for the MCP endpoint.
        cors_origins: Optional list of allowed CORS origins.

    Returns:
        FastAPI ASGI application.
    """
    app = FastAPI(
        title=mcp.name,
        description=f"MCP server: {mcp.name}",
        version=getattr(mcp, "version", "0.1.0"),
    )

    # CORS
    if cors_origins:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Health endpoints (outside MCP scope, pure FastAPI)
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": mcp.name}

    @app.get("/ready")
    def ready() -> dict[str, Any]:
        caps = {}
        try:
            caps = {
                "tools": [t.name for t in mcp.list_tools()],
            }
        except Exception:
            pass
        return {"status": "ok", "service": mcp.name, "capabilities": caps}

    # Mount the MCP Starlette app under /mcp
    # http_app() returns Starlette, which FastAPI can mount
    mcp_starlette = mcp.http_app(
        path=path,
        transport=transport,  # type: ignore[arg-type]
    )
    app.mount("/mcp", mcp_starlette)

    logger.info(f"MCP server '{mcp.name}' mounted at /mcp with transport={transport}")
    return app


def run_mcp_server(
    mcp: FastMCP,
    port: int = 8000,
    transport: str = "http",
) -> None:
    """Run a standalone MCP server (FastAPI + uvicorn).

    For simple cases where a single file owns both mcp and app.
    """
    import uvicorn

    app = create_mcp_app(mcp, transport=transport)
    uvicorn.run(app, host="0.0.0.0", port=port)
