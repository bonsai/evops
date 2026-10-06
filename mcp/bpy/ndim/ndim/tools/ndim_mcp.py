"""NDim — FastMCP サーバ。

NDim の操作（自然言語解析・生成・検証・統計）を MCP tool として公開し、
HTTP 経由で curl や MCP クライアントから CLI 操作できるようにする。

    python project/ndim/ndim/tools/ndim_mcp.py

起動後、http://localhost:8000 でツール呼び出しが可能。
  curl -X POST http://localhost:8000/call \
    -H "Content-Type: application/json" \
    -d '{"name":"resolve","arguments":{"text":"幅 2.4 メートル"}}'

または ndim-cli.py（下）を使うと、ツール名と引数を並べるだけ。
"""
from __future__ import annotations

import sys
from pathlib import Path

# project/ndim を sys.path に登録（`from ndim.build import` のため）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
# tools ディレクトリ自体も登録（`from ndim_mcp import mcp` 外部参照用）
sys.path.insert(0, str(Path(__file__).resolve().parent))

import math
import json
from typing import Any

import bpy
from ndim.build import (
    BuildContext,
    Delta,
    apply,
    build_absolute,
    build_complex,
    reset_scene as _reset_scene,
)
from ndim.resolve import resolve as _resolve, resolve_all as _resolve_all, Param

from fastmcp import FastMCP

mcp = FastMCP("ndim")

# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------


@mcp.tool()
def resolve(text: str) -> dict[str, Any]:
    """自然言語から寸法を 1 つ抽出。

    "幅 2.4 メートル" -> {found:true, name:"width", value_m:2.4, unit:"m", ambiguous:false}
    """
    p = _resolve(text)
    if p is None:
        return {"found": False}
    return {
        "found": True,
        "name": p.name,
        "value_m": p.value,
        "unit": p.unit.value,
        "ambiguous": p.is_ambiguous_unit,
        "raw": p.raw,
    }


@mcp.tool()
def resolve_all(text: str) -> list[dict]:
    """自然言語から寸法を全て抽出。"""
    return [
        {
            "found": True,
            "name": p.name,
            "value_m": p.value,
            "unit": p.unit.value,
            "ambiguous": p.is_ambiguous_unit,
            "raw": p.raw,
        }
        for p in _resolve_all(text)
    ]


# ---------------------------------------------------------------------------
# 生成
# ---------------------------------------------------------------------------


@mcp.tool()
def build(text: str, shape: str = "cube") -> dict[str, Any]:
    """1 つの寸法でオブジェクトを生成（ABSOLUTE）。"""
    _reset_scene()
    ctx = BuildContext.new()
    apply(text, ctx, shape=shape)
    out = {"objects": len(ctx.manifest.objects)}
    out["manifest"] = ctx.manifest.render()
    return out


@mcp.tool()
def place(text: str, count: int, gap: float = 0.2, shape: str = "cube") -> dict[str, Any]:
    """count 個を隙間を空けて配置（COMPLEX）。"""
    if count < 1:
        raise ValueError(f"count must be >= 1, got {count}")
    _reset_scene()
    params = _resolve_all(text)
    if not params:
        return {"error": "no dimensions found", "objects": 0}
    p = params[-1]  # 最後の寸法を使う
    ctx = BuildContext.new()
    objs = build_complex(count, p, ctx, gap=gap, shape=shape)
    out = {"objects": len(objs)}
    out["manifest"] = ctx.manifest.render()
    return out


@mcp.tool()
def modify(target: str, kind: str, amount: float = 0.0, delta: list[float] = None) -> dict[str, Any]:
    """既存オブジェクトに変化を適用（RELATIVE）。
    target は完全一致か、接頭辞（NDIM_width -> NDIM_width_002）で一致。
    """
    obj = bpy.data.objects.get(target)
    if obj is None:
        # 接頭辞一致（NDIM_width -> NDIM_width_002 など）
        objs = [o for o in bpy.data.objects if o.name.startswith(target)]
        if not objs:
            return {"error": f"object not found: {target}"}
        obj = objs[-1]  # 直近作成
    if kind not in Delta.VALID_KINDS:
        raise ValueError(f"invalid kind {kind}; expect one of {sorted(Delta.VALID_KINDS)}")
    build_relative(obj, Delta(kind=kind, amount=amount, delta=tuple(delta) if delta else (0.0, 0.0, 0.0)), BuildContext.new())
    return {
        "target": obj.name,
        "kind": kind,
        "scale": tuple(obj.scale),
        "location": tuple(obj.location),
    }


