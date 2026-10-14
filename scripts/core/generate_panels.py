#!/usr/bin/env python3
"""Generate panels.html from evolution directories."""
from __future__ import annotations

import json
from pathlib import Path

EVOLUTION_DIR = Path("/home/bons/evops/outputs/evolution")


def find_evolution_dirs():
    dirs = [d for d in EVOLUTION_DIR.iterdir() if d.is_dir() and d.name.startswith("don")]
    # Sort by modification time (most recent first)
    dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return dirs[:4]  # Top 4 recent runs


def generate_panels_html():
    dirs = find_evolution_dirs()
    cards = []
    
    for d in dirs:
        # Find report file
        report_path = d / f"{d.name.split('_')[0]}_evolution_report.json"
        if not report_path.exists():
            # Try alternate naming
            for f in d.glob("*_evolution_report.json"):
                report_path = f
                break
        
        if not report_path.exists():
            continue
            
        report = json.loads(report_path.read_text(encoding="utf-8"))
        iterations = report.get("iterations", [])
        
        cards.append(f"""
        <div class="evolution-card">
          <div class="iteration-header">
            <span class="iteration-title">{report['concept']} — {d.name}</span>
            <span class="score-badge score-{report['final_score']//20 if report['final_score']>=90 else 'B' if report['final_score']>=75 else 'C' if report['final_score']>=60 else 'D'}">{report['final_score']}</span>
          </div>
          <p style="color:#666; font-size:12px">Converged: {'✅ YES' if report.get('converged') else '❌ NO'} | Iterations: {len(iterations)}</p>
          <div class="evolution-grid" style="grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 8px;">
    """)
        
        for it in iterations:
            gen_id = it['generation_id']
            score = it['score']
            grade = it['grade']
            
            # Try to find image
            panel_path = d / f"gen_{gen_id}.png"
            if panel_path.exists():
                img_path = f"/outputs/evolution/{d.name}/{panel_path.name}"
                img_tag = f'<img class="panel-image" src="{img_path}" alt="{gen_id}" style="max-height:140px; object-fit:cover;">'
            else:
                img_tag = f'<div style="background:#333; padding:20px; border-radius:6px; text-align:center; color:#555; font-size:11px;">{gen_id}<br>`No PNG`</div>'
            
            cards.append(f"""
            <div style="background:{'#1a3a1a' if grade=='A' else '#2a2a10' if grade=='B' else '#3a1a1a' if grade=='C' else '#3a1a1a'}; border-radius:8px; padding:8px;">
              <div style="font-weight:700; font-size:13px;">Gen {it['iteration']} — {grade}</div>
              <div style="font-size:10px; color:#aaa;">Score: {score}</div>
              {img_tag}
            </div>
            """)
        
        cards.append("</div></div>")
    
    # Build cards HTML string
    cards_str = "\n".join(cards)
    
    template = Path("/home/bons/evops/skills/evolution-dashboard/panels.html").read_text(encoding="utf-8")
    html = template.replace("__PANEL_CARDS__", cards_str)
    html = html.replace("__CONCEPT__", dirs[0].name.split("_")[0] if dirs else "unknown")
    html = html.replace("__TOTAL__", str(len(dirs)))
    html = html.replace("__GEN_COUNT__", str(sum(len(json.loads((d / f"{d.name.split('_')[0]}_evolution_report.json").read_text()).get("iterations",[])) for d in dirs if (d / f"{d.name.split('_')[0]}_evolution_report.json").exists())))
    
    output_path = Path("/home/bons/evops/outputs/evolution/panels.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"[PANELS] Generated: {output_path}")

if __name__ == "__main__":
    generate_panels_html()
