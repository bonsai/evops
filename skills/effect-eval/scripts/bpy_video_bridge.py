#!/usr/bin/env python3
"""Bridge: evaluate bpy (Blender Python) generated video/effect."""
import json, sys, os, subprocess

def evaluate_bpy_video(video_path: str) -> dict:
    if not os.path.exists(video_path):
        return {"axis": "bpy_video", "status": "error", "message": "file not found"}
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", video_path]
    info = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    fmt = info.get("format", {})
    return {
        "axis": "bpy_video",
        "status": "ok",
        "effect_type": "blender_3d_render",
        "duration": float(fmt.get("duration", 0)),
        "width": video.get("width"),
        "height": video.get("height"),
        "evaluated_by": "bpy_video_bridge.py",
    }

if __name__ == "__main__":
    print(json.dumps(evaluate_bpy_video(sys.argv[1]), indent=2))
