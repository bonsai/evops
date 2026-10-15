# editor-pm — 編集者の進行管理エージェント

提出デッキ（`docs/40-submit`）を**1ページ＝1フォルダ**で管理し、
どのページが PASS / FAIL / HOLD / NOT_RUN かを台帳から判定する。

進行の原則はひとつ。**PASS していないページが残る限り、次のページには進まない。**

## 何をするか

| コマンド | 内容 |
|---|---|
| `index` | 原本 HTML を走査して台帳 `page-tests/pages.csv` を作る |
| `index --scaffold` | 各ページのフォルダと `content.json` / `test.json` の雛形を作る |
| `status` | 全ページの判定と進捗（PASS 数 / 総数）を出す |
| `next` | 次に着手すべき 1 ページと、その手順を出す |
| `show <page_id>` | 1 ページの台帳行と `test.json` を出す |

```bash
python3 agents/editor-pm/cli.py index --scaffold
python3 agents/editor-pm/cli.py status
python3 agents/editor-pm/cli.py next
```

## 編集者の順番

`next` は台帳の順に機械的に先頭を返すのではない。編集者の手順で選ぶ。

1. **着手済み**（FAIL / HOLD）のページを先に消化する
2. そのうえで**未着手**（NOT_RUN）の先頭を開く
3. 扉ページ（`kind=divider`）は本文の品質ゲート対象外なので飛ばす

## 判定を捏造しない

このツールは**判定をしない**。判定は次の 3 つが行う。

- `page-tests/render_page.py` — 既存 CSS で対象 section だけを A4 横に描画
- ヘッドレス Chrome — 実スクリーンショット
- `page-tests/vlm_judge.py` — LM Studio のローカル VLM による目視判定

`editor-pm` はそれらが `test.json` に書いた**事実だけ**を読む。
`test.json` が無ければ `NOT_RUN`。`gates` に BLOCKED / NOT_RUN が残っていれば HOLD。
未実行を PASS に読み替えることはしない。

## ページ番号（page_id の頭の数字）

`page_id` は必ず番号で始まる。`p<番号>-<slug>`。

- 番号は**その紙に印刷されているページ番号**（`hd-no`）。
- 印刷番号を持たない紙（表紙・扉）は**物理順**で採番する。
  表紙は `p01-cover`、検討項目扉は空いている `03` をとって `p03-study-divider`。
- 納品物扉は印刷番号を持たず、`p10` は本文（提出物一覧）が使っている。
  そこで `p10-deliverables-divider` として物理順のまま置く。
  この1組だけ `ls` の並びが紙の順と入れ替わる（p10-deliverables-checklist が先）。
  並びの正は台帳の `order` 列。扉は品質ゲートの対象外なので実害はない。
- 読み替えが必要な例外は `cli.py` の `ALIASES` にだけ書く。

## 管理対象の原本

`cli.py` の `DEFAULT_PARTS` が原本。順序がそのままページ順。

```python
DEFAULT_PARTS = ["part01_plan.html", "part02_deliver.html"]
```

発表パート（`index.html` 内にのみ存在）を足すときは `--parts` で指定する。

## 成果物の契約

```
docs/40-submit/page-tests/
├── pages.csv                      # 台帳（進行管理の唯一の真実）
├── render_page.py                 # 描画ハーネス
├── vlm_judge.py                   # VLM 判定
└── <page_id>/
    ├── content.json               # 内容（人が埋める）
    ├── test.json                  # 判定記録（未実行を PASS にしない）
    └── render/
        ├── page.html              # 既存 CSS で描いた 1 ページ
        ├── page.png               # 実スクリーンショット
        └── vlm_judgment.json      # VLM の生の返答
```
