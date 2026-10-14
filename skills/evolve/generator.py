#!/usr/bin/env python3
"""Blender character render invocation."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skills.cli_mcp.config import EVOPS_ROOT, CONCEPTS


def render(concept: str, generation_id: str, output_dir: Path, **flags) -> Path:
    """Render a concept using the matching bpy-gen script."""
    out_path = output_dir / f"gen_{generation_id}.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    script = EVOPS_ROOT / CONCEPTS[concept]["script"]
    cmd = ["blender", "--background", "--python", str(script), "--",
           "--output", str(out_path)]

    for k, v in flags.items():
        if v:
            cmd.append(f"--{k.replace('_', '-')}")

    print(f"[GEN] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"[GEN] Error: {result.stderr[:500]}")
    else:
        print(f"[GEN] Saved: {out_path}")
    return out_path
