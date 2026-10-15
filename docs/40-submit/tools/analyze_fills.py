from pathlib import Path
import re

base = Path("/home/bons/evops/docs/40-submit/split")
p2 = (base/"part02_deliver.html").read_text(encoding="utf-8")

# Find all fill spans
fills = re.findall(r'<span[^>]*class="fill[^"]*"[^>]*>(.*?)</span>', p2)
print(f"Total fill spans: {len(fills)}")
for f in fills[:40]:
    print(f"  - {f[:80]}")
