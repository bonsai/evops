#!/usr/bin/env python3
"""Judge one rendered page with the local VLM (LM Studio, OpenAI-compatible API).

This is the visual gate from the AW: a real VLM inference on a real screenshot.
It is NOT an MCP server; it calls LM Studio's HTTP API directly. Results are
labelled accordingly so a gate is never recorded as "VLM-MCP PASS".

Usage:
    python3 page-tests/vlm_judge.py <page_id> <image.png> [--model ID] [--note TEXT]
"""
from __future__ import annotations

import base64
import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
# VLM 評定：LM Studio 直接 HTTP (デフォルト) または MCP (mcp/evaluator/server.py @port 8007) 経由
# MCP が起動している場合は MCP の evaluate_images_kaggle を優先使用
API = "http://127.0.0.1:1234/v1/chat/completions"
MCP_EVAL_URL = "http://127.0.0.1:8007/evaluate_images_kaggle"  # mcp/evaluator/server.py
DEFAULT_MODEL = "tempura-qwen2.5-vl-3b"

PROMPT = """You are a strict print-layout reviewer. You see one A4 landscape page
from a Japanese graduation-project deck. Judge ONLY what you can actually see.

Report JSON with this exact shape:
{
  "legibility": "PASS|FAIL",
  "clipping": "PASS|FAIL",
  "overlap": "PASS|FAIL",
  "spacing": "PASS|FAIL",
  "contrast": "PASS|FAIL",
  "figure_matches_text": "PASS|FAIL|UNCLEAR",
  "findings": [{"severity":"critical|major|minor","where":"...","evidence":"...","fix":"..."}],
  "confidence": "high|medium|low",
  "summary": "one sentence, Japanese"
}

Rules:
- clipping = any text or diagram cut off by the page edge.
- overlap = elements drawn on top of each other so they cannot both be read.
- legibility = text is readable at this size, no blur from downscaling.
- figure_matches_text = the diagram and the surrounding text describe the same thing.
- If you cannot read the text well enough to judge, say so in summary and set confidence low.
- Do not invent details you cannot see."""


def encode(path: Path, max_side: int = 1400) -> tuple[str, dict]:
    """PNG -> data URI, downscaled so the VLM's vision encoder accepts it.

    The local 3B VLM answers 400 ("failed to process mtmd chunk") for a
    full 2246px render, so the long side is clamped. The scale factor is
    returned and recorded: the judgement is made on the downscaled image.
    """
    original = Image.open(path)
    meta = {"original_size": list(original.size), "sent_size": None, "scale": 1.0}
    image = original
    if max(original.size) > max_side:
        image = original.copy()
        image.thumbnail((max_side, max_side))
        meta["scale"] = round(image.size[0] / original.size[0], 4)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    meta["sent_size"] = list(image.size)
    meta["sent_bytes"] = buf.tell()
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}", meta


def call(model: str, data_uri: str, extra: str = "") -> dict:
    body = {
        "model": model,
        "temperature": 0,
        "max_tokens": 900,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT + extra},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
    }
    req = urllib.request.Request(
        API, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> None:
    page_id = sys.argv[1]
    image = Path(sys.argv[2])
    model = DEFAULT_MODEL
    note = ""
    max_side = 1400
    args = sys.argv[3:]
    for i, a in enumerate(args):
        if a == "--model":
            model = args[i + 1]
        if a == "--note":
            note = args[i + 1]
        if a == "--max-side":
            max_side = int(args[i + 1])
    extra = f"\n\nExtra context: {note}" if note else ""

    data_uri, meta = encode(image, max_side)
    resp = call(model, data_uri, extra)
    text = resp["choices"][0]["message"]["content"]
    out = {
        "engine": "LM Studio /v1/chat/completions (direct HTTP, not MCP)",
        "model": model,
        "page_id": page_id,
        "image": str(image.name),
        "image_bytes": image.stat().st_size,
        "image_meta": meta,
        "raw_response": text,
    }
    target = image.parent / "vlm_judgment.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(text)
    print(f"\n[saved] {target}")


if __name__ == "__main__":
    main()
