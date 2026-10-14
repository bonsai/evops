#!/usr/bin/env python3
"""MCP Server manager — list, start, stop, status, call."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

# allow running before evops root is on PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skills.cli_mcp.config import MCP_SERVERS, EVOPS_ROOT


def _run(cmd: list[str], cwd: Path = EVOPS_ROOT, check: bool = False):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def list_servers():
    print(f"{'NAME':<20} {'PORT':>6} {'PATH'}")
    print("-" * 60)
    for name, info in MCP_SERVERS.items():
        print(f"{name:<20} {info['port']:>6} {info['path']}")


def start_server(name: str):
    if name not in MCP_SERVERS:
        print(f"Unknown server: {name}")
        return 1
    info = MCP_SERVERS[name]
    port = info["port"]
    script = EVOPS_ROOT / info["path"]
    print(f"Starting {name} on port {port} …")
    cmd = [sys.executable, str(script), "--http", "--port", str(port)]
    subprocess.Popen(
        cmd, cwd=EVOPS_ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    time.sleep(2)
    # health check
    try:
        import urllib.request
        with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=3) as r:
            print(f"  ✅ {name} healthy ({r.status})")
    except Exception as e:
        print(f"  ⚠️  {name} may still be starting ({e})")
    return 0


def start_all():
    for name in MCP_SERVERS:
        start_server(name)
    return 0


def status():
    import urllib.request
    print(f"{'NAME':<20} {'PORT':>6} {'STATUS'}")
    print("-" * 50)
    for name, info in MCP_SERVERS.items():
        port = info["port"]
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=2) as r:
                print(f"{name:<20} {port:>6} 🟢 OK")
        except Exception:
            print(f"{name:<20} {port:>6} 🔴 DOWN")
    return 0


def stop():
    for name, info in MCP_SERVERS.items():
        port = info["port"]
        _run(["pkill", "-f", f"--port.*{port}"])
        print(f"Stopped {name} (port {port})")
    return 0


def call_tool(server: str, tool: str, args_json: str):
    if server not in MCP_SERVERS:
        print(f"Unknown server: {server}")
        return 1
    port = MCP_SERVERS[server]["port"]
    payload = {"tool": tool, "args": json.loads(args_json)}
    body = json.dumps(payload).encode()
    import urllib.request
    req = urllib.request.Request(
        f"http://localhost:{port}/call",
        data=body, headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(r.read().decode())
    except Exception as e:
        print(f"Error calling {server}/{tool}: {e}")
    return 0


# CLI entry-point for back-compat
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="EvOps MCP Manager")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List registered MCP servers")
    p_start = sub.add_parser("start", help="Start a specific MCP server")
    p_start.add_argument("name")
    sub.add_parser("start-all", help="Start all MCP servers")
    sub.add_parser("status", help="Check all server health")
    sub.add_parser("stop", help="Stop all MCP servers")
    p_call = sub.add_parser("call", help="Call an MCP tool")
    p_call.add_argument("server")
    p_call.add_argument("tool")
    p_call.add_argument("args", default="{}")

    args = parser.parse_args()
    cmds = {
        "list": list_servers,
        "start": lambda: start_server(args.name),
        "start-all": start_all,
        "status": status,
        "stop": stop,
        "call": lambda: call_tool(args.server, args.tool, args.args),
    }
    fn = cmds.get(args.cmd)
    if fn:
        sys.exit(fn())
    else:
        parser.print_help()
        sys.exit(1)
