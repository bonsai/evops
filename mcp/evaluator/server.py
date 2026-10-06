"""Lightweight image evaluation MCP server.

Runs on CPU with small models. Provides:
- CLIP text-image similarity
- CLIP image-image similarity
- Basic image metrics (size, aspect ratio, color stats)
- Perceptual metrics (SSIM-style via simple pixel stats)

Run:
    python mcp/evaluator/server.py

Query:
    curl -X POST http://localhost:8002/call \
      -H "Content-Type: application/json" \
      -d '{"name":"clip_text_similarity","arguments":{"image_path":"/path/to/img.png","text":"a cute character"}}'
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from fastmcp import FastMCP

try:
    import torch
    from transformers import CLIPProcessor, CLIPModel
    _HAS_CLIP = True
except ImportError:
    _HAS_CLIP = False
    CLIPModel = None  # type: ignore
    CLIPProcessor = None  # type: ignore

mcp = FastMCP("sotsusei-evaluator")

# Lazy-loaded CLIP cache
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
        "capabilities": [
            "clip_text_similarity",
            "clip_image_similarity",
            "basic_image_metrics",
            "color_statistics",
        ],
    }


@mcp.tool()
def clip_text_similarity(
    image_path: str,
    text: str,
    model_name: str = "openai/clip-vit-base-patch32",
) -> dict[str, Any]:
    """Compute CLIP cosine similarity between an image and a text prompt.

    Returns a score roughly in [-1, 1]; higher means more aligned.
    """
    model, processor = _load_clip(model_name)
    image = _load_image(image_path)
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        score = logits_per_image.item() / 100.0
    return {
        "axis": "clip_text_similarity",
        "score": score,
        "model": model_name,
        "prompt": text,
    }


@mcp.tool()
def clip_image_similarity(
    image_path_a: str,
    image_path_b: str,
    model_name: str = "openai/clip-vit-base-patch32",
) -> dict[str, Any]:
    """Compute CLIP cosine similarity between two images."""
    model, processor = _load_clip(model_name)
    img_a = _load_image(image_path_a)
    img_b = _load_image(image_path_b)
    inputs = processor(images=[img_a, img_b], return_tensors="pt", padding=True)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        a = image_features[0]
        b = image_features[1]
        cos = torch.nn.functional.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0))
    return {
        "axis": "clip_image_similarity",
        "score": cos.item(),
        "model": model_name,
    }


@mcp.tool()
def basic_image_metrics(image_path: str) -> dict[str, Any]:
    """Return basic non-ML metrics: width, height, aspect ratio, file size."""
    p = Path(image_path)
    img = _load_image(image_path)
    w, h = img.size
    aspect = round(w / h, 4) if h else 0.0
    return {
        "axis": "basic_metrics",
        "width": w,
        "height": h,
        "aspect_ratio": aspect,
        "file_size_bytes": p.stat().st_size if p.exists() else None,
        "megapixels": round((w * h) / 1_000_000, 3),
    }


@mcp.tool()
def color_statistics(image_path: str) -> dict[str, Any]:
    """Return mean color, brightness, saturation hints from a resized image."""
    img = _load_image(image_path, size=(224, 224))
    arr = np.array(img).astype(np.float32) / 255.0
    mean_rgb = arr.mean(axis=(0, 1)).tolist()
    brightness = float(arr.mean())
    std = float(arr.std())
    # Simple colorfulness proxy: average channel std
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
    """Run a configurable evaluation suite on an image.

    axes: list of metric names. If None, runs all available metrics.
    """
    axes = axes or ["basic", "color", "clip_text"]
    results: dict[str, Any] = {}

    if "basic" in axes:
        results["basic"] = basic_image_metrics(image_path=image_path)
    if "color" in axes:
        results["color"] = color_statistics(image_path=image_path)
    if "clip_text" in axes and prompt:
        if _HAS_CLIP:
            results["clip_text"] = clip_text_similarity(
                image_path=image_path, text=prompt
            )
        else:
            results["clip_text"] = {"error": "CLIP not installed"}
    if "clip_image" in axes and reference_path:
        if _HAS_CLIP:
            results["clip_image"] = clip_image_similarity(
                image_path_a=image_path, image_path_b=reference_path
            )
        else:
            results["clip_image"] = {"error": "CLIP not installed"}

    # Compute a simple aggregate if possible
    scores = []
    for v in results.values():
        if isinstance(v, dict) and "score" in v:
            scores.append(v["score"])
    if scores:
        results["aggregate"] = {
            "mean": round(sum(scores) / len(scores), 4),
            "count": len(scores),
        }

    return {"image_path": image_path, "prompt": prompt, "results": results}


if __name__ == "__main__":
    # stdio is the standard MCP transport; clients connect via MCP client SDK.
    mcp.run(transport="stdio")
