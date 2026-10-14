#!/usr/bin/env python3
"""
Evolution Dashboard Server
FastAPI (HTTP + OpenAPI) + FastMCP (stdio)
Visualize generation-by-generation evaluate-and-evolve results.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, "/home/bons/evops")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel

# ── Pydantic Models ────────────────────────────────────────────

class AttrCheck(BaseModel):
    attribute: str
    status: str
    score: float

class Suggestion(BaseModel):
    axis: str
    priority: str
    issue: str
    action: str
    payload: dict | None = None

class EvalResult(BaseModel):
    generation: str
    score: int
    max_score: int
    grade: str
    attribute_check: list[AttrCheck]
    attribute_ratio: float
    prompt_score: float
    missing_attributes: list[str]
    suggestions: list[Suggestion]
    converged: bool

class Iteration(BaseModel):
    iteration: int
    generation_id: str
    prompt: str
    score: int
    grade: str
    eval: EvalResult

class ReferenceConcept(BaseModel):
    title: str
    attributes: dict[str, str]
    mood: str
    reference_images: list[str]

class EvolutionReport(BaseModel):
    concept: str
    target_score: int
    max_iterations: int
    iterations: list[Iteration]
    final_score: int
    converged: bool
    reference_concept: ReferenceConcept


# ── Report Discovery ───────────────────────────────────────────

EVOLUTION_DIR = Path("/home/bons/evops/outputs/evolution")


def discover_reports() -> list[Path]:
    """outputs/evolution 以下の全レポートを発見"""
    if not EVOLUTION_DIR.exists():
        return []
    reports = sorted(EVOLUTION_DIR.rglob("*_evolution_report.json"))
    return reports


def load_latest_report() -> dict[str, Any]:
    reports = discover_reports()
    if not reports:
        return {}
    with open(reports[-1], "r", encoding="utf-8") as f:
        return json.load(f)


def load_report_by_concept(concept: str) -> dict[str, Any]:
    for r in discover_reports():
        if concept in r.name:
            with open(r, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}


# ── HTML Dashboard ─────────────────────────────────────────────

DASHBOARD_HTML = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Evolution Dashboard</title>
<style>
  :root { --bg:#0f0f12; --fg:#e8e8ec; --accent:#7c3aed; --ok:#3a3; --warn:#f66; --card:#1a1a20; }
  body { background:var(--bg); color:var(--fg); font-family:system-ui,"Noto Sans JP",sans-serif; margin:0; padding:32px; }
  h1 { font-size:28px; margin-bottom:8px; }
  .meta { color:#666; font-size:14px; margin-bottom:24px; }
  .gen-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:16px; }
  .gen-card { background:var(--card); border:1px solid #2a2a32; border-radius:14px; padding:20px; }
  .gen-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
  .gen-title { font-size:18px; font-weight:700; }
  .score { font-size:24px; font-weight:800; }
  .score.A { color:var(--ok); }
  .score.B { color:#6f6; }
  .score.C { color:#ff6; }
  .score.D { color:var(--warn); }
  .badge { font-size:11px; padding:2px 8px; border-radius:4px; background:#333; color:#aaa; }
  .converged { background:var(--ok); color:#fff; }
  .prompt-box { background:#222; border-radius:8px; padding:12px; font-size:13px; color:#bbb; margin:10px 0; line-height:1.5; word-break:break-all; }
  .attr-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(90px, 1fr)); gap:6px; margin-top:10px; }
  .attr { font-size:12px; padding:4px 8px; border-radius:4px; text-align:center; }
  .attr.ok { background:#1a3a1a; color:#5a5; }
  .attr.miss { background:#3a1a1a; color:#a55; }
  .suggestions { margin-top:10px; }
  .sug { font-size:12px; color:#a88; margin:3px 0; padding-left:12px; border-left:2px solid #533; }
</style>
</head>
<body>
<h1>🧬 Evolution Dashboard</h1>
<p class="meta">Concept: <strong>__CONCEPT__</strong> ｜ Target: __TARGET__ ｜ Iterations: __TOTAL__ ｜ Final Score: __FINAL__ ｜ Converged: __CONVERGED__</p>
<div class="gen-grid">
__GEN_CARDS__
</div>
<script>
setTimeout(() => location.reload(), 10000);
</script>
</body>
</html>
"""


def render_attr_badge(check: dict) -> str:
    cls = "ok" if check["status"] == "present" else "miss"
    return f'<div class="attr {cls}">{check["attribute"]} {check["score"]:.0f}</div>'


def render_gen_card(it: dict) -> str:
    ev = it["eval"]
    grade_cls = ev["grade"]
    converged_badge = '<span class="badge converged">✅ CONVERGED</span>' if ev["converged"] else '<span class="badge">running...</span>'
    attrs = "\n".join(render_attr_badge(c) for c in ev["attribute_check"])
    sugs = ""
    for s in ev.get("suggestions", []):
        sugs += f'<div class="sug">[{s["priority"].upper()}] {s["issue"]}</div>'
    suggestions_html = f'<div class="suggestions">{sugs}</div>' if sugs else ""
    
    return f"""<div class="gen-card">
  <div class="gen-header">
    <span class="gen-title">Gen {it["iteration"]} — {it["generation_id"]}</span>
    <span class="score {grade_cls}">{ev["score"]}</span>
  </div>
  {converged_badge}
  <div class="prompt-box">{it["prompt"]}</div>
  <div class="attr-grid">
    {attrs}
  </div>
  {suggestions_html}
</div>"""


