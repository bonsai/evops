#!/usr/bin/env python3
"""Convert ASCII art text to SVG."""
import sys

def aa_to_svg(aa_text: str, font_family="monospace", font_size=12) -> str:
    lines = aa_text.splitlines()
    h = len(lines) * font_size
    w = max(len(l) for l in lines) * font_size * 0.6
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">',
        '<rect width="100%" height="100%" fill="black"/>',
        f'<text x="0" y="0" font-family="{font_family}" font-size="{font_size}" fill="white">'
    ]
    for i, line in enumerate(lines):
        y = (i + 1) * font_size
        # Escape XML
        safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg_parts.append(f'<tspan x="0" dy="{font_size}">{safe}</tspan>')
    svg_parts.append('</text></svg>')
    return "\n".join(svg_parts)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: aa_to_svg.py <input.txt> <output.svg>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    svg = aa_to_svg(text)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(svg)
    print("done:", sys.argv[2])
