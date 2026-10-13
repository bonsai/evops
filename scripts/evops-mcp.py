#!/usr/bin/env python3
"""evops-mcp — Unified MCP server manager for evops.

Discovers, starts, stops, and health-checks all MCP servers.

Usage:
    python scripts/evops-mcp.py list
    python scripts/evops-mcp.py start <name>
    python scripts/evops-mcp.py start-all [--detach]
    python scripts/evops-mcp.py status
    python scripts/evops-mcp.py stop <name>
    python scripts/evops-mcp.py call <name> <tool> [json-args]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

EVOPS_ROOT = Path("/home/bons/evops")

# Auto-discovered + well-known MCP servers
_DEFAULT_REGISTRY: dict[str, dict[str, int | str]] = {
    "db": {"port": 8001, "path": "mcp/db/server.py"},
    "evaluator": {"port": 8002, "path": "mcp/evaluator/server.py"},
    "gateway": {"port": 8000, "path": "mcp/gateway/server.py"},
    "sf-paper-comic": {"port": 8004, "path": "skills/sf-paper-comic/server.py"},
    "bpy-gen": {"port": 8005, "path": "skills/bpy-gen/server.py"},
    "videogen": {"port": 8006, "path": "skills/videogen/server.py"},
    "artcraft": {"port": 8007, "path": "skills/artcraft/server.py"},
}

_PROCS: dict[str, subprocess.Popen] = {}


def _discover() -> dict[str, dict[str, int | str]]:
    """Auto-discover server.py files under mcp/ and skills/."""
    registry = dict(_DEFAULT_REGISTRY)
    for pattern in ["mcp/*/server.py", "skills/*/server.py"]:
        for p in sorted(EVOPS_ROOT.glob(pattern)):
            name = p.parent.name
            if name in registry:
                continue
            # Try to infer port by reading file
            port = _infer_port(p)
            registry[name] = {"port": port, "path": str(p.relative_to(EVOPS_ROOT))}
    return registry


def _infer_port(path: Path) -> int:
    try:
        text = path.read_text()
        for kw in ["default=800", "port=800", "port:", "port "]:
            if kw in text:
                idx = text.find(kw)
                sub = text[idx : idx + 20]
                digits = "".join(c for c in sub if c.isdigit())
                if len(digits) >= 4:
                    return int(digits[:4])
    except Exception:
        pass
    return 0  # unknown


def _health(name: str, port: int) -> dict[str, Any]:
    try:
        req = urllib.request.Request(f"http://localhost:{port}/health", method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            return {"name": name, "port": port, "status": "ok", "response": json.loads(resp.read().decode())}
    except Exception as e:
        return {"name": name, "port": port, "status": "down", "error": str(e)}


def cmd_list(args: argparse.Namespace):
    registry = _discover()
    print(f"{'NAME':<20} {'PORT':<6} {'PATH'}")
    print("-" * 60)
    for name, info in sorted(registry.items()):
        print(f"{name:<20} {info['port']:<6} {info['path']}")


def cmd_start(args: argparse.Namespace):
    registry = _discover()
    name = args.name
    if name not in registry:
        print(f"Unknown server: {name}", file=sys.stderr)
        sys.exit(1)
    info = registry[name]
    port = int(info["port"])
    spath = EVOPS_ROOT / str(info["path"])
    cmd = [sys.executable, str(spath), "--http", "--port", str(port)]
    print(f"Starting {name} on port {port}...")
    if args.detach:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _PROCS[name] = proc
        print(f"  PID {proc.pid} (detached)")
    else:
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass


def cmd_start_all(args: argparse.Namespace):
    registry = _discover()
    for name, info in sorted(registry.items()):
        if info["port"] == 0:
            continue
        args.name = name
        args.detach = True
        cmd_start(args)
    print(f"\nStarted {len(registry)} servers.")


def cmd_status(args: argparse.Namespace):
    registry = _discover()
    print(f"{'NAME':<20} {'PORT':<6} {'STATUS'}")
    print("-" * 50)
    for name, info in sorted(registry.items()):
        port = int(info["port"])
        if port == 0:
            print(f"{name:<20} {'?':<6} unknown-port")
            continue
        h = _health(name, port)
        status = "ok" if h["status"] == "ok" else f"DOWN ({h.get('error','')})"
        print(f"{name:<20} {port:<6} {status[:40]}")


def cmd_stop(args: argparse.Namespace):
    name = args.name
    if name in _PROCS:
        p = _PROCS[name]
        p.terminate()
        p.wait(timeout=5)
        del _PROCS[name]
        print(f"Stopped {name} (PID {p.pid})")
        return
    print(f"No managed process for {name}. Kill manually or use pkill -f '{name}'")


def cmd_call(args: argparse.Namespace):
    registry = _discover()
    name = args.name
    if name not in registry:
        print(f"Unknown server: {name}", file=sys.stderr)
        sys.exit(1)
    port = int(registry[name]["port"])
    tool = args.tool
    payload = {"name": tool, "arguments": json.loads(args.args or "{}")}
    url = f"http://localhost:{port}/call"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(json.dumps(json.loads(resp.read().decode()), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="evops-mcp: Unified MCP server manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all MCP servers")

    p_start = sub.add_parser("start", help="Start an MCP server")
    p_start.add_argument("name")
    p_start.add_argument("--detach", action="store_true", help="Run in background")

    p_start_all = sub.add_parser("start-all", help="Start all MCP servers")
    p_start_all.add_argument("--detach", action="store_true", default=True)

    sub.add_parser("status", help="Health-check all MCP servers")

    p_stop = sub.add_parser("stop", help="Stop a managed MCP server")
    p_stop.add_argument("name")

    p_call = sub.add_parser("call", help="Call an MCP tool via HTTP")
    p_call.add_argument("name", help="Server name")
    p_call.add_argument("tool", help="Tool name")
    p_call.add_argument("args", nargs="?", default="{}", help="JSON arguments string")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "list": cmd_list,
        "start": cmd_start,
        "start-all": cmd_start_all,
        "status": cmd_status,
        "stop": cmd_stop,
        "call": cmd_call,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
