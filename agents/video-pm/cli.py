#!/usr/bin/env python3
"""
Video Manager CLI — Agent responsible for video lifecycle management.
Handles: generation tracking, asset inventory, kanban sync, dashboard updates.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path("/home/bons/evops")
OUTPUTS = REPO_ROOT / "outputs"
PAPERS = REPO_ROOT / "papers"
KANBAN_CSV = REPO_ROOT / "kanban.csv"
DASHBOARD = OUTPUTS / "kanban_dashboard_blocks.html"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac"}
SVG_EXTENSIONS = {".svg"}
JSON_EXTENSIONS = {".json"}


class VideoManager:
    def __init__(self, repo: Path = REPO_ROOT, output: Path = OUTPUTS):
        self.repo = repo
        self.output = output
        self.papers_dir = PAPERS
        self.kanban_path = KANBAN_CSV
        self.dashboard_path = DASHBOARD

    def scan_paper_outputs(self) -> dict:
        """Scan all P*/ folders for video assets and metadata."""
        results = {}
        for paper_dir in sorted(self.output.glob("P*")):
            if not paper_dir.is_dir():
                continue
            pid = paper_dir.name
            assets = {
                "video": [],
                "audio": [],
                "svg": [],
                "json": [],
                "html": [],
            }
            for f in paper_dir.rglob("*"):
                if f.is_file():
                    suffix = f.suffix.lower()
                    rel = f.relative_to(paper_dir)
                    if suffix in VIDEO_EXTENSIONS:
                        assets["video"].append(str(rel))
                    elif suffix in AUDIO_EXTENSIONS:
                        assets["audio"].append(str(rel))
                    elif suffix in SVG_EXTENSIONS:
                        assets["svg"].append(str(rel))
                    elif suffix in JSON_EXTENSIONS:
                        assets["json"].append(str(rel))
                    elif suffix == ".html":
                        assets["html"].append(str(rel))
            if any(assets.values()):
                results[pid] = assets
        return results

    def load_kanban(self) -> list:
        """Load existing kanban.csv as list of dicts."""
        if not self.kanban_path.exists():
            return []
        rows = []
        with open(self.kanban_path, encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
            if not lines:
                return []
            headers = [h.strip() for h in lines[0].split(",")]
            for line in lines[1:]:
                vals = [v.strip().strip('"') for v in line.split(",")]
                if len(vals) == len(headers):
                    rows.append(dict(zip(headers, vals)))
        return rows

    def write_kanban(self, rows: list):
        """Write kanban.csv with updated asset info."""
        headers = ["scene", "paper_id", "paper_title", "episode_json", "tts_audio", "svg_panels", "comic_html", "final_video", "notes"]
        lines = [",".join(headers)]
        for r in rows:
            vals = [f'"{r.get(h, "")}"' for h in headers]
            lines.append(",".join(vals))
        self.kanban_path.write_text("\n".join(lines), encoding="utf-8")

    def sync_kanban_with_assets(self):
        """Update kanban.csv with current asset inventory."""
        assets = self.scan_paper_outputs()
        rows = self.load_kanban()
        # Build lookup
        by_paper = {r["paper_id"]: r for r in rows if r.get("paper_id")}
        for pid, a in assets.items():
            if pid not in by_paper:
                # Create new row
                by_paper[pid] = {
                    "scene": pid,
                    "paper_id": pid,
                    "paper_title": pid,
                    "episode_json": "",
                    "tts_audio": "",
                    "svg_panels": "",
                    "comic_html": "",
                    "final_video": "",
                    "notes": "Auto-synced from assets",
                }
            row = by_paper[pid]
            row["episode_json"] = ";".join(a["json"]) if a["json"] else row.get("episode_json", "")
            row["tts_audio"] = ";".join(a["audio"]) if a["audio"] else row.get("tts_audio", "")
            row["svg_panels"] = ";".join(a["svg"]) if a["svg"] else row.get("svg_panels", "")
            row["comic_html"] = ";".join(a["html"]) if a["html"] else row.get("comic_html", "")
            row["final_video"] = ";".join(a["video"]) if a["video"] else row.get("final_video", "")
            row["notes"] = f"Last sync: {datetime.now().isoformat(timespec='seconds')}"
        # Preserve order: P01-P38 + kanban_* rows
        ordered = []
        for i in range(1, 39):
            pid = f"P{i:02d}"
            if pid in by_paper:
                ordered.append(by_paper[pid])
        for r in rows:
            if r.get("paper_id", "").startswith("kanban_"):
                ordered.append(r)
        self.write_kanban(ordered)
        print(f"Kanban synced: {len(assets)} paper folders updated")

    def generate_dashboard(self):
        """Regenerate kanban_dashboard_blocks.html from kanban.csv."""
        rows = self.load_kanban()
        html = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><title>Kanban Dashboard</title><style>
body{font-family:system-ui,sans-serif;background:#1a1c23;color:#e8ecf1;padding:20px;line-height:1.6}
h1{color:#b45309;border-bottom:3px solid #b45309;padding-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:20px}
.card{background:#23262b;border:1px solid #333;border-radius:10px;padding:16px}
.card h3{margin:0 0 8px;color:#fff;font-size:1rem}
.card .asset{font-size:11pt;color:#aaa;margin:4px 0}
.card .asset.ok{color:#1d4ed8}
.card .asset.warn{color:#b45309}
.card .asset.err{color:#dc2626}
.tag{display:inline-block;padding:2px 6px;background:#b45309;color:#fff;border-radius:4px;font-size:9pt;margin:2px}
</style></head><body>
<h1>Video PM Kanban Dashboard</h1>
<p>Last updated: """ + datetime.now().isoformat(timespec='seconds') + """</p>
<div class="grid">
"""
        for r in rows:
            pid = r.get("paper_id", "")
            html += f'<div class="card"><h3>{pid}: {r.get("paper_title", "")}</h3>'
            for key, label, cls in [
                ("episode_json", "📄 Episode JSON", "ok"),
                ("tts_audio", "🎙 TTS Audio", "ok"),
                ("svg_panels", "🎬 SVG Panels", "ok"),
                ("comic_html", "📖 4-Koma HTML", "ok"),
                ("final_video", "🎥 Final Video", "ok"),
            ]:
                val = r.get(key, "")
                if val:
                    html += f'<div class="asset {cls}">{label}: {val}</div>'
                else:
                    html += f'<div class="asset err">{label}: (missing)</div>'
            notes = r.get("notes", "")
            if notes:
                html += f'<div class="asset warn">{notes}</div>'
            html += "</div>"
        html += """</div></body></html>"""
        self.dashboard_path.write_text(html, encoding="utf-8")
        print(f"Dashboard generated: {self.dashboard_path}")

    def run_full_sync(self):
        """Full workflow: scan → kanban sync → dashboard regenerate."""
        print("🔍 Scanning paper outputs...")
        self.sync_kanban_with_assets()
        print("📊 Regenerating dashboard...")
        self.generate_dashboard()
        print("✅ Video management workflow complete")


def main():
    parser = argparse.ArgumentParser(description="Video Manager Agent CLI")
    parser.add_argument("command", choices=["manage", "sync", "dashboard", "scan"])
    parser.add_argument("--repo", default=str(REPO_ROOT))
    parser.add_argument("--output", default=str(OUTPUTS))
    parser.add_argument("--kanban", default=str(KANBAN_CSV))
    parser.add_argument("--dashboard", default=str(DASHBOARD))
    args = parser.parse_args()

    mgr = VideoManager(Path(args.repo), Path(args.output))

    if args.command == "manage" or args.command == "sync":
        mgr.run_full_sync()
    elif args.command == "dashboard":
        mgr.generate_dashboard()
    elif args.command == "scan":
        assets = mgr.scan_paper_outputs()
        print(json.dumps(assets, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()