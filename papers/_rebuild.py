#!/usr/bin/env python3
"""Reconstruct papers/P##-*/ directories and README.md from papers.json"""
import json, re, os, textwrap
from pathlib import Path

BASE = Path("/home/bons/evops/papers")

def slugify(title: str, year: int, known: dict = None) -> str:
    """Generate short slug from paper title"""
    # Known mappings to preserve consistency
    known_slugs = {
        1: "vemo",
        2: "evalcrafter",
        3: "videoscore",
        4: "visualprompter",
        5: "3d-animation-qa",
        6: "dreamfusion",
        7: "point-e",
        8: "magic3d",
        9: "idefics2",
        10: "clip",
        11: "pick-a-pic",
        12: "imagereward",
        13: "hpsv2",
        14: "instructgpt-rlhf",
        15: "dpo",
        16: "active-learning-llm",
        17: "mcp",
        18: "a2a",
        19: "phi-3",
        20: "llama-3.2",
        21: "false-dawn-slm",
        22: "watermark-llm",
        23: "vquala",
        24: "uniapo",
        25: "b-coder",
        26: "mlops-eval-loop",
        27: "vlm-eval-automation",
        28: "evolutionary-gen-loop",
        29: "jev-driven-mlops",
        30: "model-free-visual-synthesis",
        31: "inverse-preference-learning",
        32: "cost-aware-rotation-loop",
        33: "structured-feature-axes",
        34: "from-evaluation-to-knowledge",
        35: "unified-dsl",
        36: "multi-metric-story-eval",
        37: "observability-dashboards",
    }
    if known and known.get("id") in known_slugs:
        return f"{known_slugs[known['id']]}-{year}"
    
    # Fallback: derive from title
    t = title.lower()
    t = re.sub(r'[:\-/]', ' ', t)
    t = re.sub(r'[\(\)\[\]\{\}\.,;!?]', '', t)
    words = [w for w in t.split() if w not in {
        'a', 'an', 'the', 'for', 'and', 'or', 'of', 'in', 'to', 'with', 'from',
        'using', 'via', 'by', 'on', 'at', 'as', 'is', 'are', 'be', 'being'
    }]
    slug = '-'.join(words[:5])
    return f"{slug}-{year}"

with open(BASE / "papers.json") as f:
    data = json.load(f)

created = 0
for p in data["papers"]:
    pid = p["id"]
    year = p["year"]
    slug = slugify(p["title"], year, p)
    dname = f"P{pid:02d}-{slug}"
    dpath = BASE / dname
    dpath.mkdir(exist_ok=True)
    
    is_in_house = p.get("venue") == "in-house"
    
    if is_in_house:
        # Full abstract for original papers
        content = f"""# P{pid}: {p['title']}

> **{p['title']}** / {p['venue']} / {year}

## Abstract

{p['body']}

## Short
{p['short']}

## Keywords

{', '.join(p['categories'])}
"""
    else:
        # Minimal entry for external papers
        content = f"""# P{pid}: {p['title']}

> **{p['title']}** / {p['venue']} / {year}

## Short
{p['short']}

## Relevance
{p['relevance']}

## Keywords

{', '.join(p['categories'])}
"""
    (dpath / "README.md").write_text(content, encoding="utf-8")
    created += 1

print(f"Created {created} paper directories under {BASE}")
