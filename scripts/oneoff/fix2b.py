from pathlib import Path
base = Path("/home/bons/evops/docs/40-submit/split")
p2 = (base/"part02_deliver.html").read_text(encoding="utf-8")
idx = p2.find("誰が（何が）使うか")
ts = p2.rfind("<tr>", 0, idx)
rows=[]; i=ts
for j in range(4):
    te = p2.find("</tr>", i)
    rows.append(p2[i:te+5]); i = te+5
old = "".join(rows)
new = "<tr><td>誰が（何が）使うか</td><td><span class=\"fill\">AI画像生成クリエイター</span></td></tr><tr><td>どこから使うか</td><td><span class=\"fill\">デスクトップ（ローカル）アプリ</span></td></tr><tr><td>自動で動くか</td><td><span class=\"fill\">評価・修復ループは自動実行</span></td></tr><tr><td>システム名は何か</td><td><span class=\"fill\">AI評価・修復ループ</span></td></tr>"
p2 = p2.replace(old, new)
(base/"part02_deliver.html").write_text(p2, encoding="utf-8")
print("ok")
