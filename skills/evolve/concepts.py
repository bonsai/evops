#!/usr/bin/env python3
"""Reference concept definitions for evolve loop."""
from skills.cli_mcp.config import CONCEPTS


def load_reference_concept(concept: str = "don_quixote") -> dict:
    """Return reference concept definition."""
    return CONCEPTS.get(concept, CONCEPTS["don_quixote"])
