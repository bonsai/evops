#!/usr/bin/env python3
"""bpy-gen generation ledger — linked to evops MCP SQLite database.

Uses the main evops database at /home/bons/evops/mcp/db/sotsusei.db
instead of an isolated ~/.db/bpy_gen.db.
This ensures the generation lineage is part of the shared experiment DB.
"""
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

# Main evops MCP database path (shared across all services)
DB_PATH = Path("/home/bons/evops/mcp/db/sotsusei.db")

# Also maintain a JSONL ledger for quick audit (optional)
LEDGER = Path.home() / "bpy-gen" / "outputs" / ".ledger.jsonl"


def init():
    """Initialize the main evops database with required tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
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
        CREATE TABLE IF NOT EXISTS generated_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter_id INTEGER REFERENCES parameters(id),
            file_path TEXT,
            item_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        -- bpy-gen lineage tables
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script_name TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            content_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            prompt TEXT,
            parent_id INTEGER REFERENCES generations(id),
            git_commit TEXT,
            file_path TEXT NOT NULL,
            UNIQUE(script_name, version)
        );
        CREATE TABLE IF NOT EXISTS renders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_id INTEGER NOT NULL REFERENCES generations(id),
            output_path TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT DEFAULT 'ok',
            engine TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_gen_name ON generations(script_name);
        CREATE INDEX IF NOT EXISTS idx_gen_parent ON generations(parent_id);
        """)
        conn.commit()


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _git_commit() -> str | None:
    import subprocess
    try:
        return (
            subprocess.check_output(
                ["git", "-C", "/home/bons/evops/mcp/bpy-gen"], "rev-parse", "--short", "HEAD"
            )
            .decode()
            .strip()
        )
    except Exception:
        return None


def bake(script_path: Path, prompt: str | None = None, parent_id: int | None = None):
    """Bake a script generation into the database.
    Returns (generation_id, version).
    """
    init()
    name = script_path.stem.replace("_bpy", "")
    content_hash = _hash(script_path)
    ts = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        # detect if same hash already exists
        row = conn.execute(
            "SELECT id, version FROM generations WHERE script_name=? AND content_hash=?",
            (name, content_hash),
        ).fetchone()
        if row:
            return row[0], row[1]  # existing id, version

        max_v = conn.execute(
            "SELECT COALESCE(MAX(version), 0) FROM generations WHERE script_name=?",
            (name,),
        ).fetchone()[0]
        version = max_v + 1

        cur = conn.execute(
            """INSERT INTO generations(script_name, version, content_hash, created_at,
                                        prompt, parent_id, git_commit, file_path)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                name,
                version,
                content_hash,
                ts,
                prompt,
                parent_id,
                _git_commit(),
                str(script_path),
            ),
        )
        conn.commit()
        return cur.lastrowid, version


def log_render(generation_id: int, output_path: Path, engine: str = "WORKBENCH"):
    """Log a render output linked to a generation."""
    init()
    ts = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO renders(generation_id, output_path, timestamp, engine) VALUES (?,?,?,?)",
            (generation_id, str(output_path), ts, engine),
        )
        conn.commit()

    # Also append to JSONL ledger for quick audit
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": ts,
        "generation_id": generation_id,
        "output": str(output_path),
        "status": "ok",
        "engine": engine,
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def list_generations(script_name: str | None = None):
    """List generations, optionally filtered by script name."""
    init()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        if script_name:
            rows = conn.execute(
                "SELECT * FROM generations WHERE script_name=? ORDER BY version",
                (script_name,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM generations ORDER BY script_name, version"
            ).fetchall()
        return [dict(r) for r in rows]


def tree(script_name: str):
    """Return generational tree as nested dict."""
    gens = list_generations(script_name)
    by_id = {g["id"]: g for g in gens}
    roots = [g for g in gens if g["parent_id"] is None]

    def _children(pid):
        return [_attach(c) for c in gens if c["parent_id"] == pid]

    def _attach(g):
        node = dict(g)
        node["children"] = _children(g["id"])
        return node

    return [_attach(r) for r in roots]


def main():
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"
    if cmd == "init":
        init()
        print(f"DB ready: {DB_PATH}")
    elif cmd == "bake":
        path = Path(sys.argv[2])
        gid, ver = bake(path)
        print(f"Baked: {path.stem} v{ver} (gen_id={gid})")
    elif cmd == "list":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        for g in list_generations(name):
            print(f"  {g['script_name']:20s} v{g['version']:3d}  {g['content_hash']}  {g['created_at']}")
    elif cmd == "log_render":
        # usage: db.py log_render <generation_id> <output_path> [engine]
        gen_id = int(sys.argv[2])
        out = Path(sys.argv[3])
        engine = sys.argv[4] if len(sys.argv) > 4 else "WORKBENCH"
        log_render(gen_id, out, engine)
        print(f"Logged render: gen_id={gen_id} -> {out}")
    elif cmd == "tree":
        import json as _json
        print(_json.dumps(tree(sys.argv[2]), indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()