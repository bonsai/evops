#!/usr/bin/env python3
"""Append render metadata to JSONL ledger and evops database.

Links render to generation in the main evops MCP database.
Also maintains a local JSONL ledger for quick audit.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp.bpy_gen.tools.db import log_render as db_log_render

LEDGER = Path.home() / "bpy-gen" / "outputs" / ".ledger.jsonl"


def append(model: str, output: str, status: str, duration_sec: float | None = None):
    # Write to JSONL ledger (local audit trail)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "output": output,
        "status": status,
        "duration_sec": duration_sec,
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def link_to_db(generation_id: int, output_path: Path, engine: str = "WORKBENCH"):
    """Also link the render to the main evops database."""
    db_log_render(generation_id, output_path, engine)


if __name__ == "__main__":
    model = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    output = sys.argv[2] if len(sys.argv) > 2 else ""
    status = sys.argv[3] if len(sys.argv) > 3 else "ok"
    append(model, output, status)