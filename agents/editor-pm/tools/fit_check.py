#!/usr/bin/env python3
"""Deterministic gate: the rendered page must fit A4 landscape at 96dpi.

The VLM can only guess whether content is cut off; this measures it. The page
is rendered into a deliberately tall window, then the bounding box of non-white
pixels is compared with the A4 frame (1123 x 794 CSS px). Anything beyond the
frame is what a print would clip.

Usage:
    python3 page-tests/fit_check.py <page_id>
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
A4_W, A4_H = 1123, 794          # 297mm x 210mm at 96dpi
PROBE_H = 4000                   # room to see the overflow
DRIVERS = ("google-chrome", "chromium", "microsoft-edge", "chromium-browser")


def driver() -> str:
    for name in DRIVERS:
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("no headless browser found: " + ", ".join(DRIVERS))


def main() -> None:
    page_id = sys.argv[1]
    render = HERE / page_id / "render"
    page_html = render / "page.html"
    probe = render / "fit_probe.png"

    subprocess.run(
        [
            driver(),
            "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--user-data-dir=/tmp/chrome-pqg",
            f"--window-size={A4_W},{PROBE_H}",
            f"--screenshot={probe}",
            f"file://{page_html}",
        ],
        check=True,
        capture_output=True,
    )

    a = np.asarray(Image.open(probe).convert("RGB"))
    ink = (a < 250).any(axis=2)
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if not len(rows):
        raise SystemExit("nothing was drawn")

    top, bottom = int(rows[0]), int(rows[-1]) + 1
    left, right = int(cols[0]), int(cols[-1]) + 1
    out = {
        "page_id": page_id,
        "frame": {"w": A4_W, "h": A4_H},
        "content": {"top": top, "bottom": bottom, "left": left, "right": right,
                    "w": right - left, "h": bottom - top},
        "overflow": {"bottom": max(0, bottom - A4_H), "right": max(0, right - A4_W)},
    }
    out["fits"] = out["overflow"]["bottom"] == 0 and out["overflow"]["right"] == 0

    target = render / "fit_check.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verdict = "PASS" if out["fits"] else "FAIL"
    print(f"{verdict}  content {out['content']['w']}x{out['content']['h']} "
          f"in frame {A4_W}x{A4_H}"
          + ("" if out["fits"] else f"  overflow bottom={out['overflow']['bottom']}px right={out['overflow']['right']}px"))
    print(f"[saved] {target.relative_to(HERE.parent.parent.parent)}")


if __name__ == "__main__":
    main()
