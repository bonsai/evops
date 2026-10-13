"""Lightweight image/video evaluation MCP server with FastAPI integration.

Run:
    python mcp/evaluator/server.py        # stdio mode
    python mcp/evaluator/server.py --http # HTTP mode on port 8002
"""
from __future__ import annotations

import argparse
import math
import json
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from fastmcp import FastMCP

from mcp.base_server import create_mcp_app, run_mcp_server

# Local video evaluation helper
try:
    from mcp.evaluator.tools.video_eval import video_metrics
    _HAS_VIDEO_EVAL = True
except Exception:
    _HAS_VIDEO_EVAL = False
    def video_metrics(path): return {"axis": "video_metrics", "status": "error", "reason": "video_eval not available"}

try:
    import torch
    from transformers import CLIPProcessor, CLIPModel
    _HAS_CLIP = True
except ImportError:
    _HAS_CLIP = False
    CLIPModel = None  # type: ignore
    CLIPProcessor = None  # type: ignore

mcp = FastMCP("sotsusei-evaluator")
_CLIP_CACHE: dict[str, Any] = {}


def _load_clip(model_name: str = "openai/clip-vit-base-patch32") -> tuple[Any, Any]:
    if not _HAS_CLIP:
        raise RuntimeError("CLIP not available. Install transformers and torch.")
    if model_name not in _CLIP_CACHE:
        model = CLIPModel.from_pretrained(model_name)
        processor = CLIPProcessor.from_pretrained(model_name)
        model.eval()
        _CLIP_CACHE[model_name] = (model, processor)
    return _CLIP_CACHE[model_name]


def _load_image(path: str, size: tuple[int, int] | None = None) -> Image.Image:
    img = Image.open(path).convert("RGB")
    if size:
        img = img.resize(size, Image.Resampling.LANCZOS)
    return img


@mcp.tool()
def list_capabilities() -> dict[str, Any]:
    """List available evaluators and their status."""
    return {
        "clip_available": _HAS_CLIP,
        "video_eval_available": _HAS_VIDEO_EVAL,
        "capabilities": [
            "clip_text_similarity",
            "clip_image_similarity",
            "basic_image_metrics",
            "color_statistics",
            "video_metrics",
            "ascii_art_metrics",
            "effect_metrics",
        ],
    }


@mcp.tool()
def clip_text_similarity(
    image_path: str, text: str,
    model_name: str = "openai/clip-vit-base-patch32",
) -> dict[str, Any]:
    """Compute CLIP cosine similarity between an image and a text prompt."""
    model, processor = _load_clip(model_name)
    image = _load_image(image_path)
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        score = outputs.logits_per_image.item() / 100.0
    return {"axis": "clip_text_similarity", "score": score, "model": model_name, "prompt": text}


@mcp.tool()
def clip_image_similarity(
    image_path_a: str, image_path_b: str,
    model_name: str = "openai/clip-vit-base-patch32",
) -> dict[str, Any]:
    """Compute CLIP cosine similarity between two images."""
    model, processor = _load_clip(model_name)
    img_a = _load_image(image_path_a)
    img_b = _load_image(image_path_b)
    inputs = processor(images=[img_a, img_b], return_tensors="pt", padding=True)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        cos = torch.nn.functional.cosine_similarity(
            image_features[0].unsqueeze(0), image_features[1].unsqueeze(0)
        )
    return {"axis": "clip_image_similarity", "score": cos.item(), "model": model_name}


@mcp.tool()
def basic_image_metrics(image_path: str) -> dict[str, Any]:
    """Return basic non-ML metrics: width, height, aspect ratio, file size."""
    p = Path(image_path)
    img = _load_image(image_path)
    w, h = img.size
    aspect = round(w / h, 4) if h else 0.0
    return {
        "axis": "basic_metrics",
        "width": w, "height": h, "aspect_ratio": aspect,
        "file_size_bytes": p.stat().st_size if p.exists() else None,
        "megapixels": round((w * h) / 1_000_000, 3),
    }


