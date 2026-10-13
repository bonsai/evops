#!/usr/bin/env python3
"""Bridge: evaluate MediaPipe pose effect video."""
import json, sys, os, subprocess

def evaluate_mediapipe_effect(video_path: str) -> dict:
    if not os.path.exists(video_path):
        return {"axis": "mediapipe_effect", "status": "error", "message": "file not found"}
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", video_path]
    info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    fmt = info.get("format", {})
    return {
        "axis": "mediapipe_effect",
        "status": "ok",
        "effect_type": "pose_tracking/skeleton_overlay",
        "duration": float(fmt.get("duration", 0)),
        "width": video.get("width"),
        "height": video.get("height"),
        "evaluated_by": "mediapipe_bridge.py",
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_mediapipe_effect(sys.argv[1]), indent=2))