def build_dashboard(report: dict) -> str:
    if not report:
        return "<h1>Evolution Dashboard</h1><p>No report found.</p>"
    cards = "\n".join(render_gen_card(it) for it in report.get("iterations", []))
    html = DASHBOARD_HTML
    html = html.replace("__CONCEPT__", report.get("concept", "?"))
    html = html.replace("__TARGET__", str(report.get("target_score", 75)))
    html = html.replace("__TOTAL__", str(len(report.get("iterations", []))))
    html = html.replace("__FINAL__", str(report.get("final_score", 0)))
    html = html.replace("__CONVERGED__", "YES" if report.get("converged") else "NO")
    html = html.replace("__GEN_CARDS__", cards)
    return html


# ── FastAPI App ────────────────────────────────────────────────

app = FastAPI(title="evolution-dashboard", version="1.0.0")


@app.get("/", response_class=HTMLResponse)
def dashboard():
    report = load_latest_report()
    return build_dashboard(report)


@app.get("/api/reports", response_model=list[dict])
def list_reports():
    """発見された全レポートのメタ情報を返す"""
    reports = []
    for p in discover_reports():
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        reports.append({
            "concept": data.get("concept"),
            "final_score": data.get("final_score"),
            "converged": data.get("converged"),
            "iterations": len(data.get("iterations", [])),
            "path": str(p),
        })
    return reports


@app.get("/api/report/latest", response_model=EvolutionReport)
def get_latest_report():
    report = load_latest_report()
    if not report:
        return EvolutionReport(concept="", target_score=75, max_iterations=0, iterations=[], final_score=0, converged=False, reference_concept=ReferenceConcept(title="", attributes={}, mood="", reference_images=[]))
    return EvolutionReport(**report)


@app.get("/api/report/{concept}")
def get_report_by_concept(concept: str):
    report = load_report_by_concept(concept)
    if not report:
        return {"error": "Report not found"}
    return report


@app.get("/api/generations/{concept}")
def list_generations(concept: str):
    report = load_report_by_concept(concept)
    if not report:
        return {"error": "Report not found"}
    return [
        {
            "iteration": it["iteration"],
            "generation_id": it["generation_id"],
            "score": it["score"],
            "grade": it["grade"],
            "converged": it["eval"]["converged"],
        }
        for it in report.get("iterations", [])
    ]


@app.get("/api/generations/{concept}/{iteration}")
def get_generation(concept: str, iteration: int):
    report = load_report_by_concept(concept)
    if not report:
        return {"error": "Report not found"}
    for it in report.get("iterations", []):
        if it["iteration"] == iteration:
            return it
    return {"error": "Generation not found"}


@app.get("/api/compare/{concept}")
def compare_first_last(concept: str):
    report = load_report_by_concept(concept)
    if not report:
        return {"error": "Report not found"}
    its = report.get("iterations", [])
    if len(its) < 2:
        return {"error": "Need at least 2 iterations"}
    first, last = its[0], its[-1]
    return {
        "concept": concept,
        "first": {"iteration": first["iteration"], "score": first["score"], "grade": first["grade"]},
        "last": {"iteration": last["iteration"], "score": last["score"], "grade": last["grade"]},
        "delta_score": last["score"] - first["score"],
        "improved": last["score"] > first["score"],
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "evolution-dashboard"}


# ── MCP (FastMCP) ──────────────────────────────────────────────

def run_stdio():
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("evolution-dashboard")

    @mcp.tool()
    def list_generations_tool(concept: str) -> list[dict]:
        """List all generations for a concept."""
        report = load_report_by_concept(concept)
        if not report:
            return []
        return [
            {"iteration": it["iteration"], "generation_id": it["generation_id"], "score": it["score"], "grade": it["grade"], "converged": it["eval"]["converged"]}
            for it in report.get("iterations", [])
        ]

    @mcp.tool()
    def get_generation_tool(concept: str, iteration: int) -> dict:
        """Get a specific generation details."""
        report = load_report_by_concept(concept)
        if not report:
            return {"error": "Report not found"}
        for it in report.get("iterations", []):
            if it["iteration"] == iteration:
                return it
        return {"error": "Generation not found"}

    @mcp.tool()
    def get_evolution_report_tool(concept: str) -> dict:
        """Get full evolution report."""
        return load_report_by_concept(concept) or {"error": "Report not found"}

    @mcp.tool()
    def compare_generations_tool(concept: str) -> dict:
        """Compare first and last generation."""
        report = load_report_by_concept(concept)
        if not report:
            return {"error": "Report not found"}
        its = report.get("iterations", [])
        if len(its) < 2:
            return {"error": "Need at least 2 iterations"}
        first, last = its[0], its[-1]
        return {
            "first": {"iteration": first["iteration"], "score": first["score"], "grade": first["grade"]},
            "last": {"iteration": last["iteration"], "score": last["score"], "grade": last["grade"]},
            "delta_score": last["score"] - first["score"],
            "converged": last["eval"]["converged"],
        }

    mcp.run(transport="stdio")


# ── Main ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--stdio", action="store_true")
    args = parser.parse_args()

    if args.http or not args.stdio:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        run_stdio()
