#!/usr/bin/env python3
"""Split index.html into per-page standalone HTML files under docs/40-submit/pages/<page_id>/"""
import re, json
from pathlib import Path

REPO = Path("/home/bons/evops")
SUBMIT = REPO / "docs/40-submit"
INDEX = SUBMIT / "index.html"
PAGES = SUBMIT / "pages"

html = INDEX.read_text(encoding="utf-8")

# Extract the <style> block (everything between <style> and </style>)
style_m = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
style = style_m.group(1) if style_m else ""

# Extract all sections in order
sections = re.findall(
    r'<!-- ============ .*? ============ -->\s*'
    r'(<section class="sheet[^"]*"[^>]*data-t="([^"]*)"[^>]*>.*?</section>)',
    html, re.DOTALL
)

print(f"Found {len(sections)} sections")

# Page ID mapping from pages.csv
csv_path = PAGES / "pages.csv"
page_map = {}
if csv_path.exists():
    import csv
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            page_map[row["data_t"]] = row["page_id"]

# Also map by title (data-t may have spaces)
for tag, pid in page_map.items():
    pass

# Fallback: derive page_id from the section's hd-no or order
used = set()
results = []
for i, (sec, tag) in enumerate(sections):
    # Try exact match first
    pid = page_map.get(tag)
    if not pid:
        # Try matching by title text
        title_m = re.search(r'<h2 class="hd-title">(.*?)</h2>', sec, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else tag
        # Try partial match in page_map
        for k, v in page_map.items():
            if k in tag or tag in k or k in title or title in k:
                pid = v
                break
    if not pid:
        # Fallback: use hd-no or order
        no_m = re.search(r'<span class="hd-no">\s*(\d+)\s*</span>', sec)
        num = no_m.group(1) if no_m else f"{i+1:02d}"
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', tag.lower()).strip('-')[:30]
        pid = f"p{num}-{slug}"
        if pid in used:
            pid = f"p{num}d-{slug}"
    used.add(pid)
    results.append((pid, tag, sec))

# Write each page
for pid, tag, sec in results:
    page_dir = PAGES / pid
    page_dir.mkdir(parents=True, exist_ok=True)
    
    # Build standalone HTML with the same CSS
    standalone = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{tag} — 総合演習 卒業制作</title>
<style>
{style}
</style>
</head>
<body>
<div class="stage" id="stage"><div class="stage-inner" id="sheets">
{sec}
</div></div>
</body>
</html>
"""
    out = page_dir / "page.html"
    out.write_text(standalone, encoding="utf-8")
    print(f"  {pid}: {tag} -> {out.relative_to(REPO)}")

# Update kanban.json
kanban_path = SUBMIT / "kanban.json"
kanban = json.loads(kanban_path.read_text(encoding="utf-8"))
for pid, tag, sec in results:
    kanban["pages"][pid] = "rendered"
kanban["last_updated"] = "2023-10-15T13:35:00Z"
kanban_path.write_text(json.dumps(kanban, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"\nUpdated kanban.json: {kanban_path.relative_to(REPO)}")