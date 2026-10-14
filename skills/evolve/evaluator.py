#!/usr/bin/env python3
"""Character evaluation against reference concepts."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skills.cli_mcp.config import CONCEPTS


def _build_keywords(reference: dict) -> dict:
    """Build keyword map from reference attributes."""
    attr_keywords = {}
    alias_map = {
        "lance":  ["spear", "やり"],
        "shield": ["buckler", "たて"],
        "armor":  ["armour", "鎧", "よろい"],
        "helmet": ["兜", "かぶと", "helm"],
        "beard":  ["髭", "ひげ"],
        "stature":["thin", "痩せ", "やせ", "slender"],
        "horse":  ["馬", "うま", "rocinante"],
        "body":   ["penguin", "ペンギン", "white belly", "black back"],
        "eyes":   ["eye", "目", "big eye", "cute"],
        "beak":   ["くちばし", "bill", "yellow"],
        "cheeks": ["ほっぺ", "blush", "pink"],
        "cap":    ["帽子", "pink cap", "どんぺん"],
        "star":   ["星", "gold"],
        "wings":  ["翼", "羽"],
        "feet":   ["足", "flipper", "yellow"],
    }
    for attr, desc in reference["attributes"].items():
        keywords = [desc.lower()]
        keywords.extend(desc.lower().split())
        if attr in alias_map:
            keywords.extend(alias_map[attr])
        attr_keywords[attr] = keywords
    return attr_keywords


def evaluate(image_path: Path, reference: dict, prompt_used: str) -> dict:
    """Evaluate how well the prompt matches the reference concept."""
    prompt_lower = prompt_used.lower()
    attr_keywords = _build_keywords(reference)

    checks = []
    attr_score = 0
    for attr, keywords in attr_keywords.items():
        matched = any(kw in prompt_lower for kw in keywords)
        if matched:
            attr_score += 1
            checks.append({"attribute": attr, "status": "present", "score": 1.0})
        else:
            checks.append({"attribute": attr, "status": "missing", "score": 0.0})

    attr_ratio = attr_score / max(len(attr_keywords), 1)

    # Prompt richness (unique segments / 300 chars max)
    segments = [s.strip() for s in prompt_used.split(",")]
    unique = []
    for s in segments:
        if not any(s in existing for existing in unique):
            unique.append(s)
    prompt_score = min(len(", ".join(unique)) / 300, 1.0)

    total = int(attr_ratio * 70 + prompt_score * 30)
    missing = [c["attribute"] for c in checks if c["status"] == "missing"]

    suggestions = []
    if missing:
        suggestions.append({
            "axis": "attributes", "priority": "high",
            "issue": f"Missing attrs: {', '.join(missing)}",
            "action": "add_to_prompt",
            "payload": {a: reference["attributes"][a] for a in missing}
        })
    if prompt_score < 0.5:
        suggestions.append({
            "axis": "prompt", "priority": "medium",
            "issue": "Prompt richness too low", "action": "lengthen_prompt"
        })

    return {
        "generation": image_path.stem,
        "score": total,
        "max_score": 100,
        "grade": "A" if total >= 90 else "B" if total >= 75 else "C" if total >= 60 else "D",
        "attribute_check": checks,
        "attribute_ratio": round(attr_ratio, 2),
        "prompt_score": round(prompt_score, 2),
        "missing_attributes": missing,
        "suggestions": suggestions,
        "converged": total >= 75,
    }
