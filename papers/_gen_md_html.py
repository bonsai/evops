#!/usr/bin/env python3
"""Generate papers.md and index.html from papers.json"""
import json
from pathlib import Path

BASE = Path("/home/bons/evops/papers")

with open(BASE / "papers.json", encoding="utf-8") as f:
    data = json.load(f)

# papers.md
md = f"""# SSSS Papers

## Research Question
{data['research_question']}

## External Papers

"""
for p in data["papers"]:
    if p.get("venue") == "in-house":
        continue
    url = p.get("url")
    link = f" [{p['venue']}]({url})" if url else f" {p['venue']}"
    md += f"""### P{p['id']:02d} — {p['title']}
**{p['title']} /{link} / {p['year']}**

{p['body']}

**Relevance**: {p['relevance']}

"""

md += "\n## EvOps Original Papers\n\n"
for p in data["papers"]:
    if p.get("venue") != "in-house":
        continue
    dname = f"P{p['id']:02d}-" + p['short'].lower().replace(' ', '-')[:25].rstrip('-') + f"-{p['year']}"
    md += f"""### P{p['id']:02d} — {p['title']}
**{p['title']} / in-house / {p['year']}**

{p['body']}

**Keywords**: {', '.join(p['categories'])}

**Doc**: [{dname}/README.md]({dname}/README.md)

"""

md += "\n## Synthesis\n"
for item in data["synthesis"]:
    md += f"1. {item}\n"
md += f"\n## Loop\n{data['loop']}\n"

with open(BASE / "papers.md", "w", encoding="utf-8") as f:
    f.write(md)

# index.html
html = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EvOps Papers</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;line-height:1.6}
h1{margin-bottom:4px} .lead{color:#555}
article{border:1px solid #ddd;border-radius:10px;padding:16px;margin:12px 0}
h2{margin:0 0 4px;font-size:1.05rem} p{margin:4px 0 8px}
a{color:#0645ad}
.section-title{margin-top:32px;font-size:1.3rem;border-bottom:2px solid #333;padding-bottom:4px}
</style>
</head>
<body>
<h1>EvOps Papers — Research Evidence</h1>
<p class="lead">Research question: LMS/VLMを共通評価器として使い、評価結果をDBへ蓄積し、MLによる改善へ接続できるか。</p>

<h2 class="section-title">External Papers</h2>
"""

for p in data["papers"]:
    if p.get("venue") == "in-house":
        continue
    pid = f"P{p['id']:02d}"
    link = ""
    if p.get("url"):
        label = "PDF" if ".pdf" in p["url"] else "Spec"
        link = f'<a href="{p["url"]}">{label}</a>'
    else:
        link = '<span style="color:#999">PDF unavailable</span>'
    html += f"""<article><h2>{pid} — {p['title']}</h2><p>{p['short']}</p><p><strong>{p['venue']}</strong> / {p['year']} / {link}</p></article>\n"""

html += '<h2 class="section-title">EvOps Original Papers</h2>\n'

for p in data["papers"]:
    if p.get("venue") != "in-house":
        continue
    pid = f"P{p['id']:02d}"
    slug = '-'.join(p['short'].lower().replace('/', '-').replace(':', ' ').split()[:5])
    dname = f"{pid}-{slug}-{p['year']}"
    html += f"""<article><h2>{pid} — {p['title']}</h2><p>{p['short']}</p><p><strong>in-house</strong> / {p['year']} / <a href="{dname}/README.md">Doc</a></p></article>\n"""

html += """</body>\n</html>"""

with open(BASE / "index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated papers.md and index.html")
