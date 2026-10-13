"""NDim CLI — MCP サーバ上のツールを CLI から操作する。

    python project/ndim/ndim-cli.py resolve "幅 2.4 メートル"
    python project/ndim/ndim-cli.py build "幅 2.4 メートル、高さ 3 メートル"
    python project/ndim/ndim-cli.py batch-verify fixtures.json
    python project/ndim/ndim-cli.py scene-stats

MCP サーバは事前に起動:
    python project/ndim/tools/ndim_mcp.py
"""
from __future__ import annotations

import argparse
import json
import sys

import requests


BASE = "http://127.0.0.1:8000/call"


def _call(tool: str, arguments: dict) -> dict:
    resp = requests.post(BASE, json={"name": tool, "arguments": arguments}, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"tool {tool} failed: {resp.status_code} {resp.text}")
    return resp.json()


def _main() -> int:
    parser = argparse.ArgumentParser(description="NDim CLI (via MCP)")
    sub = parser.add_subparsers(dest="tool", required=True)

    # resolve / resolve_all
    p = sub.add_parser("resolve", help="自然言語から寸法を 1 つ抽出")
    p.add_argument("text", help="例: 幅 2.4 メートル")

    p = sub.add_parser("resolve-all", help="自然言語から寸法を全て抽出")
    p.add_argument("text", help="例: 幅 2.4 メートル、高さ 3 メートル")

    # build / place / reset
    p = sub.add_parser("build", help="1 つの寸法でオブジェクトを生成")
    p.add_argument("text", help="例: 幅 2.4 メートル")
    p.add_argument("--shape", choices=["cube", "cylinder", "plane"], default="cube")

    p = sub.add_parser("place", help="count 個を隙間を空けて配置")
    p.add_argument("text", help="例: 幅 1 メートル")
    p.add_argument("count", type=int)
    p.add_argument("--gap", type=float, default=0.2)
    p.add_argument("--shape", choices=["cube", "cylinder", "plane"], default="cube")

    p = sub.add_parser("reset", help="シーンを空にする")

    # modify (relative)
    p = sub.add_parser("modify", help="既存オブジェクトに変化を適用")
    p.add_argument("target", help="オブジェクト名")
    p.add_argument("kind", choices=["bevel", "scale", "move", "rotate"])
    p.add_argument("--amount", type=float, default=0.0)
    p.add_argument("--delta", nargs=3, type=float, default=[0.0, 0.0, 0.0])

    # verify / batch-verify / scene-stats
    p = sub.add_parser("verify", help="生成物の尺度を検証")
    p.add_argument("text", help="例: 幅 2.4 メートル")
    p.add_argument("expected_m", type=float)
    p.add_argument("--tol-m", type=float, default=0.001)

    p = sub.add_parser("batch-verify", help="複数フィクスチャで一括検証")
    p.add_argument("fixtures", type=str, help="fixtures.json のパス（標準入力の '-' も可）")

    p = sub.add_parser("scene-stats", help="現在のシーンを統計")

    args = parser.parse_args()

    if args.tool == "resolve":
        print(json.dumps(_call("resolve", {"text": args.text}), ensure_ascii=False, indent=2))
    elif args.tool == "resolve-all":
        print(json.dumps(_call("resolve-all", {"text": args.text}), ensure_ascii=False, indent=2))
    elif args.tool == "build":
        print(json.dumps(_call("build", {"text": args.text, "shape": args.shape}), ensure_ascii=False, indent=2))
    elif args.tool == "place":
        print(json.dumps(_call("place", {"text": args.text, "count": args.count, "gap": args.gap, "shape": args.shape}), ensure_ascii=False, indent=2))
    elif args.tool == "reset":
        print(json.dumps(_call("reset_scene", {}), ensure_ascii=False, indent=2))
    elif args.tool == "modify":
        print(json.dumps(_call("modify", {"target": args.target, "kind": args.kind, "amount": args.amount, "delta": args.delta}), ensure_ascii=False, indent=2))
    elif args.tool == "verify":
        print(json.dumps(_call("verify", {"text": args.text, "expected_m": args.expected_m, "tol_m": args.tol_m}), ensure_ascii=False, indent=2))
    elif args.tool == "batch-verify":
        src = sys.stdin if args.fixtures == "-" else args.fixtures
        fixtures = json.load(open(src, encoding="utf-8"))
        print(json.dumps(_call("batch-verify", {"fixtures": fixtures}), ensure_ascii=False, indent=2))
    elif args.tool == "scene-stats":
        print(json.dumps(_call("scene-stats", {}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
