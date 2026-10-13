#!/usr/bin/env bash
# CLI for SF paper comic — 4-panel manga SVG creation
# Usage:
#   ./cli.sh <paper_id> <title> <hook> <panel1> <panel2> <panel3> <panel4>

set -euo pipefail

python3 - << 'PYTHON'
import sys
sys.path.insert(0, "/home/bons/evops/mcp")
from sf_paper_comic.server import make_episode, make_timeline

# Example: create episode and write metadata
paper_id = sys.argv[1] if len(sys.argv) > 1 else "default-paper"
result = make_episode(
    paper_id=paper_id,
    title=sys.argv[2] if len(sys.argv) > 2 else "SF 落語",
    hook=sys.argv[3] if len(sys.argv) > 3 else "評価ループから知識へ",
    panel1=sys.argv[4] if len(sys.argv) > 4 else "問題提起",
    panel2=sys.argv[5] if len(sys.argv) > 5 else "評価軸分析",
    panel3=sys.argv[6] if len(sys.argv) > 6 else "成長パターン発見",
    panel4=sys.argv[7] if len(sys.argv) > 7 else "再生成ループ",
)
print(f"Created: {paper_id}")
print(f"Title: {result['title']}")
for p in result["panels"]:
    print(f"  P{p['no']} [{p['role']}]: {p['text']}")
print(f"Animation: {result['animation']['sequence']}")
PYTHON