@mcp.tool()
def color_statistics(image_path: str) -> dict[str, Any]:
    """Return mean color, brightness, saturation hints."""
    img = _load_image(image_path, size=(224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    mean_rgb = arr.mean(axis=(0, 1)).tolist()
    brightness = float(arr.mean())
    std = float(arr.std())
    colorfulness = float(np.std(arr, axis=(0, 1)).mean())
    return {
        "axis": "color_statistics",
        "mean_rgb": [round(c, 4) for c in mean_rgb],
        "brightness": round(brightness, 4),
        "std": round(std, 4),
        "colorfulness": round(colorfulness, 4),
    }


@mcp.tool()
def evaluate_image(
    image_path: str,
    prompt: str | None = None,
    reference_path: str | None = None,
    axes: list[str] | None = None,
) -> dict[str, Any]:
    """Run a configurable evaluation suite on an image."""
    axes = axes or ["basic", "color", "clip_text"]
    results: dict[str, Any] = {}
    if "basic" in axes:
        results["basic"] = basic_image_metrics(image_path=image_path)
    if "color" in axes:
        results["color"] = color_statistics(image_path=image_path)
    if "clip_text" in axes and prompt and _HAS_CLIP:
        results["clip_text"] = clip_text_similarity(image_path=image_path, text=prompt)
    if "clip_image" in axes and reference_path and _HAS_CLIP:
        results["clip_image"] = clip_image_similarity(image_path_a=image_path, image_path_b=reference_path)

    scores = [v["score"] for v in results.values() if isinstance(v, dict) and "score" in v]
    if scores:
        results["aggregate"] = {"mean": round(sum(scores) / len(scores), 4), "count": len(scores)}
    return {"image_path": image_path, "prompt": prompt, "results": results}


@mcp.tool()
def evaluate_video(video_path: str) -> dict[str, Any]:
    """Evaluate a video file: duration, resolution, fps, bitrate."""
    metrics = video_metrics(video_path)
    return {"video_path": video_path, "results": metrics}


@mcp.tool()
def ascii_art_metrics(ascii_path: str) -> dict[str, Any]:
    """Evaluate ASCII art text file: line count, width, height, density."""
    p = Path(ascii_path)
    if not p.exists():
        return {"axis": "ascii_art", "status": "error", "reason": "file not found"}
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    h = len(lines)
    w = max(len(l) for l in lines) if lines else 0
    density = sum(len(l.strip()) for l in lines) / (w * h) if w * h else 0
    non_ascii_ratio = sum(1 for l in lines for ch in l if ord(ch) > 127) / max(sum(len(l) for l in lines), 1)
    return {
        "axis": "ascii_art",
        "width": w, "height": h,
        "line_count": len(lines),
        "density": round(density, 4),
        "non_ascii_ratio": round(non_ascii_ratio, 4),
    }


@mcp.tool()
def effect_metrics(effect_video_path: str, effect_type: str = "generic") -> dict[str, Any]:
    """Evaluate a video effect output (zanzou, bpy, mediapipe).
    Calls bridge scripts for type-specific metrics."""
    bridges = {
        "zanzou": "/home/bons/evops/skills/effect-eval/scripts/zanzou_bridge.py",
        "bpy": "/home/bons/evops/skills/effect-eval/scripts/bpy_video_bridge.py",
        "mediapipe": "/home/bons/evops/skills/effect-eval/scripts/mediapipe_bridge.py",
    }
    script = bridges.get(effect_type)
    if script:
        result = subprocess.run(["python3", script, effect_video_path], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    # Fallback to generic video metrics
    return video_metrics(effect_video_path)


@mcp.tool()
def evaluate_all(artifacts_dir: str, prompt: str | None = None) -> dict[str, Any]:
    """Batch evaluate all artifacts in a directory."""
    base = Path(artifacts_dir)
    report = {}
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        suffix = p.suffix.lower()
        if suffix in (".png", ".jpg", ".jpeg"):
            report[str(p)] = evaluate_image(str(p), prompt=prompt).get("results", {})
        elif suffix == ".mp4":
            report[str(p)] = evaluate_video(str(p)).get("results", {})
        elif suffix == ".txt":
            report[str(p)] = ascii_art_metrics(str(p))
    return {"artifacts_dir": artifacts_dir, "evaluated": len(report), "report": report}


app = create_mcp_app(mcp, transport="http")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8002)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
