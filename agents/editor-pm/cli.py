#!/usr/bin/env python3
"""editor-pm — 編集者の進行管理エージェント（ページ単位の品質ゲート用）。

docs/40-submit の提出デッキを「1ページ＝1フォルダ」で管理し、
どのページが PASS / FAIL / HOLD / NOT_RUN かを台帳（pages.csv）から判定する。
PASS していないページが残る限り、次のページには進めない。

このツールは判定を捏造しない。VLM やレンダリングの結果は
各ページの test.json に記録されたものだけを読む。

使い方:
    python3 agents/editor-pm/cli.py index             # 台帳を再生成（構造の再走査）
    python3 agents/editor-pm/cli.py index --scaffold   # 各ページのフォルダと雛形を作る
    python3 agents/editor-pm/cli.py status             # 進捗の一覧
    python3 agents/editor-pm/cli.py next               # 次にやる1ページと手順
    python3 agents/editor-pm/cli.py show <page_id>     # 1ページの詳細
"""
from __future__ import annotations

import argparse
import csv
import html as html_mod
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SUBMIT = REPO / "docs/40-submit"
TESTS = SUBMIT / "page-tests"
LEDGER = TESTS / "pages.csv"

# 管理対象の原本。増やすときはここに足す（順序がそのままページ順）。
DEFAULT_PARTS = ["part01_plan.html", "part02_deliver.html"]

# page_id の頭に付く番号は「印刷ページ番号」。番号を持たない紙（表紙・扉）は
# 物理順で採番し、衝突したら末尾に d を付ける。ここは読み替えの必要な既知の例外。
ALIASES = {
    "Kaguru Agent 画像生成ワークフロー": "p26-kaguru-agent-kaggle-evops-workflow",
}

# 日本語見出し → 英字トークン。ID を人が読める形に保つための対訳表。
TRANSLIT = {
    "表紙": "cover", "目次": "toc", "付録": "appendix",
    "検討項目": "study", "検討": "study", "効果": "effect",
    "全体像": "overview", "範囲": "scope", "スケジュール": "schedule",
    "開発カレンダー": "calendar",
    "納品物": "deliverables", "扉": "divider", "チェックリスト": "checklist",
    "要求": "requirements", "境界": "boundary", "アクター": "actors",
    "ユースケース図": "usecase", "ユースケース": "usecase", "仕様": "spec",
    "分析": "analysis", "ロバストネス": "robustness", "クラス": "class",
    "一覧": "list", "シーケンス図": "sequence", "設計": "design",
    "パッケージ構成": "packages", "プログラム": "program", "構成": "structure",
    "主要部": "core", "操作マニュアル": "manual", "実行イメージ": "runtime",
    "補足": "note", "発表": "present", "カバー": "cover",
    "簡単な説明": "brief", "問題意識": "problem", "機能説明": "features",
    "構造の説明": "structure", "実演": "demo", "振り返り": "reflection",
}

SECTION_RE = re.compile(
    r'<section class="sheet(?P<cls>[^"]*)"[^>]*data-t="(?P<tag>[^"]*)"[^>]*>(?P<body>.*?)</section>',
    re.DOTALL,
)


def clean(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html_mod.unescape(text)).strip()


def stem(tag: str) -> str:
    """見出し → 英字スラグ。長い日本語トークンから先に置換する（「検討項目」>「検討」）。"""
    work = tag
    for ja in sorted((k for k in TRANSLIT if not k.isascii()), key=len, reverse=True):
        if ja in work:
            work = work.replace(ja, f" {TRANSLIT[ja]} ")
    tokens = [t.lower() for t in re.split(r"[^0-9A-Za-z]+", work) if t]
    return "-".join(dict.fromkeys(tokens)) or "page"


def assign_ids(pages: list[dict]) -> None:
    """page_id = p<番号>-<slug>。

    番号は原則その紙に印刷されているページ番号（hd-no）。印刷番号を持たない
    紙（表紙・扉）は物理順で採番し、既に使われていれば末尾に d を付ける。
    """
    used: set[str] = set()
    for p in pages:
        if p["data_t"] in ALIASES:
            pid = ALIASES[p["data_t"]]
        else:
            num = p["no"] or f"{p['order']:02d}"
            pid = f"p{num}-{stem(p['data_t'])}"
            if pid in used:
                pid = f"p{num}d-{stem(p['data_t'])}"
        p["page_id"] = pid
        used.add(pid)


