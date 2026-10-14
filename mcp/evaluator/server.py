#!/usr/bin/env python3
"""
Artcraft Evaluation MCP — 画像ベースの評価パイプライン
動画 → 画像(SVG/PNG) に切り替え、Kaggle GPU で ML 評価
"""
import json, subprocess, os, sys, tempfile
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, "/home/bons/evops")

# 評価対象の画像ディレクトリ
KAGGLE_SCRIPT = Path("/home/bons/evops/docker/eval_clip_gpu.py")

from fastmcp import FastMCP
mcp = FastMCP("artcraft-eval")

@mcp.tool()
def generate_panel_images(episode_path: str, output_dir: str) -> Dict[str, Any]:
    """episode.json から panel 画像 (PNG/SVG) を生成"""
    with open(episode_path) as f:
        ep = json.load(f)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for i, panel in enumerate(ep.get("panels", []), 1):
        svg_path = out_dir / f"panel_{i:02d}.svg"
        png_path = out_dir / f"panel_{i:02d}.png"
        text = panel.get("text", "")
        speaker = panel.get("speaker", "")
        svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480"><rect width="640" height="480" fill="#1a1a2e"/><text x="320" y="200" font-family="IPAexGothic" font-size="28" fill="#ffd700" text-anchor="middle">{speaker}</text><text x="320" y="260" font-family="IPAexGothic" font-size="20" fill="#fff" text-anchor="middle">{text}</text><text x="320" y="400" font-family="IPAexGothic" font-size="16" fill="#888" text-anchor="middle">Panel {i}/4</text></svg>'
        svg_path.write_text(svg_content, encoding="utf-8")
        generated.append(str(svg_path))
        try:
            subprocess.run(["rsvg-convert", "-o", str(png_path), str(svg_path)], check=True, timeout=30)
            generated.append(str(png_path))
        except:
            pass
    return {"status": "ok", "generated": generated, "count": len(generated)}

@mcp.tool()
def evaluate_images_kaggle(image_dir: str, prompt: str = "quality, composition, relevance") -> Dict[str, Any]:
    """Kaggle GPU で画像評価 (CLIP / BLIP 等)"""
    if not KAGGLE_SCRIPT.exists():
        return {"status": "error", "message": f"Kaggle script not found: {KAGGLE_SCRIPT}"}
    try:
        env = os.environ.copy()
        env["EVAL_PROMPT"] = prompt
        env["EVAL_IMAGE_DIR"] = image_dir
        result = subprocess.run(
            ["python3", str(KAGGLE_SCRIPT)],
            capture_output=True, text=True, timeout=600, env=env
        )
        return {"status": "ok" if result.returncode == 0 else "error", "stdout": result.stdout[-2000:], "stderr": result.stderr[-2000:], "returncode": result.returncode}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def compose_image_grid(image_paths: list, output_path: str, cols: int = 2) -> Dict[str, Any]:
    """複数画像をグリッド結合"""
    if not image_paths:
        return {"status": "error", "message": "No images provided"}
    try:
        cmd = ["montage"] + image_paths + ["-tile", f"{cols}x", "-geometry", "+10+10", "-background", "#1a1a2e", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        success = result.returncode == 0 and Path(output_path).exists()
        return {"status": "ok" if success else "error", "output": output_path, "stderr": result.stderr[-500:]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
def video_to_keyframes(video_path: str, output_dir: str, fps: float = 1.0) -> Dict[str, Any]:
    """動画からキーフレーム抽出（画像化）"""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", f"fps={fps}", str(out_dir / "frame_%04d.png")]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        frames = list(out_dir.glob("frame_*.png"))
        return {"status": "ok" if result.returncode == 0 else "error", "frames": [str(f) for f in frames], "count": len(frames)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8007)
    args = parser.parse_args()
    from mcp_core.base_server import create_mcp_app, run_mcp_server
    app = create_mcp_app(mcp, transport="http")
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