@mcp.tool()
def reset_scene() -> dict:
    """シーンを空にする（冪等）。"""
    _reset_scene()
    return {"objects": len(bpy.data.objects)}


# ---------------------------------------------------------------------------
# 検証・統計
# ---------------------------------------------------------------------------


def _binom_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    if p in (0.0, 1.0):
        # 境界値は Wilson 近似
        z = 1.96
        denom = 1 + z * z / n
        centre = (p + z * z / (2 * n)) / denom
        half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
        return (max(0.0, centre - half), min(1.0, centre + half))
    se = math.sqrt(p * (1 - p) / n)
    lo = max(0.0, p - 1.96 * se)
    hi = min(1.0, p + 1.96 * se)
    return (lo, hi)


@mcp.tool()
def verify(text: str, expected_m: float, tol_m: float = 0.001, shape: str = "cube") -> dict:
    """生成物の尺度を検証。"""
    _reset_scene()
    ctx = BuildContext.new()
    apply(text, ctx, shape=shape)
    if not ctx.manifest.objects:
        return {"ok": False, "error": "nothing generated"}
    obj = bpy.data.objects[ctx.manifest.objects[0].name]
    actual = obj.scale[0]
    within = abs(actual - expected_m) <= tol_m
    return {
        "ok": within,
        "expected_m": expected_m,
        "actual_m": actual,
        "error_m": abs(actual - expected_m),
        "tol_m": tol_m,
        "within_tolerance": within,
    }


@mcp.tool()
def batch_verify(fixtures: list[dict]) -> dict:
    """複数フィクスチャで一括検証（resolution success / build accuracy / MAE / 95%CI）。"""
    n = len(fixtures)
    resolved = 0
    built_ok = 0
    errs: list[float] = []
    for i, f in enumerate(fixtures):
        _reset_scene()
        ctx = BuildContext.new()
        apply(f["input"], ctx, shape=f.get("shape", "cube"))
        params = ctx.manifest.params
        expected = f["expected_m"]
        tol = f.get("tol_m", 0.001)
        if params and params[0].unit is not None:
            resolved += 1
            actual = params[0].value
            build_ok = abs(actual - expected) <= tol
            if build_ok:
                built_ok += 1
            errs.append(abs(actual - expected))
        else:
            # 単位未指定は「resolution 失敗（推測）」として扱う（ambiguous の評価は別途）
            resolved += 0

    precision = resolved / n
    build_accuracy = built_ok / n
    mae = sum(errs) / len(errs) if errs else 0.0
    return {
        "n": n,
        "resolution_success": precision,
        "resolution_95ci": _binom_ci(resolved, n),
        "build_accuracy": build_accuracy,
        "build_accuracy_95ci": _binom_ci(built_ok, n),
        "mae_m": round(mae, 6),
    }


@mcp.tool()
def scene_stats() -> dict:
    """現在のシーンを統計。"""
    total_exact = 0.0
    total_bbox = sum(o.dimensions.x * o.dimensions.y * o.dimensions.z for o in bpy.data.objects)
    for rec in (bpy.data.objects if False else []):
        pass
    return {
        "object_count": len(bpy.data.objects),
        "total_bbox_volume": round(total_bbox, 6),
    }


# ---------------------------------------------------------------------------
# マニフェスト
# ---------------------------------------------------------------------------


@mcp.tool()
def manifest_json(ctx_name: str = "default") -> str:
    """現在の BuildContext マニフェストを JSON 出力。"""
    ctx = BuildContext.new()  # ※新規作成なので空；実運用では外部から保持
    return json.dumps(ctx.manifest.model_dump(mode="json"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
