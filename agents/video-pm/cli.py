#!/usr/bin/env python3
"""FastAPI Video Management Agent - Real-time monitoring and workflow automation
Handles video production from papers, TTS integration, SVG panel generation, and GitHub issue tracking.
"""
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import time
import os
import json

app = FastAPI(title="EvOps Video Management Agent")

# Configuration
OUTPUTS_DIR = Path("/home/bons/evops/outputs")
PAPERS_DIR = Path("/home/bons/evops/papers")
MCP_DIR = Path("/home/bons/evops/skills/sf-paper-comic")
MCP_SERVER = "http://localhost:8004"

# GitHub API integration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_placeholder")
GITHUB_REPO = "bonsai/hw-sotsusei"

class VideoProject:
    def __init__(self, paper_id: str, output_dir: Path):
        self.paper_id = paper_id
        self.output_dir = output_dir
        self.assets_dir = output_dir / "assets"
        self.panels_dir = output_dir / "panels"
        self.svg_dir = output_dir / "svg"
        self.templates_dir = output_dir / "templates"
        self.episode_json = output_dir / "episode.json"
        self.final_video = output_dir / "final.mp4"
        self.svgs = []
        self.templates = []
        self.init_assets()

    def init_assets(self):
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.panels_dir.mkdir(parents=True, exist_ok=True)
        self.svg_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.episode_json.touch(exist_ok=True)
        self.final_video.touch(exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def get_paper_info(self) -> dict:
        """Get paper metadata from README or paper directory."""
        readme_path = self.papers_dir / f"P{paper_id}-{paper_id[-2:]}.md"
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title and year from header
                lines = content.split('\n')
                title_line = next((line for line in lines if "Title" in line or "title" in line.lower()), "")
                year_line = next((line for line in lines if "202" in line and "202" in line), "unknown")
                return {
                    "title": title_line.split("**")[-1].strip() if "title" in line.lower() else "Unknown Paper",
                    "year": year_line.split()[-1],
                    "paper_id": self.paper_id
                }
        return {
            "title": "Unknown Paper",
            "year": "unknown",
            "paper_id": self.paper_id
        }

    def create_video_asset(self, paper_id: str, paper_title: str, paper_year: str):
        """Create a new video project with proper structure."""
        # Clean existing output
        for item in self.output_dir.iterdir():
            if item.is_file() or item.is_dir():
                item.unlink(missing_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create episode structure
        episode_data = {
            "id": paper_id,
            "title": paper_title,
            "year": paper_year,
            "panels": [
                {"no": 1, "role": "problem", "text": f"Paper {paper_id} setup challenge"},
                {"no": 2, "role": "challenge", "text": "Complex evaluation requirements"},
                {"no": 4, "role": "solution", "text": "Automated workflow implementation"},
                {"no": 4, "role": "resolution", "text": "Video production automated"}
            ],
            "metadata": {
                "paper_id": paper_id,
                "title": paper_title,
                "year": paper_year,
                "created": datetime.now().isoformat()
            }
        }
        
        with open(self.episode_json, 'w', encoding='utf-8') as f:
            json.dump(episode_data, f, indent=2, ensure_ascii=False)
        
        print(f"Created video project for {paper_id} with 4 panels")

    def generate_svg_panels(self):
        """Generate SVG panels using sf-paper-comic tool"""
        if not self.panels_dir.exists():
            self.panels_dir.mkdir(parents=True, exist_ok=True)
            
        # Create sample episode.json for 4-panel comic
        episode_data = {
            "title": f"{self.paper_id} - {self.paper_id[-2:]}",
            "panels": [
                {"no": 1, "role": "problem", "text": "Paper evaluation challenge", "speaker": "常識"},
                {"no": 2, "role": "anomaly", "text": "Complex evaluation requirements", "speaker": "研究者"},
                {"no": 3, "role": "invention", "text": "Automated workflow solution", "speaker": "研究者"},
                {"no": 4, "role": "research-connection", "text": "Video management integration", "speaker": "AI君"}
            ],
            "visual": {"theme": "SF research lab", "accent": "#7c3aed"},
            "animation": {"sequence": [1, 2, 3, 4], "transition": "cut", "duration": 60}
        }
        
        episode_json = self.output_dir / "episode.json"
        with open(episode_json, 'w', encoding='utf-8') as f:
            json.dump(episode_data, f, ensure_ascii=False, indent=2)
            
        # Generate SVG panels using external tool
        cmd = [
            "python", "/home/bons/evops/skills/sf-paper-comic/svg-gen.py",
            "--episode", str(episode_json),
            "--output-dir", str(self.output_dir),
            "--font", "gothic",
            "--paper-id", paper_id
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"SVG generation failed: {result.stderr}")
            
        self.svgs = [f"{paper_id}_panel_{i+1:02d}.svg" for i in range(4)]
        print(f"Generated 4 SVG panels for {paper_id}")

    def get_video_status(self) -> dict:
        """Check current video management status."""
        status = {
            "paper_id": self.paper_id,
            "status": "pending",
            "last_updated": datetime.now().isoformat(),
            "panels": len(self.panels_dir.iterdir()),
            "svg_files": len(self.svg_dir.iterdir()),
            "tts_files": len(self.assets_dir.glob("voice_*.mp3")),
            "final_video": str(self.final_video.exists()),
            "comic": str(self.output_dir / f"comic_{self.paper_id}.html").exists()
        }
        return status

    def get_github_issues(self) -> list:
        """Get GitHub issues related to this paper."""
        # This would integrate with GitHub API in production
        return [
            {"number": 1, "title": "Video management workflow", "status": "open"},
            {"number": 2, "title": "SVG panel generation", "status": "in progress"},
            {"number": 3, "title": "TTS integration", "status": "pending"}
        ]

    def get_dashboard_data(self) -> dict:
        """Return data for real-time dashboard."""
        return {
            "paper_id": self.paper_id,
            "title": self.paper_info["title"],
            "year": self.paper_info["year"],
            "status": self.get_video_status(),
            "github_issues": self.get_github_issues(),
            "last_updated": datetime.now().isoformat()
        }

# Initialize agent
video_manager = VideoProject("P01", Path("/home/bons/evops/outputs/P01"))

# Initialize FastAPI app
app = FastAPI(title="EvOps Video Management Agent")

@app.get("/status")
def get_status():
    return video_manager.get_video_status()

@app.get("/dashboard")
def get_dashboard():
    return video_manager.get_dashboard_data()

@app.get("/papers")
def list_papers():
    papers = []
    for paper_dir in sorted(Path("/home/bons/evops/papers").glob("P*")):
        paper_id = paper_dir.name.split("-")[0]
        papers.append({
            "id": paper_id,
            "title": paper_dir.name,
            "year": paper_dir.name.split("-")[-1]
        })
    return papers

@app.get("/papers/{paper_id}")
def get_paper_details(paper_id: str):
    if paper_id not in [p.name for p in Path("/home/bons/evops/papers").iterdir()]:
        raise HTTPException(status_code=404, detail="Paper not found")
    video_dir = Path("/home/bons/evops/outputs") / paper_id
    return video_manager.get_dashboard_data()

@app.get("/papers/{paper_id}/comic")
def get_comic(paper_id: str):
    comic_path = Path("/home/bons/evops/outputs") / f"comic_{paper_id}.html"
    if comic_path.exists():
        return FileResponse(comic_path)
    raise HTTPException(status_code=404, detail="Comic not found")

@app.get("/papers/{paper_id}/svg")
def get_svg_panels(paper_id: str):
    video_dir = Path("/home/bons/evops/outputs") / paper_id
    svg_files = sorted(video_dir.glob("*.svg"))
    return {"panels": [f.name for f in svg_files]}

if __name__ == "__main__":
    # Test the agent
    print("Starting Video Management Agent...")
    video_manager = VideoProject("P01", Path("/home/bons/evops/outputs/P01"))
    video_manager.create_video_asset("P01", "VeMo", "2026")
    video_manager.generate_svg_panels()
    print("Agent initialized successfully!")