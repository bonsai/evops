from __future__ import annotations
import sys
sys.path.insert(0, "/home/bons/evops")
sys.path.insert(0, "/home/bons/paper-survey-agent/src")
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

from survey_agent.digester.manager import EvOpsSurveyManager

mcp = FastMCP("paper-digest")
manager = EvOpsSurveyManager()

@mcp.tool()
def digest_paper(text: str, title: str = "Untitled Paper", domain: str = "comic") -> dict:
    """
    論文テキストをユニバーサルに分解・咀嚼し、指定したドメイン（漫才/4コマ/note/youtube）に変換します。
    """
    res = manager.process_paper(text, title, domain)
    if "error" in res:
        return {"status": "error", "message": res["error"]}
    
    return {
        "status": "ok",
        "domain": res["domain"],
        "output": res["result"],
        "seed_json": res["digested_seed"]
    }

@mcp.tool()
def list_domains() -> dict:
    """利用可能な変換ドメインを返します。"""
    return {
        "domains": list(manager.adapters.keys()),
        "description": "comic: 4コマ漫画, manzai: 漫才, note: 解説記事, youtube: 動画構成案"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
