from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")
import subprocess, os, json, tempfile
from pathlib import Path
from fastmcp import FastMCP
from mcp_core.base_server import create_mcp_app, run_mcp_server

mcp = FastMCP("bpy-gen")
HERE = Path(__file__).resolve().parent
BLENDER = os.environ.get("BLENDER_EXECUTABLE", "blender")

@mcp.tool()
def render_doraemon(output_path: str = "/tmp/bpy_gen_doraemon.png") -> dict:
    cmd = [BLENDER, "--background", "--python", str(HERE/"tools/doraemon_bpy.py"), "--", "--output", output_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {"status":"ok" if r.returncode==0 else "error","output_path":output_path,"returncode":r.returncode,"stderr_tail":r.stderr[-500:]}

@mcp.tool()
def render_pagoda(output_path: str = "/tmp/bpy_gen_pagoda.png") -> dict:
    cmd = [BLENDER, "--background", "--python", str(HERE/"tools/pagoda_bpy.py"), "--", "--output", output_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {"status":"ok" if r.returncode==0 else "error","output_path":output_path,"returncode":r.returncode,"stderr_tail":r.stderr[-500:]}

@mcp.tool()
def render_bear(output_path: str = "/tmp/bpy_gen_bear.png") -> dict:
    cmd = [BLENDER, "--background", "--python", str(HERE/"tools/bear_bpy.py"), "--", "--output", output_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {"status":"ok" if r.returncode==0 else "error","output_path":output_path,"returncode":r.returncode,"stderr_tail":r.stderr[-500:]}

@mcp.tool()
def bpy_gen_dsl(dsl_json: str = '{"objects":[{"mesh":"cube","loc":[0,0,0],"scale":2}],"render":{"res":[512,512],"file":"/tmp/bpy_dsl.png"}}') -> dict:
    """DSL → AST → IR で bpy 生成。dsl_json はシーン記述の JSON 文字列。"""
    dsl = json.loads(dsl_json)
    objects = dsl.get("objects", [])
    ir_lines = [
        "import bpy",
        "bpy.ops.object.select_all(action='SELECT')",
        "bpy.ops.object.delete(use_global=False)",
    ]
    for o in objects:
        mesh = o.get("mesh", "cube")
        loc = o.get("loc", [0, 0, 0])
        scale = o.get("scale", 1)
        ir_lines.append(
            f"bpy.ops.mesh.primitive_{mesh}_add(size={scale}, location=({loc[0]},{loc[1]},{loc[2]}))"
        )
    render_cfg = dsl.get("render", {})
    out_path = render_cfg.get("file", "/tmp/bpy_dsl.png")
    res = render_cfg.get("res", [512, 512])
    ir_lines.extend([
        "bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'",
        f"bpy.context.scene.render.resolution_x = {res[0]}",
        f"bpy.context.scene.render.resolution_y = {res[1]}",
        f"bpy.context.scene.render.filepath = '{out_path}'",
        "bpy.ops.render.render(write_still=True)",
        f"print('OUT:', '{out_path}')",
    ])
    ir_script = "\n".join(ir_lines)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(ir_script)
        sp = f.name
    try:
        res_sub = subprocess.run(["blender", "-b", "--python", sp], capture_output=True, text=True, timeout=60)
        ok = os.path.exists(out_path)
        return {
            "ok": ok and res_sub.returncode == 0,
            "dsl_ast": dsl,
            "dsl_ir": ir_script,
            "image_path": out_path if ok else None,
            "stdout_tail": res_sub.stdout[-200:] if len(res_sub.stdout) > 200 else res_sub.stdout,
            "stderr_tail": res_sub.stderr[-200:] if len(res_sub.stderr) > 200 else res_sub.stderr,
        }
    finally:
        os.unlink(sp)

@mcp.tool()
def list_tools() -> dict:
    return {
        "tools": [
            "render_doraemon — fixed character script",
            "render_pagoda — fixed pagoda script",
            "render_bear — fixed bear script",
            "bpy_gen_dsl — procedural DSL-to-Blender generation",
        ],
        "note": "bpy_gen_dsl is the generic entrypoint; render_* are legacy presets"
    }

app = create_mcp_app(mcp, transport="http")
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8005)
    args = parser.parse_args()
    if args.http:
        run_mcp_server(mcp, port=args.port, transport="http")
    else:
        mcp.run(transport="stdio")
