"""Build SVG-based presentation from slides.json.

Usage:
    python presen/web/build.py

Output:
    presen/web/index.html
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def escape(text: str) -> str:
    return html.escape(text).replace("\n", "&#10;")


def render_title(slide: dict, w: int, h: int) -> str:
    return f"""
<svg class="slide" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">
  <rect width="{w}" height="{h}" fill="#0f172a"/>
  <rect x="0" y="0" width="{w*0.25:.0f}" height="{h}" fill="#3b82f6"/>
  <text x="{w*0.55:.0f}" y="{h*0.42:.0f}" text-anchor="middle" fill="#f8fafc"
        font-size="{h*0.12:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{escape(slide["title"])}</text>
  <text x="{w*0.55:.0f}" y="{h*0.56:.0f}" text-anchor="middle" fill="#94a3b8"
        font-size="{h*0.05:.0f}" font-family="Noto Sans JP, sans-serif">{escape(slide["subtitle"])}</text>
  <text x="{w*0.55:.0f}" y="{h*0.85:.0f}" text-anchor="middle" fill="#64748b"
        font-size="{h*0.03:.0f}" font-family="Noto Sans JP, sans-serif">{escape(slide["footer"])}</text>
</svg>
"""


def render_content(slide: dict, w: int, h: int) -> str:
    no = slide.get("number", "")
    title = escape(slide["title"])
    bullets = slide.get("bullets", [])
    start_y = h * 0.35
    gap = h * 0.11
    items = "\n".join(
        f"""<text x="{w*0.12:.0f}" y="{start_y + i*gap:.0f}" fill="#e2e8f0"
              font-size="{h*0.052:.0f}" font-weight="600" font-family="Noto Sans JP, sans-serif">{escape(f"• {b}")}</text>"""
        for i, b in enumerate(bullets)
    )
    return f"""
<svg class="slide" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">
  <rect width="{w}" height="{h}" fill="#0f172a"/>
  <rect x="0" y="0" width="{w}" height="{h*0.08:.0f}" fill="#1e293b"/>
  <text x="{w*0.05:.0f}" y="{h*0.055:.0f}" fill="#64748b"
        font-size="{h*0.04:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{escape(no)}</text>
  <text x="{w*0.5:.0f}" y="{h*0.055:.0f}" text-anchor="middle" fill="#f8fafc"
        font-size="{h*0.05:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{title}</text>
  {items}
</svg>
"""


def render_demo(slide: dict, w: int, h: int) -> str:
    no = slide.get("number", "")
    title = escape(slide["title"])
    lines = slide.get("lines", [])
    # Demo screen: large centered text, minimal decoration
    return f"""
<svg class="slide demo" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">
  <rect width="{w}" height="{h}" fill="#020617"/>
  <rect x="{w*0.08:.0f}" y="{h*0.12:.0f}" width="{w*0.84:.0f}" height="{h*0.76:.0f}" rx="20"
        fill="#1e293b" stroke="#3b82f6" stroke-width="6"/>
  <text x="{w*0.5:.0f}" y="{h*0.24:.0f}" text-anchor="middle" fill="#60a5fa"
        font-size="{h*0.07:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{title}</text>
  <text x="{w*0.5:.0f}" y="{h*0.42:.0f}" text-anchor="middle" fill="#f8fafc"
        font-size="{h*0.08:.0f}" font-weight="700" font-family="Noto Sans JP, sans-serif">{escape(lines[0]) if lines else ""}</text>
  <text x="{w*0.5:.0f}" y="{h*0.55:.0f}" text-anchor="middle" fill="#94a3b8"
        font-size="{h*0.05:.0f}" font-family="Noto Sans JP, sans-serif">{escape(lines[1]) if len(lines) > 1 else ""}</text>
  <text x="{w*0.5:.0f}" y="{h*0.66:.0f}" text-anchor="middle" fill="#64748b"
        font-size="{h*0.04:.0f}" font-family="Noto Sans JP, sans-serif">{escape(lines[2]) if len(lines) > 2 else ""}</text>
  <text x="{w*0.95:.0f}" y="{h*0.06:.0f}" text-anchor="end" fill="#64748b"
        font-size="{h*0.04:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{escape(no)}</text>
