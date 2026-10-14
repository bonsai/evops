#!/usr/bin/env python3
"""SVG Generator — speech bubbles, captions, font selection.
Reads episode.json to generate panel SVGs."""
import argparse
import json
import os

# Font options
FONT_MAP = {
    "mincho": "IPAexMincho, serif",
    "gothic": "IPAexGothic, sans-serif",
    "lato": "Lato, sans-serif",
    "inter": "Inter, sans-serif",
}


def generate_panel_svg(panel: dict, index: int, font: str = "gothic", paper_id: str = "UNKNOWN") -> str:
    font_family = FONT_MAP.get(font, FONT_MAP["gothic"])
    text = panel.get("text", "")
    speaker = panel.get("speaker", "")
    role = panel.get("role", "")
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480" width="100%" height="100%">
  <rect x="0" y="0" width="640" height="480" fill="#faf8ff"/>
  <text x="320" y="40" text-anchor="middle" font-family="{font_family}" font-size="20" font-weight="bold" fill="#7c3aed">[{paper_id}] コマ{index+1} — {role}</text>
  
  <!-- Stick figure placeholder -->
  <circle cx="320" cy="180" r="40" fill="none" stroke="#334" stroke-width="3"/>
  <line x1="320" y1="220" x2="320" y2="340" stroke="#334" stroke-width="3"/>
  <line x1="260" y1="260" x2="380" y2="260" stroke="#334" stroke-width="3"/>
  <line x1="320" y1="340" x2="280" y2="420" stroke="#334" stroke-width="3"/>
  <line x1="320" y1="340" x2="360" y2="420" stroke="#334" stroke-width="3"/>
  
  <!-- Speech bubble -->
  <rect x="80" y="320" width="480" height="100" rx="20" fill="#fff" stroke="#334" stroke-width="2"/>
  <polygon points="300,320 320,300 340,320" fill="#fff" stroke="#334" stroke-width="2"/>
  <text x="320" y="355" text-anchor="middle" font-family="{font_family}" font-size="16" fill="#222">{text}</text>
  <text x="320" y="380" text-anchor="middle" font-family="{font_family}" font-size="12" fill="#555">— {speaker}</text>
</svg>"""


def generate_from_episode(episode_path: str, output_dir: str, font: str = "gothic", paper_id: str = None):
    with open(episode_path, "r", encoding="utf-8") as f:
        ep = json.load(f)
    os.makedirs(output_dir, exist_ok=True)
    
    # Auto-detect paper_id from output_dir if not provided
    if paper_id is None:
        paper_id = os.path.basename(os.path.normpath(output_dir))
        if paper_id.startswith("papers"):
            paper_id = os.path.basename(os.path.dirname(os.path.normpath(output_dir)))
    
    panels = ep.get("panels", [])
    generated = []
    for i, panel in enumerate(panels):
        svg = generate_panel_svg(panel, i, font, paper_id)
        out_path = os.path.join(output_dir, f"{paper_id}_panel_{i+1:02d}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Generated: {out_path}")
        generated.append(out_path)
    return generated


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SVG Generator from episode.json")
    parser.add_argument("--episode", required=True, help="episode.json path")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--font", default="gothic", choices=["mincho", "gothic", "lato", "inter"])
    parser.add_argument("--paper-id", default=None, help="Paper ID (e.g. S01, P03)")
    args = parser.parse_args()
    generate_from_episode(args.episode, args.output_dir, args.font, args.paper_id)
