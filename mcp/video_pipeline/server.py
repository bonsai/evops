#!/usr/bin/env python3
"""
MCP Video Pipeline — P01 (VeMo), P02 (EvalCrafter), P03 (VideoScore)
Expose pipeline steps as MCP tools.
"""
import json, sys, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

VIDEO_DIR = "/home/bons/evops/outputs/paper_videos"
KANBAN = "/home/bons/evops/outputs/kanban.jsonl"

PIPELINES = {
    "P01": {"title": "VeMo: Zero-Shot Text-to-Motion", "asset": "P01/video.mp4"},
    "P02": {"title": "EvalCrafter: Benchmarking Video Gen", "asset": "P02/video.mp4"},
    "P03": {"title": "VideoScore: Fine-grained Feedback", "asset": "P03/video.mp4"},
}

def generate_video(pipe_id: str) -> dict:
    info = PIPELINES.get(pipe_id)
    if not info:
        return {"status": "error", "message": f"Unknown pipeline: {pipe_id}"}
    video_path = os.path.join(VIDEO_DIR, info["asset"])
    # Placeholder: update kanban to in-progress if not already
    # Real pipeline: voicevox → kamishibai → ffmpeg
    return {
        "status": "started",
        "pipeline": pipe_id,
        "title": info["title"],
        "video_path": video_path,
        "message": "Pipeline triggered via MCP — use TUI or direct call to complete",
    }

def list_pipelines() -> list:
    result = []
    for pid, info in PIPELINES.items():
        video_path = os.path.join(VIDEO_DIR, info["asset"])
        status = "pending"
        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            status = "done"
        result.append({
            "pipeline": pid,
            "title": info["title"],
            "video_path": video_path,
            "status": status,
        })
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pipeline", choices=list(PIPELINES.keys()))
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        for item in list_pipelines():
            print(json.dumps(item))
    elif args.pipeline:
        print(json.dumps(generate_video(args.pipeline)))
    else:
        parser.print_help()
