#!/usr/bin/env python3
"""
Unified EvOps CLI — 統合コマンドラインインターフェース
Usage:
    evops mcp list
    evops mcp start-all
    evops mcp status
    evops evolve --concept donpen --iterations 5
    evops pipeline render --paper-id S01
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure evops root is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skills.cli_mcp import mcp_manager
from skills.evolve.loop import run as evolve_run


def _mcp_cmd(args):
    cmds = {
        "list":      mcp_manager.list_servers,
        "start":     lambda: mcp_manager.start_server(args.name),
        "start-all": mcp_manager.start_all,
        "status":    mcp_manager.status,
        "stop":      mcp_manager.stop,
        "call":      lambda: mcp_manager.call_tool(args.server, args.tool, args.args_json),
    }
    fn = cmds.get(args.mcp_action)
    if fn:
        return fn()
    print(f"Unknown mcp action: {args.mcp_action}")
    return 1


def _evolve_cmd(args):
    evolve_run(
        concept=args.concept,
        max_iterations=args.iterations,
        target_score=args.target,
        output_dir=args.output_dir,
    )
    return 0


def _pipeline_cmd(args):
    print("Pipeline commands: Coming soon")
    print(f"  Paper ID requested: {getattr(args, 'paper_id', 'n/a')}")
    return 0


def _youtube_cmd(args):
    print("YouTube skill — available tools:")
    print("  upload_video_tool(video_path, title)")
    print("  generate_thumbnail_tool(concept, output_path)")
    print(f"  Server: skills/youtube/server.py (port 8011)")
    return 0


def _sdk_cmd(args):
    print("SDK skill — available tools:")
    print("  get_client_config_tool()")
    print("  render_remote_tool(concept, format)")
    print("  Server: skills/sdk/server.py (port 8012)")
    return 0


def _lms_cmd(args):
    print("LMS skill — available tools:")
    print("  submit_training_job_tool(dataset_path, model)")
    print("  get_eval_curriculum_tool()")
    print("  Server: skills/lms/server.py (port 8013)")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="evops",
        description="EvOps — Evaluate Operations unified CLI",
    )
    sub = parser.add_subparsers(dest="command")

    # ... subparsers same as before ...
    # ── mcp ──
    p_mcp = sub.add_parser("mcp", help="MCP server management")
    mcp_sub = p_mcp.add_subparsers(dest="mcp_action")
    mcp_sub.add_parser("list", help="List registered servers")
    mcp_sub.add_parser("start-all", help="Start all servers")
    mcp_sub.add_parser("status", help="Check server health")
    mcp_sub.add_parser("stop", help="Stop all servers")
    p_start = mcp_sub.add_parser("start", help="Start a server")
    p_start.add_argument("name")
    p_call = mcp_sub.add_parser("call", help="Call an MCP tool")
    p_call.add_argument("server")
    p_call.add_argument("tool")
    p_call.add_argument("args_json", default="{}")

    # ── evolve ──
    p_evo = sub.add_parser("evolve", help="Run evolution loop")
    p_evo.add_argument("--concept",    default="don_quixote")
    p_evo.add_argument("--iterations", type=int, default=5)
    p_evo.add_argument("--target",     type=int, default=75)
    p_evo.add_argument("--output-dir", type=Path, default=None)

    # ── pipeline ──
    p_pipe = sub.add_parser("pipeline", help="Pipeline operations")
    pipe_sub = p_pipe.add_subparsers(dest="pipe_action")
    p_render = pipe_sub.add_parser("render", help="Render paper comics")
    p_render.add_argument("--paper-id", default="S01")

    # ── youtube ──
    p_yt = sub.add_parser("youtube", help="YouTube content tools")
    yt_sub = p_yt.add_subparsers(dest="yt_action")
    yt_sub.add_parser("setup", help="Show Blender MCP setup guide")
    yt_sub.add_parser("narrate", help="Extract narration text")

    # ── sdk ──
    p_sdk = sub.add_parser("sdk", help="SDK skill tools")
    sdk_sub = p_sdk.add_subparsers(dest="sdk_action")
    sdk_sub.add_parser("config", help="Show SDK config")

    # ── lms ──
    p_lms = sub.add_parser("lms", help="LMS skill tools")
    lms_sub = p_lms.add_subparsers(dest="lms_action")
    lms_sub.add_parser("curriculum", help="Show eval curriculum")

    args = parser.parse_args(argv)

    # Back-compat: bare mcp commands (e.g., "evops-mcp status")
    bare_mcp_cmds = {"list", "start", "start-all", "status", "stop", "call"}
    if args.command is None and argv and argv[0] in bare_mcp_cmds:
        args.command = "mcp"
        args.mcp_action = argv[0]
        if args.mcp_action == "start":
            args.name = argv[1] if len(argv) > 1 else None
        elif args.mcp_action == "call":
            args.server = argv[1] if len(argv) > 1 else None
            args.tool = argv[2] if len(argv) > 2 else None
            args.args_json = argv[3] if len(argv) > 3 else "{}"
        else:
            args.name = args.server = args.tool = args.args_json = None

    dispatch = {
        "mcp":      _mcp_cmd,
        "evolve":   _evolve_cmd,
        "pipeline": _pipeline_cmd,
        "youtube":  _youtube_cmd,
        "sdk":      _sdk_cmd,
        "lms":      _lms_cmd,
    }
    fn = dispatch.get(args.command)
    if fn:
        return fn(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