def scan_parts(parts: list[str]) -> list[dict]:
    """原本 HTML を走査してページを列挙する。順序はデッキの順序。"""
    pages: list[dict] = []
    order = 0
    for part in parts:
        path = SUBMIT / part
        if not path.exists():
            print(f"[warn] part not found: {part}", file=sys.stderr)
            continue
        html = path.read_text(encoding="utf-8")
        for m in SECTION_RE.finditer(html):
            order += 1
            body = m.group("body")
            no_m = re.search(r'<span class="hd-no">\s*(\d+)\s*</span>', body)
            no = no_m.group(1) if no_m else ""
            tag = m.group("tag")
            title, subtitle = "", ""
            title_m = re.search(r'<h2 class="hd-title">(.*?)</h2>', body, re.DOTALL)
            if title_m:
                inner = title_m.group(1)
                sub_m = re.search(r"<small>(.*?)</small>", inner, re.DOTALL)
                if sub_m:
                    subtitle = clean(sub_m.group(1))
                    inner = inner.replace(sub_m.group(0), " ")
                title = clean(inner)
            pages.append({
                "order": order,
                "no": no,
                "page_id": "",
                "data_t": tag,
                "kind": "divider" if "divider" in m.group("cls") else "sheet",
                "title": title or tag,
                "subtitle": subtitle,
                "part": part,
            })
    assign_ids(pages)
    return pages


def page_dir(page: dict) -> Path:
    return TESTS / page["page_id"]


def read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def decision_of(page: dict) -> tuple[str, str]:
    """(decision, note) — test.json に書かれた事実だけを読む。"""
    t = read_json(page_dir(page) / "test.json")
    if t is None:
        return "NOT_RUN", "test.json なし"
    d = t.get("decision") or t.get("status") or "NOT_RUN"
    gates = t.get("gates") or {}
    blocked = [k for k, v in gates.items()
               if isinstance(v, dict) and str(v.get("status", "")).upper() in {"BLOCKED", "NOT_RUN", "PENDING", "REVIEW", "FAIL"}]
    note = t.get("next_action") or ""
    if blocked:
        note = f"未了: {', '.join(sorted(blocked))}" + (f" / {note}" if note else "")
    return str(d).upper(), note


STATUS_MARK = {
    "PASS": "PASS", "FAIL": "FAIL", "HOLD": "HOLD",
    "NOT_RUN": "-----", "INCOMPLETE": "HOLD", "TODO": "-----",
}


