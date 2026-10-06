"""SQLite MCP server for the visual evaluation loop.

Provides structured storage for generated items, parameters, evaluations,
human feedback, and intent vectors.

Run:
    python mcp/db/server.py

Then query via HTTP:
    curl -X POST http://localhost:8001/call \
      -H "Content-Type: application/json" \
      -d '{"name":"save_record","arguments":{"table":"experiments","record":{"name":"test","task_context":"image","intent_text":"cute character"}}}'
"""
from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

DB_PATH = Path(__file__).resolve().parent / "sotsusei.db"

mcp = FastMCP("sotsusei-db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    task_context TEXT,
    intent_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER REFERENCES experiments(id),
    param_json TEXT,
    prompt_text TEXT,
    tool_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS generated_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parameter_id INTEGER REFERENCES parameters(id),
    file_path TEXT,
    item_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auto_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES generated_items(id),
    evaluator_name TEXT,
    axis_name TEXT,
    score REAL,
    raw_output TEXT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS human_evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES generated_items(id),
    overall_score INTEGER,
    axis_scores TEXT,
    comment TEXT,
    evaluator_id TEXT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pairwise_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_a_id INTEGER REFERENCES generated_items(id),
    item_b_id INTEGER REFERENCES generated_items(id),
    winner_id TEXT,
    reason TEXT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER REFERENCES generated_items(id),
    failure_description TEXT,
    repair_instruction TEXT,
    next_parameters TEXT
);

CREATE TABLE IF NOT EXISTS intent_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER REFERENCES experiments(id),
    vector_json TEXT,
    hypothesis TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def _init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def _serialize(value: Any) -> str:
    if isinstance(value, str):
        try:
            json.loads(value)
            return value
        except json.JSONDecodeError:
            return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)


@mcp.tool()
def init_schema() -> dict[str, Any]:
    """Initialize all tables. Safe to call multiple times."""
    _init_db()
    return {"status": "ok", "db_path": str(DB_PATH)}


@mcp.tool()
def save_record(table: str, record: dict[str, Any]) -> dict[str, Any]:
    """Insert a record into a table. JSON fields are serialized automatically."""
    _init_db()
    # Auto-serialize known JSON columns
    json_cols = {
        "param_json",
        "axis_scores",
        "next_parameters",
        "vector_json",
        "raw_output",
    }
    record = {
        k: _serialize(v) if k in json_cols and not isinstance(v, str) else v
        for k, v in record.items()
    }
    cols = list(record.keys())
    vals = list(record.values())
    placeholders = ",".join("?" for _ in cols)
    sql = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql, vals)
        conn.commit()
        return {"status": "ok", "id": cur.lastrowid, "table": table}


@mcp.tool()
def query_records(
    table: str,
    filters: dict[str, Any] | None = None,
    order_by: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Query records from a table with optional filters."""
    _init_db()
    filters = filters or {}
    where_clauses = []
    params = []
    for k, v in filters.items():
        where_clauses.append(f"{k} = ?")
        params.append(v)
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    order_sql = f"ORDER BY {order_by}" if order_by else ""
    sql = f"SELECT * FROM {table} {where_sql} {order_sql} LIMIT ?"
    params.append(limit)
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]


@mcp.tool()
def execute_sql(sql: str, params: list[Any] | None = None) -> dict[str, Any]:
    """Execute arbitrary SELECT/INSERT/UPDATE/DELETE SQL. Use with care."""
    _init_db()
    params = params or []
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql, params)
        conn.commit()
        if sql.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            return {"status": "ok", "rows": [dict(r) for r in rows]}
        return {"status": "ok", "rowcount": cur.rowcount, "lastrowid": cur.lastrowid}


@mcp.tool()
def get_tables() -> list[str]:
    """List all tables in the database."""
    _init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [r[0] for r in cur.fetchall()]


@mcp.tool()
def get_recent_evaluations(limit: int = 10) -> list[dict[str, Any]]:
    """Get recent items with their auto and human scores joined."""
    _init_db()
    sql = """
    SELECT
        gi.id AS item_id,
        gi.file_path,
        p.prompt_text,
        ae.evaluator_name,
        ae.axis_name,
        ae.score AS auto_score,
        he.overall_score AS human_score,
        he.comment,
        gi.created_at
    FROM generated_items gi
    LEFT JOIN parameters p ON gi.parameter_id = p.id
    LEFT JOIN auto_evaluations ae ON ae.item_id = gi.id
    LEFT JOIN human_evaluations he ON he.item_id = gi.id
    ORDER BY gi.created_at DESC
    LIMIT ?
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, (limit,)).fetchall()
        return [dict(r) for r in rows]


if __name__ == "__main__":
    _init_db()
    # stdio is the standard MCP transport; clients connect via MCP client SDK.
    mcp.run(transport="stdio")
