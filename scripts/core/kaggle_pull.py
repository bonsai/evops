#!/usr/bin/env python3
"""
Kaggle Pull — Download evaluation results from Kaggle and merge into sotsusei.db
Usage:
    python3 kaggle_pull.py --kernel evops-clip-eval --output outputs/papers/S01/kaggle_scores.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/bons/evops")


def download_results(kernel_name: str, output_path: Path) -> Path:
    """Stub: Download Kaggle notebook output."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # In production: use kaggle.api.kaggle_api.download_output
    print(f"[KAGGLE PULL] Would download from kernel: {kernel_name}")
    print(f"[KAGGLE PULL] Output: {output_path}")
    return output_path


def merge_to_db(csv_path: Path, concept: str, paper_id: str) -> int:
    """Merge Kaggle scores into sotsusei.db eval_kaggle table."""
    import sqlite3
    db_path = Path("/home/bons/evops/mcp_core/db/sotsusei.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eval_kaggle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concept TEXT,
            paper_id TEXT,
            frame TEXT,
            clip_score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    count = 0
    if csv_path.exists():
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO eval_kaggle (concept, paper_id, frame, clip_score) VALUES (?, ?, ?, ?)",
                    (concept, paper_id, row.get("frame", ""), float(row.get("clip_score", 0)))
                )
                count += 1

    conn.commit()
    conn.close()
    print(f"[KAGGLE PULL] Merged {count} scores into eval_kaggle")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", type=str, default="evops-clip-eval")
    parser.add_argument("--output", type=Path, default=Path("outputs/kaggle_results/scores.csv"))
    parser.add_argument("--concept", type=str, default="donpen")
    parser.add_argument("--paper-id", type=str, default="S01")
    args = parser.parse_args()

    csv_path = download_results(args.kernel, args.output)
    merge_to_db(csv_path, args.concept, args.paper_id)