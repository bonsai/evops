#!/usr/bin/env python3
"""evops-mcp — Unified MCP server manager for evops."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time, urllib.request
from pathlib import Path
from typing import Any

EVOPS_ROOT = Path("/home/bons/evops")
_DEFAULT_REGISTRY = {
    "db": {"port": 8001, "path": "mcp/db/server.py"},
    "evaluator": {"port": 8002, "path": "mcp/evaluator/server.py"},
    "gateway": {"port": 8000, "path": "mcp/gateway/server.py"},
    "sf-paper-comic": {"port": 8004, "path": "skills/sf-paper-comic/server.py"},
    "bpy-gen": {"port": 8005, "path": "skills/bpy-gen/server.py"},
    "videogen": {"port": 8006, "path": "skills/videogen/server.py"},
    "artcraft": {"port": 8007, "path": "skills/artcraft/server.py"},
}

def _discover():
    registry = dict(_DEFAULT_REGISTRY)
    for pattern in ["mcp/*/server.py", "skills/*/server.py"]:
        for p in sorted(EVOPS_ROOT.glob(pattern)):
            name = p.parent.name
            if name not in registry:
                registry[name] = {"port": 0, "path": str(p.relative_to(EVOPS_ROOT))}
    return registry

def _health(name, port):
    try:
        req = urllib.request.Request(f"http://localhost:{port}/health", method="GET")
        with urllib.request.urlopen(req, timeout=1) as resp:
            return {"name": name, "port": port, "status": "ok"}
    except: return {"name": name, "port": port, "status": "down"}

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    p_list = sub.add_parser("list")
    p_list.add_argument("--json", action="store_true")
    p_start = sub.add_parser("start")
    p_start.add_argument("name")
    p_start.add_argument("--detach", action="store_true")
    sub.add_parser("status")
    p_stop = sub.add_parser("stop")
    p_stop.add_argument("name")
    p_call = sub.add_parser("call")
    p_call.add_argument("name")
    p_call.add_argument("tool")
    p_call.add_argument("args", nargs="?", default="{}")

    args = parser.parse_args()
    reg = _discover()
    if args.command == "list":
        if getattr(args, "json", False): print(json.dumps(reg, indent=2))
        else:
            print(f"{'NAME':<20} {'PORT':<6} {'PATH'}")
            for n, i in sorted(reg.items()): print(f"{n:<20} {i['port']:<6} {i['path']}")
    elif args.command == "status":
        for n, i in sorted(reg.items()):
            h = _health(n, i["port"])
            print(f"{n:<20} {i['port']:<6} {h['status']}")
    elif args.command == "start":
        info = reg[args.name]
        cmd = [sys.executable, str(EVOPS_ROOT/info["path"]), "--http", "--port", str(info["port"])]
        if args.detach: subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else: subprocess.run(cmd)
    elif args.command == "call":
        port = reg[args.name]["port"]
        req = urllib.request.Request(f"http://localhost:{port}/mcp/call", data=json.dumps({"name": args.tool, "arguments": json.loads(args.args)}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp: print(resp.read().decode())

if __name__ == "__main__":
    main()