</svg>
"""


def render_repo(slide: dict, w: int, h: int) -> str:
    no = slide.get("number", "")
    title = escape(slide["title"])
    repo = escape(slide["repo"])
    paths = slide.get("paths", [])
    qr = slide.get("qr", "")
    start_y = h * 0.32
    gap = h * 0.09
    path_items = "\n".join(
        f"""<text x="{w*0.1:.0f}" y="{start_y + i*gap:.0f}" fill="#e2e8f0"
              font-size="{h*0.045:.0f}" font-family="Noto Sans JP, sans-serif">{escape(f"- {p}")}</text>"""
        for i, p in enumerate(paths)
    )
    return f"""
<svg class="slide" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">
  <rect width="{w}" height="{h}" fill="#0f172a"/>
  <text x="{w*0.5:.0f}" y="{h*0.15:.0f}" text-anchor="middle" fill="#f8fafc"
        font-size="{h*0.09:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{title}</text>
  <text x="{w*0.5:.0f}" y="{h*0.24:.0f}" text-anchor="middle" fill="#3b82f6"
        font-size="{h*0.045:.0f}" font-family="monospace">{repo}</text>
  {path_items}
  <image href="{qr}" x="{w*0.72:.0f}" y="{h*0.35:.0f}" width="{h*0.3:.0f}" height="{h*0.3:.0f}"/>
  <text x="{w*0.95:.0f}" y="{h*0.06:.0f}" text-anchor="end" fill="#64748b"
        font-size="{h*0.04:.0f}" font-weight="800" font-family="Noto Sans JP, sans-serif">{escape(no)}</text>
</svg>
"""


def render_slide(slide: dict, w: int, h: int) -> str:
    t = slide.get("type", "content")
    if t == "title":
        return render_title(slide, w, h)
    if t == "demo":
        return render_demo(slide, w, h)
    if t == "repo":
        return render_repo(slide, w, h)
    return render_content(slide, w, h)


def build() -> None:
    data = json.loads((HERE / "slides.json").read_text(encoding="utf-8"))
    meta = data["meta"]
    w, h = meta["width"], meta["height"]

    slides_html = "\n".join(render_slide(s, w, h) for s in data["slides"])

    html_doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(meta["title"])}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  width: 100%; height: 100%;
  background: #020617;
  overflow: hidden;
  font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif;
}}
#stage {{
  width: 100vw; height: 100vh;
  display: flex; align-items: center; justify-content: center;
}}
.slide {{
  width: 100%; height: 100%;
  display: none;
  max-width: 100vw; max-height: 100vh;
}}
.slide.active {{ display: block; }}
#counter {{
  position: fixed; bottom: 12px; right: 16px;
  color: #64748b; font-size: 14px; font-family: monospace;
  z-index: 10;
}}
#hint {{
  position: fixed; bottom: 12px; left: 16px;
  color: #334155; font-size: 12px;
  z-index: 10;
}}
@media print {{
  html, body {{ overflow: visible; background: #fff; }}
  #stage {{ display: block; }}
  .slide {{
    display: block !important;
    page-break-after: always;
    width: 297mm; height: 210mm;
    max-width: none; max-height: none;
  }}
  #counter, #hint {{ display: none; }}
}}
</style>
</head>
<body>
<div id="stage">
{slides_html}
</div>
<div id="counter">1 / {len(data["slides"])}</div>
<div id="hint">← → または ↑ ↓ / スペース / タップで移動</div>
<script>
const slides = document.querySelectorAll('.slide');
let idx = 0;
function show(i) {{
  slides[idx].classList.remove('active');
  idx = Math.max(0, Math.min(slides.length - 1, i));
  slides[idx].classList.add('active');
  document.getElementById('counter').textContent = (idx + 1) + ' / ' + slides.length;
}}
show(0);
document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {{
    e.preventDefault(); show(idx + 1);
  }} else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {{
    e.preventDefault(); show(idx - 1);
  }} else if (e.key === 'Home') {{
    e.preventDefault(); show(0);
  }} else if (e.key === 'End') {{
    e.preventDefault(); show(slides.length - 1);
  }}
}});
document.addEventListener('click', () => show(idx + 1));
</script>
</body>
</html>
"""

    target = HERE / "index.html"
    target.write_text(html_doc, encoding="utf-8")
    print(f"written: {target} ({len(data['slides'])} slides)")


if __name__ == "__main__":
    build()
