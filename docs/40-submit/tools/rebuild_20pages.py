from pathlib import Path
import re

base = Path("/home/bons/evops/docs/40-submit/split")
html = (base/"index.html").read_text(encoding="utf-8")

# Extract all top-level sections
sections = re.findall(r'(<section class="sheet[^"]*".*?</section>)', html, re.DOTALL)
print(f"Found {len(sections)} sections")

# Keep only first 20
sections = sections[:20]
print(f"Keeping {len(sections)} sections")

# Update page numbers in TOC and headers
# Simple approach: renumber hd-no spans from 01 to 20
for i, sec in enumerate(sections):
    # Update hd-no if present
    sec = re.sub(r'<span class="hd-no">(\d+)</span>', f'<span class="hd-no">{i+1:02d}</span>', sec)
    sections[i] = sec

# Update cover footer
cover = sections[0]
cover = re.sub(r'全 \d+ ページ', '全 20 ページ', cover)
cover = re.sub(r'p\.\d+', 'p.01', cover)
sections[0] = cover

# Update TOC page numbers
toc = sections[1]
toc = re.sub(r'<span class="pg">(\d+)</span>', lambda m: f'<span class="pg">{int(m.group(1)):02d}</span>', toc)
sections[1] = toc

# Rebuild HTML
new_html = '<!DOCTYPE html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>総合演習 卒業制作 — 提出一式 &amp; 発表資料（A4横・全20ペ）</title>\n<link rel="stylesheet" href="styles.css">\n</head>\n<body>\n<div class="stage" id="stage">\n<div class="stage-inner" id="sheets">\n\n'
for i, sec in enumerate(sections):
    new_html += sec + '\n\n'
new_html += '</div>\n</div>\n</body>\n</html>'

(base/"index.html").write_text(new_html, encoding="utf-8")
print(f"Written: {len(new_html)} bytes")

# Verify
assert '<section class="sheet cover' in new_html
assert '全 20 ページ' in new_html
print("OK")