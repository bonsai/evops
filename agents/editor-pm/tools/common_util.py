# 共通ユーティリティ — デッキ編集・品質ゲート用
# skills / cli から import して使う

import json, csv, re, html
from pathlib import Path

def load_json(p): return json.loads(Path(p).read_text("utf-8"))
def save_json(p, d): Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def page_id_from_tag(tag): 
    # data-t からページIDを推定（簡易）
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", tag.lower()).strip("-")
    return slug[:30]

def read_kanban(p="docs/40-submit/kanban.json"):
    return load_json(p)

def write_kanban(p="docs/40-submit/kanban.json", d=None):
    save_json(p, d or read_kanban(p))

def get_render_path(page_id, root="docs/40-submit"):
    return Path(root) / "pages" / page_id / "render" / "page.html"
