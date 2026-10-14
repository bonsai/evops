#!/usr/bin/env python3
"""
Evolve Skill MCP Server
Exposes generation→evaluation→evolution loop as an MCP tool.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("evolve-skill")


@mcp.tool()
def run_evolve_loop_tool(concept: str = "don_quixote", iterations: int = 5, target_score: int = 75) -> dict:
    """Run the generate→evaluate→evolve loop for a concept."""
    from skills.evolve.loop import run
    report = run(concept=concept, max_iterations=iterations, target_score=target_score)
    return {
        "concept": report["concept"],
        "final_score": report["final_score"],
        "converged": report["converged"],
        "iterations": len(report["iterations"]),
        "report_path": str(Path(report["iterations"][0]["generation_id"]).parent / f"{concept}_evolution_report.json") if report["iterations"] else None,
    }


@mcp.tool()
def list_supported_concepts_tool() -> list[str]:
    """List available character concepts."""
    from skills.cli_mcp.config import CONCEPTS
    return list(CONCEPTS.keys())


if __name__ == "__main__":
    mcp.run(transport="stdio")
