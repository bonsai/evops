#!/usr/bin/env python3
"""Batch narration generation from episode.json using Voicevox (Hibiki / speaker 8)."""
import json, sys, os, subprocess

episode_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/episode.json"
output_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/narration.mp3"

with open(episode_path, "r", encoding="utf-8") as f:
    ep = json.load(f)

# Combine all panel texts with pauses
ts = " ".join(p.get("text", "") for p in ep.get("panels", []))

# Call voicevox-cli.js for each segment or combined
# Simplified: combined narration
subprocess.run([
    "node", "/home/bons/evops/skills/voicevox/bin/voicevox-cli.js",
    "--text", ts,
    "--speaker", "8",  # Hibiki（空野ヒビキ）
    "--output", output_path
], check=True)
print(f"Batch narration done: {output_path}")
