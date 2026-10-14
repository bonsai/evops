#!/usr/bin/env python3
"""Generate HTML evolution gallery."""
from __future__ import annotations

import json
from pathlib import Path


def _attr_badge(check: dict) -> str:
    cls = "ok" if check["status"] == "present" else "miss"
    return f'<div class="attr {cls}">{check["attribute"]} {check["score"]:.0f}</div>'


def _gen_card(it: dict) -> str:
    ev = it["eval"]
    grade_cls = ev["grade"]
    badge = '<span class="badge converged">✅ CONVERGED</span>' if ev["converged"] else '<span class="badge">running...</span>'
    attrs = "\n".join(_attr_badge(c) for c in ev["attribute_check"])
    sugs = "".join(f'<div class="sug">[{s["priority"].upper()}] {s["issue"]}</div>' for s in ev.get("suggestions", []))
    return f"""<div class="gen-card">
  <div class="gen-header">
    <span class="gen-title">Gen {it["iteration"]} — {it["generation_id"]}</span>
    <span class="score {grade_cls}">{ev["score"]}</span>
  </div>
  {badge}
  <div class="prompt-box">{it["prompt"]}</div>
  <div class="attr-grid">{attrs}</div>
  <div class="suggestions">{sugs}</div>
</div>"""


def generate_html(report: dict, output_path: Path):
    cards = "\n".join(_gen_card(it) for it in report.get("iterations", []))
    html = f"""<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>Evolution — {report['concept']}</title>
<style>
:root{{--bg:#0f0f12;--fg:#e8e8ec;--card:#1a1a20;--ok:#3a3;--warn:#f66}}
body{{background:var(--bg);color:var(--fg);font-family:system-ui,sans-serif;margin:0;padding:32px}}
h1{{font-size:28px;margin-bottom:8px}}.meta{{color:#666;font-size:14px;margin-bottom:24px}}
.gen-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
.gen-card{{background:var(--card);border:1px solid #2a2a32;border-radius:14px;padding:20px}}
.gen-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
.gen-title{{font-size:18px;font-weight:700}}.score{{font-size:24px;font-weight:800}}
.score.A{{color:var(--ok)}}.score.B{{color:#6f6}}.score.C{{color:#ff6}}.score.D{{color:var(--warn)}}
.badge{{font-size:11px;padding:2px 8px;border-radius:4px;background:#333;color:#aaa}}
.converged{{background:var(--ok);color:#fff}}.prompt-box{{background:#222;border-radius:8px;padding:12px;font-size:13px;color:#bbb;margin:10px 0;word-break:break-all}}
.attr-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(90px,1fr));gap:6px;margin-top:10px}}
.attr{{font-size:12px;padding:4px 8px;border-radius:4px;text-align:center}}
.attr.ok{{background:#1a3a1a;color:#5a5}}.attr.miss{{background:#3a1a1a;color:#a55}}
.suggestions{{margin-top:10px}}.sug{{font-size:12px;color:#a88;margin:3px 0;padding-left:12px;border-left:2px solid #533}}
</style></head>
<body>
<h1>🧬 Evolution — {report['concept']}</h1>
<p class="meta">Target: {report['target_score']} | Iterations: {len(report['iterations'])} | Final: {report['final_score']} | Converged: {'YES' if report['converged'] else 'NO'}</p>
<div class="gen-grid">{cards}</div>
<script>setTimeout(()=>location.reload(),10000)</script>
</body></html>"""
    output_path.write_text(html, encoding="utf-8")
    print(f"[GALLERY] {output_path}")
