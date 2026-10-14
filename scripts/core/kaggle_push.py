#!/usr/bin/env python3
"""
Kaggle Push — Upload evaluation artifacts to Kaggle Dataset
Usage:
    python3 kaggle_push.py --input outputs/papers/S01/final.mp4 --concept donpen --paper-id S01
"""
from __future__ import annotations

import argparse
import zipfile
import sys
from pathlib import Path

sys.path.insert(0, "/home/bons/evops")


def create_zip(input_path: Path, concept: str, paper_id: str, output_zip: Path) -> Path:
    """Create zip archive for Kaggle dataset upload."""
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w") as zf:
        if input_path.is_dir():
            for file in input_path.rglob("*"):
                if file.is_file():
                    zf.write(file, arcname=f"{paper_id}/{file.name}")
        else:
            zf.write(input_path, arcname=f"{paper_id}/{input_path.name}")
    print(f"[KAGGLE PUSH] Created: {output_zip} ({output_zip.stat().st_size} bytes)")
    return output_zip


def upload_to_kaggle(zip_path: Path, dataset_name: str = "evops-eval"):
    """Stub: Upload dataset to Kaggle (requires Kaggle API token)."""
    import subprocess
    print(f"[KAGGLE PUSH] Uploading to dataset: {dataset_name}")
    # Stub: in production, use kaggle.api.dataset_create_new or similar
    print(f"[KAGGLE PUSH] Would run: kaggle datasets version -m 'eval {dataset_name}'")
    print(f"[KAGGLE PUSH] Dataset: {dataset_name}, File: {zip_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Input file or directory")
    parser.add_argument("--concept", type=str, default="donpen")
    parser.add_argument("--paper-id", type=str, default="S01")
    parser.add_argument("--output", type=Path, default=Path("outputs/kaggle_input/evops_input.zip"))
    parser.add_argument("--dataset", type=str, default="evops-eval")
    args = parser.parse_args()

    zip_path = create_zip(args.input, args.concept, args.paper_id, args.output)
    upload_to_kaggle(zip_path, args.dataset)
