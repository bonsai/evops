#!/usr/bin/env python3
"""Shared configuration for all evops scripts."""
from pathlib import Path

EVOLUTION_DIR = Path("/home/bons/evops/outputs/evolution")
EVOPS_ROOT    = Path("/home/bons/evops")
DB_PATH       = EVOPS_ROOT / "mcp_core/db/sotsusei.db"
EVALUATOR_URL = "http://localhost:8002"

# MCP registry (port -> module path)
MCP_SERVERS = {
    "bpy-gen":             {"port": 8005, "path": "skills/bpy-gen/server.py"},
    "videogen":            {"port": 8006, "path": "skills/videogen/server.py"},
    "artcraft":            {"port": 8007, "path": "skills/artcraft/server.py"},
    "paper-digest":        {"port": 8008, "path": "skills/paper-digest/server.py"},
    "storyboard":          {"port": 8009, "path": "skills/storyboard/server.py"},
    "evolution-dashboard": {"port": 8010, "path": "skills/evolution-dashboard/server.py"},
    "evaluator":           {"port": 8002, "path": "mcp_core/evaluator/server.py"},
    "youtube":             {"port": 8011, "path": "skills/youtube/server.py"},
    "sdk":                 {"port": 8012, "path": "skills/sdk/server.py"},
    "lms":                 {"port": 8013, "path": "skills/lms/server.py"},
    "evolve":              {"port": 8014, "path": "skills/evolve/server.py"},
    "pipeline":            {"port": 8015, "path": "skills/pipeline/server.py"},
}

CONCEPTS = {
    "don_quixote": {
        "title": "Don Quixote de la Mancha",
        "attributes": {
            "lance":   "long lance (spear)",
            "shield":  "simple buckler shield",
            "armor":   "rusty old armor",
            "helmet":  "barber helmet (tin / makeshift)",
            "beard":   "thin gaunt beard",
            "stature": "tall and thin figure",
            "horse":   "thin horse (Rocinante)",
        },
        "mood": "dignified yet comical",
        "script": "skills/bpy-gen/tools/don_quixote_bpy.py",
    },
    "donpen": {
        "title": "Donpen-chan (ドン・キホーテ)",
        "attributes": {
            "body":   "penguin body white belly black back",
            "eyes":   "big cute round eyes with catch-light",
            "beak":   "small yellow beak",
            "cheeks": "pink blush circles",
            "cap":    "pink cone cap with dark pink brim",
            "star":   "gold star on cap front",
            "wings":  "short black stubby wings",
            "feet":   "yellow flipper feet",
        },
        "mood": "kawaii, cheerful, round and chubby",
        "script": "skills/bpy-gen/tools/donpen_bpy.py",
    },
    "doraemon": {
        "title": "Doraemon",
        "attributes": {
            "body":    "round blue body",
            "belly":   "white pocket belly",
            "eyes":    "big round eyes",
            "whiskers":"six black whiskers",
            "nose":    "red round nose",
            "collar":  "red collar with bell",
        },
        "mood": "friendly, futuristic, helpful",
        "script": "skills/bpy-gen/tools/doraemon_bpy.py",
    },
}
