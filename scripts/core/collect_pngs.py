#!/bin/bin/env python3
"""
Collect and display all evolution PNGs
"""
import json
import os
import shutil
from pathlib import Path

# Collect all PNGs
evolution_dirs = [
    Path("/home/bons/evops/outputs/donpen_1013_152334"),
    Path("/home/bons/evops/outputs/donpen_1013_152326"),
    Path("/home/bons/evops/outputs/don_quixote_1013_152344"),
    Path("/home/bons/evops/outputs/donpen_1013_150017"),
    Path("/home/bons/evops/outputs/don_quixote_1013_141149"),
    Path("/home/bons/evops/outputs/don_quixote_1013_141217"),
]

# Create unified output directory
output_dir = Path("/home/bons/evops/outputs/unified_png")
output_dir.mkdir(parents=True, exist_ok=True)

# Collect all PNGs
all_pngs = []
for d in evolution_dirs:
    for png_file in d.rglob("*.png"):
        if png_file.exists():
            rel_path = png_file.relative_to("/home/bons/evops")
            new_path = output_dir / rel_path.name
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png_file, new_path)
            all_pngs.append({
                "path": str(rel_path),
                "name": png_file.name,
                "size": png_file.stat().st_size,
            })

print(f"Collected {len(all_pngs)} PNG files")

# Generate simple HTML gallery
html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Unified Evolution PNG Gallery</title>
<style>
  body { background: #0f0f12; color: #e8e8ec; font-family: system-ui; }
  .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px; }
  .image-card { background: #1a1a20; border: 1px solid #2a2a32; border-radius: 8px; overflow: hidden; }
  .image-card img { width: 100%; height: auto; display: block; }
  .info { padding: 12px; font-size: 14px; }
  .name { font-weight: bold; margin-bottom: 4px; }
  .path { color: #666; font-size: 12px; }
</style>
</head>
<body>
<h1 style="padding: 20px; color: #7c3aed;">🧬 Unified Evolution PNG Gallery</h1>
<div class="gallery">
"""

for img in all_pngs:
    html_content += f"""
    <div class="image-card">
      <img src="{img['path']}" alt="{img['name']}">
      <div class="info">
        <div class="name">{img['name']}</div>
        <div class="path">{img['path']}</div>
      </div>
    </div>
"""

html_content += """
</div>
</body>
</html>
"""

# Save HTML gallery
html_path = output_dir / "gallery.html"
html_path.write_text(html_content, encoding="utf-8")
print(f"HTML gallery saved to: {html_path}")

# Generate JSON report
report = {
    "total_images": len(all_pngs),
    "generated_at": "2026-10-13",
    "sources": [str(d) for d in evolution_dirs]
}
report_path = output_dir / "report.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Report saved to: {report_path}")

print("\n✨ All evolution PNGs collected and gallery generated!")
print(f"📂 View at: file://{html_path}")
"""
< /home/bons/evops/outputs/unified_png/gallery.html

PNG files:
$(find /home/bons/evops/outputs/unified_png -name "*.png" | wc -l)
"""