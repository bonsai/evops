#!/usr/bin/env python3
"""Prompt evolution from evaluation results."""


def evolve(eval_result: dict, current_prompt: str, reference: dict) -> str:
    """Generate next prompt based on evaluation feedback."""
    existing = [p.strip().lower() for p in current_prompt.split(",")]
    additions = []

    for suggestion in eval_result.get("suggestions", []):
        action = suggestion.get("action")
        if action == "add_to_prompt":
            for attr, desc in suggestion.get("payload", {}).items():
                desc_lower = desc.lower()
                if not any(desc_lower in ex or ex in desc_lower for ex in existing):
                    additions.append(desc)
        elif action == "lengthen_prompt":
            for attr, desc in reference["attributes"].items():
                desc_lower = desc.lower()
                if not any(desc_lower in ex or ex in desc_lower for ex in existing):
                    additions.append(desc)

    new_prompt = current_prompt
    if additions:
        new_prompt += ", " + ", ".join(additions)
    if new_prompt == current_prompt:
        new_prompt += ", detailed, high quality"
    return new_prompt.strip()
