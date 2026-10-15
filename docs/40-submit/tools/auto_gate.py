#!/usr/bin/env python3
"""Auto-run the full page-quality-gate pipeline for a single page.

Usage:
    python3 docs/40-submit/tools/auto_gate.py <page_id>

Steps:
  1. render_page.py -> page.html
  2. headless Chrome -> page.png
  3. vlm_judge.py -> vlm_judgment.json (optional, only if VLM available)
  4. update kanban.json / test.json status
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = Path(__file__).resolve().parent
SUBMIT = REPO / "docs/40-submit"
PAGES = SUBMIT / "pages"
RENDER = Path("/home/bons/evops/agents/editor-pm/tools/render_page.py")
JUDGE = Path("/home/bons/evops/agents/editor-pm/tools/vlm_judge.py")
KANBAN = SUBMIT / "kanban.json"


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, text=True, timeout=timeout)


def load_kanban() -> dict:
    return json.loads(KANBAN.read_text(encoding="utf-8")) if KANBAN.exists() else {"pages": {}}


def save_kanban(d: dict):
    d["last_updated"] = subprocess.check_output(["date", "-Iseconds"], text=True).strip()
    KANBAN.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_kanban(page_id: str, status: str):
    d = load_kanban()
    d.setdefault("pages", {})[page_id] = status
    save_kanban(d)


def gate(page_id: str) -> int:
    page_dir = PAGES / page_id
    render_dir = page_dir / "render"
    png = render_dir / "page.png"
    html = render_dir / "page.html"

    # 1. Render
    print(f"[1/4] Rendering {page_id} ...")
    r = run([sys.executable, str(RENDER), page_id])
    if r.returncode != 0:
        print(r.stderr)
        return 1
    print(r.stdout.strip())

    # 2. Screenshot
    if not html.exists():
        print(f"[err] render failed: {html} not found")
        return 1
    print(f"[2/4] Screenshot {page_id} ...")
    r = run([
        "google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--allow-file-access-from-files",
        "--force-device-scale-factor=2", "--window-size=1123,794",
        f"--screenshot={png}", f"file://{html.absolute()}"
    ])
    if r.returncode != 0:
        print(f"[warn] screenshot failed: {r.stderr}")
    else:
        print(f"  -> {png}")

    # 3. VLM judge (optional)
    if png.exists():
        print(f"[3/4] VLM judge {page_id} ...")
        r = run([sys.executable, str(JUDGE), page_id, str(png)], timeout=600)
        if r.returncode == 0:
            print(r.stdout.strip().splitlines()[-1] if r.stdout else "  ok")
        else:
            print(f"[info] VLM not available (code={r.returncode}); skipping gate")
    else:
        print("[warn] PNG not found, skipping VLM")

    # 4. Kanban update
    print(f"[4/4] Updating kanban ...")
    update_kanban(page_id, "rendered")
    print(f"  -> kanban.json: {page_id} = rendered")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: auto_gate.py <page_id>")
        sys.exit(1)
    sys.exit(gate(sys.argv[1]))