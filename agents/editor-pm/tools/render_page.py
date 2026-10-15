#!/usr/bin/env python3
"""Render exactly one page of the submit deck, using the deck's existing CSS.

Reads docs/40-submit/pages/<page_id>/content.json, extracts the single
section named by source.section_selector from source.html, and wraps it with the
canonical stylesheet that index.html already loads. No page-specific CSS is
created: the only addition is the deck's own print framing (stage padding reset),
which index.html already declares under @media print.

Usage:
    python3 render_page.py p26-kaguru-agent-kaggle-evops-workflow
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # evops repo root
SUBMIT = REPO / "docs/40-submit"
PAGES = SUBMIT / "pages"
DECK_CSS_SOURCE = SUBMIT / "index.html"

# Mirrors the @media print block that index.html already ships.
PRINT_FRAMING = """
html,body{background:#fff!important}
.stage{transform:none!important}
.stage-inner{padding:0!important}
.sheet{box-shadow:none!important;margin:0!important}
*{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
"""


def canonical_css() -> str:
    html = DECK_CSS_SOURCE.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    if not m:
        raise SystemExit(f"no <style> in {DECK_CSS_SOURCE}")
    return m.group(1)


def section_for(page_id: str) -> tuple[str, str]:
    cfg = json.loads((PAGES / page_id / "content.json").read_text(encoding="utf-8"))
    src = SUBMIT / Path(cfg["source"]["html"]).relative_to("docs/40-submit")
    selector = cfg["source"]["section_selector"]
    m = re.search(r'data-t="([^"]+)"', selector)
    if not m:
        raise SystemExit(f"unsupported selector: {selector}")
    data_t = m.group(1)
    html = src.read_text(encoding="utf-8")
    sec = re.search(
        r'<section class="sheet[^"]*"[^>]*data-t="%s".*?</section>' % re.escape(data_t),
        html,
        re.DOTALL,
    )
    if not sec:
        raise SystemExit(f"section not found: {data_t} in {src}")
    return sec.group(0), data_t


def main() -> None:
    page_id = sys.argv[1] if len(sys.argv) > 1 else "p26-kaguru-agent-kaggle-evops-workflow"
    css = canonical_css()
    section, data_t = section_for(page_id)

    out_dir = PAGES / page_id / "render"
    out_dir.mkdir(parents=True, exist_ok=True)

    # base href: render/ -> pages/ -> 40-submit/  (so figures/... resolves)
    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>page-quality-gate: {page_id}</title>
<base href="../../..">
<style>
{css}
{PRINT_FRAMING}
</style>
</head>
<body>
<div class="stage" id="stage"><div class="stage-inner" id="sheets">
{section}
</div></div>
</body>
</html>
"""
    (out_dir / "page.html").write_text(doc, encoding="utf-8")
    print(f"rendered: {out_dir.relative_to(REPO)}/page.html")


if __name__ == "__main__":
    main()