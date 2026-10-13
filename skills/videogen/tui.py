#!/usr/bin/env python3
"""TUI for videogen MCP server.

Controls video composition (merge panels, add audio/subtitles) via MCP HTTP API.
"""
import curses
import json
import os
import sys
import urllib.request
import urllib.error

DEFAULT_HOST = os.environ.get("VIDEOGEN_HOST", "http://localhost:8006")
TOOLS_BASE = f"{DEFAULT_HOST}/mcp/tools"


def call_tool(tool_name: str, payload: dict) -> dict:
    """Call MCP tool via HTTP POST."""
    url = f"{TOOLS_BASE}/{tool_name}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"status": "error", "message": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_health() -> dict:
    url = f"{DEFAULT_HOST}/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"status": "error", "message": str(e)}


class VideogenTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.height, self.width = stdscr.getmaxyx()
        self.menu_items = [
            "Compose Video (input + audio + subtitles)",
            "Merge Panels (concat panel_*.mp4)",
            "Check Server Health",
            "Exit",
        ]
        self.selected = 0

    def draw_header(self):
        title = " videogen TUI — MCP Video Editor "
        self.stdscr.addstr(0, 0, title.center(self.width), curses.A_REVERSE)
        host_line = f" Server: {DEFAULT_HOST} "
        self.stdscr.addstr(1, 0, host_line.center(self.width))

    def draw_menu(self):
        start_y = 3
        for i, item in enumerate(self.menu_items):
            y = start_y + i
            if i == self.selected:
                self.stdscr.addstr(y, 2, f"> {item}", curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, 2, f"  {item}")

    def draw_footer(self, msg=""):
        self.stdscr.addstr(self.height - 1, 0, " " * (self.width - 1))
        if msg:
            self.stdscr.addstr(self.height - 1, 0, msg[: self.width - 1])

    def run(self):
        while True:
            self.stdscr.clear()
            self.draw_header()
            self.draw_menu()
            self.draw_footer()
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if key == curses.KEY_UP:
                self.selected = (self.selected - 1) % len(self.menu_items)
            elif key == curses.KEY_DOWN:
                self.selected = (self.selected + 1) % len(self.menu_items)
            elif key in (curses.KEY_ENTER, 10, 13):  # Enter
                if self.selected == 0:
                    self.compose_video_flow()
                elif self.selected == 1:
                    self.merge_panels_flow()
                elif self.selected == 2:
                    self.health_flow()
                elif self.selected == 3:
                    break

    def get_input(self, prompt, default=""):
        """Prompt user for a string input."""
        self.stdscr.clear()
        self.draw_header()
        self.stdscr.addstr(3, 2, prompt)
        if default:
            self.stdscr.addstr(f" [{default}]")
        self.stdscr.addstr(": ")
        curses.echo()
        curses.curs_set(1)
        self.stdscr.refresh()
        try:
            inp = self.stdscr.getstr().decode("utf-8").strip()
        except Exception:
            inp = ""
        curses.noecho()
        curses.curs_set(0)
        return inp if inp else default

    def show_result(self, result: dict):
        self.stdscr.clear()
        self.draw_header()
        lines = [json.dumps(result, indent=2, ensure_ascii=False)]
        for i, line in enumerate(lines):
            self.stdscr.addstr(3 + i, 2, line)
        self.draw_footer("Press any key to continue...")
        self.stdscr.refresh()
        self.stdscr.getch()

    def compose_video_flow(self):
        self.stdscr.clear()
        self.draw_header()
        self.stdscr.addstr(3, 2, "=== Compose Video ===")
        self.stdscr.refresh()

        input_video = self.get_input("Input video path", "/tmp/merged.mp4")
        audio_path = self.get_input("Audio path (optional)", "")
        subtitle_path = self.get_input("Subtitle path (optional)", "")
        output_path = self.get_input("Output path", "/tmp/final.mp4")
        resolution = int(self.get_input("Resolution (width)", "1280"))
        fps = int(self.get_input("FPS", "30"))

        payload = {
            "input_video": input_video,
            "output_path": output_path,
            "resolution": resolution,
            "fps": fps,
        }
        if audio_path:
            payload["audio_path"] = audio_path
        if subtitle_path:
            payload["subtitle_path"] = subtitle_path

        self.draw_footer("Calling compose_video...")
        self.stdscr.refresh()
        result = call_tool("compose_video", payload)
        self.show_result(result)

    def merge_panels_flow(self):
        self.stdscr.clear()
        self.draw_header()
        self.stdscr.addstr(3, 2, "=== Merge Panels ===")
        self.stdscr.refresh()

        panel_dir = self.get_input("Panel directory", "/tmp/panels")
        output_path = self.get_input("Output path", "/tmp/merged.mp4")

        payload = {"panel_dir": panel_dir, "output_path": output_path}

        self.draw_footer("Calling merge_panels...")
        self.stdscr.refresh()
        result = call_tool("merge_panels", payload)
        self.show_result(result)

    def health_flow(self):
        self.draw_footer("Checking health...")
        self.stdscr.refresh()
        result = check_health()
        self.show_result(result)


def main(stdscr):
    tui = VideogenTUI(stdscr)
    tui.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass