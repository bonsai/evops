#!/usr/bin/env python3
"""Bridge: evaluate Zanzou (Psychedelic Pose Projection) output video."""
import json, sys, subprocess, os

def evaluate_zanzou(video_path: str) -> dict:
    if not os.path.exists(video_path):
        return {"axis": "zanzou_effect", "status": "error", "message": "file not found"}
    # Run ffprobe for basic metrics
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", video_path],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    fmt = info.get("format", {})
    return {
        "axis": "zanzou_effect",
        "status": "ok",
        "effect_type": "afterimage/pose_projection",
        "duration": float(fmt.get("duration", 0)),
        "width": video.get("width"),
        "height": video.get("height"),
        "evaluated_by": "zanzou_bridge.py",
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_zanzou(sys.argv[1]), indent=2))
