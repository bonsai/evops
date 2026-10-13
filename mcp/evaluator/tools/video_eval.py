#!/usr/bin/env python3
"""Video evaluation helpers for evops pipeline."""
import json, subprocess, os, re
from pathlib import Path

def ffprobe_json(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def video_metrics(path: str) -> dict:
    """Return duration, width, height, fps, bitrate, frame count."""
    data = ffprobe_json(path)
    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    fmt = data.get("format", {})
    duration = float(fmt.get("duration", 0))
    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    fps_str = video_stream.get("r_frame_rate", "0/1")
    num, denom = map(int, fps_str.split("/"))
    fps = num / denom if denom else 0
    bitrate = int(fmt.get("bit_rate", 0))
    frame_count = int(duration * fps) if fps else 0
    return {
        "axis": "video_metrics",
        "duration_sec": round(duration, 3),
        "width": width, "height": height,
        "fps": round(fps, 2),
        "bitrate": bitrate,
        "frame_count": frame_count,
        "file_size_mb": round(os.path.getsize(path) / (1024 * 1024), 2),
    }

if __name__ == "__main__":
    import sys
    print(json.dumps(video_metrics(sys.argv[1]), indent=2))
