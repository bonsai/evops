#!/usr/bin/env python3
"""SQLite -> BQMLite Dataset JSON converter.

Usage:
  sqlite_to_dataset.py <db> <sql> <target> <out.json> [--name NAME]

Reads rows from a SQLite DB with a read-only connection, emits the
BQMLite Dataset shape:
  {"name": "...", "target": "<col>", "rows": [ {col: val, ...}, ... ]}

- `target` must be one of the selected columns and numeric for engines.
- Values come back as int / float / str / None from sqlite3.
"""
import argparse, json, sqlite3, sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("sql")
    ap.add_argument("target")
    ap.add_argument("out")
    ap.add_argument("--name", default=None)
    a = ap.parse_args()

    con = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    try:
        cur = con.execute(a.sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        if a.target not in cols:
            print(f"target {a.target!r} not in selected columns {cols}", file=sys.stderr)
            return 2
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        con.close()

    if not rows:
        print("query returned 0 rows", file=sys.stderr)
        return 3

    ds = {"name": a.name or a.out, "target": a.target, "rows": rows}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {a.out}: {len(rows)} rows, target={a.target}, cols={cols}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
