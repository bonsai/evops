from pathlib import Path
import re

html = (Path("/home/bons/evops/docs/40-submit/split")/"index.html").read_text(encoding="utf-8")
secs = re.findall(r'<section class="sheet[^"]*"[^>]*>.*?<div class="hd">', html, re.DOTALL)
print(f"Sections: {len(secs)}")
for i, s in enumerate(secs[-3:]):
    print(f"  {len(secs)-3+i+1}: {s[:120]}")