def cmd_index(args: argparse.Namespace) -> int:
    pages = scan_parts(args.parts)
    if not pages:
        print("no pages found", file=sys.stderr)
        return 1

    TESTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in pages:
        d = page_dir(p)
        created = []
        if args.scaffold:
            d.mkdir(parents=True, exist_ok=True)
            cj = d / "content.json"
            if not cj.exists():
                cj.write_text(json.dumps({
                    "schema_version": "1.0",
                    "page_id": p["page_id"],
                    "state": "scaffold",
                    "language": "ja",
                    "title": p["title"],
                    "subtitle": p["subtitle"] or None,
                    "purpose": None,
                    "stages": [],
                    "diagram": {"path": None, "alt": None, "caption": None},
                    "source": {
                        "html": f"docs/40-submit/{p['part']}",
                        "section_selector": f'section.sheet[data-t="{p["data_t"]}"]',
                    },
                    "notes": ["自動生成の雛形。purpose / stages / diagram は人が埋める。"],
                }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                created.append("content.json")
            tj = d / "test.json"
            if not tj.exists():
                tj.write_text(json.dumps({
                    "schema_version": "1.0",
                    "page_id": p["page_id"],
                    "status": "NOT_RUN",
                    "gates": {
                        "content_json": {"status": "NOT_RUN"},
                        "html_svg_consistency": {"status": "NOT_RUN"},
                        "existing_css": {"status": "NOT_RUN"},
                        "deterministic_checks": {"status": "NOT_RUN"},
                        "browser_render": {"status": "NOT_RUN"},
                        "vlm_mcp": {"status": "BLOCKED", "note": "未設定。判定済みとして扱わない。"},
                    },
                    "decision": "NOT_RUN",
                    "next_action": "content.json を埋め、レンダリングしてから判定する。",
                }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                created.append("test.json")
        decision, note = decision_of(p)
        rows.append({
            "order": p["order"], "no": p["no"], "page_id": p["page_id"],
            "data_t": p["data_t"], "kind": p["kind"], "title": p["title"],
            "subtitle": p["subtitle"],
            "part": p["part"],
            "content_json": "yes" if (d / "content.json").exists() else "no",
            "test_json": "yes" if (d / "test.json").exists() else "no",
            "decision": decision, "next_action": note,
        })
        if created:
            print(f"[scaffold] {p['page_id']}: {', '.join(created)}")

    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"pages: {len(rows)}")
    print(f"ledger: {LEDGER.relative_to(REPO)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    rows = load_ledger()
    if not rows:
        print("台帳がありません。先に `index` を実行してください。", file=sys.stderr)
        return 1
    counts: dict[str, int] = {}
    print(f"{'no':>3} {'order':>5}  {'decision':<7} {'page_id':<42} title")
    print("-" * 100)
    for r in rows:
        mark = STATUS_MARK.get(r["decision"], r["decision"])
        counts[mark] = counts.get(mark, 0) + 1
        print(f"{r['no'] or '--':>3} {r['order']:>5}  {mark:<7} {r['page_id']:<42} {r['title'][:40]}")
    print("-" * 100)
    total = len(rows)
    passed = counts.get("PASS", 0)
    print(f"total={total} PASS={passed} FAIL={counts.get('FAIL',0)} "
          f"HOLD={counts.get('HOLD',0)} NOT_RUN={counts.get('-----',0)}")
    print(f"progress: {passed}/{total} ({100*passed//total}%)")
    return 0


def load_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    with LEDGER.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def first_open(rows: list[dict]) -> dict | None:
    """編集者の順番: 着手済み（FAIL/HOLD）を先に消化し、その後に未着手を順に開く。

    扉ページは本文の品質ゲート対象外なので飛ばす。
    """
    live = [r for r in rows if r["kind"] != "divider"]
    for r in live:
        if STATUS_MARK.get(r["decision"], r["decision"]) in {"FAIL", "HOLD"}:
            return r
    for r in live:
        if STATUS_MARK.get(r["decision"], r["decision"]) != "PASS":
            return r
    return None


def cmd_next(args: argparse.Namespace) -> int:
    rows = load_ledger()
    if not rows:
        print("台帳がありません。先に `index` を実行してください。", file=sys.stderr)
        return 1
    r = first_open(rows)
    if r is None:
        print("全ページ PASS。次は通し印刷と提出チェック。")
        return 0
    d = page_dir(r)
    print(f"next page : {r['page_id']}")
    print(f"no        : {r['no'] or '--'}")
    print(f"section   : {r['data_t']}")
    print(f"html      : docs/40-submit/{r['part']}")
    print(f"folder    : {d.relative_to(REPO)}")
    print(f"decision  : {r['decision']}")
    if r["next_action"]:
        print(f"todo      : {r['next_action']}")
    print()
    print("手順:")
    print(f"  1. python3 docs/40-submit/page-tests/render_page.py {r['page_id']}")
    print(f"  2. google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \\")
    print(f"       --allow-file-access-from-files --force-device-scale-factor=2 \\")
    print(f"       --window-size=1123,794 --screenshot=page.png \\")
    print(f"       file://$PWD/docs/40-submit/page-tests/{r['page_id']}/render/page.html")
    print(f"  3. python3 docs/40-submit/page-tests/vlm_judge.py {r['page_id']} \\")
    print(f"       docs/40-submit/page-tests/{r['page_id']}/render/page.png")
    print(f"  4. 結果を docs/40-submit/page-tests/{r['page_id']}/test.json に記録")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    rows = {r["page_id"]: r for r in load_ledger()}
    r = rows.get(args.page_id)
    if not r:
        print(f"unknown page_id: {args.page_id}", file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=2))
    t = read_json(page_dir(r) / "test.json")
    if t:
        print("\n--- test.json ---")
        print(json.dumps(t, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="editor-pm", description="ページ単位の進行管理")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("index", help="デッキを走査して台帳を作る")
    p.add_argument("--parts", nargs="*", default=DEFAULT_PARTS,
                   help=f"原本 HTML（既定: {' '.join(DEFAULT_PARTS)}）")
    p.add_argument("--scaffold", action="store_true", help="ページフォルダと雛形を作る")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("status", help="進捗一覧")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("next", help="次にやる1ページ")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("show", help="1ページの詳細")
    p.add_argument("page_id")
    p.set_defaults(func=cmd_show)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
